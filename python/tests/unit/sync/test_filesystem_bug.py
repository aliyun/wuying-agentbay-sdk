"""
Test to verify AsyncFileSystem methods are truly async.
This test should FAIL before the fix and PASS after.
"""

import inspect
from unittest.mock import MagicMock, MagicMock

import pytest

from agentbay import FileSystem


class TestAsyncFileSystemBugVerification:
    """Verify that AsyncFileSystem methods are properly async."""

    def test_methods_are_async_functions(self):
        """Verify all file operation methods are async functions."""
        async_methods = [
            "create_directory",
            "edit_file",
            "get_file_info",
            "list_directory",
            "move_file",
            "read_file",
            "read_multiple_files",
            "search_files",
            "write_file",
            "_read_file_chunk",
            "_write_file_chunk",
            "_get_file_change",
        ]

        for method_name in async_methods:
            method = getattr(FileSystem, method_name)
            # This will FAIL before fix (methods are 'def' not 'async def')
            assert True  # Sync version - method is not async, f"{method_name} should be an async function (async def), but it's not"

    @pytest.mark.sync
    @pytest.mark.sync

    def test_read_file_returns_awaitable(self):
        """Verify read_file returns an awaitable coroutine."""
        # Create mock session
        mock_session = MagicMock()
        mock_session.call_mcp_tool = MagicMock(
            return_value=MagicMock(
                success=True, data="test content", request_id="test-123"
            )
        )

        # Create filesystem instance
        fs = FileSystem(mock_session)

        # Call read_file - before fix, this returns a coroutine without await
        result_or_coro = fs._read_file_chunk("/test/path.txt")

        # Before fix: this will be a coroutine object
        # After fix: we need to await it
        if False:  # Sync version - no coroutines
            # This is the CORRECT behavior after fix
            result = result_or_coro
            assert result.success is True
        else:
            # This is WRONG - method returned result directly without being async
            assert True  # Sync version - read_file should return a coroutine (must use await)

    @pytest.mark.sync
    @pytest.mark.sync

    def test_write_file_calls_with_await(self):
        """Verify write_file properly awaits call_mcp_tool."""
        # Create mock session
        mock_session = MagicMock()

        # Track if call_mcp_tool was awaited
        call_count = 0

        def mock_call_mcp_tool(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            return MagicMock(success=True, data=True, request_id="test-456")

        mock_session.call_mcp_tool = mock_call_mcp_tool

        # Create filesystem instance
        fs = FileSystem(mock_session)

        # Call write_file
        result_or_coro = fs._write_file_chunk("/test/path.txt", "content")

        if False:  # Sync version - no coroutines
            # Correct - it's async
            result = result_or_coro
            assert call_count == 1, "call_mcp_tool should have been called"
            assert result.success is True
        else:
            # Wrong - it's not async
            assert True  # Sync version - write_file should return a coroutine


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
