from card import SetCard
from color import SetColor
from shading import SetShading
from shape import SetShape

class SetDeck(object):

    def __init__(self):
        self.cards = []
        # Borrowed from the test code that proves we can
        # generate all the cards:
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
                        self.cards.append(card)
