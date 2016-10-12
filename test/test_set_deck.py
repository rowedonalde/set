import unittest

from setgame import DeckEmpty, SetDeck

class TestSetGameDeck(unittest.TestCase):

    def setUp(self):
        # "System Under Test," i.e., the deck:
        self.SUT = SetDeck()

    def test_create_deck_generates_all_cards(self):
        self.assertEqual(3**4, len(self.SUT.cards))

    def test_create_deck_generates_unique_cards(self):
        self.assertEqual(3**4, len(self.SUT.cards_by_encoding))

    def test_deck_draw_random_removes_card(self):
        card = self.SUT.draw_random()

        self.assertNotIn(card, self.SUT.cards)
        self.assertNotIn(card.encoding, self.SUT.cards_by_encoding)

    def test_deck_draw_random_raises_DeckEmpty_when_no_cards_left(self):
        self.SUT.cards_by_encoding = {}

        with self.assertRaises(DeckEmpty):
            self.SUT.draw_random()
