import unittest

from setgame import SetBoard, SetDeck

class TestSetGameBoard(unittest.TestCase):

    def setUp(self):
        self.deck = SetDeck()

        # "System Under Test," i.e., the board:
        self.SUT = SetBoard(self.deck)

    def test_board_init_leaves_cards_be(self):
        self.assertEqual(81, len(self.deck.cards))
        self.assertEqual(0, len(self.SUT.cards))

    def test_board_setup_uniquely_puts_cards_on_board(self):
        self.SUT.setup()

        self.assertEqual(12, len(self.SUT.cards))
        self.assertEqual(69, len(self.deck.cards))

        for card in self.SUT.cards_by_encoding:
            self.assertNotIn(card, self.deck.cards_by_encoding)

    def test_board_draw_from_deck_draws_uniquely(self):
        card = self.SUT.draw_from_deck()

        self.assertEqual(card, self.SUT.cards_by_encoding[card.encoding])
        self.assertEqual(80, len(self.deck.cards))
        self.assertNotIn(card, self.deck.cards)
