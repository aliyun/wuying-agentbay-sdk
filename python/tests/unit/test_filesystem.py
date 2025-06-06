import unittest
from unittest.mock import MagicMock, patch

from agentbay.exceptions import FileError
from agentbay.filesystem.filesystem import \
    FileSystem  # Adjust based on actual module path


class DummySession:
    def __init__(self):
        self.api_key = "dummy_key"
        self.session_id = "dummy_session"
        self.client = MagicMock()

    def get_api_key(self):
        return self.api_key

    def get_session_id(self):
        return self.session_id

    def get_client(self):
        return self.client


class TestFileSystem(unittest.TestCase):
    def setUp(self):
        self.session = DummySession()
        self.fs = FileSystem(self.session)

    @patch("agentbay.filesystem.filesystem.CallMcpToolRequest")
    def test_read_file_success(self, MockCallMcpToolRequest):
        print("test_read_file_success")
        mock_response = MagicMock()
        mock_response.to_map.return_value = {
            "body": {"Data": {"content": [{"text": "file content"}]}}
        }
        self.session.client.call_mcp_tool.return_value = mock_response

        result = self.fs.read_file("/path/to/file.txt")
        self.assertEqual(result, "file content")
        MockCallMcpToolRequest.assert_called_once()

    @patch("agentbay.filesystem.filesystem.CallMcpToolRequest")
    def test_read_file_get_false(self, MockCallMcpToolRequest):
        print("test_read_file_no_content")
        mock_response = MagicMock()
        mock_response.to_map.return_value = {
            "body": {
                "Data": {
                    "isError": True,
                    "content": [{"text": "some error message"}],
                }  # No content field
            }
        }
        self.session.client.call_mcp_tool.return_value = mock_response

        with self.assertRaises(FileError) as context:
            self.fs.read_file("/path/to/file.txt")

        self.assertIn("Failed to read file:", str(context.exception))

    @patch("agentbay.filesystem.filesystem.CallMcpToolRequest")
    def test_read_file_error_format(self, MockCallMcpToolRequest):
        print("test_read_file_no_content")
        mock_response = MagicMock()
        mock_response.to_map.return_value = {"some_unknown_key": {""}}
        self.session.client.call_mcp_tool.return_value = mock_response

        with self.assertRaises(FileError) as context:
            self.fs.read_file("/path/to/file.txt")

        self.assertIn("Failed to read file:", str(context.exception))
        self.assertIn("KeyError", str(context.exception))


if __name__ == "__main__":
    unittest.main()
