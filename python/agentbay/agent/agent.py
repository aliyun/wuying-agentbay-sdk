from agentbay.exceptions import AgentError
from agentbay.api.base_service import BaseService
from agentbay.model import ApiResponse


class TaskResult(ApiResponse):
    """Result of task execution."""

    def __init__(
        self,
        request_id: str = "",
        success: bool = False,
        output: str = "",
        error_message: str = "",
    ):
        """
        Initialize a TaskResult object.

        Args:
            request_id (str, optional): Unique identifier for the API request.
            success (bool, optional): Whether the execution was successful.
            output (str, optional): The command output.
            error_message (str, optional): Error message if the execution failed.
        """
        super().__init__(request_id)
        self.success = success
        self.output = output
        self.error_message = error_message


class Agent(BaseService):
    """
    An Agent to manipulate applications to complete specific tasks.
    """

    def __init__(self, session):
        self.session = session

    def flux_execute_task(self, task: str) -> TaskResult:
        """
        To execute a specific task described in the humman language.

        Args:
            task: Task description in human language.

        Returns:
            TaskResult: Result object containing success status, task output,
            and error message if any.
        """
        try:
            args = {"task": task}

            result = self._call_mcp_tool("flux_execute_task", args)
            print(f"Task execution response: {result}")

            if result.success:
                return TaskResult(
                    request_id=result.request_id,
                    success=True,
                    output=result.data,
                )
            else:
                return TaskResult(
                    request_id=result.request_id,
                    success=False,
                    error_message=result.error_message or "Failed to execute task",
                )
        except AgentError as e:
            return TaskResult(request_id="", success=False, error_message=str(e))
        except Exception as e:
            return TaskResult(
                request_id="",
                success=False,
                error_message=f"Failed to execute: {e}",
            )

    def flux_terminate_task(self, task_id: str) -> TaskResult:
        """
        Terminate a task  with a specified task_id.

        Args:
            task_id: The id of the runnning task.

        Returns:
            TaskResult: Result object containing success status, task output,
            and error message if any.
        """
        try:
            args = {"task_id": task_id}

            result = self._call_mcp_tool("flux_terminate_task", args)
            print(f"Task termination response: {result}")

            if result.success:
                return TaskResult(
                    request_id=result.request_id,
                    success=True,
                    output=result.data,
                )
            else:
                return TaskResult(
                    request_id=result.request_id,
                    success=False,
                    error_message=result.error_message or "Failed to terminate task",
                )
        except AgentError as e:
            return TaskResult(request_id="", success=False, error_message=str(e))
        except Exception as e:
            return TaskResult(
                request_id="",
                success=False,
                error_message=f"Failed to terminate: {e}",
            )
