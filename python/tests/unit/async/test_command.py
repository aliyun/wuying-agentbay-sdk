import unittest
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from agentbay import OperationResult
from agentbay import AsyncCommand
from agentbay import CommandResult


class DummySession:
    def __init__(self):
        self.api_key = "dummy_key"
        self.session_id = "dummy_session"
        self.client = MagicMock()
        # Add call_mcp_tool method for new API
        self.call_mcp_tool = MagicMock()

    def get_api_key(self):
        return self.api_key

    def get_session_id(self):
        return self.session_id

    def get_client(self):
        return self.client


class TestAsyncCommand(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.session = DummySession()
        self.command = AsyncCommand(self.session)

    @pytest.mark.asyncio


    async def test_execute_command_success(self):
        """
        Test execute_command method with successful response.
        """
        from agentbay import McpToolResult

        mock_result = McpToolResult(
            request_id="request-123", success=True, data="line1\nline2\n"
        )
        self.session.call_mcp_tool = AsyncMock(return_value=mock_result)

        result = await self.command.execute_command("ls -la")
        self.assertIsInstance(result, CommandResult)
        self.assertTrue(result.success)
        self.assertEqual(result.request_id, "request-123")
        self.assertEqual(result.output, "line1\nline2\n")
        self.assertEqual(result.error_message, "")

        # Verify call arguments
        self.session.call_mcp_tool.assert_called_once()
        args = self.session.call_mcp_tool.call_args[0][1]
        self.assertEqual(args["command"], "ls -la")
        self.assertEqual(args["timeout_ms"], 50000)  # Default timeout (60000ms) is limited to 50000ms

    @pytest.mark.asyncio


    async def test_execute_command_with_custom_timeout(self):
        """
        Test execute_command method with custom timeout.
        """
        from agentbay import McpToolResult

        mock_result = McpToolResult(
            request_id="request-123", success=True, data="line1\nline2\n"
        )
        self.session.call_mcp_tool = AsyncMock(return_value=mock_result)

        custom_timeout = 2000
        result = await self.command.execute_command("ls -la", timeout_ms=custom_timeout)
        self.assertIsInstance(result, CommandResult)
        self.assertTrue(result.success)
        self.assertEqual(result.output, "line1\nline2\n")

        # Verify custom timeout was used
        self.session.call_mcp_tool.assert_called_once()
        args = self.session.call_mcp_tool.call_args[0][1]
        self.assertEqual(args["timeout_ms"], custom_timeout)

    @pytest.mark.asyncio


    async def test_execute_command_error(self):
        """
        Test execute_command method with error response.
        """
        from agentbay import McpToolResult

        mock_result = McpToolResult(
            request_id="request-123",
            success=False,
            error_message="Command execution failed",
        )
        self.session.call_mcp_tool = AsyncMock(return_value=mock_result)

        result = await self.command.execute_command("ls -la")
        self.assertIsInstance(result, CommandResult)
        self.assertFalse(result.success)
        self.assertEqual(result.request_id, "request-123")
        self.assertEqual(result.error_message, "Command execution failed")
        self.assertEqual(result.output, "")

    @pytest.mark.asyncio


    async def test_execute_command_exception(self):
        """
        Test execute_command method with exception.
        """
        self.session.call_mcp_tool = AsyncMock(side_effect=Exception("mock error"))

        result = await self.command.execute_command("ls -la")
        self.assertIsInstance(result, CommandResult)
        self.assertFalse(result.success)
        self.assertEqual(result.request_id, "")
        self.assertIn("Failed to execute command: mock error", result.error_message)
        self.assertEqual(result.output, "")

    async def test_execute_command_with_new_json_format(self):
        """
        Test execute_command method with new JSON format response.
        """
        from agentbay import McpToolResult
        import json

        # New format JSON response (success case, traceId should be empty or not present)
        json_data = json.dumps({
            "stdout": "output text",
            "stderr": "error text",
            "errorCode": 0,
        })
        mock_result = McpToolResult(
            request_id="request-123", success=True, data=json_data
        )
        self.session.call_mcp_tool = AsyncMock(return_value=mock_result)

        result = await self.command.execute_command("ls -la")
        self.assertIsInstance(result, CommandResult)
        self.assertTrue(result.success)
        self.assertEqual(result.request_id, "request-123")
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.stdout, "output text")
        self.assertEqual(result.stderr, "error text")
        self.assertEqual(result.output, "output texterror text")  # output = stdout + stderr for backward compatibility
        self.assertEqual(result.trace_id, "")  # traceId should be empty for success

    async def test_execute_command_with_new_json_format_error(self):
        """
        Test execute_command method with new JSON format response (error case).
        """
        from agentbay import McpToolResult
        import json

        # New format JSON response with error
        json_data = json.dumps({
            "stdout": "",
            "stderr": "command not found",
            "errorCode": 127,
            "traceId": "trace-123"
        })
        mock_result = McpToolResult(
            request_id="request-123", success=True, data=json_data
        )
        self.session.call_mcp_tool = AsyncMock(return_value=mock_result)

        result = await self.command.execute_command("invalid_command")
        self.assertIsInstance(result, CommandResult)
        self.assertFalse(result.success)  # errorCode != 0 means failure
        self.assertEqual(result.request_id, "request-123")
        self.assertEqual(result.exit_code, 127)
        self.assertEqual(result.stdout, "")
        self.assertEqual(result.stderr, "command not found")
        self.assertEqual(result.output, "command not found")  # output = stdout + stderr ("" + "command not found")
        self.assertEqual(result.trace_id, "trace-123")  # traceId should be present for errors

    async def test_execute_command_with_cwd_and_envs(self):
        """
        Test execute_command method with cwd and envs parameters.
        """
        from agentbay import McpToolResult

        mock_result = McpToolResult(
            request_id="request-123", success=True, data="test output"
        )
        self.session.call_mcp_tool = AsyncMock(return_value=mock_result)

        result = await self.command.execute_command(
            "pwd",
            timeout_ms=5000,
            cwd="/tmp",
            envs={"TEST_VAR": "test_value"}
        )
        self.assertIsInstance(result, CommandResult)
        self.assertTrue(result.success)

        # Verify call arguments
        self.session.call_mcp_tool.assert_called_once()
        args = self.session.call_mcp_tool.call_args[0][1]
        self.assertEqual(args["command"], "pwd")
        self.assertEqual(args["timeout_ms"], 5000)
        self.assertEqual(args["cwd"], "/tmp")
        self.assertEqual(args["envs"], {"TEST_VAR": "test_value"})

    async def test_execute_command_timeout_limit(self):
        """
        Test execute_command method with timeout exceeding maximum limit (50s).
        """
        from agentbay import McpToolResult

        mock_result = McpToolResult(
            request_id="request-123", success=True, data="test output"
        )
        self.session.call_mcp_tool = AsyncMock(return_value=mock_result)

        # Test with timeout exceeding 50s (50000ms)
        result = await self.command.execute_command("ls -la", timeout_ms=60000)
        self.assertIsInstance(result, CommandResult)
        self.assertTrue(result.success)

        # Verify timeout was limited to 50000ms
        self.session.call_mcp_tool.assert_called_once()
        args = self.session.call_mcp_tool.call_args[0][1]
        self.assertEqual(args["timeout_ms"], 50000)  # Should be limited to 50s

        # Test with timeout exactly at limit
        self.session.call_mcp_tool.reset_mock()
        result = await self.command.execute_command("ls -la", timeout_ms=50000)
        args = self.session.call_mcp_tool.call_args[0][1]
        self.assertEqual(args["timeout_ms"], 50000)  # Should remain 50s

        # Test with timeout below limit
        self.session.call_mcp_tool.reset_mock()
        result = await self.command.execute_command("ls -la", timeout_ms=30000)
        args = self.session.call_mcp_tool.call_args[0][1]
        self.assertEqual(args["timeout_ms"], 30000)  # Should remain unchanged

    async def test_execute_command_invalid_envs_key(self):
        """
        Test execute_command method with invalid envs key (not string).
        Should raise ValueError.
        """
        # Test with non-string key
        with self.assertRaises(ValueError) as context:
            await self.command.execute_command(
                "echo test",
                envs={123: "value"}  # Invalid: key is int, not string
            )
        self.assertIn("Invalid environment variables", str(context.exception))
        self.assertIn("must be strings", str(context.exception))

    async def test_execute_command_invalid_envs_value(self):
        """
        Test execute_command method with invalid envs value (not string).
        Should raise ValueError.
        """
        # Test with non-string value
        with self.assertRaises(ValueError) as context:
            await self.command.execute_command(
                "echo test",
                envs={"TEST_VAR": 123}  # Invalid: value is int, not string
            )
        self.assertIn("Invalid environment variables", str(context.exception))
        self.assertIn("must be strings", str(context.exception))

    async def test_execute_command_invalid_envs_mixed(self):
        """
        Test execute_command method with mixed valid and invalid envs.
        Should raise ValueError.
        """
        # Test with mixed valid and invalid values
        with self.assertRaises(ValueError) as context:
            await self.command.execute_command(
                "echo test",
                envs={"VALID": "ok", "INVALID": True, "ANOTHER": 123}  # Mixed valid and invalid
            )
        self.assertIn("Invalid environment variables", str(context.exception))
        self.assertIn("must be strings", str(context.exception))

    async def test_execute_command_valid_envs(self):
        """
        Test execute_command method with valid envs (all strings).
        Should not raise any error.
        """
        from agentbay import McpToolResult

        mock_result = McpToolResult(
            request_id="request-123", success=True, data='{"stdout": "test", "stderr": "", "errorCode": 0}'
        )
        self.session.call_mcp_tool = AsyncMock(return_value=mock_result)

        # Test with valid envs (all strings)
        result = await self.command.execute_command(
            "echo test",
            envs={"TEST_VAR": "123", "MODE": "production"}
        )
        self.assertIsInstance(result, CommandResult)
        self.assertTrue(result.success)

        # Verify envs were passed correctly
        self.session.call_mcp_tool.assert_called_once()
        args = self.session.call_mcp_tool.call_args[0][1]
        self.assertEqual(args["envs"], {"TEST_VAR": "123", "MODE": "production"})


if __name__ == "__main__":
    unittest.main()
