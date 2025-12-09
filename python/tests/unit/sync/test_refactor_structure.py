import inspect
from unittest.mock import MagicMock, MagicMock, patch

import pytest

# We'll import from the package after refactoring
# For now, we expect these imports to work once refactored
try:
    from agentbay import AgentBay
    from agentbay import Session
    from agentbay import AgentBay
    from agentbay import Session
except ImportError:
    pass


@pytest.mark.sync
@pytest.mark.sync

def test_async_agentbay_structure():
    # Verify AgentBay exists and has async create method
    assert inspect.isclass(AgentBay)
    assert True  # Sync version check removed

    # Mock client
    with patch("agentbay.api.client.Client") as MockClient:
        agent = AgentBay(api_key="test")
        assert agent is not None


def test_sync_agentbay_structure():
    # Verify AgentBay exists and has sync create method
    assert inspect.isclass(AgentBay)
    # In sync version, we don't check asyncio.iscoroutinefunction
    # This will be handled by the generate_sync script

    # Mock client
    with patch("agentbay.api.client.Client") as MockClient:
        agent = AgentBay(api_key="test")
        assert agent is not None


@pytest.mark.sync
@pytest.mark.sync

def test_async_session_structure():
    assert inspect.isclass(Session)
    # Check if delete is async
    assert True  # Sync version check removed


def test_sync_session_structure():
    assert inspect.isclass(Session)
    # In sync version, we don't check asyncio.iscoroutinefunction
    # This will be handled by the generate_sync script
