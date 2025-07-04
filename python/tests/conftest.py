import os
import shutil
import tempfile
from unittest.mock import Mock, patch

import pytest

from agentbay.agentbay import AgentBay
from agentbay.session import Session


@pytest.fixture(autouse=True)
def mock_api_calls(monkeypatch):
    """Mock API calls to avoid requiring real credentials during testing."""
    # Set a dummy API key if not provided
    if not os.getenv("AGENTBAY_API_KEY"):
        monkeypatch.setenv("AGENTBAY_API_KEY", "test_api_key_for_testing")

    # Mock the client to avoid real API calls in integration tests
    # This can be overridden in specific tests if real API testing is needed
    return None


@pytest.fixture(autouse=True)
def mock_agent_bay_integration(monkeypatch):
    """Automatically mock AgentBay for integration tests."""
    # Create a mock client instance
    mock_client = Mock()

    # Mock create_mcp_session response
    mock_session_response = Mock()
    mock_session_response.to_map.return_value = {
        "body": {"Data": {"SessionId": "mocked_session_123"}}
    }
    mock_client.create_mcp_session.return_value = mock_session_response

    # Mock call_mcp_tool response
    mock_tool_response = Mock()
    mock_tool_response.to_map.return_value = {
        "body": {
            "Data": {
                "Result": "success",
                "content": [{"text": "mocked command output"}],
            }
        }
    }
    mock_client.call_mcp_tool.return_value = mock_tool_response

    # Mock delete_mcp_session response
    mock_delete_response = Mock()
    mock_delete_response.to_map.return_value = {"body": {"Data": {"Success": True}}}
    mock_client.delete_mcp_session.return_value = mock_delete_response

    # Patch the Client class to return our mock
    # Since AgentBay imports Client as mcp_client, we need to patch it in
    # agentbay.agentbay module
    monkeypatch.setattr("agentbay.agentbay.mcp_client", lambda config: mock_client)

    yield mock_client


@pytest.fixture
def mock_client():
    """Provide a mock client for unit tests."""
    client = Mock()

    # Mock create_mcp_session response
    mock_response = Mock()
    mock_response.to_map.return_value = {
        "body": {"Data": {"SessionId": "test_session_123"}}
    }
    client.create_mcp_session.return_value = mock_response

    # Mock call_mcp_tool response
    mock_tool_response = Mock()
    mock_tool_response.to_map.return_value = {
        "body": {
            "Data": {
                "Result": "success",
                "content": [{"text": "mock response"}],
            }
        }
    }
    client.call_mcp_tool.return_value = mock_tool_response

    return client


@pytest.fixture
def mock_agent_bay(mock_client):
    """Provide a mock AgentBay instance for testing."""
    with patch("agentbay.api.client.Client") as mock_client_class:
        mock_client_class.return_value = mock_client
        agent_bay = AgentBay(api_key="test_key")
        return agent_bay


@pytest.fixture
def mock_session(mock_agent_bay, mock_client):
    """Provide a mock Session instance for testing."""
    # Create a mock session without making real API calls
    session = Session(mock_agent_bay, "test_session_123")
    session.client = mock_client
    return session


@pytest.fixture
def temp_dir():
    """Provide a temporary directory for file operations testing."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture
def sample_files(temp_dir):
    """Create sample files for testing."""
    files = {}

    # Create a text file
    text_file = os.path.join(temp_dir, "test.txt")
    with open(text_file, "w") as f:
        f.write("Hello, World!")
    files["text"] = text_file

    # Create a JSON file
    json_file = os.path.join(temp_dir, "test.json")
    with open(json_file, "w") as f:
        f.write('{"key": "value"}')
    files["json"] = json_file

    return files


@pytest.fixture(scope="session")
def test_config():
    """Provide test configuration that persists across all tests."""
    return {
        "api_endpoint": "https://test.api.agentbay.com",
        "timeout": 30,
        "retry_count": 3,
    }


# Pytest hooks for custom behavior
def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line("markers", "integration: mark test as integration test")
    config.addinivalue_line("markers", "slow: mark test as slow running")
    config.addinivalue_line("markers", "api: mark test as requiring API access")


def pytest_collection_modifyitems(config, items):
    """Modify collected test items to add markers automatically."""
    for item in items:
        # Mark test_agent_bay.py tests as integration tests
        if "test_agent_bay" in item.nodeid:
            item.add_marker(pytest.mark.integration)
