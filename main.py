import json

import socketio
from aiohttp import web

from runner import Runner

sio = socketio.AsyncServer(async_mode="aiohttp", cors_allowed_origins="*")
app = web.Application()
runner = Runner()
sio.attach(app)

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
    
    print(f"moves: {moves}")

    response_data = {
        "moves_vector": moves,
        "game_board": board,
        "reward": reward,
        "state": state.__str__()
    }

    await sio.emit("get_response", json.dumps(response_data), room=sid)


if __name__ == '__main__':
    web.run_app(app, host="localhost", port=5002)
