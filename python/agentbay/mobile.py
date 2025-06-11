import json
from typing import Any, Dict, List, Optional

from agentbay.api.models import CallMcpToolRequest
from agentbay.exceptions import AgentBayError

class KeyCode:
    HOME = 3
    BACK = 4
    VOLUME_UP = 24
    VOLUME_DOWN = 25
    POWER = 26
    MENU = 82


class InstalledApp:
    """
    Represents an installed application.
    """

    def __init__(self, name: str, start_cmd: str, stop_cmd: str = "", work_dir: str = ""):
        self.name = name
        self.start_cmd = start_cmd
        self.stop_cmd = stop_cmd
        self.work_dir = work_dir

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "InstalledApp":
        return cls(
            name=data.get("name", ""),
            start_cmd=data.get("start_cmd", ""),
            stop_cmd=data.get("stop_cmd", ""),
            work_dir=data.get("work_dir", ""),
        )

    def __repr__(self):
        return (
            f"InstalledApp(name='{self.name}', "
            f"start_cmd='{self.start_cmd}', "
            f"stop_cmd='{self.stop_cmd}', "
            f"work_dir='{self.work_dir}')"
        )


class Process:
    """
    Represents a running process.

    Attributes:
        pname (str): The name of the process.
        pid (int): The process ID.
        cmdline (Optional[str]): The command line used to start the process.
    """

    def __init__(self, pname: str, pid: int, cmdline: Optional[str] = None):
        """
        Initialize a Process object.

        Args:
            pname (str): The name of the process.
            pid (int): The process ID.
            cmdline (Optional[str], optional): The command line used to start the process. Defaults to None.
        """
        self.pname = pname
        self.pid = pid
        self.cmdline = cmdline

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Process":
        """
        Create a Process object from a dictionary.

        Args:
            data (Dict[str, Any]): The dictionary containing the process data.

        Returns:
            Process: The created Process object.
        """
        return cls(
            pname=data.get("pname", ""),
            pid=data.get("pid", 0),
            cmdline=data.get("cmdline"),
        )

    def __repr__(self):
        return (
            f"Process(pname='{self.pname}', "
            f"pid={self.pid}, "
            f"cmdline='{self.cmdline}')"
        )


class MobileSystem:
    """
    Handles mobile system operations in the AgentBay cloud environment.
    """

    def __init__(self, session):
        """
        Initialize a MobileSystem object.

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
            print(f"Calling MCP tool {name} with args: {args_json}")

            response = self.session.get_client().call_mcp_tool(request)
            response_map = response.to_map()
            print(f"Response from MCP tool {name}: {response_map}")
            if not response_map:
                raise AgentBayError("Invalid response format")

            body = response_map.get("body", {})
            print(f"Body: {body}")
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
            if body.get("Data", {}).get("isError", True):
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

            # Extract text field from the first content item
            content_item = content[0]
            json_text = content_item.get("text")

            # Return the JSON text
            return json_text
        except Exception as e:
            raise AgentBayError(f"{e}")

    def get_installed_apps(
        self,
        start_menu: bool = True,
        desktop: bool = False,
        ignore_system_apps: bool = True,
    ) -> List[InstalledApp]:
        """
        Retrieves a list of installed applications.

        Args:
            start_menu (bool, optional): Whether to include applications from the start menu. Defaults to True.
            desktop (bool, optional): Whether to include applications from the desktop. Defaults to False.
            ignore_system_apps (bool, optional): Whether to ignore system applications. Defaults to True.

        Returns:
            List[InstalledApp]: A list of installed applications.

        Raises:
            AgentBayError: If the operation fails.
        """
        args = {
            "start_menu": start_menu,
            "desktop": desktop,
            "ignore_system_app": ignore_system_apps,
        }

        try:
            result = self._call_mcp_tool("get_installed_apps", args)
            apps_data = json.loads(result)
            if not isinstance(apps_data, list):
                raise AgentBayError("Invalid apps data format")

            # return installed_apps
            return [InstalledApp.from_dict(app_data) for app_data in apps_data]
        except AgentBayError:
            raise
        except Exception as e:
            raise AgentBayError(f"Failed to get installed apps: {e}")

    def start_app(self, start_cmd: str, work_directory: str = "") -> List[Process]:
        """
        Starts an application with the given command and optional working directory.

        Args:
            start_cmd (str): The command to start the application.
            work_directory (str, optional): The working directory for the application. Defaults to "".

        Returns:
            List[Process]: A list of processes started.

        Raises:
            AgentBayError: If the operation fails.
        """
        args = {"start_cmd": start_cmd}

        if work_directory:
            args["work_directory"] = work_directory

        try:
            result = self._call_mcp_tool("start_app", args)
            print(f"Result from start_app: {result}")
            process_list = json.loads(result)

            if not isinstance(process_list, list):
                raise AgentBayError("Invalid response format from start_app")

            return [Process.from_dict(process) for process in process_list]
        except AgentBayError:
            raise
        except Exception as e:
            raise AgentBayError(f"Failed to start app: {e}")

    def stop_app_by_cmd(self, stop_cmd: str) -> None:
        """
        Stops an application using the provided stop command.

        Args:
            stop_cmd (str): The command to stop the application.

        Raises:
            AgentBayError: If the operation fails.
        """
        args = {"stop_cmd": stop_cmd}

        try:
            self._call_mcp_tool("stop_app_by_cmd", args)
        except AgentBayError:
            raise
        except Exception as e:
            raise AgentBayError(f"Failed to stop app: {e}")

    def get_clickable_ui_elements(self, timeout_ms: int = 1000) -> List[Dict[str, Any]]:
        """
        Retrieves all clickable UI elements within the specified timeout.

        Args:
            timeout_ms (int, optional): Timeout in milliseconds. Defaults to 1000.

        Returns:
            List[Dict[str, Any]]: A list of clickable UI elements.

        Raises:
            AgentBayError: If the operation fails.
        """
        args = {"timeout_ms": timeout_ms}

        try:
            result = self._call_mcp_tool("get_clickable_ui_elements", args)
            print(f"Result from get_clickable_ui_elements: {result}")
            elements = json.loads(result)
            return elements
        except AgentBayError:
            raise
        except Exception as e:
            raise AgentBayError(f"Failed to get clickable UI elements: {e}")

    def get_all_ui_elements(self, timeout_ms: int = 1000) -> List[Dict[str, Any]]:
        """
        Retrieves all UI elements within the specified timeout.

        Args:
            timeout_ms (int, optional): Timeout in milliseconds. Defaults to 1000.

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

            # Recursively parse children if present
            children = element.get("children", [])
            if children:
                parsed["children"] = [parse_element(child) for child in children]
            else:
                parsed["children"] = []

            return parsed

        try:
            result = self._call_mcp_tool("get_all_ui_elements", args)
            elements = json.loads(result)
            print(f"Result from get_all_ui_elements: {elements}")
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

        Raises:
            AgentBayError: If the operation fails.
        """
        args = {"key": key}

        try:
            result = self._call_mcp_tool("send_key", args)
            print(f"Result from send_key: {result}")
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
