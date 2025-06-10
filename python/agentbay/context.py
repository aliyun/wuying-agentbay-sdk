from typing import List, Optional, Set

from agentbay.api.models import (DeleteContextRequest, GetContextRequest,
                                 ListContextsRequest, ModifyContextRequest)
from agentbay.exceptions import AgentBayError


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
            state (str, optional): The current state of the context. Defaults to "available".
            created_at (Optional[str], optional): Date and time when the Context was created. Defaults to None.
            last_used_at (Optional[str], optional): Date and time when the Context was last used. Defaults to None.
            os_type (Optional[str], optional): The operating system type this context is bound to. Defaults to None.
        """
        self.id = id
        self.name = name
        self.state = state
        self.created_at = created_at
        self.last_used_at = last_used_at
        self.os_type = os_type


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

    def list(self) -> List[Context]:
        """
        Lists all available contexts.

        Returns:
            List[Context]: A list of Context objects.
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
            print(f"Response from ListContexts: {response}")

            contexts = []

            response_data = response.to_map().get("body", {}).get("Data", [])
            if response_data:
                for context_data in response_data:
                    context = Context(
                        id=context_data.get("Id"),
                        name=context_data.get("Name"),
                        state=context_data.get("State"),
                        created_at=context_data.get("CreateTime"),
                        last_used_at=context_data.get("LastUsedTime"),
                        os_type=context_data.get("OsType"),
                    )
                    contexts.append(context)

            return contexts
        except Exception as e:
            print(f"Error calling ListContexts: {e}")
            raise AgentBayError(f"Failed to list contexts: {e}")

    def get(self, name: str, create: bool = False) -> Optional[Context]:
        """
        Gets a context by name. Optionally creates it if it doesn't exist.

        Args:
            name (str): The name of the context to get.
            create (bool, optional): Whether to create the context if it doesn't exist. Defaults to False.

        Returns:
            Optional[Context]: The Context object if found or created, None if not found and create is False.
        """
        try:
            # Log API request
            print("API Call: GetContext")
            print(f"Request: Name={name}, AllowCreate={create}")

            request = GetContextRequest(
                name=name,
                allow_create="true" if create else "false",
                authorization=f"Bearer {self.agent_bay.api_key}",
            )
            response = self.agent_bay.client.get_context(request)

            # Log API response
            print(f"Response from GetContext: {response}")

            context_id = response.to_map().get("body", {}).get("Data", {}).get("Id")
            if not context_id:
                return None

            # Get the full context details
            contexts = self.list()
            for context in contexts:
                if context.id == context_id:
                    return context

            # If we couldn't find the context in the list, create a basic one
            return Context(id=context_id, name=name)
        except Exception as e:
            print(f"Error calling GetContext: {e}")
            raise AgentBayError(f"Failed to get context {name}: {e}")

    def create(self, name: str) -> Context:
        """
        Creates a new context with the given name.

        Args:
            name (str): The name for the new context.

        Returns:
            Context: The created Context object.
        """
        return self.get(name, create=True)

    def update(self, context: Context) -> bool:
        """
        Updates the specified context.

        Args:
            context (Context): The Context object to update.

        Returns:
            bool: True if the update was successful, False otherwise.
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

            # Validate response
            response_map = response.to_map()
            if not response_map:
                raise AgentBayError("Invalid response format")

            body = response_map.get("body", {})
            if not body:
                raise AgentBayError("Invalid response body")

            # Check for success
            if not body.get("Success"):
                raise AgentBayError(f"Update failed: {body.get('Code')}")

            return body.get("Success", False)
        except Exception as e:
            print(f"Error calling ModifyContext: {e}")
            raise AgentBayError(f"Failed to update context {context.id}: {e}")

    def delete(self, context: Context) -> None:
        """
        Deletes the specified context.

        Args:
            context (Context): The Context object to delete.
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
        except Exception as e:
            print(f"Error calling DeleteContext: {e}")
            raise AgentBayError(f"Failed to delete context {context.id}: {e}")
