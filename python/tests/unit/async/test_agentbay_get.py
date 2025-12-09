import os
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from agentbay import AsyncAgentBay
from agentbay import SessionResult
from agentbay import AsyncSession


class TestAgentBayGet:
    """Unit tests for AgentBay.get method."""

    @patch("agentbay._async.agentbay._load_config")
    @patch("agentbay._async.agentbay.mcp_client")
    async def test_get_empty_session_id(self, mock_mcp_client, mock_load_config):
        """Test get with empty session ID."""
        # Mock configuration
        mock_load_config.return_value = {
            "endpoint": "test.endpoint.com",
            "timeout_ms": 30000,
            "region_id": None,
        }

        # Mock client
        mock_client = MagicMock()
        mock_mcp_client.return_value = mock_client

        agentbay = AsyncAgentBay(api_key="test-api-key")

        result = await agentbay.get("")

        assert isinstance(result, SessionResult)
        assert not result.success
        assert "session_id is required" in result.error_message

    @patch("agentbay._async.agentbay._load_config")
    @patch("agentbay._async.agentbay.mcp_client")
    async def test_get_none_session_id(self, mock_mcp_client, mock_load_config):
        """Test get with None session ID."""
        # Mock configuration
        mock_load_config.return_value = {
            "endpoint": "test.endpoint.com",
            "timeout_ms": 30000,
            "region_id": None,
        }

        # Mock client
        mock_client = MagicMock()
        mock_mcp_client.return_value = mock_client

        agentbay = AsyncAgentBay(api_key="test-api-key")

        result = await agentbay.get(None)

        assert isinstance(result, SessionResult)
        assert not result.success
        assert "session_id is required" in result.error_message

    @patch("agentbay._async.agentbay._load_config")
    @patch("agentbay._async.agentbay.mcp_client")
    async def test_get_whitespace_session_id(self, mock_mcp_client, mock_load_config):
        """Test get with whitespace-only session ID."""
        # Mock configuration
        mock_load_config.return_value = {
            "endpoint": "test.endpoint.com",
            "timeout_ms": 30000,
            "region_id": None,
        }

        # Mock client
        mock_client = MagicMock()
        mock_mcp_client.return_value = mock_client

        agentbay = AsyncAgentBay(api_key="test-api-key")

        result = await agentbay.get("   ")

        assert isinstance(result, SessionResult)
        assert not result.success
        assert "session_id is required" in result.error_message

    @patch("agentbay._async.agentbay._load_config")
    @patch("agentbay._async.agentbay.mcp_client")
    async def test_get_method_exists(self, mock_mcp_client, mock_load_config):
        """Test that get method exists and has correct signature."""
        # Mock configuration
        mock_load_config.return_value = {
            "endpoint": "test.endpoint.com",
            "timeout_ms": 30000,
            "region_id": None,
        }

        # Mock client
        mock_client = MagicMock()
        mock_mcp_client.return_value = mock_client

        agentbay = AsyncAgentBay(api_key="test-api-key")

        # Verify method exists
        assert hasattr(agentbay, "get")
        assert callable(getattr(agentbay, "get"))

    @patch("agentbay._async.agentbay._load_config")
    @patch("agentbay._async.agentbay.mcp_client")
    async def test_get_returns_session_result_type(self, mock_mcp_client, mock_load_config):
        """Test that get method returns SessionResult."""
        # Mock configuration
        mock_load_config.return_value = {
            "endpoint": "test.endpoint.com",
            "timeout_ms": 30000,
            "region_id": None,
        }

        # Mock client
        mock_client = MagicMock()
        mock_mcp_client.return_value = mock_client

        agentbay = AsyncAgentBay(api_key="test-api-key")

        # Check the method exists and is callable
        get_method = getattr(agentbay, "get", None)
        assert get_method is not None
        assert callable(get_method)

        # Test with invalid input to verify it returns SessionResult
        result = await agentbay.get("")
        assert isinstance(result, SessionResult)

    @patch("agentbay._async.agentbay._load_config")
    @patch("agentbay._async.agentbay.mcp_client")
    async def test_get_error_message_format(self, mock_mcp_client, mock_load_config):
        """Test error message formatting for various invalid inputs."""
        # Mock configuration
        mock_load_config.return_value = {
            "endpoint": "test.endpoint.com",
            "timeout_ms": 30000,
            "region_id": None,
        }

        # Mock client
        mock_client = MagicMock()
        mock_mcp_client.return_value = mock_client

        agentbay = AsyncAgentBay(api_key="test-api-key")

        test_cases = [
            ("", "session_id is required"),
            (None, "session_id is required"),
            ("   ", "session_id is required"),
        ]

        for session_id, expected_error in test_cases:
            result = await agentbay.get(session_id)
            assert isinstance(result, SessionResult)
            assert not result.success
            assert expected_error in result.error_message


class TestAgentBayGetValidation:
    """Validation tests for AgentBay.get method."""

    @patch.dict(os.environ, {}, clear=True)
    @patch("agentbay._async.agentbay._load_config")
    async def test_get_requires_api_key(self, mock_load_config):
        """Test that AgentBay requires an API key."""
        # Mock configuration
        mock_load_config.return_value = {
            "endpoint": "test.endpoint.com",
            "timeout_ms": 30000,
            "region_id": None,
        }

        # Test initialization failure with empty API key
        with pytest.raises(ValueError):
            AsyncAgentBay(api_key="")

    @patch("agentbay._async.agentbay._load_config")
    @patch("agentbay._async.agentbay.mcp_client")
    async def test_get_interface_compliance(self, mock_mcp_client, mock_load_config):
        """Test that get method has the expected interface."""
        # Mock configuration
        mock_load_config.return_value = {
            "endpoint": "test.endpoint.com",
            "timeout_ms": 30000,
            "region_id": None,
        }

        # Mock client
        mock_client = MagicMock()
        mock_mcp_client.return_value = mock_client

        agentbay = AsyncAgentBay(api_key="test-key")

        # Method should exist
        assert hasattr(agentbay, "get")

        # Method should be callable
        get_method = getattr(agentbay, "get")
        assert callable(get_method)


@patch("agentbay._async.agentbay._load_config")
@patch("agentbay._async.agentbay.mcp_client")
def test_get_documentation(mock_mcp_client, mock_load_config):
    """Test that get method is properly documented."""
    # Mock configuration
    mock_load_config.return_value = {
        "endpoint": "test.endpoint.com",
        "timeout_ms": 30000,
        "region_id": None,
    }

    # Mock client
    mock_client = MagicMock()
    mock_mcp_client.return_value = mock_client

    agentbay = AsyncAgentBay(api_key="test-key")

    get_method = getattr(agentbay, "get", None)
    assert get_method is not None

    # Method should have docstring
    assert get_method.__doc__ is not None
    assert len(get_method.__doc__.strip()) > 0
