"""
Command module data models.
"""

from .response import ApiResponse


class CommandResult(ApiResponse):
    """Result of command execution operations."""

    def __init__(
        self,
        request_id: str = "",
        success: bool = False,
        output: str = "",
        error_message: str = "",
        exit_code: int = 0,
        stdout: str = "",
        stderr: str = "",
        trace_id: str = "",
    ):
        """
        Initialize a CommandResult.

        Args:
            request_id (str, optional): Unique identifier for the API request.
            success (bool, optional): Whether the operation was successful.
            output (str, optional): The command execution output (stdout + stderr). 
            error_message (str, optional): Error message if the operation failed (stderr or system error).
            exit_code (int, optional): The exit code of the command execution. Default is 0.
            stdout (str, optional): Standard output from the command execution.
            stderr (str, optional): Standard error from the command execution.
            trace_id (str, optional): Trace ID for error tracking. Only present when exit_code != 0.
                Used for quick problem localization.
        """
        super().__init__(request_id)
        self.success = success
        self.output = output
        self.error_message = error_message
        self.exit_code = exit_code
        self.stdout = stdout
        self.stderr = stderr
        self.trace_id = trace_id

