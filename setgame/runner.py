from board import SetBoard
from deck import DeckEmpty, SetDeck

class SetRunner(object):

    def __init__(self):
        self.deck = SetDeck()
        self.board = SetBoard(self.deck)

    def play(self):
        print 'Starting a game of Set!'
        print

        self.board.setup()

        print 'Initial board:\n{0}'.format(self.board)
        print
        print 'Looking for sets'
        print

        first_hand = self.board.find_set()

        if first_hand is None:
            print 'Hmm, no sets so far...'
        else:
            print 'Set!'
            print 'Found a set in the first 12 cards:\n{0}'.format(first_hand)

        while self.deck.cards:
            print
            print 'Now the board is:\n{0}'.format(self.board)
            print
            print 'Dealing out three new cards:'
            print

            next_hand = self.board.deal_and_search(quiet=False)
            print

            if next_hand is None:
                print 'Didn\'t find any sets!'
            else:
                print 'Set!'
                print 'Found a set:\n{0}'.format(next_hand)

        print
        print 'Now the deck is empty, so let\'s burn down what we have:'
        print self.board
        print

        next_set = True

        while next_hand:
            next_hand = self.board.find_set()

            if next_hand:
                print 'Set!'
                print 'Found a set:\n{0}'.format(next_hand)
                print
                print 'Now the board is:\n{0}'.format(self.board)

        print 'No more sets!'
        print

        if self.board.cards:
            print 'There were some cards left on the board:'
            print self.board
        else:
            print 'We were able to make sets using all the cards!'

if __name__ == '__main__':
    runner = SetRunner()
    runner.play()
