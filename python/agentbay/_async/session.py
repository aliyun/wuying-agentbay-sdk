import asyncio
import json
import time
from typing import TYPE_CHECKING, Any, Dict, Optional

from .._common.exceptions import SessionError
from .._common.logger import (
    _log_api_call,
    _log_api_response_with_details,
    _log_info_with_color,
    _log_operation_error,
    _log_operation_start,
    _log_operation_success,
    _log_warning,
    get_logger,
)
from .._common.models import (
    DeleteResult,
    McpToolResult,
    OperationResult,
    SessionPauseResult,
    SessionResumeResult,
    extract_request_id,
)
from ..api.models import (
    CallMcpToolRequest,
    DeleteSessionAsyncRequest,
    GetLabelRequest,
    GetLinkRequest,
    GetLinkResponse,
    GetMcpResourceRequest,
    ListMcpToolsRequest,
    PauseSessionAsyncRequest,
    ReleaseMcpSessionRequest,
    ResumeSessionAsyncRequest,
    SetLabelRequest,
)
from .agent import AsyncAgent
from .browser import AsyncBrowser
from .code import AsyncCode
from .command import AsyncCommand
from .computer import AsyncComputer
from .context_manager import AsyncContextManager
from .filesystem import AsyncFileSystem
from .mobile import AsyncMobile
from .oss import AsyncOss

if TYPE_CHECKING:
    from .agentbay import AsyncAgentBay

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


