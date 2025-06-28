import unittest
from unittest.mock import MagicMock, patch

from agentbay.session import Session
from agentbay.model import DeleteResult, extract_request_id


class DummyAgentBay:
    def __init__(self):
        self.api_key = "test_api_key"
        self.client = MagicMock()


class TestSession(unittest.TestCase):
    def setUp(self):
        self.agent_bay = DummyAgentBay()
        self.session_id = "test_session_id"
        self.session = Session(self.agent_bay, self.session_id)

    def test_initialization(self):
        self.assertEqual(self.session.session_id, self.session_id)
        self.assertEqual(self.session.agent_bay, self.agent_bay)
        self.assertIsNotNone(self.session.file_system)
        self.assertIsNotNone(self.session.command)
        self.assertEqual(self.session.file_system.session, self.session)
        self.assertEqual(self.session.command.session, self.session)

    def test_get_api_key(self):
        self.assertEqual(self.session.get_api_key(), "test_api_key")

    def test_get_client(self):
        self.assertEqual(self.session.get_client(), self.agent_bay.client)

    def test_get_session_id(self):
        self.assertEqual(self.session.get_session_id(), "test_session_id")

    @patch("agentbay.session.extract_request_id")
    @patch("agentbay.session.ReleaseMcpSessionRequest")
    def test_delete_success(self, MockReleaseMcpSessionRequest, mock_extract_request_id):
        mock_request = MagicMock()
        mock_response = MagicMock()
        MockReleaseMcpSessionRequest.return_value = mock_request
        mock_extract_request_id.return_value = "request-123"
        self.agent_bay.client.release_mcp_session.return_value = mock_response

        result = self.session.delete()
        self.assertIsInstance(result, DeleteResult)
        self.assertEqual(result.request_id, "request-123")
        self.assertTrue(result.success)

        MockReleaseMcpSessionRequest.assert_called_once_with(
            authorization="Bearer test_api_key", session_id="test_session_id"
        )
        self.agent_bay.client.release_mcp_session.assert_called_once_with(mock_request)

    @patch("agentbay.session.extract_request_id")
    @patch("agentbay.session.ReleaseMcpSessionRequest")
    def test_delete_failure(self, MockReleaseMcpSessionRequest, mock_extract_request_id):
        mock_request = MagicMock()
        MockReleaseMcpSessionRequest.return_value = mock_request
        self.agent_bay.client.release_mcp_session.side_effect = Exception("Test error")

        result = self.session.delete()
        self.assertIsInstance(result, DeleteResult)
        self.assertFalse(result.success)
        self.assertEqual(
            result.error_message,
            f"Failed to delete session {self.session_id}: Test error",
        )

        MockReleaseMcpSessionRequest.assert_called_once_with(
            authorization="Bearer test_api_key", session_id="test_session_id"
        )
        self.agent_bay.client.release_mcp_session.assert_called_once_with(mock_request)


if __name__ == "__main__":
    unittest.main()
