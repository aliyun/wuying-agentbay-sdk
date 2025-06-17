import json
from typing import List, Dict, Union, Any, Optional

from agentbay.api.models import CallMcpToolRequest
from agentbay.exceptions import FileError


class FileSystem:
    """
    Handles file operations in the AgentBay cloud environment.
    """

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
            return response == "True"
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

            return response == "True"
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
        args = {"path": path}
        try:
            args_json = json.dumps(args, ensure_ascii=False)
            request = CallMcpToolRequest(
                authorization=f"Bearer {self.session.get_api_key()}",
                session_id=self.session.get_session_id(),
                name="list_directory",
                args=args_json,
            )
            response = self.session.get_client().call_mcp_tool(request)
            response_map = response.to_map()
            if not response_map:
                raise FileError("Invalid response format")
            body = response_map.get("body", {})
            print("body =", body)

            if not body:
                raise FileError("Invalid response body")

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

            # Handle 'results' field for search_files
            if "entries" in response_data:
                files_list = response_data["entries"]
                if isinstance(files_list, list):
                    return files_list
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
            return response == "True"
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
        args = {"paths": paths}
        try:
            args_json = json.dumps(args, ensure_ascii=False)
            request = CallMcpToolRequest(
                authorization=f"Bearer {self.session.get_api_key()}",
                session_id=self.session.get_session_id(),
                name="read_multiple_files",
                args=args_json,
            )
            response = self.session.get_client().call_mcp_tool(request)
            response_map = response.to_map()
            if not response_map:
                raise FileError("Invalid response format")
            body = response_map.get("body", {})
            print("body =", body)

            if not body:
                raise FileError("Invalid response body")

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

            # Handle 'results' field for search_files
            if "files" in response_data:
                files_list = response_data["files"]
                if isinstance(files_list, dict):
                    return files_list

            raise FileError("Invalid response format for read_multiple_files")
        except Exception as e:
            raise FileError(f"Failed to read multiple files: {e}")

    def search_files(self, path: str, pattern: str, exclude_patterns: Optional[List[str]] = None) -> List[Dict[str, Any]]:
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
            args_json = json.dumps(args, ensure_ascii=False)
            request = CallMcpToolRequest(
                authorization=f"Bearer {self.session.get_api_key()}",
                session_id=self.session.get_session_id(),
                name="search_files",
                args=args_json,
            )
            response = self.session.get_client().call_mcp_tool(request)
            response_map = response.to_map()
            if not response_map:
                raise FileError("Invalid response format")
            body = response_map.get("body", {})
            print("body =", body)

            if not body:
                raise FileError("Invalid response body")

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

            # Handle 'results' field for search_files
            if "results" in response_data:
                files_list = response_data["results"]
                if isinstance(files_list, list):
                    return files_list

            raise FileError("Invalid response format for search_files")
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
            return response == "True"
        except FileError:
            raise
        except Exception as e:
            raise FileError(f"Failed to write file: {e}")
