"""
Mobile module for mobile device UI automation and configuration.
Handles touch operations, UI element interactions, application management, screenshot capabilities,
and mobile environment configuration operations.
"""

from typing import Any, Dict, List, Optional

from .._common.exceptions import AgentBayError, SessionError
from .._common.logger import get_logger
from .._common.models.response import (
    AdbUrlResult,
    ApiResponse,
    BoolResult,
    OperationResult,
)
from .._common.utils.command_templates import MOBILE_COMMAND_TEMPLATES
from .base_service import AsyncBaseService
from .computer import (
    AppOperationResult,
    InstalledApp,
    InstalledAppListResult,
    Process,
    ProcessListResult,
)

# Initialize logger for this module
_logger = get_logger("mobile")


from .._common.models.mobile import UIElementListResult, KeyCode


def _parse_bounds_rect(bounds: Any) -> Optional[Dict[str, int]]:
    """
    Normalize mobile UI element bounds into a stable dict shape.

    Compatibility notes:
    - Some backends return bounds as a dict: {"left":..,"top":..,"right":..,"bottom":..}
    - Others return bounds as a string like "left,top,right,bottom" or "[0,0][100,100]"

    Returns:
        A dict with keys: left, top, right, bottom, or None if parsing fails.
    """
    if bounds is None:
        return None

    if isinstance(bounds, dict):
        left = bounds.get("left")
        top = bounds.get("top")
        right = bounds.get("right")
        bottom = bounds.get("bottom")
        if all(isinstance(v, int) for v in [left, top, right, bottom]):
            return {"left": left, "top": top, "right": right, "bottom": bottom}
        return None

    if isinstance(bounds, str):
        import re

        nums = re.findall(r"-?\d+", bounds)
        if len(nums) >= 4:
            left, top, right, bottom = (int(nums[0]), int(nums[1]), int(nums[2]), int(nums[3]))
            return {"left": left, "top": top, "right": right, "bottom": bottom}
        return None

    return None


def _augment_bounds_rect(elem: Any) -> Any:
    """
    Add `bounds_rect` to element dicts recursively, keeping `bounds` unchanged.

    Deprecated field:
        - element["bounds"] is deprecated. It may be a string or dict depending on backend.
          Use element["bounds_rect"] (stable dict) instead.
    """
    if not isinstance(elem, dict):
        return elem

    out = dict(elem)
    out["bounds_rect"] = _parse_bounds_rect(out.get("bounds"))

    children = out.get("children")
    if isinstance(children, list):
        out["children"] = [_augment_bounds_rect(c) for c in children]
    return out


