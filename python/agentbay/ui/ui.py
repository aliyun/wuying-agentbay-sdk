import json
from typing import Any, Dict, List

from agentbay.api.models import CallMcpToolRequest
from agentbay.exceptions import AgentBayError

class KeyCode:
    """
    Key codes for mobile device input.
    """
    HOME = 3
    BACK = 4
    VOLUME_UP = 24
    VOLUME_DOWN = 25
    POWER = 26
    MENU = 82


class UI:
    """
    Handles UI operations in the AgentBay cloud environment.
    """
    def __init__(self, session):
        """
        Initialize a UI object.

        Args:
            session: The session object that provides access to the AgentBay API.
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
            AgentBayError: If the tool call fails.
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
                raise AgentBayError("Invalid response format")
            body = response_map.get("body", {})
            if not body:
                raise AgentBayError("Invalid response body")
            return self._parse_response_body(body)
        except (KeyError, TypeError, ValueError) as e:
            raise AgentBayError(f"Failed to parse MCP tool response: {e}")
        except Exception as e:
            raise AgentBayError(f"Failed to call MCP tool {name}: {e}")

    def _parse_response_body(self, body: Dict[str, Any]) -> Any:
        """
        Parses the response body from the MCP tool.

        Args:
            body (Dict[str, Any]): The response body.

        Returns:
            Any: The parsed content.

        Raises:
            AgentBayError: If the response contains errors or is invalid.
        """
        try:
            if body.get("Data", {}).get("isError", False):
                error_content = body.get("Data", {}).get("content", [])
                error_message = "; ".join(
                    item.get("text", "Unknown error")
                    for item in error_content
                    if isinstance(item, dict)
                )
                raise AgentBayError(f"Error in response: {error_message}")
            response_data = body.get("Data", {})
            if not response_data:
                raise AgentBayError("No data field in response")
            content = response_data.get("content", [])
            if not content or not isinstance(content, list):
                raise AgentBayError("No content found in response")
            content_item = content[0]
            json_text = content_item.get("text")
            return json_text
        except Exception as e:
            raise AgentBayError(f"{e}")

    def get_clickable_ui_elements(self, timeout_ms: int = 2000) -> List[Dict[str, Any]]:
        """
        Retrieves all clickable UI elements within the specified timeout.

        Args:
            timeout_ms (int, optional): Timeout in milliseconds. Defaults to 2000.

        Returns:
            List[Dict[str, Any]]: A list of clickable UI elements.

        Raises:
            AgentBayError: If the operation fails.
        """
        args = {"timeout_ms": timeout_ms}
        try:
            result = self._call_mcp_tool("get_clickable_ui_elements", args)
            elements = json.loads(result)
            return elements
        except AgentBayError:
            raise
        except Exception as e:
            raise AgentBayError(f"Failed to get clickable UI elements: {e}")

    def get_all_ui_elements(self, timeout_ms: int = 2000) -> List[Dict[str, Any]]:
        """
        Retrieves all UI elements within the specified timeout.

        Args:
            timeout_ms (int, optional): Timeout in milliseconds. Defaults to 2000.

        Returns:
            List[Dict[str, Any]]: A list of all UI elements with parsed details.

        Raises:
            AgentBayError: If the operation fails.
        """
        args = {"timeout_ms": timeout_ms}
        def parse_element(element: Dict[str, Any]) -> Dict[str, Any]:
            """
            Recursively parses a UI element and its children.

            Args:
                element (Dict[str, Any]): The UI element to parse.

            Returns:
                Dict[str, Any]: The parsed UI element.
            """
            parsed = {
                "bounds": element.get("bounds", ""),
                "className": element.get("className", ""),
                "text": element.get("text", ""),
                "type": element.get("type", ""),
                "resourceId": element.get("resourceId", ""),
                "index": element.get("index", -1),
                "isParent": element.get("isParent", False),
            }
            children = element.get("children", [])
            if children:
                parsed["children"] = [parse_element(child) for child in children]
            else:
                parsed["children"] = []
            return parsed
        try:
            result = self._call_mcp_tool("get_all_ui_elements", args)
            elements = json.loads(result)
            return [parse_element(element) for element in elements]
        except AgentBayError:
            raise
        except Exception as e:
            raise AgentBayError(f"Failed to get all UI elements: {e}")

    def send_key(self, key: int) -> bool:
        """
        Sends a key press event.

        Args:
            key (int): The key code to send. Supported key codes are:
                - 3 : HOME
                - 4 : BACK
                - 24 : VOLUME UP
                - 25 : VOLUME DOWN
                - 26 : POWER
                - 82 : MENU

        Returns:
            bool: True if the key was sent successfully.

        Raises:
            AgentBayError: If the operation fails.
        """
        args = {"key": key}
        try:
            result = self._call_mcp_tool("send_key", args)
            return result
        except AgentBayError:
            raise
        except Exception as e:
            raise AgentBayError(f"Failed to send key: {e}")

    def input_text(self, text: str) -> None:
        """
        Inputs text into the active field.

        Args:
            text (str): The text to input.

        Raises:
            AgentBayError: If the operation fails.
        """
        args = {"text": text}
        try:
            self._call_mcp_tool("input_text", args)
        except AgentBayError:
            raise
        except Exception as e:
            raise AgentBayError(f"Failed to input text: {e}")

    def swipe(self, start_x: int, start_y: int, end_x: int, end_y: int, duration_ms: int = 300) -> None:
        """
        Performs a swipe gesture on the screen.

        Args:
            start_x (int): Starting X coordinate.
            start_y (int): Starting Y coordinate.
            end_x (int): Ending X coordinate.
            end_y (int): Ending Y coordinate.
            duration_ms (int, optional): Duration of the swipe in milliseconds. Defaults to 300.

        Raises:
            AgentBayError: If the operation fails.
        """
        args = {
            "start_x": start_x,
            "start_y": start_y,
            "end_x": end_x,
            "end_y": end_y,
            "duration_ms": duration_ms,
        }
        try:
            self._call_mcp_tool("swipe", args)
        except AgentBayError:
            raise
        except Exception as e:
            raise AgentBayError(f"Failed to perform swipe: {e}")

    def click(self, x: int, y: int, button: str = "left") -> None:
        """
        Clicks on the screen at the specified coordinates.

        Args:
            x (int): X coordinate.
            y (int): Y coordinate.
            button (str, optional): Button type (left, middle, right). Defaults to "left".

        Raises:
            AgentBayError: If the operation fails.
        """
        args = {"x": x, "y": y, "button": button}
        try:
            self._call_mcp_tool("click", args)
        except AgentBayError:
            raise
        except Exception as e:
            raise AgentBayError(f"Failed to perform click: {e}")

    def screenshot(self) -> str:
        """
        Takes a screenshot of the current screen using the system_screenshot tool.

        Returns:
            str: The screenshot data.

        Raises:
            AgentBayError: If the operation fails.
        """
        args = {}
        try:
            result = self._call_mcp_tool("system_screenshot", args)
            return result
        except AgentBayError:
            raise
        except Exception as e:
            raise AgentBayError(f"Failed to take screenshot: {e}")
