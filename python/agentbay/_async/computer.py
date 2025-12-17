"""
Computer module for desktop UI automation.
Handles mouse operations, keyboard operations, window management,
application management, and screen operations.
"""

import json
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from .._common.exceptions import AgentBayError
from .._common.models.computer import (
    AppOperationResult,
    InstalledApp,
    InstalledAppListResult,
    MouseButton,
    Process,
    ProcessListResult,
    ScrollDirection,
    Window,
    WindowInfoResult,
    WindowListResult,
)
from .._common.models.response import ApiResponse, BoolResult, OperationResult
from .base_service import AsyncBaseService


class AsyncComputer(AsyncBaseService):
    """
    Handles computer UI automation operations in the AgentBay cloud environment.
    Provides comprehensive desktop automation capabilities including mouse, keyboard,
    window management, application management, and screen operations.
    """

    def __init__(self, session):
        """
        Initialize a Computer object.

        Args:
            session: The session object that provides access to the AgentBay API.
        """
        super().__init__(session)

    # Mouse Operations
    async def click_mouse(
        self, x: int, y: int, button: Union[MouseButton, str] = MouseButton.LEFT
    ) -> BoolResult:
        """
        Clicks the mouse at the specified screen coordinates.

        Args:
            x (int): X coordinate in pixels (0 is left edge of screen).
            y (int): Y coordinate in pixels (0 is top edge of screen).
            button (Union[MouseButton, str], optional): Mouse button to click. Options:
                - MouseButton.LEFT or "left": Single left click
                - MouseButton.RIGHT or "right": Right click (context menu)
                - MouseButton.MIDDLE or "middle": Middle click (scroll wheel)
                - MouseButton.DOUBLE_LEFT or "double_left": Double left click
                Defaults to MouseButton.LEFT.

        Returns:
            BoolResult: Object containing:
                - success (bool): Whether the click succeeded
                - data (bool): True if successful, None otherwise
                - error_message (str): Error description if failed

        Raises:
            ValueError: If button is not one of the valid options.

        Behavior:
            - Clicks at the exact pixel coordinates provided
            - Does not move the mouse cursor before clicking
            - For double-click, use MouseButton.DOUBLE_LEFT
            - Right-click typically opens context menus

        Example:
            ```python
            session = await agent_bay.create().session
            await session.computer.click_mouse(100, 200)
            await session.computer.click_mouse(300, 400, MouseButton.RIGHT)
            await session.delete()
            ```

        Note:
            - Coordinates are absolute screen positions, not relative to windows
            - Use `get_screen_size()` to determine valid coordinate ranges
            - Consider using `move_mouse()` first if you need to see cursor movement
            - For UI automation, consider using higher-level methods from `ui` module

        See Also:
            move_mouse, drag_mouse, get_cursor_position, get_screen_size
        """
        button_str = button.value if isinstance(button, MouseButton) else button
        valid_buttons = [b.value for b in MouseButton]
        if button_str not in valid_buttons:
            raise ValueError(
                f"Invalid button '{button_str}'. Must be one of {valid_buttons}"
            )

        args = {"x": x, "y": y, "button": button_str}
        try:
            result = await self.session.call_mcp_tool("click_mouse", args)

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
                error_message=f"Failed to click mouse: {str(e)}",
            )

    async def move_mouse(self, x: int, y: int) -> BoolResult:
        """
        Moves the mouse to the specified coordinates.

        Args:
            x (int): X coordinate.
            y (int): Y coordinate.

        Returns:
            BoolResult: Result object containing success status and error message if any.

        Example:
            ```python
            session = await agent_bay.create().session
            await session.computer.move_mouse(500, 300)
            position = await session.computer.get_cursor_position()
            print(f"Cursor at: {position.data}")
            await session.delete()
            ```

        Note:
            - Moves the cursor smoothly to the target position
            - Does not click after moving
            - Use get_cursor_position() to verify the new position

        See Also:
            click_mouse, drag_mouse, get_cursor_position
        """
        args = {"x": x, "y": y}
        try:
            result = await self.session.call_mcp_tool("move_mouse", args)

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
                error_message=f"Failed to move mouse: {str(e)}",
            )

    async def drag_mouse(
        self,
        from_x: int,
        from_y: int,
        to_x: int,
        to_y: int,
        button: Union[MouseButton, str] = MouseButton.LEFT,
    ) -> BoolResult:
        """
        Drags the mouse from one point to another.

        Args:
            from_x (int): Starting X coordinate.
            from_y (int): Starting Y coordinate.
            to_x (int): Ending X coordinate.
            to_y (int): Ending Y coordinate.
            button (Union[MouseButton, str], optional): Button type. Can be MouseButton enum or string.
                Valid values: MouseButton.LEFT, MouseButton.RIGHT, MouseButton.MIDDLE
                or their string equivalents. Defaults to MouseButton.LEFT.
                Note: DOUBLE_LEFT is not supported for drag operations.

        Returns:
            BoolResult: Result object containing success status and error message if any.

        Raises:
            ValueError: If button is not a valid option.

        Example:
            ```python
            session = await agent_bay.create().session
            await session.computer.drag_mouse(100, 100, 300, 300)
            await session.computer.drag_mouse(200, 200, 400, 400, MouseButton.RIGHT)
            await session.delete()
            ```

        Note:
            - Performs a click-and-drag operation from start to end coordinates
            - Useful for selecting text, moving windows, or drawing
            - DOUBLE_LEFT button is not supported for drag operations
            - Use LEFT, RIGHT, or MIDDLE button only

        See Also:
            click_mouse, move_mouse
        """
        button_str = button.value if isinstance(button, MouseButton) else button
        valid_buttons = ["left", "right", "middle"]
        if button_str not in valid_buttons:
            raise ValueError(
                f"Invalid button '{button_str}'. Must be one of {valid_buttons}"
            )

        args = {
            "from_x": from_x,
            "from_y": from_y,
            "to_x": to_x,
            "to_y": to_y,
            "button": button_str,
        }
        try:
            result = await self.session.call_mcp_tool("drag_mouse", args)

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
                error_message=f"Failed to drag mouse: {str(e)}",
            )

    async def scroll(
        self,
        x: int,
        y: int,
        direction: Union[ScrollDirection, str] = ScrollDirection.UP,
        amount: int = 1,
    ) -> BoolResult:
        """
        Scrolls the mouse wheel at the specified coordinates.

        Args:
            x (int): X coordinate.
            y (int): Y coordinate.
            direction (Union[ScrollDirection, str], optional): Scroll direction. Can be ScrollDirection enum or string.
                Valid values: ScrollDirection.UP, ScrollDirection.DOWN, ScrollDirection.LEFT, ScrollDirection.RIGHT
                or their string equivalents. Defaults to ScrollDirection.UP.
            amount (int, optional): Scroll amount. Defaults to 1.

        Returns:
            BoolResult: Result object containing success status and error message if any.

        Raises:
            ValueError: If direction is not a valid option.

        Example:
            ```python
            session = await agent_bay.create().session
            await session.computer.scroll(500, 500, ScrollDirection.DOWN, 3)
            await session.computer.scroll(500, 500, ScrollDirection.UP, 2)
            await session.delete()
            ```

        Note:
            - Scroll operations are performed at the specified coordinates
            - The amount parameter controls how many scroll units to move
            - Larger amounts result in faster scrolling
            - Useful for navigating long documents or web pages

        See Also:
            click_mouse, move_mouse
        """
        direction_str = (
            direction.value if isinstance(direction, ScrollDirection) else direction
        )
        valid_directions = [d.value for d in ScrollDirection]
        if direction_str not in valid_directions:
            raise ValueError(
                f"Invalid direction '{direction_str}'. Must be one of {valid_directions}"
            )

        args = {"x": x, "y": y, "direction": direction_str, "amount": amount}
        try:
            result = await self.session.call_mcp_tool("scroll", args)

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
                error_message=f"Failed to scroll: {str(e)}",
            )

    async def get_cursor_position(self) -> OperationResult:
        """
        Gets the current cursor position.

        Returns:
            OperationResult: Result object containing cursor position data
                with keys 'x' and 'y', and error message if any.

        Example:
            ```python
            session = await agent_bay.create().session
            await session.computer.move_mouse(800, 600)
            position = await session.computer.get_cursor_position()
            print(f"Cursor is at x={position.data['x']}, y={position.data['y']}")
            await session.delete()
            ```

        Note:
            - Returns the absolute screen coordinates
            - Useful for verifying mouse movements
            - Position is in pixels from top-left corner (0, 0)

        See Also:
            move_mouse, click_mouse, get_screen_size
        """
        args = {}
        try:
            result = await self.session.call_mcp_tool("get_cursor_position", args)

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
                error_message=f"Failed to get cursor position: {str(e)}",
            )

    # Keyboard Operations
    async def input_text(self, text: str) -> BoolResult:
        """
        Types text into the currently focused input field.

        Args:
            text (str): The text to input. Supports Unicode characters.

        Returns:
            BoolResult: Object with success status and error message if any.

        Example:
            ```python
            session = await agent_bay.create().session
            await session.computer.click_mouse(500, 300)
            await session.computer.input_text("Hello, World!")
            await session.delete()
            ```

        Note:
            - Requires an input field to be focused first
            - Use click_mouse() or UI automation to focus the field
            - Supports special characters and Unicode

        See Also:
            press_keys, click_mouse
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

    async def press_keys(self, keys: List[str], hold: bool = False) -> BoolResult:
        """
        Presses the specified keys.

        Args:
            keys (List[str]): List of keys to press (e.g., ["Ctrl", "a"]).
            hold (bool, optional): Whether to hold the keys. Defaults to False.

        Returns:
            BoolResult: Result object containing success status and error message if any.

        Example:
            ```python
            session = await agent_bay.create().session
            await session.computer.press_keys(["Ctrl", "c"])
            await session.computer.press_keys(["Ctrl", "v"])
            await session.delete()
            ```

        Note:
            - Key names are case-sensitive
            - When hold=True, remember to call release_keys() afterwards
            - Supports modifier keys like Ctrl, Alt, Shift
            - Can press multiple keys simultaneously for shortcuts

        See Also:
            release_keys, input_text
        """
        args = {"keys": keys, "hold": hold}
        try:
            result = await self.session.call_mcp_tool("press_keys", args)

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
                error_message=f"Failed to press keys: {str(e)}",
            )

    async def release_keys(self, keys: List[str]) -> BoolResult:
        """
        Releases the specified keys.

        Args:
            keys (List[str]): List of keys to release (e.g., ["Ctrl", "a"]).

        Returns:
            BoolResult: Result object containing success status and error message if any.

        Example:
            ```python
            session = await agent_bay.create().session
            await session.computer.press_keys(["Shift"], hold=True)
            await session.computer.input_text("hello")
            await session.computer.release_keys(["Shift"])
            await session.delete()
            ```

        Note:
            - Should be used after press_keys() with hold=True
            - Key names are case-sensitive
            - Releases all keys specified in the list

        See Also:
            press_keys, input_text
        """
        args = {"keys": keys}
        try:
            result = await self.session.call_mcp_tool("release_keys", args)

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
                error_message=f"Failed to release keys: {str(e)}",
            )

    # Screen Operations
    async def get_screen_size(self) -> OperationResult:
        """
        Gets the screen size and DPI scaling factor.

        Returns:
            OperationResult: Result object containing screen size data
                with keys 'width', 'height', and 'dpiScalingFactor',
                and error message if any.

        Example:
            ```python
            result = await agent_bay.create()
            session = result.session
            size = await session.computer.get_screen_size()
            print(
                f"Screen: {size.data['width']}x{size.data['height']}, DPI: {size.data['dpiScalingFactor']}"
            )
            await session.delete()
            ```

        Note:
            - Returns the full screen dimensions in pixels
            - DPI scaling factor affects coordinate calculations on high-DPI displays
            - Use this to determine valid coordinate ranges for mouse operations

        See Also:
            click_mouse, move_mouse, screenshot
        """
        args = {}
        try:
            result = await self.session.call_mcp_tool("get_screen_size", args)

            if not result.success:
                return OperationResult(
                    request_id=result.request_id,
                    success=False,
                    data=None,
                    error_message=result.error_message,
                )

            data = result.data
            if isinstance(data, str) and data:
                try:
                    data = json.loads(data)
                except json.JSONDecodeError as e:
                    return OperationResult(
                        request_id=result.request_id,
                        success=False,
                        data=None,
                        error_message=f"Failed to parse screen size JSON: {e}",
                    )

            return OperationResult(
                request_id=result.request_id,
                success=True,
                data=data,
                error_message="",
            )
        except Exception as e:
            return OperationResult(
                request_id="",
                success=False,
                data=None,
                error_message=f"Failed to get screen size: {str(e)}",
            )

    async def screenshot(self) -> OperationResult:
        """
        Takes a screenshot of the current screen.

        Returns:
            OperationResult: Result object containing the path to the screenshot
                and error message if any.

        Example:
            ```python
            session = await agent_bay.create().session
            screenshot = await session.computer.screenshot()
            print(f"Screenshot URL: {screenshot.data}")
            await session.delete()
            ```

        Note:
            - Returns an OSS URL to the screenshot image
            - Screenshot captures the entire screen
            - Useful for debugging and verification
            - Image format is typically PNG

        See Also:
            get_screen_size
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

    # Window Management Operations
    async def list_root_windows(self, timeout_ms: int = 3000) -> WindowListResult:
        """
        Lists all root windows.

        Args:
            timeout_ms (int, optional): Timeout in milliseconds. Defaults to 3000.

        Returns:
            WindowListResult: Result object containing list of windows and error message if any.

        Example:
            ```python
            session = await agent_bay.create().session
            windows = await session.computer.list_root_windows()
            for window in windows.windows:
                print(f"Window: {window.title}, ID: {window.window_id}")
            await session.delete()
            ```
        """
        try:
            args = {"timeout_ms": timeout_ms}
            result = await self.session.call_mcp_tool("list_root_windows", args)

            if not result.success:
                return WindowListResult(
                    request_id=result.request_id,
                    success=False,
                    windows=[],
                    error_message=result.error_message,
                )

            # Parse the windows data
            windows = []
            if result.data:
                try:
                    windows_data = json.loads(result.data)
                    for window_data in windows_data:
                        windows.append(Window._from_dict(window_data))
                except json.JSONDecodeError as e:
                    return WindowListResult(
                        request_id=result.request_id,
                        success=False,
                        windows=[],
                        error_message=f"Failed to parse windows JSON: {e}",
                    )

            return WindowListResult(
                request_id=result.request_id,
                success=True,
                windows=windows,
                error_message="",
            )
        except Exception as e:
            return WindowListResult(
                request_id="",
                success=False,
                windows=[],
                error_message=f"Failed to list root windows: {str(e)}",
            )

    async def get_active_window(self) -> WindowInfoResult:
        """
        Gets the currently active window.

        Returns:
            WindowInfoResult: Result object containing active window info and error message if any.

        Example:
            ```python
            session = await agent_bay.create().session
            active = await session.computer.get_active_window()
            print(f"Active window: {active.window.title}")
            await session.delete()
            ```
        """
        try:
            args = {}
            result = await self.session.call_mcp_tool("get_active_window", args)

            if not result.success:
                return WindowInfoResult(
                    request_id=result.request_id,
                    success=False,
                    window=None,
                    error_message=result.error_message,
                )

            # Parse the window data
            window = None
            if result.data:
                try:
                    window_data = json.loads(result.data)
                    window = Window._from_dict(window_data)
                except json.JSONDecodeError as e:
                    return WindowInfoResult(
                        request_id=result.request_id,
                        success=False,
                        window=None,
                        error_message=f"Failed to parse window JSON: {e}",
                    )

            return WindowInfoResult(
                request_id=result.request_id,
                success=True,
                window=window,
                error_message="",
            )
        except Exception as e:
            return WindowInfoResult(
                request_id="",
                success=False,
                window=None,
                error_message=f"Failed to get active window: {str(e)}",
            )

    async def activate_window(self, window_id: int) -> BoolResult:
        """
        Activates the specified window.

        Args:
            window_id (int): The ID of the window to activate.

        Returns:
            BoolResult: Result object containing success status and error message if any.

        Example:
            ```python
            session = await agent_bay.create().session
            windows = await session.computer.list_root_windows()
            if windows.windows:
                await session.computer.activate_window(windows.windows[0].window_id)
            await session.delete()
            ```

        Note:
            - The window must exist in the system
            - Use list_root_windows() to get available window IDs
            - Activating a window brings it to the foreground

        See Also:
            list_root_windows, get_active_window, close_window
        """
        try:
            args = {"window_id": window_id}
            result = await self.session.call_mcp_tool("activate_window", args)

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
                error_message=f"Failed to activate window: {str(e)}",
            )

    async def close_window(self, window_id: int) -> BoolResult:
        """
        Closes the specified window.

        Args:
            window_id (int): The ID of the window to close.

        Returns:
            BoolResult: Result object containing success status and error message if any.

        Example:
            ```python
            session = await agent_bay.create().session
            windows = await session.computer.list_root_windows()
            if windows.windows:
                await session.computer.close_window(windows.windows[0].window_id)
            await session.delete()
            ```

        Note:
            - The window must exist in the system
            - Use list_root_windows() to get available window IDs
            - Closing a window terminates it permanently

        See Also:
            list_root_windows, activate_window, minimize_window
        """
        try:
            args = {"window_id": window_id}
            result = await self.session.call_mcp_tool("close_window", args)

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
                error_message=f"Failed to close window: {str(e)}",
            )

    async def maximize_window(self, window_id: int) -> BoolResult:
        """
        Maximizes the specified window.

        Args:
            window_id (int): The ID of the window to maximize.

        Returns:
            BoolResult: Result object containing success status and error message if any.

        Example:
            ```python
            session = await agent_bay.create().session
            active = await session.computer.get_active_window()
            if active.window:
                await session.computer.maximize_window(active.window.window_id)
            await session.delete()
            ```

        Note:
            - The window must exist in the system
            - Maximizing expands the window to fill the screen
            - Use restore_window() to return to previous size

        See Also:
            minimize_window, restore_window, fullscreen_window, resize_window
        """
        try:
            args = {"window_id": window_id}
            result = await self.session.call_mcp_tool("maximize_window", args)

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
                error_message=f"Failed to maximize window: {str(e)}",
            )

    async def minimize_window(self, window_id: int) -> BoolResult:
        """
        Minimizes the specified window.

        Args:
            window_id (int): The ID of the window to minimize.

        Returns:
            BoolResult: Result object containing success status and error message if any.

        Example:
            ```python
            session = await agent_bay.create().session
            active = await session.computer.get_active_window()
            if active.window:
                await session.computer.minimize_window(active.window.window_id)
            await session.delete()
            ```

        Note:
            - The window must exist in the system
            - Minimizing hides the window in the taskbar
            - Use restore_window() or activate_window() to bring it back

        See Also:
            maximize_window, restore_window, activate_window
        """
        try:
            args = {"window_id": window_id}
            result = await self.session.call_mcp_tool("minimize_window", args)

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
                error_message=f"Failed to minimize window: {str(e)}",
            )

    async def restore_window(self, window_id: int) -> BoolResult:
        """
        Restores the specified window.

        Args:
            window_id (int): The ID of the window to restore.

        Returns:
            BoolResult: Result object containing success status and error message if any.

        Example:
            ```python
            session = await agent_bay.create().session
            active = await session.computer.get_active_window()
            if active.window:
                wid = active.window.window_id
                await session.computer.minimize_window(wid)
                await session.computer.restore_window(wid)
            await session.delete()
            ```

        Note:
            - The window must exist in the system
            - Restoring returns a minimized or maximized window to its normal state
            - Works for windows that were previously minimized or maximized

        See Also:
            minimize_window, maximize_window, activate_window
        """
        try:
            args = {"window_id": window_id}
            result = await self.session.call_mcp_tool("restore_window", args)

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
                error_message=f"Failed to restore window: {str(e)}",
            )

    async def resize_window(
        self, window_id: int, width: int, height: int
    ) -> BoolResult:
        """
        Resizes the specified window.

        Args:
            window_id (int): The ID of the window to resize.
            width (int): New width of the window.
            height (int): New height of the window.

        Returns:
            BoolResult: Result object containing success status and error message if any.

        Example:
            ```python
            session = await agent_bay.create().session
            active = await session.computer.get_active_window()
            if active.window:
                await session.computer.resize_window(active.window.window_id, 800, 600)
            await session.delete()
            ```

        Note:
            - The window must exist in the system
            - Width and height are in pixels
            - Some windows may have minimum or maximum size constraints

        See Also:
            maximize_window, restore_window, get_screen_size
        """
        try:
            args = {"window_id": window_id, "width": width, "height": height}
            result = await self.session.call_mcp_tool("resize_window", args)

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
                error_message=f"Failed to resize window: {str(e)}",
            )

    async def fullscreen_window(self, window_id: int) -> BoolResult:
        """
        Makes the specified window fullscreen.

        Args:
            window_id (int): The ID of the window to make fullscreen.

        Returns:
            BoolResult: Result object containing success status and error message if any.

        Example:
            ```python
            session = await agent_bay.create().session
            active = await session.computer.get_active_window()
            if active.window:
                await session.computer.fullscreen_window(active.window.window_id)
            await session.delete()
            ```

        Note:
            - The window must exist in the system
            - Fullscreen mode hides window borders and taskbar
            - Different from maximize_window() which keeps window borders
            - Press F11 or ESC to exit fullscreen in most applications

        See Also:
            maximize_window, restore_window
        """
        try:
            args = {"window_id": window_id}
            result = await self.session.call_mcp_tool("fullscreen_window", args)

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
                error_message=f"Failed to fullscreen window: {str(e)}",
            )

    async def focus_mode(self, on: bool) -> BoolResult:
        """
        Toggles focus mode on or off.

        Args:
            on (bool): True to enable focus mode, False to disable it.

        Returns:
            BoolResult: Result object containing success status and error message if any.

        Example:
            ```python
            session = await agent_bay.create().session
            await session.computer.focus_mode(True)
            await session.computer.focus_mode(False)
            await session.delete()
            ```

        Note:
            - Focus mode helps reduce distractions by managing window focus
            - When enabled, may prevent background windows from stealing focus
            - Behavior depends on the window manager and OS settings

        See Also:
            activate_window, get_active_window
        """
        try:
            args = {"on": on}
            result = await self.session.call_mcp_tool("focus_mode", args)

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
                error_message=f"Failed to toggle focus mode: {str(e)}",
            )

    # Application Management Operations
    async def get_installed_apps(
        self,
        start_menu: bool = True,
        desktop: bool = False,
        ignore_system_apps: bool = True,
    ) -> InstalledAppListResult:
        """
        Gets the list of installed applications.

        Args:
            start_menu (bool, optional): Whether to include start menu applications. Defaults to True.
            desktop (bool, optional): Whether to include desktop applications. Defaults to False.
            ignore_system_apps (bool, optional): Whether to ignore system applications. Defaults to True.

        Returns:
            InstalledAppListResult: Result object containing list of installed apps and error message if any.

        Example:
            ```python
            session = await agent_bay.create().session
            apps = await session.computer.get_installed_apps()
            for app in apps.data:
                print(f"{app.name}: {app.start_cmd}")
            await session.delete()
            ```

        Note:
            - start_menu parameter includes applications from Windows Start Menu
            - desktop parameter includes shortcuts from Desktop
            - ignore_system_apps parameter filters out system applications
            - Each app object contains name, start_cmd, stop_cmd, and work_directory

        See Also:
            start_app, list_visible_apps, stop_app_by_pname
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
        Starts the specified application.

        Args:
            start_cmd (str): The command to start the application.
            work_directory (str, optional): Working directory for the application. Defaults to "".
            activity (str, optional): Activity name to launch (for mobile apps). Defaults to "".

        Returns:
            ProcessListResult: Result object containing list of processes started and error message if any.

        Example:
            ```python
            session = await agent_bay.create().session
            processes = await session.computer.start_app("notepad.exe")
            print(f"Started {len(processes.data)} process(es)")
            await session.delete()
            ```

        Note:
            - The start_cmd can be an executable name or full path
            - work_directory is optional and defaults to the system default
            - activity parameter is for mobile apps (Android)
            - Returns process information for all started processes

        See Also:
            get_installed_apps, stop_app_by_pname, list_visible_apps
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

    async def list_visible_apps(self) -> ProcessListResult:
        """
        Lists all applications with visible windows.

        Returns detailed process information for applications that have visible windows,
        including process ID, name, command line, and other system information.
        This is useful for system monitoring and process management tasks.

        Returns:
            ProcessListResult: Result object containing list of visible applications
                with detailed process information.

        Example:
            ```python
            session = await agent_bay.create().session
            apps = await session.computer.list_visible_apps()
            for app in apps.data:
                print(f"App: {app.pname}, PID: {app.pid}")
            await session.delete()
            ```

        Note:
            - Only returns applications with visible windows
            - Hidden or minimized windows may not appear
            - Useful for monitoring currently active applications
            - Process information includes PID, name, and command line

        See Also:
            get_installed_apps, start_app, stop_app_by_pname, stop_app_by_pid
        """
        try:
            result = await self.session.call_mcp_tool("list_visible_apps", {})

            if not result.success:
                return ProcessListResult(
                    request_id=result.request_id,
                    success=False,
                    error_message=result.error_message,
                )

            try:
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

    async def stop_app_by_pname(self, pname: str) -> AppOperationResult:
        """
        Stops an application by process name.

        Args:
            pname (str): The process name of the application to stop.

        Returns:
            AppOperationResult: Result object containing success status and error message if any.

        Example:
            ```python
            session = await agent_bay.create().session
            await session.computer.start_app("notepad.exe")
            result = await session.computer.stop_app_by_pname("notepad.exe")
            await session.delete()
            ```

        Note:
            - The process name should match exactly (case-sensitive on some systems)
            - This will stop all processes matching the given name
            - If multiple instances are running, all will be terminated
            - The .exe extension may be required on Windows

        See Also:
            start_app, stop_app_by_pid, stop_app_by_cmd, list_visible_apps
        """
        try:
            args = {"pname": pname}
            result = await self.session.call_mcp_tool("stop_app_by_pname", args)

            return AppOperationResult(
                request_id=result.request_id,
                success=result.success,
                error_message=result.error_message,
            )
        except Exception as e:
            return AppOperationResult(success=False, error_message=str(e))

    async def stop_app_by_pid(self, pid: int) -> AppOperationResult:
        """
        Stops an application by process ID.

        Args:
            pid (int): The process ID of the application to stop.

        Returns:
            AppOperationResult: Result object containing success status and error message if any.

        Example:
            ```python
            session = await agent_bay.create().session
            processes = await session.computer.start_app("notepad.exe")
            pid = processes.data[0].pid
            result = await session.computer.stop_app_by_pid(pid)
            await session.delete()
            ```

        Note:
            - PID must be a valid process ID
            - More precise than stopping by name (only stops specific process)
            - The process must be owned by the session or have appropriate permissions
            - PID can be obtained from start_app() or list_visible_apps()

        See Also:
            start_app, stop_app_by_pname, stop_app_by_cmd, list_visible_apps
        """
        try:
            args = {"pid": pid}
            result = await self.session.call_mcp_tool("stop_app_by_pid", args)

            return AppOperationResult(
                request_id=result.request_id,
                success=result.success,
                error_message=result.error_message,
            )
        except Exception as e:
            return AppOperationResult(success=False, error_message=str(e))

    async def stop_app_by_cmd(self, stop_cmd: str) -> AppOperationResult:
        """
        Stops an application by stop command.

        Args:
            stop_cmd (str): The command to stop the application.

        Returns:
            AppOperationResult: Result object containing success status and error message if any.

        Example:
            ```python
            session = await agent_bay.create().session
            apps = await session.computer.get_installed_apps()
            if apps.data and apps.data[0].stop_cmd:
                result = await session.computer.stop_app_by_cmd(apps.data[0].stop_cmd)
            await session.delete()
            ```

        Note:
            - The stop_cmd should be the command registered to stop the application
            - Typically obtained from get_installed_apps() which returns app metadata
            - Some applications may not have a stop command defined
            - The command is executed as-is without shell interpretation

        See Also:
            get_installed_apps, start_app, stop_app_by_pname, stop_app_by_pid
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
