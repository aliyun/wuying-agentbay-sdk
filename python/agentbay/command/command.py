from typing import Tuple, Optional
import json
from agentbay.api.models import CallMcpToolRequest
from agentbay.exceptions import CommandError


class Command:
    """
    Handles command execution operations in the AgentBay cloud environment.
    """

    def __init__(self, session):
        """
        Initialize a Command object.

        Args:
            session: The Session instance that this Command belongs to.
        """
        self.session = session

    def execute_command(self, command: str) -> str:
        """
        Execute a command in the cloud environment.

        Args:
            command: The command to execute.

        Returns:
            Dict[str, Any]: The result of the command execution.
        """
        try:
            args = {
                "command": command
            }
            args_json = json.dumps(args, ensure_ascii=False)

            request = CallMcpToolRequest(
                authorization=f"Bearer {self.session.get_api_key()}",
                session_id=self.session.get_session_id(),
                name="execute_command",
                args=args_json
            )
            print("request =", request)
            response = self.session.get_client().call_mcp_tool(request)
            print("response =", response)
            content_array = (
                    response.to_map()
                    .get("body", {})
                    .get("Data", {})
                    .get("content")
                )

            if not isinstance(content_array, list):
                raise CommandError("content field not found or not an array")

            full_text = ""
            for item in content_array:
                if not isinstance(item, dict):
                    continue
                text = item.get("text")
                if isinstance(text, str):
                    full_text += text + "\n"
            return full_text
        except Exception as e:
            raise CommandError(f"Failed to execute command: {e}")