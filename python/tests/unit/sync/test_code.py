import unittest
import pytest
from unittest.mock import MagicMock, Mock, MagicMock

from agentbay import Code
from agentbay import EnhancedCodeExecutionResult, CodeExecutionResult


class TestAsyncCode(unittest.TestCase):
    """Unit tests for Code module."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_session = MagicMock()
        self.session = self.mock_session  # Add session reference
        self.mock_session._get_api_key.return_value = "test-api-key"
        self.mock_session._get_session_id.return_value = "test-session-id"
        self.mock_session._is_vpc_enabled.return_value = False
        
        self.mock_client = MagicMock()
        self.mock_session._get_client.return_value = self.mock_client
        
        # AsyncCode constructor calls super which stores session
        self.code = Code(self.mock_session)

    @pytest.mark.sync
    def test_run_code_success_python(self):
        """
        Test run_code method with Python code.
        """
        # Setup mock client response
        # Legacy format simulation
        response_body = {
            "Success": True,
            "Data": {
                "content": [{"text": "Hello, world!\n2\n"}],
                "execution_count": 1
            },
            "RequestId": "test-request-id"
        }
        mock_response = MagicMock()
        mock_response.to_map.return_value = {"body": response_body}
        self.mock_client.call_mcp_tool.return_value = mock_response

        code = "print('Hello, world!')\nx = 1 + 1\nprint(x)"
        result = self.code.run_code(code, "python")

        # Verify the call to client
        # We need to verify args passed to call_mcp_tool_async
        # This is harder to verify exactly due to Request object, but we can verify called
        self.mock_client.call_mcp_tool.assert_called_once()
        
        # Verify the result
        self.assertIsInstance(result, EnhancedCodeExecutionResult)
        self.assertTrue(result.success)
        self.assertEqual(result.result, "Hello, world!\n2\n")
        self.assertEqual(result.request_id, "test-request-id")

    @pytest.mark.sync
    def test_run_code_success_javascript(self):
        """
        Test run_code method with JavaScript code.
        """
        response_body = {
            "Success": True,
            "Data": {
                "content": [{"text": "Hello, world!\n2\n"}],
                "execution_count": 1
            },
            "RequestId": "test-request-id"
        }
        mock_response = MagicMock()
        mock_response.to_map.return_value = {"body": response_body}
        self.mock_client.call_mcp_tool.return_value = mock_response

        code = "console.log('Hello, world!');\nconst x = 1 + 1;\nconsole.log(x);"
        custom_timeout = 120

        result = self.code.run_code(code, "javascript", timeout_s=custom_timeout)

        self.mock_client.call_mcp_tool.assert_called_once()

        self.assertIsInstance(result, EnhancedCodeExecutionResult)
        self.assertTrue(result.success)
        self.assertEqual(result.result, "Hello, world!\n2\n")
        self.assertEqual(result.request_id, "test-request-id")

    @pytest.mark.sync
    def test_run_code_invalid_language(self):
        """
        Test run_code method with invalid language.
        """
        result = self.code.run_code("print('test')", "invalid_language")

        self.assertIsInstance(result, EnhancedCodeExecutionResult)
        self.assertFalse(result.success)
        self.assertIn("Unsupported language", result.error_message)

    @pytest.mark.sync
    def test_run_code_error(self):
        """
        Test run_code method with error response.
        """
        # Simulate error response from tool (isError=True)
        response_body = {
            "Success": True,
            "Data": {
                "isError": True,
                "content": [{"text": "Execution failed"}]
            },
            "RequestId": "test-request-id"
        }
        mock_response = MagicMock()
        mock_response.to_map.return_value = {"body": response_body}
        self.mock_client.call_mcp_tool.return_value = mock_response

        result = self.code.run_code("print('test')", "python")

        self.assertIsInstance(result, EnhancedCodeExecutionResult)
        self.assertFalse(result.success)
        # Parse logic raises AgentBayError("Error in response: ..."), which is caught and returned as EnhancedCodeExecutionResult with error_message
        self.assertIn("Execution failed", result.error_message)
        self.assertEqual(result.request_id, "test-request-id")

    @pytest.mark.sync
    def test_run_code_exception(self):
        """
        Test run_code method with exception.
        """
        self.mock_client.call_mcp_tool.side_effect = Exception("Network error")

        result = self.code.run_code("print('test')", "python")

        self.assertIsInstance(result, EnhancedCodeExecutionResult)
        self.assertFalse(result.success)
        self.assertIn("Network error", result.error_message)


if __name__ == "__main__":
    unittest.main()
