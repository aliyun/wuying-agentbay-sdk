"""
Code module data models.
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from .response import ApiResponse


@dataclass
class ExecutionResult:
    """Single execution result supporting multiple formats"""

    text: Optional[str] = None
    html: Optional[str] = None
    markdown: Optional[str] = None
    png: Optional[str] = None  # base64 encoded
    jpeg: Optional[str] = None  # base64 encoded
    svg: Optional[str] = None
    json: Optional[dict] = None
    latex: Optional[str] = None
    chart: Optional[dict] = None  # chart data
    is_main_result: bool = False

    def formats(self) -> List[str]:
        """Returns all available formats"""
        return [k for k, v in self.__dict__.items() if v is not None and k != "is_main_result"]


@dataclass
class ExecutionLogs:
    """Execution logs"""

    stdout: List[str] = field(default_factory=list)
    stderr: List[str] = field(default_factory=list)


@dataclass
class ExecutionError:
    """Detailed error information"""

    name: str
    value: str
    traceback: str


@dataclass
class EnhancedCodeExecutionResult(ApiResponse):
    """Enhanced code execution result"""

    # Basic information
    request_id: str = ""
    success: bool = False
    execution_count: Optional[int] = None
    execution_time: float = 0.0

    # Output streams (key improvement)
    logs: ExecutionLogs = field(default_factory=ExecutionLogs)

    # Multi-format result support (major upgrade)
    results: List[ExecutionResult] = field(default_factory=list)

    # Error details
    error: Optional[ExecutionError] = None
    error_message: str = ""  # backward compatibility

    # Backward compatibility property
    @property
    def result(self) -> str:
        """Backward compatible text result"""
        # Search for main result first
        for res in self.results:
            if res.is_main_result and res.text:
                return res.text
        # Fallback to first result text
        if self.results and self.results[0].text:
            return self.results[0].text
        
        # If no result text, check logs
        if self.logs.stdout:
             return "".join(self.logs.stdout)
             
        return ""


class CodeExecutionResult(ApiResponse):
    """Result of code execution operations. Kept for backward compatibility but users should transition to EnhancedCodeExecutionResult."""

    def __init__(
        self,
        request_id: str = "",
        success: bool = False,
        result: str = "",
        error_message: str = "",
    ):
        """
        Initialize a CodeExecutionResult.

        Args:
            request_id (str, optional): Unique identifier for the API request.
            success (bool, optional): Whether the operation was successful.
            result (str, optional): The execution result.
            error_message (str, optional): Error message if the operation failed.
        """
        super().__init__(request_id)
        self.success = success
        self.result = result
        self.error_message = error_message
