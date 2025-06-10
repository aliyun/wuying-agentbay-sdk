import json
import traceback
from typing import Any, Dict

from agentbay.api.models import CallMcpToolRequest
from agentbay.exceptions import AdbError


class Adb:
    """
    Adb handles ADB operations in the AgentBay mobile environment.
    """

    def __init__(self, session):
        """
        Initialize the Adb object.

        Args:
            session: The session object that provides access to the AgentBay API.
        """
        self.session = session

    def shell(self, command: str) -> str:
        """
        Execute an ADB shell command in the mobile environment.

        Args:
            command: The ADB shell command to execute.

        Returns:
            The output of the ADB shell command.

        Raises:
            Exception: If the command execution fails.
        """
        args = {"command": command}

        request = CallMcpToolRequest(
            args=json.dumps(args, ensure_ascii=False),
            authorization="Bearer " + str(self.session.get_api_key()),
            name="shell",
            session_id=str(self.session.get_session_id()),
        )

        try:
            response = self.session.get_client().call_mcp_tool(request)
            respoonse_map = response.to_map()

            body_map = respoonse_map["body"]
            data_map = body_map["Data"]
            if data_map.get("isError", False):
                error_msg = json.dumps(data_map, ensure_ascii=False)
                raise AdbError(error_msg)
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
            raise AdbError(
                f"Failed to execute ADB shell command: {error}\n{error_detail}"
            )
