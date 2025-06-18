import unittest
import os
import time
from agentbay import AgentBay
from agentbay.filesystem.filesystem import FileSystem
from agentbay.session_params import CreateSessionParams
from agentbay.exceptions import FileError

class TestFileSystemIntegration(unittest.TestCase):
    def setUp(self):
        """
        Set up the test environment by creating a session and initializing FileSystem.
        """
        time.sleep(3)  # Ensure a delay to avoid session creation conflicts
        api_key = os.getenv("AGENTBAY_API_KEY")
        if not api_key:
            api_key = "akm-xxx"  # Replace with your actual API key for testing
            print("Warning: Using default API key. Set AGENTBAY_API_KEY environment variable for production use.")
        self.agent_bay = AgentBay(api_key=api_key) # Replace DummySession with actual session implementation
        params = CreateSessionParams(
            image_id="linux_latest",
        )
        self.session = self.agent_bay.create(params)
        self.fs = FileSystem(self.session)

    def tearDown(self):
        """Tear down test fixtures."""
        print("Cleaning up: Deleting the session...")
        try:
            self.agent_bay.delete(self.session)
        except Exception as e:
            print(f"Warning: Error deleting session: {e}")

    def test_read_file(self):
        """
        Test reading a file.
        """
        test_content = "This is a test file content for ReadFile test."
        test_file_path = "/tmp/test_read.txt"

        # Write the test file
        self.fs.write_file(test_file_path, test_content, "overwrite")

        # Read the file
        content = self.fs.read_file(test_file_path)
        self.assertEqual(content, test_content)

    def test_write_file(self):
        """
        Test writing to a file.
        """
        test_content = "This is a test file content for WriteFile test."
        test_file_path = "/tmp/test_write.txt"

        # Write the file
        success = self.fs.write_file(test_file_path, test_content, "overwrite")
        self.assertTrue(success)

        # Verify the file content
        content = self.fs.read_file(test_file_path)
        self.assertEqual(content, test_content)

    def test_create_directory(self):
        """
        Test creating a directory.
        """
        test_dir_path = "/tmp/test_directory"

        # Create the directory
        success = self.fs.create_directory(test_dir_path)
        self.assertTrue(success)

        # Verify the directory exists
        entries = self.fs.list_directory("/tmp/")
        directory_names = [entry["name"] for entry in entries]
        self.assertIn("test_directory", directory_names)

    def test_edit_file(self):
        """
        Test editing a file.
        """
        initial_content = "This is the original content.\nLine to be replaced.\nThis is the final line."
        test_file_path = "/tmp/test_edit.txt"

        # Write the initial file
        self.fs.write_file(test_file_path, initial_content, "overwrite")

        # Edit the file
        edits = [{"oldText": "Line to be replaced.", "newText": "This line has been edited."}]
        result = self.fs.edit_file(test_file_path, edits, False)
        self.assertTrue(result)

        # Verify the file content
        expected_content = "This is the original content.\nThis line has been edited.\nThis is the final line."
        content = self.fs.read_file(test_file_path)
        self.assertEqual(content, expected_content)

    def test_get_file_info(self):
        """
        Test getting file information.
        """
        test_content = "This is a test file for GetFileInfo."
        test_file_path = "/tmp/test_info.txt"

        # Write the test file
        self.fs.write_file(test_file_path, test_content, "overwrite")

        # Get file info
        file_info = self.fs.get_file_info(test_file_path)
        self.assertEqual(file_info["isDirectory"], False)
        self.assertGreater(file_info["size"], 0)
        self.assertFalse(file_info["isDirectory"])

    def test_list_directory(self):
        """
        Test listing a directory.
        """
        entries = self.fs.list_directory("/tmp/")
        self.assertGreater(len(entries), 0)
        self.assertIn("name", entries[0])
        self.assertIn("isDirectory", entries[0])

    def test_move_file(self):
        """
        Test moving a file.
        """
        test_content = "This is a test file for MoveFile."
        source_file_path = "/tmp/test_source.txt"
        dest_file_path = "/tmp/test_destination.txt"

        # Write the source file
        self.fs.write_file(source_file_path, test_content, "overwrite")

        # Move the file
        success = self.fs.move_file(source_file_path, dest_file_path)
        self.assertTrue(success)

        # Verify the destination file content
        content = self.fs.read_file(dest_file_path)
        self.assertEqual(content, test_content)

        # Verify the source file no longer exists
        with self.assertRaises(FileError):
            self.fs.get_file_info(source_file_path)

    def test_read_multiple_files(self):
        """
        Test reading multiple files.
        """
        file1_content = "This is test file 1 content."
        file2_content = "This is test file 2 content."
        test_file1_path = "/tmp/test_file1.txt"
        test_file2_path = "/tmp/test_file2.txt"

        # Write the test files
        self.fs.write_file(test_file1_path, file1_content, "overwrite")
        self.fs.write_file(test_file2_path, file2_content, "overwrite")

        # Read multiple files
        contents = self.fs.read_multiple_files([test_file1_path, test_file2_path])
        self.assertEqual(contents[test_file1_path], file1_content)
        self.assertEqual(contents[test_file2_path], file2_content)

    def test_search_files(self):
        """
        Test searching for files.
        """
        test_subdir_path = "/tmp/search_test_dir"
        self.fs.create_directory(test_subdir_path)

        file1_content = "This is test file 1 content."
        file2_content = "This is test file 2 content."
        file3_content = "This is test file 3 content."
        search_file1_path = f"{test_subdir_path}/SEARCHABLE_PATTERN_file1.txt"
        search_file2_path = f"{test_subdir_path}/regular_file2.txt"
        search_file3_path = f"{test_subdir_path}/SEARCHABLE_PATTERN_file3.txt"

        # Write the test files
        self.fs.write_file(search_file1_path, file1_content, "overwrite")
        self.fs.write_file(search_file2_path, file2_content, "overwrite")
        self.fs.write_file(search_file3_path, file3_content, "overwrite")

        # Search for files
        search_pattern = "SEARCHABLE_PATTERN"
        exclude_patterns = ["ignored_pattern"]
        results = self.fs.search_files(test_subdir_path, search_pattern, exclude_patterns)
        self.assertEqual(len(results), 2)
        self.assertIn(search_file1_path, results)
        self.assertIn(search_file3_path, results)


if __name__ == "__main__":
    unittest.main()