class AsyncSession:
    """
    AsyncSession represents a session in the AgentBay cloud environment.
    """

    def __init__(self, agent_bay: "AsyncAgentBay", session_id: str):
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
            True  # Whether browser recording is enabled for this session
        )

        # MCP tools available for this session
        self.mcp_tools = []  # List[McpTool]

        # Initialize file system, command and code handlers
        self.file_system = AsyncFileSystem(self)
        self.command = AsyncCommand(self)
        self.code = AsyncCode(self)
        self.oss = AsyncOss(self)

        # Initialize Computer and Mobile modules
        self.computer = AsyncComputer(self)
        self.mobile = AsyncMobile(self)

        self.context = AsyncContextManager(self)
        self.browser = AsyncBrowser(self)

        self.agent = AsyncAgent(self)

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

    async def delete(self, sync_context: bool = False) -> DeleteResult:
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
        """
        try:
            # Perform context synchronization if needed
            if sync_context:
                _log_operation_start(
                    "Context synchronization", "Before session deletion"
                )

                sync_start_time = time.time()

                try:
                    # Sync all contexts
                    sync_result = await self.context.sync()
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
            request = DeleteSessionAsyncRequest(
                authorization=f"Bearer {self._get_api_key()}",
                session_id=self.session_id,
            )
            client = self._get_client()
            response = await client.delete_session_async_async(request)

            # Extract request ID
            request_id = extract_request_id(response)

            # Check if the response is success
            response_map = response.to_map()
            body = response_map.get("body", {})
            success = body.get("Success", True)

            if not success:
                error_message = f"[{body.get('Code', 'Unknown')}] {body.get('Message', 'Failed to delete session')}"
                _log_api_response_with_details(
                    api_name="DeleteSessionAsync",
                    request_id=request_id,
                    success=False,
                    full_response=json.dumps(body, ensure_ascii=False, indent=2),
                )
                return DeleteResult(
                    request_id=request_id,
                    success=False,
                    error_message=error_message,
                )

            # Poll for session deletion status
            _logger.info(f"🔄 Waiting for session {self.session_id} to be deleted...")
            poll_timeout = 50.0  # 50 seconds timeout
            poll_interval = 1.0  # Poll every 1 second
            poll_start_time = time.time()

            while True:
                # Check timeout
                elapsed_time = time.time() - poll_start_time
                if elapsed_time >= poll_timeout:
                    error_message = f"Timeout waiting for session deletion after {poll_timeout}s"
                    _logger.warning(f"⏱️  {error_message}")
                    return DeleteResult(
                        request_id=request_id,
                        success=False,
                        error_message=error_message,
                    )

                # Get session status
                session_result = await self.agent_bay.get_session(self.session_id)

                # Check if session is deleted (NotFound error)
                if not session_result.success:
                    error_code = session_result.code or ""
                    error_message = session_result.error_message or ""
                    http_status_code = session_result.http_status_code or 0

                    # Check for InvalidMcpSession.NotFound, 400 with "not found", or error_message containing "not found"
                    is_not_found = (
                        error_code == "InvalidMcpSession.NotFound" or
                        (http_status_code == 400 and (
                            "not found" in error_message.lower() or
                            "NotFound" in error_message or
                            "not found" in error_code.lower()
                        )) or
                        "not found" in error_message.lower()
                    )

                    if is_not_found:
                        # Session is deleted
                        _logger.info(f"✅ Session {self.session_id} successfully deleted (NotFound)")
                        break
                    else:
                        # Other error, continue polling
                        _logger.debug(f"⚠️  Get session error (will retry): {error_message}")
                        # Continue to next poll iteration

                # Check session status if we got valid data
                elif session_result.data and session_result.data.status:
                    status = session_result.data.status
                    _logger.debug(f"📊 Session status: {status}")
                    if status == "FINISH":
                        _logger.info(f"✅ Session {self.session_id} successfully deleted")
                        break

                # Wait before next poll
                await asyncio.sleep(poll_interval)

            # Log successful deletion
            _log_api_response_with_details(
                api_name="DeleteSessionAsync",
                request_id=request_id,
                success=True,
                key_fields={"session_id": self.session_id},
            )

            # Return success result with request ID
            return DeleteResult(request_id=request_id, success=True)

        except Exception as e:
            _log_operation_error("delete_session_async", str(e), exc_info=True)
            # In case of error, return failure result with error message
            return DeleteResult(
                success=False,
                error_message=f"Failed to delete session {self.session_id}: {e}",
            )

    def _validate_labels(self, labels: Dict[str, str]) -> Optional[OperationResult]:
        """
        Validates labels parameter for label operations.
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

    async def set_labels(self, labels: Dict[str, str]) -> OperationResult:
        """
        Sets the labels for this session asynchronously.
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

            client = self._get_client()
            response = await client.set_label_async(request)

            # Extract request ID
            request_id = extract_request_id(response)

            # Log successful label setting
            _log_api_response_with_details(
                api_name="SetLabel",
                request_id=request_id,
                success=True,
                key_fields={"session_id": self.session_id, "labels_count": len(labels)},
            )

            return OperationResult(request_id=request_id, success=True)

        except Exception as e:
            _logger.exception(f"❌ Failed to set labels for session {self.session_id}")
            raise SessionError(
                f"Failed to set labels for session {self.session_id}: {e}"
            )

    async def get_labels(self) -> OperationResult:
        """
        Gets the labels for this session asynchronously.
        """
        try:
            request = GetLabelRequest(
                authorization=f"Bearer {self._get_api_key()}",
                session_id=self.session_id,
            )

            # Try async method first, fall back to sync wrapped in asyncio.to_thread
            client = self._get_client()
            response = await client.get_label_async(request)

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
                key_fields={"session_id": self.session_id, "labels_count": len(labels)},
            )

            return OperationResult(request_id=request_id, success=True, data=labels)

        except Exception as e:
            _logger.exception(f"❌ Failed to get labels for session {self.session_id}")
            raise SessionError(
                f"Failed to get labels for session {self.session_id}: {e}"
            )

    async def info(self) -> OperationResult:
        """
        Get detailed information about this session asynchronously.
        """
        try:
            request = GetMcpResourceRequest(
                authorization=f"Bearer {self._get_api_key()}",
                session_id=self.session_id,
            )

            _log_api_call("GetMcpResource", f"SessionId={self.session_id}")

            # Try async method first, fall back to sync wrapped in asyncio.to_thread
            client = self._get_client()
            response = await client.get_mcp_resource_async(request)

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
                    "resource_type": session_info.resource_type,
                },
            )

            return OperationResult(
                request_id=request_id, success=True, data=session_info
            )

        except Exception as e:
            # Check if this is an expected business error (e.g., session not found)
            error_str = str(e)
            error_code = ""

            # Try to extract error code from the exception
            if hasattr(e, "data") and hasattr(e.data, "get"):
                error_code = e.data.get("Code", "")
            elif "InvalidMcpSession.NotFound" in error_str or "NotFound" in error_str:
                error_code = "InvalidMcpSession.NotFound"

            if error_code == "InvalidMcpSession.NotFound":
                # This is an expected error - session doesn't exist
                # Use info level logging without stack trace, but with red color for visibility
                _log_info_with_color(f"Session not found: {self.session_id}")
                _logger.debug(f"GetMcpResource error details: {error_str}")
                return OperationResult(
                    request_id="",
                    success=False,
                    error_message=f"Session {self.session_id} not found",
                )
            else:
                # This is an unexpected error - log with full error
                _logger.exception(
                    f"❌ Failed to get session info for session {self.session_id}"
                )
                raise SessionError(
                    f"Failed to get session info for session {self.session_id}: {e}"
                )

    async def get_link(
        self,
        protocol_type: Optional[str] = None,
        port: Optional[int] = None,
        options: Optional[str] = None,
    ) -> OperationResult:
        """
        Asynchronously get a link associated with the current session.
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
                f"Port={port or 'default'}, Options={'provided' if options else 'none'}",
            )

            request = GetLinkRequest(
                authorization=f"Bearer {self._get_api_key()}",
                session_id=self._get_session_id(),
                protocol_type=protocol_type,
                port=port,
                options=options,
            )

            # Try async method first, fall back to sync wrapped in asyncio.to_thread
            client = self.agent_bay.client
            response = await client.get_link_async(request)

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
                    "port": port or "default",
                },
            )

            return OperationResult(request_id=request_id, success=True, data=url)

        except SessionError:
            raise
        except Exception as e:
            _logger.error(f"❌ Failed to get link for session {self.session_id}: {e}")
            raise SessionError(f"Failed to get link: {e}")

    async def list_mcp_tools(self, image_id: Optional[str] = None):
        """
        List MCP tools available for this session asynchronously.
        """
        from .._common.models.response import McpToolsResult
        from .._common.models.mcp_tool import McpTool

        # Use provided image_id, session's image_id, or default
        if image_id is None:
            image_id = getattr(self, "image_id", "") or "linux_latest"

        request = ListMcpToolsRequest(
            authorization=f"Bearer {self._get_api_key()}", image_id=image_id
        )

        _log_api_call("ListMcpTools", f"ImageId={image_id}")

        # Try async method first, fall back to sync wrapped in asyncio.to_thread
        client = self._get_client()
        response = await client.list_mcp_tools_async(request)

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
            key_fields={"image_id": image_id, "tools_count": len(tools)},
        )

        return McpToolsResult(request_id=request_id, tools=tools)

    async def call_mcp_tool(
        self,
        tool_name: str,
        args: Dict[str, Any],
        read_timeout: Optional[int] = None,
        connect_timeout: Optional[int] = None,
        auto_gen_session: bool = False,
    ):
        """
        Call an MCP tool directly asynchronously.
        """
        try:
            # Normalize press_keys arguments for better case compatibility
            if tool_name == "press_keys" and "keys" in args:
                from .._common.utils.key_normalizer import normalize_keys

                args = args.copy()  # Don't modify the original args
                args["keys"] = normalize_keys(args["keys"])
                _logger.debug(f"Normalized press_keys arguments: {args}")

            args_json = json.dumps(args, ensure_ascii=False)

            # Check if this is a VPC session
            if self._is_vpc_enabled():
                return await self._call_mcp_tool_vpc(tool_name, args_json)

            # Non-VPC mode: use traditional API call
            result_data = await self._call_mcp_tool_api(
                tool_name, args_json, read_timeout, connect_timeout, auto_gen_session
            )
            return result_data
        except Exception as e:
            _logger.error(f"❌ Failed to call MCP tool {tool_name}: {e}")
            return McpToolResult(
                request_id="",
                success=False,
                data="",
                error_message=f"Failed to call MCP tool: {e}",
            )

    async def _call_mcp_tool_vpc(self, tool_name: str, args_json: str):
        """
        Handle VPC-based MCP tool calls using HTTP requests asynchronously.
        """
        import random
        import string
        import time

        import httpx

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
            # Send HTTP request asynchronously using httpx
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    base_url, params=params, headers=headers, timeout=30
                )
                response.raise_for_status()
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

        except httpx.RequestError as e:
            _log_operation_error("CallMcpTool(VPC)", f"HTTP request failed: {e}", True)
            return McpToolResult(
                request_id=request_id,
                success=False,
                data="",
                error_message=f"HTTP request failed: {e}",
            )
        except Exception as e:
            _log_operation_error("CallMcpTool(VPC)", f"Unexpected error: {e}", True)
            return McpToolResult(
                request_id=request_id,
                success=False,
                data="",
                error_message=f"Unexpected error: {e}",
            )

    async def _call_mcp_tool_api(
        self,
        tool_name: str,
        args_json: str,
        read_timeout: Optional[int] = None,
        connect_timeout: Optional[int] = None,
        auto_gen_session: bool = False,
    ):
        """
        Handle traditional API-based MCP tool calls asynchronously.
        """
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
            # Try async method first, fall back to sync wrapped in asyncio.to_thread
            client = self._get_client()
            response = await client.call_mcp_tool_async(
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
                elif isinstance(data_str, str):
                    data_obj = json.loads(data_str)
                else:
                    # Handle MagicMock or other non-string types in tests
                    data_obj = {}
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

    async def pause(
        self, timeout: int = 600, poll_interval: float = 2.0
    ) -> SessionPauseResult:
        """
        Asynchronously pause this session, putting it into a dormant state.
        This method waits until the session enters the PAUSED state.
        """
        try:
            # Call the async initiate method first
            result = await self.pause_async()
            if not result.success:
                return result

            request_id = result.request_id

            _log_operation_success(
                "PauseSessionAsync",
                f"Session {self.session_id} pause initiated successfully",
            )

            # Poll for session status until PAUSED or timeout
            start_time = time.time()
            max_attempts = int(timeout / poll_interval)
            attempt = 0

            while attempt < max_attempts:
                attempt += 1

                try:
                    # Check session status using get_session
                    # This will work if agent_bay has get_session (which it does)
                    session_result = await self.agent_bay.get_session(self.session_id)
                    if session_result.success and session_result.data:
                        status = session_result.data.status
                        if status == "PAUSED":
                            _log_operation_success(
                                "PauseSessionAsync",
                                f"Session {self.session_id} is now PAUSED",
                            )
                            return SessionPauseResult(
                                request_id=request_id,
                                success=True,
                                status="PAUSED",
                            )
                        elif (
                            status == "ERROR" or status == "FAILED"
                        ):  # Add other failure states if known
                            _log_operation_error(
                                "PauseSessionAsync",
                                f"Session entered error state: {status}",
                            )
                            return SessionPauseResult(
                                request_id=request_id,
                                success=False,
                                error_message=f"Session entered error state: {status}",
                                status=status,
                            )
                except Exception:
                    pass

                # Check timeout
                if time.time() - start_time > timeout:
                    break

                # Wait before next poll
                await asyncio.sleep(poll_interval)

            _log_operation_error(
                "PauseSessionAsync",
                f"Timed out waiting for session {self.session_id} to pause",
            )
            return SessionPauseResult(
                request_id=request_id,
                success=False,
                status="PAUSING",  # Still technically pausing or unknown
                error_message=f"Timed out after {timeout} seconds waiting for session to pause",
            )

        except Exception as e:
            _log_operation_error("PauseSessionAsync", str(e))
            return SessionPauseResult(
                request_id="",
                success=False,
                error_message=f"Unexpected error pausing session: {e}",
            )

    async def pause_async(self) -> SessionPauseResult:
        """
        Asynchronously initiate the pause session operation without waiting for completion.
        """
        try:
            request = PauseSessionAsyncRequest(
                authorization=f"Bearer {self._get_api_key()}",
                session_id=self.session_id,
            )

            _log_api_call("PauseSessionAsync", f"SessionId={self.session_id}")

            client = self._get_client()
            response = await client.pause_session_async_async(request)

            # Extract request ID
            request_id = extract_request_id(response)

            # Check for API-level errors
            response_map = response.to_map()
            if not response_map:
                return SessionPauseResult(
                    request_id=request_id,
                    success=False,
                    error_message="Invalid response format",
                )

            body = response_map.get("body", {})
            if not body:
                return SessionPauseResult(
                    request_id=request_id,
                    success=False,
                    error_message="Invalid response body",
                )

            # Extract fields from response body
            success = body.get("Success", False)
            code = body.get("Code", "")
            message = body.get("Message", "")
            http_status_code = body.get("HttpStatusCode", 0)

            _log_api_response_with_details(
                api_name="PauseSessionAsync",
                request_id=request_id,
                success=True,
                key_fields={"session_id": self.session_id},
            )

            if not success:
                error_message = (
                    f"[{code}] {message}" if code or message else "Unknown error"
                )
                _log_operation_error("PauseSessionAsync", error_message)
                return SessionPauseResult(
                    request_id=request_id,
                    success=False,
                    error_message=error_message,
                    code=code,
                    message=message,
                    http_status_code=http_status_code,
                )

            return SessionPauseResult(
                request_id=request_id, success=True, status="PAUSING"
            )

        except Exception as e:
            _log_operation_error("PauseSessionAsync", str(e))
            return SessionPauseResult(
                request_id="",
                success=False,
                error_message=f"Unexpected error pausing session: {e}",
            )

    async def resume(
        self, timeout: int = 600, poll_interval: float = 2.0
    ) -> SessionResumeResult:
        """
        Asynchronously resume this session from a paused state.
        This method waits until the session enters the RUNNING state.
        """
        try:
            # Call the async initiate method first
            result = await self.resume_async()
            if not result.success:
                return result

            request_id = result.request_id

            _log_operation_success(
                "ResumeSessionAsync",
                f"Session {self.session_id} resume initiated successfully",
            )

            # Poll for session status until RUNNING or timeout
            start_time = time.time()
            max_attempts = int(timeout / poll_interval)
            attempt = 0

            while attempt < max_attempts:
                attempt += 1

                try:
                    # Check session status using get_session
                    session_result = await self.agent_bay.get_session(self.session_id)
                    if session_result.success and session_result.data:
                        status = session_result.data.status
                        if status == "RUNNING":
                            _log_operation_success(
                                "ResumeSessionAsync",
                                f"Session {self.session_id} is now RUNNING",
                            )
                            return SessionResumeResult(
                                request_id=request_id,
                                success=True,
                                status="RUNNING",
                            )
                        elif status == "ERROR" or status == "FAILED":
                            _log_operation_error(
                                "ResumeSessionAsync",
                                f"Session entered error state: {status}",
                            )
                            return SessionResumeResult(
                                request_id=request_id,
                                success=False,
                                error_message=f"Session entered error state: {status}",
                                status=status,
                            )
                except Exception:
                    pass

                # Check timeout
                if time.time() - start_time > timeout:
                    break

                # Wait before next poll
                await asyncio.sleep(poll_interval)

            _log_operation_error(
                "ResumeSessionAsync",
                f"Timed out waiting for session {self.session_id} to resume",
            )
            return SessionResumeResult(
                request_id=request_id,
                success=False,
                status="RESUMING",  # Still technically resuming or unknown
                error_message=f"Timed out after {timeout} seconds waiting for session to resume",
            )

        except Exception as e:
            _log_operation_error("ResumeSessionAsync", str(e))
            return SessionResumeResult(
                request_id="",
                success=False,
                error_message=f"Unexpected error resuming session: {e}",
            )

    async def resume_async(self) -> SessionResumeResult:
        """
        Asynchronously initiate the resume session operation without waiting for completion.
        """
        try:
            request = ResumeSessionAsyncRequest(
                authorization=f"Bearer {self._get_api_key()}",
                session_id=self.session_id,
            )

            _log_api_call("ResumeSessionAsync", f"SessionId={self.session_id}")

            client = self._get_client()
            response = await client.resume_session_async_async(request)

            request_id = extract_request_id(response)

            response_map = response.to_map()
            if not response_map:
                return SessionResumeResult(
                    request_id=request_id,
                    success=False,
                    error_message="Invalid response format",
                )
            body = response_map.get("body", {})
            if not body:
                return SessionResumeResult(
                    request_id=request_id,
                    success=False,
                    error_message="Invalid response body",
                )

            success = body.get("Success", False)
            code = body.get("Code", "")
            message = body.get("Message", "")
            http_status_code = body.get("HttpStatusCode", 0)

            if not success:
                error_message = (
                    f"[{code}] {message}" if code or message else "Unknown error"
                )
                _log_operation_error("ResumeSessionAsync", error_message)
                return SessionResumeResult(
                    request_id=request_id,
                    success=False,
                    error_message=error_message,
                    code=code,
                    message=message,
                    http_status_code=http_status_code,
                )

            _log_api_response_with_details(
                api_name="ResumeSessionAsync",
                request_id=request_id,
                success=True,
                key_fields={"session_id": self.session_id},
            )

            return SessionResumeResult(
                request_id=request_id, success=True, status="RESUMING"
            )

        except Exception as e:
            _log_operation_error("ResumeSessionAsync", str(e))
            return SessionResumeResult(
                request_id="",
                success=False,
                error_message=f"Unexpected error resuming session: {e}",
            )
