import os
import sys
import unittest
from unittest.mock import MagicMock, Mock, patch

from agentbay import AgentBay
from agentbay import CreateSessionParams

# Add the parent directory to the path so we can import the agentbay package
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)


class TestAsyncRefactoredMethods(unittest.TestCase):
    """Test cases for refactored methods in AgentBay class."""

    def setUp(self):
        """Set up test fixtures."""
        self.agent_bay = AgentBay(api_key="test-api-key")

    def test_build_session_from_response(self):
        """Test _build_session_from_response method."""
        # Mock response data
        response_data = {
            "SessionId": "test-session-123",
            "ResourceUrl": "https://test.example.com",
            "NetworkInterfaceIp": "192.168.1.1",
            "HttpPort": 8080,
            "Token": "test-token",
        }

        # Mock params
        params = Mock()
        params.is_vpc = True
        params.enable_browser_replay = True
        params.image_id = "test-image"
        params.extra_configs = None

        # Mock session - need to patch the correct path after refactoring
        with patch("agentbay._sync.agentbay.Session") as mock_session_class:
            mock_session = Mock()
            mock_session_class.return_value = mock_session

            # Call the method
            result = self.agent_bay._build_session_from_response(response_data, params)

            # Verify session was created with correct parameters
            mock_session_class.assert_called_once_with(
                self.agent_bay, "test-session-123"
            )

            # Verify session properties were set
            self.assertEqual(mock_session.is_vpc, True)
            self.assertEqual(mock_session.network_interface_ip, "192.168.1.1")
            self.assertEqual(mock_session.http_port, 8080)
            self.assertEqual(mock_session.token, "test-token")
            self.assertEqual(mock_session.resource_url, "https://test.example.com")
            self.assertEqual(mock_session.enableBrowserReplay, True)

            # Verify result
            self.assertEqual(result, mock_session)

    def test_fetch_mcp_tools_for_vpc_session(self):
        """Test _fetch_mcp_tools_for_vpc_session method."""
        # Mock session
        mock_session = Mock()
        mock_tools_result = Mock()
        mock_tools_result.tools = ["tool1", "tool2", "tool3"]
        mock_tools_result.request_id = "test-request-123"
        mock_session.list_mcp_tools = MagicMock(return_value=mock_tools_result)

        # Call the method
        self.agent_bay._fetch_mcp_tools_for_vpc_session(mock_session)

        # Verify list_mcp_tools was called
        mock_session.list_mcp_tools.assert_called_once()

    def test_fetch_mcp_tools_for_vpc_session_with_error(self):
        """Test _fetch_mcp_tools_for_vpc_session method with error."""
        # Mock session that raises an exception
        mock_session = Mock()
        mock_session.list_mcp_tools = MagicMock(side_effect=Exception("Test error"))

        # Call the method - should not raise an exception
        self.agent_bay._fetch_mcp_tools_for_vpc_session(mock_session)

        # Verify list_mcp_tools was called
        mock_session.list_mcp_tools.assert_called_once()

    def test_wait_for_context_synchronization(self):
        """Test _wait_for_context_synchronization method."""
        # Mock session
        mock_session = Mock()
        mock_context = Mock()
        mock_session.context = mock_context

        # Mock context info result
        mock_context_item = Mock()
        mock_context_item.context_id = "test-context-123"
        mock_context_item.status = "Success"
        mock_context_item.path = "/test/path"
        mock_context_item.error_message = None

        mock_info_result = Mock()
        mock_info_result.context_status_data = [mock_context_item]
        mock_context.info = MagicMock(return_value=mock_info_result)

        # Call the method
        self.agent_bay._wait_for_context_synchronization(mock_session)

        # Verify context.info was called
        mock_context.info.assert_called_once()

    def test_log_request_debug_info(self):
        """Test _log_request_debug_info method."""
        # Mock request
        mock_request = Mock()
        mock_request.to_map.return_value = {
            "Authorization": "Bearer test-token-1234567890",
            "OtherField": "test-value",
        }

        # Call the method
        self.agent_bay._log_request_debug_info(mock_request)

        # Verify to_map was called
        mock_request.to_map.assert_called_once()

    def test_log_request_debug_info_with_short_auth(self):
        """Test _log_request_debug_info method with short authorization."""
        # Mock request with short authorization
        mock_request = Mock()
        mock_request.to_map.return_value = {
            "Authorization": "short",
            "OtherField": "test-value",
        }

        # Call the method
        self.agent_bay._log_request_debug_info(mock_request)

        # Verify to_map was called
        mock_request.to_map.assert_called_once()

    def test_log_request_debug_info_with_exception(self):
        """Test _log_request_debug_info method with exception."""
        # Mock request that raises an exception
        mock_request = Mock()
        mock_request.to_map.side_effect = Exception("Test error")

        # Call the method - should not raise an exception
        self.agent_bay._log_request_debug_info(mock_request)

        # Verify to_map was called
        mock_request.to_map.assert_called_once()


if __name__ == "__main__":
    unittest.main()
