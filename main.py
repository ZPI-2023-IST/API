import json

import socketio
from aiohttp import web
from game.Freecell import FreeCell
from translator.freecell_translator.freecell_translator import FreecellTranslator

sio = socketio.AsyncServer(async_mode="aiohttp", cors_allowed_origins="*")
app = web.Application()
sio.attach(app)

game = FreeCell(seed=0)
translator = FreecellTranslator(game)
i = 0

@sio.event
async def make_move(sid, data):
    global translator
    global game
    global i
    
    i += 1
    
    data = json.loads(data)
    move_ml = data.get("move")

    print(data)
    print(f"sender: {sid} tells translator to make move:")
    print(f"move_ml: {move_ml}")
    print(f"step: {i}")
    
    if move_ml is None:
        print("Resetting game")
        game = FreeCell(seed=0)
        translator = FreecellTranslator(game)
    else:
        translator.make_move(move_ml)
    
    state = translator.get_state()
    reward = translator.get_reward()
    moves = translator.get_moves()
    board = translator.get_board()
    
    print(f"moves: {moves}")

    response_data = {
        "moves_vector": moves,
        "game_board": board,
        "reward": reward,
        "state": state.__str__(),
        "control": i
    }

    await sio.emit("get_response", json.dumps(response_data), room=sid)


if __name__ == '__main__':
    web.run_app(app, host="localhost", port=5002)
