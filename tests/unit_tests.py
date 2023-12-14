import unittest
from unittest.mock import patch

from api.main import SocketIOServer


class TestSocketIOServer(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.server = SocketIOServer()

    @patch('api.main.web.run_app')
    def test_run_method(self, mock_run_app):
        # Create an instance of SocketIOServer
        server = SocketIOServer()

        # Call the run method
        server.run()

        # Verify that web.run_app was called with the correct arguments
        mock_run_app.assert_called_once_with(server.app, host="0.0.0.0", port=5002)

    async def test_make_move(self):
        with patch.object(self.server.runner.translator, 'make_move') as mock_make_move:
            await self.server.make_move("test_sid", '{"move": "test_move"}')
            mock_make_move.assert_called_with("test_move")

    async def test_parse_board(self):
        # Assuming you have a sample board.py for testing
        sample_board = [
            [[1, 2], [3, 4]],
            [5, 6, 7],
            [8, 9, 10]]

        # Mock the runner game board.py
        with patch.object(self.server.runner.game, 'get_board', return_value=sample_board):
            result = self.server.parse_board(sample_board)

        expected_result = {
            "Board": [['1', '2'], ['3', '4']],
            "FreeCells": ['5', '6', '7'],
            "Stack": ['8', '9', '10']
        }

        self.assertEqual(result, expected_result)

    async def test_make_move_reset(self):
        with patch.object(self.server.runner, 'reset') as mock_reset:
            await self.server.make_move("test_sid", '{"move": null}')
            mock_reset.assert_called_once()


if __name__ == '__main__':
    unittest.main()
