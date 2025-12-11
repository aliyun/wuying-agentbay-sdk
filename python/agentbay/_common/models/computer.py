"""
Computer module data models.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from .response import ApiResponse


class MouseButton(str, Enum):
    """
    Mouse button types for click and drag operations.

    Available values: left, right, middle, double_left.
    """

    LEFT = "left"
    RIGHT = "right"
    MIDDLE = "middle"
    DOUBLE_LEFT = "double_left"


class ScrollDirection(str, Enum):
    """Scroll direction for scroll operations."""

    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"


class InstalledApp:
    """Represents an installed application."""

    def __init__(
        self,
        name: str,
        start_cmd: str,
        stop_cmd: Optional[str] = None,
        work_directory: Optional[str] = None,
    ):
        self.name = name
        self.start_cmd = start_cmd
        self.stop_cmd = stop_cmd
        self.work_directory = work_directory

    @classmethod
    def _from_dict(cls, data: Dict[str, Any]) -> "InstalledApp":
        return cls(
            name=data.get("name", ""),
            start_cmd=data.get("start_cmd", ""),
            stop_cmd=data.get("stop_cmd"),
            work_directory=data.get("work_directory"),
        )


class Process:
    """Represents a running process."""

    def __init__(self, pname: str, pid: int, cmdline: Optional[str] = None):
        self.pname = pname
        self.pid = pid
        self.cmdline = cmdline

    @classmethod
    def _from_dict(cls, data: Dict[str, Any]) -> "Process":
        return cls(
            pname=data.get("pname", ""),
            pid=data.get("pid", 0),
            cmdline=data.get("cmdline"),
        )


class Window:
    """Represents a window in the system."""

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
        child_windows: Optional[List["Window"]] = None,
    ):
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
    def _from_dict(cls, data: Dict[str, Any]) -> "Window":
        child_windows = []
        if "child_windows" in data and data["child_windows"]:
            child_windows = [cls._from_dict(child) for child in data["child_windows"]]
        return cls(
            window_id=data.get("window_id", 0),
            title=data.get("title", ""),
            absolute_upper_left_x=data.get("absolute_upper_left_x"),
            absolute_upper_left_y=data.get("absolute_upper_left_y"),
            width=data.get("width"),
            height=data.get("height"),
            pid=data.get("pid"),
            pname=data.get("pname"),
            child_windows=child_windows,
        )


class InstalledAppListResult(ApiResponse):
    """Result of operations returning a list of InstalledApps."""

    def __init__(
        self,
        request_id: str = "",
        success: bool = False,
        data: Optional[List[InstalledApp]] = None,
        error_message: str = "",
    ):
        super().__init__(request_id)
        self.success = success
        self.data = data if data is not None else []
        self.error_message = error_message


class ProcessListResult(ApiResponse):
    """Result of operations returning a list of Processes."""

    def __init__(
        self,
        request_id: str = "",
        success: bool = False,
        data: Optional[List[Process]] = None,
        error_message: str = "",
    ):
        super().__init__(request_id)
        self.success = success
        self.data = data if data is not None else []
        self.error_message = error_message


class AppOperationResult(ApiResponse):
    """Result of application operations like start/stop."""

    def __init__(
        self,
        request_id: str = "",
        success: bool = False,
        error_message: str = "",
    ):
        super().__init__(request_id)
        self.success = success
        self.error_message = error_message


class WindowListResult(ApiResponse):
    """Result of window listing operations."""

    def __init__(
        self,
        request_id: str = "",
        success: bool = False,
        windows: Optional[List[Any]] = None,
        error_message: str = "",
    ):
        super().__init__(request_id)
        self.success = success
        self.windows = windows or []
        self.error_message = error_message


class WindowInfoResult(ApiResponse):
    """Result of window info operations."""

    def __init__(
        self,
        request_id: str = "",
        success: bool = False,
        window: Any = None,
        error_message: str = "",
    ):
        super().__init__(request_id)
        self.success = success
        self.window = window
        self.error_message = error_message

