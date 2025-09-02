from typing import Any, Dict, List, Optional, Union
import json

from agentbay.api.base_service import BaseService
from ..logger import get_logger, log_api_response, log_operation_start, log_operation_success
from agentbay.exceptions import AgentBayError, FileError
from agentbay.model import ApiResponse, BoolResult

# Initialize logger for this module
logger = get_logger("filesystem")


class FileInfoResult(ApiResponse):
    """Result of file info operations."""

    def __init__(
        self,
        request_id: str = "",
        success: bool = False,
        file_info: Optional[Dict[str, Any]] = None,
        error_message: str = "",
    ):
        """
        Initialize a FileInfoResult.

        Args:
            request_id (str, optional): Unique identifier for the API request.
                Defaults to "".
            success (bool, optional): Whether the operation was successful.
                Defaults to False.
            file_info (Dict[str, Any], optional): File information. Defaults to None.
            error_message (str, optional): Error message if the operation failed.
                Defaults to "".
        """
        super().__init__(request_id)
        self.success = success
        self.file_info = file_info or {}
        self.error_message = error_message


class DirectoryListResult(ApiResponse):
    """Result of directory listing operations."""

    def __init__(
        self,
        request_id: str = "",
        success: bool = False,
        entries: Optional[List[Dict[str, Any]]] = None,
        error_message: str = "",
    ):
        """
        Initialize a DirectoryListResult.

        Args:
            request_id (str, optional): Unique identifier for the API request.
                Defaults to "".
            success (bool, optional): Whether the operation was successful.
                Defaults to False.
            entries (List[Dict[str, Any]], optional): Directory entries. Defaults to
                None.
            error_message (str, optional): Error message if the operation failed.
                Defaults to "".
        """
        super().__init__(request_id)
        self.success = success
        self.entries = entries or []
        self.error_message = error_message


class FileContentResult(ApiResponse):
    """Result of file read operations."""

    def __init__(
        self,
        request_id: str = "",
        success: bool = False,
        content: str = "",
        error_message: str = "",
    ):
        """
        Initialize a FileContentResult.

        Args:
            request_id (str, optional): Unique identifier for the API request.
                Defaults to "".
            success (bool, optional): Whether the operation was successful.
                Defaults to False.
            content (str, optional): File content. Defaults to "".
            error_message (str, optional): Error message if the operation failed.
                Defaults to "".
        """
        super().__init__(request_id)
        self.success = success
        self.content = content
        self.error_message = error_message


class MultipleFileContentResult(ApiResponse):
    """Result of multiple file read operations."""

    def __init__(
        self,
        request_id: str = "",
        success: bool = False,
        contents: Optional[Dict[str, str]] = None,
        error_message: str = "",
    ):
        """
        Initialize a MultipleFileContentResult.

        Args:
            request_id (str, optional): Unique identifier for the API request.
                Defaults to "".
            success (bool, optional): Whether the operation was successful.
                Defaults to False.
            contents (Dict[str, str], optional): Dictionary of file paths to file
                contents. Defaults to None.
            error_message (str, optional): Error message if the operation failed.
                Defaults to "".
        """
        super().__init__(request_id)
        self.success = success
        self.contents = contents or {}
        self.error_message = error_message


class FileSearchResult(ApiResponse):
    """Result of file search operations."""

    def __init__(
        self,
        request_id: str = "",
        success: bool = False,
        matches: Optional[List[str]] = None,
        error_message: str = "",
    ):
        """
        Initialize a FileSearchResult.

        Args:
            request_id (str, optional): Unique identifier for the API request.
                Defaults to "".
            success (bool, optional): Whether the operation was successful.
                Defaults to False.
            matches (List[str], optional): Matching file paths. Defaults to None.
            error_message (str, optional): Error message if the operation failed.
                Defaults to "".
        """
        super().__init__(request_id)
        self.success = success
        self.matches = matches or []
        self.error_message = error_message


