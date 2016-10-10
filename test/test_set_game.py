import unittest

from setgame import SetCard, SetColor, SetShading, SetShape

class TestSetGameCard(unittest.TestCase):

    def test_create_card_exhaustive(self):
        # There are 3^4=81 possible cards, so why not make sure
        # we can make them all?
        total = 0

        for count in range(1, 3 + 1):
            for color in SetColor:
                for shading in SetShading:
                    for shape in SetShape:
                        card = SetCard(
                            count=count,
                            color=color,
                            shading=shading,
                            shape=shape
                        )

                        self.assertEqual(count, card.count)
                        self.assertEqual(color, card.color)
                        self.assertEqual(shading, card.shading)
                        self.assertEqual(shape, card.shape)
                        total += 1

        self.assertEqual(3**4, total)

    def test_create_card_input_does_not_allow_count_under_1(self):
        with self.assertRaises(ValueError):
            card = SetCard(
                count=0,
                color=SetColor.red,
                shading=SetShading.solid,
                shape=SetShape.squiggles
            )

    def test_create_card_input_does_not_allow_count_over_3(self):
        with self.assertRaises(ValueError):
            card = SetCard(
                count=4,
                color=SetColor.red,
                shading=SetShading.solid,
                shape=SetShape.squiggles
            )

    def test_create_card_input_color_must_be_SetColor(self):
        with self.assertRaises(TypeError):
            card = SetCard(
                count=1,
                color='red',
                shading=SetShading.solid,
                shape=SetShape.squiggles
            )

    def test_create_card_input_shading_must_be_SetShading(self):
        with self.assertRaises(TypeError):
            card = SetCard(
                count=1,
                color=SetColor.red,
                shading=1,
                shape=SetShape.squiggles
            )

    def test_create_card_input_shape_must_be_SetShape(self):
        with self.assertRaises(TypeError):
            card = SetCard(
                count=1,
                color=SetColor.red,
                shading=SetShading.solid,
                shape=None
            )
