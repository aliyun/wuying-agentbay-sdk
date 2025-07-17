import json
from agentbay.exceptions import AgentError
from agentbay.api.models import CallMcpToolRequest
from typing import Dict, Any


class ActionResult:
    """
    Result of the puppeteer action.
    """

    def __init__(self, success: bool, message: str, action: str):
        self.success = success
        self.message = message
        self.action = action


class Agent:
    """
    An Agent to manipulate applications to complete specific tasks.
    """

    def __init__(self, session):
        self.session = session

    def flux_execute_task(self, task: str):
        """
        To execute a specific task described in the humman language.
        """
        try:
            args = {
                "task": task,
            }
            response = self.call_mcp_tool("execute_flux_task", args)
            print("Response from execute_flux_task:", response)
            import json as _json

            if isinstance(response, str):
                data = _json.loads(response)
            else:
                data = response
            success = data.get("success", False)
            message = data.get("message", "")
            action = data.get("action", "")
            return ActionResult(success=success, message=message, action=action)
        except Exception as e:
            raise AgentError(f"Failed to execute task: {e}")

    def flux_terminate_task(self, task_id: str) -> ActionResult:
        """
        To terminate a running task with specified taskId.
        """
        try:
            args = {
                "task_id": task_id,
            }
            response = self.call_mcp_tool("terminate_flux_task", args)
            print("Response from terminate_flux_task:", response)
            import json as _json

            if isinstance(response, str):
                data = _json.loads(response)
            else:
                data = response
            success = data.get("success", False)
            message = data.get("message", "")
            action = data.get("action", "")
            return ActionResult(success=success, message=message, action=action)
        except Exception as e:
            raise AgentError(f"Failed to execute task: {e}")

    def call_mcp_tool(self, name: str, args: dict):
        """
        Call an MCP tool and handle errors.
        Args:
            name (str): The name of the tool to call.
            args (dict): Arguments to pass to the tool.
        Returns:
            Any: The response from the tool.
        Raises:
            AgentError: If the tool call fails.
        """
        try:
            request = CallMcpToolRequest(
                authorization=f"Bearer {self.session.get_api_key()}",
                session_id=self.session.get_session_id(),
                name=name,
                args=json.dumps(args, ensure_ascii=False),
            )
            response = self.session.get_client().call_mcp_tool(request)
            response_map = response.to_map()
            if not response_map:
                raise AgentError("Invalid response format")
            body = response_map.get("body", {})
            if not body:
                raise AgentError("Invalid response body")
            return self.parse_response_body(body)
        except Exception as e:
            raise AgentError(f"Failed to call MCP tool {name}: {e}")

    def parse_response_body(self, body: Dict[str, Any]) -> Any:
        """
        Parses the response body from the MCP tool.

        Args:
            body (Dict[str, Any]): The response body.

        Returns:
            Any: The parsed content.

        Raises:
            BrowserError: If the response contains errors or is invalid.
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
                raise AgentError(f"Error in response: {error_message}")

            response_data = body.get("Data", {})
            if not response_data:
                raise AgentError("No data field in response")

            # Handle 'content' field for other methods
            content = response_data.get("content", [])
            if not content or not isinstance(content, list):
                raise AgentError("No content found in response")

            content_item = content[0]
            json_text = content_item.get("text")
            return json_text
        except Exception as e:
            raise AgentError(f"{e}")
