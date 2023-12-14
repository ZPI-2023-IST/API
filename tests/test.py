import json
import unittest
from aiohttp import web, ClientSession
from aiohttp.test_utils import AioHTTPTestCase
from socketio import AsyncClient
from unittest.mock import ANY as _
from api.main import SocketIOServer
import asyncio
from .board import BOARD

class TestSocketIOServerIntegration(AioHTTPTestCase):
    async def get_application(self):
        self.server = SocketIOServer()
        return self.server.app

    async def test_make_move_integration(self):
        try:
            self.sio_client = AsyncClient()
            await self.sio_client.connect('http://localhost:5002')

            # Assuming you have a sample move
            sample_move = {"move": None}

            # Create an asyncio.Event to signal when the 'get_response' event is received
            response_event = asyncio.Event()

            # Define a callback to handle the 'get_response' event
            async def response_callback(data):
                self.received_data = data
                response_event.set()

            # Register the callback for the 'get_response' event
            self.sio_client.on('get_response', response_callback)

            # Emit the 'make_move' event from the client
            await self.sio_client.emit('make_move', json.dumps(sample_move))

            # Wait for the 'get_response' event from the server
            await asyncio.wait_for(response_event.wait(), timeout=5)  # Adjust the timeout if needed

            # Perform your assertions here
            self.assertTrue(response_event.is_set())
            self.assertIsNotNone(self.received_data)
            self.assertEqual(self.received_data,json.dumps(BOARD))

        finally:
            await self.sio_client.disconnect()

if __name__ == '__main__':
    unittest.main()
