from collections import defaultdict
from uuid import uuid1

from flask import Flask, jsonify, make_response, request

from setgame import DeckEmpty, SetBoard, SetCard, SetDeck, SetHand

AI_NAME = 'house'

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
    200 -- array of arrays of players' matching sets
    404 -- no board exists with that ID; returns null'''

    try:
        sets_for_board = sets[board_id]
    except KeyError:
        return make_response(jsonify(None), 404)

    def printable_hands(hands):
        return [str(hand) for hand in hands]

    formatted_sets_by_player = {name: printable_hands(hands) for name, hands in sets_for_board.iteritems()}

    return jsonify(formatted_sets_by_player)

@app.route('/api/set/<board_id>/<username>', methods=['POST'])
def claim_set(board_id, username):
    '''
    Verify and attribute a set to a user if valid.

    Responses:
    201 -- {"success": true, "board": [cards now on board]}
    400 -- {"success": false, "reason": str}'''

    payload = request.get_json(force=True)
    board = boards[board_id]

    claimed_cards = [SetCard.from_str(c) for c in payload['cards']]
    claimed_cards_encodings = [c.encoding for c in claimed_cards]

    claimed_hand = SetHand(*claimed_cards)

    if not claimed_hand.is_set():
        return make_response(jsonify(dict(success=False, reason='Not a valid set')), 400)

    try:
        board.remove_set(*claimed_cards_encodings)
    except KeyError:
        return make_response(jsonify(dict(success=False, reason='Card not on board')), 400)

    # Attribute set to player:
    sets[board_id][username].append(claimed_hand)

    for i in range(SetBoard.deal_size):
        board.draw_from_deck()

    return make_response(jsonify(dict(success=True, board=[str(c) for c in board.cards])))

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
    sets[board_id] = defaultdict(list)
    return make_response(
        jsonify({board_id: [str(card) for card in board.cards]}),
        201
    )

@app.route('/api/board/<board_id>/next', methods=['POST'])
def board_step_forward(board_id):
    '''
    Step forward in the game with the A.I.

    Try to find a set amongst the cards. Then, try to deal out three
    more cards. If there are no more cards in the deck and no set
    could be made, flag that the game is finished. In each case,
    return the set (if there was one) and the cards remaining on the
    board after any such set was made.

    Responses:
    200 -- Any match (or null), the board after any match, and a done flag
    404 -- The board does not exist; return null'''

    try:
        board = boards[board_id]
    except KeyError:
        return make_response(jsonify(None), 404)

    set_found = board.find_set()

    if set_found is not None:
        sets[board_id][AI_NAME].append(set_found)
        set_found = [str(card) for card in set_found.cards]

    try:
        board.deal_in()
        last_turn = False
    except DeckEmpty:
        last_turn = set_found is None

    ret = dict(
        set_found=set_found,
        board=[str(card) for card in board.cards],
        last_turn=last_turn
    )

    return jsonify(ret)

@app.route('/api/board/<board_id>/deal', methods=['POST'])
def deal_in(board_id):
    '''
    Deal in three cards.

    Responses:
    200 -- The new cards (if any), the board including the new cards,
        and the number of cards remaining in the deck.
    404 -- The board does not exist; return null'''

    try:
        board = boards[board_id]
    except KeyError:
        return make_response(jsonify(None), 404)

    try:
        new_cards = board.deal_in()
    except DeckEmpty:
        new_cards = list()

    ret = dict(
        new_cards=new_cards,
        remaining=len(board.deck.cards),
        board=[str(c) for c in board.cards]
    )

    return make_response(jsonify(ret))

if __name__ == '__main__':
    app.run()