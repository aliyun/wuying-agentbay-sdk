#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Example demonstrating FileSystem operations with AgentBay SDK.
This example shows how to use various file system operations including:
- Basic file reading and writing
- Directory operations
- File information retrieval
- File editing
- File searching
- Multiple file reading
- Large file operations with chunking
"""

import os
import time
from agentbay import AgentBay
from agentbay.session_params import CreateSessionParams
from agentbay.filesystem.filesystem import FileSystem

def main():
    # Get API key from environment variable
    api_key = os.getenv("AGENTBAY_API_KEY")
    if not api_key:
        print("Error: AGENTBAY_API_KEY environment variable not set")
        return

    # Initialize AgentBay client
    print("Initializing AgentBay client...")
    agent_bay = AgentBay(api_key=api_key)

    # Create a session
    print("Creating a new session...")
    params = CreateSessionParams(
        image_id="linux_latest",  # Specify the image ID
    )
    session = agent_bay.create(params)
    print(f"Session created with ID: {session.get_session_id()}")

    try:
        # Get the FileSystem interface
        fs = FileSystem(session)

        # ===== BASIC FILE OPERATIONS =====
        print("\n===== BASIC FILE OPERATIONS =====")

        # Example 1: Write a simple file
        print("\nExample 1: Writing a simple file...")
        test_content = "This is a test file content.\nIt has multiple lines.\nThis is the third line."
        test_file_path = "/tmp/test_file.txt"

        success = fs.write_file(test_file_path, test_content, "overwrite")
        print(f"File write successful: {success}")

        # Example 2: Read the file
        print("\nExample 2: Reading the file...")
        content = fs.read_file(test_file_path)
        print(f"File content ({len(content)} bytes):")
        print(content)
        print(f"Content matches original: {content == test_content}")

        # Example 3: Append to the file
        print("\nExample 3: Appending to the file...")
        append_content = "\nThis is an appended line."
        success = fs.write_file(test_file_path, append_content, "append")
        print(f"File append successful: {success}")

        # Read the file again to verify append
        updated_content = fs.read_file(test_file_path)
        print(f"Updated file content ({len(updated_content)} bytes):")
        print(updated_content)
        print(f"Content matches expected: {updated_content == test_content + append_content}")

        # ===== DIRECTORY OPERATIONS =====
        print("\n===== DIRECTORY OPERATIONS =====")

        # Example 4: Create a directory
        print("\nExample 4: Creating a directory...")
        test_dir_path = "/tmp/test_directory"
        success = fs.create_directory(test_dir_path)
        print(f"Directory creation successful: {success}")

        # Example 5: List directory contents
        print("\nExample 5: Listing directory contents...")
        entries = fs.list_directory("/tmp")
        print(f"Found {len(entries)} entries in /tmp:")
        for entry in entries:
            entry_type = "Directory" if entry["isDirectory"] else "File"
            print(f"  - {entry['name']} ({entry_type})")

        # ===== FILE INFORMATION =====
        print("\n===== FILE INFORMATION =====")

        # Example 6: Get file information
        print("\nExample 6: Getting file information...")
        file_info = fs.get_file_info(test_file_path)
        print(f"File information for {test_file_path}:")
        for key, value in file_info.items():
            print(f"  - {key}: {value}")

        # ===== FILE EDITING =====
        print("\n===== FILE EDITING =====")

        # Example 7: Edit a file
        print("\nExample 7: Editing a file...")
        edits = [
            {"oldText": "This is the third line.", "newText": "This line has been edited."}
        ]
        success = fs.edit_file(test_file_path, edits)
        print(f"File edit successful: {success}")

        # Read the file again to verify edit
        edited_content = fs.read_file(test_file_path)
        print(f"Edited file content ({len(edited_content)} bytes):")
        print(edited_content)

        # ===== FILE MOVING =====
        print("\n===== FILE MOVING =====")

        # Example 8: Move a file
        print("\nExample 8: Moving a file...")
        source_path = "/tmp/test_file.txt"
        dest_path = "/tmp/test_directory/moved_file.txt"
        success = fs.move_file(source_path, dest_path)
        print(f"File move successful: {success}")

        # Verify the file was moved
        moved_content = fs.read_file(dest_path)
        print(f"Moved file content length: {len(moved_content)} bytes")
        print(f"Content preserved after move: {moved_content == edited_content}")

        # ===== FILE SEARCHING =====
        print("\n===== FILE SEARCHING =====")

        # Create some files for searching
        fs.write_file("/tmp/test_directory/file1.txt", "This file contains the word SEARCHABLE", "overwrite")
        fs.write_file("/tmp/test_directory/file2.txt", "This file does not contain the keyword", "overwrite")
        fs.write_file("/tmp/test_directory/file3.txt", "This file also contains SEARCHABLE term", "overwrite")

        # Example 9: Search for files
        print("\nExample 9: Searching for files...")
        search_results = fs.search_files("/tmp/test_directory", "SEARCHABLE")
        print(f"Found {len(search_results)} files matching the search pattern:")
        for result in search_results:
            print(f"  - {result}")

        # ===== MULTIPLE FILE READING =====
        print("\n===== MULTIPLE FILE READING =====")

        # Example 10: Read multiple files
        print("\nExample 10: Reading multiple files...")
        file_paths = [
            "/tmp/test_directory/file1.txt",
            "/tmp/test_directory/file2.txt",
            "/tmp/test_directory/file3.txt"
        ]
        multi_file_contents = fs.read_multiple_files(file_paths)
        print(f"Read {len(multi_file_contents)} files:")
        for path, content in multi_file_contents.items():
            print(f"  - {path}: {len(content)} bytes")
            print(f"    Content: {content}")

        # ===== LARGE FILE OPERATIONS =====
        print("\n===== LARGE FILE OPERATIONS =====")

        # Example 11: Write a large file with default chunk size
        print("\nExample 11: Writing a large file with default chunk size...")

        # Generate approximately 1MB of test content
        line_content = "This is a line of test content for large file testing. " * 20
        large_content = line_content * 500  # About 1MB
        test_file_path = "/tmp/large_file_default.txt"

        print(f"Generated test content size: {len(large_content)} bytes")

        # Write the large file
        start_time = time.time()
        success = fs.write_large_file(test_file_path, large_content)
        write_time = time.time() - start_time

        print(f"Write operation completed in {write_time:.2f} seconds")
        print(f"Success: {success}")

        # Example 12: Read the large file with default chunk size
        print("\nExample 12: Reading the large file with default chunk size...")

        start_time = time.time()
        read_content = fs.read_large_file(test_file_path)
        read_time = time.time() - start_time

        print(f"Read operation completed in {read_time:.2f} seconds")
        print(f"Content length: {len(read_content)} bytes")
        print(f"Content matches original: {read_content == large_content}")

        # Example 13: Write a large file with custom chunk size
        print("\nExample 13: Writing a large file with custom chunk size (100KB)...")

        custom_chunk_size = 50 * 1024  # 50KB
        test_file_path2 = "/tmp/large_file_custom.txt"

        start_time = time.time()
        success = fs.write_large_file(test_file_path2, large_content, custom_chunk_size)
        write_time = time.time() - start_time

        print(f"Write operation with custom chunk size completed in {write_time:.2f} seconds")
        print(f"Success: {success}")

        # Example 14: Read the large file with custom chunk size
        print("\nExample 14: Reading the large file with custom chunk size (80KB)...")

        read_chunk_size = 80 * 1024  # 80KB
        start_time = time.time()
        read_content2 = fs.read_large_file(test_file_path2, read_chunk_size)
        read_time = time.time() - start_time

        print(f"Read operation with custom chunk size completed in {read_time:.2f} seconds")
        print(f"Content length: {len(read_content2)} bytes")
        print(f"Content matches original: {read_content2 == large_content}")

    finally:
        # Clean up: Delete the session
        print("\nCleaning up: Deleting the session...")
        agent_bay.delete(session)
        print("Session deleted successfully")

if __name__ == "__main__":
    main()