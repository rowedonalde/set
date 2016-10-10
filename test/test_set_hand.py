import unittest

from setgame import SetCard, SetHand, SetColor, SetShading, SetShape

class TestSetGameHand(unittest.TestCase):

    def test_create_hand_holds_onto_cards(self):
        card1 = SetCard(
            count=1,
            color=SetColor.green,
            shading=SetShading.solid,
            shape=SetShape.diamond
        )

        card2 = SetCard(
            count=2,
            color=SetColor.green,
            shading=SetShading.solid,
            shape=SetShape.diamond
        )

        card3 = SetCard(
            count=3,
            color=SetColor.green,
            shading=SetShading.solid,
            shape=SetShape.diamond
        )

        hand = SetHand(card1, card2, card3)

        self.assertEqual(3, len(hand.cards))

        for card in (card1, card2, card3):
            self.assertIn(card, hand.cards)
