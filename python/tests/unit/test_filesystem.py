import unittest
from unittest.mock import patch, MagicMock

from agentbay.exceptions import FileError
from agentbay.filesystem.filesystem import \
    FileSystem  # Adjust based on actual module path


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

    @patch("agentbay.filesystem.filesystem.CallMcpToolRequest")
    def test_read_file_success(self, MockCallMcpToolRequest):
        print("test_read_file_success")
        mock_response = MagicMock()
        mock_response.to_map.return_value = {
            "body": {"Data": {"content": [{"text": "file content"}]}}
        }
        self.session.client.call_mcp_tool.return_value = mock_response

        result = self.fs.read_file("/path/to/file.txt")
        self.assertEqual(result, "file content")
        MockCallMcpToolRequest.assert_called_once()

    @patch("agentbay.filesystem.filesystem.CallMcpToolRequest")
    def test_read_file_get_false(self, MockCallMcpToolRequest):
        print("test_read_file_no_content")
        mock_response = MagicMock()
        mock_response.to_map.return_value = {
            "body": {
                "Data": {
                    "isError": True,
                    "content": [{"text": "some error message"}],
                }
            }
        }
        self.session.client.call_mcp_tool.return_value = mock_response

        with self.assertRaises(FileError) as context:
            self.fs.read_file("/path/to/file.txt")

        self.assertIn("Failed to read file:", str(context.exception))

    @patch("agentbay.filesystem.filesystem.CallMcpToolRequest")
    def test_read_file_error_format(self, MockCallMcpToolRequest):
        print("test_read_file_no_content")
        mock_response = MagicMock()
        mock_response.to_map.return_value = {"some_unknown_key": {""}}
        self.session.client.call_mcp_tool.return_value = mock_response

        with self.assertRaises(FileError) as context:
            self.fs.read_file("/path/to/file.txt")

        self.assertIn("Failed to read file:", str(context.exception))
        self.assertIn("Invalid response body", str(context.exception))

    @patch("agentbay.filesystem.filesystem.CallMcpToolRequest")
    def test_create_directory_success(self, MockCallMcpToolRequest):
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
        self.session.get_client().call_mcp_tool.return_value = mock_response

        result = self.fs.create_directory("/path/to/directory")
        self.assertTrue(result)

    @patch("agentbay.filesystem.filesystem.CallMcpToolRequest")
    def test_create_directory_error(self, MockCallMcpToolRequest):
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
        self.session.get_client().call_mcp_tool.return_value = mock_response

        with self.assertRaises(FileError) as context:
            self.fs.create_directory("/path/to/directory")
        self.assertIn("Error in response: Directory creation failed", str(context.exception))

    @patch("agentbay.filesystem.filesystem.CallMcpToolRequest")
    def test_edit_file_success(self, MockCallMcpToolRequest):
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
        self.session.get_client().call_mcp_tool.return_value = mock_response

        result = self.fs.edit_file("/path/to/file.txt", [{"oldText": "foo", "newText": "bar"}])
        print(f"type(result)= {type(result)}")
        self.assertTrue(result)

    @patch("agentbay.filesystem.filesystem.CallMcpToolRequest")
    def test_edit_file_error(self, MockCallMcpToolRequest):
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
        self.session.get_client().call_mcp_tool.return_value = mock_response

        with self.assertRaises(FileError) as context:
            self.fs.edit_file("/path/to/file.txt", [{"oldText": "foo", "newText": "bar"}])
        self.assertIn("Error in response: Edit failed", str(context.exception))

    @patch("agentbay.filesystem.filesystem.CallMcpToolRequest")
    def test_write_file_success(self, MockCallMcpToolRequest):
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
        self.session.get_client().call_mcp_tool.return_value = mock_response

        result = self.fs.write_file("/path/to/file.txt", "content to write", "overwrite")
        self.assertTrue(result)

    @patch("agentbay.filesystem.filesystem.CallMcpToolRequest")
    def test_write_file_error(self, MockCallMcpToolRequest):
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
        self.session.get_client().call_mcp_tool.return_value = mock_response

        with self.assertRaises(FileError) as context:
            self.fs.write_file("/path/to/file.txt", "content to write", "overwrite")
        self.assertIn("Error in response: Write failed", str(context.exception))

    @patch("agentbay.filesystem.filesystem.CallMcpToolRequest")
    def test_get_file_info_success(self, MockCallMcpToolRequest):
        """
        Test get_file_info method with successful response.
        """
        mock_response = MagicMock()
        mock_response.to_map.return_value = {
            "body": {
                "Data": {
                    "content": [{"text": "size: 36\nisDirectory: false\nisFile: true\npermissions: rw-r--r--"}],
                    "isError": False,
                }
            }
        }
        self.session.get_client().call_mcp_tool.return_value = mock_response

        result = self.fs.get_file_info("/path/to/file.txt")
        self.assertEqual(result["size"], 36)
        self.assertFalse(result["isDirectory"])
        self.assertTrue(result["isFile"])
        self.assertEqual(result["permissions"], "rw-r--r--")

    @patch("agentbay.filesystem.filesystem.CallMcpToolRequest")
    def test_get_file_info_error(self, MockCallMcpToolRequest):
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
        self.session.get_client().call_mcp_tool.return_value = mock_response

        with self.assertRaises(FileError) as context:
            self.fs.get_file_info("/path/to/file.txt")
        self.assertIn("Error in response: File not found", str(context.exception))

    @patch("agentbay.filesystem.filesystem.CallMcpToolRequest")
    def test_list_directory_success(self, MockCallMcpToolRequest):
        """
        Test list_directory method with successful response.
        """
        mock_response = MagicMock()
        mock_response.to_map.return_value = {
            "body": {
                "Data": {
                    "content": [
                        {"text":
                             "[DIR] subdir\n [FILE] file1.txt"
                        }
                    ],
                    "isError": False,
                }
            }
        }
        self.session.get_client().call_mcp_tool.return_value = mock_response

        result = self.fs.list_directory("/path/to/directory")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["name"], "subdir")
        self.assertTrue(result[0]["isDirectory"])
        self.assertEqual(result[1]["name"], "file1.txt")
        self.assertFalse(result[1]["isDirectory"])

    @patch("agentbay.filesystem.filesystem.CallMcpToolRequest")
    def test_list_directory_error(self, MockCallMcpToolRequest):
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
        self.session.get_client().call_mcp_tool.return_value = mock_response

        with self.assertRaises(FileError) as context:
            self.fs.list_directory("/path/to/directory")
        self.assertIn("Error in response: Directory not found", str(context.exception))

    @patch("agentbay.filesystem.filesystem.CallMcpToolRequest")
    def test_move_file_success(self, MockCallMcpToolRequest):
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
        self.session.get_client().call_mcp_tool.return_value = mock_response

        result = self.fs.move_file("/path/to/source.txt", "/path/to/destination.txt")
        self.assertTrue(result)

    @patch("agentbay.filesystem.filesystem.CallMcpToolRequest")
    def test_move_file_error(self, MockCallMcpToolRequest):
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
        self.session.get_client().call_mcp_tool.return_value = mock_response

        with self.assertRaises(FileError) as context:
            self.fs.move_file("/path/to/source.txt", "/path/to/destination.txt")
        self.assertIn("Error in response: Move failed", str(context.exception))

    @patch("agentbay.filesystem.filesystem.CallMcpToolRequest")
    def test_read_multiple_files_success(self, MockCallMcpToolRequest):
        """
        Test read_multiple_files method with successful response.
        """
        mock_response = MagicMock()
        mock_response.to_map.return_value = {
            "body": {
                "Data": {
                    "content": [{
                        "text": "/path/to/file1.txt: Content of file1\n\n---\n/path/to/file2.txt: \nContent of file2\n"
                    }],
                    "isError": False,
                }
            }
        }
        self.session.get_client().call_mcp_tool.return_value = mock_response

        result = self.fs.read_multiple_files(["/path/to/file1.txt", "/path/to/file2.txt"])
        self.assertEqual(result["/path/to/file1.txt"], "Content of file1")
        self.assertEqual(result["/path/to/file2.txt"], "Content of file2")

    @patch("agentbay.filesystem.filesystem.CallMcpToolRequest")
    def test_search_files_success(self, MockCallMcpToolRequest):
        """
        Test search_files method with successful response.
        """
        mock_response = MagicMock()
        mock_response.to_map.return_value = {
            "body": {
                "Data": {
                    "content": [{"text": "/path/to/file1.txt\n/path/to/file2.txt"}],
                    "isError": False,
                }
            }
        }
        self.session.get_client().call_mcp_tool.return_value = mock_response

        result = self.fs.search_files("/path/to/directory", "pattern", ["ignored_pattern"])
        print("Result:", result)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], "/path/to/file1.txt")
        self.assertEqual(result[1], "/path/to/file2.txt")

    @patch("agentbay.filesystem.filesystem.FileSystem.get_file_info")
    @patch("agentbay.filesystem.filesystem.FileSystem.read_file")
    def test_read_large_file_success(self, mock_read_file, mock_get_file_info):
        """
        Test read_large_file method with successful response.
        """
        # Mock get_file_info to return a file size of 150KB
        mock_get_file_info.return_value = {"size": 150 * 1024, "isDirectory": False}

        # Mock read_file to return chunks of content
        mock_read_file.side_effect = [
            "chunk1_content",
            "chunk2_content",
            "chunk3_content"
        ]

        # Set a smaller chunk size for testing (50KB)
        test_chunk_size = 50 * 1024

        result = self.fs.read_large_file("/path/to/large_file.txt", test_chunk_size)

        # Verify the result is the concatenation of all chunks
        self.assertEqual(result, "chunk1_contentchunk2_contentchunk3_content")

        # Verify get_file_info was called once
        mock_get_file_info.assert_called_once_with("/path/to/large_file.txt")

        # Verify read_file was called three times with correct offsets and lengths
        self.assertEqual(mock_read_file.call_count, 3)
        mock_read_file.assert_any_call("/path/to/large_file.txt", 0, test_chunk_size)
        mock_read_file.assert_any_call("/path/to/large_file.txt", test_chunk_size, test_chunk_size)
        mock_read_file.assert_any_call("/path/to/large_file.txt", test_chunk_size * 2, test_chunk_size)

    @patch("agentbay.filesystem.filesystem.FileSystem.get_file_info")
    def test_read_large_file_error(self, mock_get_file_info):
        """
        Test read_large_file method with error response.
        """
        # Mock get_file_info to raise an error
        mock_get_file_info.side_effect = FileError("File not found")

        with self.assertRaises(FileError) as context:
            self.fs.read_large_file("/path/to/nonexistent_file.txt")

        self.assertIn("Failed to read large file", str(context.exception))
        mock_get_file_info.assert_called_once_with("/path/to/nonexistent_file.txt")

    @patch("agentbay.filesystem.filesystem.FileSystem.write_file")
    def test_write_large_file_success(self, mock_write_file):
        """
        Test write_large_file method with successful response.
        """
        # Mock write_file to return True
        mock_write_file.return_value = True

        # Create a large content string (150KB)
        large_content = "x" * (150 * 1024)

        # Set a smaller chunk size for testing (50KB)
        test_chunk_size = 50 * 1024

        result = self.fs.write_large_file("/path/to/large_file.txt", large_content, test_chunk_size)

        # Verify the result is True
        self.assertTrue(result)

        # Verify write_file was called three times with correct chunks
        self.assertEqual(mock_write_file.call_count, 3)
        mock_write_file.assert_any_call("/path/to/large_file.txt", large_content[:test_chunk_size], "overwrite")
        mock_write_file.assert_any_call("/path/to/large_file.txt", large_content[test_chunk_size:test_chunk_size*2], "append")
        mock_write_file.assert_any_call("/path/to/large_file.txt", large_content[test_chunk_size*2:], "append")

    @patch("agentbay.filesystem.filesystem.FileSystem.write_file")
    def test_write_large_file_small_content(self, mock_write_file):
        """
        Test write_large_file method with content smaller than chunk size.
        """
        # Mock write_file to return True
        mock_write_file.return_value = True

        # Create a small content string (10KB)
        small_content = "x" * (10 * 1024)

        # Set a larger chunk size for testing (50KB)
        test_chunk_size = 50 * 1024

        result = self.fs.write_large_file("/path/to/small_file.txt", small_content, test_chunk_size)

        # Verify the result is True
        self.assertTrue(result)

        # Verify write_file was called once with the entire content
        mock_write_file.assert_called_once_with("/path/to/small_file.txt", small_content, "overwrite")

    @patch("agentbay.filesystem.filesystem.FileSystem.write_file")
    def test_write_large_file_error(self, mock_write_file):
        """
        Test write_large_file method with error response.
        """
        # Mock write_file to raise an error
        mock_write_file.side_effect = FileError("Failed to write large file")

        # Create a large content string (150KB)
        large_content = "x" * (150 * 1024)

        with self.assertRaises(FileError) as context:
            self.fs.write_large_file("/path/to/large_file.txt", large_content)

        self.assertIn("Failed to write large file", str(context.exception))
        mock_write_file.assert_called_once()

if __name__ == "__main__":
    unittest.main()