import unittest
from unittest.mock import MagicMock, patch
from agentbay.session import Session, DeleteResult

class DummyAgentBay:
    def __init__(self):
        self.client = MagicMock()
        self.api_key = "test_api_key"

    def get_api_key(self):
        return self.api_key

    def get_client(self):
        return self.client

class TestSession(unittest.TestCase):
    def setUp(self):
        self.agent_bay = DummyAgentBay()
        self.session_id = "test_session_id"
        self.session = Session(self.agent_bay, self.session_id)

    def test_validate_labels_success(self):
        # Test successful validation with valid labels
        labels = {"key1": "value1", "key2": "value2"}
        result = self.session._validate_labels(labels)
        self.assertIsNone(result)

    def test_validate_labels_none(self):
        # Test validation with None labels
        labels = None
        result = self.session._validate_labels(labels)
        self.assertIsNotNone(result)
        self.assertFalse(result.success)
        self.assertIn("Labels cannot be null", result.error_message)

    def test_validate_labels_list(self):
        # Test validation with list instead of dict
        labels = ["key1", "value1"]
        result = self.session._validate_labels(labels)
        self.assertIsNotNone(result)
        self.assertFalse(result.success)
        self.assertIn("Labels cannot be an array", result.error_message)

    def test_validate_labels_empty_dict(self):
        # Test validation with empty dict
        labels = {}
        result = self.session._validate_labels(labels)
        self.assertIsNotNone(result)
        self.assertFalse(result.success)
        self.assertIn("Labels cannot be empty", result.error_message)

    def test_validate_labels_empty_key(self):
        # Test validation with empty key
        labels = {"": "value1"}
        result = self.session._validate_labels(labels)
        self.assertIsNotNone(result)
        self.assertFalse(result.success)
        self.assertIn("Label keys cannot be empty", result.error_message)

    def test_validate_labels_empty_value(self):
        # Test validation with empty value
        labels = {"key1": ""}
        result = self.session._validate_labels(labels)
        self.assertIsNotNone(result)
        self.assertFalse(result.success)
        self.assertIn("Label values cannot be empty", result.error_message)

    def test_validate_labels_none_value(self):
        # Test validation with None value
        labels = {"key1": None}
        result = self.session._validate_labels(labels)
        self.assertIsNotNone(result)
        self.assertFalse(result.success)
        self.assertIn("Label values cannot be empty", result.error_message)

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
    def test_delete_success(
        self, MockReleaseMcpSessionRequest, mock_extract_request_id
    ):
        mock_request = MagicMock()
        mock_response = MagicMock()
        MockReleaseMcpSessionRequest.return_value = mock_request
        mock_extract_request_id.return_value = "request-123"
        self.agent_bay.client.release_mcp_session.return_value = mock_response

        # Mock the response.to_map() method
        mock_response.to_map.return_value = {
            "body": {"Data": {"IsError": False}, "Success": True}
        }

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
    def test_delete_without_params(
        self, MockReleaseMcpSessionRequest, mock_extract_request_id
    ):
        # Test default behavior when no parameters are provided
        mock_request = MagicMock()
        mock_response = MagicMock()
        MockReleaseMcpSessionRequest.return_value = mock_request
        mock_extract_request_id.return_value = "request-123"
        self.agent_bay.client.release_mcp_session.return_value = mock_response

        # Mock the response.to_map() method
        mock_response.to_map.return_value = {
            "body": {"Data": {"IsError": False}, "Success": True}
        }

        # Set up context mock object
        self.session.context = MagicMock()

        # Call delete method without parameters
        result = self.session.delete()
        self.assertIsInstance(result, DeleteResult)
        self.assertTrue(result.success)

        # Verify sync was not called
        self.session.context.sync.assert_not_called()

        # Verify API call is correct
        MockReleaseMcpSessionRequest.assert_called_once_with(
            authorization="Bearer test_api_key", session_id="test_session_id"
        )
        self.agent_bay.client.release_mcp_session.assert_called_once_with(mock_request)

    @patch("agentbay.session.extract_request_id")
    @patch("agentbay.session.ReleaseMcpSessionRequest")
    def test_delete_with_sync_context(
        self, MockReleaseMcpSessionRequest, mock_extract_request_id
    ):
        # Test behavior when sync_context=True
        mock_request = MagicMock()
        mock_response = MagicMock()
        MockReleaseMcpSessionRequest.return_value = mock_request
        mock_extract_request_id.return_value = "request-123"
        self.agent_bay.client.release_mcp_session.return_value = mock_response

        # Mock the response.to_map() method
        mock_response.to_map.return_value = {
            "body": {"Data": {"IsError": False}, "Success": True}
        }

        # Set up context mock object
        self.session.context = MagicMock()

        # Mock context.sync return value
        sync_result = MagicMock()
        sync_result.success = True
        self.session.context.sync.return_value = sync_result

        # Mock context.info return value
        info_result = MagicMock()
        info_result.context_status_data = [
            MagicMock(status="Success", task_type="upload", context_id="ctx1")
        ]
        self.session.context.info.return_value = info_result

        # Call delete method with sync_context=True
        result = self.session.delete(sync_context=True)
        self.assertIsInstance(result, DeleteResult)
        self.assertTrue(result.success)

        # Verify sync and info were called
        self.session.context.sync.assert_called_once()
        self.session.context.info.assert_called_once()

        # Verify API call is correct
        MockReleaseMcpSessionRequest.assert_called_once_with(
            authorization="Bearer test_api_key", session_id="test_session_id"
        )
        self.agent_bay.client.release_mcp_session.assert_called_once_with(mock_request)

    @patch("agentbay.session.extract_request_id")
    @patch("agentbay.session.ReleaseMcpSessionRequest")
    def test_delete_failure(
        self, MockReleaseMcpSessionRequest, mock_extract_request_id
    ):
        mock_request = MagicMock()
        MockReleaseMcpSessionRequest.return_value = mock_request
        mock_extract_request_id.return_value = "request-123"
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


class TestAgentBayDelete(unittest.TestCase):
    def setUp(self):
        self.agent_bay = DummyAgentBay()
        self.session = MagicMock()
        self.session.session_id = "test_session_id"
        # Add _lock mock
        self.agent_bay._lock = MagicMock()
        self.agent_bay._sessions = {"test_session_id": self.session}

    def test_delete_without_params(self):
        # Test AgentBay.delete without parameters
        # Mock session.delete return value
        delete_result = DeleteResult(request_id="request-123", success=True)
        self.session.delete.return_value = delete_result

        # Import AgentBay class
        from agentbay import AgentBay
        # Monkey patch AgentBay instance
        self.agent_bay.__class__ = AgentBay

        # Call delete method without parameters
        result = self.agent_bay.delete(self.session)

        # Verify session.delete was called with default sync_context=False
        self.session.delete.assert_called_once_with(sync_context=False)
        self.assertEqual(result, delete_result)

    def test_delete_with_sync_context(self):
        # Test AgentBay.delete with sync_context=True
        # Mock session.delete return value
        delete_result = DeleteResult(request_id="request-456", success=True)
        self.session.delete.return_value = delete_result

        # Import AgentBay class
        from agentbay import AgentBay
        # Monkey patch AgentBay instance
        self.agent_bay.__class__ = AgentBay

        # Call delete method with sync_context=True
        result = self.agent_bay.delete(self.session, sync_context=True)

        # Verify session.delete was called with sync_context=True
        self.session.delete.assert_called_once_with(sync_context=True)
        self.assertEqual(result, delete_result)


if __name__ == "__main__":
    unittest.main()
