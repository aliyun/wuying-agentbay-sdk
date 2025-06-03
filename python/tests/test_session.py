import unittest
from unittest.mock import MagicMock, patch

from agentbay.session import Session


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
        self.assertIsNotNone(self.session.adb)
        self.assertEqual(self.session.file_system.session, self.session)
        self.assertEqual(self.session.command.session, self.session)
        self.assertEqual(self.session.adb.session, self.session)

    def test_get_api_key(self):
        self.assertEqual(self.session.get_api_key(), "test_api_key")

    def test_get_client(self):
        self.assertEqual(self.session.get_client(), self.agent_bay.client)

    def test_get_session_id(self):
        self.assertEqual(self.session.get_session_id(), "test_session_id")

    @patch("agentbay.session.ReleaseMcpSessionRequest")
    def test_delete_success(self, MockReleaseMcpSessionRequest):
        mock_request = MagicMock()
        MockReleaseMcpSessionRequest.return_value = mock_request
        self.agent_bay.client.release_mcp_session.return_value = "deleted"
        self.session.delete()
        MockReleaseMcpSessionRequest.assert_called_once_with(
            authorization="Bearer test_api_key", session_id="test_session_id"
        )
        self.agent_bay.client.release_mcp_session.assert_called_once_with(mock_request)

    @patch("agentbay.session.ReleaseMcpSessionRequest")
    def test_delete_failure(self, MockReleaseMcpSessionRequest):
        mock_request = MagicMock()
        MockReleaseMcpSessionRequest.return_value = mock_request
        self.agent_bay.client.release_mcp_session.side_effect = Exception("Test error")
        with self.assertRaises(Exception) as context:
            self.session.delete()
        self.assertEqual(
            str(context.exception),
            f"Failed to delete session {self.session_id}: Test error",
        )
        MockReleaseMcpSessionRequest.assert_called_once_with(
            authorization="Bearer test_api_key", session_id="test_session_id"
        )
        self.agent_bay.client.release_mcp_session.assert_called_once_with(mock_request)


if __name__ == "__main__":
    unittest.main()
