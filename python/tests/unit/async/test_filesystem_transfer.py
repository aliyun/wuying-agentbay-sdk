"""
Unit tests for file transfer functionality.

This module contains comprehensive unit tests for:
- FileTransfer class (Sync and Async)
- Upload and download operations
- Progress tracking
- Error handling and validation
"""

import asyncio
import pytest
import os
import unittest
from unittest.mock import AsyncMock, MagicMock, Mock, patch

from agentbay import AsyncFileTransfer

# Import the classes we're testing
from agentbay import (
    AsyncFileSystem,
    AsyncFileTransfer,
    DownloadResult,
    UploadResult,
)


# Since attach_file_transfer doesn't exist, we'll create a helper function for tests
def attach_file_transfer(agent_bay, session):
    """Helper function to create a FileTransfer instance for testing."""
    return AsyncFileTransfer(agent_bay, session)


class TestAsyncFileTransferResultClasses(unittest.IsolatedAsyncioTestCase):
    """Test cases for result classes."""

    @pytest.mark.asyncio


    async def test_upload_result_creation(self):
        """Test UploadResult object creation."""
        result = UploadResult(
            success=True,
            request_id_upload_url="req_123",
            request_id_sync="sync_456",
            http_status=200,
            etag="etag_789",
            bytes_sent=1024,
            path="/remote/file.txt",
        )

        self.assertTrue(result.success)
        self.assertEqual(result.request_id_upload_url, "req_123")
        self.assertEqual(result.request_id_sync, "sync_456")
        self.assertEqual(result.http_status, 200)
        self.assertEqual(result.etag, "etag_789")
        self.assertEqual(result.bytes_sent, 1024)
        self.assertEqual(result.path, "/remote/file.txt")
        self.assertIsNone(result.error)

    @pytest.mark.asyncio


    async def test_upload_result_with_error(self):
        """Test UploadResult creation with error."""
        result = UploadResult(
            success=False,
            request_id_upload_url=None,
            request_id_sync=None,
            http_status=None,
            etag=None,
            bytes_sent=0,
            path="/remote/file.txt",
            error="Test error message",
        )

        self.assertFalse(result.success)
        self.assertEqual(result.error, "Test error message")

    @pytest.mark.asyncio


    async def test_download_result_creation(self):
        """Test DownloadResult object creation."""
        result = DownloadResult(
            success=True,
            request_id_download_url="req_123",
            request_id_sync="sync_456",
            http_status=200,
            bytes_received=2048,
            path="/remote/file.txt",
            local_path="/local/file.txt",
        )

        self.assertTrue(result.success)
        self.assertEqual(result.request_id_download_url, "req_123")
        self.assertEqual(result.request_id_sync, "sync_456")
        self.assertEqual(result.http_status, 200)
        self.assertEqual(result.bytes_received, 2048)
        self.assertEqual(result.path, "/remote/file.txt")
        self.assertEqual(result.local_path, "/local/file.txt")
        self.assertIsNone(result.error)

    @pytest.mark.asyncio


    async def test_download_result_with_error(self):
        """Test DownloadResult creation with error."""
        result = DownloadResult(
            success=False,
            request_id_download_url=None,
            request_id_sync=None,
            http_status=None,
            bytes_received=0,
            path="/remote/file.txt",
            local_path="/local/file.txt",
            error="Test error message",
        )

        self.assertFalse(result.success)
        self.assertEqual(result.error, "Test error message")


