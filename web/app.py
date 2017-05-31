from uuid import uuid1

from flask import Flask, jsonify, make_response

from setgame import SetBoard, SetDeck
app = Flask(__name__)

boards = {}

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
    return make_response(
        jsonify({board_id: [str(card) for card in board.cards]}),
        201
    )

if __name__ == '__main__':
    app.run()