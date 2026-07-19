# API Documentation

Frontend contract for the Japanese riichi mahjong calculator backend.

## Base URL

```text
http://127.0.0.1:8005
```

CORS is enabled for local frontend development.

## Primary Endpoint: `POST /score-hand`

Calculates score from entered tiles and win context. This is the endpoint the frontend should use.

### Request

```json
{
  "tiles": ["2m", "2m", "4m", "4m", "4m", "3p", "3p", "3p", "5p", "6p", "7p", "4s", "4s", "4s"],
  "winning_tile": "4s",
  "win_type": "ron",
  "winner_seat": "south",
  "round_wind": "east",
  "melds": [],
  "dora_indicators": [],
  "ura_dora_indicators": [],
  "conditions": {
    "riichi": true
  },
  "honba": 0,
  "riichi_sticks": 0,
  "rules": {
    "has_aka_dora": true,
    "has_open_tanyao": false,
    "has_double_yakuman": true
  }
}
```

### Tile IDs

- Suits: `1m`-`9m`, `1p`-`9p`, `1s`-`9s`.
- Red fives: `0m`, `0p`, `0s`.
- Honors: `1z` east, `2z` south, `3z` west, `4z` north, `5z` white, `6z` green, `7z` red.

### Melds

```json
{
  "type": "pon",
  "tiles": ["5z", "5z", "5z"]
}
```

Accepted `type` values: `chi`, `pon`, `kan`, `closed_kan`.

### Success Response `200`

```json
{
  "is_valid": true,
  "errors": [],
  "warnings": [],
  "han": 2,
  "fu": 40,
  "limit": "no limit",
  "base_points": null,
  "win_type": "ron",
  "winner_seat": "south",
  "round_wind": "east",
  "honba": 0,
  "riichi_sticks": 0,
  "payments": {
    "discarder": 2600
  },
  "riichi_bonus": 0,
  "total_points": 2600,
  "display": "2600",
  "yaku": [
    {
      "name": "Riichi",
      "han": 1,
      "is_yakuman": false
    },
    {
      "name": "Tanyao",
      "han": 1,
      "is_yakuman": false
    }
  ],
  "fu_details": []
}
```

### Error Response `400`

```json
{
  "is_valid": false,
  "errors": [
    "Those tiles do not form a complete winning hand. Check the winning tile and any called groups."
  ],
  "warnings": [],
  "han": null,
  "fu": null,
  "limit": null,
  "payments": {},
  "display": "",
  "yaku": [],
  "fu_details": []
}
```

## Metadata: `GET /rules`

Returns endpoint descriptions, tile groups, winds, meld types, supported conditions, and default rules.

## Health: `GET /health`

```json
{
  "status": "ok"
}
```

## Advanced Manual Endpoint: `POST /calculate`

The old endpoint still calculates from known `han` and `fu`. Keep it for advanced/manual use, but do not use it as the main beginner frontend workflow.
