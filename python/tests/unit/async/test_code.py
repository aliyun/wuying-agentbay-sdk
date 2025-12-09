import unittest
import pytest
from unittest.mock import AsyncMock, Mock, patch

from agentbay import AsyncCode
from agentbay import CodeExecutionResult


class TestAsyncCode(unittest.IsolatedAsyncioTestCase):
    """Unit tests for Code module."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_session = Mock()
        self.session = self.mock_session  # Add session reference
        self.mock_session.get_api_key.return_value = "test-api-key"
        self.mock_session.get_session_id.return_value = "test-session-id"
        self.mock_session.get_client.return_value = Mock()
        self.mock_session.call_mcp_tool = AsyncMock()

        self.code = AsyncCode(self.mock_session)

    @pytest.mark.asyncio


    async def test_run_code_success_python(self):
        """
        Test run_code method with Python code.
        """
        # Setup mock response
        mock_result = Mock()
        mock_result.success = True
        mock_result.data = "Hello, world!\n2\n"
        mock_result.request_id = "test-request-id"
        self.session.call_mcp_tool.return_value = mock_result

        code = "print('Hello, world!')\nx = 1 + 1\nprint(x)"
        result = await self.code.run_code(code, "python")

        # Verify the call
        self.session.call_mcp_tool.assert_called_once_with(
            "run_code", {"code": code, "language": "python", "timeout_s": 60}
        )

        # Verify the result
        self.assertIsInstance(result, CodeExecutionResult)
        self.assertTrue(result.success)
        self.assertEqual(result.result, "Hello, world!\n2\n")
        self.assertEqual(result.request_id, "test-request-id")

    @pytest.mark.asyncio


    async def test_run_code_success_javascript(self):
        """
        Test run_code method with JavaScript code.
        """
        # Setup mock response
        mock_result = Mock()
        mock_result.success = True
        mock_result.data = "Hello, world!\n2\n"
        mock_result.request_id = "test-request-id"
        self.session.call_mcp_tool.return_value = mock_result

        code = "console.log('Hello, world!');\nconst x = 1 + 1;\nconsole.log(x);"
        custom_timeout = 120

        result = await self.code.run_code(code, "javascript", timeout_s=custom_timeout)

        # Verify the call
        self.session.call_mcp_tool.assert_called_once_with(
            "run_code",
            {"code": code, "language": "javascript", "timeout_s": custom_timeout},
        )

        # Verify the result
        self.assertIsInstance(result, CodeExecutionResult)
        self.assertTrue(result.success)
        self.assertEqual(result.result, "Hello, world!\n2\n")
        self.assertEqual(result.request_id, "test-request-id")

    @pytest.mark.asyncio


    async def test_run_code_invalid_language(self):
        """
        Test run_code method with invalid language.
        """
        result = await self.code.run_code("print('test')", "invalid_language")

        self.assertIsInstance(result, CodeExecutionResult)
        self.assertFalse(result.success)
        self.assertIn("Unsupported language", result.error_message)

    @pytest.mark.asyncio


    async def test_run_code_error(self):
        """
        Test run_code method with error response.
        """
        # Setup mock response
        mock_result = Mock()
        mock_result.success = False
        mock_result.error_message = "Execution failed"
        mock_result.request_id = "test-request-id"
        self.session.call_mcp_tool.return_value = mock_result

        result = await self.code.run_code("print('test')", "python")

        self.assertIsInstance(result, CodeExecutionResult)
        self.assertFalse(result.success)
        self.assertEqual(result.error_message, "Execution failed")
        self.assertEqual(result.request_id, "test-request-id")

    @pytest.mark.asyncio


    async def test_run_code_exception(self):
        """
        Test run_code method with exception.
        """
        self.session.call_mcp_tool.side_effect = Exception("Network error")

        result = await self.code.run_code("print('test')", "python")

        self.assertIsInstance(result, CodeExecutionResult)
        self.assertFalse(result.success)
        self.assertEqual(result.error_message, "Failed to run code: Network error")


if __name__ == "__main__":
    unittest.main()
