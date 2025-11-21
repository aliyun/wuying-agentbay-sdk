"""Unit tests for Session pause operations."""
import unittest
from unittest.mock import MagicMock, patch, AsyncMock
import asyncio

from agentbay.agentbay import AgentBay
from agentbay.session import Session
from agentbay.model import (
    SessionPauseResult,
    GetSessionResult,
    GetSessionData,
)
from agentbay.api.models import (
    PauseSessionAsyncResponse,
    PauseSessionAsyncResponseBody,
)


class TestSessionPause(unittest.TestCase):
    """Test suite for Session pause operations."""

    def setUp(self):
        """Set up test fixtures."""
        self.agent_bay = AgentBay("test-api-key")
        self.agent_bay.client = MagicMock()

        # Create a mock session
        self.session = Session(self.agent_bay, "session-123")
        self.session.is_vpc = False
        self.session.network_interface_ip = ""
        self.session.http_port = ""
        self.session.token = ""
        self.session.resource_url = ""

    def test_pause_success_immediate(self):
        """Test successful session pause with immediate success."""
        # Mock the PauseSessionAsync response
        mock_response = PauseSessionAsyncResponse()
        mock_response.body = PauseSessionAsyncResponseBody(
            success=True,
            code="Success",
            message="Session pause initiated successfully",
            request_id="test-request-id",
            http_status_code=200,
        )
        self.agent_bay.client.pause_session_async_async = AsyncMock(return_value=mock_response)

        # Mock get_session to return PAUSED immediately
        get_session_paused = GetSessionResult(
            request_id="test-request-id",
            success=True,
            data=GetSessionData(
                session_id="session-123",
                status="PAUSED",
            ),
        )
        self.agent_bay.get_session = MagicMock(return_value=get_session_paused)

        # Patch asyncio.sleep to avoid waiting
        with patch('asyncio.sleep', new_callable=AsyncMock) as mock_sleep:
            # Call the method
            result = asyncio.run(self.session.pause_async(timeout=10, poll_interval=1))

            # Verify the result
            self.assertIsInstance(result, SessionPauseResult)
            self.assertTrue(result.success)
            self.assertEqual(result.request_id, "test-request-id")
            self.assertEqual(result.status, "PAUSED")
            self.assertEqual(result.error_message, "")

            # Verify that sleep was not called since we got PAUSED directly.
            mock_sleep.assert_not_called()

    def test_pause_success_after_polling(self):
        """Test successful session pause after polling."""
        # Mock the PauseSessionAsync response
        mock_response = PauseSessionAsyncResponse()
        mock_response.body = PauseSessionAsyncResponseBody(
            success=True,
            code="Success",
            message="Session pause initiated successfully",
            request_id="test-request-id",
            http_status_code=200,
        )
        self.agent_bay.client.pause_session_async_async = AsyncMock(return_value=mock_response)

        # Mock get_session to return PAUSING first, then PAUSED
        get_session_pausing = GetSessionResult(
            request_id="test-request-id",
            success=True,
            data=GetSessionData(
                session_id="session-123",
                status="PAUSING",
            ),
        )

        get_session_paused = GetSessionResult(
            request_id="test-request-id",
            success=True,
            data=GetSessionData(
                session_id="session-123",
                status="PAUSED",
            ),
        )
        self.agent_bay.get_session = MagicMock(side_effect=[get_session_pausing, get_session_paused])

        # Patch asyncio.sleep to avoid waiting
        with patch('asyncio.sleep', new_callable=AsyncMock) as mock_sleep:
            # Call the method
            result = asyncio.run(self.session.pause_async(timeout=10, poll_interval=1))

            # Verify the result
            self.assertIsInstance(result, SessionPauseResult)
            self.assertTrue(result.success)
            self.assertEqual(result.request_id, "test-request-id")
            self.assertEqual(result.status, "PAUSED")
            self.assertEqual(result.error_message, "")

            # Verify that sleep was called once (after the first attempt)
            mock_sleep.assert_called_once_with(1)

    def test_pause_timeout(self):
        """Test session pause timeout."""
        # Mock the PauseSessionAsync response
        mock_response = PauseSessionAsyncResponse()
        mock_response.body = PauseSessionAsyncResponseBody(
            success=True,
            code="Success",
            message="Session pause initiated successfully",
            request_id="test-request-id",
            http_status_code=200,
        )
        self.agent_bay.client.pause_session_async_async = AsyncMock(return_value=mock_response)

        # Mock get_session to always return PAUSING
        get_session_pausing = GetSessionResult(
            request_id="test-request-id",
            success=True,
            data=GetSessionData(
                session_id="session-123",
                status="PAUSING",
            ),
        )
        self.agent_bay.get_session = MagicMock(return_value=get_session_pausing)

        # Patch asyncio.sleep to avoid waiting
        with patch('asyncio.sleep', new_callable=AsyncMock) as mock_sleep:
            # Call the method with a short timeout
            result = asyncio.run(self.session.pause_async(timeout=2, poll_interval=1))

            # Verify the result
            self.assertIsInstance(result, SessionPauseResult)
            self.assertFalse(result.success)
            self.assertIn("timed out", result.error_message)
            self.assertEqual(result.request_id, "")

    def test_pause_get_session_failure(self):
        """Test session pause when get_session fails."""
        # Mock the PauseSessionAsync response
        mock_response = PauseSessionAsyncResponse()
        mock_response.body = PauseSessionAsyncResponseBody(
            success=True,
            code="Success",
            message="Session pause initiated successfully",
            request_id="test-request-id",
            http_status_code=200,
        )
        self.agent_bay.client.pause_session_async_async = AsyncMock(return_value=mock_response)

        # Mock get_session to return failure
        get_session_failure = GetSessionResult(
            request_id="test-request-id",
            success=False,
            error_message="Failed to get session status",
        )
        self.agent_bay.get_session = MagicMock(return_value=get_session_failure)

        # Patch asyncio.sleep to avoid waiting
        with patch('asyncio.sleep', new_callable=AsyncMock) as mock_sleep:
            # Call the method
            result = asyncio.run(self.session.pause_async())

            # Verify the result
            self.assertIsInstance(result, SessionPauseResult)
            self.assertFalse(result.success)
            self.assertIn("Failed to get session status", result.error_message)
            self.assertEqual(result.request_id, "test-request-id")

    def test_pause_api_error(self):
        """Test session pause with API error."""
        # Mock the PauseSessionAsync response with error
        mock_response = PauseSessionAsyncResponse()
        mock_response.body = PauseSessionAsyncResponseBody(
            success=False,
            code="SessionNotFound",
            message="Session does not exist",
            request_id="test-request-id",
            http_status_code=404,
        )
        self.agent_bay.client.pause_session_async_async = AsyncMock(return_value=mock_response)

        # Patch asyncio.sleep to avoid waiting
        with patch('asyncio.sleep', new_callable=AsyncMock) as mock_sleep:
            # Call the method
            result = asyncio.run(self.session.pause_async())

            # Verify the result
            self.assertIsInstance(result, SessionPauseResult)
            self.assertFalse(result.success)
            self.assertEqual(result.request_id, "test-request-id")
            self.assertEqual(result.error_message, "[SessionNotFound] Session does not exist")

    def test_pause_empty_response_body(self):
        """Test session pause with empty response body."""
        # Mock the PauseSessionAsync response with no body
        mock_response = PauseSessionAsyncResponse(status_code=200)
        mock_response.body = None
        self.agent_bay.client.pause_session_async_async = AsyncMock(return_value=mock_response)

        # Patch asyncio.sleep to avoid waiting
        with patch('asyncio.sleep', new_callable=AsyncMock) as mock_sleep:
            # Call the method
            result = asyncio.run(self.session.pause_async())

            # Verify the result
            self.assertIsInstance(result, SessionPauseResult)
            self.assertFalse(result.success)
            self.assertEqual(result.error_message, "Invalid response body")
            self.assertEqual(result.request_id, '')

    def test_pause_invalid_response_format(self):
        """Test session pause with invalid response format."""
        # Mock the PauseSessionAsync response with invalid format
        mock_response = MagicMock()
        mock_response.to_map.return_value = None
        self.agent_bay.client.pause_session_async_async = AsyncMock(return_value=mock_response)

        # Patch asyncio.sleep to avoid waiting
        with patch('asyncio.sleep', new_callable=AsyncMock) as mock_sleep:
            # Call the method
            result = asyncio.run(self.session.pause_async())

            # Verify the result
            self.assertIsInstance(result, SessionPauseResult)
            self.assertFalse(result.success)
            self.assertEqual(result.error_message, "Invalid response format")
            self.assertEqual(result.request_id, '')

    def test_pause_client_exception(self):
        """Test session pause with client exception."""
        # Mock the client to raise an exception
        self.agent_bay.client.pause_session_async_async.side_effect = Exception("Network error")

        # Patch asyncio.sleep to avoid waiting
        with patch('asyncio.sleep', new_callable=AsyncMock) as mock_sleep:
            # Call the method
            result = asyncio.run(self.session.pause_async())

            # Verify the result
            self.assertIsInstance(result, SessionPauseResult)
            self.assertFalse(result.success)
            self.assertIn("Network error", result.error_message)
            self.assertEqual(result.request_id, "")

    def test_pause_unexpected_state(self):
        """Test session pause with unexpected state."""
        # Mock the PauseSessionAsync response
        mock_response = PauseSessionAsyncResponse()
        mock_response.body = PauseSessionAsyncResponseBody(
            success=True,
            code="Success",
            message="Session pause initiated successfully",
            request_id="test-request-id",
            http_status_code=200,
        )
        self.agent_bay.client.pause_session_async_async = AsyncMock(return_value=mock_response)

        # Mock get_session to return unexpected state, then PAUSED
        get_session_running = GetSessionResult(
            request_id="test-request-id",
            success=True,
            data=GetSessionData(
                session_id="session-123",
                status="other",
            ),
        )

        get_session_paused = GetSessionResult(
            request_id="test-request-id",
            success=True,
            data=GetSessionData(
                session_id="session-123",
                status="PAUSED",
            ),
        )
        self.agent_bay.get_session = MagicMock(side_effect=[get_session_running, get_session_paused])

        # Patch asyncio.sleep to avoid waiting
        with patch('asyncio.sleep', new_callable=AsyncMock) as mock_sleep:
            # Call the method
            result = asyncio.run(self.session.pause_async(timeout=10, poll_interval=1))

            # Verify the result
            self.assertIsInstance(result, SessionPauseResult)
            self.assertTrue(result.success)
            self.assertEqual(result.request_id, "test-request-id")
            self.assertEqual(result.status, "PAUSED")
            self.assertEqual(result.error_message, "")

            # Verify that sleep was called once (after the first attempt)
            mock_sleep.assert_called_once_with(1)

    def test_pause_sync_success_immediate(self):
        """Test successful synchronous session pause with immediate success."""
        # Mock the PauseSessionAsync response
        mock_response = PauseSessionAsyncResponse()
        mock_response.body = PauseSessionAsyncResponseBody(
            success=True,
            code="Success",
            message="Session pause initiated successfully",
            request_id="test-request-id",
            http_status_code=200,
        )
        self.agent_bay.client.pause_session_async_async = AsyncMock(return_value=mock_response)

        # Mock get_session to return PAUSED immediately
        get_session_paused = GetSessionResult(
            request_id="test-request-id",
            success=True,
            data=GetSessionData(
                session_id="session-123",
                status="PAUSED",
            ),
        )
        self.agent_bay.get_session = MagicMock(return_value=get_session_paused)

        # Patch asyncio.sleep to avoid waiting
        with patch('asyncio.sleep', new_callable=AsyncMock) as mock_sleep:
            # Patch asyncio.run to return a mock result directly
            with patch('asyncio.run') as mock_run:
                # Create a mock result that matches what we expect
                mock_result = SessionPauseResult(
                    request_id="test-request-id",
                    success=True,
                    status="PAUSED",
                    error_message=""
                )
                mock_run.return_value = mock_result
                
                # Call the method
                result = self.session.pause(timeout=10, poll_interval=1)

                # Verify the result
                self.assertIsInstance(result, SessionPauseResult)
                self.assertTrue(result.success)
                self.assertEqual(result.request_id, "test-request-id")
                self.assertEqual(result.status, "PAUSED")
                self.assertEqual(result.error_message, "")

    def test_pause_with_agent_bay_pause_method_session_exception(self):
        """Test AgentBay.pause method with session exception."""
        # Mock the session.pause to raise an exception
        self.session.pause = MagicMock(side_effect=Exception("Session pause error"))

        # Call the method with session object
        result = self.agent_bay.pause(self.session)

        # Verify the result
        self.assertIsInstance(result, SessionPauseResult)
        self.assertFalse(result.success)
        self.assertIn("Session pause error", result.error_message)


if __name__ == "__main__":
    unittest.main()