class AsyncMobile(AsyncBaseService):
    """
    Handles mobile UI automation operations and configuration in the AgentBay cloud environment.
    Provides comprehensive mobile automation capabilities including touch operations,
    UI element interactions, application management, screenshot capabilities,
    and mobile environment configuration operations.
    """

    def __init__(self, session):
        """
        Initialize a Mobile object.

        Args:
            session: The session object that provides access to the AgentBay API.
        """
        super().__init__(session)

    # Touch Operations
    async def tap(self, x: int, y: int) -> BoolResult:
        """
        Taps on the mobile screen at the specified coordinates.

        Args:
            x (int): X coordinate in pixels.
            y (int): Y coordinate in pixels.

        Returns:
            BoolResult: Object with success status and error message if any.

        Example:
            ```python
            session = (await agent_bay.create(image="mobile_latest")).session
            await session.mobile.tap(500, 800)
            await session.delete()
            ```

        See Also:
            swipe, long_press
        """
        args = {"x": x, "y": y}
        try:
            result = await self.session.call_mcp_tool("tap", args)

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

    async def swipe(
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

        Example:
            ```python
            session = (await agent_bay.create(image="mobile_latest")).session
            await session.mobile.swipe(100, 1000, 100, 200, duration_ms=500)
            await session.delete()
            ```
        """
        args = {
            "start_x": start_x,
            "start_y": start_y,
            "end_x": end_x,
            "end_y": end_y,
            "duration_ms": duration_ms,
        }
        try:
            result = await self.session.call_mcp_tool("swipe", args)

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

    async def input_text(self, text: str) -> BoolResult:
        """
        Inputs text into the active field.

        Args:
            text (str): The text to input.

        Returns:
            BoolResult: Result object containing success status and error message if any.

        Example:
            ```python
            session = (await agent_bay.create(image="mobile_latest")).session
            await session.mobile.input_text("Hello Mobile!")
            await session.delete()
            ```
        """
        args = {"text": text}
        try:
            result = await self.session.call_mcp_tool("input_text", args)

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

    async def send_key(self, key: int) -> BoolResult:
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

        Example:
            ```python
            session = (await agent_bay.create(image="mobile_latest")).session
            await session.mobile.send_key(4)  # Press BACK button
            await session.delete()
            ```
        """
        args = {"key": key}
        try:
            result = await self.session.call_mcp_tool("send_key", args)

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
    async def get_clickable_ui_elements(
        self, timeout_ms: int = 2000
    ) -> UIElementListResult:
        """
        Retrieves all clickable UI elements within the specified timeout.

        Args:
            timeout_ms (int, optional): Timeout in milliseconds. Defaults to 2000.

        Returns:
            UIElementListResult: Result object containing clickable UI elements and
                error message if any.

        Deprecated:
            - Each returned element may include `bounds` from backend which is not stable in type.
              Use `bounds_rect` (dict with left/top/right/bottom) instead.

        Example:
            ```python
            session = (await agent_bay.create(image="mobile_latest")).session
            result = await session.mobile.get_clickable_ui_elements()
            print(f"Found {len(result.elements)} clickable elements")
            await session.delete()
            ```
        """
        args = {"timeout_ms": timeout_ms}
        try:
            result = await self.session.call_mcp_tool("get_clickable_ui_elements", args)
            request_id = result.request_id

            if not result.success:
                return UIElementListResult(
                    request_id=request_id,
                    success=False,
                    elements=None,
                    error_message=result.error_message,
                )

            try:
                import json

                elements = json.loads(result.data)
                if isinstance(elements, list):
                    elements = [_augment_bounds_rect(e) for e in elements]
                return UIElementListResult(
                    request_id=request_id,
                    success=True,
                    elements=elements,
                    error_message="",
                )
            except Exception as e:
                return UIElementListResult(
                    request_id=request_id,
                    success=False,
                    elements=None,
                    error_message=f"Failed to parse clickable UI elements data: {e}",
                )
        except Exception as e:
            return UIElementListResult(
                request_id="",
                success=False,
                elements=None,
                error_message=f"Failed to get clickable UI elements: {str(e)}",
            )

    async def get_all_ui_elements(self, timeout_ms: int = 2000) -> UIElementListResult:
        """
        Retrieves all UI elements within the specified timeout.

        Args:
            timeout_ms (int, optional): Timeout in milliseconds. Defaults to 2000.

        Returns:
            UIElementListResult: Result object containing UI elements and error
                message if any.

        Deprecated:
            - Each returned element may include `bounds` from backend which is not stable in type.
              Use `bounds_rect` (dict with left/top/right/bottom) instead.

        Example:
            ```python
            session = (await agent_bay.create(image="mobile_latest")).session
            result = await session.mobile.get_all_ui_elements()
            print(f"Found {len(result.elements)} UI elements")
            await session.delete()
            ```
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
            raw_bounds = element.get("bounds", "")
            parsed = {
                "bounds": raw_bounds,
                "bounds_rect": _parse_bounds_rect(raw_bounds),
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
            result = await self.session.call_mcp_tool("get_all_ui_elements", args)
            request_id = result.request_id

            if not result.success:
                return UIElementListResult(
                    request_id=request_id,
                    success=False,
                    elements=None,
                    error_message=result.error_message,
                )

            try:
                import json

                elements = json.loads(result.data)
                parsed_elements = [parse_element(element) for element in elements]
                return UIElementListResult(
                    request_id=request_id,
                    success=True,
                    elements=parsed_elements,
                    error_message="",
                )
            except Exception as e:
                return UIElementListResult(
                    request_id=request_id,
                    success=False,
                    elements=None,
                    error_message=f"Failed to parse UI elements data: {e}",
                )
        except Exception as e:
            return UIElementListResult(
                request_id="",
                success=False,
                elements=None,
                error_message=f"Failed to get all UI elements: {str(e)}",
            )

    # Application Management Operations
    async def get_installed_apps(
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

        Example:
            ```python
            session = (await agent_bay.create(image="mobile_latest")).session
            apps = await session.mobile.get_installed_apps(True, False, True)
            print(f"Found {len(apps.data)} apps")
            await session.delete()
            ```
        """
        try:
            args = {
                "start_menu": start_menu,
                "desktop": desktop,
                "ignore_system_apps": ignore_system_apps,
            }

            result = await self.session.call_mcp_tool("get_installed_apps", args)

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
                    app = InstalledApp._from_dict(app_data)
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
            return InstalledAppListResult(success=False, error_message=str(e))

    async def start_app(
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

        Example:
            ```python
            session = (await agent_bay.create(image="mobile_latest")).session
            processes = await session.mobile.start_app("monkey -p com.android.settings 1")
            print(f"Started {len(processes.data)} process(es)")
            await session.delete()
            ```
        """
        try:
            args = {"start_cmd": start_cmd}
            if work_directory:
                args["work_directory"] = work_directory
            if activity:
                args["activity"] = activity

            result = await self.session.call_mcp_tool("start_app", args)

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
                    process = Process._from_dict(process_data)
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

    async def stop_app_by_cmd(self, stop_cmd: str) -> AppOperationResult:
        """
        Stops an application by stop command.

        Args:
            stop_cmd (str): The command to stop the application.

        Returns:
            AppOperationResult: The result of the operation.

        Example:
            ```python
            session = (await agent_bay.create(image="mobile_latest")).session
            result = await session.mobile.stop_app_by_cmd("com.android.settings")
            print(f"Stop successful: {result.success}")
            await session.delete()
            ```
        """
        try:
            args = {"stop_cmd": stop_cmd}
            result = await self.session.call_mcp_tool("stop_app_by_cmd", args)

            return AppOperationResult(
                request_id=result.request_id,
                success=result.success,
                error_message=result.error_message,
            )
        except Exception as e:
            return AppOperationResult(success=False, error_message=str(e))

    # Screenshot Operations
    async def screenshot(self) -> OperationResult:
        """
        Takes a screenshot of the current screen.

        Returns:
            OperationResult: Result object containing the path to the screenshot
                and error message if any.

        Example:
            ```python
            session = (await agent_bay.create(image="mobile_latest")).session
            result = await session.mobile.screenshot()
            print(f"Screenshot URL: {result.data}")
            await session.delete()
            ```
        """
        args = {}
        try:
            result = await self.session.call_mcp_tool("system_screenshot", args)

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

    # Mobile Configuration Operations
    async def configure(self, mobile_config):
        """
        Configure mobile settings from MobileExtraConfig.

        This method is typically called automatically during session creation when
        MobileExtraConfig is provided in CreateSessionParams. It can also be called
        manually to reconfigure mobile settings during a session.

        Args:
            mobile_config (MobileExtraConfig): Mobile configuration object with settings for:
                - lock_resolution (bool): Whether to lock device resolution
                - app_manager_rule (AppManagerRule): App whitelist/blacklist rules
                - hide_navigation_bar (bool): Whether to hide navigation bar
                - uninstall_blacklist (List[str]): Apps protected from uninstallation

        Example:
            ```python
            from agentbay import AsyncAgentBay, CreateSessionParams, MobileExtraConfig
            agent_bay = AsyncAgentBay(api_key="your_api_key")
            result = await agent_bay.create(CreateSessionParams(image_id="mobile_latest"))
            session = result.session
            mobile_config = MobileExtraConfig(lock_resolution=True)
            await session.mobile.configure(mobile_config)
            await agent_bay.delete(session)
            ```

        Note:
            - This method is called automatically during session creation if MobileExtraConfig is provided
            - Configuration changes are applied immediately
            - Resolution lock prevents resolution changes
            - App whitelist/blacklist affects app launching permissions
            - Uninstall blacklist protects apps from being uninstalled

        See Also:
            set_resolution_lock, set_app_whitelist, set_app_blacklist,
            set_navigation_bar_visibility, set_uninstall_blacklist
        """
        if not mobile_config:
            _logger.warning("No mobile configuration provided")
            return

        # Configure resolution lock
        if mobile_config.lock_resolution is not None:
            await self._set_resolution_lock(mobile_config.lock_resolution)

        # Configure app management rules
        if mobile_config.app_manager_rule and mobile_config.app_manager_rule.rule_type:
            app_rule = mobile_config.app_manager_rule
            package_names = app_rule.app_package_name_list or []

            if package_names and app_rule.rule_type in ["White", "Black"]:
                if app_rule.rule_type == "White":
                    await self._set_app_whitelist(package_names)
                else:
                    await self._set_app_blacklist(package_names)
            elif not package_names:
                _logger.warning(
                    f"No package names provided for {app_rule.rule_type} list"
                )

        # Configure navigation bar visibility
        if mobile_config.hide_navigation_bar is not None:
            await self._set_navigation_bar_visibility(mobile_config.hide_navigation_bar)

        # Configure uninstall blacklist
        if (
            mobile_config.uninstall_blacklist
            and len(mobile_config.uninstall_blacklist) > 0
        ):
            await self._set_uninstall_blacklist(mobile_config.uninstall_blacklist)

    async def set_resolution_lock(self, enable: bool):
        """
        Set display resolution lock for mobile devices.

        Args:
            enable (bool): True to enable, False to disable.

        Example:
            ```python
            session = (await agent_bay.create(image="mobile_latest")).session
            await session.mobile.set_resolution_lock(True)
            await session.mobile.set_resolution_lock(False)
            await session.delete()
            ```
        """
        await self._set_resolution_lock(enable)

    async def set_app_whitelist(self, package_names: List[str]):
        """
        Set application whitelist.

        Args:
            package_names (List[str]): List of Android package names to whitelist.

        Example:
            ```python
            session = (await agent_bay.create(image="mobile_latest")).session
            whitelist = ["com.android.settings", "com.android.chrome"]
            await session.mobile.set_app_whitelist(whitelist)
            await session.delete()
            ```

        Notes:
            - Only apps in the whitelist will be allowed to run
            - System apps may be affected depending on the configuration
            - Whitelist takes precedence over blacklist if both are set
        """
        if not package_names:
            _logger.warning("Empty package names list for whitelist")
            return
        await self._set_app_whitelist(package_names)

    async def set_app_blacklist(self, package_names: List[str]):
        """
        Set application blacklist.

        Args:
            package_names (List[str]): List of Android package names to blacklist.

        Example:
            ```python
            session = (await agent_bay.create(image="mobile_latest")).session
            blacklist = ["com.example.app1", "com.example.app2"]
            await session.mobile.set_app_blacklist(blacklist)
            await session.delete()
            ```

        Notes:
            - Apps in the blacklist will be blocked from running
            - Whitelist takes precedence over blacklist if both are set
        """
        if not package_names:
            _logger.warning("Empty package names list for blacklist")
            return
        await self._set_app_blacklist(package_names)

    async def set_navigation_bar_visibility(self, hide: bool):
        """
        Set navigation bar visibility for mobile devices.

        Args:
            hide (bool): True to hide navigation bar, False to show navigation bar.

        Example:
            ```python
            session = (await agent_bay.create(image="mobile_latest")).session
            await session.mobile.set_navigation_bar_visibility(hide=True)
            await session.mobile.set_navigation_bar_visibility(hide=False)
            await session.delete()
            ```

        Notes:
            - Hiding the navigation bar provides a fullscreen experience
            - The navigation bar can still be accessed by swiping from the edge
        """
        await self._set_navigation_bar_visibility(hide)

    async def set_uninstall_blacklist(self, package_names: List[str]):
        """
        Set uninstall protection blacklist for mobile devices.

        Args:
            package_names (List[str]): List of Android package names to protect from uninstallation.

        Example:
            ```python
            session = (await agent_bay.create(image="mobile_latest")).session
            protected_apps = ["com.android.settings", "com.android.chrome"]
            await session.mobile.set_uninstall_blacklist(protected_apps)
            await session.delete()
            ```

        Notes:
            - Apps in the uninstall blacklist cannot be uninstalled
            - This is useful for protecting critical applications
            - The protection persists for the session lifetime
        """
        if not package_names:
            _logger.warning("Empty package names list for uninstall blacklist")
            return
        await self._set_uninstall_blacklist(package_names)

    async def get_adb_url(self, adbkey_pub: str) -> AdbUrlResult:
        """
        Retrieves the ADB connection URL for the mobile environment.

        This method is only supported in mobile environments (mobile_latest image).
        It uses the provided ADB public key to establish the connection and returns
        the ADB connect URL.

        Args:
            adbkey_pub (str): The ADB public key for connection authentication.

        Returns:
            AdbUrlResult: Result object containing the ADB connection URL
                         (format: "adb connect <IP>:<Port>") and request ID.
                         Returns error if not in mobile environment.

        Raises:
            SessionError: If the session is not in mobile environment.

        Example:
            ```python
            session = (await agent_bay.create(image="mobile_latest")).session
            adbkey_pub = "your_adb_public_key"
            adb_result = await session.mobile.get_adb_url(adbkey_pub)
            print(f"ADB URL: {adb_result.data}")
            await session.delete()
            ```
        """
        try:
            # Build options JSON with adbkey_pub
            import json

            from ..api.models import GetAdbLinkRequest

            options_json = json.dumps({"adbkey_pub": adbkey_pub})

            # Call get_adb_link API
            # NOTE: We need to use the async version of the client method here, but it's on session.agent_bay.client
            # The session.agent_bay.client is the sync/async client.
            # In async session, session.agent_bay is AsyncAgentBay, and client is AsyncClient.
            # So we should await the method call.

            request = GetAdbLinkRequest(
                authorization=f"Bearer {self.session.agent_bay.api_key}",
                session_id=self.session.session_id,
                option=options_json,
            )
            response = await self.session.agent_bay.client.get_adb_link_async(request)

            # Check response
            if response.body and response.body.success and response.body.data:
                adb_url = response.body.data.url
                request_id = response.body.request_id or ""
                _logger.info(
                    f"✅ get_adb_url completed successfully. RequestID: {request_id}"
                )
                return AdbUrlResult(
                    request_id=request_id,
                    success=True,
                    data=adb_url,
                    error_message="",
                )
            else:
                error_msg = response.body.message if response.body else "Unknown error"
                request_id = response.body.request_id if response.body else ""
                _logger.error(f"❌ Failed to get ADB URL: {error_msg}")
                return AdbUrlResult(
                    request_id=request_id,
                    success=False,
                    data="",
                    error_message=error_msg,
                )

        except Exception as e:
            error_msg = f"Failed to get ADB URL: {str(e)}"
            _logger.error(f"❌ {error_msg}")
            return AdbUrlResult(
                request_id="",
                success=False,
                data=None,
                error_message=error_msg,
            )

    async def _execute_template_command(
        self, template_name: str, params: Dict[str, Any], operation_name: str
    ):
        """Execute a command using template and parameters."""
        template = MOBILE_COMMAND_TEMPLATES.get(template_name)
        if not template:
            _logger.error(f"Template '{template_name}' not found")
            return

        command = template.format(**params)

        _logger.info(f"Executing {operation_name}")
        # execute_command is async in AsyncCommand
        result = await self.session.command.execute_command(command)

        if result.success:
            _logger.info(f"✅ {operation_name} completed successfully")
        else:
            _logger.error(f"❌ {operation_name} failed: {result.error_message}")

    async def _set_resolution_lock(self, enable: bool):
        """Execute resolution lock command."""
        params = {"lock_switch": 1 if enable else 0}
        operation_name = f"Resolution lock {'enable' if enable else 'disable'}"
        await self._execute_template_command("resolution_lock", params, operation_name)

    async def _set_app_whitelist(self, package_names: List[str]):
        """Execute app whitelist command."""
        params = {
            "package_list": "\n".join(package_names),
            "package_count": len(package_names),
        }
        operation_name = f"App whitelist configuration ({len(package_names)} packages)"
        await self._execute_template_command("app_whitelist", params, operation_name)

    async def _set_app_blacklist(self, package_names: List[str]):
        """Execute app blacklist command."""
        params = {
            "package_list": "\n".join(package_names),
            "package_count": len(package_names),
        }
        operation_name = f"App blacklist configuration ({len(package_names)} packages)"
        await self._execute_template_command("app_blacklist", params, operation_name)

    async def _set_navigation_bar_visibility(self, hide: bool):
        """Execute navigation bar visibility command."""
        template_name = "hide_navigation_bar" if hide else "show_navigation_bar"
        operation_name = f"Navigation bar visibility (hide: {hide})"
        await self._execute_template_command(template_name, {}, operation_name)

    async def _set_uninstall_blacklist(self, package_names: List[str]):
        """Execute uninstall blacklist command."""
        import time

        # Use newline-separated format for uninstall blacklist file content
        params = {
            "package_list": "\n".join(package_names),
            "timestamp": str(int(time.time())),
        }
        operation_name = (
            f"Uninstall blacklist configuration ({len(package_names)} packages)"
        )
        await self._execute_template_command(
            "uninstall_blacklist", params, operation_name
        )