class FileSystem(BaseService):
    """
    Handles file operations in the AgentBay cloud environment.
    """

    # Default chunk size is 50KB
    DEFAULT_CHUNK_SIZE = 50 * 1024

    def _handle_error(self, e):
        """
        Convert AgentBayError to FileError for compatibility.

        Args:
            e (Exception): The exception to convert.

        Returns:
            FileError: The converted exception.
        """
        if isinstance(e, FileError):
            return e
        if isinstance(e, AgentBayError):
            return FileError(str(e))
        return e

    def create_directory(self, path: str) -> BoolResult:
        """
        Create a new directory at the specified path.

        Args:
            path: The path of the directory to create.

        Returns:
            BoolResult: Result object containing success status and error message if
                any.
        """
        args = {"path": path}
        try:
            result = self._call_mcp_tool("create_directory", args)
            logger.debug(f"📥 create_directory response: {result}")
            if result.success:
                return BoolResult(request_id=result.request_id, success=True, data=True)
            else:
                return BoolResult(
                    request_id=result.request_id,
                    success=False,
                    error_message=result.error_message,
                )
        except FileError as e:
            return BoolResult(request_id="", success=False, error_message=str(e))
        except Exception as e:
            return BoolResult(
                request_id="",
                success=False,
                error_message=f"Failed to create directory: {e}",
            )

    def edit_file(
        self, path: str, edits: List[Dict[str, str]], dry_run: bool = False
    ) -> BoolResult:
        """
        Edit a file by replacing occurrences of oldText with newText.

        Args:
            path: The path of the file to edit.
            edits: A list of dictionaries specifying oldText and newText.
            dry_run: If True, preview changes without applying them.

        Returns:
            BoolResult: Result object containing success status and error message if
                any.
        """
        args = {"path": path, "edits": edits, "dryRun": dry_run}
        try:
            result = self._call_mcp_tool("edit_file", args)
            logger.debug(f"📥 edit_file response: {result}")
            if result.success:
                return BoolResult(request_id=result.request_id, success=True, data=True)
            else:
                return BoolResult(
                    request_id=result.request_id,
                    success=False,
                    error_message=result.error_message,
                )
        except FileError as e:
            return BoolResult(request_id="", success=False, error_message=str(e))
        except Exception as e:
            return BoolResult(
                request_id="",
                success=False,
                error_message=f"Failed to edit file: {e}",
            )

    def get_file_info(self, path: str) -> FileInfoResult:
        """
        Get information about a file or directory.

        Args:
            path: The path of the file or directory to inspect.

        Returns:
            FileInfoResult: Result object containing file info and error message if any.
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
            result = self._call_mcp_tool("get_file_info", args)
            try:
                response_body = json.dumps(
                    getattr(result, "body", result), ensure_ascii=False, indent=2
                )
                log_api_response(response_body)
            except Exception:
                logger.debug(f"📥 Response: {result}")
            if result.success:
                file_info = parse_file_info(result.data)
                return FileInfoResult(
                    request_id=result.request_id,
                    success=True,
                    file_info=file_info,
                )
            else:
                return FileInfoResult(
                    request_id=result.request_id,
                    success=False,
                    error_message=result.error_message or "Failed to get file info",
                )
        except FileError as e:
            return FileInfoResult(request_id="", success=False, error_message=str(e))
        except Exception as e:
            return FileInfoResult(
                request_id="",
                success=False,
                error_message=f"Failed to get file info: {e}",
            )

    def list_directory(self, path: str) -> DirectoryListResult:
        """
        List the contents of a directory.

        Args:
            path: The path of the directory to list.

        Returns:
            DirectoryListResult: Result object containing directory entries and error
                message if any.
        """

        def parse_directory_listing(text) -> List[Dict[str, Union[str, bool]]]:
            """
            Parse a directory listing text into a list of file/directory entries.

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
            """
            result = []
            lines = text.split("\n")

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
            result = self._call_mcp_tool("list_directory", args)
            try:
                response_body = json.dumps(
                    getattr(result, "body", result), ensure_ascii=False, indent=2
                )
                log_api_response(response_body)
            except Exception:
                logger.debug(f"📥 Response: {result}")
            if result.success:
                entries = parse_directory_listing(result.data)
                return DirectoryListResult(
                    request_id=result.request_id, success=True, entries=entries
                )
            else:
                return DirectoryListResult(
                    request_id=result.request_id,
                    success=False,
                    error_message=result.error_message or "Failed to list directory",
                )
        except FileError as e:
            return DirectoryListResult(
                request_id="", success=False, error_message=str(e)
            )
        except Exception as e:
            return DirectoryListResult(
                request_id="",
                success=False,
                error_message=f"Failed to list directory: {e}",
            )

    def move_file(self, source: str, destination: str) -> BoolResult:
        """
        Move a file or directory from source path to destination path.

        Args:
            source: The source path of the file or directory.
            destination: The destination path.

        Returns:
            BoolResult: Result object containing success status and error message if
                any.
        """
        args = {"source": source, "destination": destination}
        try:
            result = self._call_mcp_tool("move_file", args)
            logger.debug(f"📥 move_file response: {result}")
            if result.success:
                return BoolResult(request_id=result.request_id, success=True, data=True)
            else:
                return BoolResult(
                    request_id=result.request_id,
                    success=False,
                    error_message=result.error_message or "Failed to move file",
                )
        except AgentBayError as e:
            return BoolResult(request_id="", success=False, error_message=str(e))
        except Exception as e:
            return BoolResult(
                request_id="",
                success=False,
                error_message=f"Failed to move file: {e}",
            )

    def _read_file_chunk(
        self, path: str, offset: int = 0, length: int = 0
    ) -> FileContentResult:
        """
        Internal method to read a file chunk. Used for chunked file operations.

        Args:
            path: The path of the file to read.
            offset: Byte offset to start reading from (0-based).
            length: Number of bytes to read. If 0, reads the entire file from offset.

        Returns:
            FileContentResult: Result object containing file content and error message
                if any.
        """
        args = {"path": path}
        if offset >= 0:
            args["offset"] = offset
        if length >= 0:
            args["length"] = length

        try:
            result = self._call_mcp_tool("read_file", args)
            try:
                response_body = json.dumps(
                    getattr(result, "body", result), ensure_ascii=False, indent=2
                )
                log_api_response(response_body)
            except Exception:
                logger.debug(f"📥 Response: {result}")
            if result.success:
                return FileContentResult(
                    request_id=result.request_id,
                    success=True,
                    content=result.data,
                )
            else:
                return FileContentResult(
                    request_id=result.request_id,
                    success=False,
                    error_message=result.error_message or "Failed to read file",
                )
        except FileError as e:
            return FileContentResult(request_id="", success=False, error_message=str(e))
        except Exception as e:
            return FileContentResult(
                request_id="",
                success=False,
                error_message=f"Failed to read file: {e}",
            )

    def read_multiple_files(self, paths: List[str]) -> MultipleFileContentResult:
        """
        Read the contents of multiple files at once.

        Args:
            paths: A list of file paths to read.

        Returns:
            MultipleFileContentResult: Result object containing a dictionary mapping
                file paths to contents,
            and error message if any.
        """

        def parse_multiple_files_response(text: str) -> Dict[str, str]:
            """
            Parse the response from reading multiple files.

            Args:
                text (str): The response string containing file contents.
                Format: "/path/to/file1.txt: Content of file1\n\n---\n
                    /path/to/file2.txt: \nContent of file2\n"

            Returns:
                Dict[str, str]: A dictionary mapping file paths to their content.
            """
            result = {}
            if not text:
                return result

            lines = text.split("\n")
            current_path = None
            current_content = []

            for i, line in enumerate(lines):
                # Check if this line contains a file path (ends with a colon)
                if ":" in line and not current_path:
                    # Extract path (everything before the first colon)
                    path_end = line.find(":")
                    path = line[:path_end].strip()

                    # Start collecting content (everything after the colon)
                    current_path = path

                    # If there's content on the same line after the colon, add it
                    if len(line) > path_end + 1:
                        content_start = line[path_end + 1 :].strip()
                        if content_start:
                            current_content.append(content_start)

                # Check if this is a separator line
                elif line.strip() == "---":
                    # Save the current file content
                    if current_path:
                        result[current_path] = "\n".join(current_content).strip()
                        current_path = None
                        current_content = []

                # If we're collecting content for a path, add this line
                elif current_path is not None:
                    current_content.append(line)

            # Save the last file content if exists
            if current_path:
                result[current_path] = "\n".join(current_content).strip()

            return result

        args = {"paths": paths}
        try:
            result = self._call_mcp_tool("read_multiple_files", args)
            try:
                response_body = json.dumps(
                    getattr(result, "body", result), ensure_ascii=False, indent=2
                )
                log_api_response(response_body)
            except Exception:
                logger.debug(f"📥 Response: {result}")

            if result.success:
                files_content = parse_multiple_files_response(result.data)
                return MultipleFileContentResult(
                    request_id=result.request_id,
                    success=True,
                    contents=files_content,
                )
            else:
                return MultipleFileContentResult(
                    request_id=result.request_id,
                    success=False,
                    error_message=result.error_message
                    or "Failed to read multiple files",
                )
        except FileError as e:
            return MultipleFileContentResult(
                request_id="", success=False, error_message=str(e)
            )
        except Exception as e:
            return MultipleFileContentResult(
                request_id="",
                success=False,
                error_message=f"Failed to read multiple files: {e}",
            )

    def search_files(
        self,
        path: str,
        pattern: str,
        exclude_patterns: Optional[List[str]] = None,
    ) -> FileSearchResult:
        """
        Search for files in the specified path using a pattern.

        Args:
            path: The base directory path to search in.
            pattern: The glob pattern to search for.
            exclude_patterns: Optional list of patterns to exclude from the search.

        Returns:
            FileSearchResult: Result object containing matching file paths and error
                message if any.
        """
        args = {"path": path, "pattern": pattern}
        if exclude_patterns:
            args["excludePatterns"] = exclude_patterns

        try:
            result = self._call_mcp_tool("search_files", args)
            logger.debug(f"📥 search_files response: {result}")

            if result.success:
                matching_files = result.data.strip().split("\n") if result.data else []
                return FileSearchResult(
                    request_id=result.request_id,
                    success=True,
                    matches=matching_files,
                )
            else:
                return FileSearchResult(
                    request_id=result.request_id,
                    success=False,
                    error_message=result.error_message or "Failed to search files",
                )
        except FileError as e:
            return FileSearchResult(request_id="", success=False, error_message=str(e))
        except Exception as e:
            return FileSearchResult(
                request_id="",
                success=False,
                error_message=f"Failed to search files: {e}",
            )

    def _write_file_chunk(
        self, path: str, content: str, mode: str = "overwrite"
    ) -> BoolResult:
        """
        Internal method to write a file chunk. Used for chunked file operations.

        Args:
            path: The path of the file to write.
            content: The content to write to the file.
            mode: The write mode ("overwrite" or "append").

        Returns:
            BoolResult: Result object containing success status and error message if
                any.
        """
        if mode not in ["overwrite", "append"]:
            return BoolResult(
                request_id="",
                success=False,
                error_message=(
                    f"Invalid write mode: {mode}. Must be 'overwrite' or " "'append'."
                ),
            )

        args = {"path": path, "content": content, "mode": mode}
        try:
            result = self._call_mcp_tool("write_file", args)
            logger.debug(f"📥 write_file response: {result}")
            if result.success:
                return BoolResult(request_id=result.request_id, success=True, data=True)
            else:
                return BoolResult(
                    request_id=result.request_id,
                    success=False,
                    error_message=result.error_message or "Failed to write file",
                )
        except FileError as e:
            return BoolResult(request_id="", success=False, error_message=str(e))
        except Exception as e:
            return BoolResult(
                request_id="",
                success=False,
                error_message=f"Failed to write file: {e}",
            )

    def read_file(self, path: str) -> FileContentResult:
        """
        Read the contents of a file. Automatically handles large files by chunking.

        Args:
            path: The path of the file to read.

        Returns:
            FileContentResult: Result object containing file content and error message
                if any.
        """
        # Use default chunk size
        chunk_size = self.DEFAULT_CHUNK_SIZE

        try:
            # Get file info to check size
            file_info_result = self.get_file_info(path)
            if not file_info_result.success:
                return FileContentResult(
                    request_id=file_info_result.request_id,
                    success=False,
                    error_message=file_info_result.error_message,
                )

            # Check if file exists and is a file (not a directory)
            if not file_info_result.file_info or file_info_result.file_info.get(
                "isDirectory", False
            ):
                return FileContentResult(
                    request_id=file_info_result.request_id,
                    success=False,
                    error_message=f"Path does not exist or is a directory: {path}",
                )

            # If the file is empty, return empty string
            file_size = file_info_result.file_info.get("size", 0)
            if file_size == 0:
                return FileContentResult(
                    request_id=file_info_result.request_id,
                    success=True,
                    content="",
                )

            # Read the file in chunks
            content = []
            offset = 0
            chunk_count = 0
            while offset < file_size:
                length = min(chunk_size, file_size - offset)
                chunk_result = self.read_file(path, offset, length)
                log_operation_start(
                    f"ReadLargeFile chunk {chunk_count + 1}",
                    f"{length} bytes at offset {offset}/{file_size}"
                )

                if not chunk_result.success:
                    return chunk_result  # Return the error

                content.append(chunk_result.content)
                offset += length
                chunk_count += 1

            return FileContentResult(
                request_id=file_info_result.request_id,
                success=True,
                content="".join(content),
            )

        except FileError as e:
            return FileContentResult(request_id="", success=False, error_message=str(e))
        except Exception as e:
            return FileContentResult(
                request_id="",
                success=False,
                error_message=f"Failed to read file: {e}",
            )

    def write_file(
        self, path: str, content: str, mode: str = "overwrite"
    ) -> BoolResult:
        """
        Write content to a file. Automatically handles large files by chunking.

        Args:
            path: The path of the file to write.
            content: The content to write to the file.
            mode: The write mode ("overwrite" or "append").

        Returns:
            BoolResult: Result object containing success status and error message if
                any.
        """
        # Use default chunk size
        chunk_size = self.DEFAULT_CHUNK_SIZE
        content_len = len(content)
        log_operation_start(
            f"WriteLargeFile to {path}",
            f"total size: {content_len} bytes, chunk size: {chunk_size} bytes"
        )

        # If the content length is less than the chunk size, write it directly
        if content_len <= chunk_size:
            return self._write_file_chunk(path, content, mode)

        try:
            # Write the first chunk (creates or overwrites the file)
            first_chunk = content[:chunk_size]
            result = self._write_file_chunk(path, first_chunk, mode)
            if not result.success:
                return result

            # Write the rest in chunks (appending)
            offset = chunk_size
            while offset < content_len:
                end = min(offset + chunk_size, content_len)
                current_chunk = content[offset:end]
                result = self._write_file_chunk(path, current_chunk, "append")
                if not result.success:
                    return result
                offset = end

            return BoolResult(request_id=result.request_id, success=True, data=True)

        except FileError as e:
            return BoolResult(request_id="", success=False, error_message=str(e))
        except Exception as e:
            return BoolResult(
                request_id="",
                success=False,
                error_message=f"Failed to write file: {e}",
            )
