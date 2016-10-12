from hand import SetHand

class SetBoard(object):
    start_size = 12
    deal_size = 3

    def __init__(self, deck):
        # Get handle to deck:
        self.deck = deck

        self.cards_by_encoding = {}
        self.graveyard_by_encoding = {}

        # Key: encoding
        # Value: list of Python sets of two other encodings
        self.waitlist = {}

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
        cards = tx.values()
        return SetHand(*cards)

    def add_to_waitlist(self, missing, partner_1, partner_2):
        '''
        Add the encoding of the missing card to a waitlist
        associating that encoding with the encodings of
        existing cards that would form a valid set with it.
        Note that one card can match with more than one pair
        of cards. This method trusts that the missing encoding
        was calculated accurately by missing_encoding_from.'''

        try:
            self.waitlist[missing].append(set([partner_1, partner_2]))
        except KeyError:
            self.waitlist[missing] = [set([partner_1, partner_2])]

    def try_remove_from_waitlist(self, new_card_encoding):
        '''
        Return a hand of the card denoted by the given encoding
        and its partners if they exist in the board. Raise
        KeyError if the card is not on the waitlist or if the
        partner cards have already been used in another set
        and the waitlist entry has gone stale. The
        new_card_encoding will idempotently not exist in the
        waitlist afterward.'''

        partner_sets = self.waitlist[new_card_encoding]

        # Keep trying the partner cards until you find a group
        # That isn't stale:
        while len(partner_sets) > 0:
            partners = list(partner_sets.pop())
            partners.append(new_card_encoding)
            try:
                return self.remove_set(*partners)
            except KeyError:
                # At least one of the other two cards no longer
                # exists on the board, so this particular partner
                # duo is stale
                pass

        # All of the partner sets have gone stale:
        del self.waitlist[new_card_encoding]
        raise KeyError

    def find_set(self, encodings=None):
        '''
        Return a valid hand of three cards from the board or
        None if there are no valid sets on the board.'''

        # We can't refer to self for the default value, but by
        # default we want to search with all the encodings:
        if encodings is None:
            encodings = self.cards_by_encoding.keys()

        # Search greedily for valid sets, and only compare
        # forward against cards we haven't tried so we don't
        # duplicate work:

        for i in range(len(encodings)):
            encoding_1 = encodings[i]
            for encoding_2 in encodings[i+1:]:

                # Figure out what third card would be needed to make
                # a valid hand with encoding_1 and encoding_2:
                encoding_3 = SetBoard.missing_encoding_from(
                    encoding_1,
                    encoding_2
                )

                try:
                    # If the third card exists on the board, make a
                    # valid set out of them:
                    return self.remove_set(encoding_3, encoding_2, encoding_1)
                except KeyError:
                    # Otherwise, record the third card on the waitlist
                    # so we can make this group when the card shows up:
                    self.add_to_waitlist(encoding_3, encoding_1, encoding_2)

        return None

    def deal_and_search(self):
        new_cards = []
        for i in range(SetBoard.deal_size):
            new_card = self.draw_from_deck()
            new_cards.append(new_card)

        new_encodings = [c.encoding for c in new_cards]

        possible_hand = SetHand(*new_cards)

        if possible_hand.is_set():
            # draw_from_deck already puts it in cards,
            # so we need to use this to add them to the
            # graveyard:
            self.remove_set(*new_encodings)
            return possible_hand

        # Check waitlist to see if any of the new cards
        # have an existing match:
        for new_card in new_cards:
            try:
                return self.try_remove_from_waitlist(new_card.encoding)
            except KeyError:
                # No match for this card
                pass

        # Check pairs of new cards to see if the third was already
        # on the board:
        return self.find_set(encodings=new_encodings)

        # We don't need to check new cards against the cards that were
        # already on the board. If the third card in such a group were
        # already on the board, we would have found the current card in
        # the waitlist. If the third card were in this new hand dealt
        # out, we would have found it when searching pairwise in the
        # new deal-out.

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
