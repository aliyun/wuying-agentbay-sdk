import unittest
from unittest.mock import MagicMock, patch

from agentbay.agent import Agent, TaskResult
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


class TestAgent(unittest.TestCase):
    def setUp(self):
        self.session = DummySession()
        self.agent = Agent(self.session)

    @patch("agentbay.agent.Agent._call_mcp_tool")
    def test_task_execute_success(self, mock_call_mcp_tool):
        """
        Test flux_execute_task method with successful response.
        """
        mock_result = OperationResult(
            request_id="request-123", success=True, data="line1\nline2\n"
        )
        mock_call_mcp_tool.return_value = mock_result

        result = self.agent.flux_execute_task("Say hello")
        self.assertIsInstance(result, TaskResult)
        self.assertTrue(result.success)
        self.assertEqual(result.request_id, "request-123")
        self.assertEqual(result.output, "line1\nline2\n")
        self.assertEqual(result.error_message, "")

        # Verify call arguments
        mock_call_mcp_tool.assert_called_once()
        args = mock_call_mcp_tool.call_args[0][1]
        self.assertEqual(args["task"], "Say hello")

    @patch("agentbay.agent.Agent._call_mcp_tool")
    def test_execute_task_error(self, mock_call_mcp_tool):
        """
        Test flux_execute_task method with error response.
        """
        mock_result = OperationResult(
            request_id="request-123",
            success=False,
            error_message="Task execution failed",
        )
        mock_call_mcp_tool.return_value = mock_result

        result = self.agent.flux_execute_task("Say hello")
        self.assertIsInstance(result, TaskResult)
        self.assertFalse(result.success)
        self.assertEqual(result.request_id, "request-123")
        self.assertEqual(result.error_message, "Task execution failed")
        self.assertEqual(result.output, "")

    @patch("agentbay.agent.Agent._call_mcp_tool")
    def test_task_terminate_success(self, mock_call_mcp_tool):
        """
        Test flux_terminate_task method with successful response.
        """
        mock_result = OperationResult(
            request_id="request-123", success=True, data="line1\nline2\n"
        )
        mock_call_mcp_tool.return_value = mock_result

        result = self.agent.flux_terminate_task("task123")
        self.assertIsInstance(result, TaskResult)
        self.assertTrue(result.success)
        self.assertEqual(result.request_id, "request-123")
        self.assertEqual(result.output, "line1\nline2\n")
        self.assertEqual(result.error_message, "")

        # Verify call arguments
        mock_call_mcp_tool.assert_called_once()
        args = mock_call_mcp_tool.call_args[0][1]
        self.assertEqual(args["task_id"], "task123")


if __name__ == "__main__":
    unittest.main()
