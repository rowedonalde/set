class SetBoard(object):
    start_size = 12
    deal = 3

    def __init__(self, deck):
        # Get handle to deck:
        self.deck = deck

        self.cards_by_encoding = {}
        self.graveyard_by_encoding = {}

    @property
    def cards(self):
        return self.cards_by_encoding.values()

    @property
    def graveyard(self):
        return self.graveyard_by_encoding.values()

    def setup(self):
        '''Draw enough cards at random to start a game.'''

        for i in range(SetBoard.start_size):
            self.draw_from_deck()

        return self.cards_by_encoding

    def draw_from_deck(self):
        '''
        Remove one card randomly from the deck and put
        it on the board.'''

        card = self.deck.draw_random()
        self.cards_by_encoding[card.encoding] = card

        return card

    def remove_set(self, encoding_1, encoding_2, encoding_3):
        '''
        Move the cards denoted by the encodings into the
        graveyard and return those cards as well. This happens
        transactionally so if one of the keys is not actually
        on the board, any cards that did get moved are rolled
        back before the KeyError propagates.'''

        tx = {}

        for encoding in (encoding_1, encoding_2, encoding_3):
            try:
                tx[encoding] = self.cards_by_encoding.pop(encoding)
            except KeyError:
                # Rollback transaction:
                self.cards_by_encoding.update(tx)
                raise

        self.graveyard_by_encoding.update(tx)
        return tx

    def find_set(self):
        '''
        Return a valid set of three cards from the board or
        None if there are no valid sets on the board.'''

        return None

        # Search greedily for valid sets, and only compare
        # forward against cards we haven't tried so we don't
        # duplicate work:
        #encodings = self.cards_by_encoding.keys()

        #for i in range(len(encodings)):
        #    encoding_1 = encodings[i]
        #    for encoding_2 in encodings[i+1:]:
        #        encoding_3 = SetBoard.missing_encoding_from(
        #            encoding_1,
        #            encoding_2,
        #        )

        #        try:
        #            return self.remove_set(encoding_3, encoding_2, encoding_1)

    @staticmethod
    def missing_encoding_from(card_encoding_1, card_encoding_2):
        '''
        Return the encoding of the card that would make a
        valid set with the cards of the given encodings.'''

        # The running total of the encoding of the third card
        # in the set suggested by the given encodings:
        output_encoding = 0

        # The current shifting of the input values:
        rem_1 = card_encoding_1
        rem_2 = card_encoding_2

        # The number of times we need to shift:
        trits = 4

        # We're working in an unsigned ternary system since
        # there are three possible values for each attribute:
        base = 3

        # We don't need to reconstruct the card or the actual
        # attributes, so we can just treat each trit as an
        # arbitrary flag where the values will either be all the
        # same or all different:

        for exp in range(trits):
            attr_val_1 = rem_1 % base
            attr_val_2 = rem_2 % base

            if attr_val_1 == attr_val_2:
                output_attr_val = attr_val_1
            else:
                output_attr_val = base - attr_val_1 - attr_val_2

            output_encoding += (base ** exp) * output_attr_val

            # Shift tritwise to the right:
            rem_1 /= base
            rem_2 /= base

        return output_encoding
