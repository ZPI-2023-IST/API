import json

import socketio
from aiohttp import web

from runner import Runner

sio = socketio.AsyncServer(async_mode="aiohttp", cors_allowed_origins="*")
app = web.Application()
runner = Runner()
sio.attach(app)


def parse_board(board):
    new_board =   {"Board": [], "FreeCells": [], "Stack": []}
    for stack in board[0]:
        new_board["Board"].append([])
        for card in stack:
            new_board["Board"][-1].append(card.__repr__())
    for card in board[1]:
        new_board["FreeCells"].append(card.__repr__())
    for card in board[2]:
        new_board["Stack"].append(card.__repr__())
    return new_board


@sio.event
async def make_move(sid, data):
    data = json.loads(data)
    move_ml = data.get("move")

    print(data)
    print(f"sender: {sid} tells translator to make move:")
    print(f"move_ml: {move_ml}")
    
    if move_ml is None:
        runner.reset()
    else:
        runner.translator.make_move(move_ml)
    
    state = runner.translator.get_state()
    reward = runner.translator.get_reward()
    moves = runner.translator.get_moves()
    board = runner.translator.get_board()
    board_raw = runner.game.get_board()
        
    print(f"moves: {moves}")

    response_data = {
        "moves_vector": moves,
        "game_board": board,
        "reward": reward,
        "state": state.name,
        "board_raw": parse_board(board_raw)
    }

    await sio.emit("get_response", json.dumps(response_data), room=sid)



if __name__ == '__main__':
    web.run_app(app, host="0.0.0.0", port=5002)
