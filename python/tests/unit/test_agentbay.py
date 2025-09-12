import os
import unittest
from unittest.mock import MagicMock, patch

from agentbay import AgentBay
from agentbay.session_params import CreateSessionParams, ListSessionParams


class TestAgentBay(unittest.TestCase):
    """Test the functionality of the main AgentBay class"""

    @patch.dict(os.environ, {"AGENTBAY_API_KEY": "test-api-key"})
    @patch("agentbay.agentbay.load_config")
    @patch("agentbay.agentbay.mcp_client")
    def test_initialization_with_env_var(self, mock_mcp_client, mock_load_config):
        """Test initializing AgentBay with an API key from environment variable"""
        # Mock configuration
        mock_load_config.return_value = {
            "region_id": "cn-shanghai",
            "endpoint": "test.endpoint.com",
            "timeout_ms": 30000,
        }

        # Mock client
        mock_client = MagicMock()
        mock_mcp_client.return_value = mock_client

        # Create AgentBay instance
        agent_bay = AgentBay()

        # Verify results
        self.assertEqual(agent_bay.api_key, "test-api-key")
        self.assertEqual(agent_bay.region_id, "cn-shanghai")
        self.assertEqual(agent_bay.client, mock_client)
        self.assertDictEqual(agent_bay._sessions, {})
        self.assertIsNotNone(agent_bay._lock)
        self.assertIsNotNone(agent_bay.context)

    @patch("agentbay.agentbay.load_config")
    @patch("agentbay.agentbay.mcp_client")
    def test_initialization_with_provided_key(self, mock_mcp_client, mock_load_config):
        """Test initializing AgentBay with a provided API key"""
        # Mock configuration
        mock_load_config.return_value = {
            "region_id": "cn-beijing",
            "endpoint": "another.endpoint.com",
            "timeout_ms": 60000,
        }

        # Mock client
        mock_client = MagicMock()
        mock_mcp_client.return_value = mock_client

        # Create AgentBay instance
        agent_bay = AgentBay(api_key="provided-api-key")

        # Verify results
        self.assertEqual(agent_bay.api_key, "provided-api-key")
        self.assertEqual(agent_bay.region_id, "cn-beijing")

    @patch.dict(os.environ, {}, clear=True)
    @patch("agentbay.agentbay.load_config")
    def test_initialization_without_api_key(self, mock_load_config):
        """Test initialization failure when no API key is available"""
        # Mock configuration
        mock_load_config.return_value = {
            "region_id": "cn-shanghai",
            "endpoint": "test.endpoint.com",
            "timeout_ms": 30000,
        }

        # Test initialization failure
        with self.assertRaises(ValueError) as context:
            AgentBay()

        self.assertIn("API key is required", str(context.exception))

    @patch("agentbay.agentbay.extract_request_id")
    @patch("agentbay.agentbay.load_config")
    @patch("agentbay.agentbay.mcp_client")
    def test_create_session_success(
        self, mock_mcp_client, mock_load_config, mock_extract_request_id
    ):
        """Test successfully creating a session"""
        # Mock configuration and request ID
        mock_load_config.return_value = {
            "region_id": "cn-shanghai",
            "endpoint": "test.endpoint.com",
            "timeout_ms": 30000,
        }
        mock_extract_request_id.return_value = "create-request-id"

        # Mock client and response
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.to_map.return_value = {
            "body": {
                "Data": {
                    "SessionId": "new-session-id",
                    "ResourceUrl": "http://resource.url",
                }
            }
        }
        mock_client.create_mcp_session.return_value = mock_response
        mock_mcp_client.return_value = mock_client

        # Create AgentBay instance and session parameters
        agent_bay = AgentBay(api_key="test-key")
        params = CreateSessionParams(labels={"env": "test"})

        # Test creating a session
        result = agent_bay.create(params)

        # Verify results
        self.assertEqual(result.request_id, "create-request-id")
        self.assertIsNotNone(result.session)
        self.assertEqual(result.session.session_id, "new-session-id")


        # Verify session was added to the internal dictionary
        self.assertIn("new-session-id", agent_bay._sessions)
        self.assertEqual(agent_bay._sessions["new-session-id"], result.session)

    @patch("agentbay.agentbay.extract_request_id")
    @patch("agentbay.agentbay.load_config")
    @patch("agentbay.agentbay.mcp_client")
    def test_create_session_with_network_id(
        self, mock_mcp_client, mock_load_config, mock_extract_request_id
    ):
        """Test creating a session with network_id parameter"""
        # Mock configuration and request ID
        mock_load_config.return_value = {
            "region_id": "cn-shanghai",
            "endpoint": "test.endpoint.com",
            "timeout_ms": 30000,
        }
        mock_extract_request_id.return_value = "create-request-id"

        # Mock client and response
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.to_map.return_value = {
            "body": {
                "Data": {
                    "SessionId": "new-session-id",
                    "ResourceUrl": "http://resource.url",
                }
            }
        }
        mock_client.create_mcp_session.return_value = mock_response
        mock_mcp_client.return_value = mock_client

        # Create AgentBay instance and session parameters with network_id
        agent_bay = AgentBay(api_key="test-key")
        params = CreateSessionParams(
            labels={"env": "test"},
            network_id="net-123456"
        )

        # Test creating a session
        result = agent_bay.create(params)

        # Verify the request was made with network_id
        create_call_args = mock_client.create_mcp_session.call_args[0][0]
        self.assertEqual(create_call_args.network_id, "net-123456")

        # Verify results
        self.assertEqual(result.request_id, "create-request-id")
        self.assertIsNotNone(result.session)
        self.assertEqual(result.session.session_id, "new-session-id")

    @patch("agentbay.agentbay.load_config")
    @patch("agentbay.agentbay.mcp_client")
    def test_create_session_invalid_response(self, mock_mcp_client, mock_load_config):
        """Test handling invalid response when creating a session"""
        # Mock configuration
        mock_load_config.return_value = {
            "region_id": "cn-shanghai",
            "endpoint": "test.endpoint.com",
            "timeout_ms": 30000,
        }

        # Mock client and invalid response
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.to_map.return_value = {
            "body": {"Data": None}  # Invalid Data field
        }
        mock_client.create_mcp_session.return_value = mock_response
        mock_mcp_client.return_value = mock_client

        # Create AgentBay instance
        agent_bay = AgentBay(api_key="test-key")

        # Test session creation with invalid response
        result = agent_bay.create()

        # Verify the result indicates failure
        self.assertFalse(result.success)
        self.assertIsNone(result.session)
        self.assertIn("Invalid response format", result.error_message)

    @patch("agentbay.agentbay.extract_request_id")
    @patch("agentbay.agentbay.load_config")
    @patch("agentbay.agentbay.mcp_client")
    def test_list_by_labels(
        self, mock_mcp_client, mock_load_config, mock_extract_request_id
    ):
        """Test listing sessions by labels"""
        # Mock configuration and request ID
        mock_load_config.return_value = {
            "region_id": "cn-shanghai",
            "endpoint": "test.endpoint.com",
            "timeout_ms": 30000,
        }
        mock_extract_request_id.return_value = "list-request-id"

        # Mock client and response
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.to_map.return_value = {
            "body": {
                "Data": [
                    {"SessionId": "session-1"},
                    {"SessionId": "session-2"},
                ]
            }
        }
        mock_client.list_session.return_value = mock_response
        mock_mcp_client.return_value = mock_client

        # Create AgentBay instance
        agent_bay = AgentBay(api_key="test-key")

        # Create ListSessionParams object with labels
        params = ListSessionParams(labels={"env": "prod", "app": "test"})

        # Test listing sessions by labels
        result = agent_bay.list_by_labels(params)

        # Verify results
        self.assertEqual(result.request_id, "list-request-id")
        self.assertEqual(len(result.sessions), 2)
        self.assertEqual(result.sessions[0].session_id, "session-1")
        self.assertEqual(result.sessions[1].session_id, "session-2")

        # Verify cached sessions
        self.assertEqual(len(agent_bay._sessions), 2)
        self.assertIn("session-1", agent_bay._sessions)
        self.assertIn("session-2", agent_bay._sessions)

    @patch("agentbay.agentbay.extract_request_id")
    @patch("agentbay.agentbay.load_config")
    @patch("agentbay.agentbay.mcp_client")
    def test_list(self, mock_mcp_client, mock_load_config, mock_extract_request_id):
        """Test listing all sessions"""
        # Mock configuration
        mock_load_config.return_value = {
            "region_id": "cn-shanghai",
            "endpoint": "test.endpoint.com",
            "timeout_ms": 30000,
        }

        # Mock client
        mock_client = MagicMock()
        mock_mcp_client.return_value = mock_client

        # Create AgentBay instance and cached sessions
        agent_bay = AgentBay(api_key="test-key")
        session1 = MagicMock()
        session2 = MagicMock()
        agent_bay._sessions = {"session-1": session1, "session-2": session2}

        # Test listing all sessions
        sessions = agent_bay.list()

        # Verify results
        self.assertEqual(len(sessions), 2)
        self.assertIn(session1, sessions)
        self.assertIn(session2, sessions)

    @patch("agentbay.agentbay.extract_request_id")
    @patch("agentbay.agentbay.load_config")
    @patch("agentbay.agentbay.mcp_client")
    def test_create_session_with_mcp_policy_id(self, mock_mcp_client, mock_load_config, mock_extract_request_id):
        """Ensure mcp_policy_id is passed to create_mcp_session body"""
        mock_load_config.return_value = {
            "region_id": "cn-shanghai",
            "endpoint": "test.endpoint.com",
            "timeout_ms": 30000,
        }
        mock_extract_request_id.return_value = "create-request-id"

        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.to_map.return_value = {
            "body": {
                "Data": {
                    "SessionId": "new-session-id",
                    "ResourceUrl": "http://resource.url",
                },
                "RequestId": "create-request-id",
            }
        }
        mock_client.create_mcp_session.return_value = mock_response
        mock_mcp_client.return_value = mock_client

        agent_bay = AgentBay(api_key="test-key")
        params = CreateSessionParams(mcp_policy_id="policy-xyz")

        result = agent_bay.create(params)
        self.assertTrue(result.success)
        mock_client.create_mcp_session.assert_called_once()
        call_arg = mock_client.create_mcp_session.call_args[0][0]
        # Ensure mcp_policy_id is carried on the request object; client will include it in request body
        self.assertEqual(getattr(call_arg, "mcp_policy_id", None) or getattr(call_arg, "McpPolicyId", None), "policy-xyz")
        # Basic success assertion remains; deep body behavior is validated in client integration tests


if __name__ == "__main__":
    unittest.main()
