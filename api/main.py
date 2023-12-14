import json
from aiohttp import web
import sys
import socketio
from runner import Runner


class SocketIOServer:
    def __init__(self, host="0.0.0.0", port=5002):
        self.runner = Runner()
        self.sio = socketio.AsyncServer(async_mode="aiohttp", cors_allowed_origins="*")
        self.app = web.Application()
        self.sio.attach(self.app)

        # Register event handlers
        self.sio.event(self.make_move)

        # Define routes or other app-specific configurations as needed

    async def make_move(self, sid, data):
        data = json.loads(data)
        move_ml = data.get("move")

        print(data)
        print(f"sender: {sid} tells translator to make move:")
        print(f"move_ml: {move_ml}")

        if move_ml is None:
            self.runner.reset()
        else:
            self.runner.translator.make_move(move_ml)

        state = self.runner.translator.get_state()
        reward = self.runner.translator.get_reward()
        moves = self.runner.translator.get_moves()
        board = self.runner.translator.get_board()
        board_raw = self.runner.game.get_board()

        print(f"moves: {moves}")

        response_data = {
            "moves_vector": moves,
            "game_board": board,
            "reward": reward,
            "state": state.name,
            "board_raw": self.parse_board(board_raw)
        }

        await self.sio.emit("get_response", json.dumps(response_data), room=sid)

    def parse_board(self, board):
        new_board = {"Board": [], "FreeCells": [], "Stack": []}
        for stack in board[0]:
            new_board["Board"].append([])
            for card in stack:
                card = card.__repr__() if card is not None else None
                new_board["Board"][-1].append(card)
        for card in board[1]:
            card = card.__repr__() if card is not None else None
            new_board["FreeCells"].append(card)
        for card in board[2]:
            card = card.__repr__() if card is not None else None
            new_board["Stack"].append(card)
        return new_board

    def run(self):
        web.run_app(self.app, host="0.0.0.0", port=5002)


if __name__ == '__main__':
    server = SocketIOServer()
    server.run()
