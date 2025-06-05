import unittest
from unittest.mock import MagicMock, patch
from agentbay.command.command import Command
from agentbay.exceptions import CommandError

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

class TestCommand(unittest.TestCase):
    def setUp(self):
        self.session = DummySession()
        self.command = Command(self.session)

    @patch("agentbay.command.command.CallMcpToolRequest")
    def test_execute_command_success(self, MockCallMcpToolRequest):
        mock_response = MagicMock()
        mock_response.to_map.return_value = {
            "body": {
                "Data": {
                    "content": [
                        {"text": "line1"},
                        {"text": "line2"}
                    ]
                }
            }
        }
        self.session.client.call_mcp_tool.return_value = mock_response

        result = self.command.execute_command("ls -la")
        self.assertEqual(result, "line1\nline2\n")
        MockCallMcpToolRequest.assert_called_once()

    @patch("agentbay.command.command.CallMcpToolRequest")
    def test_execute_command_no_content(self, MockCallMcpToolRequest):
        mock_response = MagicMock()
        mock_response.to_map.return_value = {
            "body": {
                "Data": {
                    # No content field
                }
            }
        }
        self.session.client.call_mcp_tool.return_value = mock_response

        with self.assertRaises(CommandError) as context:
            self.command.execute_command("ls -la")
        self.assertIn("content field not found", str(context.exception))

    @patch("agentbay.command.command.CallMcpToolRequest")
    def test_execute_command_exception(self, MockCallMcpToolRequest):
        self.session.client.call_mcp_tool.side_effect = Exception("mock error")
        with self.assertRaises(CommandError) as context:
            self.command.execute_command("ls -la")
        self.assertIn("Failed to execute command: mock error", str(context.exception))

if __name__ == "__main__":
    unittest.main()