import unittest

from setgame import SetRunner

class TestSetRunner(unittest.TestCase):

    def test_set_runner_deck_is_empty_after_game(self):
        runner = SetRunner()
        self.assertEqual(81, len(runner.deck.cards))

        runner.play()

        self.assertEqual(0, len(runner.deck.cards))
        self.assertEqual(81, len(runner.board.cards) + len(runner.board.graveyard))
