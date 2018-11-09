import chess
import chess.uci
import json
import os.path

from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin
from os import listdir
from os.path import isfile, join
from pathlib import Path

app = Flask(__name__)
CORS(app)
boards = {}

def get_file_name(game):
    return "games/" + game + ".txt"

def get_raw_board(game):
    file = open(get_file_name(game), "r")
    return file.read()

def setup_engine():
    eng = chess.uci.popen_engine("C:\ChessEngines\Rybka\Rybkav2.3.2a.mp.w32.exe")
    eng.uci()
    return eng

engine = setup_engine()

def get_board(game):
    board = boards.get(game)
    if (board != None):
        return board

    if (os.path.isfile(get_file_name(game))):
        boards[game] = chess.Board(get_raw_board(game))
        return boards.get(game)
    else:
        boards[game] = chess.Board()
        save_board_into_storage(game, boards[game])
        return boards.get(game)

def save_board_into_storage(game, board):
    game_file = open(get_file_name(game), "w")
    game_file.write(board.fen())
    game_file.close()

@app.route('/game/<game>/board/moves/best',  methods = ['POST'])
def best_move(game):
    board_game = get_board(game)
    engine.position(board_game)

    command = engine.go(movetime=1000, async_callback=True)
    command.done()

    resultMove = get_best_move(command)

    board_game.push(chess.Move.from_uci(resultMove))
    engine.position(board_game)

    save_board_into_storage(game, board_game)

    response = json.dumps({"Game": game, "Move" : resultMove}), 201, {'ContentType':'application/json'}

    return response


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

def remove_extension(file):
    return Path(file).stem

def get_games_store():
    list = []
    games = [f for f in listdir("games") if isfile(join("games", f))]
    for game in games:
        list.append(remove_extension(game))
    return list

@app.route('/games', methods = ['GET'])
def get_all_games():
    games = get_games_store()
    return json.dumps({"Games": games})

if __name__ == '__main__':
    app.run(debug=True)

