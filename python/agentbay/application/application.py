import json
from typing import Any, Dict, List, Optional

from agentbay.exceptions import ApplicationError, AgentBayError
from agentbay.model import (
    ApiResponse,
    BoolResult,
)
from agentbay.api.base_service import BaseService


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


class ProcessListResult(ApiResponse):
    """Result of operations returning a list of Processes."""

    def __init__(self, request_id: str = "", success: bool = False,
                 data: Optional[List[Process]] = None, error_message: str = ""):
        """
        Initialize a ProcessListResult.

        Args:
            request_id (str, optional): Unique identifier for the API request. Defaults to "".
            success (bool, optional): Whether the operation was successful. Defaults to False.
            data (Optional[List[Process]], optional): The list of process objects. Defaults to None.
            error_message (str, optional): Error message if the operation failed. Defaults to "".
        """
        super().__init__(request_id)
        self.success = success
        self.data = data if data is not None else []
        self.error_message = error_message


class InstalledAppListResult(ApiResponse):
    """Result of operations returning a list of InstalledApps."""

    def __init__(self, request_id: str = "", success: bool = False,
                 data: Optional[List[InstalledApp]] = None, error_message: str = ""):
        """
        Initialize an InstalledAppListResult.

        Args:
            request_id (str, optional): Unique identifier for the API request. Defaults to "".
            success (bool, optional): Whether the operation was successful. Defaults to False.
            data (Optional[List[InstalledApp]], optional): The list of installed app objects. Defaults to None.
            error_message (str, optional): Error message if the operation failed. Defaults to "".
        """
        super().__init__(request_id)
        self.success = success
        self.data = data if data is not None else []
        self.error_message = error_message


class AppInfoResult(ApiResponse):
    """Result of application info operations."""

    def __init__(self, request_id: str = "", success: bool = False,
                 app_info: Optional[Dict[str, Any]] = None, error_message: str = ""):
        """
        Initialize an AppInfoResult.

        Args:
            request_id (str, optional): Unique identifier for the API request. Defaults to "".
            success (bool, optional): Whether the operation was successful. Defaults to False.
            app_info (Dict[str, Any], optional): Application information. Defaults to None.
            error_message (str, optional): Error message if the operation failed. Defaults to "".
        """
        super().__init__(request_id)
        self.success = success
        self.app_info = app_info or {}
        self.error_message = error_message


class AppListResult(ApiResponse):
    """Result of application listing operations."""

    def __init__(self, request_id: str = "", success: bool = False,
                 apps: Optional[List[Dict[str, Any]]] = None, error_message: str = ""):
        """
        Initialize an AppListResult.

        Args:
            request_id (str, optional): Unique identifier for the API request. Defaults to "".
            success (bool, optional): Whether the operation was successful. Defaults to False.
            apps (List[Dict[str, Any]], optional): List of applications. Defaults to None.
            error_message (str, optional): Error message if the operation failed. Defaults to "".
        """
        super().__init__(request_id)
        self.success = success
        self.apps = apps or []
        self.error_message = error_message


