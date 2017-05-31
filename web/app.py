from uuid import uuid1

from flask import Flask, jsonify, make_response

from setgame import SetBoard, SetDeck
app = Flask(__name__)

boards = {}
sets = {}

@app.route('/api/boards')
def get_boards():
    '''
    Return all current set game IDs

    Responses:
    200 -- array of IDs'''
    return jsonify(boards.keys())

@app.route('/api/board/<board_id>')
def get_board_by_id(board_id):
    '''
    Return the board with the given ID.

    Responses:
    200 -- list of card descriptions on the board
    404 -- no board exists with that ID; returns null'''

    try:
        board = boards[board_id]
    except KeyError:
        return make_response(jsonify(None), 404)
    return jsonify([str(card) for card in board.cards])

@app.route('/api/sets/<board_id>')
def get_sets_by_board_id(board_id):
    '''
    Return the sets found so far for a given ID.

    Responses:
    200 -- array of arrays of matching sets
    404 -- no board exists with that ID; returns null'''

    try:
        sets_for_board = sets[board_id]
    except KeyError:
        return make_response(jsonify(None), 404)

    formatted_sets = []

    for hand in sets_for_board:
        formatted_sets.append([str(card) for card in hand.cards])

    return jsonify(formatted_sets)

@app.route('/api/board', methods=['POST'])
def new_board():
    '''
    Generate a new board

    Responses:
    201 -- {ID: [Array of cards]}'''

    deck = SetDeck()
    board = SetBoard(deck)
    board.setup()

    board_id = str(uuid1())

    boards[board_id] = board
    sets[board_id] = []
    return make_response(
        jsonify({board_id: [str(card) for card in board.cards]}),
        201
    )

@app.route('/api/board/<board_id>/next', methods=['POST'])
def board_step_forward(board_id):
    '''
    Step forward in the game with the A.I.

    If this is the first step after dealing, just try to find
    a set amongst these 12 cards. If not, deal out 3 more cards
    and try to find a set. If there are no more cards in the
    deck, keep making sets until no possible sets remain on the
    board. In each case, return the set (if there was one) and
    the cards remaining on the board after any such set was made.

    Responses:
    200 -- Any match, the board after any match, and a done flag
    404 -- The board does not exist; return null'''

    try:
        board = boards[board_id]
    except KeyError:
        return make_response(jsonify(None), 404)

    last_turn = False

    # First turn:
    if len(board.graveyard) == 0 and len(board.cards) == SetBoard.start_size:
        set_found = board.find_set()
    elif board.deck.cards:
        set_found = board.deal_and_search()
    else:
        set_found = board.find_set()
        last_turn = set_found is None

    if set_found is not None:
        sets[board_id].append(set_found)
        set_found = [str(card) for card in set_found.cards]

    ret = {
        'set_found': set_found,
        'board': [str(card) for card in board.cards],
        'last_turn': last_turn
    }

    return jsonify(ret)

if __name__ == '__main__':
    app.run()