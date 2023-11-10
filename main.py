import socketio
from aiohttp import web

sio = socketio.AsyncServer(async_mode="aiohttp", cors_allowed_origins="*")
app = web.Application()
sio.attach(app)


@sio.event
async def make_move(sid, move):
    print(f"sender: {sid} tells translator to make move: {move}")
    await sio.emit("get_response", "[moves_vector,game_state_vector,reward]", room=sid)


if __name__ == '__main__':
    web.run_app(app, host="localhost", port=5002)