class Application(BaseService):
    """
    Handles application operations in the AgentBay cloud environment.
    """

    def _handle_error(self, e):
        """
        Convert AgentBayError to ApplicationError for compatibility.

        Args:
            e (Exception): The exception to convert.

        Returns:
            ApplicationError: The converted exception.
        """
        if isinstance(e, ApplicationError):
            return e
        if isinstance(e, AgentBayError):
            return ApplicationError(str(e))
        return e

    def get_app_info(self, package_name: str) -> AppInfoResult:
        """
        Get information about an application.

        Args:
            package_name: The package name of the application.

        Returns:
            AppInfoResult: Result object containing application info and error message if any.
        """
        args = {"package_name": package_name}

        try:
            result = self._call_mcp_tool("get_app_info", args)
            if result.success:
                try:
                    app_info = json.loads(result.data)
                    return AppInfoResult(request_id=result.request_id, success=True, app_info=app_info)
                except json.JSONDecodeError:
                    return AppInfoResult(request_id=result.request_id, success=False, error_message="Failed to parse app info JSON")
            else:
                return AppInfoResult(request_id=result.request_id, success=False, error_message=result.error_message or "Failed to get app info")
        except ApplicationError as e:
            return AppInfoResult(request_id="", success=False, error_message=str(e))
        except Exception as e:
            return AppInfoResult(request_id="", success=False, error_message=f"Failed to get app info: {e}")

    def list_installed_apps(self) -> AppListResult:
        """
        List all installed applications.

        Returns:
            AppListResult: Result object containing list of applications and error message if any.
        """
        args = {}

        try:
            result = self._call_mcp_tool("list_installed_apps", args)
            if result.success:
                try:
                    apps = json.loads(result.data)
                    return AppListResult(request_id=result.request_id, success=True, apps=apps)
                except json.JSONDecodeError:
                    return AppListResult(request_id=result.request_id, success=False, error_message="Failed to parse app list JSON")
            else:
                return AppListResult(request_id=result.request_id, success=False, error_message=result.error_message or "Failed to list installed apps")
        except ApplicationError as e:
            return AppListResult(request_id="", success=False, error_message=str(e))
        except Exception as e:
            return AppListResult(request_id="", success=False, error_message=f"Failed to list installed apps: {e}")

    def launch_app(self, package_name: str) -> BoolResult:
        """
        Launch an application.

        Args:
            package_name: The package name of the application to launch.

        Returns:
            BoolResult: Result object containing success status and error message if any.
        """
        args = {"package_name": package_name}

        try:
            result = self._call_mcp_tool("launch_app", args)
            if result.success:
                return BoolResult(request_id=result.request_id, success=True, data=True)
            else:
                return BoolResult(request_id=result.request_id, success=False, error_message=result.error_message or "Failed to launch app")
        except ApplicationError as e:
            return BoolResult(request_id="", success=False, error_message=str(e))
        except Exception as e:
            return BoolResult(request_id="", success=False, error_message=f"Failed to launch app: {e}")

    def stop_app(self, package_name: str) -> BoolResult:
        """
        Stop a running application.

        Args:
            package_name: The package name of the application to stop.

        Returns:
            BoolResult: Result object containing success status and error message if any.
        """
        args = {"package_name": package_name}

        try:
            result = self._call_mcp_tool("stop_app", args)
            if result.success:
                return BoolResult(request_id=result.request_id, success=True, data=True)
            else:
                return BoolResult(request_id=result.request_id, success=False, error_message=result.error_message or "Failed to stop app")
        except ApplicationError as e:
            return BoolResult(request_id="", success=False, error_message=str(e))
        except Exception as e:
            return BoolResult(request_id="", success=False, error_message=f"Failed to stop app: {e}")

    def install_app(self, apk_path: str) -> BoolResult:
        """
        Install an application from an APK file.

        Args:
            apk_path: The path to the APK file.

        Returns:
            BoolResult: Result object containing success status and error message if any.
        """
        args = {"apk_path": apk_path}

        try:
            result = self._call_mcp_tool("install_app", args)
            if result.success:
                return BoolResult(request_id=result.request_id, success=True, data=True)
            else:
                return BoolResult(request_id=result.request_id, success=False, error_message=result.error_message or "Failed to install app")
        except ApplicationError as e:
            return BoolResult(request_id="", success=False, error_message=str(e))
        except Exception as e:
            return BoolResult(request_id="", success=False, error_message=f"Failed to install app: {e}")

    def uninstall_app(self, package_name: str) -> BoolResult:
        """
        Uninstall an application.

        Args:
            package_name: The package name of the application to uninstall.

        Returns:
            BoolResult: Result object containing success status and error message if any.
        """
        args = {"package_name": package_name}

        try:
            result = self._call_mcp_tool("uninstall_app", args)
            if result.success:
                return BoolResult(request_id=result.request_id, success=True, data=True)
            else:
                return BoolResult(request_id=result.request_id, success=False, error_message=result.error_message or "Failed to uninstall app")
        except ApplicationError as e:
            return BoolResult(request_id="", success=False, error_message=str(e))
        except Exception as e:
            return BoolResult(request_id="", success=False, error_message=f"Failed to uninstall app: {e}")

    def clear_app_data(self, package_name: str) -> BoolResult:
        """
        Clear an application's data.

        Args:
            package_name: The package name of the application to clear data for.

        Returns:
            BoolResult: Result object containing success status and error message if any.
        """
        args = {"package_name": package_name}

        try:
            result = self._call_mcp_tool("clear_app_data", args)
            if result.success:
                return BoolResult(request_id=result.request_id, success=True, data=True)
            else:
                return BoolResult(request_id=result.request_id, success=False, error_message=result.error_message or "Failed to clear app data")
        except ApplicationError as e:
            return BoolResult(request_id="", success=False, error_message=str(e))
        except Exception as e:
            return BoolResult(request_id="", success=False, error_message=f"Failed to clear app data: {e}")
