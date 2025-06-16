import unittest
import json
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
            "body": {"Data": {"content": [{"text": "line1"}, {"text": "line2"}]}}
        }
        self.session.client.call_mcp_tool.return_value = mock_response

        result = self.command.execute_command("ls -la")
        self.assertEqual(result, "line1\nline2\n")
        MockCallMcpToolRequest.assert_called_once()

        # Verify default timeout was used
        args_dict = json.loads(MockCallMcpToolRequest.call_args.kwargs['args'])
        self.assertEqual(args_dict["timeout_ms"], 1000)

    @patch("agentbay.command.command.CallMcpToolRequest")
    def test_execute_command_with_custom_timeout(self, MockCallMcpToolRequest):
        mock_response = MagicMock()
        mock_response.to_map.return_value = {
            "body": {"Data": {"content": [{"text": "line1"}, {"text": "line2"}]}}
        }
        self.session.client.call_mcp_tool.return_value = mock_response

        custom_timeout = 2000
        result = self.command.execute_command("ls -la", timeout_ms=custom_timeout)
        self.assertEqual(result, "line1\nline2\n")
        MockCallMcpToolRequest.assert_called_once()

        # Verify custom timeout was used
        args_dict = json.loads(MockCallMcpToolRequest.call_args.kwargs['args'])
        self.assertEqual(args_dict["timeout_ms"], custom_timeout)

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

    @patch("agentbay.command.command.CallMcpToolRequest")
    def test_run_code_success_python(self, MockCallMcpToolRequest):
        mock_response = MagicMock()
        mock_response.to_map.return_value = {
            "body": {"Data": {"output": "Hello, world!\n2\n"}}
        }
        self.session.client.call_mcp_tool.return_value = mock_response

        code = """
print("Hello, world!")
x = 1 + 1
print(x)
"""
        result = self.command.run_code(code, "python")
        self.assertEqual(result, "Hello, world!\n2\n")
        MockCallMcpToolRequest.assert_called_once()

        args_dict = json.loads(MockCallMcpToolRequest.call_args.kwargs['args'])
        self.assertEqual(args_dict["timeout_s"], 300)
        self.assertEqual(args_dict["language"], "python")

    @patch("agentbay.command.command.CallMcpToolRequest")
    def test_run_code_success_javascript(self, MockCallMcpToolRequest):
        mock_response = MagicMock()
        mock_response.to_map.return_value = {
            "body": {"Data": {"output": "Hello, world!\n2\n"}}
        }
        self.session.client.call_mcp_tool.return_value = mock_response

        code = """
console.log("Hello, world!");
const x = 1 + 1;
console.log(x);
"""
        custom_timeout = 600
        result = self.command.run_code(code, "javascript", timeout_s=custom_timeout)
        self.assertEqual(result, "Hello, world!\n2\n")
        MockCallMcpToolRequest.assert_called_once()

        # Verify custom timeout was used
        args_dict = json.loads(MockCallMcpToolRequest.call_args.kwargs['args'])
        self.assertEqual(args_dict["timeout_s"], custom_timeout)
        self.assertEqual(args_dict["language"], "javascript")

    @patch("agentbay.command.command.CallMcpToolRequest")
    def test_run_code_invalid_language(self, MockCallMcpToolRequest):
        with self.assertRaises(CommandError) as context:
            self.command.run_code("print('test')", "invalid_language")
        self.assertIn("Unsupported language", str(context.exception))
        MockCallMcpToolRequest.assert_not_called()

    @patch("agentbay.command.command.CallMcpToolRequest")
    def test_run_code_no_output(self, MockCallMcpToolRequest):
        mock_response = MagicMock()
        mock_response.to_map.return_value = {
            "body": {"Data": {
                # No output field
            }}
        }
        self.session.client.call_mcp_tool.return_value = mock_response

        with self.assertRaises(CommandError) as context:
            self.command.run_code("print('test')", "python")
        self.assertIn("output field not found", str(context.exception))

    @patch("agentbay.command.command.CallMcpToolRequest")
    def test_run_code_exception(self, MockCallMcpToolRequest):
        self.session.client.call_mcp_tool.side_effect = Exception("mock error")
        with self.assertRaises(CommandError) as context:
            self.command.run_code("print('test')", "python")
        self.assertIn("Failed to execute code: mock error", str(context.exception))


if __name__ == "__main__":
    unittest.main()
