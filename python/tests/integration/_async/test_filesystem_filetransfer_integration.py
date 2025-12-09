"""
Integration tests for the FileTransfer functionality.
These tests verify the complete functionality of the FileTransfer class
with real sessions and actual file transfers.
"""

import os
import tempfile
import time

import pytest
import pytest_asyncio

from agentbay import AsyncAgentBay
from agentbay import BrowserContext, CreateSessionParams


@pytest_asyncio.fixture(scope="module")
async def agent_bay():
    """Create an AsyncAgentBay instance."""
    api_key = os.getenv("AGENTBAY_API_KEY")
    if not api_key:
        pytest.skip("AGENTBAY_API_KEY environment variable not set")
    return AsyncAgentBay(api_key=api_key)


@pytest_asyncio.fixture(scope="module")
async def file_transfer_session(agent_bay):
    """Create a session and context for file transfer testing."""
    # Get API key from environment
    api_key = os.getenv("AGENTBAY_API_KEY")
    if not api_key:
        pytest.skip("AGENTBAY_API_KEY environment variable not set")

    # Initialize AgentBay client
    # Create a unique context for testing
    context_name = f"file-transfer-test-{int(time.time())}"
    context_result = await agent_bay.context.get(context_name, True)
    if not context_result.success or not context_result.context:
        pytest.skip("Failed to create context")

    context = context_result.context
    print(f"Context created with ID: {context.id}")

    # Create browser session with context for testing
    browser_context = BrowserContext(context_id=context.id, auto_upload=True)

    params = CreateSessionParams(
        image_id="browser_latest",  # Use browser image for more comprehensive testing
        browser_context=browser_context,
    )

    session_result = await agent_bay.create(params)
    if not session_result.success or not session_result.session:
        pytest.skip("Failed to create session")

    session = session_result.session
    print(f"Browser session created with ID: {session.session_id}")

    yield session, context

    # Clean up resources
    print("Cleaning up: Deleting the session...")
    try:
        # Delete session with context synchronization
        result = await agent_bay.delete(session, sync_context=True)
        if result.success:
            print("Session successfully deleted with context sync")
        else:
            print(f"Warning: Error deleting session: {result.error_message}")
    except Exception as e:
        print(f"Warning: Error deleting session: {e}")

    # Clean up context
    try:
        await agent_bay.context.delete(context)
        print("Context successfully deleted")
    except Exception as e:
        print(f"Warning: Error deleting context: {e}")


@pytest.mark.asyncio
async def test_file_upload_integration():
    """Test complete file upload workflow with real session and verification."""
    api_key = os.getenv("AGENTBAY_API_KEY")
    if not api_key:
        pytest.skip("AGENTBAY_API_KEY environment variable not set")

    agent_bay = AsyncAgentBay(api_key=api_key)

    # Create a simple session - let AgentBay handle context creation automatically
    params = CreateSessionParams(
        image_id="linux_latest",  # Use linux image for stable file transfer testing
    )

    session_result = await agent_bay.create(params)
    if not session_result.success or not session_result.session:
        pytest.skip("Failed to create session")

    session = session_result.session
    print(f"Session created with ID: {session.session_id}")

    try:
        print("Testing file upload...")
        # Create a temporary file for upload
        with tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".txt"
        ) as temp_file:
            test_content = (
                "This is a test file for AgentBay FileTransfer upload integration test.\n"
                * 10
            )
            temp_file.write(test_content)
            temp_file.flush()  # Ensure content is written to disk
            temp_file_path = temp_file.name

        try:
            # Upload the file - use path that matches the auto-created file_transfer context
            remote_path = "/tmp/file-transfer/upload_test.txt"  # Use the same path as auto-created context sync

            upload_result = await session.file_system.upload_file(
                local_path=temp_file_path,
                remote_path=remote_path,
            )

            # Verify upload result
            assert upload_result.success, f"Upload failed: {upload_result.error}"
            assert upload_result.bytes_sent > 0
            assert upload_result.request_id_upload_url is not None
            assert upload_result.request_id_sync is not None

            ls_result = await session.command.execute_command(
                "ls -la /tmp/file-transfer/"
            )
            if not ls_result.success:
                print("    ❌ fileTransfer directory not found")
                assert False

            print(f"    ✅ fileTransfer directory exists: /tmp/file-transfer/")
            print(f"    Directory content:\n{ls_result.output}")

            # Verify file exists in remote location by listing directory
            list_result = await session.file_system.list_directory("/tmp/file-transfer/")
            assert (
                list_result.success
            ), f"Failed to list directory: {list_result.error_message}"

            # Check if our uploaded file is in the directory listing
            file_found = False
            for entry in list_result.entries:
                if entry.name == "upload_test.txt":
                    file_found = True
                    break

            assert file_found, "Uploaded file not found in remote directory"

            # Verify file content by reading it back
            read_result = await session.file_system.read_file(remote_path)
            assert (
                read_result.success
            ), f"Failed to read uploaded file: {read_result.error_message}"
            assert read_result.content == test_content

        finally:
            # Clean up local temporary file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
    finally:
        # Clean up session and context
        try:
            result = await session.delete()
            if result.success:
                print("Session successfully deleted")
            else:
                print(f"Warning: Error deleting session: {result.error_message}")
        except Exception as e:
            print(f"Warning: Error deleting session: {e}")


