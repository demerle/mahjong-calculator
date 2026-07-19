import json
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer

from mahjong_score.scoring import ScoreRequest
from mahjong_score.scoring import calculate_score
from mahjong_score.hand_scoring import get_hand_rules
from mahjong_score.hand_scoring import score_hand_from_data


HOST = "127.0.0.1"
PORT = 8005


class MahjongScoreHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(204)
        self.send_cors_headers()
        self.end_headers()

    def do_GET(self):
        if self.path == "/health":
            self.send_json(200, {"status": "ok"})
            return

        if self.path == "/rules":
            self.send_json(200, get_rules())
            return

        self.send_json(404, {"error": "Not found"})

    def do_POST(self):
        if self.path == "/score-hand":
            self.handle_score_hand()
            return

        if self.path != "/calculate":
            self.send_json(404, {"error": "Not found"})
            return

        try:
            request_body = self.read_json_body()
            score_request = ScoreRequest(
                han=int(request_body.get("han", 0)),
                fu=int(request_body.get("fu", 0)),
                win_type=str(request_body.get("win_type", "")),
                winner_seat=str(request_body.get("winner_seat", "")),
                honba=int(request_body.get("honba", 0)),
                riichi_sticks=int(request_body.get("riichi_sticks", 0)),
                yakuman_count=int(request_body.get("yakuman_count", 0)),
            )
            result = calculate_score(score_request)
            self.send_json(200, result)
        except ValueError as error:
            self.send_json(400, {"error": str(error)})
        except json.JSONDecodeError:
            self.send_json(400, {"error": "Request body must be valid JSON"})

    def handle_score_hand(self):
        try:
            request_body = self.read_json_body()
            result = score_hand_from_data(request_body)
            if result["is_valid"]:
                self.send_json(200, result)
            else:
                self.send_json(400, result)
        except ValueError as error:
            self.send_json(400, {"error": str(error)})
        except json.JSONDecodeError:
            self.send_json(400, {"error": "Request body must be valid JSON"})

    def read_json_body(self):
        content_length = int(self.headers.get("Content-Length", 0))
        raw_body = self.rfile.read(content_length).decode("utf-8")
        if not raw_body:
            return {}
        return json.loads(raw_body)

    def send_json(self, status_code, data):
        response = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response)))
        self.send_cors_headers()
        self.end_headers()
        self.wfile.write(response)

    def send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def log_message(self, format, *args):
        return


def get_rules():
    return {
        "game": "Japanese riichi mahjong",
        "endpoints": {
            "GET /health": "Check that the backend is running.",
            "GET /rules": "Show supported scoring rules.",
            "POST /score-hand": "Calculate from entered tiles and win conditions.",
            "POST /calculate": "Calculate the payment for a winning hand.",
        },
        "hand_scoring": get_hand_rules(),
        "calculate_fields": {
            "han": "Integer han value. Use 0 if yakuman_count is set.",
            "fu": "Integer fu value. Use 0 if yakuman_count is set.",
            "win_type": "ron or tsumo.",
            "winner_seat": "dealer or non_dealer.",
            "honba": "Optional repeat counter. Default is 0.",
            "riichi_sticks": "Optional 1000-point sticks on table. Default is 0.",
            "yakuman_count": "Optional yakuman multiplier. Default is 0.",
        },
        "limits": [
            "mangan",
            "haneman",
            "baiman",
            "sanbaiman",
            "kazoe yakuman",
            "single or multiple yakuman",
        ],
    }


def run_server(host=HOST, port=PORT):
    server = HTTPServer((host, port), MahjongScoreHandler)
    print(f"Mahjong score backend running at http://{host}:{port}")
    print("Try GET /health, GET /rules, or POST /calculate")
    server.serve_forever()


if __name__ == "__main__":
    run_server()
