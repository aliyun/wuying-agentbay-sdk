import json
from typing import Any, Dict, List, Optional

from agentbay.api.models import CallMcpToolRequest
from agentbay.exceptions import AgentBayError


class InstalledApp:
    """
    Represents an installed application.

    Attributes:
        name (str): The name of the application.
        start_cmd (str): The command to start the application.
        stop_cmd (Optional[str]): The command to stop the application.
        work_directory (Optional[str]): The working directory for the application.
    """

    def __init__(
        self,
        name: str,
        start_cmd: str,
        stop_cmd: Optional[str] = None,
        work_directory: Optional[str] = None,
    ):
        """
        Initialize an InstalledApp object.

        Args:
            name (str): The name of the application.
            start_cmd (str): The command to start the application.
            stop_cmd (Optional[str], optional): The command to stop the application. Defaults to None.
            work_directory (Optional[str], optional): The working directory for the application. Defaults to None.
        """
        self.name = name
        self.start_cmd = start_cmd
        self.stop_cmd = stop_cmd
        self.work_directory = work_directory

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "InstalledApp":
        """
        Create an InstalledApp object from a dictionary.

        Args:
            data (Dict[str, Any]): The dictionary containing the application data.

        Returns:
            InstalledApp: The created InstalledApp object.
        """
        return cls(
            name=data.get("name", ""),
            start_cmd=data.get("start_cmd", ""),
            stop_cmd=data.get("stop_cmd"),
            work_directory=data.get("work_directory"),
        )

    def __repr__(self):
        return (
            f"InstalledApp(name='{self.name}', "
            f"start_cmd='{self.start_cmd}', "
            f"stop_cmd='{self.stop_cmd}', "
            f"work_directory='{self.work_directory}')"
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


class ApplicationManager:
    """
    Handles application management operations in the AgentBay cloud environment.
    """

    def __init__(self, session):
        """
        Initialize an ApplicationManager object.

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
            Dict[str, Any]: The response from the tool.

        Raises:
            AgentBayError: If the tool call fails.
        """
        try:
            args_json = json.dumps(args)
            request = CallMcpToolRequest(
                authorization=f"Bearer {self.session.get_api_key()}",
                session_id=self.session.get_session_id(),
                name=name,
                args=args_json,
            )

            response = self.session.get_client().call_mcp_tool(request)

            # Parse the response
            response_map = response.to_map()
            if not response_map:
                raise AgentBayError(f"Invalid response format")

            body = response_map.get("body", {})
            if not body:
                raise AgentBayError(f"Invalid response body")

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
        desktop: bool = True,
        ignore_system_apps: bool = True,
    ) -> List[InstalledApp]:
        """
        Retrieves a list of installed applications.

        Args:
            start_menu (bool, optional): Whether to include applications from the start menu. Defaults to True.
            desktop (bool, optional): Whether to include applications from the desktop. Defaults to True.
            ignore_system_apps (bool, optional): Whether to ignore system applications. Defaults to True.

        Returns:
            List[InstalledApp]: A list of installed applications.

        Raises:
            AgentBayError: If the operation fails.
        """
        args = {
            "start_menu": start_menu,
            "desktop": desktop,
            "ignore_system_apps": ignore_system_apps,
        }

        try:
            result = self._call_mcp_tool("get_installed_apps", args)
            apps_data = json.loads(result)
            if not isinstance(apps_data, list):
                raise AgentBayError("Invalid apps data format")

            # return installed_apps
            return [InstalledApp.from_dict(app) for app in apps_data]
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
            process_list = json.loads(result)

            if not isinstance(process_list, list):
                raise AgentBayError("Invalid response format from start_app")

            return [Process.from_dict(process) for process in process_list]
        except AgentBayError:
            raise
        except Exception as e:
            raise AgentBayError(f"Failed to start app: {e}")

    def stop_app_by_pname(self, pname: str) -> None:
        """
        Stops an application by process name.

        Args:
            pname (str): The name of the process to stop.

        Raises:
            AgentBayError: If the operation fails.
        """
        args = {"pname": pname}

        try:
            self._call_mcp_tool("stop_app_by_pname", args)

        except AgentBayError:
            raise
        except Exception as e:
            raise AgentBayError(f"Failed to stop app by pname: {e}")

    def stop_app_by_pid(self, pid: int) -> None:
        """
        Stops an application by process ID.

        Args:
            pid (int): The ID of the process to stop.

        Raises:
            AgentBayError: If the operation fails.
        """
        args = {"pid": pid}

        try:
            self._call_mcp_tool("stop_app_by_pid", args)
        except AgentBayError:
            raise
        except Exception as e:
            raise AgentBayError(f"Failed to stop app by pid: {e}")

    def stop_app_by_cmd(self, stop_cmd: str) -> None:
        """
        Stops an application by stop command.

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
            raise AgentBayError(f"Failed to stop app by command: {e}")

    def list_visible_apps(self) -> List[Process]:
        """
        Lists all currently visible applications.

        Returns:
            List[Process]: A list of visible processes.

        Raises:
            AgentBayError: If the operation fails.
        """
        args = {}

        try:
            result = self._call_mcp_tool("list_visible_apps", args)
            process_list = json.loads(result)
            if not isinstance(process_list, list):
                raise AgentBayError("Invalid apps data format")

            # return installed_apps
            return [Process.from_dict(process) for process in process_list]
        except AgentBayError:
            raise
        except Exception as e:
            raise AgentBayError(f"Failed to list visible apps: {e}")
