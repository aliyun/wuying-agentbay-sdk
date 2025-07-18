import unittest
from unittest.mock import MagicMock, patch

from agentbay.filesystem.filesystem import (
    BoolResult,
    DirectoryListResult,
    FileContentResult,
    FileInfoResult,
    FileSearchResult,
    FileSystem,
    MultipleFileContentResult,
)
from agentbay.model import OperationResult


class DummySession:
    def __init__(self):
        self.api_key = "dummy_key"
        self.session_id = "dummy_session"
        self.client = MagicMock()

    def get_api_key(self):
        return self.api_key

    def get_session_id(self):
        return self.session_id

    def get_client(self):
        return self.client


class TestFileSystem(unittest.TestCase):
    def setUp(self):
        self.session = DummySession()
        self.fs = FileSystem(self.session)

    @patch("agentbay.filesystem.filesystem.FileSystem._call_mcp_tool")
    def test_read_file_success(self, mock_call_mcp_tool):
        """
        Test read_file method with successful response.
        """
        mock_result = OperationResult(
            request_id="request-123", success=True, data="file content"
        )
        mock_call_mcp_tool.return_value = mock_result

        result = self.fs.read_file("/path/to/file.txt")
        self.assertIsInstance(result, FileContentResult)
        self.assertTrue(result.success)
        self.assertEqual(result.content, "file content")
        self.assertEqual(result.request_id, "request-123")

    @patch("agentbay.filesystem.filesystem.FileSystem._call_mcp_tool")
    def test_read_file_error(self, mock_call_mcp_tool):
        """
        Test read_file method with error response.
        """
        mock_result = OperationResult(
            request_id="request-123",
            success=False,
            error_message="Error in response: some error message",
        )
        mock_call_mcp_tool.return_value = mock_result

        result = self.fs.read_file("/path/to/file.txt")
        self.assertIsInstance(result, FileContentResult)
        self.assertFalse(result.success)
        self.assertEqual(result.request_id, "request-123")
        self.assertEqual(result.error_message, "Error in response: some error message")
        self.assertEqual(result.content, "")

    @patch("agentbay.filesystem.filesystem.FileSystem._call_mcp_tool")
    def test_read_file_error_format(self, mock_call_mcp_tool):
        """
        Test read_file method with invalid format response.
        """
        mock_result = OperationResult(
            request_id="request-123",
            success=False,
            error_message="Invalid response body",
        )
        mock_call_mcp_tool.return_value = mock_result

        result = self.fs.read_file("/path/to/file.txt")
        self.assertIsInstance(result, FileContentResult)
        self.assertFalse(result.success)
        self.assertEqual(result.request_id, "request-123")
        self.assertEqual(result.error_message, "Invalid response body")

    @patch("agentbay.filesystem.filesystem.FileSystem._call_mcp_tool")
    def test_create_directory_success(self, mock_call_mcp_tool):
        """
        Test create_directory method with successful response.
        """
        mock_result = OperationResult(
            request_id="request-123", success=True, data="True"
        )
        mock_call_mcp_tool.return_value = mock_result

        result = self.fs.create_directory("/path/to/directory")
        self.assertIsInstance(result, BoolResult)
        self.assertTrue(result.success)
        self.assertEqual(result.request_id, "request-123")
        self.assertTrue(result.data)

    @patch("agentbay.filesystem.filesystem.FileSystem._call_mcp_tool")
    def test_create_directory_error(self, mock_call_mcp_tool):
        """
        Test create_directory method with error response.
        """
        # Create an OperationResult object with error_message and request_id
        mock_result = OperationResult(
            request_id="request-123",
            success=False,
            error_message="Directory creation failed",
        )
        mock_call_mcp_tool.return_value = mock_result

        result = self.fs.create_directory("/path/to/directory")
        self.assertIsInstance(result, BoolResult)
        self.assertFalse(result.success)
        self.assertEqual(result.request_id, "request-123")
        self.assertEqual(result.error_message, "Directory creation failed")

    @patch("agentbay.filesystem.filesystem.FileSystem._call_mcp_tool")
    def test_edit_file_success(self, mock_call_mcp_tool):
        """
        Test edit_file method with successful response.
        """
        mock_result = OperationResult(
            request_id="request-123", success=True, data="True"
        )
        mock_call_mcp_tool.return_value = mock_result

        result = self.fs.edit_file(
            "/path/to/file.txt", [{"oldText": "foo", "newText": "bar"}]
        )
        self.assertIsInstance(result, BoolResult)
        self.assertTrue(result.success)
        self.assertEqual(result.request_id, "request-123")
        self.assertTrue(result.data)

    @patch("agentbay.filesystem.filesystem.FileSystem._call_mcp_tool")
    def test_edit_file_error(self, mock_call_mcp_tool):
        """
        Test edit_file method with error response.
        """
        mock_result = OperationResult(
            request_id="request-123",
            success=False,
            error_message="Edit failed",
        )
        mock_call_mcp_tool.return_value = mock_result

        result = self.fs.edit_file(
            "/path/to/file.txt", [{"oldText": "foo", "newText": "bar"}]
        )
        self.assertIsInstance(result, BoolResult)
        self.assertFalse(result.success)
        self.assertEqual(result.request_id, "request-123")
        self.assertEqual(result.error_message, "Edit failed")

    @patch("agentbay.filesystem.filesystem.FileSystem._call_mcp_tool")
    def test_write_file_success(self, mock_call_mcp_tool):
        """
        Test write_file method with successful response.
        """
        mock_result = OperationResult(
            request_id="request-123", success=True, data="True"
        )
        mock_call_mcp_tool.return_value = mock_result

        result = self.fs.write_file(
            "/path/to/file.txt", "content to write", "overwrite"
        )
        self.assertIsInstance(result, BoolResult)
        self.assertTrue(result.success)
        self.assertEqual(result.request_id, "request-123")
        self.assertTrue(result.data)

    @patch("agentbay.filesystem.filesystem.FileSystem._call_mcp_tool")
    def test_write_file_error(self, mock_call_mcp_tool):
        """
        Test write_file method with error response.
        """
        mock_result = OperationResult(
            request_id="request-123",
            success=False,
            error_message="Write failed",
        )
        mock_call_mcp_tool.return_value = mock_result

        result = self.fs.write_file(
            "/path/to/file.txt", "content to write", "overwrite"
        )
        self.assertIsInstance(result, BoolResult)
        self.assertFalse(result.success)
        self.assertEqual(result.request_id, "request-123")
        self.assertEqual(result.error_message, "Write failed")

    @patch("agentbay.filesystem.filesystem.FileSystem._call_mcp_tool")
    def test_get_file_info_success(self, mock_call_mcp_tool):
        """
        Test get_file_info method with successful response.
        """
        mock_result = OperationResult(
            request_id="request-123",
            success=True,
            data="name: test.txt\nsize: 100\nmodified: 2023-01-01T12:00:00Z\nisDirectory: false",
        )
        mock_call_mcp_tool.return_value = mock_result

        result = self.fs.get_file_info("/path/to/file.txt")
        self.assertIsInstance(result, FileInfoResult)
        self.assertTrue(result.success)
        self.assertEqual(result.request_id, "request-123")
        self.assertEqual(result.file_info["name"], "test.txt")
        self.assertEqual(result.file_info["size"], 100)
        self.assertEqual(result.file_info["modified"], "2023-01-01T12:00:00Z")
        self.assertEqual(result.file_info["isDirectory"], False)

    @patch("agentbay.filesystem.filesystem.FileSystem._call_mcp_tool")
    def test_get_file_info_error(self, mock_call_mcp_tool):
        """
        Test get_file_info method with error response.
        """
        mock_result = OperationResult(
            request_id="request-123",
            success=False,
            error_message="File not found",
        )
        mock_call_mcp_tool.return_value = mock_result

        result = self.fs.get_file_info("/path/to/file.txt")
        self.assertIsInstance(result, FileInfoResult)
        self.assertFalse(result.success)
        self.assertEqual(result.request_id, "request-123")
        self.assertEqual(result.error_message, "File not found")

    @patch("agentbay.filesystem.filesystem.FileSystem._call_mcp_tool")
    def test_list_directory_success(self, mock_call_mcp_tool):
        """
        Test list_directory method with successful response.
        """
        mock_result = OperationResult(
            request_id="request-123",
            success=True,
            data="[FILE] file1.txt\n[DIR] dir1\n[FILE] file2.txt",
        )
        mock_call_mcp_tool.return_value = mock_result

        result = self.fs.list_directory("/path/to/directory")
        self.assertIsInstance(result, DirectoryListResult)
        self.assertTrue(result.success)
        self.assertEqual(result.request_id, "request-123")
        self.assertEqual(len(result.entries), 3)
        self.assertEqual(result.entries[0]["name"], "file1.txt")
        self.assertEqual(result.entries[0]["isDirectory"], False)
        self.assertEqual(result.entries[1]["name"], "dir1")
        self.assertEqual(result.entries[1]["isDirectory"], True)
        self.assertEqual(result.entries[2]["name"], "file2.txt")
        self.assertEqual(result.entries[2]["isDirectory"], False)

    @patch("agentbay.filesystem.filesystem.FileSystem._call_mcp_tool")
    def test_list_directory_error(self, mock_call_mcp_tool):
        """
        Test list_directory method with error response.
        """
        mock_result = OperationResult(
            request_id="request-123",
            success=False,
            error_message="Directory not found",
        )
        mock_call_mcp_tool.return_value = mock_result

        result = self.fs.list_directory("/path/to/directory")
        self.assertIsInstance(result, DirectoryListResult)
        self.assertFalse(result.success)
        self.assertEqual(result.request_id, "request-123")
        self.assertEqual(result.error_message, "Directory not found")
        self.assertEqual(result.entries, [])

    @patch("agentbay.filesystem.filesystem.FileSystem._call_mcp_tool")
    def test_move_file_success(self, mock_call_mcp_tool):
        """
        Test move_file method with successful response.
        """
        mock_result = OperationResult(
            request_id="request-123", success=True, data="True"
        )
        mock_call_mcp_tool.return_value = mock_result

        result = self.fs.move_file("/path/to/source.txt", "/path/to/dest.txt")
        self.assertIsInstance(result, BoolResult)
        self.assertTrue(result.success)
        self.assertEqual(result.request_id, "request-123")
        self.assertTrue(result.data)

    @patch("agentbay.filesystem.filesystem.FileSystem._call_mcp_tool")
    def test_move_file_error(self, mock_call_mcp_tool):
        """
        Test move_file method with error response.
        """
        mock_result = OperationResult(
            request_id="request-123",
            success=False,
            error_message="Move operation failed",
        )
        mock_call_mcp_tool.return_value = mock_result

        result = self.fs.move_file("/path/to/source.txt", "/path/to/dest.txt")
        self.assertIsInstance(result, BoolResult)
        self.assertFalse(result.success)
        self.assertEqual(result.request_id, "request-123")
        self.assertEqual(result.error_message, "Move operation failed")

    @patch("agentbay.filesystem.filesystem.FileSystem._call_mcp_tool")
    def test_read_multiple_files_success(self, mock_call_mcp_tool):
        """
        Test read_multiple_files method with successful response.
        """
        mock_result = OperationResult(
            request_id="request-123",
            success=True,
            data="file1.txt:\nFile 1 content\n---\nfile2.txt:\nFile 2 content\n---",
        )
        mock_call_mcp_tool.return_value = mock_result

        result = self.fs.read_multiple_files(
            ["/path/to/file1.txt", "/path/to/file2.txt"]
        )
        self.assertIsInstance(result, MultipleFileContentResult)
        self.assertTrue(result.success)
        self.assertEqual(result.request_id, "request-123")
        self.assertEqual(len(result.contents), 2)
        self.assertEqual(result.contents["file1.txt"], "File 1 content")
        self.assertEqual(result.contents["file2.txt"], "File 2 content")

    @patch("agentbay.filesystem.filesystem.FileSystem._call_mcp_tool")
    def test_search_files_success(self, mock_call_mcp_tool):
        """
        Test search_files method with successful response.
        """
        mock_result = OperationResult(
            request_id="request-123",
            success=True,
            data="/path/to/file1.txt\n/path/to/file2.txt",
        )
        mock_call_mcp_tool.return_value = mock_result

        result = self.fs.search_files("/path/to", "pattern")
        self.assertIsInstance(result, FileSearchResult)
        self.assertTrue(result.success)
        self.assertEqual(result.request_id, "request-123")
        self.assertEqual(len(result.matches), 2)
        self.assertEqual(result.matches[0], "/path/to/file1.txt")
        self.assertEqual(result.matches[1], "/path/to/file2.txt")

    @patch("agentbay.filesystem.filesystem.FileSystem._call_mcp_tool")
    def test_search_files_with_exclude(self, mock_call_mcp_tool):
        """
        Test search_files method with exclude patterns.
        """
        mock_result = OperationResult(
            request_id="request-123", success=True, data="/path/to/file1.txt"
        )
        mock_call_mcp_tool.return_value = mock_result

        result = self.fs.search_files(
            "/path/to", "pattern", exclude_patterns=["*.py", "node_modules"]
        )
        self.assertIsInstance(result, FileSearchResult)
        self.assertTrue(result.success)
        self.assertEqual(result.request_id, "request-123")
        self.assertEqual(len(result.matches), 1)
        self.assertEqual(result.matches[0], "/path/to/file1.txt")

    @patch("agentbay.filesystem.filesystem.FileSystem.get_file_info")
    @patch("agentbay.filesystem.filesystem.FileSystem.read_file")
    def test_read_large_file_success(self, mock_read_file, mock_get_file_info):
        """
        Test read_large_file method with successful response.
        """
        # Mock file info
        file_info_result = FileInfoResult(
            request_id="request-123",
            success=True,
            file_info={"size": 600, "isDirectory": False},
        )
        mock_get_file_info.return_value = file_info_result

        # Mock chunked reads
        mock_read_file.side_effect = [
            FileContentResult(
                request_id="request-123-1", success=True, content="chunk1"
            ),
            FileContentResult(
                request_id="request-123-2", success=True, content="chunk2"
            ),
            FileContentResult(
                request_id="request-123-3", success=True, content="chunk3"
            ),
        ]

        result = self.fs.read_large_file("/path/to/large_file.txt", chunk_size=200)
        self.assertIsInstance(result, FileContentResult)
        self.assertTrue(result.success)
        self.assertEqual(result.content, "chunk1chunk2chunk3")
        mock_get_file_info.assert_called_once()
        self.assertEqual(mock_read_file.call_count, 3)

    @patch("agentbay.filesystem.filesystem.FileSystem.get_file_info")
    def test_read_large_file_error(self, mock_get_file_info):
        """
        Test read_large_file method with error in get_file_info.
        """
        error_result = FileInfoResult(
            request_id="request-123",
            success=False,
            error_message="File not found",
        )
        mock_get_file_info.return_value = error_result

        result = self.fs.read_large_file("/path/to/large_file.txt")
        self.assertIsInstance(result, FileContentResult)
        self.assertFalse(result.success)
        self.assertEqual(result.error_message, "File not found")
        mock_get_file_info.assert_called_once()

    @patch("agentbay.filesystem.filesystem.FileSystem.write_file")
    def test_write_large_file_success(self, mock_write_file):
        """
        Test write_large_file method with successful response.
        """
        mock_write_file.side_effect = [
            BoolResult(request_id="request-123-1", success=True, data=True),
            BoolResult(request_id="request-123-2", success=True, data=True),
            BoolResult(request_id="request-123-3", success=True, data=True),
        ]

        content = "a" * 300  # 300 bytes content
        result = self.fs.write_large_file(
            "/path/to/large_file.txt", content, chunk_size=100
        )
        self.assertIsInstance(result, BoolResult)
        self.assertTrue(result.success)
        self.assertTrue(result.data)
        self.assertEqual(mock_write_file.call_count, 3)

        # Verify the calls
        mock_write_file.assert_any_call(
            "/path/to/large_file.txt", "a" * 100, "overwrite"
        )
        mock_write_file.assert_any_call("/path/to/large_file.txt", "a" * 100, "append")

    @patch("agentbay.filesystem.filesystem.FileSystem.write_file")
    def test_write_large_file_small_content(self, mock_write_file):
        """
        Test write_large_file method with content smaller than chunk size.
        """
        mock_write_file.return_value = BoolResult(
            request_id="request-123", success=True, data=True
        )

        content = "small content"
        result = self.fs.write_large_file("/path/to/file.txt", content, chunk_size=100)
        self.assertIsInstance(result, BoolResult)
        self.assertTrue(result.success)
        self.assertTrue(result.data)
        mock_write_file.assert_called_once_with("/path/to/file.txt", content)

    @patch("agentbay.filesystem.filesystem.FileSystem.write_file")
    def test_write_large_file_error(self, mock_write_file):
        """
        Test write_large_file method with error in first write.
        """
        mock_write_file.return_value = BoolResult(
            request_id="request-123",
            success=False,
            error_message="Write error",
        )

        content = "a" * 300  # 300 bytes content
        result = self.fs.write_large_file(
            "/path/to/large_file.txt", content, chunk_size=100
        )
        self.assertIsInstance(result, BoolResult)
        self.assertFalse(result.success)
        self.assertEqual(result.error_message, "Write error")
        mock_write_file.assert_called_once()

    def test_write_file_invalid_mode(self):
        """
        Test write_file method with invalid mode.
        """
        result = self.fs.write_file("/path/to/file.txt", "content", "invalid_mode")
        self.assertIsInstance(result, BoolResult)
        self.assertFalse(result.success)
        self.assertIn("Invalid write mode", result.error_message)


if __name__ == "__main__":
    unittest.main()
