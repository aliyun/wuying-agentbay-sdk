import json
from typing import TYPE_CHECKING, Dict, Optional

from agentbay.api.models import (
    GetLabelRequest,
    GetLinkRequest,
    GetLinkResponse,
    GetMcpResourceRequest,
    ReleaseMcpSessionRequest,
    SetLabelRequest,
)
from agentbay.application import ApplicationManager
from agentbay.command import Command
from agentbay.exceptions import SessionError
from agentbay.filesystem import FileSystem
from agentbay.model import DeleteResult, OperationResult, extract_request_id
from agentbay.oss import Oss
from agentbay.ui import UI
from agentbay.window import WindowManager
from agentbay.context_manager import ContextManager

if TYPE_CHECKING:
    from agentbay.agentbay import AgentBay


class SessionInfo:
    """
    SessionInfo contains information about a session.
    """

    def __init__(
        self,
        session_id: str = "",
        resource_url: str = "",
        app_id: str = "",
        auth_code: str = "",
        connection_properties: str = "",
        resource_id: str = "",
        resource_type: str = "",
        ticket: str = "",
    ):
        self.session_id = session_id
        self.resource_url = resource_url
        self.app_id = app_id
        self.auth_code = auth_code
        self.connection_properties = connection_properties
        self.resource_id = resource_id
        self.resource_type = resource_type
        self.ticket = ticket


