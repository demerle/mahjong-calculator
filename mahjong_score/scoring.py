from dataclasses import dataclass


VALID_WIN_TYPES = ("ron", "tsumo")
VALID_WINNER_SEATS = ("dealer", "non_dealer")


@dataclass
class ScoreRequest:
    han: int
    fu: int
    win_type: str
    winner_seat: str
    honba: int = 0
    riichi_sticks: int = 0
    yakuman_count: int = 0


def round_up_to_hundred(points):
    return ((points + 99) // 100) * 100


def get_limit(base_points, han, yakuman_count):
    if yakuman_count > 0:
        if yakuman_count == 1:
            return "yakuman"
        return f"{yakuman_count}x yakuman"

    if han >= 13:
        return "kazoe yakuman"
    if han >= 11:
        return "sanbaiman"
    if han >= 8:
        return "baiman"
    if han >= 6:
        return "haneman"
    if han == 5 or base_points >= 2000:
        return "mangan"
    return "no limit"


def get_base_points(han, fu, yakuman_count):
    if yakuman_count > 0:
        return 8000 * yakuman_count

    if han >= 13:
        return 8000
    if han >= 11:
        return 6000
    if han >= 8:
        return 4000
    if han >= 6:
        return 3000

    base_points = fu * (2 ** (han + 2))

    if han == 5 or base_points >= 2000:
        return 2000

    return base_points


def validate_score_request(score_request):
    errors = []

    if score_request.win_type not in VALID_WIN_TYPES:
        errors.append("win_type must be 'ron' or 'tsumo'")

    if score_request.winner_seat not in VALID_WINNER_SEATS:
        errors.append("winner_seat must be 'dealer' or 'non_dealer'")

    if score_request.honba < 0:
        errors.append("honba must be 0 or more")

    if score_request.riichi_sticks < 0:
        errors.append("riichi_sticks must be 0 or more")

    if score_request.yakuman_count < 0:
        errors.append("yakuman_count must be 0 or more")

    if score_request.yakuman_count == 0:
        if score_request.han < 1:
            errors.append("han must be at least 1")
        if score_request.fu < 20:
            errors.append("fu must be at least 20")
        if score_request.fu % 10 != 0 and score_request.fu != 25:
            errors.append("fu must be 25 or a multiple of 10")
    else:
        if score_request.han < 0:
            errors.append("han must be 0 or more when yakuman_count is used")

    return errors


def calculate_score(score_request):
    errors = validate_score_request(score_request)
    if errors:
        raise ValueError("; ".join(errors))

    base_points = get_base_points(
        score_request.han,
        score_request.fu,
        score_request.yakuman_count,
    )
    limit = get_limit(base_points, score_request.han, score_request.yakuman_count)

    if score_request.win_type == "ron":
        payments = calculate_ron_payments(score_request, base_points)
    else:
        payments = calculate_tsumo_payments(score_request, base_points)

    riichi_bonus = score_request.riichi_sticks * 1000
    total_points = get_total_points(score_request, payments) + riichi_bonus

    return {
        "han": score_request.han,
        "fu": score_request.fu,
        "win_type": score_request.win_type,
        "winner_seat": score_request.winner_seat,
        "honba": score_request.honba,
        "riichi_sticks": score_request.riichi_sticks,
        "yakuman_count": score_request.yakuman_count,
        "base_points": base_points,
        "limit": limit,
        "payments": payments,
        "riichi_bonus": riichi_bonus,
        "total_points": total_points,
        "display": make_display_text(score_request, payments),
    }


def calculate_ron_payments(score_request, base_points):
    honba_bonus = score_request.honba * 300

    if score_request.winner_seat == "dealer":
        return {"discarder": round_up_to_hundred(base_points * 6) + honba_bonus}

    return {"discarder": round_up_to_hundred(base_points * 4) + honba_bonus}


def calculate_tsumo_payments(score_request, base_points):
    honba_bonus = score_request.honba * 100

    if score_request.winner_seat == "dealer":
        payment = round_up_to_hundred(base_points * 2) + honba_bonus
        return {"each_non_dealer": payment}

    dealer_payment = round_up_to_hundred(base_points * 2) + honba_bonus
    non_dealer_payment = round_up_to_hundred(base_points) + honba_bonus
    return {
        "dealer": dealer_payment,
        "each_non_dealer": non_dealer_payment,
    }


def get_total_points(score_request, payments):
    if score_request.win_type == "ron":
        return payments["discarder"]

    if score_request.winner_seat == "dealer":
        return payments["each_non_dealer"] * 3

    return payments["dealer"] + (payments["each_non_dealer"] * 2)


def make_display_text(score_request, payments):
    if score_request.win_type == "ron":
        return str(payments["discarder"])

    if score_request.winner_seat == "dealer":
        return f"{payments['each_non_dealer']} all"

    return f"{payments['each_non_dealer']} / {payments['dealer']}"
