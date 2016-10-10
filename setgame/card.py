from color import SetColor
from shading import SetShading
from shape import SetShape

class SetCard(object):
    '''Represents a card in the Set card game.'''

    def __init__(self, count, color, shading, shape):
        if count < 1 or count > 3:
            raise ValueError('Count must be 1, 2, or 3.')

        self.count = count

        if color not in SetColor:
            raise TypeError(
                'color must be one of the values enumerated in SetColor'
            )

        self.color = color

        if shading not in SetShading:
            raise TypeError(
                'shading must be one of the values enumerated in SetShading'
            )

        self.shading = shading

        if shape not in SetShape:
            raise TypeError(
                'shape must be one of the values enumerated in SetShape'
            )

        self.shape = shape