class Session:
    """
    Session represents a session in the AgentBay cloud environment.
    """

    def __init__(self, agent_bay: "AgentBay", session_id: str):
        self.agent_bay = agent_bay
        self.session_id = session_id
        self.resource_url = ""

        # Initialize file system, command handlers
        self.file_system = FileSystem(self)
        self.command = Command(self)
        self.oss = Oss(self)

        # Initialize application and window managers
        self.application = ApplicationManager(self)
        self.window = WindowManager(self)

        self.ui = UI(self)
        self.context = ContextManager(self)

    def get_api_key(self) -> str:
        """Return the API key for this session."""
        return self.agent_bay.api_key

    def get_client(self):
        """Return the HTTP client for this session."""
        return self.agent_bay.client

    def get_session_id(self) -> str:
        """Return the session_id for this session."""
        return self.session_id

    def delete(self) -> DeleteResult:
        """
        Delete this session.

        Returns:
            DeleteResult: Result indicating success or failure and request ID.
        """
        try:
            request = ReleaseMcpSessionRequest(
                authorization=f"Bearer {self.get_api_key()}",
                session_id=self.session_id,
            )
            response = self.get_client().release_mcp_session(request)
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

            # Check if the response is success
            response_map = response.to_map()
            success = response_map.get("body", {}).get("Success", True)

            if not success:
                return DeleteResult(
                    request_id=request_id,
                    success=False,
                    error_message="Failed to delete session",
                )

            # Return success result with request ID
            return DeleteResult(request_id=request_id, success=True)

        except Exception as e:
            print("Error calling release_mcp_session:", e)
            # In case of error, return failure result with error message
            return DeleteResult(
                success=False,
                error_message=f"Failed to delete session {self.session_id}: {e}",
            )

    def set_labels(self, labels: Dict[str, str]) -> OperationResult:
        """
        Sets the labels for this session.

        Args:
            labels (Dict[str, str]): The labels to set for the session.

        Returns:
            OperationResult: Result indicating success or failure with request ID.

        Raises:
            SessionError: If the operation fails.
        """
        try:
            # Convert labels to JSON string
            labels_json = json.dumps(labels)

            request = SetLabelRequest(
                authorization=f"Bearer {self.get_api_key()}",
                session_id=self.session_id,
                labels=labels_json,
            )

            response = self.get_client().set_label(request)

            # Extract request ID
            request_id = extract_request_id(response)

            return OperationResult(request_id=request_id, success=True)

        except Exception as e:
            print("Error calling set_label:", e)
            raise SessionError(
                f"Failed to set labels for session {self.session_id}: {e}"
            )

    def get_labels(self) -> OperationResult:
        """
        Gets the labels for this session.

        Returns:
            OperationResult: Result containing the labels as data and request ID.

        Raises:
            SessionError: If the operation fails.
        """
        try:
            request = GetLabelRequest(
                authorization=f"Bearer {self.get_api_key()}",
                session_id=self.session_id,
            )

            response = self.get_client().get_label(request)

            # Extract request ID
            request_id = extract_request_id(response)

            # Extract labels from response
            labels_json = (
                response.to_map().get("body", {}).get("Data", {}).get("Labels")
            )

            labels = {}
            if labels_json:
                labels = json.loads(labels_json)

            return OperationResult(request_id=request_id, success=True, data=labels)

        except Exception as e:
            print("Error calling get_label:", e)
            raise SessionError(
                f"Failed to get labels for session {self.session_id}: {e}"
            )

    def info(self) -> OperationResult:
        """
        Gets information about this session.

        Returns:
            OperationResult: Result containing the session information as data and
                request ID.

        Raises:
            SessionError: If the operation fails.
        """
        try:
            request = GetMcpResourceRequest(
                authorization=f"Bearer {self.get_api_key()}",
                session_id=self.session_id,
            )

            print("API Call: GetMcpResource")
            print(f"Request: SessionId={self.session_id}")

            response = self.get_client().get_mcp_resource(request)
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

            # Extract session info from response
            response_map = response.to_map()
            data = response_map.get("body", {}).get("Data", {})

            session_info = SessionInfo()

            if "SessionId" in data:
                session_info.session_id = data["SessionId"]

            if "ResourceUrl" in data:
                session_info.resource_url = data["ResourceUrl"]
                # Update the session's resource_url with the latest value
                self.resource_url = data["ResourceUrl"]
            # Transfer DesktopInfo fields to SessionInfo
            if "DesktopInfo" in data:
                desktop_info = data["DesktopInfo"]
                if "AppId" in desktop_info:
                    session_info.app_id = desktop_info["AppId"]
                if "AuthCode" in desktop_info:
                    session_info.auth_code = desktop_info["AuthCode"]
                if "ConnectionProperties" in desktop_info:
                    session_info.connection_properties = desktop_info[
                        "ConnectionProperties"
                    ]
                if "ResourceId" in desktop_info:
                    session_info.resource_id = desktop_info["ResourceId"]
                if "ResourceType" in desktop_info:
                    session_info.resource_type = desktop_info["ResourceType"]
                if "Ticket" in desktop_info:
                    session_info.ticket = desktop_info["Ticket"]

            return OperationResult(
                request_id=request_id, success=True, data=session_info
            )

        except Exception as e:
            print("Error calling GetMcpResource:", e)
            raise SessionError(
                f"Failed to get session info for session {self.session_id}: {e}"
            )

    def get_link(
        self, protocol_type: Optional[str] = None, port: Optional[int] = None
    ) -> OperationResult:
        """
        Get a link associated with the current session.

        Args:
            protocol_type (Optional[str], optional): The protocol type to use for the
                link. Defaults to None.
            port (Optional[int], optional): The port to use for the link.

        Returns:
            OperationResult: Result containing the link as data and request ID.

        Raises:
            SessionError: If the request fails or the response is invalid.
        """
        try:
            request = GetLinkRequest(
                authorization=f"Bearer {self.get_api_key()}",
                session_id=self.get_session_id(),
                protocol_type=protocol_type,
                port=port,
            )
            response: GetLinkResponse = self.agent_bay.client.get_link(request)

            # Extract request ID
            request_id = extract_request_id(response)

            response_map = response.to_map()

            if not isinstance(response_map, dict):
                raise SessionError(
                    "Invalid response format: expected a dictionary from "
                    "response.to_map()"
                )

            body = response_map.get("body", {})
            if not isinstance(body, dict):
                raise SessionError(
                    "Invalid response format: 'body' field is not a dictionary"
                )

            data = body.get("Data", {})
            print(f"Data: {data}")

            if not isinstance(data, dict):
                try:
                    data = json.loads(data) if isinstance(data, str) else {}
                except json.JSONDecodeError:
                    data = {}

            url = data.get("Url", "")

            return OperationResult(request_id=request_id, success=True, data=url)

        except SessionError:
            raise
        except Exception as e:
            raise SessionError(f"Failed to get link: {e}")

    async def get_link_async(
        self, protocol_type: Optional[str] = None, port: Optional[int] = None
    ) -> OperationResult:
        """
        Asynchronously get a link associated with the current session.

        Args:
            protocol_type (Optional[str], optional): The protocol type to use for the
                link. Defaults to None.
            port (Optional[int], optional): The port to use for the link.
                Defaults to None.

        Returns:
            OperationResult: Result containing the link as data and request ID.

        Raises:
            SessionError: If the request fails or the response is invalid.
        """
        try:
            request = GetLinkRequest(
                authorization=f"Bearer {self.get_api_key()}",
                session_id=self.get_session_id(),
                protocol_type=protocol_type,
                port=port,
            )
            response: GetLinkResponse = await self.agent_bay.client.get_link_async(
                request
            )

            # Extract request ID
            request_id = extract_request_id(response)

            response_map = response.to_map()

            if not isinstance(response_map, dict):
                raise SessionError(
                    "Invalid response format: expected a dictionary from "
                    "response.to_map()"
                )

            body = response_map.get("body", {})
            if not isinstance(body, dict):
                raise SessionError(
                    "Invalid response format: 'body' field is not a dictionary"
                )

            data = body.get("Data", {})
            print(f"Data: {data}")

            if not isinstance(data, dict):
                try:
                    data = json.loads(data) if isinstance(data, str) else {}
                except json.JSONDecodeError:
                    data = {}

            url = data.get("Url", "")

            return OperationResult(request_id=request_id, success=True, data=url)

        except SessionError:
            raise
        except Exception as e:
            raise SessionError(f"Failed to get link asynchronously: {e}")
