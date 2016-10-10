class SetHand(object):

    def __init__(self, card1, card2, card3):
        self.cards = set([card1, card2, card3])

    def is_set(self):
        '''
        Return true if these three cards represent a valid set in
        the card game Set.

        The three cards represent a valid set if, for each of the
        four attributes, the cards are all the same or all different
        for that attribute.'''

        # A dict of the number of occurrences of each attribute
        # value. If the cards are a valid set, each attribute may
        # be seen 0 times (if that attribute were the same across the
        # cards, but for another value), 1 time (if the cards were
        # all different for that attribute), or 3 times (if the cards
        # all were the same for that attribute, and it was that value).
        # No attribute value can be seen more than 3 times in a hand,
        # therefore, we know that this hand is not a valid set if
        # any value is seen exactly 2 times.
        attribute_occurrences = dict()

        for card in self.cards:
            for attr in (card.count, card.color, card.shading, card.shape):
                try:
                    attribute_occurrences[attr] += 1
                except KeyError:
                    attribute_occurrences[attr] = 1

        return 2 not in attribute_occurrences.values()
