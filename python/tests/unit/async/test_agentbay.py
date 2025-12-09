import os
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from agentbay import (
    AsyncAgentBay,
    CreateSessionParams,
    ListSessionParams,
    AppManagerRule,
    ExtraConfigs,
    MobileExtraConfig,
)


class TestAsyncAgentBay(unittest.IsolatedAsyncioTestCase):
    """Test the functionality of the main AsyncAgentBay class"""

    @patch.dict(os.environ, {"AGENTBAY_API_KEY": "test-api-key"})
    @patch("agentbay._async.agentbay._load_config")
    @patch("agentbay._async.agentbay.mcp_client")
    async def test_initialization_with_env_var(self, mock_mcp_client, mock_load_config):
        """Test initializing AgentBay with an API key from environment variable"""
        # Mock configuration
        mock_load_config.return_value = {
            "endpoint": "test.endpoint.com",
            "timeout_ms": 30000,
            "region_id": None,
        }

        # Mock client
        mock_client = MagicMock()
        mock_mcp_client.return_value = mock_client

        # Create AsyncAgentBay instance
        agent_bay = AsyncAgentBay()

        # Verify results
        self.assertEqual(agent_bay.api_key, "test-api-key")
        self.assertEqual(agent_bay.client, mock_client)
        self.assertDictEqual(agent_bay._sessions, {})
        self.assertIsNotNone(agent_bay._lock)
        self.assertIsNotNone(agent_bay.context)

    @patch("agentbay._async.agentbay._load_config")
    @patch("agentbay._async.agentbay.mcp_client")
    async def test_initialization_with_provided_key(
        self, mock_mcp_client, mock_load_config
    ):
        """Test initializing AgentBay with a provided API key"""
        # Mock configuration
        mock_load_config.return_value = {
            "endpoint": "another.endpoint.com",
            "timeout_ms": 60000,
            "region_id": None,
        }

        # Mock client
        mock_client = MagicMock()
        mock_mcp_client.return_value = mock_client

        # Create AsyncAgentBay instance
        agent_bay = AsyncAgentBay(api_key="provided-api-key")

        # Verify results
        self.assertEqual(agent_bay.api_key, "provided-api-key")

    @patch.dict(os.environ, {}, clear=True)
    @patch("agentbay._async.agentbay._load_config")
    async def test_initialization_without_api_key(self, mock_load_config):
        """Test initialization failure when no API key is available"""
        # Mock configuration
        mock_load_config.return_value = {
            "endpoint": "test.endpoint.com",
            "timeout_ms": 30000,
            "region_id": None,
        }

        # Test initialization failure
        with self.assertRaises(ValueError) as context:
            AsyncAgentBay()

        self.assertIn("API key is required", str(context.exception))

    @patch("agentbay._async.agentbay.extract_request_id")
    @patch("agentbay._async.agentbay._load_config")
    @patch("agentbay._async.agentbay.mcp_client")
    async def test_create_session_success(
        self, mock_mcp_client, mock_load_config, mock_extract_request_id
    ):
        """Test successfully creating a session"""
        # Mock configuration and request ID
        mock_load_config.return_value = {
            "region_id": "cn-hangzhou",
            "endpoint": "test.endpoint.com",
            "timeout_ms": 30000,
            "region_id": None,
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
        mock_client.create_mcp_session_async = AsyncMock(return_value=mock_response)

        # Mock context info response
        mock_context_response = MagicMock()
        mock_context_response.to_map.return_value = {
            "body": {"Data": {"ContextStatusDataList": []}, "Success": True}
        }
        mock_client.get_context_info_async = AsyncMock(
            return_value=mock_context_response
        )
        mock_mcp_client.return_value = mock_client

        # Create AgentBay instance and session parameters
        agent_bay = AsyncAgentBay(api_key="test-key")

        # Mock context service
        mock_context = MagicMock()
        mock_context.get = AsyncMock(
            return_value=MagicMock(success=True, context_id="test-context")
        )
        agent_bay.context = mock_context

        params = CreateSessionParams(labels={"env": "test"})

        # Test creating a session
        result = await agent_bay.create(params)

        # Verify results
        self.assertEqual(result.request_id, "create-request-id")
        self.assertIsNotNone(result.session)
        self.assertEqual(result.session.session_id, "new-session-id")

        # Verify session was added to the internal dictionary
        self.assertIn("new-session-id", agent_bay._sessions)
        self.assertEqual(agent_bay._sessions["new-session-id"], result.session)

    @patch("agentbay._async.agentbay._load_config")
    @patch("agentbay._async.agentbay.mcp_client")
    async def test_create_session_invalid_response(
        self, mock_mcp_client, mock_load_config
    ):
        """Test handling invalid response when creating a session"""
        # Mock configuration
        mock_load_config.return_value = {
            "endpoint": "test.endpoint.com",
            "timeout_ms": 30000,
            "region_id": None,
        }

        # Mock client and invalid response
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.to_map.return_value = {
            "body": {"Data": None}  # Invalid Data field
        }
        mock_client.create_mcp_session_async = AsyncMock(return_value=mock_response)

        # Mock context info response
        mock_context_response = MagicMock()
        mock_context_response.to_map.return_value = {
            "body": {"Data": {"ContextStatusDataList": []}, "Success": True}
        }
        mock_client.get_context_info_async = AsyncMock(
            return_value=mock_context_response
        )
        mock_mcp_client.return_value = mock_client

        # Create AgentBay instance
        agent_bay = AsyncAgentBay(api_key="test-key")

        # Mock context service
        mock_context = MagicMock()
        mock_context.get = AsyncMock(
            return_value=MagicMock(success=True, context_id="test-context")
        )
        agent_bay.context = mock_context

        # Mock context service
        mock_context = MagicMock()
        mock_context.get = AsyncMock(
            return_value=MagicMock(success=True, context_id="test-context")
        )
        agent_bay.context = mock_context

        # Test session creation with invalid response
        result = await agent_bay.create()

        # Verify the result indicates failure
        self.assertFalse(result.success)
        self.assertIsNone(result.session)
        self.assertIn("Invalid response format", result.error_message)

    @patch("agentbay._async.agentbay.extract_request_id")
    @patch("agentbay._async.agentbay._load_config")
    @patch("agentbay._async.agentbay.mcp_client")
    async def test_list(
        self, mock_mcp_client, mock_load_config, mock_extract_request_id
    ):
        """Test listing sessions using the new list API"""
        # Mock configuration and request ID
        mock_load_config.return_value = {
            "region_id": "cn-hangzhou",
            "endpoint": "test.endpoint.com",
            "timeout_ms": 30000,
            "region_id": None,
        }
        mock_extract_request_id.return_value = "list-request-id"

        # Mock client and response
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.to_map.return_value = {
            "body": {
                "Success": True,
                "Data": [
                    {"SessionId": "session-1"},
                    {"SessionId": "session-2"},
                    {"SessionId": "session-3"},
                ],
                "TotalCount": 3,
                "MaxResults": 10,
            }
        }
        mock_client.list_session_async = AsyncMock(return_value=mock_response)
        mock_mcp_client.return_value = mock_client

        # Create AgentBay instance
        agent_bay = AsyncAgentBay(api_key="test-key")

        # Mock context service
        mock_context = MagicMock()
        mock_context.get = AsyncMock(
            return_value=MagicMock(success=True, context_id="test-context")
        )
        agent_bay.context = mock_context

        # Test listing all sessions (no labels)
        result = await agent_bay.list()
        self.assertEqual(result.request_id, "list-request-id")
        self.assertEqual(len(result.session_ids), 3)
        self.assertEqual(result.total_count, 3)
        self.assertTrue(result.success)

        # Test listing sessions with labels
        result = await agent_bay.list(labels={"env": "prod"})
        self.assertEqual(result.request_id, "list-request-id")
        self.assertEqual(len(result.session_ids), 3)

        # Test listing sessions with pagination
        result = await agent_bay.list(labels={"env": "prod"}, page=1, limit=2)
        self.assertEqual(result.request_id, "list-request-id")
        self.assertEqual(len(result.session_ids), 3)

    @patch("agentbay._async.agentbay.extract_request_id")
    @patch("agentbay._async.agentbay._load_config")
    @patch("agentbay._async.agentbay.mcp_client")
    async def test_list_pagination(
        self, mock_mcp_client, mock_load_config, mock_extract_request_id
    ):
        """Test list API pagination logic"""
        # Mock configuration and request ID
        mock_load_config.return_value = {
            "region_id": "cn-hangzhou",
            "endpoint": "test.endpoint.com",
            "timeout_ms": 30000,
            "region_id": None,
        }
        mock_extract_request_id.return_value = "list-request-id"

        # Mock client and responses for pagination
        mock_client = MagicMock()

        # First page response
        mock_response_page1 = MagicMock()
        mock_response_page1.to_map.return_value = {
            "body": {
                "Success": True,
                "Data": [{"SessionId": "session-1"}, {"SessionId": "session-2"}],
                "TotalCount": 4,
                "MaxResults": 2,
                "NextToken": "token-page2",
            }
        }

        # Second page response
        mock_response_page2 = MagicMock()
        mock_response_page2.to_map.return_value = {
            "body": {
                "Success": True,
                "Data": [{"SessionId": "session-3"}, {"SessionId": "session-4"}],
                "TotalCount": 4,
                "MaxResults": 2,
                "NextToken": "",
            }
        }

        # Set up mock to return different responses
        mock_client.list_session_async = AsyncMock(
            side_effect=[
                mock_response_page1,
                mock_response_page2,
            ]
        )
        mock_mcp_client.return_value = mock_client

        # Create AgentBay instance
        agent_bay = AsyncAgentBay(api_key="test-key")

        # Mock context service
        mock_context = MagicMock()
        mock_context.get = AsyncMock(
            return_value=MagicMock(success=True, context_id="test-context")
        )
        agent_bay.context = mock_context

        # Test getting page 2
        result = await agent_bay.list(labels={"env": "prod"}, page=2, limit=2)
        self.assertEqual(result.request_id, "list-request-id")
        self.assertEqual(len(result.session_ids), 2)
        self.assertEqual(result.session_ids[0], "session-3")
        self.assertEqual(result.session_ids[1], "session-4")

    @patch("agentbay._async.agentbay.extract_request_id")
    @patch("agentbay._async.agentbay._load_config")
    @patch("agentbay._async.agentbay.mcp_client")
    async def test_create_session_with_policy_id(
        self, mock_mcp_client, mock_load_config, mock_extract_request_id
    ):
        """Ensure policy_id is passed to create_mcp_session body"""
        mock_load_config.return_value = {
            "region_id": "cn-hangzhou",
            "endpoint": "test.endpoint.com",
            "timeout_ms": 30000,
            "region_id": None,
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
        mock_client.create_mcp_session_async = AsyncMock(return_value=mock_response)

        # Mock context info response
        mock_context_response = MagicMock()
        mock_context_response.to_map.return_value = {
            "body": {"Data": {"ContextStatusDataList": []}, "Success": True}
        }
        mock_client.get_context_info_async = AsyncMock(
            return_value=mock_context_response
        )
        mock_mcp_client.return_value = mock_client

        agent_bay = AsyncAgentBay(api_key="test-key")

        # Mock context service
        mock_context = MagicMock()
        mock_context.get = AsyncMock(
            return_value=MagicMock(success=True, context_id="test-context")
        )
        agent_bay.context = mock_context

        params = CreateSessionParams(policy_id="policy-xyz")

        result = await agent_bay.create(params)
        self.assertTrue(result.success)
        mock_client.create_mcp_session_async.assert_called_once()
        call_arg = mock_client.create_mcp_session_async.call_args[0][0]
        # Ensure policy_id is carried on the request object; client will include it in request body
        self.assertEqual(
            getattr(call_arg, "mcp_policy_id", None)
            or getattr(call_arg, "McpPolicyId", None),
            "policy-xyz",
        )
        # Basic success assertion remains; deep body behavior is validated in client integration tests

    @patch("agentbay._async.agentbay._load_config")
    @patch("agentbay._async.agentbay.mcp_client")
    async def test_create_with_mobile_extra_configs(
        self, mock_mcp_client, mock_load_config
    ):
        """Test creating a session with mobile extra configurations"""
        # Mock configuration
        mock_load_config.return_value = {
            "endpoint": "test.endpoint.com",
            "timeout_ms": 30000,
            "region_id": None,
        }

        # Mock client and response
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.to_map.return_value = {
            "body": {
                "Data": {
                    "SessionId": "mobile-session-id",
                    "ResourceUrl": "http://mobile.resource.url",
                },
                "RequestId": "mobile-create-request-id",
            }
        }
        mock_client.create_mcp_session_async = AsyncMock(return_value=mock_response)

        # Mock call_mcp_tool_async for mobile configuration
        mock_tool_response = MagicMock()
        mock_tool_response.to_map.return_value = {
            "body": {
                "Data": {"Success": True, "Output": "Command executed"},
                "RequestId": "tool-request-id",
            }
        }
        mock_client.call_mcp_tool_async = AsyncMock(return_value=mock_tool_response)

        # Mock context info response
        mock_context_response = MagicMock()
        mock_context_response.to_map.return_value = {
            "body": {"Data": {"ContextStatusDataList": []}, "Success": True}
        }
        mock_client.get_context_info_async = AsyncMock(
            return_value=mock_context_response
        )
        mock_mcp_client.return_value = mock_client

        # Create mobile configuration
        app_rule = AppManagerRule(
            rule_type="White",
            app_package_name_list=["com.allowed.app", "com.trusted.service"],
        )
        mobile_config = MobileExtraConfig(
            lock_resolution=True,
            app_manager_rule=app_rule,
            hide_navigation_bar=True,
            uninstall_blacklist=["com.android.systemui", "com.android.settings"],
        )
        extra_configs = ExtraConfigs(mobile=mobile_config)

        agent_bay = AsyncAgentBay(api_key="test-key")

        # Mock context service
        mock_context = MagicMock()
        mock_context.get = AsyncMock(
            return_value=MagicMock(success=True, context_id="test-context")
        )
        agent_bay.context = mock_context

        params = CreateSessionParams(
            labels={"project": "mobile-testing"}, extra_configs=extra_configs
        )

        result = await agent_bay.create(params)
        self.assertTrue(result.success)
        self.assertIsNotNone(result.session)
        if result.session:
            self.assertEqual(result.session.session_id, "mobile-session-id")

        # Verify the client was called with extra configs
        mock_client.create_mcp_session_async.assert_called_once()
        call_arg = mock_client.create_mcp_session_async.call_args[0][0]

        # Check that extra_configs is present in the request
        self.assertIsNotNone(call_arg.extra_configs)
        self.assertIsNotNone(call_arg.extra_configs.mobile)
        self.assertTrue(call_arg.extra_configs.mobile.lock_resolution)
        self.assertTrue(call_arg.extra_configs.mobile.hide_navigation_bar)
        self.assertEqual(len(call_arg.extra_configs.mobile.uninstall_blacklist), 2)
        self.assertEqual(
            call_arg.extra_configs.mobile.app_manager_rule.rule_type, "White"
        )
        self.assertEqual(
            len(call_arg.extra_configs.mobile.app_manager_rule.app_package_name_list), 2
        )

    @patch("agentbay._async.agentbay._load_config")
    @patch("agentbay._async.agentbay.mcp_client")
    async def test_create_with_mobile_blacklist_config(
        self, mock_mcp_client, mock_load_config
    ):
        """Test creating a session with mobile blacklist configuration"""
        # Mock configuration
        mock_load_config.return_value = {
            "endpoint": "test.endpoint.com",
            "timeout_ms": 30000,
            "region_id": None,
        }

        # Mock client and response
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.to_map.return_value = {
            "body": {
                "Data": {
                    "SessionId": "secure-session-id",
                    "ResourceUrl": "http://secure.resource.url",
                },
                "RequestId": "secure-create-request-id",
            }
        }
        mock_client.create_mcp_session_async = AsyncMock(return_value=mock_response)

        # Mock call_mcp_tool_async for mobile configuration
        mock_tool_response = MagicMock()
        mock_tool_response.to_map.return_value = {
            "body": {
                "Data": {"Success": True, "Output": "Command executed"},
                "RequestId": "tool-request-id",
            }
        }
        mock_client.call_mcp_tool_async = AsyncMock(return_value=mock_tool_response)

        # Mock context info response
        mock_context_response = MagicMock()
        mock_context_response.to_map.return_value = {
            "body": {"Data": {"ContextStatusDataList": []}, "Success": True}
        }
        mock_client.get_context_info_async = AsyncMock(
            return_value=mock_context_response
        )
        mock_mcp_client.return_value = mock_client

        # Create mobile blacklist configuration
        app_rule = AppManagerRule(
            rule_type="Black",
            app_package_name_list=["com.malware.app", "com.blocked.service"],
        )
        mobile_config = MobileExtraConfig(
            lock_resolution=False, app_manager_rule=app_rule
        )
        extra_configs = ExtraConfigs(mobile=mobile_config)

        agent_bay = AsyncAgentBay(api_key="test-key")

        # Mock context service
        mock_context = MagicMock()
        mock_context.get = AsyncMock(
            return_value=MagicMock(success=True, context_id="test-context")
        )
        agent_bay.context = mock_context

        params = CreateSessionParams(
            labels={"project": "security-testing"}, extra_configs=extra_configs
        )

        result = await agent_bay.create(params)
        self.assertTrue(result.success)
        self.assertIsNotNone(result.session)
        if result.session:
            self.assertEqual(result.session.session_id, "secure-session-id")

        # Verify the client was called with blacklist extra configs
        mock_client.create_mcp_session_async.assert_called_once()
        call_arg = mock_client.create_mcp_session_async.call_args[0][0]

        # Check that extra_configs with blacklist is present in the request
        self.assertIsNotNone(call_arg.extra_configs)
        self.assertIsNotNone(call_arg.extra_configs.mobile)
        self.assertFalse(call_arg.extra_configs.mobile.lock_resolution)
        self.assertEqual(
            call_arg.extra_configs.mobile.app_manager_rule.rule_type, "Black"
        )
        self.assertIn(
            "com.malware.app",
            call_arg.extra_configs.mobile.app_manager_rule.app_package_name_list,
        )

    @patch("agentbay._async.agentbay.extract_request_id")
    @patch("agentbay._async.agentbay._load_config")
    @patch("agentbay._async.agentbay.mcp_client")
    @patch("agentbay._async.agentbay._log_api_response_with_details")
    async def test_create_session_logs_full_resource_url(
        self,
        mock_log_api_response,
        mock_mcp_client,
        mock_load_config,
        mock_extract_request_id,
    ):
        """Test that resource_url is logged in full without truncation"""
        # Mock configuration and request ID
        mock_load_config.return_value = {
            "endpoint": "test.endpoint.com",
            "timeout_ms": 30000,
            "region_id": None,
        }
        mock_extract_request_id.return_value = "create-request-id"

        # Create a very long resource URL (more than 50 characters)
        long_url = "https://pre-myspace-wuying.aliyun.com/app/InnoArch/instance/s-04bdw8oc5n0ftg4kl/dashboard?token=verylongtokenstring123456789abcdefghijklmnopqrstuvwxyz"

        # Mock client and response
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.to_map.return_value = {
            "body": {
                "Data": {
                    "SessionId": "new-session-id",
                    "ResourceUrl": long_url,
                }
            }
        }
        mock_client.create_mcp_session_async = AsyncMock(return_value=mock_response)

        # Mock context info response
        mock_context_response = MagicMock()
        mock_context_response.to_map.return_value = {
            "body": {"Data": {"ContextStatusDataList": []}, "Success": True}
        }
        mock_client.get_context_info_async = AsyncMock(
            return_value=mock_context_response
        )
        mock_mcp_client.return_value = mock_client

        # Create AgentBay instance
        agent_bay = AsyncAgentBay(api_key="test-key")

        # Mock context service
        mock_context = MagicMock()
        mock_context.get = AsyncMock(
            return_value=MagicMock(success=True, context_id="test-context")
        )
        agent_bay.context = mock_context
        params = CreateSessionParams()

        # Test creating a session
        result = await agent_bay.create(params)

        # Verify results
        self.assertTrue(result.success)
        self.assertIsNotNone(result.session)
        self.assertEqual(result.session.resource_url, long_url)

        # Verify that the logging function was called with the full URL
        mock_log_api_response.assert_called_once()
        call_kwargs = mock_log_api_response.call_args[1]

        # Check that the resource_url in key_fields is the full URL, not truncated
        self.assertIn("key_fields", call_kwargs)
        key_fields = call_kwargs["key_fields"]
        self.assertIn("resource_url", key_fields)
        logged_url = key_fields["resource_url"]

        # Verify the URL is not truncated (should not end with "...")
        self.assertNotIn("...", logged_url)
        # Verify it's the full URL
        self.assertEqual(logged_url, long_url)
        # Verify the URL length is greater than 50 characters
        self.assertGreater(len(logged_url), 50)


if __name__ == "__main__":
    unittest.main()
