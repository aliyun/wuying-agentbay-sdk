"""
Mobile module for mobile device UI automation.
Handles touch operations, UI element interactions, application management, and screenshot capabilities.
"""

from typing import List, Optional, Dict, Any

from agentbay.api.base_service import BaseService
from agentbay.exceptions import AgentBayError
from agentbay.model import BoolResult, OperationResult
from agentbay.ui.ui import UIElementListResult
from agentbay.application.application import InstalledAppListResult


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

    # Application Management Operations (delegated to existing application module)
    def get_installed_apps(
        self,
        include_system: bool = False,
        include_user: bool = True,
        include_third_party: bool = True,
    ) -> InstalledAppListResult:
        """
        Gets the list of installed applications.

        Args:
            include_system (bool, optional): Include system applications. Defaults to False.
            include_user (bool, optional): Include user applications. Defaults to True.
            include_third_party (bool, optional): Include third-party applications. Defaults to True.

        Returns:
            InstalledAppsResult: Result object containing list of installed apps and error message if any.
        """
        from agentbay.application import ApplicationManager
        app_manager = ApplicationManager(self.session)
        return app_manager.get_installed_apps(include_system, include_user, include_third_party)

    def start_app(self, app_name: str, activity: Optional[str] = None) -> BoolResult:
        """
        Starts the specified application.

        Args:
            app_name (str): The package name of the application to start.
            activity (Optional[str], optional): Specific activity to start. Defaults to None.

        Returns:
            BoolResult: Result object containing success status and error message if any.
        """
        args = {"app_name": app_name}
        if activity:
            args["activity"] = activity

        try:
            result = self._call_mcp_tool("start_app", args)

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
                error_message=f"Failed to start app: {str(e)}",
            )

    def list_visible_apps(self):
        """
        Lists all visible applications.

        Returns:
            Result object containing list of visible apps and error message if any.
        """
        from agentbay.application import ApplicationManager
        app_manager = ApplicationManager(self.session)
        return app_manager.list_visible_apps()

    def stop_app_by_pname(self, pname: str) -> BoolResult:
        """
        Stops an application by process name.

        Args:
            pname (str): The process name of the application to stop.

        Returns:
            BoolResult: Result object containing success status and error message if any.
        """
        from agentbay.application import ApplicationManager
        app_manager = ApplicationManager(self.session)
        return app_manager.stop_app_by_pname(pname)

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