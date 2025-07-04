import unittest
from unittest.mock import MagicMock, patch

from agentbay.command.command import CodeExecutionResult, Command, CommandResult
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

    @patch("agentbay.command.command.Command._call_mcp_tool")
    def test_execute_command_success(self, mock_call_mcp_tool):
        """
        Test execute_command method with successful response.
        """
        mock_result = OperationResult(
            request_id="request-123", success=True, data="line1\nline2\n"
        )
        mock_call_mcp_tool.return_value = mock_result

        result = self.command.execute_command("ls -la")
        self.assertIsInstance(result, CommandResult)
        self.assertTrue(result.success)
        self.assertEqual(result.request_id, "request-123")
        self.assertEqual(result.output, "line1\nline2\n")
        self.assertEqual(result.error_message, "")

        # Verify call arguments
        mock_call_mcp_tool.assert_called_once()
        args = mock_call_mcp_tool.call_args[0][1]
        self.assertEqual(args["command"], "ls -la")
        self.assertEqual(args["timeout_ms"], 1000)  # Default timeout

    @patch("agentbay.command.command.Command._call_mcp_tool")
    def test_execute_command_with_custom_timeout(self, mock_call_mcp_tool):
        """
        Test execute_command method with custom timeout.
        """
        mock_result = OperationResult(
            request_id="request-123", success=True, data="line1\nline2\n"
        )
        mock_call_mcp_tool.return_value = mock_result

        custom_timeout = 2000
        result = self.command.execute_command("ls -la", timeout_ms=custom_timeout)
        self.assertIsInstance(result, CommandResult)
        self.assertTrue(result.success)
        self.assertEqual(result.output, "line1\nline2\n")

        # Verify custom timeout was used
        mock_call_mcp_tool.assert_called_once()
        args = mock_call_mcp_tool.call_args[0][1]
        self.assertEqual(args["timeout_ms"], custom_timeout)

    @patch("agentbay.command.command.Command._call_mcp_tool")
    def test_execute_command_error(self, mock_call_mcp_tool):
        """
        Test execute_command method with error response.
        """
        mock_result = OperationResult(
            request_id="request-123",
            success=False,
            error_message="Command execution failed",
        )
        mock_call_mcp_tool.return_value = mock_result

        result = self.command.execute_command("ls -la")
        self.assertIsInstance(result, CommandResult)
        self.assertFalse(result.success)
        self.assertEqual(result.request_id, "request-123")
        self.assertEqual(result.error_message, "Command execution failed")
        self.assertEqual(result.output, "")

    @patch("agentbay.command.command.Command._call_mcp_tool")
    def test_execute_command_exception(self, mock_call_mcp_tool):
        """
        Test execute_command method with exception.
        """
        mock_call_mcp_tool.side_effect = Exception("mock error")

        result = self.command.execute_command("ls -la")
        self.assertIsInstance(result, CommandResult)
        self.assertFalse(result.success)
        self.assertEqual(result.request_id, "")
        self.assertIn("Failed to execute command: mock error", result.error_message)
        self.assertEqual(result.output, "")

    @patch("agentbay.command.command.Command._call_mcp_tool")
    def test_run_code_success_python(self, mock_call_mcp_tool):
        """
        Test run_code method with Python code.
        """
        mock_result = OperationResult(
            request_id="request-123", success=True, data="Hello, world!\n2\n"
        )
        mock_call_mcp_tool.return_value = mock_result

        code = """
print("Hello, world!")
x = 1 + 1
print(x)
"""
        result = self.command.run_code(code, "python")
        self.assertIsInstance(result, CodeExecutionResult)
        self.assertTrue(result.success)
        self.assertEqual(result.request_id, "request-123")
        self.assertEqual(result.result, "Hello, world!\n2\n")
        self.assertEqual(result.error_message, "")

        # Verify arguments
        mock_call_mcp_tool.assert_called_once()
        args = mock_call_mcp_tool.call_args[0][1]
        self.assertEqual(args["language"], "python")
        self.assertEqual(args["timeout_s"], 300)  # Default timeout

    @patch("agentbay.command.command.Command._call_mcp_tool")
    def test_run_code_success_javascript(self, mock_call_mcp_tool):
        """
        Test run_code method with JavaScript code.
        """
        mock_result = OperationResult(
            request_id="request-123", success=True, data="Hello, world!\n2\n"
        )
        mock_call_mcp_tool.return_value = mock_result

        code = """
console.log("Hello, world!");
const x = 1 + 1;
console.log(x);
"""
        custom_timeout = 600
        result = self.command.run_code(code, "javascript", timeout_s=custom_timeout)
        self.assertIsInstance(result, CodeExecutionResult)
        self.assertTrue(result.success)
        self.assertEqual(result.request_id, "request-123")
        self.assertEqual(result.result, "Hello, world!\n2\n")

        # Verify custom timeout
        mock_call_mcp_tool.assert_called_once()
        args = mock_call_mcp_tool.call_args[0][1]
        self.assertEqual(args["timeout_s"], custom_timeout)
        self.assertEqual(args["language"], "javascript")

    def test_run_code_invalid_language(self):
        """
        Test run_code method with invalid language.
        """
        result = self.command.run_code("print('test')", "invalid_language")
        self.assertIsInstance(result, CodeExecutionResult)
        self.assertFalse(result.success)
        self.assertEqual(result.request_id, "")
        self.assertIn("Unsupported language", result.error_message)
        self.assertEqual(result.result, "")

    @patch("agentbay.command.command.Command._call_mcp_tool")
    def test_run_code_error(self, mock_call_mcp_tool):
        """
        Test run_code method with error response.
        """
        mock_result = OperationResult(
            request_id="request-123",
            success=False,
            error_message="Code execution failed",
        )
        mock_call_mcp_tool.return_value = mock_result

        result = self.command.run_code("print('test')", "python")
        self.assertIsInstance(result, CodeExecutionResult)
        self.assertFalse(result.success)
        self.assertEqual(result.request_id, "request-123")
        self.assertEqual(result.error_message, "Code execution failed")
        self.assertEqual(result.result, "")

    @patch("agentbay.command.command.Command._call_mcp_tool")
    def test_run_code_exception(self, mock_call_mcp_tool):
        """
        Test run_code method with exception.
        """
        mock_call_mcp_tool.side_effect = Exception("mock error")

        result = self.command.run_code("print('test')", "python")
        self.assertIsInstance(result, CodeExecutionResult)
        self.assertFalse(result.success)
        self.assertEqual(result.request_id, "")
        self.assertIn("Failed to run code: mock error", result.error_message)
        self.assertEqual(result.result, "")


if __name__ == "__main__":
    unittest.main()
