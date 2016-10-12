import unittest

from setgame import SetRunner

class TestSetRunner(unittest.TestCase):

    def test_set_runner_deck_is_empty_after_game(self):
        runner = SetRunner(quiet=True)
        self.assertEqual(81, len(runner.deck.cards))

        sets_found = runner.play()

        self.assertEqual(0, len(runner.deck.cards))
        self.assertEqual(81, len(runner.board.cards) + len(runner.board.graveyard))

        self.assertTrue(len(sets_found) > 0)

        total_cards = 3 * len(sets_found) + len(runner.board.cards)

        self.assertEqual(81, total_cards)
