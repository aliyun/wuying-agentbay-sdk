"""
Mobile module for mobile device UI automation.
Handles touch operations, UI element interactions, application management, and screenshot capabilities.
"""

from typing import List, Optional, Dict, Any

from agentbay.api.base_service import BaseService
from agentbay.exceptions import AgentBayError
from agentbay.model import BoolResult, OperationResult
from agentbay.ui.ui import UIElementListResult
from agentbay.application.application import (
    InstalledAppListResult,
    ProcessListResult,
    AppOperationResult,
    Process,
    InstalledApp,
)


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


class Mobile(BaseService):
    """
    Handles mobile UI automation operations in the AgentBay cloud environment.
    Provides comprehensive mobile automation capabilities including touch operations,
    UI element interactions, application management, and screenshot capabilities.
    """

    def __init__(self, session):
        """
        Initialize a Mobile object.

        Args:
            session: The session object that provides access to the AgentBay API.
        """
        super().__init__(session)

    # Touch Operations
    def tap(self, x: int, y: int) -> BoolResult:
        """
        Taps on the screen at the specified coordinates.

        Args:
            x (int): X coordinate.
            y (int): Y coordinate.

        Returns:
            BoolResult: Result object containing success status and error message if any.
        """
        args = {"x": x, "y": y}
        try:
            result = self._call_mcp_tool("tap", args)

            if not result.success:
                return BoolResult(
                    request_id=result.request_id,
                    success=False,
                    data=None,
                    error_message=result.error_message,
                )

            return BoolResult(
                request_id=result.request_id,
                success=True,
                data=True,
                error_message="",
            )
        except Exception as e:
            return BoolResult(
                request_id="",
                success=False,
                data=None,
                error_message=f"Failed to tap: {str(e)}",
            )

    def swipe(
        self,
        start_x: int,
        start_y: int,
        end_x: int,
        end_y: int,
        duration_ms: int = 300,
    ) -> BoolResult:
        """
        Performs a swipe gesture from one point to another.

        Args:
            start_x (int): Starting X coordinate.
            start_y (int): Starting Y coordinate.
            end_x (int): Ending X coordinate.
            end_y (int): Ending Y coordinate.
            duration_ms (int, optional): Duration of the swipe in milliseconds.
                Defaults to 300.

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
        try:
            result = self._call_mcp_tool("swipe", args)

            if not result.success:
                return BoolResult(
                    request_id=result.request_id,
                    success=False,
                    data=None,
                    error_message=result.error_message,
                )

            return BoolResult(
                request_id=result.request_id,
                success=True,
                data=True,
                error_message="",
            )
        except Exception as e:
            return BoolResult(
                request_id="",
                success=False,
                data=None,
                error_message=f"Failed to perform swipe: {str(e)}",
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
        try:
            result = self._call_mcp_tool("input_text", args)

            if not result.success:
                return BoolResult(
                    request_id=result.request_id,
                    success=False,
                    data=None,
                    error_message=result.error_message,
                )

            return BoolResult(
                request_id=result.request_id,
                success=True,
                data=True,
                error_message="",
            )
        except Exception as e:
            return BoolResult(
                request_id="",
                success=False,
                data=None,
                error_message=f"Failed to input text: {str(e)}",
            )

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
        try:
            result = self._call_mcp_tool("send_key", args)

            if not result.success:
                return BoolResult(
                    request_id=result.request_id,
                    success=False,
                    data=None,
                    error_message=result.error_message,
                )

            return BoolResult(
                request_id=result.request_id,
                success=True,
                data=True,
                error_message="",
            )
        except Exception as e:
            return BoolResult(
                request_id="",
                success=False,
                data=None,
                error_message=f"Failed to send key: {str(e)}",
            )

    # UI Element Operations
    def get_clickable_ui_elements(self, timeout_ms: int = 2000) -> UIElementListResult:
        """
        Retrieves all clickable UI elements within the specified timeout.

        Args:
            timeout_ms (int, optional): Timeout in milliseconds. Defaults to 2000.

        Returns:
            UIElementListResult: Result object containing clickable UI elements and
                error message if any.
        """
        args = {"timeout_ms": timeout_ms}
        try:
            result = self._call_mcp_tool("get_clickable_ui_elements", args)
            request_id = result.request_id

            if not result.success:
                return UIElementListResult(
                    request_id=request_id,
                    success=False,
                    elements=[],
                    error_message=result.error_message,
                )

            elements = result.data if result.data else []
            return UIElementListResult(
                request_id=request_id,
                success=True,
                elements=elements,
                error_message="",
            )
        except Exception as e:
            return UIElementListResult(
                request_id="",
                success=False,
                elements=[],
                error_message=f"Failed to get clickable UI elements: {str(e)}",
            )

    def get_all_ui_elements(self, timeout_ms: int = 2000) -> UIElementListResult:
        """
        Retrieves all UI elements within the specified timeout.

        Args:
            timeout_ms (int, optional): Timeout in milliseconds. Defaults to 2000.

        Returns:
            UIElementListResult: Result object containing all UI elements and
                error message if any.
        """
        args = {"timeout_ms": timeout_ms}
        try:
            result = self._call_mcp_tool("get_all_ui_elements", args)
            request_id = result.request_id

            if not result.success:
                return UIElementListResult(
                    request_id=request_id,
                    success=False,
                    elements=[],
                    error_message=result.error_message,
                )

            elements = result.data if result.data else []
            return UIElementListResult(
                request_id=request_id,
                success=True,
                elements=elements,
                error_message="",
            )
        except Exception as e:
            return UIElementListResult(
                request_id="",
                success=False,
                elements=[],
                error_message=f"Failed to get all UI elements: {str(e)}",
            )

    # Application Management Operations
    def get_installed_apps(
        self, start_menu: bool, desktop: bool, ignore_system_apps: bool
    ) -> InstalledAppListResult:
        """
        Retrieves a list of installed applications.

        Args:
            start_menu (bool): Whether to include start menu applications.
            desktop (bool): Whether to include desktop applications.
            ignore_system_apps (bool): Whether to ignore system applications.

        Returns:
            InstalledAppListResult: The result containing the list of installed
                applications.
        """
        try:
            args = {
                "start_menu": start_menu,
                "desktop": desktop,
                "ignore_system_apps": ignore_system_apps,
            }

            result = self._call_mcp_tool("get_installed_apps", args)

            if not result.success:
                return InstalledAppListResult(
                    request_id=result.request_id,
                    success=False,
                    error_message=result.error_message,
                )

            try:
                import json
                apps_json = json.loads(result.data)
                installed_apps = []

                for app_data in apps_json:
                    app = InstalledApp.from_dict(app_data)
                    installed_apps.append(app)

                return InstalledAppListResult(
                    request_id=result.request_id,
                    success=True,
                    data=installed_apps,
                )
            except json.JSONDecodeError as e:
                return InstalledAppListResult(
                    request_id=result.request_id,
                    success=False,
                    error_message=f"Failed to parse applications JSON: {e}",
                )
        except Exception as e:
            return InstalledAppListResult(
                success=False, error_message=str(e)
            )

    def start_app(
        self, start_cmd: str, work_directory: str = "", activity: str = ""
    ) -> ProcessListResult:
        """
        Starts an application with the given command, optional working directory and
            optional activity.

        Args:
            start_cmd (str): The command to start the application.
            work_directory (str, optional): The working directory for the application.
            activity (str, optional): Activity name to launch (e.g. ".SettingsActivity"
                or "com.package/.Activity"). Defaults to "".

        Returns:
            ProcessListResult: The result containing the list of processes started.
        """
        try:
            args = {"start_cmd": start_cmd}
            if work_directory:
                args["work_directory"] = work_directory
            if activity:
                args["activity"] = activity

            result = self._call_mcp_tool("start_app", args)

            if not result.success:
                return ProcessListResult(
                    request_id=result.request_id,
                    success=False,
                    error_message=result.error_message,
                )

            try:
                import json
                processes_json = json.loads(result.data)
                processes = []

                for process_data in processes_json:
                    process = Process.from_dict(process_data)
                    processes.append(process)

                return ProcessListResult(
                    request_id=result.request_id, success=True, data=processes
                )
            except json.JSONDecodeError as e:
                return ProcessListResult(
                    request_id=result.request_id,
                    success=False,
                    error_message=f"Failed to parse processes JSON: {e}",
                )
        except Exception as e:
            return ProcessListResult(success=False, error_message=str(e))

    def stop_app_by_cmd(self, stop_cmd: str) -> AppOperationResult:
        """
        Stops an application by stop command.

        Args:
            stop_cmd (str): The command to stop the application.

        Returns:
            AppOperationResult: The result of the operation.
        """
        try:
            args = {"stop_cmd": stop_cmd}
            result = self._call_mcp_tool("stop_app_by_cmd", args)

            return AppOperationResult(
                request_id=result.request_id,
                success=result.success,
                error_message=result.error_message,
            )
        except Exception as e:
            return AppOperationResult(success=False, error_message=str(e))

    # Screenshot Operations
    def screenshot(self) -> OperationResult:
        """
        Takes a screenshot of the current screen.

        Returns:
            OperationResult: Result object containing the path to the screenshot
                and error message if any.
        """
        args = {}
        try:
            result = self._call_mcp_tool("system_screenshot", args)

            if not result.success:
                return OperationResult(
                    request_id=result.request_id,
                    success=False,
                    data=None,
                    error_message=result.error_message,
                )

            return OperationResult(
                request_id=result.request_id,
                success=True,
                data=result.data,
                error_message="",
            )
        except Exception as e:
            return OperationResult(
                request_id="",
                success=False,
                data=None,
                error_message=f"Failed to take screenshot: {str(e)}",
            ) 