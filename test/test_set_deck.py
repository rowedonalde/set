import unittest

from setgame import SetDeck

class TestSetGameDeck(unittest.TestCase):

    def test_create_deck_generates_all_cards(self):
        deck = SetDeck()

        self.assertEqual(3**4, len(deck.cards))

    def test_create_deck_generates_unique_cards(self):
        deck = SetDeck()

        encodings = set([card.encoding for card in deck.cards])

        self.assertEqual(3**4, len(encodings))
