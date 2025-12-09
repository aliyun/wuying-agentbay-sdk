"""
Unit tests for Session.call_mcp_tool() public API.

This test suite follows TDD principles:
1. Write tests first (red)
2. Implement functionality (green)
3. Refactor if needed
"""

import json
import pytest
import unittest
from unittest.mock import MagicMock, MagicMock, Mock, patch


class DummyAgentBay:
    """Mock AgentBay for testing."""

    def __init__(self):
        self.client = MagicMock()
        self.api_key = "test_api_key"

    def get_api_key(self):
        return self.api_key

    def get_client(self):
        return self.client


class TestAsyncSessionCallMcpTool(unittest.TestCase):
    """Test cases for Session.call_mcp_tool() public API."""

    def setUp(self):
        """Set up test fixtures."""
        from agentbay import Session

        self.agent_bay = DummyAgentBay()
        self.session_id = "test_session_id"
        self.session = Session(self.agent_bay, self.session_id)

    def test_call_mcp_tool_method_exists(self):
        """Test that call_mcp_tool method exists and is public."""
        self.assertTrue(hasattr(self.session, "call_mcp_tool"))
        self.assertTrue(callable(getattr(self.session, "call_mcp_tool")))

    @patch("agentbay._sync.session.CallMcpToolRequest")
    @patch("agentbay._sync.session.extract_request_id")
    @pytest.mark.sync

    def test_call_mcp_tool_success_non_vpc(
        self, mock_extract_request_id, MockCallMcpToolRequest
    ):
        """Test successful MCP tool call in non-VPC mode."""
        # Setup mocks
        mock_request = MagicMock()
        mock_response = MagicMock()
        MockCallMcpToolRequest.return_value = mock_request
        mock_extract_request_id.return_value = "request-123"
        self.agent_bay.client.call_mcp_tool = MagicMock(
            return_value=mock_response
        )

        # Mock response structure
        mock_response.to_map.return_value = {
            "body": {
                "Data": json.dumps(
                    {
                        "content": [{"type": "text", "text": "command output"}],
                        "isError": False,
                    }
                ),
                "Success": True,
            }
        }

        # Call the method
        result = self.session.call_mcp_tool(
            "shell", {"command": "ls", "timeout_ms": 1000}
        )

        # Assertions
        self.assertIsNotNone(result)
        self.assertEqual(result.request_id, "request-123")
        self.assertTrue(result.success)
        self.assertEqual(result.data, "command output")
        self.assertEqual(result.error_message, "")

        # Verify API was called correctly
        MockCallMcpToolRequest.assert_called_once()
        call_args = MockCallMcpToolRequest.call_args
        self.assertEqual(call_args[1]["authorization"], "Bearer test_api_key")
        self.assertEqual(call_args[1]["session_id"], "test_session_id")
        self.assertEqual(call_args[1]["name"], "shell")
        args_dict = json.loads(call_args[1]["args"])
        self.assertEqual(args_dict["command"], "ls")
        self.assertEqual(args_dict["timeout_ms"], 1000)

    @patch("agentbay._sync.session.CallMcpToolRequest")
    @patch("agentbay._sync.session.extract_request_id")
    @pytest.mark.sync

    def test_call_mcp_tool_with_error_response(
        self, mock_extract_request_id, MockCallMcpToolRequest
    ):
        """Test MCP tool call with error response."""
        # Setup mocks
        mock_request = MagicMock()
        mock_response = MagicMock()
        MockCallMcpToolRequest.return_value = mock_request
        mock_extract_request_id.return_value = "request-456"
        self.agent_bay.client.call_mcp_tool = MagicMock(
            return_value=mock_response
        )

        # Mock error response
        mock_response.to_map.return_value = {
            "body": {
                "Data": json.dumps(
                    {
                        "content": [
                            {"type": "text", "text": "Error: command not found"}
                        ],
                        "isError": True,
                    }
                ),
                "Success": False,
            }
        }

        # Call the method
        result = self.session.call_mcp_tool("shell", {"command": "invalid_cmd"})

        # Assertions
        self.assertIsNotNone(result)
        self.assertEqual(result.request_id, "request-456")
        self.assertFalse(result.success)
        self.assertIn("Error", result.error_message)

    @patch("agentbay._sync.session.CallMcpToolRequest")
    @patch("agentbay._sync.session.extract_request_id")
    @pytest.mark.sync

    def test_call_mcp_tool_api_exception(
        self, mock_extract_request_id, MockCallMcpToolRequest
    ):
        """Test MCP tool call when API raises exception."""
        # Setup mocks
        mock_request = MagicMock()
        MockCallMcpToolRequest.return_value = mock_request
        mock_extract_request_id.return_value = "request-789"
        self.agent_bay.client.call_mcp_tool = MagicMock(
            side_effect=Exception("Network error")
        )

        # Call the method
        result = self.session.call_mcp_tool("shell", {"command": "ls"})

        # Assertions
        self.assertIsNotNone(result)
        self.assertFalse(result.success)
        self.assertIn("Network error", result.error_message)

    @patch("httpx.Client")
    @pytest.mark.sync

    def test_call_mcp_tool_vpc_mode_success(self, mock_httpx_client):
        """Test successful MCP tool call in VPC mode."""
        # Setup VPC session
        self.session.is_vpc = True
        self.session.network_interface_ip = "192.168.1.100"
        self.session.http_port = "8080"
        self.session.token = "vpc_token_123"
        # Create a proper mock tool
        mock_tool = MagicMock()
        mock_tool.name = "shell"
        mock_tool.server = "test_server"
        self.session.mcp_tools = [mock_tool]

        # Mock HTTP response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "content": [{"type": "text", "text": "vpc output"}],
            "isError": False,
        }

        # Setup httpx async client mock
        # async with httpx.AsyncClient() as client: await client.get(...)
        mock_client_instance = MagicMock()
        mock_httpx_client.return_value.__enter__ = MagicMock(
            return_value=mock_client_instance
        )
        mock_httpx_client.return_value.__exit__ = MagicMock(return_value=None)
        mock_client_instance.get = MagicMock(return_value=mock_response)

        # Call the method
        result = self.session.call_mcp_tool("shell", {"command": "pwd"})

        # Assertions
        self.assertIsNotNone(result)
        self.assertTrue(result.success)
        self.assertEqual(result.data, "vpc output")

        # Verify HTTP request was made
        mock_client_instance.get.assert_called_once()
        call_args = mock_client_instance.get.call_args
        self.assertIn("192.168.1.100", call_args[0][0])
        self.assertIn("8080", call_args[0][0])

    @pytest.mark.sync


    def test_call_mcp_tool_vpc_mode_server_not_found(self):
        """Test VPC mode when server for tool is not found."""
        # Setup VPC session without matching tool
        self.session.is_vpc = True
        self.session.network_interface_ip = "192.168.1.100"
        self.session.http_port = "8080"
        self.session.token = "vpc_token_123"
        self.session.mcp_tools = []  # No tools available

        # Call the method
        result = self.session.call_mcp_tool("nonexistent_tool", {})

        # Assertions
        self.assertIsNotNone(result)
        self.assertFalse(result.success)
        self.assertIn("server not found", result.error_message.lower())

    @pytest.mark.sync


    def test_call_mcp_tool_vpc_mode_incomplete_config(self):
        """Test VPC mode with incomplete network configuration."""
        # Setup VPC session with incomplete config
        self.session.is_vpc = True
        self.session.network_interface_ip = ""  # Missing
        self.session.http_port = ""  # Missing
        self.session.token = "vpc_token_123"
        # Add a tool so it doesn't fail on "server not found" first
        mock_tool = MagicMock()
        mock_tool.name = "shell"
        mock_tool.server = "test_server"
        self.session.mcp_tools = [mock_tool]

        # Call the method
        result = self.session.call_mcp_tool("shell", {"command": "ls"})

        # Assertions
        self.assertIsNotNone(result)
        self.assertFalse(result.success)
        self.assertIn("network configuration", result.error_message.lower())

    @patch("agentbay._sync.session.CallMcpToolRequest")
    @patch("agentbay._sync.session.extract_request_id")
    @pytest.mark.sync

    def test_call_mcp_tool_with_custom_timeouts(
        self, mock_extract_request_id, MockCallMcpToolRequest
    ):
        """Test MCP tool call with custom timeout parameters."""
        # Setup mocks
        mock_request = MagicMock()
        mock_response = MagicMock()
        MockCallMcpToolRequest.return_value = mock_request
        mock_extract_request_id.return_value = "request-999"
        self.agent_bay.client.call_mcp_tool = MagicMock(
            return_value=mock_response
        )

        # Mock response
        mock_response.to_map.return_value = {
            "body": {
                "Data": json.dumps(
                    {
                        "content": [{"type": "text", "text": "output"}],
                        "isError": False,
                    }
                ),
                "Success": True,
            }
        }

        # Call with custom timeouts
        result = self.session.call_mcp_tool(
            "shell", {"command": "ls"}, read_timeout=60, connect_timeout=10
        )

        # Assertions
        self.assertTrue(result.success)

        # Verify timeouts were passed to client
        self.agent_bay.client.call_mcp_tool.assert_called_once()
        call_kwargs = self.agent_bay.client.call_mcp_tool.call_args[1]
        self.assertEqual(call_kwargs.get("read_timeout"), 60)
        self.assertEqual(call_kwargs.get("connect_timeout"), 10)

    @patch("agentbay._sync.session.CallMcpToolRequest")
    @patch("agentbay._sync.session.extract_request_id")
    @pytest.mark.sync

    def test_call_mcp_tool_with_complex_args(
        self, mock_extract_request_id, MockCallMcpToolRequest
    ):
        """Test MCP tool call with complex nested arguments."""
        # Setup mocks
        mock_request = MagicMock()
        mock_response = MagicMock()
        MockCallMcpToolRequest.return_value = mock_request
        mock_extract_request_id.return_value = "request-complex"
        self.agent_bay.client.call_mcp_tool = MagicMock(
            return_value=mock_response
        )

        # Mock response
        mock_response.to_map.return_value = {
            "body": {
                "Data": json.dumps(
                    {
                        "content": [{"type": "text", "text": "processed"}],
                        "isError": False,
                    }
                ),
                "Success": True,
            }
        }

        # Complex arguments
        complex_args = {
            "input_data": "sample",
            "options": {
                "format": "json",
                "compress": True,
                "filters": ["filter1", "filter2"],
            },
            "metadata": {"user": "test_user", "timestamp": 1234567890},
        }

        # Call the method
        result = self.session.call_mcp_tool("data_processor", complex_args)

        # Assertions
        self.assertTrue(result.success)

        # Verify args were serialized correctly
        call_args = MockCallMcpToolRequest.call_args[1]
        args_dict = json.loads(call_args["args"])
        self.assertEqual(args_dict["input_data"], "sample")
        self.assertEqual(args_dict["options"]["format"], "json")
        self.assertTrue(args_dict["options"]["compress"])
        self.assertEqual(len(args_dict["options"]["filters"]), 2)

    @pytest.mark.sync


    def test_call_mcp_tool_return_type(self):
        """Test that call_mcp_tool returns McpToolResult type."""
        from agentbay import McpToolResult

        # Mock the client
        mock_response = MagicMock()
        mock_response.to_map.return_value = {
            "body": {
                "Data": json.dumps(
                    {
                        "content": [{"type": "text", "text": "output"}],
                        "isError": False,
                    }
                ),
                "Success": True,
            }
        }
        self.agent_bay.client.call_mcp_tool = MagicMock(
            return_value=mock_response
        )

        # Call the method
        result = self.session.call_mcp_tool("shell", {"command": "ls"})

        # Verify return type
        self.assertIsInstance(result, McpToolResult)
        self.assertTrue(hasattr(result, "request_id"))
        self.assertTrue(hasattr(result, "success"))
        self.assertTrue(hasattr(result, "data"))
        self.assertTrue(hasattr(result, "error_message"))


class TestAsyncMcpToolResult(unittest.TestCase):
    """Test cases for McpToolResult model."""

    def test_mcp_tool_result_initialization(self):
        """Test McpToolResult can be initialized with all fields."""
        from agentbay import McpToolResult

        result = McpToolResult(
            request_id="req-123", success=True, data="test data", error_message=""
        )

        self.assertEqual(result.request_id, "req-123")
        self.assertTrue(result.success)
        self.assertEqual(result.data, "test data")
        self.assertEqual(result.error_message, "")

    def test_mcp_tool_result_defaults(self):
        """Test McpToolResult default values."""
        from agentbay import McpToolResult

        result = McpToolResult()

        self.assertEqual(result.request_id, "")
        self.assertFalse(result.success)
        self.assertEqual(result.data, "")
        self.assertEqual(result.error_message, "")


if __name__ == "__main__":
    unittest.main()
