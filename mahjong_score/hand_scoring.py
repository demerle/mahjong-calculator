from collections import Counter
from dataclasses import dataclass

from mahjong import constants
from mahjong.hand_calculating.hand import HandCalculator
from mahjong.hand_calculating.hand_config import HandConfig
from mahjong.hand_calculating.hand_config import OptionalRules
from mahjong.meld import Meld


SUIT_OFFSETS = {"m": 0, "p": 9, "s": 18, "z": 27}
WIND_VALUES = {
    "east": constants.EAST,
    "south": constants.SOUTH,
    "west": constants.WEST,
    "north": constants.NORTH,
}
MELD_TYPES = {
    "chi": Meld.CHI,
    "pon": Meld.PON,
    "kan": Meld.KAN,
    "closed_kan": Meld.KAN,
}
RED_FIVE_136 = {"0m": constants.FIVE_RED_MAN, "0p": constants.FIVE_RED_PIN, "0s": constants.FIVE_RED_SOU}


@dataclass
class HandScoreRequest:
    tiles: list[str]
    winning_tile: str
    win_type: str
    winner_seat: str
    round_wind: str
    melds: list
    dora_indicators: list[str]
    ura_dora_indicators: list[str]
    conditions: dict
    honba: int
    riichi_sticks: int
    rules: dict


def score_hand_from_data(data):
    request = make_hand_score_request(data)
    errors = validate_hand_score_request(request)
    if errors:
        return make_error_response(errors)

    has_aka_dora = bool(request.rules.get("has_aka_dora", True))
    melds = make_melds(request.melds, set(), has_aka_dora)
    tiles = make_complete_tiles(request, set(), has_aka_dora)
    win_tile = find_winning_tile(request.winning_tile, tiles)
    dora_indicators = tile_ids_to_136(request.dora_indicators, set(), has_aka_dora)
    ura_dora_indicators = tile_ids_to_136(request.ura_dora_indicators, set(), has_aka_dora)
    config = make_hand_config(request)

    if win_tile is None:
        return make_error_response(["Winning tile must be one of the entered hand tiles."])

    result = HandCalculator.estimate_hand_value(
        tiles,
        win_tile,
        melds=melds,
        dora_indicators=dora_indicators,
        ura_dora_indicators=ura_dora_indicators,
        config=config,
    )

    if result.error:
        return make_error_response([make_beginner_error(result.error)], tiles=request.tiles)

    return make_success_response(result, request)


def make_hand_score_request(data):
    tiles = data.get("tiles")
    if tiles is None:
        tiles = list(data.get("closed_tiles", []))
        winning_tile = data.get("winning_tile")
        if winning_tile and winning_tile not in tiles:
            tiles.append(winning_tile)
        for meld in data.get("melds", []):
            tiles.extend(meld.get("tiles", []))

    return HandScoreRequest(
        tiles=list(tiles or []),
        winning_tile=str(data.get("winning_tile", "")),
        win_type=str(data.get("win_type", "")),
        winner_seat=str(data.get("winner_seat", "")),
        round_wind=str(data.get("round_wind", "")),
        melds=list(data.get("melds", [])),
        dora_indicators=list(data.get("dora_indicators", [])),
        ura_dora_indicators=list(data.get("ura_dora_indicators", [])),
        conditions=dict(data.get("conditions", {})),
        honba=int(data.get("honba", 0)),
        riichi_sticks=int(data.get("riichi_sticks", 0)),
        rules=dict(data.get("rules", {})),
    )


def validate_hand_score_request(request):
    errors = []

    if request.win_type not in ("ron", "tsumo"):
        errors.append("Choose whether the hand won by ron or tsumo.")

    if request.winner_seat not in WIND_VALUES:
        errors.append("Choose the winner seat wind.")

    if request.round_wind not in WIND_VALUES:
        errors.append("Choose the round wind.")

    if not request.winning_tile:
        errors.append("Choose the winning tile.")

    if request.honba < 0:
        errors.append("Honba must be 0 or more.")

    if request.riichi_sticks < 0:
        errors.append("Riichi sticks must be 0 or more.")

    all_tile_ids = list(request.tiles)
    all_tile_ids.extend(request.dora_indicators)
    all_tile_ids.extend(request.ura_dora_indicators)
    for meld in request.melds:
        all_tile_ids.extend(meld.get("tiles", []))

    invalid_tiles = [tile_id for tile_id in all_tile_ids if not is_valid_tile_id(tile_id)]
    if invalid_tiles:
        errors.append(f"Invalid tile id: {invalid_tiles[0]}.")

    hand_counts = Counter(normal_tile_id(tile_id) for tile_id in request.tiles)
    if any(count > 4 for count in hand_counts.values()):
        errors.append("A hand cannot contain more than four copies of the same tile.")

    hand_tile_count = len(request.tiles)
    if hand_tile_count not in (14, 15, 16, 17, 18):
        errors.append("Enter 14 tiles for a normal winning hand. Kans add one extra tile each.")

    for meld in request.melds:
        meld_type = meld.get("type")
        meld_tiles = meld.get("tiles", [])
        if meld_type not in MELD_TYPES:
            errors.append("Each called group must be chi, pon, kan, or closed_kan.")
        if meld_type in ("chi", "pon") and len(meld_tiles) != 3:
            errors.append("Chi and pon groups must have exactly 3 tiles.")
        if meld_type in ("kan", "closed_kan") and len(meld_tiles) != 4:
            errors.append("Kan groups must have exactly 4 tiles.")

    return errors


