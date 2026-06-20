import unittest

from mahjong_score.scoring import ScoreRequest
from mahjong_score.scoring import calculate_score


class ScoringTests(unittest.TestCase):
    def test_non_dealer_ron_basic_hand(self):
        request = ScoreRequest(
            han=3,
            fu=40,
            win_type="ron",
            winner_seat="non_dealer",
        )

        result = calculate_score(request)

        self.assertEqual(result["limit"], "no limit")
        self.assertEqual(result["payments"], {"discarder": 5200})
        self.assertEqual(result["display"], "5200")

    def test_dealer_ron_basic_hand(self):
        request = ScoreRequest(
            han=3,
            fu=40,
            win_type="ron",
            winner_seat="dealer",
        )

        result = calculate_score(request)

        self.assertEqual(result["payments"], {"discarder": 7700})

    def test_non_dealer_tsumo_basic_hand(self):
        request = ScoreRequest(
            han=3,
            fu=40,
            win_type="tsumo",
            winner_seat="non_dealer",
        )

        result = calculate_score(request)

        self.assertEqual(result["payments"]["dealer"], 2600)
        self.assertEqual(result["payments"]["each_non_dealer"], 1300)
        self.assertEqual(result["display"], "1300 / 2600")

    def test_dealer_tsumo_basic_hand(self):
        request = ScoreRequest(
            han=3,
            fu=40,
            win_type="tsumo",
            winner_seat="dealer",
        )

        result = calculate_score(request)

        self.assertEqual(result["payments"]["each_non_dealer"], 2600)
        self.assertEqual(result["total_points"], 7800)
        self.assertEqual(result["display"], "2600 all")

    def test_mangan_ron(self):
        request = ScoreRequest(
            han=5,
            fu=30,
            win_type="ron",
            winner_seat="non_dealer",
        )

        result = calculate_score(request)

        self.assertEqual(result["limit"], "mangan")
        self.assertEqual(result["payments"], {"discarder": 8000})

    def test_haneman_tsumo(self):
        request = ScoreRequest(
            han=6,
            fu=30,
            win_type="tsumo",
            winner_seat="non_dealer",
        )

        result = calculate_score(request)

        self.assertEqual(result["limit"], "haneman")
        self.assertEqual(result["display"], "3000 / 6000")

    def test_yakuman_dealer_ron(self):
        request = ScoreRequest(
            han=0,
            fu=0,
            win_type="ron",
            winner_seat="dealer",
            yakuman_count=1,
        )

        result = calculate_score(request)

        self.assertEqual(result["limit"], "yakuman")
        self.assertEqual(result["payments"], {"discarder": 48000})

    def test_honba_and_riichi_sticks(self):
        request = ScoreRequest(
            han=1,
            fu=30,
            win_type="ron",
            winner_seat="non_dealer",
            honba=2,
            riichi_sticks=1,
        )

        result = calculate_score(request)

        self.assertEqual(result["payments"], {"discarder": 1600})
        self.assertEqual(result["riichi_bonus"], 1000)
        self.assertEqual(result["total_points"], 2600)

    def test_invalid_fu_raises_error(self):
        request = ScoreRequest(
            han=2,
            fu=28,
            win_type="ron",
            winner_seat="non_dealer",
        )

        with self.assertRaises(ValueError):
            calculate_score(request)


if __name__ == "__main__":
    unittest.main()
