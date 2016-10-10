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

    def test_hand_is_set_when_all_attributes_different(self):
        card1 = SetCard(
            count=1,
            color=SetColor.red,
            shading=SetShading.solid,
            shape=SetShape.squiggles
        )

        card2 = SetCard(
            count=2,
            color=SetColor.green,
            shading=SetShading.empty,
            shape=SetShape.diamond
        )

        card3 = SetCard(
            count=3,
            color=SetColor.purple,
            shading=SetShading.striped,
            shape=SetShape.oval
        )

        hand = SetHand(card1, card2, card3)

        self.assertTrue(hand.is_set())

    def test_hand_is_set_with_mixture_of_all_different_and_all_same(self):
        card1 = SetCard(
            count=1,
            color=SetColor.red,
            shading=SetShading.solid,
            shape=SetShape.squiggles
        )

        card2 = SetCard(
            count=1,
            color=SetColor.green,
            shading=SetShading.empty,
            shape=SetShape.diamond
        )

        card3 = SetCard(
            count=1,
            color=SetColor.purple,
            shading=SetShading.striped,
            shape=SetShape.oval
        )

        hand = SetHand(card1, card2, card3)

        self.assertTrue(hand.is_set())

    def test_hand_is_not_set_when_some_attribute_is_neither_all_different_or_all_same(self):
        card1 = SetCard(
            count=1,
            color=SetColor.red,
            shading=SetShading.solid,
            shape=SetShape.squiggles
        )

        card2 = SetCard(
            count=1,
            color=SetColor.green,
            shading=SetShading.empty,
            shape=SetShape.diamond
        )

        card3 = SetCard(
            count=3,
            color=SetColor.purple,
            shading=SetShading.striped,
            shape=SetShape.oval
        )

        hand = SetHand(card1, card2, card3)

        self.assertFalse(hand.is_set())
