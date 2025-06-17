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
                    "entries": [
                        {"name": "file1.txt", "isDirectory": False},
                        {"name": "subdir", "isDirectory": True},
                    ],
                    "isError": False,
                }
            }
        }
        self.session.get_client().call_mcp_tool.return_value = mock_response

        result = self.fs.list_directory("/path/to/directory")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["name"], "file1.txt")
        self.assertFalse(result[0]["isDirectory"])
        self.assertEqual(result[1]["name"], "subdir")
        self.assertTrue(result[1]["isDirectory"])

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
                    "files": {
                        "/path/to/file1.txt": "Content of file1",
                        "/path/to/file2.txt": "Content of file2",
                    },
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
                    "results": [
                        {"path": "/path/to/file1.txt"},
                        {"path": "/path/to/file2.txt"},
                    ],
                    "isError": False,
                }
            }
        }
        self.session.get_client().call_mcp_tool.return_value = mock_response

        result = self.fs.search_files("/path/to/directory", "pattern", ["ignored_pattern"])
        print("Result:", result)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["path"], "/path/to/file1.txt")
        self.assertEqual(result[1]["path"], "/path/to/file2.txt")

if __name__ == "__main__":
    unittest.main()