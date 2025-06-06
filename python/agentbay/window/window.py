import json
from typing import Dict, List, Optional, Any, Union
from agentbay.exceptions import AgentBayError
from agentbay.api.models import CallMcpToolRequest


class Window:
    """
    Represents a window in the system.

    Attributes:
        window_id (int): The ID of the window.
        title (str): The title of the window.
        absolute_upper_left_x (Optional[int]): The x-coordinate of the upper left corner of the window.
        absolute_upper_left_y (Optional[int]): The y-coordinate of the upper left corner of the window.
        width (Optional[int]): The width of the window.
        height (Optional[int]): The height of the window.
        pid (Optional[int]): The process ID of the window.
        pname (Optional[str]): The process name of the window.
        child_windows (List['Window']): The child windows of this window.
    """

    def __init__(
        self,
        window_id: int,
        title: str,
        absolute_upper_left_x: Optional[int] = None,
        absolute_upper_left_y: Optional[int] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        pid: Optional[int] = None,
        pname: Optional[str] = None,
        child_windows: Optional[List['Window']] = None
    ):
        """
        Initialize a Window object.

        Args:
            window_id (int): The ID of the window.
            title (str): The title of the window.
            absolute_upper_left_x (Optional[int], optional): The x-coordinate of the upper left corner of the window. Defaults to None.
            absolute_upper_left_y (Optional[int], optional): The y-coordinate of the upper left corner of the window. Defaults to None.
            width (Optional[int], optional): The width of the window. Defaults to None.
            height (Optional[int], optional): The height of the window. Defaults to None.
            pid (Optional[int], optional): The process ID of the window. Defaults to None.
            pname (Optional[str], optional): The process name of the window. Defaults to None.
            child_windows (Optional[List['Window']], optional): The child windows of this window. Defaults to None.
        """
        self.window_id = window_id
        self.title = title
        self.absolute_upper_left_x = absolute_upper_left_x
        self.absolute_upper_left_y = absolute_upper_left_y
        self.width = width
        self.height = height
        self.pid = pid
        self.pname = pname
        self.child_windows = child_windows or []

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Window':
        """
        Create a Window object from a dictionary.

        Args:
            data (Dict[str, Any]): The dictionary containing the window data.

        Returns:
            Window: The created Window object.
        """
        child_windows = []
        if 'child_windows' in data and data['child_windows']:
            child_windows = [cls.from_dict(child) for child in data['child_windows']]

        return cls(
            window_id=data.get('window_id', 0),
            title=data.get('title', ''),
            absolute_upper_left_x=data.get('absolute_upper_left_x'),
            absolute_upper_left_y=data.get('absolute_upper_left_y'),
            width=data.get('width'),
            height=data.get('height'),
            pid=data.get('pid'),
            pname=data.get('pname'),
            child_windows=child_windows
        )


