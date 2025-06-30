import json
from typing import Any, Dict, List, Optional

from agentbay.exceptions import AgentBayError, UIError
from agentbay.model import (
    OperationResult, BoolResult, ApiResponse
)
from agentbay.api.base_service import BaseService


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


class UIElementListResult(ApiResponse):
    """Result of UI element listing operations."""

    def __init__(self, request_id: str = "", success: bool = False,
                 elements: Optional[List[Dict[str, Any]]] = None, error_message: str = ""):
        """
        Initialize a UIElementListResult.

        Args:
            request_id (str, optional): Unique identifier for the API request. Defaults to "".
            success (bool, optional): Whether the operation was successful. Defaults to False.
            elements (List[Dict[str, Any]], optional): UI elements. Defaults to None.
            error_message (str, optional): Error message if the operation failed. Defaults to "".
        """
        super().__init__(request_id)
        self.success = success
        self.elements = elements or []
        self.error_message = error_message


class UI(BaseService):
    """
    Handles UI operations in the AgentBay cloud environment.
    """

    def __init__(self, session):
        """
        Initialize a UI object.

        Args:
            session: The session object that provides access to the AgentBay API.
        """
        super().__init__(session)

    def _handle_error(self, e):
        """
        Convert AgentBayError to UIError for compatibility.

        Args:
            e (Exception): The exception to convert.

        Returns:
            UIError: The converted exception.
        """
        if isinstance(e, UIError):
            return e
        if isinstance(e, AgentBayError):
            return UIError(str(e))
        return e

    def get_clickable_ui_elements(self, timeout_ms: int = 2000) -> UIElementListResult:
        """
        Retrieves all clickable UI elements within the specified timeout.

        Args:
            timeout_ms (int, optional): Timeout in milliseconds. Defaults to 2000.

        Returns:
            UIElementListResult: Result object containing clickable UI elements and error message if any.
        """
        args = {"timeout_ms": timeout_ms}
        result = self._call_mcp_tool("get_clickable_ui_elements", args)
        request_id = result.request_id

        if not result.success:
            return UIElementListResult(request_id=request_id, success=False, error_message=result.error_message)

        try:
            elements = json.loads(result.data)
            return UIElementListResult(request_id=request_id, success=True, elements=elements)
        except Exception as e:
            return UIElementListResult(request_id=request_id, success=False, error_message=f"Failed to parse clickable UI elements data: {e}")

    def get_all_ui_elements(self, timeout_ms: int = 2000) -> UIElementListResult:
        """
        Retrieves all UI elements within the specified timeout.

        Args:
            timeout_ms (int, optional): Timeout in milliseconds. Defaults to 2000.

        Returns:
            UIElementListResult: Result object containing UI elements and error message if any.
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

        result = self._call_mcp_tool("get_all_ui_elements", args)
        request_id = result.request_id

        if not result.success:
            return UIElementListResult(request_id=request_id, success=False, error_message=result.error_message)

        try:
            elements = json.loads(result.data)
            parsed_elements = [parse_element(element) for element in elements]
            return UIElementListResult(request_id=request_id, success=True, elements=parsed_elements)
        except Exception as e:
            return UIElementListResult(request_id=request_id, success=False, error_message=f"Failed to parse UI elements data: {e}")

    def send_key(self, key: int) -> BoolResult:
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
            BoolResult: Result object containing success status and error message if any.
        """
        args = {"key": key}
        result = self._call_mcp_tool("send_key", args)

        return BoolResult(
            request_id=result.request_id,
            success=result.success,
            data=True if result.success else None,
            error_message="" if result.success else result.error_message
        )

    def input_text(self, text: str) -> BoolResult:
        """
        Inputs text into the active field.

        Args:
            text (str): The text to input.

        Returns:
            BoolResult: Result object containing success status and error message if any.
        """
        args = {"text": text}
        result = self._call_mcp_tool("input_text", args)

        return BoolResult(
            request_id=result.request_id,
            success=result.success,
            data=True if result.success else None,
            error_message="" if result.success else result.error_message
        )

    def swipe(
        self, start_x: int, start_y: int, end_x: int, end_y: int, duration_ms: int = 300
    ) -> BoolResult:
        """
        Performs a swipe gesture from one point to another.

        Args:
            start_x (int): Starting X coordinate.
            start_y (int): Starting Y coordinate.
            end_x (int): Ending X coordinate.
            end_y (int): Ending Y coordinate.
            duration_ms (int, optional): Duration of the swipe in milliseconds. Defaults to 300.

        Returns:
            BoolResult: Result object containing success status and error message if any.
        """
        args = {
            "start_x": start_x,
            "start_y": start_y,
            "end_x": end_x,
            "end_y": end_y,
            "duration_ms": duration_ms,
        }
        result = self._call_mcp_tool("swipe", args)

        return BoolResult(
            request_id=result.request_id,
            success=result.success,
            data=True if result.success else None,
            error_message="" if result.success else result.error_message
        )

    def click(self, x: int, y: int, button: str = "left") -> BoolResult:
        """
        Clicks on the screen at the specified coordinates.

        Args:
            x (int): X coordinate.
            y (int): Y coordinate.
            button (str, optional): Button type (left, middle, right). Defaults to "left".

        Returns:
            BoolResult: Result object containing success status and error message if any.
        """
        args = {"x": x, "y": y, "button": button}
        result = self._call_mcp_tool("click", args)

        return BoolResult(
            request_id=result.request_id,
            success=result.success,
            data=True if result.success else None,
            error_message="" if result.success else result.error_message
        )

    def screenshot(self) -> OperationResult:
        """
        Takes a screenshot of the current screen using the system_screenshot tool.

        Returns:
            OperationResult: Result object containing the path to the screenshot and error message if any.
        """
        args = {}
        result = self._call_mcp_tool("system_screenshot", args)

        return OperationResult(
            request_id=result.request_id,
            success=result.success,
            data=result.data if result.success else None,
            error_message="" if result.success else result.error_message
        )
