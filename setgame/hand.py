class SetHand(object):

    def __init__(self, card1, card2, card3):
        self.cards = set([card1, card2, card3])

    def __str__(self):
        strs = [str(card) for card in self.cards]
        return '\n'.join(strs)

    def is_set(self):
        '''
        Return true if these three cards represent a valid set in
        the card game Set.

        The three cards represent a valid set if, for each of the
        four attributes, the cards are all the same or all different
        for that attribute.'''

        # If the cards are a valid set, each attribute may
        # be seen 0 times (if that attribute were the same across the
        # cards, but for another value), 1 time (if the cards were
        # all different for that attribute), or 3 times (if the cards
        # all were the same for that attribute, and it was that value).
        # No attribute value can be seen more than 3 times in a hand,
        # therefore, we know that this hand is not a valid set if
        # any value is seen exactly 2 times.

        # If we're going to use IntEnum values as keys in a dict,
        # we need to keep them in separate dicts since the hashes
        # will collide unlike different enumerated values from the
        # basic Enum class:
        attribute_occurrences = {
            'count': {},
            'color': {},
            'shading': {},
            'shape': {}
        }

        for card in self.cards:
            for attr in (('count', card.count), ('color', card.color),
                ('shading', card.shading), ('shape', card.shape)):
                subdict = attribute_occurrences[attr[0]]
                try:
                    subdict[attr[1]] += 1
                except KeyError:
                    subdict[attr[1]] = 1

        all_values = []

        for attr in attribute_occurrences:
            all_values += attribute_occurrences[attr].values()

        return 2 not in all_values
