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
    move_data = data.get("move", {})
    ml_no_cards = move_data.get("ml_no_cards")
    ml_src = move_data.get("ml_src")
    ml_dst = move_data.get("ml_dst")

    print(data)
    print(f"sender: {sid} tells translator to make move:")
    print(f"ml_no_cards: {ml_no_cards}, ml_src: {ml_src}, ml_dst: {ml_dst}")

    # translator.make_move(ml_no_cards, ml_src, ml_dst)

    state = translator.get_state()
    reward = translator.get_reward()
    moves = translator.get_moves()
    board = translator.get_board()

    response_data = {
        "moves_vector": moves,  # To be replaced with actual moves vector data
        "game_board": board,  # To be replaced with actual game state vector data
        "reward": reward,
        "state": state.__str__(),
    }

    await sio.emit("get_response", json.dumps(response_data), room=sid)


if __name__ == '__main__':
    game = FreeCell()
    translator = FreecellTranslator(game)
    web.run_app(app, host="127.0.0.1", port=5002)