@pytest.mark.asyncio
async def test_file_download_integration():
    """Test complete file download workflow with real session and verification."""
    api_key = os.getenv("AGENTBAY_API_KEY")
    if not api_key:
        pytest.skip("AGENTBAY_API_KEY environment variable not set")

    agent_bay = AsyncAgentBay(api_key=api_key)

    # Create a simple session - let AgentBay handle context creation automatically
    params = CreateSessionParams(
        image_id="linux_latest",  # Use linux image for stable file transfer testing
    )

    session_result = await agent_bay.create(params)
    if not session_result.success or not session_result.session:
        pytest.skip("Failed to create session")

    session = session_result.session
    print(f"Session created with ID: {session.session_id}")

    try:
        # First, create a file in the remote location
        remote_path = "/tmp/file-transfer/download_test.txt"
        test_content = (
            "This is a test file for AgentBay FileTransfer download integration test.\n"
            * 15
        )
        print("\n Creating test directory...")

        create_dir_result = await session.file_system.create_directory(
            "/tmp/file-transfer/"
        )
        print(f"Create directory result: {create_dir_result.success}")
        assert create_dir_result.success
        write_result = await session.file_system.write_file(remote_path, test_content)
        assert (
            write_result.success
        ), f"Failed to create remote file: {write_result.error_message}"

        ls_result = await session.command.execute_command("ls -la /tmp/file-transfer/")
        if not ls_result.success:
            print("    ❌ fileTransfer directory not found")
            return False

        print(f"    ✅ fileTransfer directory exists: /tmp/file-transfer/")
        print(f"    Directory content:\n{ls_result.output}")
        # Create a temporary file path for download
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as temp_file:
            temp_file_path = temp_file.name

        try:
            # Download the file
            download_result = await session.file_system.download_file(
                remote_path=remote_path,
                local_path=temp_file_path,
            )

            # Verify download result
            assert download_result.success, f"Download failed: {download_result.error}"
            assert download_result.bytes_received > 0
            assert download_result.request_id_download_url is not None
            assert download_result.request_id_sync is not None
            assert download_result.local_path == temp_file_path

            # Verify downloaded file content
            with open(temp_file_path, "r") as f:
                downloaded_content = f.read()

            print(f"Downloaded file content length: {len(downloaded_content)} bytes")
            assert downloaded_content == test_content

        finally:
            # Clean up temporary files
            for path in [temp_file_path]:
                if os.path.exists(path):
                    print(f"Deleting temporary file: {path}")
                    os.unlink(path)
    finally:
        # Clean up session and context
        try:
            result = await session.delete()
            if result.success:
                print("Session successfully deleted")
            else:
                print(f"Warning: Error deleting session: {result.error_message}")
        except Exception as e:
            print(f"Warning: Error deleting session: {e}")
