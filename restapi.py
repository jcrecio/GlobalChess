import chess
import chess.uci
import json
import os.path

from flask import Flask
from flask import request
from Model.move_dto import MoveDto

app = Flask(__name__)

boards = {}

def get_file_name(game):
    return "games/" + game + ".txt"

def get_raw_board(game):
    file = open(get_file_name(game), "r")
    return file.read()

def setup_engine():
    eng = chess.uci.popen_engine(sys.argv[0])
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

    return response, created


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

@app.route('/game/<game>/board', methods = ['GET'])
def get_board_position(game):
    board_game = get_board(game)
    engine.position(board_game)

    raw_board = str(boards[game])
    return json.dumps({"Board": raw_board})

if __name__ == '__main__':
    app.run(debug=True)


