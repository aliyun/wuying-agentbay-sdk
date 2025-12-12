import os
import pytest
import time
import unittest
from unittest.mock import AsyncMock, MagicMock

from agentbay import get_logger
from agentbay import OperationResult
from agentbay import AsyncAgent
from agentbay import ExecutionResult

logger = get_logger("agentbay-unit-test")


class DummySession:
    def __init__(self):
        self.api_key = "dummy_key"
        self.session_id = "dummy_session"
        self.client = MagicMock()
        # Add call_mcp_tool method for new API
        self.call_mcp_tool = AsyncMock()

    def get_api_key(self):
        return self.api_key

    def get_session_id(self):
        return self.session_id

    def get_client(self):
        return self.client


class TestAsyncAgentComputer(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.session = DummySession()
        self.agent = AsyncAgent(self.session)
        self.max_try_times = os.environ.get("AGENT_TASK_TIMEOUT")
        if not self.max_try_times:
            self.max_try_times = 5

    @pytest.mark.asyncio


    async def test_computer_task_execute_and_wait_success(self):
        """
        Test flux_execute_task method with successful response.
        """
        from agentbay import McpToolResult

        mock_result = McpToolResult(
            request_id="request-123",
            success=True,
            data="""{"task_id": "task-123", "status": "finished", "result":"", "product": "Task completed successfully"}""",
        )
        self.session.call_mcp_tool.return_value = mock_result

        result = await self.agent.computer.execute_task_and_wait("Hello, Computer Agent", int(self.max_try_times))
        self.assertIsInstance(result, ExecutionResult)
        self.assertTrue(result.success)
        self.assertEqual(result.request_id, "request-123")
        self.assertEqual(result.task_status, "finished")
        self.assertEqual(result.error_message, "")

        # Verify call arguments
        self.assertEqual(self.session.call_mcp_tool.call_count, 2)
        args = self.session.call_mcp_tool.call_args[0][1]
        self.assertEqual(args["task_id"], "task-123")
        logger.info(f"Result of Task Hello, Computer Agent: {result.task_result}")

    @pytest.mark.asyncio


    async def test_computer_execute_task_and_wait_error(self):
        """
        Test execute_task method with error response.
        """
        from agentbay import McpToolResult

        mock_result = McpToolResult(
            request_id="request-123",
            success=False,
            error_message="Task execution failed",
            data="""{"task_id": "task-123", "status": "failed", "result":"", "product": "Task Failed"}""",
        )
        self.session.call_mcp_tool.return_value = mock_result
        result = await self.agent.computer.execute_task_and_wait("Hello, Computer Agent", self.max_try_times)
        self.assertIsInstance(result, ExecutionResult)
        self.assertFalse(result.success)
        self.assertEqual(result.request_id, "request-123")
        self.assertEqual(result.error_message, "Task execution failed")
        self.assertEqual(result.task_status, "failed")
        args = self.session.call_mcp_tool.call_args[0][1]
        self.assertEqual(args["task"], "Hello, Computer Agent")
        logger.info(f"Result of task Hello, Computer Agent: {result.task_result}")

    @pytest.mark.asyncio


    async def test_computer_task_terminate_success(self):
        """
        Test terminate_task method with successful response.
        """
        from agentbay import McpToolResult

        mock_result = McpToolResult(
            request_id="request-123",
            success=True,
            data="""{"task_id": "task-123", "status": "finished", "result":"", "product": "Task completed successfully"}""",
        )
        self.session.call_mcp_tool.return_value = mock_result

        result = await self.agent.computer.terminate_task("task-123")
        self.assertIsInstance(result, ExecutionResult)
        self.assertTrue(result.success)
        self.assertEqual(result.request_id, "request-123")
        self.assertEqual(result.task_status, "finished")
        self.assertEqual(result.error_message, "")

        # Verify call arguments
        self.session.call_mcp_tool.assert_called_once()
        args = self.session.call_mcp_tool.call_args[0][1]
        self.assertEqual(args["task_id"], "task-123")

    @pytest.mark.asyncio


    async def test_computer_task_execute_timeout(self):
        """
        Test flux_execute_task method with successful response.
        """
        from agentbay import McpToolResult

        mock_result = McpToolResult(
            request_id="request-123",
            success=True,
            data="""{"task_id": "task-123", "status": "finished", "result":"", "product": "Task completed successfully"}""",
        )
        self.session.call_mcp_tool.return_value = mock_result

        result = await self.agent.computer.execute_task("Hello, Computer Agent")
        self.assertIsInstance(result, ExecutionResult)
        self.assertTrue(result.success)
        self.assertEqual(result.request_id, "request-123")
        self.assertEqual(result.task_status, "running")
        self.assertEqual(result.error_message, "")
        self.assertEqual(result.task_id, "task-123")

        # Verify call arguments
        self.assertEqual(self.session.call_mcp_tool.call_count, 1)

        retry_times: int = 0
        while retry_times < int(self.max_try_times):
            mock_query_result = OperationResult(
                request_id="request-123",
                success=True,
                data="""{"task_id": "task-123", "status": "running", "result":"", "product": "Task is runnning."}""",
            )
            self.session.call_mcp_tool.return_value = mock_query_result
            query_result = await self.agent.computer.get_task_status(result.task_id)
            self.assertTrue(query_result.success)
            logger.info(
                f"⏳ Task {query_result.task_id} running 🚀: {query_result.task_product}."
            )
            if query_result.task_status == "finished":
                break
            retry_times += 1
            time.sleep(3)
        self.assertTrue(retry_times >= int(self.max_try_times))

    @pytest.mark.asyncio


    async def test_computer_task_execute_success(self):
        """
        Test flux_execute_task method with successful response.
        """
        from agentbay import McpToolResult

        mock_result = McpToolResult(
            request_id="request-123",
            success=True,
            data="""{"task_id": "task-123", "status": "finished", "result":"", "product": "Task completed successfully"}""",
        )
        self.session.call_mcp_tool.return_value = mock_result

        result = await self.agent.computer.execute_task("Hello, Computer Agent")
        self.assertIsInstance(result, ExecutionResult)
        self.assertTrue(result.success)
        self.assertEqual(result.request_id, "request-123")
        self.assertEqual(result.task_status, "running")
        self.assertEqual(result.error_message, "")
        self.assertEqual(result.task_id, "task-123")

    @pytest.mark.asyncio


    async def test_computer_task_terminate_error(self):
        """
        Test terminate_task method with successful response.
        """
        from agentbay import McpToolResult

        mock_result = McpToolResult(
            request_id="request-123",
            success=False,
            data="""{"task_id": "task-123", "status": "failed", "result":"", "product": "Task Failed"}""",
        )
        self.session.call_mcp_tool.return_value = mock_result

        result = await self.agent.computer.terminate_task("task-123")
        self.assertIsInstance(result, ExecutionResult)
        self.assertFalse(result.success)
        self.assertEqual(result.request_id, "request-123")
        self.assertEqual(result.task_status, "failed")

        # Verify call arguments
        self.session.call_mcp_tool.assert_called_once()
        args = self.session.call_mcp_tool.call_args[0][1]
        self.assertEqual(args["task_id"], "task-123")

class TestAsyncAgentBrowser(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.session = DummySession()
        self.agent = AsyncAgent(self.session)
        self.max_try_times = os.environ.get("AGENT_TASK_TIMEOUT")
        if not self.max_try_times:
            self.max_try_times = 5

    @pytest.mark.asyncio


    async def test_browser_task_execute_and_wait_success(self):
        """
        Test flux_execute_task method with successful response.
        """
        from agentbay import McpToolResult

        mock_result = McpToolResult(
            request_id="request-123",
            success=True,
            data="""{"task_id": "task-123", "status": "finished", "result":"", "product": "Task completed successfully"}""",
        )
        self.session.call_mcp_tool.return_value = mock_result

        result = await self.agent.browser.execute_task_and_wait("Hello, Browser Agent", int(self.max_try_times))
        self.assertIsInstance(result, ExecutionResult)
        self.assertTrue(result.success)
        self.assertEqual(result.request_id, "request-123")
        self.assertEqual(result.task_status, "finished")
        self.assertEqual(result.error_message, "")

        # Verify call arguments
        self.assertEqual(self.session.call_mcp_tool.call_count, 2)
        args = self.session.call_mcp_tool.call_args[0][1]
        self.assertEqual(args["task_id"], "task-123")
        logger.info(f"Result of Task Hello, Browser Agent: {result.task_result}")

    @pytest.mark.asyncio


    async def test_browser_execute_task_and_wait_error(self):
        """
        Test execute_task method with error response.
        """
        from agentbay import McpToolResult

        mock_result = McpToolResult(
            request_id="request-123",
            success=False,
            error_message="Task execution failed",
            data="""{"task_id": "task-123", "status": "failed", "result":"", "product": "Task Failed"}""",
        )
        self.session.call_mcp_tool.return_value = mock_result
        result = await self.agent.browser.execute_task_and_wait("Hello, Browser Agent", self.max_try_times)
        self.assertIsInstance(result, ExecutionResult)
        self.assertFalse(result.success)
        self.assertEqual(result.request_id, "request-123")
        self.assertEqual(result.error_message, "Task execution failed")
        self.assertEqual(result.task_status, "failed")
        args = self.session.call_mcp_tool.call_args[0][1]
        self.assertEqual(args["task"], "Hello, Browser Agent")
        logger.info(f"Result of Task Hello, Browser Agent: {result.task_result}")

    @pytest.mark.asyncio


    async def test_browser_task_terminate_success(self):
        """
        Test terminate_task method with successful response.
        """
        from agentbay import McpToolResult

        mock_result = McpToolResult(
            request_id="request-123",
            success=True,
            data="""{"task_id": "task-123", "status": "finished", "result":"", "product": "Task completed successfully"}""",
        )
        self.session.call_mcp_tool.return_value = mock_result

        result = await self.agent.browser.terminate_task("task-123")
        self.assertIsInstance(result, ExecutionResult)
        self.assertTrue(result.success)
        self.assertEqual(result.request_id, "request-123")
        self.assertEqual(result.task_status, "finished")
        self.assertEqual(result.error_message, "")

        # Verify call arguments
        self.session.call_mcp_tool.assert_called_once()
        args = self.session.call_mcp_tool.call_args[0][1]
        self.assertEqual(args["task_id"], "task-123")

    @pytest.mark.asyncio


    async def test_browser_task_execute_timeout(self):
        """
        Test flux_execute_task method with successful response.
        """
        from agentbay import McpToolResult

        mock_result = McpToolResult(
            request_id="request-123",
            success=True,
            data="""{"task_id": "task-123", "status": "finished", "result":"", "product": "Task completed successfully"}""",
        )
        self.session.call_mcp_tool.return_value = mock_result

        result = await self.agent.browser.execute_task("Hello, Browser Agent")
        self.assertIsInstance(result, ExecutionResult)
        self.assertTrue(result.success)
        self.assertEqual(result.request_id, "request-123")
        self.assertEqual(result.task_status, "running")
        self.assertEqual(result.error_message, "")
        self.assertEqual(result.task_id, "task-123")

        # Verify call arguments
        self.assertEqual(self.session.call_mcp_tool.call_count, 1)

        retry_times: int = 0
        while retry_times < int(self.max_try_times):
            mock_query_result = OperationResult(
                request_id="request-123",
                success=True,
                data="""{"task_id": "task-123", "status": "running", "result":"", "product": "Task is runnning."}""",
            )
            self.session.call_mcp_tool.return_value = mock_query_result
            query_result = await self.agent.browser.get_task_status(result.task_id)
            self.assertTrue(query_result.success)
            logger.info(
                f"⏳ Task {query_result.task_id} running 🚀: {query_result.task_product}."
            )
            if query_result.task_status == "finished":
                break
            retry_times += 1
            time.sleep(3)
        self.assertTrue(retry_times >= int(self.max_try_times))

    @pytest.mark.asyncio


    async def test_browser_task_execute_success(self):
        """
        Test flux_execute_task method with successful response.
        """
        from agentbay import McpToolResult

        mock_result = McpToolResult(
            request_id="request-123",
            success=True,
            data="""{"task_id": "task-123", "status": "finished", "result":"", "product": "Task completed successfully"}""",
        )
        self.session.call_mcp_tool.return_value = mock_result

        result = await self.agent.browser.execute_task("Hello, Browser Agent")
        self.assertIsInstance(result, ExecutionResult)
        self.assertTrue(result.success)
        self.assertEqual(result.request_id, "request-123")
        self.assertEqual(result.task_status, "running")
        self.assertEqual(result.error_message, "")
        self.assertEqual(result.task_id, "task-123")

    @pytest.mark.asyncio


    async def test_browser_task_terminate_error(self):
        """
        Test terminate_task method with successful response.
        """
        from agentbay import McpToolResult

        mock_result = McpToolResult(
            request_id="request-123",
            success=False,
            data="""{"task_id": "task-123", "status": "failed", "result":"", "product": "Task Failed"}""",
        )
        self.session.call_mcp_tool.return_value = mock_result

        result = await self.agent.browser.terminate_task("task-123")
        self.assertIsInstance(result, ExecutionResult)
        self.assertFalse(result.success)
        self.assertEqual(result.request_id, "request-123")
        self.assertEqual(result.task_status, "failed")

        # Verify call arguments
        self.session.call_mcp_tool.assert_called_once()
        args = self.session.call_mcp_tool.call_args[0][1]
        self.assertEqual(args["task_id"], "task-123")

if __name__ == "__main__":
    unittest.main()
