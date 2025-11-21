"""Unit tests for Session resume operations."""
import unittest
from unittest.mock import MagicMock, patch, AsyncMock
import asyncio

from agentbay.agentbay import AgentBay
from agentbay.session import Session
from agentbay.model import (
    SessionResumeResult,
    GetSessionResult,
    GetSessionData,
)
from agentbay.api.models import (
    ResumeSessionAsyncResponse,
    ResumeSessionAsyncResponseBody,
)


class TestSessionResume(unittest.TestCase):
    """Test suite for Session resume operations."""

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

    def test_resume_async_success_immediate(self):
        """Test successful async session resume with immediate success. """
        # Mock the ResumeSessionAsync response
        mock_response = ResumeSessionAsyncResponse()
        mock_response.body = ResumeSessionAsyncResponseBody(
            success=True,
            code="Success",
            message="Session resume initiated successfully",
            request_id="test-request-id",
            http_status_code=200,
        )
        self.agent_bay.client.resume_session_async_async = AsyncMock(return_value=mock_response)

        # Mock get_session to return RUNNING immediately
        get_session_running = GetSessionResult(
            request_id="test-request-id",
            success=True,
            data=GetSessionData(
                session_id="session-123",
                status="RUNNING",
            ),
        )
        self.agent_bay.get_session = MagicMock(return_value=get_session_running)

        # Patch asyncio.sleep to avoid waiting
        with patch('asyncio.sleep', new_callable=AsyncMock) as mock_sleep:
            # Call the method
            result = asyncio.run(self.session.resume_async(timeout=10, poll_interval=1))

            # Verify the result
            self.assertIsInstance(result, SessionResumeResult)
            self.assertTrue(result.success)
            self.assertEqual(result.request_id, "test-request-id")
            self.assertEqual(result.status, "RUNNING")
            self.assertEqual(result.error_message, "")

            # Verify that sleep was not called since we got RUNNING directly.
            mock_sleep.assert_not_called()

    def test_resume_async_success_after_polling(self):
        """Test successful async session resume after polling."""
        # Mock the ResumeSessionAsync response
        mock_response = ResumeSessionAsyncResponse()
        mock_response.body = ResumeSessionAsyncResponseBody(
            success=True,
            code="Success",
            message="Session resume initiated successfully",
            request_id="test-request-id",
            http_status_code=200,
        )
        self.agent_bay.client.resume_session_async_async = AsyncMock(return_value=mock_response)

        # Mock get_session to return RESUMING first, then RUNNING
        get_session_resuming = GetSessionResult(
            request_id="test-request-id",
            success=True,
            data=GetSessionData(
                session_id="session-123",
                status="RESUMING",
            ),
        )

        get_session_running = GetSessionResult(
            request_id="test-request-id",
            success=True,
            data=GetSessionData(
                session_id="session-123",
                status="RUNNING",
            ),
        )
        self.agent_bay.get_session = MagicMock(side_effect=[get_session_resuming, get_session_running])

        # Patch asyncio.sleep to avoid waiting
        with patch('asyncio.sleep', new_callable=AsyncMock) as mock_sleep:
            # Call the method
            result = asyncio.run(self.session.resume_async(timeout=10, poll_interval=1))

            # Verify the result
            self.assertIsInstance(result, SessionResumeResult)
            self.assertTrue(result.success)
            self.assertEqual(result.request_id, "test-request-id")
            self.assertEqual(result.status, "RUNNING")
            self.assertEqual(result.error_message, "")

            # Verify that sleep was called once (after the first attempt)
            mock_sleep.assert_called_once_with(1)

    def test_resume_async_timeout(self):
        """Test async session resume timeout."""
        # Mock the ResumeSessionAsync response
        mock_response = ResumeSessionAsyncResponse()
        mock_response.body = ResumeSessionAsyncResponseBody(
            success=True,
            code="Success",
            message="Session resume initiated successfully",
            request_id="test-request-id",
            http_status_code=200,
        )
        self.agent_bay.client.resume_session_async_async = AsyncMock(return_value=mock_response)

        # Mock get_session to always return RESUMING
        get_session_resuming = GetSessionResult(
            request_id="test-request-id",
            success=True,
            data=GetSessionData(
                session_id="session-123",
                status="RESUMING",
            ),
        )
        self.agent_bay.get_session = MagicMock(return_value=get_session_resuming)

        # Patch asyncio.sleep to avoid waiting
        with patch('asyncio.sleep', new_callable=AsyncMock) as mock_sleep:
            # Call the method with a short timeout
            result = asyncio.run(self.session.resume_async(timeout=2, poll_interval=1))

            # Verify the result
            self.assertIsInstance(result, SessionResumeResult)
            self.assertFalse(result.success)
            self.assertIn("timed out", result.error_message)
            self.assertEqual(result.request_id, "")

    def test_resume_async_get_session_failure(self):
        """Test async session resume when get_session fails."""
        # Mock the ResumeSessionAsync response
        mock_response = ResumeSessionAsyncResponse()
        mock_response.body = ResumeSessionAsyncResponseBody(
            success=True,
            code="Success",
            message="Session resume initiated successfully",
            request_id="test-request-id",
            http_status_code=200,
        )
        self.agent_bay.client.resume_session_async_async = AsyncMock(return_value=mock_response)

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
            result = asyncio.run(self.session.resume_async())

            # Verify the result
            self.assertIsInstance(result, SessionResumeResult)
            self.assertFalse(result.success)
            self.assertIn("Failed to get session status", result.error_message)
            self.assertEqual(result.request_id, "test-request-id")

    def test_resume_async_api_error(self):
        """Test async session resume with API error."""
        # Mock the ResumeSessionAsync response with error
        mock_response = ResumeSessionAsyncResponse()
        mock_response.body = ResumeSessionAsyncResponseBody(
            success=False,
            code="SessionNotFound",
            message="Session does not exist",
            request_id="test-request-id",
            http_status_code=404,
        )
        self.agent_bay.client.resume_session_async_async = AsyncMock(return_value=mock_response)

        # Patch asyncio.sleep to avoid waiting
        with patch('asyncio.sleep', new_callable=AsyncMock) as mock_sleep:
            # Call the method
            result = asyncio.run(self.session.resume_async())

            # Verify the result
            self.assertIsInstance(result, SessionResumeResult)
            self.assertFalse(result.success)
            self.assertEqual(result.request_id, "test-request-id")
            self.assertEqual(result.error_message, "[SessionNotFound] Session does not exist")

    def test_resume_async_empty_response_body(self):
        """Test async session resume with empty response body."""
        # Mock the ResumeSessionAsync response with no body
        mock_response = ResumeSessionAsyncResponse(status_code=200)
        mock_response.body = None
        self.agent_bay.client.resume_session_async_async = AsyncMock(return_value=mock_response)

        # Patch asyncio.sleep to avoid waiting
        with patch('asyncio.sleep', new_callable=AsyncMock) as mock_sleep:
            # Call the method
            result = asyncio.run(self.session.resume_async())

            # Verify the result
            self.assertIsInstance(result, SessionResumeResult)
            self.assertFalse(result.success)
            self.assertEqual(result.error_message, "Invalid response body")
            self.assertEqual(result.request_id, '')

    def test_resume_async_invalid_response_format(self):
        """Test async session resume with invalid response format."""
        # Mock the ResumeSessionAsync response with invalid format
        mock_response = MagicMock()
        mock_response.to_map.return_value = None
        self.agent_bay.client.resume_session_async_async = AsyncMock(return_value=mock_response)

        # Patch asyncio.sleep to avoid waiting
        with patch('asyncio.sleep', new_callable=AsyncMock) as mock_sleep:
            # Call the method
            result = asyncio.run(self.session.resume_async())

            # Verify the result
            self.assertIsInstance(result, SessionResumeResult)
            self.assertFalse(result.success)
            self.assertEqual(result.error_message, "Invalid response format")
            self.assertEqual(result.request_id, '')

    def test_resume_async_client_exception(self):
        """Test async session resume with client exception."""
        # Mock the client to raise an exception
        self.agent_bay.client.resume_session_async_async.side_effect = Exception("Network error")

        # Patch asyncio.sleep to avoid waiting
        with patch('asyncio.sleep', new_callable=AsyncMock) as mock_sleep:
            # Call the method
            result = asyncio.run(self.session.resume_async())

            # Verify the result
            self.assertIsInstance(result, SessionResumeResult)
            self.assertFalse(result.success)
            self.assertIn("Network error", result.error_message)
            self.assertEqual(result.request_id, "")

    def test_resume_async_unexpected_state(self):
        """Test async session resume with unexpected state."""
        # Mock the ResumeSessionAsync response
        mock_response = ResumeSessionAsyncResponse()
        mock_response.body = ResumeSessionAsyncResponseBody(
            success=True,
            code="Success",
            message="Session resume initiated successfully",
            request_id="test-request-id",
            http_status_code=200,
        )
        self.agent_bay.client.resume_session_async_async = AsyncMock(return_value=mock_response)

        # Mock get_session to return unexpected state, then RUNNING
        get_session_paused = GetSessionResult(
            request_id="test-request-id",
            success=True,
            data=GetSessionData(
                session_id="session-123",
                status="other",
            ),
        )

        get_session_running = GetSessionResult(
            request_id="test-request-id",
            success=True,
            data=GetSessionData(
                session_id="session-123",
                status="RUNNING",
            ),
        )
        self.agent_bay.get_session = MagicMock(side_effect=[get_session_paused, get_session_running])

        # Patch asyncio.sleep to avoid waiting
        with patch('asyncio.sleep', new_callable=AsyncMock) as mock_sleep:
            # Call the method
            result = asyncio.run(self.session.resume_async(timeout=10, poll_interval=1))

            # Verify the result
            self.assertIsInstance(result, SessionResumeResult)
            self.assertTrue(result.success)
            self.assertEqual(result.request_id, "test-request-id")
            self.assertEqual(result.status, "RUNNING")
            self.assertEqual(result.error_message, "")

            # Verify that sleep was called once (after the first attempt)
            mock_sleep.assert_called_once_with(1)


if __name__ == "__main__":
    unittest.main()