def is_valid_tile_id(tile_id):
    if not isinstance(tile_id, str) or len(tile_id) != 2:
        return False

    rank = tile_id[0]
    suit = tile_id[1]
    if suit in ("m", "p", "s"):
        return rank in "0123456789" and rank != "0" or tile_id in RED_FIVE_136
    if suit == "z":
        return rank in "1234567"
    return False


def normal_tile_id(tile_id):
    if tile_id in RED_FIVE_136:
        return "5" + tile_id[1]
    return tile_id


def tile_id_to_34(tile_id):
    tile_id = normal_tile_id(tile_id)
    rank = int(tile_id[0])
    suit = tile_id[1]
    return SUIT_OFFSETS[suit] + rank - 1


def tile_ids_to_136(tile_ids, used_tiles, has_aka_dora):
    return [tile_id_to_136(tile_id, used_tiles, has_aka_dora) for tile_id in tile_ids]


def tile_id_to_136(tile_id, used_tiles, has_aka_dora):
    if has_aka_dora and tile_id in RED_FIVE_136 and RED_FIVE_136[tile_id] not in used_tiles:
        tile = RED_FIVE_136[tile_id]
        used_tiles.add(tile)
        return tile

    tile34 = tile_id_to_34(tile_id)
    base = tile34 * 4
    candidates = [base, base + 1, base + 2, base + 3]

    if tile_id[0] == "5" and tile_id[1] in ("m", "p", "s"):
        red_tile = RED_FIVE_136["0" + tile_id[1]]
        candidates = [tile for tile in candidates if tile != red_tile] + [red_tile]

    for tile in candidates:
        if tile not in used_tiles:
            used_tiles.add(tile)
            return tile

    raise ValueError(f"Too many copies of {normal_tile_id(tile_id)}.")


def make_melds(raw_melds, used_tiles, has_aka_dora):
    melds = []
    for raw_meld in raw_melds:
        meld_type = raw_meld.get("type")
        tiles = tile_ids_to_136(raw_meld.get("tiles", []), used_tiles, has_aka_dora)
        opened = meld_type != "closed_kan"
        melds.append(Meld(meld_type=MELD_TYPES[meld_type], tiles=tiles, opened=opened))
    return melds


def make_complete_tiles(request, used_tiles, has_aka_dora):
    try:
        return tile_ids_to_136(request.tiles, used_tiles, has_aka_dora)
    except ValueError:
        return []


def find_winning_tile(winning_tile_id, tiles):
    tile34 = tile_id_to_34(winning_tile_id)
    for tile in tiles:
        if tile // 4 == tile34:
            return tile
    return None


def make_hand_config(request):
    conditions = request.conditions
    options = OptionalRules(
        has_open_tanyao=bool(request.rules.get("has_open_tanyao", False)),
        has_aka_dora=bool(request.rules.get("has_aka_dora", True)),
        has_double_yakuman=bool(request.rules.get("has_double_yakuman", True)),
    )

    return HandConfig(
        is_tsumo=request.win_type == "tsumo",
        is_riichi=bool(conditions.get("riichi", False)),
        is_daburu_riichi=bool(conditions.get("double_riichi", False)),
        is_ippatsu=bool(conditions.get("ippatsu", False)),
        is_rinshan=bool(conditions.get("rinshan", False)),
        is_chankan=bool(conditions.get("chankan", False)),
        is_haitei=bool(conditions.get("haitei", False)),
        is_houtei=bool(conditions.get("houtei", False)),
        is_tenhou=bool(conditions.get("tenhou", False)),
        is_chiihou=bool(conditions.get("chiihou", False)),
        player_wind=WIND_VALUES[request.winner_seat],
        round_wind=WIND_VALUES[request.round_wind],
        kyoutaku_number=request.riichi_sticks,
        tsumi_number=request.honba,
        options=options,
    )


