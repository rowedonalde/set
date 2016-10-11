import unittest

from setgame import SetBoard, SetCard, SetDeck, SetHand
from setgame import SetColor, SetShading, SetShape

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

    def test_board_derives_third_encoding_in_set(self):
        card1 = SetCard(
            count=1,
            color=SetColor.red,
            shading=SetShading.empty,
            shape=SetShape.squiggles
        )
        encoding1 = card1.encoding

        card2 = SetCard(
            count=2,
            color=SetColor.green,
            shading=SetShading.striped,
            shape=SetShape.oval
        )
        encoding2 = card2.encoding

        card3 = SetCard(
            count=3,
            color=SetColor.purple,
            shading=SetShading.solid,
            shape=SetShape.diamond
        )
        encoding3 = card3.encoding

        # These all match:
        hand = SetHand(card1, card2, card3)
        self.assertTrue(hand.is_set())

        generated_third_encoding = SetBoard.missing_encoding_from(
            encoding1,
            encoding2
        )

        self.assertEqual(encoding3, generated_third_encoding)
