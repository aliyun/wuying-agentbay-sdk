import unittest
import json
from unittest.mock import MagicMock, patch

from agentbay.command.command import Command
from agentbay.exceptions import CommandError
from agentbay.model import OperationResult


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

    @patch("agentbay.command.command.extract_request_id")
    @patch("agentbay.command.command.CallMcpToolRequest")
    def test_execute_command_success(self, MockCallMcpToolRequest, mock_extract_request_id):
        mock_response = MagicMock()
        mock_response.to_map.return_value = {
            "body": {"Data": {"content": [{"text": "line1\nline2\n"}]}}
        }
        mock_extract_request_id.return_value = "request-123"
        self.session.client.call_mcp_tool.return_value = mock_response

        success, result = self.command.execute_command("ls -la")
        self.assertTrue(success)
        self.assertEqual(result, "line1\nline2\n")
        MockCallMcpToolRequest.assert_called_once()

        # Verify default timeout was used
        args_dict = json.loads(MockCallMcpToolRequest.call_args.kwargs["args"])
        self.assertEqual(args_dict["timeout_ms"], 1000)

    @patch("agentbay.command.command.extract_request_id")
    @patch("agentbay.command.command.CallMcpToolRequest")
    def test_execute_command_with_custom_timeout(self, MockCallMcpToolRequest, mock_extract_request_id):
        mock_response = MagicMock()
        mock_response.to_map.return_value = {
            "body": {"Data": {"content": [{"text": "line1\nline2\n"}]}}
        }
        mock_extract_request_id.return_value = "request-123"
        self.session.client.call_mcp_tool.return_value = mock_response

        custom_timeout = 2000
        success, result = self.command.execute_command("ls -la", timeout_ms=custom_timeout)
        self.assertTrue(success)
        self.assertEqual(result, "line1\nline2\n")
        MockCallMcpToolRequest.assert_called_once()

        # Verify custom timeout was used
        args_dict = json.loads(MockCallMcpToolRequest.call_args.kwargs["args"])
        self.assertEqual(args_dict["timeout_ms"], custom_timeout)

    @patch("agentbay.command.command.extract_request_id")
    @patch("agentbay.command.command.CallMcpToolRequest")
    def test_execute_command_no_content(self, MockCallMcpToolRequest, mock_extract_request_id):
        mock_response = MagicMock()
        mock_response.to_map.return_value = {
            "body": {"Data": {"no_content": "no_content"}}
        }
        mock_extract_request_id.return_value = "request-123"
        self.session.client.call_mcp_tool.return_value = mock_response

        success, error_msg = self.command.execute_command("ls -la")
        self.assertFalse(success)
        self.assertIn("No content found in response", error_msg)

    @patch("agentbay.command.command.extract_request_id")
    @patch("agentbay.command.command.CallMcpToolRequest")
    def test_execute_command_exception(self, MockCallMcpToolRequest, mock_extract_request_id):
        self.session.client.call_mcp_tool.side_effect = Exception("mock error")
        mock_extract_request_id.return_value = "request-123"

        success, error_msg = self.command.execute_command("ls -la")
        self.assertFalse(success)
        self.assertIn("Failed to execute command: mock error", error_msg)

    @patch("agentbay.command.command.extract_request_id")
    @patch("agentbay.command.command.CallMcpToolRequest")
    def test_run_code_success_python(self, MockCallMcpToolRequest, mock_extract_request_id):
        mock_response = MagicMock()
        mock_response.to_map.return_value = {
            "body": {"Data": {"content": [{"text": "Hello, world!\n2\n"}]}}
        }
        mock_extract_request_id.return_value = "request-123"
        self.session.client.call_mcp_tool.return_value = mock_response

        code = """
print("Hello, world!")
x = 1 + 1
print(x)
"""
        success, result = self.command.run_code(code, "python")
        self.assertTrue(success)
        self.assertEqual(result, "Hello, world!\n2\n")
        MockCallMcpToolRequest.assert_called_once()

        args_dict = json.loads(MockCallMcpToolRequest.call_args.kwargs["args"])
        self.assertEqual(args_dict["timeout_s"], 300)
        self.assertEqual(args_dict["language"], "python")

    @patch("agentbay.command.command.extract_request_id")
    @patch("agentbay.command.command.CallMcpToolRequest")
    def test_run_code_success_javascript(self, MockCallMcpToolRequest, mock_extract_request_id):
        mock_response = MagicMock()
        mock_response.to_map.return_value = {
            "body": {"Data": {"content": [{"text": "Hello, world!\n2\n"}]}}
        }
        mock_extract_request_id.return_value = "request-123"
        self.session.client.call_mcp_tool.return_value = mock_response

        code = """
console.log("Hello, world!");
const x = 1 + 1;
console.log(x);
"""
        custom_timeout = 600
        success, result = self.command.run_code(code, "javascript", timeout_s=custom_timeout)
        self.assertTrue(success)
        self.assertEqual(result, "Hello, world!\n2\n")
        MockCallMcpToolRequest.assert_called_once()

        # Verify custom timeout was used
        args_dict = json.loads(MockCallMcpToolRequest.call_args.kwargs["args"])
        self.assertEqual(args_dict["timeout_s"], custom_timeout)
        self.assertEqual(args_dict["language"], "javascript")

    def test_run_code_invalid_language(self):
        success, error_msg = self.command.run_code("print('test')", "invalid_language")
        self.assertFalse(success)
        self.assertIn("Unsupported language", error_msg)

    @patch("agentbay.command.command.extract_request_id")
    @patch("agentbay.command.command.CallMcpToolRequest")
    def test_run_code_no_output(self, MockCallMcpToolRequest, mock_extract_request_id):
        mock_response = MagicMock()
        mock_response.to_map.return_value = {
            "body": {
                "Data": {
                    # No content field
                    "no_content": "no_content"
                }
            }
        }
        mock_extract_request_id.return_value = "request-123"
        self.session.client.call_mcp_tool.return_value = mock_response

        success, error_msg = self.command.run_code("print('test')", "python")
        self.assertFalse(success)
        self.assertIn("No content found in response", error_msg)

    @patch("agentbay.command.command.extract_request_id")
    @patch("agentbay.command.command.CallMcpToolRequest")
    def test_run_code_exception(self, MockCallMcpToolRequest, mock_extract_request_id):
        self.session.client.call_mcp_tool.side_effect = Exception("mock error")
        mock_extract_request_id.return_value = "request-123"

        success, error_msg = self.command.run_code("print('test')", "python")
        self.assertFalse(success)
        self.assertIn("Failed to run code: mock error", error_msg)


if __name__ == "__main__":
    unittest.main()