class WindowManager:
    """
    Handles window management operations in the AgentBay cloud environment.
    """

    def __init__(self, session):
        """
        Initialize a WindowManager object.

        Args:
            session: The session object that provides access to the AgentBay API.
        """
        self.session = session

    def _call_mcp_tool(self, name: str, args: Dict[str, Any]) -> Any:
        """
        Call an MCP tool with the given name and arguments.

        Args:
            name (str): The name of the tool to call.
            args (Dict[str, Any]): The arguments to pass to the tool.

        Returns:
            Any: The response from the tool.

        Raises:
            AgentBayError: If the tool call fails.
        """
        try:
            args_json = json.dumps(args)
            request = CallMcpToolRequest(
                authorization=f"Bearer {self.session.get_api_key()}",
                session_id=self.session.get_session_id(),
                name=name,
                args=args_json
            )

            response = self.session.get_client().call_mcp_tool(request)

            # Parse the response
            response_map = response.to_map()
            if not response_map:
                raise AgentBayError(f"Invalid response format")

            body = response_map.get("body", {})
            if not body:
                raise AgentBayError(f"Invalid response body")

            if body.get("Data", {}).get("isError", False):
                error_content = body.get("Data", {}).get("content", "Unknown error")
                error_message = "; ".join(item.get("text", "") for item in error_content if isinstance(item, dict))
                raise AgentBayError(f"{error_message}")

            response_data = body.get("Data", {})
            if not response_data:
                raise AgentBayError(f"No data field in response ")

            # Extract content array
            content = response_data.get("content", [])
            if not content or len(content) == 0:
                raise AgentBayError(f"Invalid or empty content array in response")

            # Extract text field from the first content item
            content_item = content[0]
            json_text = content_item.get("text")
            if not json_text:
                raise AgentBayError(f"Text field not found or not a string in response")

            # Parse the JSON text
            return json.loads(json_text)
        except Exception as e:
            raise AgentBayError(f"Failed to call MCP tool {name}: {e}")

    def get_window_info_by_pname(self, pname: str) -> List[Window]:
        """
        Gets detailed window information for a process by name.

        Args:
            pname (str): The name of the process.

        Returns:
            List[Window]: A list of windows for the process.

        Raises:
            AgentBayError: If the operation fails.
        """
        args = {
            "pname": pname
        }

        try:
            result = self._call_mcp_tool("get_window_info_by_pname", args)
            return [Window.from_dict(window) for window in result]
        except Exception as e:
            raise AgentBayError(f"Failed to get window info by pname: {e}")

    def get_window_info_by_pid(self, pid: int) -> List[Window]:
        """
        Gets detailed window information for a process by ID.

        Args:
            pid (int): The ID of the process.

        Returns:
            List[Window]: A list of windows for the process.

        Raises:
            AgentBayError: If the operation fails.
        """
        args = {
            "pid": pid
        }

        try:
            result = self._call_mcp_tool("get_window_info_by_pid", args)
            return [Window.from_dict(window) for window in result]
        except Exception as e:
            raise AgentBayError(f"Failed to get window info by pid: {e}")

    def list_root_windows(self) -> List[Window]:
        """
        Lists all root windows in the system.

        Returns:
            List[Window]: A list of root windows.

        Raises:
            AgentBayError: If the operation fails.
        """
        args = {}

        try:
            result = self._call_mcp_tool("list_root_windows", args)
            return [Window.from_dict(window) for window in result]
        except Exception as e:
            raise AgentBayError(f"Failed to list root windows: {e}")

    def get_active_window(self) -> Window:
        """
        Gets the currently active window.

        Returns:
            Window: The active window.

        Raises:
            AgentBayError: If the operation fails.
        """
        args = {}

        try:
            result = self._call_mcp_tool("get_active_window", args)
            return Window.from_dict(result)
        except Exception as e:
            raise AgentBayError(f"Failed to get active window: {e}")

    def activate_window(self, window_id: int) -> None:
        """
        Activates a window by ID.

        Args:
            window_id (int): The ID of the window to activate.

        Raises:
            AgentBayError: If the operation fails.
        """
        args = {
            "window_id": window_id
        }

        try:
            self._call_mcp_tool("activate_window", args)
        except Exception as e:
            raise AgentBayError(f"Failed to activate window: {e}")

    def maximize_window(self, window_id: int) -> None:
        """
        Maximizes a window by ID.

        Args:
            window_id (int): The ID of the window to maximize.

        Raises:
            AgentBayError: If the operation fails.
        """
        args = {
            "window_id": window_id
        }

        try:
            self._call_mcp_tool("maximize_window", args)
        except Exception as e:
            raise AgentBayError(f"Failed to maximize window: {e}")

    def minimize_window(self, window_id: int) -> None:
        """
        Minimizes a window by ID.

        Args:
            window_id (int): The ID of the window to minimize.

        Raises:
            AgentBayError: If the operation fails.
        """
        args = {
            "window_id": window_id
        }

        try:
            self._call_mcp_tool("minimize_window", args)
        except Exception as e:
            raise AgentBayError(f"Failed to minimize window: {e}")

    def restore_window(self, window_id: int) -> None:
        """
        Restores a window by ID.

        Args:
            window_id (int): The ID of the window to restore.

        Raises:
            AgentBayError: If the operation fails.
        """
        args = {
            "window_id": window_id
        }

        try:
            self._call_mcp_tool("restore_window", args)
        except Exception as e:
            raise AgentBayError(f"Failed to restore window: {e}")

    def close_window(self, window_id: int) -> None:
        """
        Closes a window by ID.

        Args:
            window_id (int): The ID of the window to close.

        Raises:
            AgentBayError: If the operation fails.
        """
        args = {
            "window_id": window_id
        }

        try:
            self._call_mcp_tool("close_window", args)
        except Exception as e:
            raise AgentBayError(f"Failed to close window: {e}")

    def fullscreen_window(self, window_id: int) -> None:
        """
        Toggles fullscreen mode for a window by ID.

        Args:
            window_id (int): The ID of the window to toggle fullscreen for.

        Raises:
            AgentBayError: If the operation fails.
        """
        args = {
            "window_id": window_id
        }

        try:
            self._call_mcp_tool("fullscreen_window", args)
        except Exception as e:
            raise AgentBayError(f"Failed to fullscreen window: {e}")

    def resize_window(self, window_id: int, width: int, height: int) -> None:
        """
        Resizes a window by ID.

        Args:
            window_id (int): The ID of the window to resize.
            width (int): The new width of the window.
            height (int): The new height of the window.

        Raises:
            AgentBayError: If the operation fails.
        """
        args = {
            "window_id": window_id,
            "width": width,
            "height": height
        }

        try:
            self._call_mcp_tool("resize_window", args)
        except Exception as e:
            raise AgentBayError(f"Failed to resize window: {e}")

    def focus_mode(self, on: bool) -> None:
        """
        Enables or disables focus mode.

        Args:
            on (bool): Whether to enable focus mode.

        Raises:
            AgentBayError: If the operation fails.
        """
        args = {
            "on": on
        }

        try:
            self._call_mcp_tool("focus_mode", args)
        except Exception as e:
            raise AgentBayError(f"Failed to set focus mode: {e}")