def make_success_response(result, request):
    payments = make_payments(result.cost, request)
    limit = result.cost["yaku_level"] or "no limit"
    return {
        "is_valid": True,
        "errors": [],
        "warnings": [],
        "han": result.han,
        "fu": result.fu,
        "limit": limit,
        "base_points": None,
        "win_type": request.win_type,
        "winner_seat": request.winner_seat,
        "round_wind": request.round_wind,
        "honba": request.honba,
        "riichi_sticks": request.riichi_sticks,
        "payments": payments,
        "riichi_bonus": result.cost["kyoutaku_bonus"],
        "total_points": result.cost["total"],
        "display": make_display_text(request, payments),
        "yaku": make_yaku_list(result),
        "fu_details": result.fu_details or [],
    }


def make_payments(cost, request):
    if request.win_type == "ron":
        return {"discarder": cost["main"] + cost["main_bonus"]}

    if request.winner_seat == "east":
        return {"each_non_dealer": cost["main"] + cost["main_bonus"]}

    return {
        "dealer": cost["main"] + cost["main_bonus"],
        "each_non_dealer": cost["additional"] + cost["additional_bonus"],
    }


def make_display_text(request, payments):
    if request.win_type == "ron":
        return str(payments["discarder"])
    if request.winner_seat == "east":
        return f"{payments['each_non_dealer']} all"
    return f"{payments['each_non_dealer']} / {payments['dealer']}"


def make_yaku_list(result):
    yaku_list = []
    for yaku in result.yaku or []:
        han = yaku.han_open if result.is_open_hand else yaku.han_closed
        if yaku.is_yakuman:
            han = 13 if han == 0 else han
        yaku_list.append({"name": yaku.name, "han": han, "is_yakuman": yaku.is_yakuman})
    return yaku_list


def make_error_response(errors, tiles=None):
    return {
        "is_valid": False,
        "errors": errors,
        "warnings": [],
        "han": None,
        "fu": None,
        "limit": None,
        "base_points": None,
        "payments": {},
        "riichi_bonus": 0,
        "total_points": 0,
        "display": "",
        "yaku": [],
        "fu_details": [],
        "tiles": tiles or [],
    }


def make_beginner_error(error):
    lower_error = str(error).lower()
    if "hand is not winning" in lower_error or "hand_not_winning" in lower_error:
        return "Those tiles do not form a complete winning hand. Check the winning tile and any called groups."
    if "there are no yaku" in lower_error or "no yaku" in lower_error or "no_yaku" in lower_error:
        return "The hand shape is complete, but it has no yaku. Check riichi, tsumo, seat wind, round wind, dragons, or other conditions."
    if "winning tile" in lower_error:
        return "The winning tile must be included in the entered hand."
    return str(error)


def get_hand_rules():
    return {
        "tile_groups": {
            "manzu": [{"id": f"{rank}m", "label": f"{rank}m"} for rank in range(1, 10)],
            "pinzu": [{"id": f"{rank}p", "label": f"{rank}p"} for rank in range(1, 10)],
            "souzu": [{"id": f"{rank}s", "label": f"{rank}s"} for rank in range(1, 10)],
            "winds": [
                {"id": "1z", "label": "East"},
                {"id": "2z", "label": "South"},
                {"id": "3z", "label": "West"},
                {"id": "4z", "label": "North"},
            ],
            "dragons": [
                {"id": "5z", "label": "White"},
                {"id": "6z", "label": "Green"},
                {"id": "7z", "label": "Red"},
            ],
            "red_fives": [
                {"id": "0m", "label": "Red 5m"},
                {"id": "0p", "label": "Red 5p"},
                {"id": "0s", "label": "Red 5s"},
            ],
        },
        "win_types": ["ron", "tsumo"],
        "winds": ["east", "south", "west", "north"],
        "meld_types": ["chi", "pon", "kan", "closed_kan"],
        "conditions": [
            "riichi",
            "double_riichi",
            "ippatsu",
            "rinshan",
            "chankan",
            "haitei",
            "houtei",
            "tenhou",
            "chiihou",
        ],
        "default_rules": {
            "has_aka_dora": True,
            "has_open_tanyao": False,
            "has_double_yakuman": True,
        },
    }
