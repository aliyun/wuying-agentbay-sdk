import json
import re
from typing import List, Dict, Union, Any, Optional, Tuple

from agentbay.api.models import CallMcpToolRequest
from agentbay.exceptions import FileError


class FileSystem:
    """
    Handles file operations in the AgentBay cloud environment.
    """

    # Default chunk size is 60KB
    DEFAULT_CHUNK_SIZE = 60 * 1024

    def __init__(self, session):
        """
        Initialize a FileSystem object.

        Args:
            session: The Session instance that this FileSystem belongs to.
        """
        self.session = session

    def _call_mcp_tool(self, name: str, args: Dict[str, Any]) -> Any:
        """
        Internal helper to call MCP tool and handle errors.

        Args:
            name (str): The name of the tool to call.
            args (Dict[str, Any]): The arguments to pass to the tool.

        Returns:
            Any: The response from the tool.

        Raises:
            FileError: If the tool call fails.
        """
        try:
            args_json = json.dumps(args, ensure_ascii=False)
            request = CallMcpToolRequest(
                authorization=f"Bearer {self.session.get_api_key()}",
                session_id=self.session.get_session_id(),
                name=name,
                args=args_json,
            )
            response = self.session.get_client().call_mcp_tool(request)
            response_map = response.to_map()
            if not response_map:
                raise FileError("Invalid response format")
            body = response_map.get("body", {})
            print("response_map =", body)
            if not body:
                raise FileError("Invalid response body")
            return self._parse_response_body(body)
        except (KeyError, TypeError, ValueError) as e:
            raise FileError(f"Failed to parse MCP tool response: {e}")
        except Exception as e:
            raise FileError(f"Failed to call MCP tool {name}: {e}")

    def _parse_response_body(self, body: Dict[str, Any]) -> Any:
        """
        Parses the response body from the MCP tool.

        Args:
            body (Dict[str, Any]): The response body.

        Returns:
            Any: The parsed content.

        Raises:
            FileError: If the response contains errors or is invalid.
        """
        try:
            if body.get("Data", {}).get("isError", False):
                error_content = body.get("Data", {}).get("content", [])
                print("error_content =", error_content)
                error_message = "; ".join(
                    item.get("text", "Unknown error")
                    for item in error_content
                    if isinstance(item, dict)
                )
                raise FileError(f"Error in response: {error_message}")

            response_data = body.get("Data", {})
            if not response_data:
                raise FileError("No data field in response")

            # Handle 'content' field for other methods
            content = response_data.get("content", [])
            if not content or not isinstance(content, list):
                raise FileError("No content found in response")

            content_item = content[0]
            json_text = content_item.get("text")
            return json_text
        except Exception as e:
            raise FileError(f"{e}")
    def create_directory(self, path: str) -> bool:
        """
        Create a new directory at the specified path.

        Args:
            path: The path of the directory to create.

        Returns:
            bool: True if the directory was created successfully.

        Raises:
            FileError: If the operation fails.
        """
        args = {"path": path}
        try:
            response = self._call_mcp_tool("create_directory", args)
            print("Response from CallMcpTool - create_directory:", response)
            # If "isError" in the response is False, it would raise an exception when _parse_response_body
            return True
        except FileError:
            raise
        except Exception as e:
            raise FileError(f"Failed to create directory: {e}")

    def edit_file(self, path: str, edits: List[Dict[str, str]], dry_run: bool = False) -> bool:
        """
        Edit a file by replacing occurrences of oldText with newText.

        Args:
            path: The path of the file to edit.
            edits: A list of dictionaries specifying oldText and newText.
            dry_run: If True, preview changes without applying them.

        Returns:
            bool: True if the file was edited successfully.

        Raises:
            FileError: If the operation fails.
        """
        args = {"path": path, "edits": edits, "dryRun": dry_run}
        try:
            response = self._call_mcp_tool("edit_file", args)
            print("Response from CallMcpTool - edit_file:", response)
            # If "isError" in the response is False, it would raise an exception when _parse_response_body
            return True
        except FileError:
            raise
        except Exception as e:
            raise FileError(f"Failed to edit file: {e}")

    def get_file_info(self, path: str) -> Dict[str, Union[str, float, bool]]:
        """
        Get information about a file or directory.

        Args:
            path: The path of the file or directory to inspect.

        Returns:
            Dict[str, Union[str, float, bool]]: A dictionary containing file information.

        Raises:
            FileError: If the operation fails.
        """
        def parse_file_info(file_info_str: str) -> dict:
            """
            Parse a file info string into a dictionary.

            Args:
                file_info_str (str): The file info string to parse.

            Returns:
                dict: A dictionary containing the parsed file info.
            """
            result = {}
            lines = file_info_str.split("\n")
            for line in lines:
                if ":" in line:
                    key, value = line.split(":", 1)
                    key = key.strip()
                    value = value.strip()

                    # Convert boolean values
                    if value.lower() == "true":
                        value = True
                    elif value.lower() == "false":
                        value = False

                    # Convert numeric values
                    try:
                        if isinstance(value, str):
                            value = float(value) if "." in value else int(value)
                    except ValueError:
                        pass

                    result[key] = value
            return result

        args = {"path": path}
        try:
            response = self._call_mcp_tool("get_file_info", args)
            print("Response from CallMcpTool - get_file_info:", response)
            return parse_file_info(response)
        except FileError:
            raise
        except Exception as e:
            raise FileError(f"Failed to get file info: {e}")

    def list_directory(self, path: str) -> List[Dict[str, Union[str, bool]]]:
        """
        List the contents of a directory.

        Args:
            path: The path of the directory to list.

        Returns:
            List[Dict[str, Union[str, bool]]]: A list of dictionaries representing directory entries.

        Raises:
            FileError: If the operation fails.
        """

        def parse_directory_listing(text) -> List[Dict[str, Union[str, bool]]]:
            '''Parse directory listing text into a list of dictionaries containing file/directory information.

            Args:
                text (str): Directory listing text in format:
                    [DIR] directory_name
                    [FILE] file_name
                    Each entry should be on a new line with [DIR] or [FILE] prefix

            Returns:
                list: List of dictionaries, each containing:
                    - name (str): Name of the file or directory
                    - isDirectory (bool): True if entry is a directory, False if file

            Example:
                Input text:
                    [DIR] folder1
                    [FILE] test.txt

                Returns:
                    [
                        {"name": "folder1", "isDirectory": True},
                        {"name": "test.txt", "isDirectory": False}
                    ]
                '''
            result = []
            lines = text.split('\n')

            for line in lines:
                line = line.strip()
                if line == "":
                    continue

                entry_map = {}
                if line.startswith("[DIR]"):
                    entry_map["isDirectory"] = True
                    entry_map["name"] = line.replace("[DIR]", "").strip()
                elif line.startswith("[FILE]"):
                    entry_map["isDirectory"] = False
                    entry_map["name"] = line.replace("[FILE]", "").strip()
                else:
                    # Skip lines that don't match the expected format
                    continue

                result.append(entry_map)

            return result


        args = {"path": path}
        try:
            response = self._call_mcp_tool("list_directory", args)
            print("Response from CallMcpTool - list_directory:", response)
            return parse_directory_listing(response)
        except FileError:
            raise
        except Exception as e:
            raise FileError(f"Failed to list directory: {e}")

    def move_file(self, source: str, destination: str) -> bool:
        """
        Move a file or directory from source to destination.

        Args:
            source: The source path.
            destination: The destination path.

        Returns:
            bool: True if the file was moved successfully.

        Raises:
            FileError: If the operation fails.
        """
        args = {"source": source, "destination": destination}
        try:
            response = self._call_mcp_tool("move_file", args)
            print("Response from CallMcpTool - move_file:", response)
            # If "isError" in the response is False, it would raise an exception when _parse_response_body
            return True
        except FileError:
            raise
        except Exception as e:
            raise FileError(f"Failed to move file: {e}")

    def read_file(self, path: str, offset: int = 0, length: int = 0) -> str:
        """
        Read the contents of a file.

        Args:
            path: The path of the file to read.
            offset: Start reading from this byte offset.
            length: Number of bytes to read. If 0, read to the end of the file.

        Returns:
            str: The contents of the file.

        Raises:
            FileError: If the operation fails.
        """
        args = {"path": path}

        if offset > 0:
            args["offset"] = str(offset)
        if length > 0:
            args["length"] = str(length)

        try:
            response = self._call_mcp_tool("read_file", args)
            print("Response from CallMcpTool - read_file:", response)
            return response

        except Exception as e:
            raise FileError(f"Failed to read file: {e}")

    def read_multiple_files(self, paths: List[str]) -> Dict[str, str]:
        """
        Read the contents of multiple files.

        Args:
            paths: A list of file paths to read.

        Returns:
            Dict[str, str]: A dictionary mapping file paths to their contents.

        Raises:
            FileError: If the operation fails.
        """
        def parse_multiple_files_response(text: str) -> Dict[str, str]:
            """
            Parse the response from reading multiple files into a dictionary.

            Args:
                text (str): The response string containing file contents.
                Format: "/path/to/file1.txt: Content of file1\n\n---\n/path/to/file2.txt: \nContent of file2\n"

            Returns:
                Dict[str, str]: A dictionary mapping file paths to their contents.
            """
            result = {}
            lines = text.split('\n')
            current_path = None
            current_content = []

            for i, line in enumerate(lines):
                # Check if this line contains a file path (ends with a colon)
                if ':' in line and not current_path:
                    # Extract path (everything before the first colon)
                    path_end = line.find(':')
                    path = line[:path_end].strip()

                    # Start collecting content (everything after the colon)
                    current_path = path

                    # If there's content on the same line after the colon, add it
                    if len(line) > path_end + 1:
                        content_start = line[path_end + 1:].strip()
                        if content_start:
                            current_content.append(content_start)

                # Check if this is a separator line
                elif line.strip() == '---':
                    # Save the current file content
                    if current_path:
                        result[current_path] = '\n'.join(current_content).strip()
                        current_path = None
                        current_content = []

                # If we're collecting content for a path, add this line
                elif current_path is not None:
                    current_content.append(line)

            # Save the last file content if exists
            if current_path:
                result[current_path] = '\n'.join(current_content).strip()

            return result

        # call the MCP tool to read multiple files
        args = {"paths": paths}
        try:
            response = self._call_mcp_tool("read_multiple_files", args)
            return parse_multiple_files_response(response)

        except Exception as e:
            raise FileError(f"Failed to read multiple files: {e}")

    def search_files(self, path: str, pattern: str, exclude_patterns: Optional[List[str]] = None) -> List[str]:
        """
        Search for files matching a pattern in a directory.

        Args:
            path: The directory path to search.
            pattern: The pattern to match.
            exclude_patterns: Optional list of patterns to exclude.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries representing search results.

        Raises:
            FileError: If the operation fails.
        """
        args = {"path": path, "pattern": pattern}
        if exclude_patterns:
            args["excludePatterns"] = json.dumps(exclude_patterns)
        try:
            response = self._call_mcp_tool("search_files", args)
            print("Response from CallMcpTool - search_files:", response)

            # parse the response to list
            text_list = response.splitlines()
            if not text_list:
                raise FileError("No search results found")

            return [item.strip() for item in text_list]

        except Exception as e:
            raise FileError(f"Failed to search files: {e}")

    def write_file(self, path: str, content: str, mode: str = "overwrite") -> bool:
        """
        Write content to a file.

        Args:
            path: The path of the file to write.
            content: The content to write to the file.
            mode: The write mode ("overwrite" or "append").

        Returns:
            bool: True if the file was written successfully.

        Raises:
            FileError: If the operation fails.
        """
        args = {"path": path, "content": content, "mode": mode}
        try:
            response = self._call_mcp_tool("write_file", args)
            print("Response from CallMcpTool - write_file:", response)
            # If "isError" in the response is False, it would raise an exception when _parse_response_body
            return True
        except FileError:
            raise
        except Exception as e:
            raise FileError(f"Failed to write file: {e}")

    def read_large_file(self, path: str, chunk_size: int = 0) -> str:
        """
        Read large files by chunking to handle API size limitations.
        Automatically splits the read operation into multiple requests of chunk_size bytes each.
        If chunk_size <= 0, the default DEFAULT_CHUNK_SIZE (60KB) will be used.

        Args:
            path: The path of the file to read.
            chunk_size: Size of each chunk in bytes. Default is 0, which uses DEFAULT_CHUNK_SIZE.

        Returns:
            str: The complete content of the file.

        Raises:
            FileError: If the operation fails.
        """
        if chunk_size <= 0:
            chunk_size = self.DEFAULT_CHUNK_SIZE

        # First get the file size
        try:
            file_info = self.get_file_info(path)
            file_size = int(file_info.get("size", 0))

            if file_size == 0:
                raise FileError("Could not determine file size")

            print(f"ReadLargeFile: Starting chunked read of {path} (total size: {file_size} bytes, chunk size: {chunk_size} bytes)")

            # Prepare to read the file in chunks
            result = []
            offset = 0
            chunk_count = 0

            while offset < file_size:
                # Calculate how much to read in this chunk
                length = chunk_size
                if offset + length > file_size:
                    length = file_size - offset

                print(f"ReadLargeFile: Reading chunk {chunk_count+1} ({length} bytes at offset {offset}/{file_size})")

                # Read the chunk
                chunk = self.read_file(path, offset, length)
                result.append(chunk)

                # Move to the next chunk
                offset += length
                chunk_count += 1

            print(f"ReadLargeFile: Successfully read {path} in {chunk_count} chunks (total: {file_size} bytes)")

            return "".join(result)

        except FileError as e:
            raise FileError(f"Failed to read large file: {e}")

    def write_large_file(self, path: str, content: str, chunk_size: int = 0) -> bool:
        """
        Write large files by chunking to handle API size limitations.
        Automatically splits the write operation into multiple requests of chunk_size bytes each.
        If chunk_size <= 0, the default DEFAULT_CHUNK_SIZE (60KB) will be used.

        Args:
            path: The path of the file to write.
            content: The content to write to the file.
            chunk_size: Size of each chunk in bytes. Default is 0, which uses DEFAULT_CHUNK_SIZE.

        Returns:
            bool: True if the file was written successfully.

        Raises:
            FileError: If the operation fails.
        """
        if chunk_size <= 0:
            chunk_size = self.DEFAULT_CHUNK_SIZE

        content_len = len(content)

        print(f"WriteLargeFile: Starting chunked write to {path} (total size: {content_len} bytes, chunk size: {chunk_size} bytes)")

        # If content is small enough, use the regular write_file method
        if content_len <= chunk_size:
            print(f"WriteLargeFile: Content size ({content_len} bytes) is smaller than chunk size, using normal WriteFile")
            return self.write_file(path, content, "overwrite")

        try:
            # Write the first chunk with "overwrite" mode to create/clear the file
            first_chunk_end = min(chunk_size, content_len)
            print(f"WriteLargeFile: Writing first chunk (0-{first_chunk_end} bytes) with overwrite mode")
            self.write_file(path, content[:first_chunk_end], "overwrite")

            # Write the remaining chunks with "append" mode
            chunk_count = 1  # Already wrote first chunk
            for offset in range(first_chunk_end, content_len, chunk_size):
                end = min(offset + chunk_size, content_len)
                print(f"WriteLargeFile: Writing chunk {chunk_count+1} ({offset}-{end} bytes) with append mode")
                self.write_file(path, content[offset:end], "append")
                chunk_count += 1

            print(f"WriteLargeFile: Successfully wrote {path} in {chunk_count} chunks (total: {content_len} bytes)")
            return True

        except FileError as e:
            raise FileError(f"Failed to write large file: {e}")
