class SetBoard(object):
    start_size = 12
    deal = 3

    def __init__(self, deck):
        # Get handle to deck:
        self.deck = deck

        self.cards_by_encoding = {}

    @property
    def cards(self):
        return self.cards_by_encoding.values()

    def setup(self):
        for i in range(SetBoard.start_size):
            self.draw_from_deck()

        return self.cards_by_encoding

    def draw_from_deck(self):
        card = self.deck.draw_random()
        self.cards_by_encoding[card.encoding] = card

        return card
