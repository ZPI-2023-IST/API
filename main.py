import json

import socketio
from aiohttp import web
from game.Freecell import FreeCell
from translator.freecell_translator.freecell_translator import FreecellTranslator

sio = socketio.AsyncServer(async_mode="aiohttp", cors_allowed_origins="*")
app = web.Application()
sio.attach(app)


@sio.event
async def make_move(sid, data):
    move_ml = data.get("move")

    print(data)
    print(f"sender: {sid} tells translator to make move:")
    print(f"move_ml: {move_ml}")

    translator.make_move(move_ml)
    state = translator.get_state()
    reward = translator.get_reward()
    moves = translator.get_moves()
    board = translator.get_board()

    response_data = {
        "moves_vector": moves,
        "game_board": board,
        "reward": reward,
        "state": state.__str__(),
    }

    await sio.emit("get_response", json.dumps(response_data), room=sid)


if __name__ == '__main__':
    game = FreeCell()
    translator = FreecellTranslator(game)
    web.run_app(app, host="localhost", port=5002)
