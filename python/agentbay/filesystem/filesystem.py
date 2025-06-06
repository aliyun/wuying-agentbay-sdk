import json
import traceback

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
        # self._base_url = f"{session._base_url}/files"

    def read_file(self, path: str) -> str:
        """
        Read the contents of a file in the cloud environment.

        Args:
            path: Path to the file to read.

        Returns:
            str: The contents of the file.
        """
        args = {"path": path}

        request = CallMcpToolRequest(
            args=json.dumps(args, ensure_ascii=False),
            authorization="Bearer " + str(self.session.get_api_key()),
            name="read_file",
            session_id=str(self.session.get_session_id()),
        )

        try:
            response = self.session.get_client().call_mcp_tool(request)
            respoonse_map = response.to_map()
            body_map = respoonse_map["body"]
            data_map = body_map["Data"]

            if data_map.get("isError", False):
                error_msg = json.dumps(data_map, ensure_ascii=False)
                raise FileError(error_msg)
            content_array = data_map.get("content", [])
            text_array = []

            for item in content_array:
                try:
                    text = item.get("text", "")
                    text_array.append(str(text))
                except Exception:
                    continue
            result = "\n".join(text_array)
            return result
        except Exception as error:
            error_detail = traceback.format_exc()
            raise FileError(f"Failed to read file: {error}\n{error_detail}")
