from typing import TYPE_CHECKING, List, Optional

from agentbay.api.models import (
    DeleteContextRequest,
    GetContextRequest,
    ListContextsRequest,
    ModifyContextRequest,
)
from agentbay.exceptions import AgentBayError
from agentbay.model.response import ApiResponse, OperationResult, extract_request_id
import json

if TYPE_CHECKING:
    from agentbay.agentbay import AgentBay


class Context:
    """
    Represents a persistent storage context in the AgentBay cloud environment.

    Attributes:
        id (str): The unique identifier of the context.
        name (str): The name of the context.
        state (str): The current state of the context (e.g., "available", "in-use").
        created_at (str): Date and time when the Context was created.
        last_used_at (str): Date and time when the Context was last used.
        os_type (str): The operating system type this context is bound to.
    """

    def __init__(
        self,
        id: str,
        name: str,
        state: str = "available",
        created_at: Optional[str] = None,
        last_used_at: Optional[str] = None,
        os_type: Optional[str] = None,
    ):
        """
        Initialize a Context object.

        Args:
            id (str): The unique identifier of the context.
            name (str): The name of the context.
            state (str, optional): The current state of the context.
            created_at (Optional[str], optional): Date and time when the Context was
                created. Defaults to None.
            last_used_at (Optional[str], optional): Date and time when the Context was
                last used. Defaults to None.
            os_type (Optional[str], optional): The operating system type this context is
                bound to. Defaults to None.
        """
        self.id = id
        self.name = name
        self.state = state
        self.created_at = created_at
        self.last_used_at = last_used_at
        self.os_type = os_type


class ContextResult(ApiResponse):
    """Result of operations returning a Context."""

    def __init__(
        self,
        request_id: str = "",
        success: bool = False,
        context_id: str = "",
        context: Optional[Context] = None,
    ):
        """
        Initialize a ContextResult.

        Args:
            request_id (str, optional): Unique identifier for the API request.
            success (bool, optional): Whether the operation was successful.
            context_id (str, optional): The unique identifier of the context.
            context (Optional[Context], optional): The Context object.
        """
        super().__init__(request_id)
        self.success = success
        self.context_id = context_id
        self.context = context


class ContextListResult(ApiResponse):
    """Result of operations returning a list of Contexts."""

    def __init__(
        self,
        request_id: str = "",
        success: bool = False,
        contexts: Optional[List[Context]] = None,
    ):
        """
        Initialize a ContextListResult.

        Args:
            request_id (str, optional): Unique identifier for the API request.
            success (bool, optional): Whether the operation was successful.
            contexts (Optional[List[Context]], optional): The list of context objects.
        """
        super().__init__(request_id)
        self.success = success
        self.contexts = contexts if contexts is not None else []


