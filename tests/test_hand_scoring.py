import unittest

from mahjong_score.hand_scoring import score_hand_from_data


class HandScoringTests(unittest.TestCase):
    def test_scores_closed_riichi_tanyao_ron(self):
        result = score_hand_from_data(
            {
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
        )

        self.assertTrue(result["is_valid"])
        self.assertEqual(result["han"], 2)
        self.assertEqual(result["fu"], 40)
        self.assertEqual(result["display"], "2600")
        self.assertEqual([yaku["name"] for yaku in result["yaku"]], ["Riichi", "Tanyao"])

    def test_scores_pinfu_tsumo(self):
        result = score_hand_from_data(
            {
                "tiles": [
                    "2m",
                    "3m",
                    "4m",
                    "7m",
                    "8m",
                    "9m",
                    "1p",
                    "2p",
                    "3p",
                    "4p",
                    "5p",
                    "6p",
                    "6p",
                    "6p",
                ],
                "winning_tile": "6p",
                "win_type": "tsumo",
                "winner_seat": "south",
                "round_wind": "east",
                "conditions": {"riichi": True},
            }
        )

        self.assertTrue(result["is_valid"])
        self.assertEqual(result["han"], 3)
        self.assertEqual(result["fu"], 20)
        self.assertEqual(result["display"], "700 / 1300")

    def test_scores_yakuman(self):
        result = score_hand_from_data(
            {
                "tiles": [
                    "1m",
                    "9m",
                    "1p",
                    "9p",
                    "1s",
                    "9s",
                    "1z",
                    "2z",
                    "3z",
                    "4z",
                    "5z",
                    "6z",
                    "7z",
                    "1m",
                ],
                "winning_tile": "1m",
                "win_type": "ron",
                "winner_seat": "east",
                "round_wind": "east",
            }
        )

        self.assertTrue(result["is_valid"])
        self.assertIn("Kokushi", result["yaku"][0]["name"])
        self.assertEqual(result["payments"], {"discarder": 96000})

    def test_explains_not_winning_hand(self):
        result = score_hand_from_data(
            {
                "tiles": [
                    "1m",
                    "2m",
                    "3m",
                    "4m",
                    "5m",
                    "6m",
                    "7m",
                    "8m",
                    "9m",
                    "1p",
                    "2p",
                    "3p",
                    "4p",
                    "5p",
                ],
                "winning_tile": "5p",
                "win_type": "ron",
                "winner_seat": "south",
                "round_wind": "east",
            }
        )

        self.assertFalse(result["is_valid"])
        self.assertIn("complete winning hand", result["errors"][0])

    def test_rejects_five_copies(self):
        result = score_hand_from_data(
            {
                "tiles": [
                    "1m",
                    "1m",
                    "1m",
                    "1m",
                    "1m",
                    "2m",
                    "3m",
                    "4m",
                    "5m",
                    "6m",
                    "7m",
                    "8m",
                    "9m",
                    "1p",
                ],
                "winning_tile": "1p",
                "win_type": "ron",
                "winner_seat": "south",
                "round_wind": "east",
            }
        )

        self.assertFalse(result["is_valid"])
        self.assertIn("more than four", result["errors"][0])


if __name__ == "__main__":
    unittest.main()
