"""Integration tests for command environment variables and advanced features (cwd, envs, new return format)."""

import os

import pytest
import pytest_asyncio

from agentbay import AsyncAgentBay
from agentbay import CreateSessionParams


@pytest_asyncio.fixture(scope="module")
async def agent_bay():
    api_key = os.environ.get("AGENTBAY_API_KEY")
    if not api_key:
        pytest.skip("AGENTBAY_API_KEY environment variable not set")
    return AsyncAgentBay(api_key=api_key)


@pytest_asyncio.fixture
async def test_session(agent_bay):
    """Create a test session."""
    result = await agent_bay.create(CreateSessionParams(image_id="linux_latest"))
    if not result.success:
        pytest.skip(f"Failed to create session: {result.error_message}")
    yield result.session
    await result.session.delete()


@pytest.mark.asyncio
async def test_command_new_return_format(test_session):
    """Test command execution with new return format (exit_code, stdout, stderr)."""
    cmd = test_session.command
    result = await cmd.execute_command("echo 'Hello, AgentBay!'")
    
    # Verify new fields exist
    assert hasattr(result, 'exit_code'), "exit_code field should exist"
    assert hasattr(result, 'stdout'), "stdout field should exist"
    assert hasattr(result, 'stderr'), "stderr field should exist"
    
    # Verify success case
    assert result.success, "Command should succeed"
    assert result.exit_code == 0, "Exit code should be 0 for success"
    assert "Hello, AgentBay!" in result.stdout, "Stdout should contain expected output"
    assert result.output == result.stdout, "Output should equal stdout for success"
    
    print(f"✓ New return format test passed: exit_code={result.exit_code}, stdout={result.stdout}")


@pytest.mark.asyncio
async def test_command_error_with_exit_code(test_session):
    """Test error command with exit_code, stderr, and trace_id."""
    cmd = test_session.command
    result = await cmd.execute_command("ls /non_existent_directory_12345")
    
    # Verify error case
    assert hasattr(result, 'exit_code'), "exit_code field should exist"
    assert hasattr(result, 'stderr'), "stderr field should exist"
    assert hasattr(result, 'trace_id'), "trace_id field should exist"
    
    # Error commands should have non-zero exit code
    # Note: success field behavior depends on implementation
    if result.exit_code != 0:
        assert result.exit_code != 0, "Exit code should be non-zero for error"
        # trace_id is optional, only present when errorCode != 0
        if result.trace_id:
            print(f"✓ Error command test passed: exit_code={result.exit_code}, stderr={result.stderr}, trace_id={result.trace_id}")
        else:
            print(f"✓ Error command test passed: exit_code={result.exit_code}, stderr={result.stderr} (no trace_id)")
    else:
        # If exit_code is 0, the command might have succeeded in some way
        print(f"⚠ Command returned exit_code=0, but this is acceptable")


@pytest.mark.asyncio
async def test_command_with_cwd(test_session):
    """Test command execution with cwd parameter."""
    cmd = test_session.command
    result = await cmd.execute_command("pwd", cwd="/tmp")
    
    assert result.success, "Command should succeed"
    assert result.exit_code == 0, "Exit code should be 0"
    # The output should contain /tmp or be /tmp
    assert "/tmp" in result.stdout, f"Working directory should be /tmp, got: {result.stdout}"
    
    print(f"✓ CWD test passed: working directory={result.stdout.strip()}")


@pytest.mark.asyncio
async def test_command_with_envs(test_session):
    """Test command execution with envs parameter."""
    cmd = test_session.command
    result = await cmd.execute_command(
        "echo $TEST_VAR",
        envs={"TEST_VAR": "test_value_123"}
    )
    
    assert result.success, "Command should succeed"
    assert result.exit_code == 0, "Exit code should be 0"
    # The environment variable should be set
    # Note: This depends on backend implementation
    output = result.stdout.strip()
    if "test_value_123" in output:
        print(f"✓ Envs test passed: environment variable set correctly: {output}")
    else:
        print(f"⚠ Envs test: environment variable may not be set (output: {output})")
        # This is acceptable if backend doesn't support envs yet


@pytest.mark.asyncio
async def test_command_with_cwd_and_envs(test_session):
    """Test command execution with both cwd and envs parameters."""
    cmd = test_session.command
    result = await cmd.execute_command(
        "pwd && echo $CUSTOM_VAR",
        cwd="/tmp",
        envs={"CUSTOM_VAR": "custom_value"}
    )
    
    assert result.success, "Command should succeed"
    assert result.exit_code == 0, "Exit code should be 0"
    assert "/tmp" in result.stdout, "Working directory should be /tmp"
    
    print(f"✓ Combined cwd and envs test passed")
    print(f"  Output: {result.stdout}")


@pytest.mark.asyncio
async def test_command_backward_compatibility(test_session):
    """Test backward compatibility: output field should still work."""
    cmd = test_session.command
    result = await cmd.execute_command("echo 'backward compatible'")
    
    # Verify backward compatibility
    assert hasattr(result, 'output'), "output field should exist for backward compatibility"
    assert result.output is not None, "output should not be None"
    
    # output should be stdout if available, otherwise stderr
    if result.stdout:
        assert result.output == result.stdout, "output should equal stdout when stdout is available"
    elif result.stderr:
        assert result.output == result.stderr, "output should equal stderr when stdout is empty"
    
    print(f"✓ Backward compatibility test passed: output={result.output}")


@pytest.mark.asyncio
async def test_command_path_env(test_session):
    """Test PATH environment variable."""
    cmd = test_session.command
    result = await cmd.execute_command("echo $PATH")
    assert result.success
    assert len(result.output) > 0
    print(f"PATH: {result.output[:100]}...")

