from django.test import TestCase
from unittest.mock import patch, MagicMock

from clients.jsonrpc_client import call_jsonrpc_method


class JsonRpcClientTests(TestCase):
    @patch("clients.jsonrpc_client.urllib.request.urlopen")
    def test_successful_call(self, mock_urlopen):
        # Given
        self._mocking_response(
            b'{"jsonrpc": "2.0", "id": "test123", "result": {"data": "ok"}}',
            mock_urlopen,
        )

        # When
        result = call_jsonrpc_method("test.method", params={}, request_id="test123")

        # Then
        self.assertIn("result", result)
        self.assertIn("data", result["result"])
        self.assertEqual(result["result"]["data"], "ok")

    @patch("clients.jsonrpc_client.urllib.request.urlopen")
    def test_jsonrpc_error(self, mock_urlopen):
        # Given
        self._mocking_response(
            b'{"jsonrpc": "2.0", "id": "test123", "error": {"code": 123, "message": "Some error"}}',
            mock_urlopen,
        )

        # When
        with self.assertRaises(RuntimeError) as ctx:
            call_jsonrpc_method("test.method", params={}, request_id="test123")

        # Then
        self.assertIn("JSON-RPC error:", str(ctx.exception))

    @patch("clients.jsonrpc_client.urllib.request.urlopen")
    def test_network_error(self, mock_urlopen):
        # Given
        mock_urlopen.side_effect = Exception("Network fail")

        # When
        with self.assertRaises(RuntimeError) as ctx:
            call_jsonrpc_method("test.method", params={}, request_id="test123")

        # Then
        self.assertIn(
            "An error occurred while executing JSON-RPC request", str(ctx.exception)
        )

    @patch("clients.jsonrpc_client.urllib.request.urlopen")
    def test_invalid_json_response(self, mock_urlopen):
        # Given
        self._mocking_response(
            b'{"jsonrpc": "2.0", "id": "bad"  "result": }', mock_urlopen
        )

        # When
        with self.assertRaises(RuntimeError) as ctx:
            call_jsonrpc_method("test.method", params={}, request_id="bad")

        # Then
        self.assertIn(
            "An error occurred while executing JSON-RPC request", str(ctx.exception)
        )

    @staticmethod
    def _mocking_response(return_value, mock_urlopen):
        mock_response = MagicMock()
        mock_response.read.return_value = return_value
        mock_urlopen.return_value.__enter__.return_value = mock_response

        return mock_response
