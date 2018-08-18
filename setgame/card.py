from color import SetColor
from exponent import EncodingExponents
from shading import SetShading
from shape import SetShape

class SetCard(object):
    '''Represents a card in the Set card game.'''

    def __init__(self, count, color, shading, shape):
        # "Private" lazy cache for numeric encoding of card:
        self._encoding = None

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

    def __str__(self):
        outstr = '{0} {1} {2} {3}'.format(
            self.count,
            SetColor.format(self.color),
            SetShading.format(self.shading),
            SetShape.format(self.shape)
        )

        if self.count > 1:
            outstr += 's'

        return outstr

    @staticmethod
    def from_str(card_string):
        count, color, shading, shape = card_string.strip().split(' ')

        # We strip a possible pluralizing 's' from the shape name:
        return SetCard(int(count), SetColor.from_str(color), SetShading.from_str(shading), SetShape.from_str(shape.rstrip('s')))

    @property
    def encoding(self):
        if self._encoding is None:
            self._encoding = 0

            # Generate 4-trit ternary encoding where each trit represents
            # one of the three values an attribute can have:
            exponent_to_attribute = {
                EncodingExponents.color: self.color,
                EncodingExponents.shading: self.shading,
                EncodingExponents.shape: self.shape,
                # We want 0, 1, and 2 instead of 1, 2, and 3:
                EncodingExponents.count: self.count - 1
            }

            for exp in exponent_to_attribute:
                value = exponent_to_attribute[exp]
                self._encoding += (3 ** exp) * value

        return self._encoding