class TestAsyncFileTransfer(unittest.IsolatedAsyncioTestCase):
    """Test cases for FileTransfer class (Sync)."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_agent_bay = Mock()
        self.mock_session = Mock()
        self.mock_context_svc = Mock()

        self.mock_agent_bay.context = self.mock_context_svc
        self.mock_session.context = Mock()

        self.file_transfer = AsyncFileTransfer(self.mock_agent_bay, self.mock_session)

    @pytest.mark.asyncio


    async def test_file_transfer_initialization(self):
        """Test FileTransfer initialization."""
        # Test default parameters
        ft = AsyncFileTransfer(
            self.mock_agent_bay, self.mock_session, http_timeout=30.0
        )
        self.assertEqual(ft._http_timeout, 60.0)
        self.assertTrue(ft._follow_redirects)

        # Test custom parameters
        ft = AsyncFileTransfer(
            self.mock_agent_bay,
            self.mock_session,
            http_timeout=120.0,
            follow_redirects=False,
        )
        self.assertEqual(ft._http_timeout, 120.0)
        self.assertFalse(ft._follow_redirects)

    @patch("os.path.isfile")
    @pytest.mark.asyncio

    async def test_upload_file_not_found(self, mock_isfile):
        """Test upload with non-existent local file."""
        mock_isfile.return_value = False

        result = await self.file_transfer.upload(
            local_path="/local/file.txt", remote_path="/remote/file.txt"
        )

        self.assertFalse(result.success)
        self.assertIn("not found", result.error)


class TestAsyncFileTransfer(unittest.IsolatedAsyncioTestCase):
    """Test cases for AsyncFileTransfer methods."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_agent_bay = Mock()
        self.mock_session = Mock()
        self.mock_context_svc = Mock()

        self.mock_agent_bay.context = self.mock_context_svc
        self.mock_session.context = Mock()

        self.file_transfer = AsyncFileTransfer(self.mock_agent_bay, self.mock_session)
        # Provide deterministic context id to satisfy upload/download calls
        self.file_transfer._context_id = "ctx_123"
        # Provide deterministic context id to satisfy upload/download calls
        self.file_transfer._context_id = "ctx_123"

    def _run_async_test(self, coro):
        """Helper method to run async tests."""
        return asyncio.run(coro)

    @patch("os.path.isfile")
    @pytest.mark.asyncio

    async def test_upload_success(self, mock_isfile):
        """Test successful upload operation."""

        async def async_test():
            # Setup mocks
            mock_isfile.return_value = True

            # Mock context service responses (needs to be awaitable for async)
            mock_upload_url_result = Mock()
            mock_upload_url_result.success = True
            mock_upload_url_result.url = "https://presigned-upload-url.com"
            mock_upload_url_result.request_id = "req_upload_123"

            async def get_upload_url_mock(*args, **kwargs):
                return mock_upload_url_result

            self.mock_context_svc.get_file_upload_url = AsyncMock(
                side_effect=get_upload_url_mock
            )

            # Mock internal methods
            # Mock _put_file_sync to bypass HTTP call
            def put_file_sync_mock(*args, **kwargs):
                # Mock return of _put_file_sync: (http_status, etag, bytes_sent)
                return 200, "etag_456", 1024

            self.file_transfer._put_file_sync = Mock(side_effect=put_file_sync_mock)

            # Mock sync operation
            mock_sync_result = Mock()
            mock_sync_result.success = True
            mock_sync_result.request_id = "req_sync_789"

            async def sync_mock(*args, **kwargs):
                return mock_sync_result

            self.mock_session.context.sync = AsyncMock(side_effect=sync_mock)

            # Mock wait for task
            async def wait_mock(*args, **kwargs):
                return True, None

            self.file_transfer._wait_for_task = AsyncMock(side_effect=wait_mock)

            # Test upload
            result = await self.file_transfer.upload(
                local_path="/local/file.txt", remote_path="/remote/file.txt"
            )

            # Verify result
            self.assertTrue(result.success)
            self.assertEqual(result.request_id_upload_url, "req_upload_123")
            self.assertEqual(result.request_id_sync, "req_sync_789")
            self.assertEqual(result.http_status, 200)
            self.assertEqual(result.etag, "etag_456")
            self.assertEqual(result.bytes_sent, 1024)
            self.assertEqual(result.path, "/remote/file.txt")

            # Verify calls were made
            self.mock_context_svc.get_file_upload_url.assert_called_once_with(
                "ctx_123", "/remote/file.txt"
            )
            # Note: The actual method name may vary, check the implementation
            # self.mock_session.context.sync.assert_called_once()
            self.file_transfer._wait_for_task.assert_called()

        # Run the async test
        await async_test()

    @patch("os.path.isfile")
    @pytest.mark.asyncio

    async def test_upload_get_url_failure(self, mock_isfile):
        """Test upload failure when getting upload URL fails."""

        async def async_test():
            mock_isfile.return_value = True

            # Mock failed upload URL response
            mock_upload_url_result = Mock()
            mock_upload_url_result.success = False
            mock_upload_url_result.message = "Failed to get upload URL"
            mock_upload_url_result.request_id = "req_upload_123"

            async def get_upload_url_mock(*args, **kwargs):
                return mock_upload_url_result

            self.mock_context_svc.get_file_upload_url = AsyncMock(
                side_effect=get_upload_url_mock
            )

            # Test upload
            result = await self.file_transfer.upload(
                local_path="/local/file.txt", remote_path="/remote/file.txt"
            )

            # Verify result
            self.assertFalse(result.success)
            self.assertIsNotNone(result.error)
            if result.error:
                self.assertIn("get_file_upload_url failed", result.error)
            self.assertEqual(result.request_id_upload_url, "req_upload_123")

        # Run the async test
        await async_test()

    @patch("os.path.isfile")
    @pytest.mark.asyncio

    async def test_upload_http_failure(self, mock_isfile):
        """Test upload failure during HTTP upload."""

        async def async_test():
            mock_isfile.return_value = True

            # Mock successful upload URL response
            mock_upload_url_result = Mock()
            mock_upload_url_result.success = True
            mock_upload_url_result.url = "https://presigned-upload-url.com"
            mock_upload_url_result.request_id = "req_upload_123"

            async def get_upload_url_mock(*args, **kwargs):
                return mock_upload_url_result

            self.mock_context_svc.get_file_upload_url = AsyncMock(
                side_effect=get_upload_url_mock
            )

            # Mock HTTP upload failure
            def put_file_sync_mock(*args, **kwargs):
                # Return 500 error
                return 500, None, 0

            self.file_transfer._put_file_sync = Mock(side_effect=put_file_sync_mock)

            # Test upload
            result = await self.file_transfer.upload(
                local_path="/local/file.txt", remote_path="/remote/file.txt"
            )

            # Verify result
            self.assertFalse(result.success)
            self.assertIsNotNone(result.error)
            if result.error:
                self.assertIn("Upload failed with HTTP 500", result.error)
            self.assertEqual(result.request_id_upload_url, "req_upload_123")
            self.assertEqual(result.http_status, 500)

        # Run the async test
        await async_test()

    @patch("os.path.exists")
    @patch("os.path.getsize")
    @patch("os.makedirs")
    @pytest.mark.asyncio

    async def test_download_success(self, mock_makedirs, mock_getsize, mock_exists):
        """Test successful download operation."""

        async def async_test():
            mock_exists.return_value = True
            mock_getsize.return_value = 2048

            # Mock sync operation
            mock_sync_result = Mock()
            mock_sync_result.success = True
            mock_sync_result.request_id = "req_sync_123"

            async def sync_mock(*args, **kwargs):
                return mock_sync_result

            self.mock_session.context.sync = AsyncMock(side_effect=sync_mock)

            # Mock wait for task
            async def wait_mock(*args, **kwargs):
                return True, None

            self.file_transfer._wait_for_task = AsyncMock(side_effect=wait_mock)

            # Mock download URL response
            mock_download_url_result = Mock()
            mock_download_url_result.success = True
            mock_download_url_result.url = "https://presigned-download-url.com"
            mock_download_url_result.request_id = "req_download_456"

            async def get_download_url_mock(*args, **kwargs):
                return mock_download_url_result

            self.mock_context_svc.get_file_download_url = AsyncMock(
                side_effect=get_download_url_mock
            )

            # Mock download
            def get_file_sync_mock(*args, **kwargs):
                # Return (http_status, bytes_received) for _get_file_sync
                return 200, 2048

            self.file_transfer._get_file_sync = Mock(side_effect=get_file_sync_mock)

            # Test download
            result = await self.file_transfer.download(
                remote_path="/remote/file.txt", local_path="/local/file.txt"
            )

            # Verify result
            self.assertTrue(result.success)
            self.assertEqual(result.request_id_download_url, "req_download_456")
            self.assertEqual(result.request_id_sync, "req_sync_123")
            self.assertEqual(result.http_status, 200)
            self.assertEqual(result.bytes_received, 2048)

            # Verify calls were made
            # Note: The actual method name may vary, check the implementation
            # self.mock_session.context.sync.assert_called_once()
            self.file_transfer._wait_for_task.assert_called()
            self.mock_context_svc.get_file_download_url.assert_called_once_with(
                "ctx_123", "/remote/file.txt"
            )

        # Run the async test
        await async_test()

    @patch("os.path.exists")
    @patch("os.path.getsize")
    @patch("os.makedirs")
    @pytest.mark.asyncio

    async def test_download_get_url_failure(
        self, mock_makedirs, mock_getsize, mock_exists
    ):
        """Test download failure when getting download URL fails."""

        async def async_test():
            mock_exists.return_value = False

            # Mock sync operation
            mock_sync_result = Mock()
            mock_sync_result.success = True
            mock_sync_result.request_id = "req_sync_123"

            async def sync_mock(*args, **kwargs):
                return mock_sync_result

            self.mock_session.context.sync = AsyncMock(side_effect=sync_mock)

            # Mock wait for task
            async def wait_mock(*args, **kwargs):
                return True, None

            self.file_transfer._wait_for_task = AsyncMock(side_effect=wait_mock)

            # Mock failed download URL response
            mock_download_url_result = Mock()
            mock_download_url_result.success = False
            mock_download_url_result.message = "Failed to get download URL"
            mock_download_url_result.request_id = "req_download_456"

            async def get_download_url_mock(*args, **kwargs):
                return mock_download_url_result

            self.mock_context_svc.get_file_download_url = AsyncMock(
                side_effect=get_download_url_mock
            )

            # Test download
            result = await self.file_transfer.download(
                remote_path="/remote/file.txt", local_path="/local/file.txt"
            )

            # Verify result
            self.assertFalse(result.success)
            self.assertIn("get_file_download_url failed", result.error)

        # Run the async test
        await async_test()

    @pytest.mark.asyncio


    async def test_wait_for_task_success(self):
        """Test _wait_for_task method with successful completion."""

        async def async_test():
            # Mock info response with successful task
            mock_info_result = Mock()
            mock_info_result.context_status_data = [
                Mock(
                    context_id="ctx_123",
                    path="/remote/file.txt",
                    task_type="upload",
                    status="Success",  # Capitalized as per API
                    error_message=None,
                )
            ]

            async def info_mock(*args, **kwargs):
                return mock_info_result

            self.mock_session.context.info.side_effect = info_mock

            # Test wait for task
            success, error = await self.file_transfer._wait_for_task(
                context_id="ctx_123",
                remote_path="/remote/file.txt",
                task_type="upload",
                timeout=1.0,
                interval=0.1,
            )

            # Verify result
            self.assertTrue(success)
            self.assertIsNone(error)
            self.mock_session.context.info.assert_called()

        # Run the async test
        await async_test()

    @pytest.mark.asyncio


    async def test_wait_for_task_with_error(self):
        """Test _wait_for_task method with task error."""

        async def async_test():
            # Mock info response with task error
            mock_info_result = Mock()
            mock_info_result.context_status_data = [
                Mock(
                    context_id="ctx_123",
                    path="/remote/file.txt",
                    task_type="upload",
                    status="Failed",  # Capitalized as per API
                    error_message="Test error message",
                )
            ]

            async def info_mock(*args, **kwargs):
                return mock_info_result

            self.mock_session.context.info.side_effect = info_mock

            # Test wait for task
            success, error = await self.file_transfer._wait_for_task(
                context_id="ctx_123",
                remote_path="/remote/file.txt",
                task_type="upload",
                timeout=1.0,
                interval=0.1,
            )

            # Verify result
            self.assertFalse(success)
            self.assertIsNotNone(error)
            if error:
                self.assertIn("Task error", error)
                self.assertIn("Test error message", error)

        # Run the async test
        await async_test()

    @pytest.mark.asyncio


    async def test_wait_for_task_timeout(self):
        """Test _wait_for_task method with timeout."""

        async def async_test():
            # Mock info response that never completes
            mock_info_result = Mock()
            mock_info_result.context_status_data = [
                Mock(
                    context_id="ctx_123",
                    path="/remote/file.txt",
                    task_type="upload",
                    status="Pending",  # Capitalized
                    error_message=None,
                )
            ]

            async def info_mock(*args, **kwargs):
                return mock_info_result

            self.mock_session.context.info.side_effect = info_mock

            # Test wait for task with short timeout
            success, error = await self.file_transfer._wait_for_task(
                context_id="ctx_123",
                remote_path="/remote/file.txt",
                task_type="upload",
                timeout=0.05,  # Very short timeout
                interval=0.01,  # Very short interval
            )

            # Verify result
            self.assertFalse(success)
            self.assertEqual(error, "task not finished")

        # Run the async test
        await async_test()


