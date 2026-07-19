# Japanese Mahjong Score Calculator Backend

A small Python backend for calculating Japanese riichi mahjong hand payments.

The backend uses a small Python virtual environment and the `mahjong` riichi
scoring library.

## Run the API

```bash
python -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m mahjong_score.api
```

The backend starts at:

```text
http://127.0.0.1:8005
```

## Run the React Frontend

In another terminal:

```bash
cd frontend
npm install
npm run dev
```

The frontend starts at:

```text
http://127.0.0.1:5173
```

## Run with Docker Compose

Build and start both services:

```bash
docker compose up --build
```

The frontend is served at:

```text
http://127.0.0.1:5173
```

The backend API is exposed at:

```text
http://127.0.0.1:8005
```

For another public API URL, set `VITE_API_BASE_URL` before building the
frontend image:

```bash
VITE_API_BASE_URL=https://api.example.com docker compose up --build
```

## Main App Flow

The React frontend lets users tap their winning hand tiles, choose the winning
tile and win context, optionally mark called groups and dora indicators, then
receive han, fu, yaku, payment, and fu details.

## Endpoints

### Health check

```bash
curl http://127.0.0.1:8005/health
```

### Supported rules

```bash
curl http://127.0.0.1:8005/rules
```

### Score a hand from tiles

```bash
curl -X POST http://127.0.0.1:8005/score-hand \
  -H "Content-Type: application/json" \
  -d '{
    "tiles": ["2m", "2m", "4m", "4m", "4m", "3p", "3p", "3p", "5p", "6p", "7p", "4s", "4s", "4s"],
    "winning_tile": "4s",
    "win_type": "ron",
    "winner_seat": "south",
    "round_wind": "east",
    "conditions": { "riichi": true }
  }'
```

### Advanced manual han/fu calculation

```bash
curl -X POST http://127.0.0.1:8005/calculate \
  -H "Content-Type: application/json" \
  -d '{
    "han": 3,
    "fu": 40,
    "win_type": "ron",
    "winner_seat": "non_dealer"
  }'
```

Example response:

```json
{
  "han": 3,
  "fu": 40,
  "win_type": "ron",
  "winner_seat": "non_dealer",
  "honba": 0,
  "riichi_sticks": 0,
  "yakuman_count": 0,
  "base_points": 1280,
  "limit": "no limit",
  "payments": {
    "discarder": 5200
  },
  "riichi_bonus": 0,
  "total_points": 5200,
  "display": "5200"
}
```

For a frontend-focused contract with request tables, response shapes, error
examples, and JavaScript fetch usage, see [API.md](API.md).

## Request Fields

- `han`: hand han value.
- `fu`: hand fu value.
- `win_type`: `ron` or `tsumo`.
- `winner_seat`: `dealer` or `non_dealer`.
- `honba`: optional repeat counter. Defaults to `0`.
- `riichi_sticks`: optional 1000-point sticks on table. Defaults to `0`.
- `yakuman_count`: optional yakuman multiplier. Defaults to `0`.

For yakuman hands in the manual endpoint, set `yakuman_count` and use `0` for
`han` and `fu`.

## Rules Included

- Normal fu and han scoring.
- Mangan, haneman, baiman, sanbaiman, kazoe yakuman, and yakuman limits.
- Dealer and non-dealer ron payments.
- Dealer and non-dealer tsumo payments.
- Honba bonus.
- Riichi stick bonus.

The main `/score-hand` endpoint detects yaku and fu from tiles. The advanced
`/calculate` endpoint assumes already-calculated `han` and `fu`.

## Run Tests

```bash
.venv/bin/python -m unittest discover -s tests
cd frontend
npm run build
npm run test:e2e
```