class ContextService:
    """
    Provides methods to manage persistent contexts in the AgentBay cloud environment.
    """

    def __init__(self, agent_bay: "AgentBay"):
        """
        Initialize the ContextService.

        Args:
            agent_bay (AgentBay): The AgentBay instance.
        """
        self.agent_bay = agent_bay

    def list(self) -> ContextListResult:
        """
        Lists all available contexts.

        Returns:
            ContextListResult: A result object containing the list of Context objects
                and request ID.
        """
        try:
            # Log API request
            print("API Call: ListContexts")
            print("Request: (no parameters)")

            request = ListContextsRequest(
                authorization=f"Bearer {self.agent_bay.api_key}"
            )
            response = self.agent_bay.client.list_contexts(request)

            # Log API response
            try:
                print("Response body:")
                print(
                    json.dumps(
                        response.to_map().get("body", {}), ensure_ascii=False, indent=2
                    )
                )
            except Exception:
                print(f"Response: {response}")

            # Extract request ID
            request_id = extract_request_id(response)

            # Validate response
            try:
                response_map = response.to_map()
                if not isinstance(response_map, dict):
                    return ContextListResult(
                        request_id=request_id, success=False, contexts=[]
                    )

                body = response_map.get("body", {})
                if not isinstance(body, dict):
                    return ContextListResult(
                        request_id=request_id, success=False, contexts=[]
                    )

                contexts = []
                response_data = body.get("Data", [])
                if response_data and isinstance(response_data, list):
                    for context_data in response_data:
                        if isinstance(context_data, dict):
                            context = Context(
                                id=context_data.get("Id", ""),
                                name=context_data.get("Name", ""),
                                state=context_data.get("State", ""),
                                created_at=context_data.get("CreateTime"),
                                last_used_at=context_data.get("LastUsedTime"),
                                os_type=context_data.get("OsType"),
                            )
                            contexts.append(context)

                return ContextListResult(
                    request_id=request_id, success=True, contexts=contexts
                )
            except Exception as e:
                print(f"Error parsing ListContexts response: {e}")
                return ContextListResult(
                    request_id=request_id, success=False, contexts=[]
                )
        except Exception as e:
            print(f"Error calling ListContexts: {e}")
            raise AgentBayError(f"Failed to list contexts: {e}")

    def get(self, name: str, create: bool = False) -> ContextResult:
        """
        Gets a context by name. Optionally creates it if it doesn't exist.

        Args:
            name (str): The name of the context to get.
            create (bool, optional): Whether to create the context if it doesn't exist.

        Returns:
            ContextResult: The ContextResult object containing the Context and request
                ID.
        """
        try:
            # Log API request
            print("API Call: GetContext")
            print(f"Request: Name={name}, AllowCreate={create}")

            request = GetContextRequest(
                name=name,
                allow_create=create,
                authorization=f"Bearer {self.agent_bay.api_key}",
            )
            response = self.agent_bay.client.get_context(request)

            # Log API response
            try:
                print("Response body:")
                print(
                    json.dumps(
                        response.to_map().get("body", {}), ensure_ascii=False, indent=2
                    )
                )
            except Exception:
                print(f"Response: {response}")

            # Extract request ID
            request_id = extract_request_id(response)

            try:
                response_map = response.to_map()

                if (
                    not isinstance(response_map, dict)
                    or not isinstance(response_map.get("body", {}), dict)
                    or not isinstance(
                        response_map.get("body", {}).get("Data", {}), dict
                    )
                ):
                    return ContextResult(
                        request_id=request_id,
                        success=False,
                        context_id="",
                        context=None,
                    )

                data = response_map.get("body", {}).get("Data", {})
                context_id = data.get("Id", "")

                # Create Context object
                context = Context(
                    id=context_id,
                    name=data.get("Name", "") or name,
                    state=data.get("State", "") or "available",
                    created_at=data.get("CreateTime"),
                    last_used_at=data.get("LastUsedTime"),
                    os_type=data.get("OsType"),
                )

                return ContextResult(
                    request_id=request_id,
                    success=True,
                    context_id=context_id,
                    context=context,
                )
            except Exception as e:
                print(f"Error parsing GetContext response: {e}")
                return ContextResult(
                    request_id=request_id,
                    success=False,
                    context_id="",
                    context=None,
                )
        except Exception as e:
            print(f"Error calling GetContext: {e}")
            raise AgentBayError(f"Failed to get context {name}: {e}")

    def create(self, name: str) -> ContextResult:
        """
        Creates a new context with the given name.

        Args:
            name (str): The name for the new context.

        Returns:
            ContextResult: The created ContextResult object with request ID.
        """
        return self.get(name, create=True)

    def update(self, context: Context) -> OperationResult:
        """
        Updates the specified context.

        Args:
            context (Context): The Context object to update.

        Returns:
            OperationResult: Result object containing success status and request ID.
        """
        try:
            # Log API request
            print("API Call: ModifyContext")
            print(f"Request: Id={context.id}, Name={context.name}")

            request = ModifyContextRequest(
                id=context.id,
                name=context.name,
                authorization=f"Bearer {self.agent_bay.api_key}",
            )
            response = self.agent_bay.client.modify_context(request)

            # Log API response
            print(f"Response from ModifyContext: {response}")

            # Extract request ID
            request_id = extract_request_id(response)

            try:
                response_map = response.to_map() if hasattr(response, "to_map") else {}

                if not isinstance(response_map, dict) or not isinstance(
                    response_map.get("body", {}), dict
                ):
                    return OperationResult(
                        request_id=request_id,
                        success=False,
                        error_message="Invalid response format",
                    )

                body = response_map.get("body", {})

                # Check for success
                success = body.get("Success", False)
                error_message = "" if success else f"Update failed: {body.get('Code')}"

                return OperationResult(
                    request_id=request_id,
                    success=success,
                    data=True if success else False,
                    error_message=error_message,
                )
            except Exception as e:
                print(f"Error parsing ModifyContext response: {e}")
                return OperationResult(
                    request_id=request_id,
                    success=False,
                    error_message=f"Failed to parse response: {str(e)}",
                )
        except Exception as e:
            print(f"Error calling ModifyContext: {e}")
            raise AgentBayError(f"Failed to update context {context.id}: {e}")

    def delete(self, context: Context) -> OperationResult:
        """
        Deletes the specified context.

        Args:
            context (Context): The Context object to delete.

        Returns:
            OperationResult: Result object containing success status and request ID.
        """
        try:
            # Log API request
            print("API Call: DeleteContext")
            print(f"Request: Id={context.id}")

            request = DeleteContextRequest(
                id=context.id, authorization=f"Bearer {self.agent_bay.api_key}"
            )
            response = self.agent_bay.client.delete_context(request)

            # Log API response
            print(f"Response from DeleteContext: {response}")

            # Extract request ID
            request_id = extract_request_id(response)

            try:
                response_map = response.to_map() if hasattr(response, "to_map") else {}

                # Check response format
                if not isinstance(response_map, dict) or not isinstance(
                    response_map.get("body", {}), dict
                ):
                    return OperationResult(
                        request_id=request_id,
                        success=False,
                        error_message="Invalid response format",
                    )

                body = response_map.get("body", {})

                # Check for success
                success = body.get("Success", False)
                error_message = "" if success else f"Delete failed: {body.get('Code')}"

                return OperationResult(
                    request_id=request_id,
                    success=success,
                    data=True if success else False,
                    error_message=error_message,
                )
            except Exception as e:
                print(f"Error parsing DeleteContext response: {e}")
                return OperationResult(
                    request_id=request_id,
                    success=False,
                    error_message=f"Failed to parse response: {str(e)}",
                )
        except Exception as e:
            print(f"Error calling DeleteContext: {e}")
            raise AgentBayError(f"Failed to delete context {context.id}: {e}")
