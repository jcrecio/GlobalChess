import chess
import chess.uci
import json
import os.path
import pymongo

from pymongo import MongoClient
from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin
from bson.objectid import ObjectId

app = Flask(__name__)
CORS(app)

db_client = MongoClient()
database = db_client.games_db
games = database.games

boards = {}

def get_raw_board(game):
    raw_game = games.find_one({"gameId": game})
    if(raw_game == None): return None

    return raw_game['board']

def setup_engine():
    eng = chess.uci.popen_engine(sys.argv[0])
    eng.uci()

    return eng

engine = setup_engine()

def get_board(game):
    board = boards.get(game)
    if (board != None):
        return board

    raw_board = get_raw_board(game)
    if (raw_board == None):
        boards[game] = chess.Board()
        create_board_into_storage(game, boards[game])
    else:
        boards[game] = chess.Board(raw_board)

    return boards.get(game)

def create_board_into_storage(user, board):
    result = games.insert_one({"userId": user, "board": board.fen()})
    return str(result.inserted_id)

@app.route('/games/new', methods = ['POST'])
def new_game():
    user = request.headers.get('user')

    game_id = create_board_into_storage(user, chess.Board())
    boards[game_id] = chess.Board()

    return json.dumps({"GameId": game_id}), 201, {'ContentType': 'application/json'}

@app.route('/game/<game>/board/moves/best',  methods = ['POST'])
def best_move(game):
    user = request.headers.get('user')

    board_game = get_board(game)
    engine.position(board_game)

    command = engine.go(movetime=1000, async_callback=True)
    command.done()

    resultMove = get_best_move(command)

    board_game.push(chess.Move.from_uci(resultMove))
    engine.position(board_game)

    update_board_into_storage(game, user, board_game)

    response = json.dumps({"Game": game, "Move" : resultMove}), 201, {'ContentType':'application/json'}

    return response

def update_board_into_storage(gameId, userId, board):
    games.update({"_id": ObjectId(gameId)}, { '$set': { "board": board.fen() }})

def get_best_move(command):
    result = command.result()
    resultMove = str(result.bestmove)

    return resultMove

@app.route('/game/<game>/board/move',  methods = ['POST'])
def do_move(game):
    board_game = get_board(game)

    move = json.loads(request.data)['move']
    board_game.push(chess.Move.from_uci(move))
    engine.position(board_game)

    return json.dumps({"Move" : move}), 201, {'ContentType':'application/json'}

@app.route('/game/<game>/board/undo', methods = ['POST'])
def undo_move(game):
    board_game = get_board(game)
    board_game.pop()

    fen_board = str(board_game.fen())

    return json.dumps({"PreviousPosition": fen_board}), 201, {'ContentType': 'application/json'}

@app.route('/game/<game>/delete', methods = ['DELETE'])
def delete_game(game):
    delete_game_from_storage(game)

    return json.dumps({"Game": game}), 204, {'ContentType': 'application/json'}

def delete_game_from_storage(game):
    games.remove({"_id" : ObjectId(game)})

@app.route('/game/<game>/board', methods = ['GET'])
def get_board_position(game):
    board_game = get_board(game)
    engine.position(board_game)

    raw_board = str(boards[game])
    return json.dumps({"Board": raw_board})

@app.route('/game/<game>/board/fen', methods = ['GET'])
def get_fen_board_position(game):
    board_game = get_board(game)
    engine.position(board_game)

    fen_board = str(board_game.fen())
    return json.dumps({"Board": fen_board})

def get_games_store():
    games_list = [str(game['_id']) for game in list(games.find({}))]
    return games_list

@app.route('/games', methods = ['GET'])
def get_all_games():
    games = get_games_store()
    return json.dumps({"Games": games})

if __name__ == '__main__':
    app.run(debug=True)

