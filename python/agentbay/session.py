import json
from typing import TYPE_CHECKING, Any, Dict, Optional
from .logger import (
    get_logger,
    _log_api_call,
    _log_api_response,
    _log_api_response_with_details,
    _log_operation_start,
    _log_operation_success,
    _log_operation_error,
    _log_warning,
)

from agentbay.api.models import (
    GetLabelRequest,
    GetLinkRequest,
    GetLinkResponse,
    GetMcpResourceRequest,
    ReleaseMcpSessionRequest,
    SetLabelRequest,
)
from agentbay.code import Code
from agentbay.command import Command
from agentbay.computer import Computer
from agentbay.exceptions import SessionError
from agentbay.filesystem import FileSystem
from agentbay.mobile import Mobile
from agentbay.model import DeleteResult, OperationResult, extract_request_id
from agentbay.model import SessionPauseResult, SessionResumeResult
from agentbay.oss import Oss
from agentbay.agent import Agent
from agentbay.context_manager import ContextManager

if TYPE_CHECKING:
    from agentbay.agentbay import AgentBay

from agentbay.browser import Browser

# Initialize logger for this module
_logger = get_logger("session")


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

        # VPC-related information
        self.is_vpc = False  # Whether this session uses VPC resources
        self.network_interface_ip = ""  # Network interface IP for VPC sessions
        self.http_port = ""  # HTTP port for VPC sessions
        self.token = ""

        # Resource URL for accessing the session
        self.resource_url = ""

        # Recording functionality
        self.enableBrowserReplay = (
            False  # Whether browser recording is enabled for this session
        )

        # MCP tools available for this session
        self.mcp_tools = []  # List[McpTool]

        # File transfer context ID
        self.file_transfer_context_id: Optional[str] = None

        # Browser recording context ID
        self.record_context_id: Optional[str] = None

        # Initialize file system, command and code handlers
        self.file_system = FileSystem(self)
        self.command = Command(self)
        self.code = Code(self)
        self.oss = Oss(self)

        # Initialize Computer and Mobile modules
        self.computer = Computer(self)
        self.mobile = Mobile(self)

        self.context = ContextManager(self)
        self.browser = Browser(self)

        self.agent = Agent(self)

    def _get_api_key(self) -> str:
        """Internal method to get the API key for this session."""
        return self.agent_bay.api_key

    def _get_client(self):
        """Internal method to get the HTTP client for this session."""
        return self.agent_bay.client

    def _get_session_id(self) -> str:
        """Internal method to get the session ID."""
        return self.session_id

    def _is_vpc_enabled(self) -> bool:
        """Internal method to check if this session uses VPC resources."""
        return self.is_vpc

    def _get_network_interface_ip(self) -> str:
        """Internal method to get the network interface IP for VPC sessions."""
        return self.network_interface_ip

    def _get_http_port(self) -> str:
        """Internal method to get the HTTP port for VPC sessions."""
        return self.http_port

    def _get_token(self) -> str:
        """Internal method to get the token for VPC sessions."""
        return self.token

    def _find_server_for_tool(self, tool_name: str) -> str:
        """Internal method to find the server that provides the given MCP tool."""
        for tool in self.mcp_tools:
            if tool.name == tool_name:
                return tool.server
        return ""

    def delete(self, sync_context: bool = False) -> DeleteResult:
        """
        Delete this session and release all associated resources.

        Args:
            sync_context (bool, optional): Whether to sync context data (trigger file uploads)
                before deleting the session. Defaults to False.

        Returns:
            DeleteResult: Result indicating success or failure with request ID.
                - success (bool): True if deletion succeeded
                - error_message (str): Error details if deletion failed
                - request_id (str): Unique identifier for this API request

        Raises:
            SessionError: If the deletion request fails or the response is invalid.

        Behavior:
            The deletion process follows these steps:
            1. If sync_context=True, synchronizes all context data before deletion
            2. If browser replay is enabled, automatically syncs recording context
            3. Calls the ReleaseMcpSession API to delete the session
            4. Returns success/failure status with request ID

            Context Synchronization:
            - When sync_context=True: Uploads all modified files in all contexts
            - When browser replay enabled: Uploads browser recording data
            - Synchronization failures do not prevent session deletion

        Example:
            ```python
            session = agent_bay.create().session
            session.command.run("echo 'Hello World'")
            session.delete()
            ```

        Note:
            - Always delete sessions when done to avoid resource leaks
            - Use sync_context=True if you need to preserve modified files
            - Browser replay data is automatically synced if enabled
            - The session object becomes invalid after deletion
            - Deletion is idempotent - deleting an already deleted session succeeds

        See Also:
            AgentBay.create, AgentBay.delete, ContextManager.sync
        """
        try:
            # Determine sync behavior based on enableBrowserReplay and sync_context
            should_sync = False
            sync_context_id = None

            if sync_context:
                # User explicitly requested sync - sync all contexts
                should_sync = True
                _logger.info("🔄 User requested context synchronization")
            elif hasattr(self, "enableBrowserReplay") and self.enableBrowserReplay:
                # Browser replay enabled but no explicit sync - sync only browser recording context
                if hasattr(self, "record_context_id") and self.record_context_id:
                    should_sync = True
                    sync_context_id = self.record_context_id
                    _logger.info(f"🎥 Browser replay enabled - syncing recording context: {sync_context_id}")
                else:
                    _logger.warning("⚠️  Browser replay enabled but no record_context_id found")

            # Perform context synchronization if needed
            if should_sync:
                _log_operation_start(
                    "Context synchronization", "Before session deletion"
                )
                import time

                sync_start_time = time.time()

                try:
                    # Use asyncio.run to call the async context.sync synchronously (no callback)
                    import asyncio

                    if sync_context_id:
                        # Sync specific context (browser recording)
                        sync_result = asyncio.run(self.context.sync(context_id=sync_context_id))
                        _logger.info(f"🎥 Synced browser recording context: {sync_context_id}")
                    else:
                        # Sync all contexts
                        sync_result = asyncio.run(self.context.sync())
                        _logger.info("🔄 Synced all contexts")

                    sync_duration = time.time() - sync_start_time

                    if sync_result.success:
                        _log_operation_success("Context sync")
                        _logger.info(
                            f"⏱️  Context sync completed in {sync_duration:.2f} seconds"
                        )
                    else:
                        _log_warning("Context sync completed with failures")
                        _logger.warning(
                            f"⏱️  Context sync failed after {sync_duration:.2f} seconds"
                        )

                except Exception as e:
                    sync_duration = time.time() - sync_start_time
                    _log_warning(f"Failed to trigger context sync: {e}")
                    _logger.warning(
                        f"⏱️  Context sync failed after {sync_duration:.2f} seconds"
                    )
                    # Continue with deletion even if sync fails

            # Proceed with session deletion
            request = ReleaseMcpSessionRequest(
                authorization=f"Bearer {self._get_api_key()}",
                session_id=self.session_id,
            )
            response = self._get_client().release_mcp_session(request)

            # Extract request ID
            request_id = extract_request_id(response)

            # Check if the response is success
            response_map = response.to_map()
            body = response_map.get("body", {})
            success = body.get("Success", True)

            if not success:
                error_message = f"[{body.get('Code', 'Unknown')}] {body.get('Message', 'Failed to delete session')}"
                _log_api_response_with_details(
                    api_name="ReleaseMcpSession",
                    request_id=request_id,
                    success=False,
                    full_response=json.dumps(body, ensure_ascii=False, indent=2)
                )
                return DeleteResult(
                    request_id=request_id,
                    success=False,
                    error_message=error_message,
                )

            # Log successful deletion
            _log_api_response_with_details(
                api_name="ReleaseMcpSession",
                request_id=request_id,
                success=True,
                key_fields={"session_id": self.session_id}
            )

            # Return success result with request ID
            return DeleteResult(request_id=request_id, success=True)

        except Exception as e:
            _log_operation_error("release_mcp_session", str(e), exc_info=True)
            # In case of error, return failure result with error message
            return DeleteResult(
                success=False,
                error_message=f"Failed to delete session {self.session_id}: {e}",
            )

    def _validate_labels(self, labels: Dict[str, str]) -> Optional[OperationResult]:
        """
        Validates labels parameter for label operations.

        Args:
            labels: The labels to validate

        Returns:
            None if validation passes, or OperationResult with error if validation fails
        """
        # Check if labels is None
        if labels is None:
            return OperationResult(
                request_id="",
                success=False,
                error_message="Labels cannot be null, undefined, or invalid type. Please provide a valid labels object.",
            )

        # Check if labels is a list (array equivalent) - check this before dict check
        if isinstance(labels, list):
            return OperationResult(
                request_id="",
                success=False,
                error_message="Labels cannot be an array. Please provide a valid labels object.",
            )

        # Check if labels is not a dict (after checking for list)
        if not isinstance(labels, dict):
            return OperationResult(
                request_id="",
                success=False,
                error_message="Labels cannot be null, undefined, or invalid type. Please provide a valid labels object.",
            )

        # Check if labels object is empty
        if len(labels) == 0:
            return OperationResult(
                request_id="",
                success=False,
                error_message="Labels cannot be empty. Please provide at least one label.",
            )

        for key, value in labels.items():
            # Check key validity
            if not key or (isinstance(key, str) and key.strip() == ""):
                return OperationResult(
                    request_id="",
                    success=False,
                    error_message="Label keys cannot be empty Please provide valid keys.",
                )

            # Check value is not None or empty
            if value is None or (isinstance(value, str) and value.strip() == ""):
                return OperationResult(
                    request_id="",
                    success=False,
                    error_message="Label values cannot be empty Please provide valid values.",
                )

        # Validation passed
        return None

    def set_labels(self, labels: Dict[str, str]) -> OperationResult:
        """
        Sets the labels for this session.

        Args:
            labels (Dict[str, str]): The labels to set for the session.

        Returns:
            OperationResult: Result indicating success or failure with request ID.

        Raises:
            SessionError: If the operation fails.

        Example:
            ```python
            labels = {"environment": "production", "version": "1.0"}
            session.set_labels(labels)
            ```
        """
        try:
            # Validate labels using the extracted validation function
            validation_result = self._validate_labels(labels)
            if validation_result is not None:
                return validation_result

            # Convert labels to JSON string
            labels_json = json.dumps(labels)

            request = SetLabelRequest(
                authorization=f"Bearer {self._get_api_key()}",
                session_id=self.session_id,
                labels=labels_json,
            )

            response = self._get_client().set_label(request)

            # Extract request ID
            request_id = extract_request_id(response)

            # Log successful label setting
            _log_api_response_with_details(
                api_name="SetLabel",
                request_id=request_id,
                success=True,
                key_fields={
                    "session_id": self.session_id,
                    "labels_count": len(labels)
                }
            )

            return OperationResult(request_id=request_id, success=True)

        except Exception as e:
            _logger.exception(f"❌ Failed to set labels for session {self.session_id}")
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

        Example:
            ```python
            result = session.get_labels()
            print(result.data)
            ```
        """
        try:
            request = GetLabelRequest(
                authorization=f"Bearer {self._get_api_key()}",
                session_id=self.session_id,
            )

            response = self._get_client().get_label(request)

            # Extract request ID
            request_id = extract_request_id(response)

            # Extract labels from response
            labels_json = (
                response.to_map().get("body", {}).get("Data", {}).get("Labels")
            )

            labels = {}
            if labels_json:
                labels = json.loads(labels_json)

            # Log successful label retrieval
            _log_api_response_with_details(
                api_name="GetLabel",
                request_id=request_id,
                success=True,
                key_fields={
                    "session_id": self.session_id,
                    "labels_count": len(labels)
                }
            )

            return OperationResult(request_id=request_id, success=True, data=labels)

        except Exception as e:
            _logger.exception(f"❌ Failed to get labels for session {self.session_id}")
            raise SessionError(
                f"Failed to get labels for session {self.session_id}: {e}"
            )

    def info(self) -> OperationResult:
        """
        Get detailed information about this session.

        Returns:
            OperationResult: Result containing SessionInfo object and request ID.
                - success (bool): Always True if no exception
                - data (SessionInfo): Session information object with fields:
                    - session_id (str): The session identifier
                    - resource_url (str): URL for accessing the session
                    - app_id (str): Application ID (for desktop sessions)
                    - auth_code (str): Authentication code
                    - connection_properties (str): Connection configuration
                    - resource_id (str): Resource identifier
                    - resource_type (str): Type of resource (e.g., "Desktop")
                    - ticket (str): Access ticket
                - request_id (str): Unique identifier for this API request

        Raises:
            SessionError: If the API request fails or response is invalid.

        Behavior:
            This method calls the GetMcpResource API to retrieve session metadata.
            The returned SessionInfo contains:
            - session_id: The session identifier
            - resource_url: URL for accessing the session
            - Desktop-specific fields (app_id, auth_code, connection_properties, etc.)
              are populated from the DesktopInfo section of the API response

        Example:
            ```python
            session = agent_bay.create().session
            info_result = session.info()
            print(info_result.data.session_id)
            ```

        Note:
            - Session info is retrieved from the AgentBay API in real-time
            - The resource_url can be used for browser-based access
            - Desktop-specific fields (app_id, auth_code) are only populated for desktop sessions
            - This method does not modify the session state

        See Also:
            AgentBay.create, Session.delete, Session.get_link
        """
        try:
            request = GetMcpResourceRequest(
                authorization=f"Bearer {self._get_api_key()}",
                session_id=self.session_id,
            )

            _log_api_call("GetMcpResource", f"SessionId={self.session_id}")

            response = self._get_client().get_mcp_resource(request)

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

            # Log successful session info retrieval
            _log_api_response_with_details(
                api_name="GetMcpResource",
                request_id=request_id,
                success=True,
                key_fields={
                    "session_id": session_info.session_id,
                    "resource_url": session_info.resource_url,
                    "resource_type": session_info.resource_type
                }
            )

            return OperationResult(
                request_id=request_id, success=True, data=session_info
            )

        except Exception as e:
            # Check if this is an expected business error (e.g., session not found)
            error_str = str(e)
            error_code = ""

            # Try to extract error code from the exception
            if hasattr(e, 'data') and hasattr(e.data, 'get'):
                error_code = e.data.get('Code', '')
            elif 'InvalidMcpSession.NotFound' in error_str or 'NotFound' in error_str:
                error_code = 'InvalidMcpSession.NotFound'

            if error_code == 'InvalidMcpSession.NotFound':
                # This is an expected error - session doesn't exist
                # Use info level logging without stack trace, but with red color for visibility
                from agentbay.logger import _log_info_with_color
                _log_info_with_color(f"Session not found: {self.session_id}")
                _logger.debug(f"GetMcpResource error details: {error_str}")
                return OperationResult(
                    request_id="",
                    success=False,
                    error_message=f"Session {self.session_id} not found"
                )
            else:
                # This is an unexpected error - log with full error
                _logger.exception(f"❌ Failed to get session info for session {self.session_id}")
                raise SessionError(
                    f"Failed to get session info for session {self.session_id}: {e}"
                )

    def get_link(
        self, protocol_type: Optional[str] = None, port: Optional[int] = None, options: Optional[str] = None
    ) -> OperationResult:
        """
        Get an access link for this session.

        Args:
            protocol_type (Optional[str], optional): The protocol type for the link.
                Defaults to None (uses session default).
            port (Optional[int], optional): The port number to expose. Must be in range [30100, 30199].
                Defaults to None.
            options (Optional[str], optional): Additional configuration as JSON string.
                Defaults to None.

        Returns:
            OperationResult: Result containing the access URL and request ID.
                - success (bool): True if the operation succeeded
                - data (str): The access URL
                - request_id (str): Unique identifier for this API request

        Raises:
            SessionError: If port is out of valid range [30100, 30199] or the API request fails.

        Example:
            ```python
            session = agent_bay.create().session
            link_result = session.get_link()
            port_link_result = session.get_link(port=30150)
            ```

        Note:
            - Port must be in range [30100, 30199] if specified
            - The returned URL format depends on the session configuration
            - For mobile ADB connections, use session.mobile.get_adb_url() instead

        See Also:
            Session.info, Session.get_link_async, Mobile.get_adb_url
        """
        try:
            # Validate port range if port is provided
            if port is not None:
                if not isinstance(port, int) or port < 30100 or port > 30199:
                    raise SessionError(
                        f"Invalid port value: {port}. Port must be an integer in the range [30100, 30199]."
                    )

            # Log API call with parameters
            _log_api_call(
                "GetLink",
                f"SessionId={self.session_id}, ProtocolType={protocol_type or 'default'}, "
                f"Port={port or 'default'}, Options={'provided' if options else 'none'}"
            )

            request = GetLinkRequest(
                authorization=f"Bearer {self._get_api_key()}",
                session_id=self._get_session_id(),
                protocol_type=protocol_type,
                port=port,
                options=options,
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
            _logger.debug(f"📊 Data: {data}")

            if not isinstance(data, dict):
                try:
                    data = json.loads(data) if isinstance(data, str) else {}
                except json.JSONDecodeError:
                    data = {}

            url = data.get("Url", "")

            # Log successful link retrieval
            _log_api_response_with_details(
                api_name="GetLink",
                request_id=request_id,
                success=True,
                key_fields={
                    "session_id": self.session_id,
                    "url": url,
                    "protocol_type": protocol_type or "default",
                    "port": port or "default"
                }
            )

            return OperationResult(request_id=request_id, success=True, data=url)

        except SessionError:
            raise
        except Exception as e:
            _logger.error(f"❌ Failed to get link for session {self.session_id}: {e}")
            raise SessionError(f"Failed to get link: {e}")

    async def get_link_async(
        self, protocol_type: Optional[str] = None, port: Optional[int] = None, options: Optional[str] = None
    ) -> OperationResult:
        """
        Asynchronously get a link associated with the current session.

        Args:
            protocol_type (Optional[str], optional): The protocol type to use for the
                link. Defaults to None.
            port (Optional[int], optional): The port to use for the link. Must be an integer in the range [30100, 30199].
                Defaults to None.
            options (Optional[str], optional): Additional options as a JSON string (e.g., for adb configuration).
                Defaults to None.

        Returns:
            OperationResult: Result containing the link as data and request ID.

        Raises:
            SessionError: If the request fails or the response is invalid.
        """
        try:
            # Validate port range if port is provided
            if port is not None:
                if not isinstance(port, int) or port < 30100 or port > 30199:
                    raise SessionError(
                        f"Invalid port value: {port}. Port must be an integer in the range [30100, 30199]."
                    )

            # Log API call with parameters
            _log_api_call(
                "GetLink (async)",
                f"SessionId={self.session_id}, ProtocolType={protocol_type or 'default'}, "
                f"Port={port or 'default'}, Options={'provided' if options else 'none'}"
            )

            request = GetLinkRequest(
                authorization=f"Bearer {self._get_api_key()}",
                session_id=self._get_session_id(),
                protocol_type=protocol_type,
                port=port,
                options=options,
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
            _logger.debug(f"📊 Data: {data}")

            if not isinstance(data, dict):
                try:
                    data = json.loads(data) if isinstance(data, str) else {}
                except json.JSONDecodeError:
                    data = {}

            url = data.get("Url", "")

            # Log successful link retrieval
            _log_api_response_with_details(
                api_name="GetLink (async)",
                request_id=request_id,
                success=True,
                key_fields={
                    "session_id": self.session_id,
                    "url": url,
                    "protocol_type": protocol_type or "default",
                    "port": port or "default"
                }
            )

            return OperationResult(request_id=request_id, success=True, data=url)

        except SessionError:
            raise
        except Exception as e:
            _logger.error(f"❌ Failed to get link asynchronously for session {self.session_id}: {e}")
            raise SessionError(f"Failed to get link asynchronously: {e}")

    def list_mcp_tools(self, image_id: Optional[str] = None):
        """
        List MCP tools available for this session.

        Args:
            image_id: Optional image ID, defaults to session's image_id or "linux_latest"

        Returns:
            Result containing tools list and request ID

        Example:
            ```python
            session = agent_bay.create().session
            tools_result = session.list_mcp_tools()
            print(f"Available tools: {len(tools_result.tools)}")
            ```
        """
        from agentbay.api.models import ListMcpToolsRequest
        from agentbay.model.response import McpToolsResult
        from agentbay.models.mcp_tool import McpTool
        import json

        # Use provided image_id, session's image_id, or default
        if image_id is None:
            image_id = getattr(self, "image_id", "") or "linux_latest"

        request = ListMcpToolsRequest(
            authorization=f"Bearer {self._get_api_key()}", image_id=image_id
        )

        _log_api_call("ListMcpTools", f"ImageId={image_id}")

        response = self._get_client().list_mcp_tools(request)

        # Extract request ID
        request_id = extract_request_id(response)

        if response and response.body:
            _logger.debug(f"📥 Response from ListMcpTools: {response.body}")

        # Parse the response data
        tools = []
        if response and response.body and response.body.data:
            # The Data field is a JSON string, so we need to unmarshal it
            try:
                tools_data = json.loads(response.body.data)
                for tool_data in tools_data:
                    tool = McpTool(
                        name=tool_data.get("name", ""),
                        description=tool_data.get("description", ""),
                        input_schema=tool_data.get("inputSchema", {}),
                        server=tool_data.get("server", ""),
                        tool=tool_data.get("tool", ""),
                    )
                    tools.append(tool)
            except json.JSONDecodeError as e:
                _logger.error(f"❌ Error unmarshaling tools data: {e}")

        self.mcp_tools = tools  # Update the session's mcp_tools field

        # Log successful tools retrieval
        _log_api_response_with_details(
            api_name="ListMcpTools",
            request_id=request_id,
            success=True,
            key_fields={
                "image_id": image_id,
                "tools_count": len(tools)
            }
        )

        return McpToolsResult(request_id=request_id, tools=tools)

    def call_mcp_tool(
        self,
        tool_name: str,
        args: Dict[str, Any],
        read_timeout: Optional[int] = None,
        connect_timeout: Optional[int] = None,
        auto_gen_session: bool = False,
    ):
        """
        Call an MCP tool directly.

        This is the unified public API for calling MCP tools. All feature modules
        (Command, Code, Agent, etc.) use this method internally.

        Args:
            tool_name: Name of the MCP tool to call
            args: Arguments to pass to the tool as a dictionary
            read_timeout: Optional read timeout in seconds
            connect_timeout: Optional connection timeout in seconds
            auto_gen_session: Whether to automatically generate session if not exists (default: False)

        Returns:
            McpToolResult: Result containing success status, data, and error message

        Example:
            ```python
            result = session.call_mcp_tool("shell", {"command": "echo 'Hello World'", "timeout_ms": 1000})
            result = session.call_mcp_tool("shell", {"command": "pwd", "timeout_ms": 1000}, read_timeout=30, connect_timeout=10)
            result = session.call_mcp_tool("shell", {"command": "invalid_command_12345", "timeout_ms": 1000})
            ```

        Note:
            - For press_keys tool, key names are automatically normalized to correct case format
            - This improves case compatibility (e.g., "CTRL" -> "Ctrl", "tab" -> "Tab")
        """
        from agentbay.model import McpToolResult
        from agentbay.api.models import CallMcpToolRequest
        import requests

        try:
            # Normalize press_keys arguments for better case compatibility
            if tool_name == "press_keys" and "keys" in args:
                from agentbay.key_normalizer import normalize_keys
                args = args.copy()  # Don't modify the original args
                args["keys"] = normalize_keys(args["keys"])
                _logger.debug(f"Normalized press_keys arguments: {args}")

            args_json = json.dumps(args, ensure_ascii=False)

            # Check if this is a VPC session
            if self._is_vpc_enabled():
                return self._call_mcp_tool_vpc(tool_name, args_json)

            # Non-VPC mode: use traditional API call
            return self._call_mcp_tool_api(
                tool_name, args_json, read_timeout, connect_timeout, auto_gen_session
            )
        except Exception as e:
            _logger.error(f"❌ Failed to call MCP tool {tool_name}: {e}")
            return McpToolResult(
                request_id="",
                success=False,
                data="",
                error_message=f"Failed to call MCP tool: {e}",
            )

    def _call_mcp_tool_vpc(self, tool_name: str, args_json: str):
        """
        Handle VPC-based MCP tool calls using HTTP requests.

        Args:
            tool_name: Name of the tool to call
            args_json: JSON string of arguments

        Returns:
            McpToolResult: The response from the tool
        """
        from agentbay.model import McpToolResult
        import requests
        import time
        import random
        import string

        _log_api_call(f"CallMcpTool (VPC) - {tool_name}", f"Args={args_json}")

        # Find server for this tool
        server = self._find_server_for_tool(tool_name)
        if not server:
            _log_operation_error(
                "CallMcpTool(VPC)",
                f"server not found for tool: {tool_name}",
                False,
            )
            return McpToolResult(
                request_id="",
                success=False,
                data="",
                error_message=f"server not found for tool: {tool_name}",
            )

        # Check VPC network configuration
        if not self._get_network_interface_ip() or not self._get_http_port():
            _log_operation_error(
                "CallMcpTool(VPC)",
                f"VPC network configuration incomplete: networkInterfaceIp={self._get_network_interface_ip()}, httpPort={self._get_http_port()}",
                False,
            )
            return McpToolResult(
                request_id="",
                success=False,
                data="",
                error_message=f"VPC network configuration incomplete: networkInterfaceIp={self._get_network_interface_ip()}, httpPort={self._get_http_port()}",
            )

        # Construct VPC URL with query parameters
        base_url = f"http://{self._get_network_interface_ip()}:{self._get_http_port()}/callTool"

        # Prepare query parameters
        request_id = f"vpc-{int(time.time() * 1000)}-{''.join(random.choices(string.ascii_lowercase + string.digits, k=9))}"
        params = {
            "server": server,
            "tool": tool_name,
            "args": args_json,
            "token": self._get_token(),
            "requestId": request_id,
        }

        # Set headers
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        try:
            # Send HTTP request
            response = requests.get(
                base_url, params=params, headers=headers, timeout=30
            )
            response.raise_for_status()

            # Parse response
            response_data = response.json()

            # Extract content
            content = response_data.get("content", [])
            is_error = response_data.get("isError", False)

            # Extract text from content
            text_content = ""
            if content and isinstance(content, list) and len(content) > 0:
                first_content = content[0]
                if isinstance(first_content, dict):
                    text_content = first_content.get("text", "")

            if is_error:
                _log_operation_error(
                    "CallMcpTool(VPC)",
                    f"Tool returned error: {text_content}",
                    False,
                )
                return McpToolResult(
                    request_id=request_id,
                    success=False,
                    data="",
                    error_message=text_content,
                )

            _log_api_response_with_details(
                "CallMcpTool(VPC)",
                request_id,
                True,
                {"tool": tool_name},
                text_content[:200] if text_content else "",
            )

            return McpToolResult(
                request_id=request_id,
                success=True,
                data=text_content,
                error_message="",
            )

        except requests.exceptions.RequestException as e:
            _log_operation_error(
                "CallMcpTool(VPC)", f"HTTP request failed: {e}", True
            )
            return McpToolResult(
                request_id=request_id,
                success=False,
                data="",
                error_message=f"HTTP request failed: {e}",
            )
        except Exception as e:
            _log_operation_error(
                "CallMcpTool(VPC)", f"Unexpected error: {e}", True
            )
            return McpToolResult(
                request_id=request_id,
                success=False,
                data="",
                error_message=f"Unexpected error: {e}",
            )

    def _call_mcp_tool_api(
        self,
        tool_name: str,
        args_json: str,
        read_timeout: Optional[int] = None,
        connect_timeout: Optional[int] = None,
        auto_gen_session: bool = False,
    ):
        """
        Handle traditional API-based MCP tool calls.

        Args:
            tool_name: Name of the tool to call
            args_json: JSON string of arguments
            read_timeout: Optional read timeout in seconds
            connect_timeout: Optional connection timeout in seconds
            auto_gen_session: Whether to automatically generate session if not exists

        Returns:
            McpToolResult: The response from the tool
        """
        from agentbay.model import McpToolResult
        from agentbay.api.models import CallMcpToolRequest

        _log_api_call(
            "CallMcpTool",
            f"Tool={tool_name}, SessionId={self.session_id}, ArgsLength={len(args_json)}",
        )

        request = CallMcpToolRequest(
            authorization=f"Bearer {self._get_api_key()}",
            session_id=self.session_id,
            name=tool_name,
            args=args_json,
            auto_gen_session=auto_gen_session,
        )

        try:
            response = self._get_client().call_mcp_tool(
                request, read_timeout=read_timeout, connect_timeout=connect_timeout
            )

            # Extract request ID
            request_id = extract_request_id(response)

            # Check for API-level errors
            response_map = response.to_map()
            if not response_map:
                return McpToolResult(
                    request_id=request_id,
                    success=False,
                    data="",
                    error_message="Invalid response format",
                )

            body = response_map.get("body", {})
            if not body:
                return McpToolResult(
                    request_id=request_id,
                    success=False,
                    data="",
                    error_message="Invalid response body",
                )

            # Parse the Data field
            data_str = body.get("Data", "")
            if not data_str:
                return McpToolResult(
                    request_id=request_id,
                    success=False,
                    data="",
                    error_message="Empty response data",
                )

            # Parse JSON data
            try:
                # Handle both string and dict responses
                if isinstance(data_str, dict):
                    data_obj = data_str
                else:
                    data_obj = json.loads(data_str)
            except json.JSONDecodeError as e:
                return McpToolResult(
                    request_id=request_id,
                    success=False,
                    data="",
                    error_message=f"Failed to parse response data: {e}",
                )

            # Extract content
            content = data_obj.get("content", [])
            is_error = data_obj.get("isError", False)

            # Extract text from content
            text_content = ""
            if content and isinstance(content, list) and len(content) > 0:
                first_content = content[0]
                if isinstance(first_content, dict):
                    text_content = first_content.get("text", "")

            if is_error:
                _log_operation_error(
                    "CallMcpTool", f"Tool returned error: {text_content}", False
                )
                return McpToolResult(
                    request_id=request_id,
                    success=False,
                    data="",
                    error_message=text_content,
                )

            _log_api_response_with_details(
                "CallMcpTool",
                request_id,
                True,
                {"tool": tool_name},
                text_content[:200] if text_content else "",
            )

            return McpToolResult(
                request_id=request_id,
                success=True,
                data=text_content,
                error_message="",
            )

        except Exception as e:
            _log_operation_error("CallMcpTool", f"API request failed: {e}", True)
            return McpToolResult(
                request_id="",
                success=False,
                data="",
                error_message=f"API request failed: {e}",
            )

    def pause(self, timeout: int = 600, poll_interval: float = 2.0) -> SessionPauseResult:
        """
        Synchronously pause this session, putting it into a dormant state.

        This method internally calls the PauseSessionAsync API and then polls the GetSession API
        to check the session status until it becomes PAUSED or until timeout.

        Args:
            timeout (int, optional): Timeout in seconds to wait for the session to pause.
                Defaults to 600 seconds.
            poll_interval (float, optional): Interval in seconds between status polls.
                Defaults to 2.0 seconds.

        Returns:
            SessionPauseResult: Result containing the request ID, success status, and final session status.
                - success (bool): True if the session was successfully paused
                - request_id (str): Unique identifier for this API request
                - status (str): Final session status (should be "PAUSED" if successful)
                - error_message (str): Error description (if success is False)
                - code (str): API response code (if available)
                - message (str): API response message (if available)
                - http_status_code (int): HTTP status code (if available)

        Raises:
            SessionError: If the API request fails or response is invalid.

        Example:
            ```python
            session = agent_bay.create().session
            pause_result = session.pause()
            session.resume()
            session.delete()
            ```

        Note:
            - The session state transitions from RUNNING -> PAUSING -> PAUSED
            - Paused sessions consume fewer resources but maintain their state
            - Use resume() or resume_async() to restore the session to RUNNING state
            - The timeout parameter controls how long to wait for the PAUSED state
            - If timeout is exceeded, the method returns with success=False

        See Also:
            Session.pause_async, Session.resume, Session.resume_async, AgentBay.pause, AgentBay.pause_async
        """
        try:
            # Use asyncio.run to call the async pause API and poll for status
            # This allows us to reuse the async implementation in a synchronous context
            import asyncio
            import threading

            # Create a new event loop if there isn't one already
            try:
                loop = asyncio.get_running_loop()
                # If we're already in an event loop, run in a new thread with a new event loop
                # This prevents deadlock when calling synchronous pause() from async context
                result_container = []
                exception_container = []

                def run_in_thread():
                    try:
                        # Create a new event loop for this thread
                        new_loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(new_loop)
                        try:
                            result = new_loop.run_until_complete(self.pause_async(timeout, poll_interval))
                            result_container.append(result)
                        finally:
                            new_loop.close()
                    except Exception as e:
                        exception_container.append(e)

                thread = threading.Thread(target=run_in_thread)
                thread.start()
                thread.join()

                if exception_container:
                    raise exception_container[0]
                if result_container:
                    return result_container[0]

            except RuntimeError:
                # No event loop running, we can use asyncio.run
                result = asyncio.run(self.pause_async(timeout, poll_interval))
                return result
        except Exception as e:
            _log_operation_error("PauseSession", str(e), exc_info=True)
            return SessionPauseResult(
                request_id="",
                success=False,
                error_message=f"Unexpected error pausing session: {e}",
            )

    async def pause_async(self, timeout: int = 600, poll_interval: float = 2.0) -> SessionPauseResult:
        """
        Asynchronously pause this session, putting it into a dormant state.

        This method directly calls the PauseSessionAsync API and then polls the GetSession API
        asynchronously to check the session status until it becomes PAUSED or until timeout.

        Args:
            timeout (int, optional): Timeout in seconds to wait for the session to pause.
                Defaults to 600 seconds.
            poll_interval (float, optional): Interval in seconds between status polls.
                Defaults to 2.0 seconds.

        Returns:
            SessionPauseResult: Result containing the request ID, success status, and final session status.
                - success (bool): True if the session was successfully paused
                - request_id (str): Unique identifier for this API request
                - status (str): Final session status (should be "PAUSED" if successful)
                - error_message (str): Error description (if success is False)
                - code (str): API response code (if available)
                - message (str): API response message (if available)
                - http_status_code (int): HTTP status code (if available)

        Raises:
            SessionError: If the API request fails or response is invalid.

        Example:
            ```python
            import asyncio

            session = agent_bay.create().session
            pause_result = await session.pause_async()
            await session.resume_async()
            session.delete()
            ```

        Note:
            - The session state transitions from RUNNING -> PAUSING -> PAUSED
            - Paused sessions consume fewer resources but maintain their state
            - Use resume() or resume_async() to restore the session to RUNNING state
            - The timeout parameter controls how long to wait for the PAUSED state
            - If timeout is exceeded, the method returns with success=False

        See Also:
            Session.pause, Session.resume, Session.resume_async, AgentBay.pause_async
        """
        try:
            import asyncio
            from agentbay.api.models import PauseSessionAsyncRequest
            
            request = PauseSessionAsyncRequest(
                authorization=f"Bearer {self._get_api_key()}",
                session_id=self.session_id,
            )

            _log_api_call("PauseSessionAsync", f"SessionId={self.session_id}")

            response = await self._get_client().pause_session_async_async(request)

            # Extract request ID
            request_id = extract_request_id(response)

            # Check for API-level errors
            response_map = response.to_map()
            if not response_map:
                result = SessionPauseResult(
                    request_id=request_id,
                    success=False,
                    error_message="Invalid response format",
                )

                return result

            body = response_map.get("body", {})
            if not body:
                result = SessionPauseResult(
                    request_id=request_id,
                    success=False,
                    error_message="Invalid response body",
                )
                return result

            # Extract fields from response body
            success = body.get("Success", False)
            code = body.get("Code", "")
            message = body.get("Message", "")
            http_status_code = body.get("HttpStatusCode", 0)
            # Log API response with key details
            _log_api_response_with_details(
                api_name="PauseSessionAsync",
                request_id=request_id,
                success=True,
                key_fields={
                    "session_id": self.session_id
                }
            )
            # Build error message if not successful
            if not success:
                error_message = f"[{code}] {message}" if code or message else "Unknown error"
                _log_operation_error("PauseSessionAsync", error_message)
                result = SessionPauseResult(
                    request_id=request_id,
                    success=False,
                    error_message=error_message,
                    code=code,
                    message=message,
                    http_status_code=http_status_code,
                )
                return result

            _log_operation_success("PauseSessionAsync", f"Session {self.session_id} pause initiated successfully")

            # Poll for session status until PAUSED or timeout
            import time
            start_time = time.time()
            max_attempts = int(timeout / poll_interval)
            attempt = 0

            while attempt < max_attempts:
                # Get session status
                get_result = self.agent_bay.get_session(self.session_id)
                if not get_result.success:
                    error_msg = f"Failed to get session status: {get_result.error_message}"
                    _logger.error(error_msg)
                    result = SessionPauseResult(
                        request_id=get_result.request_id,
                        success=False,
                        error_message=error_msg,
                    )
                    return result

                # Check session status
                if get_result.data:
                    status = getattr(get_result.data, 'status', None) or "UNKNOWN"
                    _logger.info(f"Session status: {status} (attempt {attempt + 1}/{max_attempts})")

                    # Check if session is paused
                    if status == "PAUSED":
                        elapsed = time.time() - start_time
                        _logger.info(f"Session paused successfully in {elapsed:.2f} seconds")
                        result = SessionPauseResult(
                            request_id=get_result.request_id,
                            success=True,
                            status=status,
                        )
                        return result
                    elif status not in ("RUNNING", "PAUSING"):
                        # If status is not RUNNING, PAUSING, or PAUSED, treat as unexpected
                        elapsed = time.time() - start_time
                        _logger.warning(f"Session in unexpected state after {elapsed:.2f} seconds: {status}")
                        # Continue polling as the state might transition to PAUSED

                # Wait before next query (using asyncio.sleep to avoid blocking)
                # Only wait if we're not at the last attempt
                attempt += 1
                if attempt < max_attempts:
                    await asyncio.sleep(poll_interval)

            # Timeout
            elapsed = time.time() - start_time
            error_msg = f"Session pause timed out after {elapsed:.2f} seconds"
            _logger.error(error_msg)
            result = SessionPauseResult(
                request_id="",
                success=False,
                error_message=error_msg,
            )
            return result

        except Exception as e:
            _log_operation_error("PauseSessionAsync", str(e))
            result = SessionPauseResult(
                request_id="",
                success=False,
                error_message=f"Unexpected error pausing session: {e}",
            )
            return result

    def resume(self, timeout: int = 600, poll_interval: float = 2.0) -> SessionResumeResult:
        """
        Synchronously resume this session from a paused state.

        This method internally calls the ResumeSessionAsync API and then polls the GetSession API
        to check the session status until it becomes RUNNING or until timeout.

        Args:
            timeout (int, optional): Timeout in seconds to wait for the session to resume.
                Defaults to 600 seconds.
            poll_interval (float, optional): Interval in seconds between status polls.
                Defaults to 2.0 seconds.

        Returns:
            SessionResumeResult: Result containing the request ID, success status, and final session status.
                - success (bool): True if the session was successfully resumed
                - request_id (str): Unique identifier for this API request
                - status (str): Final session status (should be "RUNNING" if successful)
                - error_message (str): Error description (if success is False)
                - code (str): API response code (if available)
                - message (str): API response message (if available)
                - http_status_code (int): HTTP status code (if available)

        Raises:
            SessionError: If the API request fails or response is invalid.

        Example:
            ```python
            session = agent_bay.create().session
            session.pause()
            resume_result = session.resume()
            session.delete()
            ```

        Note:
            - The session state transitions from PAUSED -> RESUMING -> RUNNING
            - Only sessions in PAUSED state can be resumed
            - Use pause() or pause_async() to put a session into PAUSED state
            - The timeout parameter controls how long to wait for the RUNNING state
            - If timeout is exceeded, the method returns with success=False

        See Also:
            Session.pause, Session.pause_async, Session.resume_async, AgentBay.resume, AgentBay.resume_async
        """
        try:
            # Use asyncio.run to call the async resume API and poll for status
            # This allows us to reuse the async implementation in a synchronous context
            import asyncio
            import threading

            # Create a new event loop if there isn't one already
            try:
                loop = asyncio.get_running_loop()
                # If we're already in an event loop, run in a new thread with a new event loop
                # This prevents deadlock when calling synchronous resume() from async context
                result_container = []
                exception_container = []

                def run_in_thread():
                    try:
                        # Create a new event loop for this thread
                        new_loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(new_loop)
                        try:
                            result = new_loop.run_until_complete(self.resume_async(timeout, poll_interval))
                            result_container.append(result)
                        finally:
                            new_loop.close()
                    except Exception as e:
                        exception_container.append(e)

                thread = threading.Thread(target=run_in_thread)
                thread.start()
                thread.join()

                if exception_container:
                    raise exception_container[0]
                if result_container:
                    return result_container[0]

            except RuntimeError:
                # No event loop running, we can use asyncio.run
                result = asyncio.run(self.resume_async(timeout, poll_interval))
                return result
        except Exception as e:
            _log_operation_error("ResumeSession", str(e), exc_info=True)
            return SessionResumeResult(
                request_id="",
                success=False,
                error_message=f"Unexpected error resuming session: {e}",
            )

    async def resume_async(self, timeout: int = 600, poll_interval: float = 2.0) -> SessionResumeResult:
        """
        Asynchronously resume this session from a paused state.

        This method directly calls the ResumeSessionAsync API and then polls the GetSession API
        asynchronously to check the session status until it becomes RUNNING or until timeout.

        Args:
            timeout (int, optional): Timeout in seconds to wait for the session to resume.
                Defaults to 600 seconds.
            poll_interval (float, optional): Interval in seconds between status polls.
                Defaults to 2.0 seconds.

        Returns:
            SessionResumeResult: Result containing the request ID, success status, and final session status.
                - success (bool): True if the session was successfully resumed
                - request_id (str): Unique identifier for this API request
                - status (str): Final session status (should be "RUNNING" if successful)
                - error_message (str): Error description (if success is False)
                - code (str): API response code (if available)
                - message (str): API response message (if available)
                - http_status_code (int): HTTP status code (if available)

        Raises:
            SessionError: If the API request fails or response is invalid.

        Example:
            ```python
            import asyncio

            session = agent_bay.create().session
            session.pause()
            resume_result = await session.resume_async()
            session.delete()
            ```

        Note:
            - The session state transitions from PAUSED -> RESUMING -> RUNNING
            - Only sessions in PAUSED state can be resumed
            - Use pause() or pause_async() to put a session into PAUSED state
            - The timeout parameter controls how long to wait for the RUNNING state
            - If timeout is exceeded, the method returns with success=False

        See Also:
            Session.pause, Session.pause_async, Session.resume, AgentBay.resume_async
        """
        try:
            import asyncio
            from agentbay.api.models import ResumeSessionAsyncRequest
            
            request = ResumeSessionAsyncRequest(
                authorization=f"Bearer {self._get_api_key()}",
                session_id=self.session_id,
            )

            _log_api_call("ResumeSessionAsync", f"SessionId={self.session_id}")

            response = await self._get_client().resume_session_async_async(request)

            # Extract request ID
            request_id = extract_request_id(response)

            # Check for API-level errors
            response_map = response.to_map()
            if not response_map:
                result = SessionResumeResult(
                    request_id=request_id,
                    success=False,
                    error_message="Invalid response format",
                )
                return result
            body = response_map.get("body", {})
            if not body:
                result = SessionResumeResult(
                    request_id=request_id,
                    success=False,
                    error_message="Invalid response body",
                )
                return result

            # Extract fields from response body
            success = body.get("Success", False)
            code = body.get("Code", "")
            message = body.get("Message", "")
            http_status_code = body.get("HttpStatusCode", 0)
            
            # Build error message if not successful
            if not success:
                error_message = f"[{code}] {message}" if code or message else "Unknown error"
                _log_operation_error("ResumeSessionAsync", error_message)
                result = SessionResumeResult(
                    request_id=request_id,
                    success=False,
                    error_message=error_message,
                    code=code,
                    message=message,
                    http_status_code=http_status_code,
                )
                return result
            # Log API response with key details

            _log_api_response_with_details(
                api_name="ResumeSessionAsync",
                request_id=request_id,
                success=True,
                key_fields={
                    "session_id": self.session_id,
                }
            )
            _log_operation_success("ResumeSessionAsync", f"Session {self.session_id} resume initiated successfully")
            
            # Poll for session status until RUNNING or timeout
            import time
            start_time = time.time()
            max_attempts = int(timeout / poll_interval)
            attempt = 0

            while attempt < max_attempts:
                # Get session status
                get_result = self.agent_bay.get_session(self.session_id)
                if not get_result.success:
                    error_msg = f"Failed to get session status: {get_result.error_message}"
                    _logger.error(error_msg)
                    result = SessionResumeResult(
                        request_id=get_result.request_id,
                        success=False,
                        error_message=error_msg,
                    )
                    return result

                # Check session status
                if get_result.data:
                    status = getattr(get_result.data, 'status', None) or "UNKNOWN"
                    _logger.info(f"Session status: {status} (attempt {attempt + 1}/{max_attempts})")

                    # Check if session is running
                    if status == "RUNNING":
                        elapsed = time.time() - start_time
                        _logger.info(f"Session resumed successfully in {elapsed:.2f} seconds")
                        result = SessionResumeResult(
                            request_id=get_result.request_id,
                            success=True,
                            status=status,
                        )
                        return result
                    elif status not in ("PAUSED", "RESUMING"):
                        # If status is not PAUSED, RESUMING, or RUNNING, treat as unexpected
                        elapsed = time.time() - start_time
                        _logger.warning(f"Session in unexpected state after {elapsed:.2f} seconds: {status}")
                        # Continue polling as the state might transition to RUNNING

                # Wait before next query (using asyncio.sleep to avoid blocking)
                # Only wait if we're not at the last attempt
                attempt += 1
                if attempt < max_attempts:
                    await asyncio.sleep(poll_interval)

            # Timeout
            elapsed = time.time() - start_time
            error_msg = f"Session resume timed out after {elapsed:.2f} seconds"
            _logger.error(error_msg)
            result = SessionResumeResult(
                request_id="",
                success=False,
                error_message=error_msg,
            )
            return result

        except Exception as e:
            _log_operation_error("ResumeSessionAsync", str(e))
            result = SessionResumeResult(
                request_id="",
                success=False,
                error_message=f"Unexpected error resuming session: {e}",
            )
            return result
