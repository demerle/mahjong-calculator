import json
import threading
import unittest
from http.server import HTTPServer
from urllib.error import HTTPError
from urllib.request import Request
from urllib.request import urlopen

from mahjong_score.api import MahjongScoreHandler


class ApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = HTTPServer(("127.0.0.1", 0), MahjongScoreHandler)
        cls.port = cls.server.server_address[1]
        cls.thread = threading.Thread(target=cls.server.serve_forever)
        cls.thread.daemon = True
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.thread.join()
        cls.server.server_close()

    def test_health_endpoint(self):
        with urlopen(f"http://127.0.0.1:{self.port}/health") as response:
            data = json.loads(response.read().decode("utf-8"))

            self.assertEqual(response.status, 200)
        self.assertEqual(data, {"status": "ok"})

    def test_calculate_endpoint(self):
        payload = {
            "han": 3,
            "fu": 40,
            "win_type": "ron",
            "winner_seat": "non_dealer",
        }
        request = Request(
            f"http://127.0.0.1:{self.port}/calculate",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with urlopen(request) as response:
            data = json.loads(response.read().decode("utf-8"))

            self.assertEqual(response.status, 200)
        self.assertEqual(data["payments"], {"discarder": 5200})

    def test_options_endpoint_supports_cors_preflight(self):
        request = Request(
            f"http://127.0.0.1:{self.port}/calculate",
            method="OPTIONS",
        )

        with urlopen(request) as response:
            self.assertEqual(response.status, 204)
            self.assertEqual(response.headers["Access-Control-Allow-Origin"], "*")
            self.assertIn("POST", response.headers["Access-Control-Allow-Methods"])

    def test_calculate_endpoint_returns_validation_error(self):
        payload = {
            "han": 2,
            "fu": 28,
            "win_type": "ron",
            "winner_seat": "non_dealer",
        }
        request = Request(
            f"http://127.0.0.1:{self.port}/calculate",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with self.assertRaises(HTTPError) as error:
            urlopen(request)

        with error.exception as response:
            data = json.loads(response.read().decode("utf-8"))
            self.assertEqual(response.code, 400)
        self.assertIn("fu must be", data["error"])

    def test_score_hand_endpoint(self):
        payload = {
            "tiles": [
                "2m",
                "2m",
                "4m",
                "4m",
                "4m",
                "3p",
                "3p",
                "3p",
                "5p",
                "6p",
                "7p",
                "4s",
                "4s",
                "4s",
            ],
            "winning_tile": "4s",
            "win_type": "ron",
            "winner_seat": "south",
            "round_wind": "east",
            "conditions": {"riichi": True},
        }
        request = Request(
            f"http://127.0.0.1:{self.port}/score-hand",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with urlopen(request) as response:
            data = json.loads(response.read().decode("utf-8"))

            self.assertEqual(response.status, 200)
        self.assertTrue(data["is_valid"])
        self.assertEqual(data["display"], "2600")

    def test_rules_endpoint_has_hand_metadata(self):
        with urlopen(f"http://127.0.0.1:{self.port}/rules") as response:
            data = json.loads(response.read().decode("utf-8"))

            self.assertEqual(response.status, 200)
        self.assertIn("hand_scoring", data)
        self.assertIn("tile_groups", data["hand_scoring"])


if __name__ == "__main__":
    unittest.main()
