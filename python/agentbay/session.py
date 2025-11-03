import json
from typing import TYPE_CHECKING, Any, Dict, Optional
from .logger import (
    get_logger,
    log_api_call,
    log_api_response,
    log_api_response_with_details,
    log_operation_start,
    log_operation_success,
    log_operation_error,
    log_warning,
)

from agentbay.api.models import (
    GetLabelRequest,
    GetLinkRequest,
    GetLinkResponse,
    GetMcpResourceRequest,
    ReleaseMcpSessionRequest,
    SetLabelRequest,
)
from agentbay.application import ApplicationManager
from agentbay.code import Code
from agentbay.command import Command
from agentbay.computer import Computer
from agentbay.exceptions import SessionError
from agentbay.filesystem import FileSystem
from agentbay.mobile import Mobile
from agentbay.model import DeleteResult, OperationResult, extract_request_id
from agentbay.oss import Oss
from agentbay.ui import UI
from agentbay.agent import Agent
from agentbay.window import WindowManager
from agentbay.context_manager import ContextManager

if TYPE_CHECKING:
    from agentbay.agentbay import AgentBay

from agentbay.browser import Browser

# Initialize logger for this module
logger = get_logger("session")


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

        # Initialize application and window managers
        self.application = ApplicationManager(self)
        self.window = WindowManager(self)

        # Initialize Computer and Mobile modules
        self.computer = Computer(self)
        self.mobile = Mobile(self)

        self.ui = UI(self)
        self.context = ContextManager(self)
        self.browser = Browser(self)

        self.agent = Agent(self)

    def get_api_key(self) -> str:
        """Return the API key for this session."""
        return self.agent_bay.api_key

    def get_client(self):
        """Return the HTTP client for this session."""
        return self.agent_bay.client

    def get_session_id(self) -> str:
        """Return the session_id for this session."""
        return self.session_id

    def is_vpc_enabled(self) -> bool:
        """Return whether this session uses VPC resources."""
        return self.is_vpc

    def get_network_interface_ip(self) -> str:
        """Return the network interface IP for VPC sessions."""
        return self.network_interface_ip

    def get_http_port(self) -> str:
        """Return the HTTP port for VPC sessions."""
        return self.http_port

    def get_token(self) -> str:
        """Return the token for VPC sessions."""
        return self.token

    def find_server_for_tool(self, tool_name: str) -> str:
        """Find the server that provides the given tool."""
        for tool in self.mcp_tools:
            if tool.name == tool_name:
                return tool.server
        return ""

    def delete(self, sync_context: bool = False) -> DeleteResult:
        """
        Delete this session.

        Args:
            sync_context (bool): Whether to sync context data (trigger file uploads)
                before deleting the session. Defaults to False.

        Returns:
            DeleteResult: Result indicating success or failure and request ID.
        """
        try:
            # Determine sync behavior based on enableBrowserReplay and sync_context
            should_sync = False
            sync_context_id = None

            if sync_context:
                # User explicitly requested sync - sync all contexts
                should_sync = True
                logger.info("🔄 User requested context synchronization")
            elif hasattr(self, "enableBrowserReplay") and self.enableBrowserReplay:
                # Browser replay enabled but no explicit sync - sync only browser recording context
                if hasattr(self, "record_context_id") and self.record_context_id:
                    should_sync = True
                    sync_context_id = self.record_context_id
                    logger.info(f"🎥 Browser replay enabled - syncing recording context: {sync_context_id}")
                else:
                    logger.warning("⚠️  Browser replay enabled but no record_context_id found")

            # Perform context synchronization if needed
            if should_sync:
                log_operation_start(
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
                        logger.info(f"🎥 Synced browser recording context: {sync_context_id}")
                    else:
                        # Sync all contexts
                        sync_result = asyncio.run(self.context.sync())
                        logger.info("🔄 Synced all contexts")

                    sync_duration = time.time() - sync_start_time

                    if sync_result.success:
                        log_operation_success("Context sync")
                        logger.info(
                            f"⏱️  Context sync completed in {sync_duration:.2f} seconds"
                        )
                    else:
                        log_warning("Context sync completed with failures")
                        logger.warning(
                            f"⏱️  Context sync failed after {sync_duration:.2f} seconds"
                        )

                except Exception as e:
                    sync_duration = time.time() - sync_start_time
                    log_warning(f"Failed to trigger context sync: {e}")
                    logger.warning(
                        f"⏱️  Context sync failed after {sync_duration:.2f} seconds"
                    )
                    # Continue with deletion even if sync fails

            # Proceed with session deletion
            request = ReleaseMcpSessionRequest(
                authorization=f"Bearer {self.get_api_key()}",
                session_id=self.session_id,
            )
            response = self.get_client().release_mcp_session(request)

            # Extract request ID
            request_id = extract_request_id(response)

            # Check if the response is success
            response_map = response.to_map()
            body = response_map.get("body", {})
            success = body.get("Success", True)

            if not success:
                error_message = f"[{body.get('Code', 'Unknown')}] {body.get('Message', 'Failed to delete session')}"
                log_api_response_with_details(
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
            log_api_response_with_details(
                api_name="ReleaseMcpSession",
                request_id=request_id,
                success=True,
                key_fields={"session_id": self.session_id}
            )

            # Return success result with request ID
            return DeleteResult(request_id=request_id, success=True)

        except Exception as e:
            log_operation_error("release_mcp_session", str(e), exc_info=True)
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
        """
        try:
            # Validate labels using the extracted validation function
            validation_result = self._validate_labels(labels)
            if validation_result is not None:
                return validation_result

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

            # Log successful label setting
            log_api_response_with_details(
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
            logger.exception(f"❌ Failed to set labels for session {self.session_id}")
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

            # Log successful label retrieval
            log_api_response_with_details(
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
            logger.exception(f"❌ Failed to get labels for session {self.session_id}")
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

            log_api_call("GetMcpResource", f"SessionId={self.session_id}")

            response = self.get_client().get_mcp_resource(request)

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
            log_api_response_with_details(
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
            logger.exception(f"❌ Failed to get session info for session {self.session_id}")
            raise SessionError(
                f"Failed to get session info for session {self.session_id}: {e}"
            )

    def get_link(
        self, protocol_type: Optional[str] = None, port: Optional[int] = None, options: Optional[str] = None
    ) -> OperationResult:
        """
        Get a link associated with the current session.

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
            log_api_call(
                "GetLink",
                f"SessionId={self.session_id}, ProtocolType={protocol_type or 'default'}, "
                f"Port={port or 'default'}, Options={'provided' if options else 'none'}"
            )

            request = GetLinkRequest(
                authorization=f"Bearer {self.get_api_key()}",
                session_id=self.get_session_id(),
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
            logger.debug(f"📊 Data: {data}")

            if not isinstance(data, dict):
                try:
                    data = json.loads(data) if isinstance(data, str) else {}
                except json.JSONDecodeError:
                    data = {}

            url = data.get("Url", "")

            # Log successful link retrieval
            log_api_response_with_details(
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
            logger.error(f"❌ Failed to get link for session {self.session_id}: {e}")
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
            log_api_call(
                "GetLink (async)",
                f"SessionId={self.session_id}, ProtocolType={protocol_type or 'default'}, "
                f"Port={port or 'default'}, Options={'provided' if options else 'none'}"
            )

            request = GetLinkRequest(
                authorization=f"Bearer {self.get_api_key()}",
                session_id=self.get_session_id(),
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
            logger.debug(f"📊 Data: {data}")

            if not isinstance(data, dict):
                try:
                    data = json.loads(data) if isinstance(data, str) else {}
                except json.JSONDecodeError:
                    data = {}

            url = data.get("Url", "")

            # Log successful link retrieval
            log_api_response_with_details(
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
            logger.error(f"❌ Failed to get link asynchronously for session {self.session_id}: {e}")
            raise SessionError(f"Failed to get link asynchronously: {e}")

    def list_mcp_tools(self, image_id: Optional[str] = None):
        """
        List MCP tools available for this session.

        Args:
            image_id: Optional image ID, defaults to session's image_id or "linux_latest"

        Returns:
            Result containing tools list and request ID
        """
        from agentbay.api.models import ListMcpToolsRequest
        from agentbay.model.response import McpToolsResult
        from agentbay.models.mcp_tool import McpTool
        import json

        # Use provided image_id, session's image_id, or default
        if image_id is None:
            image_id = getattr(self, "image_id", "") or "linux_latest"

        request = ListMcpToolsRequest(
            authorization=f"Bearer {self.get_api_key()}", image_id=image_id
        )

        log_api_call("ListMcpTools", f"ImageId={image_id}")

        response = self.get_client().list_mcp_tools(request)

        # Extract request ID
        request_id = extract_request_id(response)

        if response and response.body:
            logger.debug(f"📥 Response from ListMcpTools: {response.body}")

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
                logger.error(f"❌ Error unmarshaling tools data: {e}")

        self.mcp_tools = tools  # Update the session's mcp_tools field

        # Log successful tools retrieval
        log_api_response_with_details(
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
            >>> result = session.call_mcp_tool("shell", {"command": "ls", "timeout_ms": 1000})
            >>> if result.success:
            >>>     print(result.data)
        """
        from agentbay.model import McpToolResult
        from agentbay.api.models import CallMcpToolRequest
        import requests

        try:
            args_json = json.dumps(args, ensure_ascii=False)

            # Check if this is a VPC session
            if self.is_vpc_enabled():
                return self._call_mcp_tool_vpc(tool_name, args_json)

            # Non-VPC mode: use traditional API call
            return self._call_mcp_tool_api(
                tool_name, args_json, read_timeout, connect_timeout, auto_gen_session
            )
        except Exception as e:
            logger.error(f"❌ Failed to call MCP tool {tool_name}: {e}")
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

        log_api_call(f"CallMcpTool (VPC) - {tool_name}", f"Args={args_json}")

        # Find server for this tool
        server = self.find_server_for_tool(tool_name)
        if not server:
            log_operation_error(
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
        if not self.get_network_interface_ip() or not self.get_http_port():
            log_operation_error(
                "CallMcpTool(VPC)",
                f"VPC network configuration incomplete: networkInterfaceIp={self.get_network_interface_ip()}, httpPort={self.get_http_port()}",
                False,
            )
            return McpToolResult(
                request_id="",
                success=False,
                data="",
                error_message=f"VPC network configuration incomplete: networkInterfaceIp={self.get_network_interface_ip()}, httpPort={self.get_http_port()}",
            )

        # Construct VPC URL with query parameters
        base_url = f"http://{self.get_network_interface_ip()}:{self.get_http_port()}/callTool"

        # Prepare query parameters
        request_id = f"vpc-{int(time.time() * 1000)}-{''.join(random.choices(string.ascii_lowercase + string.digits, k=9))}"
        params = {
            "server": server,
            "tool": tool_name,
            "args": args_json,
            "token": self.get_token(),
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
                log_operation_error(
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

            log_api_response_with_details(
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
            log_operation_error(
                "CallMcpTool(VPC)", f"HTTP request failed: {e}", True
            )
            return McpToolResult(
                request_id=request_id,
                success=False,
                data="",
                error_message=f"HTTP request failed: {e}",
            )
        except Exception as e:
            log_operation_error(
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

        log_api_call(
            "CallMcpTool",
            f"Tool={tool_name}, SessionId={self.session_id}, ArgsLength={len(args_json)}",
        )

        request = CallMcpToolRequest(
            authorization=f"Bearer {self.get_api_key()}",
            session_id=self.session_id,
            name=tool_name,
            args=args_json,
            auto_gen_session=auto_gen_session,
        )

        try:
            response = self.get_client().call_mcp_tool(
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
                log_operation_error(
                    "CallMcpTool", f"Tool returned error: {text_content}", False
                )
                return McpToolResult(
                    request_id=request_id,
                    success=False,
                    data="",
                    error_message=text_content,
                )

            log_api_response_with_details(
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
            log_operation_error("CallMcpTool", f"API request failed: {e}", True)
            return McpToolResult(
                request_id="",
                success=False,
                data="",
                error_message=f"API request failed: {e}",
            )