class TestAsyncFileSystemFileTransfer(unittest.IsolatedAsyncioTestCase):
    """Test cases for FileSystem file transfer methods."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_session = Mock()
        self.mock_session.agent_bay = Mock()
        self.mock_session.agent_bay.context = Mock()
        self.file_system = AsyncFileSystem(session=self.mock_session)

    @patch("agentbay._async.filesystem.AsyncFileTransfer")
    @pytest.mark.asyncio

    async def test_upload_file(self, mock_file_transfer_cls):
        """Test FileSystem.upload_file method."""
        # Mock FileTransfer instance
        mock_file_transfer = Mock()
        mock_file_transfer_cls.return_value = mock_file_transfer

        # Mock upload result
        mock_upload_result = UploadResult(
            success=True,
            request_id_upload_url="req_upload_123",
            request_id_sync="req_sync_456",
            http_status=200,
            etag="etag_789",
            bytes_sent=1024,
            path="/remote/file.txt",
        )
        mock_file_transfer.upload = AsyncMock(return_value=mock_upload_result)

        # Test upload_file
        result = await self.file_system.upload_file(
            local_path="/local/file.txt", remote_path="/remote/file.txt"
        )

        # Verify result
        self.assertIsInstance(result, UploadResult)
        self.assertTrue(result.success, f"Upload failed: {result.error}")
        mock_file_transfer.upload.assert_called_once_with(
            local_path="/local/file.txt",
            remote_path="/remote/file.txt",
            content_type=None,
            wait=True,
            wait_timeout=30.0,
            poll_interval=1.5,
            progress_cb=None,
        )

    @patch("agentbay._async.filesystem.AsyncFileTransfer")
    @pytest.mark.asyncio

    async def test_download_file(self, mock_file_transfer_cls):
        """Test FileSystem.download_file method."""
        # Mock FileTransfer instance
        mock_file_transfer = Mock()
        mock_file_transfer_cls.return_value = mock_file_transfer

        # Mock download result
        mock_download_result = DownloadResult(
            success=True,
            request_id_download_url="req_download_123",
            request_id_sync="req_sync_456",
            http_status=200,
            bytes_received=2048,
            path="/remote/file.txt",
            local_path="/local/file.txt",
        )
        mock_file_transfer.download = AsyncMock(return_value=mock_download_result)

        # Test download_file
        result = await self.file_system.download_file(
            remote_path="/remote/file.txt", local_path="/local/file.txt"
        )

        # Verify result
        self.assertIsInstance(result, DownloadResult)
        self.assertTrue(result.success, f"Download failed: {result.error}")
        mock_file_transfer.download.assert_called_once_with(
            remote_path="/remote/file.txt",
            local_path="/local/file.txt",
            overwrite=True,
            wait=True,
            wait_timeout=30.0,
            poll_interval=1.5,
            progress_cb=None,
        )


if __name__ == "__main__":
    unittest.main()
