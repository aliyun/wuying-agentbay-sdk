import unittest
from unittest.mock import patch, MagicMock

from agentbay.exceptions import FileError
from agentbay.filesystem.filesystem import FileSystem
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

    @patch("agentbay.filesystem.filesystem.extract_request_id")
    @patch("agentbay.filesystem.filesystem.CallMcpToolRequest")
    def test_read_file_success(self, MockCallMcpToolRequest, mock_extract_request_id):
        print("test_read_file_success")
        mock_response = MagicMock()
        mock_response.to_map.return_value = {
            "body": {"Data": {"content": [{"text": "file content"}]}}
        }
        mock_extract_request_id.return_value = "request-123"
        self.session.client.call_mcp_tool.return_value = mock_response

        success, result = self.fs.read_file("/path/to/file.txt")
        self.assertTrue(success)
        self.assertEqual(result, "file content")
        MockCallMcpToolRequest.assert_called_once()

    @patch("agentbay.filesystem.filesystem.extract_request_id")
    @patch("agentbay.filesystem.filesystem.CallMcpToolRequest")
    def test_read_file_error(self, MockCallMcpToolRequest, mock_extract_request_id):
        print("test_read_file_error")
        mock_response = MagicMock()
        mock_response.to_map.return_value = {
            "body": {
                "Data": {
                    "isError": True,
                    "content": [{"text": "some error message"}],
                }
            }
        }
        mock_extract_request_id.return_value = "request-123"
        self.session.client.call_mcp_tool.return_value = mock_response

        success, error_msg = self.fs.read_file("/path/to/file.txt")
        self.assertFalse(success)
        self.assertIn("Error in response: some error message", error_msg)

    @patch("agentbay.filesystem.filesystem.extract_request_id")
    @patch("agentbay.filesystem.filesystem.CallMcpToolRequest")
    def test_read_file_error_format(self, MockCallMcpToolRequest, mock_extract_request_id):
        print("test_read_file_error_format")
        mock_response = MagicMock()
        mock_response.to_map.return_value = {"some_unknown_key": {""}}
        mock_extract_request_id.return_value = "request-123"
        self.session.client.call_mcp_tool.return_value = mock_response

        success, error_msg = self.fs.read_file("/path/to/file.txt")
        self.assertFalse(success)
        self.assertIn("Invalid response body", error_msg)

    @patch("agentbay.filesystem.filesystem.extract_request_id")
    @patch("agentbay.filesystem.filesystem.CallMcpToolRequest")
    def test_create_directory_success(self, MockCallMcpToolRequest, mock_extract_request_id):
        """
        Test create_directory method with successful response.
        """
        mock_response = MagicMock()
        mock_response.to_map.return_value = {
            "body": {
                "Data": {
                    "content": [{"text": "True"}],
                    "isError": False,
                }
            }
        }
        mock_extract_request_id.return_value = "request-123"
        self.session.get_client().call_mcp_tool.return_value = mock_response

        success, result = self.fs.create_directory("/path/to/directory")
        self.assertTrue(success)
        self.assertTrue(result)

    @patch("agentbay.filesystem.filesystem.extract_request_id")
    @patch("agentbay.filesystem.filesystem.CallMcpToolRequest")
    def test_create_directory_error(self, MockCallMcpToolRequest, mock_extract_request_id):
        """
        Test create_directory method with error response.
        """
        mock_response = MagicMock()
        mock_response.to_map.return_value = {
            "body": {
                "Data": {
                    "content": [{"text": "Directory creation failed"}],
                    "isError": True,
                }
            }
        }
        mock_extract_request_id.return_value = "request-123"
        self.session.get_client().call_mcp_tool.return_value = mock_response

        success, error_msg = self.fs.create_directory("/path/to/directory")
        self.assertFalse(success)
        self.assertIn("Error in response: Directory creation failed", error_msg)

    @patch("agentbay.filesystem.filesystem.extract_request_id")
    @patch("agentbay.filesystem.filesystem.CallMcpToolRequest")
    def test_edit_file_success(self, MockCallMcpToolRequest, mock_extract_request_id):
        """
        Test edit_file method with successful response.
        """
        mock_response = MagicMock()
        mock_response.to_map.return_value = {
            "body": {
                "Data": {
                    "content": [{"text": "True"}],
                    "isError": False,
                }
            }
        }
        mock_extract_request_id.return_value = "request-123"
        self.session.get_client().call_mcp_tool.return_value = mock_response

        success, result = self.fs.edit_file(
            "/path/to/file.txt", [{"oldText": "foo", "newText": "bar"}]
        )
        print(f"type(result)= {type(result)}")
        self.assertTrue(success)
        self.assertTrue(result)

    @patch("agentbay.filesystem.filesystem.extract_request_id")
    @patch("agentbay.filesystem.filesystem.CallMcpToolRequest")
    def test_edit_file_error(self, MockCallMcpToolRequest, mock_extract_request_id):
        """
        Test edit_file method with error response.
        """
        mock_response = MagicMock()
        mock_response.to_map.return_value = {
            "body": {
                "Data": {
                    "content": [{"text": "Edit failed"}],
                    "isError": True,
                }
            }
        }
        mock_extract_request_id.return_value = "request-123"
        self.session.get_client().call_mcp_tool.return_value = mock_response

        success, error_msg = self.fs.edit_file(
            "/path/to/file.txt", [{"oldText": "foo", "newText": "bar"}]
        )
        self.assertFalse(success)
        self.assertIn("Error in response: Edit failed", error_msg)

    @patch("agentbay.filesystem.filesystem.extract_request_id")
    @patch("agentbay.filesystem.filesystem.CallMcpToolRequest")
    def test_write_file_success(self, MockCallMcpToolRequest, mock_extract_request_id):
        """
        Test write_file method with successful response.
        """
        mock_response = MagicMock()
        mock_response.to_map.return_value = {
            "body": {
                "Data": {
                    "content": [{"text": "True"}],
                    "isError": False,
                }
            }
        }
        mock_extract_request_id.return_value = "request-123"
        self.session.get_client().call_mcp_tool.return_value = mock_response

        success, result = self.fs.write_file(
            "/path/to/file.txt", "content to write", "overwrite"
        )
        self.assertTrue(success)
        self.assertTrue(result)

    @patch("agentbay.filesystem.filesystem.extract_request_id")
    @patch("agentbay.filesystem.filesystem.CallMcpToolRequest")
    def test_write_file_error(self, MockCallMcpToolRequest, mock_extract_request_id):
        """
        Test write_file method with error response.
        """
        mock_response = MagicMock()
        mock_response.to_map.return_value = {
            "body": {
                "Data": {
                    "content": [{"text": "Write failed"}],
                    "isError": True,
                }
            }
        }
        mock_extract_request_id.return_value = "request-123"
        self.session.get_client().call_mcp_tool.return_value = mock_response

        success, error_msg = self.fs.write_file(
            "/path/to/file.txt", "content to write", "overwrite"
        )
        self.assertFalse(success)
        self.assertIn("Error in response: Write failed", error_msg)

    @patch("agentbay.filesystem.filesystem.extract_request_id")
    @patch("agentbay.filesystem.filesystem.CallMcpToolRequest")
    def test_get_file_info_success(self, MockCallMcpToolRequest, mock_extract_request_id):
        """
        Test get_file_info method with successful response.
        """
        mock_response = MagicMock()
        mock_response.to_map.return_value = {
            "body": {
                "Data": {
                    "content": [
                        {
                            "text": "name: test.txt\nsize: 100\nmodified: 2023-01-01T12:00:00Z\nisDirectory: false"
                        }
                    ],
                    "isError": False,
                }
            }
        }
        mock_extract_request_id.return_value = "request-123"
        self.session.get_client().call_mcp_tool.return_value = mock_response

        success, result = self.fs.get_file_info("/path/to/file.txt")
        self.assertTrue(success)
        self.assertEqual(result["name"], "test.txt")
        self.assertEqual(result["size"], 100)
        self.assertEqual(result["modified"], "2023-01-01T12:00:00Z")
        self.assertEqual(result["isDirectory"], False)

    @patch("agentbay.filesystem.filesystem.extract_request_id")
    @patch("agentbay.filesystem.filesystem.CallMcpToolRequest")
    def test_get_file_info_error(self, MockCallMcpToolRequest, mock_extract_request_id):
        """
        Test get_file_info method with error response.
        """
        mock_response = MagicMock()
        mock_response.to_map.return_value = {
            "body": {
                "Data": {
                    "content": [{"text": "File not found"}],
                    "isError": True,
                }
            }
        }
        mock_extract_request_id.return_value = "request-123"
        self.session.get_client().call_mcp_tool.return_value = mock_response

        success, error_msg = self.fs.get_file_info("/path/to/file.txt")
        self.assertFalse(success)
        self.assertIn("Error in response: File not found", error_msg)

    @patch("agentbay.filesystem.filesystem.extract_request_id")
    @patch("agentbay.filesystem.filesystem.CallMcpToolRequest")
    def test_list_directory_success(self, MockCallMcpToolRequest, mock_extract_request_id):
        """
        Test list_directory method with successful response.
        """
        mock_response = MagicMock()
        mock_response.to_map.return_value = {
            "body": {
                "Data": {
                    "content": [
                        {
                            "text": "file:/path/to/file1.txt\ndirectory:/path/to/dir1\nfile:/path/to/file2.txt"
                        }
                    ],
                    "isError": False,
                }
            }
        }
        mock_extract_request_id.return_value = "request-123"
        self.session.get_client().call_mcp_tool.return_value = mock_response

        success, result = self.fs.list_directory("/path/to")
        self.assertTrue(success)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0]["path"], "/path/to/file1.txt")
        self.assertEqual(result[0]["type"], "file")
        self.assertTrue(result[0]["is_file"])
        self.assertEqual(result[1]["path"], "/path/to/dir1")
        self.assertEqual(result[1]["type"], "directory")
        self.assertTrue(result[1]["is_directory"])

    @patch("agentbay.filesystem.filesystem.extract_request_id")
    @patch("agentbay.filesystem.filesystem.CallMcpToolRequest")
    def test_list_directory_error(self, MockCallMcpToolRequest, mock_extract_request_id):
        """
        Test list_directory method with error response.
        """
        mock_response = MagicMock()
        mock_response.to_map.return_value = {
            "body": {
                "Data": {
                    "content": [{"text": "Directory not found"}],
                    "isError": True,
                }
            }
        }
        mock_extract_request_id.return_value = "request-123"
        self.session.get_client().call_mcp_tool.return_value = mock_response

        success, error_msg = self.fs.list_directory("/path/to")
        self.assertFalse(success)
        self.assertIn("Error in response: Directory not found", error_msg)

    @patch("agentbay.filesystem.filesystem.extract_request_id")
    @patch("agentbay.filesystem.filesystem.CallMcpToolRequest")
    def test_move_file_success(self, MockCallMcpToolRequest, mock_extract_request_id):
        """
        Test move_file method with successful response.
        """
        mock_response = MagicMock()
        mock_response.to_map.return_value = {
            "body": {
                "Data": {
                    "content": [{"text": "True"}],
                    "isError": False,
                }
            }
        }
        mock_extract_request_id.return_value = "request-123"
        self.session.get_client().call_mcp_tool.return_value = mock_response

        success, result = self.fs.move_file("/path/source.txt", "/path/destination.txt")
        self.assertTrue(success)
        self.assertTrue(result)

    @patch("agentbay.filesystem.filesystem.extract_request_id")
    @patch("agentbay.filesystem.filesystem.CallMcpToolRequest")
    def test_move_file_error(self, MockCallMcpToolRequest, mock_extract_request_id):
        """
        Test move_file method with error response.
        """
        mock_response = MagicMock()
        mock_response.to_map.return_value = {
            "body": {
                "Data": {
                    "content": [{"text": "Move failed"}],
                    "isError": True,
                }
            }
        }
        mock_extract_request_id.return_value = "request-123"
        self.session.get_client().call_mcp_tool.return_value = mock_response

        success, error_msg = self.fs.move_file("/path/source.txt", "/path/destination.txt")
        self.assertFalse(success)
        self.assertIn("Error in response: Move failed", error_msg)

    @patch("agentbay.filesystem.filesystem.extract_request_id")
    @patch("agentbay.filesystem.filesystem.CallMcpToolRequest")
    def test_read_multiple_files_success(self, MockCallMcpToolRequest, mock_extract_request_id):
        """
        Test read_multiple_files method with successful response.
        """
        mock_response = MagicMock()
        mock_response.to_map.return_value = {
            "body": {
                "Data": {
                    "content": [
                        {
                            "text": '--- FILE: /path/to/file1.txt ---\ncontent of file1\n--- FILE: /path/to/file2.txt ---\ncontent of file2'
                        }
                    ],
                    "isError": False,
                }
            }
        }
        mock_extract_request_id.return_value = "request-123"
        self.session.get_client().call_mcp_tool.return_value = mock_response

        success, result = self.fs.read_multiple_files(["/path/to/file1.txt", "/path/to/file2.txt"])
        self.assertTrue(success)
        self.assertEqual(result["/path/to/file1.txt"], "content of file1")
        self.assertEqual(result["/path/to/file2.txt"], "content of file2")

    @patch("agentbay.filesystem.filesystem.extract_request_id")
    @patch("agentbay.filesystem.filesystem.CallMcpToolRequest")
    def test_search_files_success(self, MockCallMcpToolRequest, mock_extract_request_id):
        """
        Test search_files method with successful response.
        """
        mock_response = MagicMock()
        mock_response.to_map.return_value = {
            "body": {
                "Data": {
                    "content": [
                        {
                            "text": "/path/to/file1.txt\n/path/to/file2.txt\n/path/to/subdir/file3.txt"
                        }
                    ],
                    "isError": False,
                }
            }
        }
        mock_extract_request_id.return_value = "request-123"
        self.session.get_client().call_mcp_tool.return_value = mock_response

        success, result = self.fs.search_files("/path/to", "*.txt")
        self.assertTrue(success)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], "/path/to/file1.txt")
        self.assertEqual(result[1], "/path/to/file2.txt")
        self.assertEqual(result[2], "/path/to/subdir/file3.txt")

    @patch("agentbay.filesystem.filesystem.extract_request_id")
    @patch("agentbay.filesystem.filesystem.CallMcpToolRequest")
    def test_search_files_with_exclude(self, MockCallMcpToolRequest, mock_extract_request_id):
        """
        Test search_files method with exclude patterns and successful response.
        """
        mock_response = MagicMock()
        mock_response.to_map.return_value = {
            "body": {
                "Data": {
                    "content": [
                        {
                            "text": "/path/to/file1.txt\n/path/to/file2.txt"
                        }
                    ],
                    "isError": False,
                }
            }
        }
        mock_extract_request_id.return_value = "request-123"
        self.session.get_client().call_mcp_tool.return_value = mock_response

        success, result = self.fs.search_files("/path/to", "*.txt", exclude_patterns=["**/subdir/**"])
        self.assertTrue(success)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], "/path/to/file1.txt")
        self.assertEqual(result[1], "/path/to/file2.txt")

    @patch("agentbay.filesystem.filesystem.FileSystem.get_file_info")
    @patch("agentbay.filesystem.filesystem.FileSystem.read_file")
    def test_read_large_file_success(self, mock_read_file, mock_get_file_info):
        """
        Test read_large_file method with successful response.
        """
        # Mock file info
        mock_get_file_info.return_value = (True, {"size": 600})

        # Mock chunked reads
        mock_read_file.side_effect = [
            (True, "chunk1"),
            (True, "chunk2"),
            (True, "chunk3"),
        ]

        success, result = self.fs.read_large_file("/path/to/large_file.txt", chunk_size=200)
        self.assertTrue(success)
        self.assertEqual(result, "chunk1chunk2chunk3")
        mock_get_file_info.assert_called_once()
        self.assertEqual(mock_read_file.call_count, 3)

    @patch("agentbay.filesystem.filesystem.FileSystem.get_file_info")
    def test_read_large_file_error(self, mock_get_file_info):
        """
        Test read_large_file method with error in get_file_info.
        """
        mock_get_file_info.return_value = (False, "File not found")

        success, error = self.fs.read_large_file("/path/to/large_file.txt")
        self.assertFalse(success)
        self.assertEqual(error, "File not found")
        mock_get_file_info.assert_called_once()

    @patch("agentbay.filesystem.filesystem.FileSystem.write_file")
    def test_write_large_file_success(self, mock_write_file):
        """
        Test write_large_file method with successful response.
        """
        mock_write_file.side_effect = [
            (True, True),  # First chunk (overwrite)
            (True, True),  # Second chunk (append)
            (True, True),  # Third chunk (append)
        ]

        content = "a" * 300  # 300 bytes content
        success, result = self.fs.write_large_file("/path/to/large_file.txt", content, chunk_size=100)
        self.assertTrue(success)
        self.assertTrue(result)
        self.assertEqual(mock_write_file.call_count, 3)

        # Verify the calls
        mock_write_file.assert_any_call("/path/to/large_file.txt", "a" * 100, "overwrite")
        mock_write_file.assert_any_call("/path/to/large_file.txt", "a" * 100, "append")

    @patch("agentbay.filesystem.filesystem.FileSystem.write_file")
    def test_write_large_file_small_content(self, mock_write_file):
        """
        Test write_large_file method with content smaller than chunk size.
        """
        mock_write_file.return_value = (True, True)

        content = "small content"
        success, result = self.fs.write_large_file("/path/to/file.txt", content, chunk_size=100)
        self.assertTrue(success)
        self.assertTrue(result)
        mock_write_file.assert_called_once_with("/path/to/file.txt", content)

    @patch("agentbay.filesystem.filesystem.FileSystem.write_file")
    def test_write_large_file_error(self, mock_write_file):
        """
        Test write_large_file method with error in first write.
        """
        mock_write_file.return_value = (False, "Write error")

        content = "a" * 300  # 300 bytes content
        success, error = self.fs.write_large_file("/path/to/large_file.txt", content, chunk_size=100)
        self.assertFalse(success)
        self.assertEqual(error, "Write error")
        mock_write_file.assert_called_once()

    def test_write_file_invalid_mode(self):
        """
        Test write_file method with invalid mode.
        """
        success, error = self.fs.write_file("/path/to/file.txt", "content", "invalid_mode")
        self.assertFalse(success)
        self.assertIn("Invalid write mode", error)


if __name__ == "__main__":
    unittest.main()
