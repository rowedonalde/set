from board import SetBoard
from deck import DeckEmpty, SetDeck

class SetRunner(object):

    def __init__(self, quiet=False):
        self.deck = SetDeck()
        self.board = SetBoard(self.deck)
        self.quiet = quiet
        self.sets_found = []

    def log(self, s=''):
        if not self.quiet:
            print s

    def call_set(self, found_set):
        self.log('Set!')
        self.log('Found a set:\n{0}'.format(found_set))
        self.sets_found.append(found_set)

    def play(self):
        self.log('Starting a game of Set!')
        self.log()

        self.board.setup()

        self.log('Initial board:\n{0}'.format(self.board))
        self.log()
        self.log('Looking for sets')
        self.log()

        first_hand = self.board.find_set()

        if first_hand is None:
            self.log('Hmm, no sets so far...')
        else:
            self.call_set(first_hand)

        while self.deck.cards:
            self.log()
            self.log('Now the board is:\n{0}'.format(self.board))
            self.log()
            self.log('Dealing out three new cards:')
            self.log()

            next_hand = self.board.deal_and_search(quiet=self.quiet)
            self.log()

            if next_hand is None:
                self.log('Didn\'t find any sets!')
            else:
                self.call_set(next_hand)

        self.log()
        self.log('Now the deck is empty, so let\'s burn down what we have:')
        self.log(self.board)

        next_set = True

        while next_hand:
            next_hand = self.board.find_set()
            self.log()

            if next_hand:
                self.call_set(next_hand)
                self.log()
                self.log('Now the board is:\n{0}'.format(self.board))

        self.log('No more sets!')
        self.log()

        if self.board.cards:
            self.log('There were some cards left on the board:')
            self.log(self.board)
        else:
            self.log('We were able to make sets using all the cards!')

        self.log()
        self.log('Here are the sets that we found:')
        self.log()

        for hand in self.sets_found:
            self.log(hand)
            self.log()

        return self.sets_found

if __name__ == '__main__':
    runner = SetRunner()
    runner.play()
