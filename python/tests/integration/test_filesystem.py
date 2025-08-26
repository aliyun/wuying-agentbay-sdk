import os
import unittest
import time
import concurrent.futures

from agentbay import AgentBay
from agentbay.filesystem.filesystem import (
    BoolResult,
    DirectoryListResult,
    FileContentResult,
    FileInfoResult,
    FileSearchResult,
    MultipleFileContentResult,
)
from agentbay.session_params import CreateSessionParams

class TestFileSystemComprehensive(unittest.TestCase):
    """
    FileSystem Comprehensive Tests

    This test suite covers comprehensive file system operations including:
    1. File Basic Operations
    2. File Information Management
    3. Batch File Operations
    4. File Edit and Move Operations
    5. Directory Management
    """

    @classmethod
    def setUpClass(cls):
        """Set up test environment before all tests."""
        # Get API key from environment
        cls.api_key = os.getenv("AGENTBAY_API_KEY")
        if not cls.api_key:
            raise unittest.SkipTest("AGENTBAY_API_KEY environment variable not set")

        # Initialize AgentBay client
        cls.agent_bay = AgentBay(cls.api_key)

        # Create a session
        print("Creating a new session for FileSystem comprehensive testing...")
        params = CreateSessionParams(
            image_id="linux_latest",
        )
        result = cls.agent_bay.create(params)
        if not result.success or not result.session:
            raise unittest.SkipTest("Failed to create session")

        cls.session = result.session
        cls.fs = cls.session.file_system
        print(f"Session created with ID: {cls.session.session_id}")

        # Create base tmp directory
        cls.fs.create_directory("/tmp")

    @classmethod
    def tearDownClass(cls):
        """Clean up test environment after all tests."""
        print("Cleaning up: Deleting the session...")
        if hasattr(cls, "session"):
            try:
                result = cls.agent_bay.delete(cls.session)
                if result.success:
                    print("Session successfully deleted")
                else:
                    print(f"Warning: Error deleting session: {result.error_message}")
            except Exception as e:
                print(f"Warning: Error deleting session: {e}")

    def setUp(self):
        """Set up before each test."""
        # Test constants
        self.test_file_path = "/tmp/test_files.txt"
        self.multiline_file_path = "/tmp/test_multiline.txt"

        # Create 30KB test file with repeated content
        test_content = "hello world!!!\n" * 2000
        write_result = self.fs.write_file(self.test_file_path, test_content, "overwrite")
        self.assertTrue(write_result.success, "Failed to create test file")

    # 1. File Basic Operations Tests
    def test_1_1_file_reading_tests(self):
        """1.1 File Reading Tests - should successfully read file content"""
        result = self.fs.read_file(self.test_file_path)

        self.assertIsInstance(result, FileContentResult)
        self.assertTrue(result.success)
        self.assertIsNotNone(result.request_id)
        self.assertNotEqual(result.request_id, "")
        self.assertIsNotNone(result.content)
        self.assertIn("hello world!!!", result.content)
        self.assertEqual(len(result.content), 30000)

    def test_1_1_file_content_pattern(self):
        """1.1 File Reading Tests - should return correct file content pattern"""
        result = self.fs.read_file(self.test_file_path)

        self.assertTrue(result.success)
        lines = result.content.split('\n')
        for line in lines:
            if line.strip() != "":
                self.assertEqual(line, "hello world!!!")

    def test_1_2_parameterized_file_reading_with_offset_length(self):
        """1.2 Parameterized File Reading Tests - should read specific bytes with offset and length parameters"""
        # Create multi-line test file
        multiline_content = "\n".join([f"Line {i + 1}: This is test content" for i in range(10)])
        write_result = self.fs.write_file(self.multiline_file_path, multiline_content, "overwrite")
        self.assertTrue(write_result.success)

        # Read from 3rd byte, 3 bytes (offset=2, length=3)
        result = self.fs.read_file(self.multiline_file_path, 2, 3)

        self.assertTrue(result.success)
        self.assertIsNotNone(result.request_id)
        self.assertIsNotNone(result.content)
        self.assertLessEqual(len(result.content), 3)

        # Verify content is from 3rd byte
        full_content = self.fs.read_file(self.multiline_file_path)
        expected_content = full_content.content[2:5]  # bytes 2-4 (3 bytes)
        self.assertEqual(result.content, expected_content)

    def test_1_2_read_from_offset_to_end(self):
        """1.2 Parameterized File Reading Tests - should read from offset to end of file"""
        multiline_content = "\n".join([f"Line {i + 1}: This is test content" for i in range(10)])
        write_result = self.fs.write_file(self.multiline_file_path, multiline_content, "overwrite")
        self.assertTrue(write_result.success)

        # Read from 6th byte to end (offset=5, length=0)
        result = self.fs.read_file(self.multiline_file_path, 5, 0)

        self.assertTrue(result.success)
        self.assertIsNotNone(result.request_id)
        self.assertIsNotNone(result.content)

        # Verify reads from 6th byte to end
        full_content = self.fs.read_file(self.multiline_file_path)
        expected_content = full_content.content[5:]  # from 6th byte to end
        self.assertEqual(result.content, expected_content)

    def test_1_2_handle_large_offset_values(self):
        """1.2 Parameterized File Reading Tests - should handle large offset values correctly"""
        multiline_content = "\n".join([f"Line {i + 1}: This is test content" for i in range(10)])
        write_result = self.fs.write_file(self.multiline_file_path, multiline_content, "overwrite")
        self.assertTrue(write_result.success)

        # Test offset greater than file size
        result = self.fs.read_file(self.multiline_file_path, 1000)

        self.assertTrue(result.success)
        self.assertIsNotNone(result.content)
        # Should return empty content since offset exceeds file size

    def test_1_2_handle_zero_length_parameter(self):
        """1.2 Parameterized File Reading Tests - should handle zero length parameter correctly"""
        multiline_content = "\n".join([f"Line {i + 1}: This is test content" for i in range(10)])
        write_result = self.fs.write_file(self.multiline_file_path, multiline_content, "overwrite")
        self.assertTrue(write_result.success)

        # Test length=0 should read from offset to end
        result = self.fs.read_file(self.multiline_file_path, 0, 0)

        self.assertTrue(result.success)
        self.assertIsNotNone(result.content)

        # length=0 should read entire file
        full_content = self.fs.read_file(self.multiline_file_path)
        self.assertEqual(result.content, full_content.content)

    def test_1_3_write_file_with_different_modes(self):
        """1.3 File Writing Tests - should write file with different modes"""
        write_test_file_path = "/tmp/test_write.txt"
        test_content = "Hello, World!"

        # Test overwrite mode
        write_result = self.fs.write_file(write_test_file_path, test_content, "overwrite")
        self.assertTrue(write_result.success)
        self.assertIsNotNone(write_result.request_id)
        self.assertTrue(write_result.data)

        # Verify content
        read_result = self.fs.read_file(write_test_file_path)
        self.assertTrue(read_result.success)
        self.assertEqual(read_result.content, test_content)

        # Test append mode
        append_result = self.fs.write_file(write_test_file_path, "\nAppended content", "append")
        self.assertTrue(append_result.success)

        read_result2 = self.fs.read_file(write_test_file_path)
        self.assertIn(test_content, read_result2.content)
        self.assertIn("Appended content", read_result2.content)

    def test_1_3_validate_write_mode_parameter(self):
        """1.3 File Writing Tests - should validate write mode parameter"""
        write_test_file_path = "/tmp/test_write.txt"
        result = self.fs.write_file(write_test_file_path, "content", "invalid_mode")
        print(f"Write result: {result.__dict__}")
        self.assertFalse(result.success)
        self.assertIn("Invalid", result.error_message)

    def test_1_4_handle_large_file_operations(self):
        """1.4 Large File Tests - should handle large file operations"""
        large_content = "Large content line. " * 3000
        large_file_path = "/tmp/large_test.txt"

        # Write large file
        write_result = self.fs.write_large_file(large_file_path, large_content)
        self.assertTrue(write_result.success)

        # Read large file
        read_result = self.fs.read_large_file(large_file_path)
        self.assertTrue(read_result.success)
        self.assertEqual(read_result.content, large_content)

    # 2. File Information Management Tests
    def test_2_get_file_info_correctly(self):
        """2. File Information Management - should get file info correctly"""
        info_test_file = "/tmp/info_test.txt"
        write_result = self.fs.write_file(info_test_file, "", "overwrite")
        self.assertTrue(write_result.success)

        result = self.fs.get_file_info(info_test_file)
        print(f"File info result: {result.__dict__}")
        self.assertIsInstance(result, FileInfoResult)
        self.assertTrue(result.success)
        self.assertEqual(result.file_info.get("size"), 0)
        self.assertFalse(result.file_info.get("isDirectory"))

    def test_2_list_directory_contents(self):
        """2. File Information Management - should list directory contents"""
        list_test_dir = "/tmp/list_test"
        self.fs.create_directory(list_test_dir)
        self.fs.write_file(f"{list_test_dir}/file1.txt", "content1", "overwrite")
        self.fs.create_directory(f"{list_test_dir}/subdir1")

        result = self.fs.list_directory(list_test_dir)
        self.assertIsInstance(result, DirectoryListResult)
        self.assertTrue(result.success)
        self.assertGreater(len(result.entries), 0)

    # 3. Batch File Operations Tests
    def test_3_read_multiple_files_correctly(self):
        """3. Batch File Operations - should read multiple files correctly"""
        files = ["/tmp/batch1.txt", "/tmp/batch2.txt", "/tmp/batch3.txt"]
        contents = ["Content 1", "", "Content 3"]

        # Create multiple files
        for i, file_path in enumerate(files):
            self.fs.write_file(file_path, contents[i], "overwrite")

        result = self.fs.read_multiple_files(files)
        self.assertIsInstance(result, MultipleFileContentResult)
        self.assertTrue(result.success)
        self.assertEqual(result.contents[files[0]], contents[0])
        self.assertEqual(result.contents[files[1]], contents[1])
        self.assertEqual(result.contents[files[2]], contents[2])

    def test_3_search_files_correctly(self):
        """3. Batch File Operations - should search files correctly"""
        search_test_dir = "/tmp/search_test"
        self.fs.create_directory(search_test_dir)
        self.fs.write_file(f"{search_test_dir}/test1.txt", "content", "overwrite")
        self.fs.write_file(f"{search_test_dir}/test2.log", "log", "overwrite")

        result1 = self.fs.search_files(search_test_dir, "test1.txt")
        self.assertTrue(result1.success)
        self.assertIsNotNone(result1.matches)

        result2 = self.fs.search_files(search_test_dir, "", ["test2.log"])
        self.assertTrue(result2.success)
        self.assertIsNotNone(result2.matches)

    # 4. File Edit and Move Operations Tests
    def test_4_edit_file_with_find_replace(self):
        """4. File Edit and Move Operations - should edit file with find-replace"""
        edit_path = "/tmp/edit_test.txt"
        initial_content = "This is old1 text with old2 content."
        self.fs.write_file(edit_path, initial_content, "overwrite")

        edits = [
            {"oldText": "old1", "newText": "new1"},
            {"oldText": "old2", "newText": "new2"}
        ]

        result = self.fs.edit_file(edit_path, edits, False)
        self.assertIsInstance(result, BoolResult)
        self.assertTrue(result.success)

        read_result = self.fs.read_file(edit_path)
        self.assertIn("new1", read_result.content)
        self.assertIn("new2", read_result.content)

    def test_4_move_file_correctly(self):
        """4. File Edit and Move Operations - should move file correctly"""
        source_path = "/tmp/move_source.txt"
        dest_path = "/tmp/move_dest.txt"
        content_to_move = "Content to move"

        self.fs.write_file(source_path, content_to_move, "overwrite")

        result = self.fs.move_file(source_path, dest_path)
        self.assertIsInstance(result, BoolResult)
        self.assertTrue(result.success)

        read_result = self.fs.read_file(dest_path)
        self.assertTrue(read_result.success)
        self.assertEqual(read_result.content, content_to_move)

    # 5. Directory Management Tests
    def test_5_create_directory_successfully(self):
        """5. Directory Management - should create directory successfully"""
        dir_path = "/tmp/new_directory"

        result = self.fs.create_directory(dir_path)
        self.assertIsInstance(result, BoolResult)
        self.assertTrue(result.success)

        info_result = self.fs.get_file_info(dir_path)
        self.assertTrue(info_result.success)
        self.assertTrue(info_result.file_info.get("isDirectory"))

    def test_5_create_nested_directories(self):
        """5. Directory Management - should create nested directories"""
        nested_path = "/tmp/level1/level2/level3"

        self.fs.create_directory("/tmp/level1")
        self.fs.create_directory("/tmp/level1/level2")
        result = self.fs.create_directory(nested_path)

        self.assertTrue(result.success)
