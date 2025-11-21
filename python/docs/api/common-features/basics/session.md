# Session API Reference

## 🔧 Related Tutorial

- [Session Management Guide](../../../../../docs/guides/common-features/basics/session-management.md) - Detailed tutorial on session lifecycle and management



## Session

```python
class Session()
```

Session represents a session in the AgentBay cloud environment.

### delete

```python
def delete(sync_context: bool = False) -> DeleteResult
```

Delete this session and release all associated resources.

**Arguments**:

- `sync_context` _bool, optional_ - Whether to sync context data (trigger file uploads)
  before deleting the session. Defaults to False.
  

**Returns**:

    DeleteResult: Result indicating success or failure with request ID.
  - success (bool): True if deletion succeeded
  - error_message (str): Error details if deletion failed
  - request_id (str): Unique identifier for this API request
  

**Raises**:

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
  

**Example**:

```python
session = agent_bay.create().session
session.command.run("echo 'Hello World'")
session.delete()
```


**Notes**:

- Always delete sessions when done to avoid resource leaks
- Use sync_context=True if you need to preserve modified files
- Browser replay data is automatically synced if enabled
- The session object becomes invalid after deletion
- Deletion is idempotent - deleting an already deleted session succeeds


**See Also**:

AgentBay.create, AgentBay.delete, ContextManager.sync

### set\_labels

```python
def set_labels(labels: Dict[str, str]) -> OperationResult
```

Sets the labels for this session.

**Arguments**:

- `labels` _Dict[str, str]_ - The labels to set for the session.
  

**Returns**:

    OperationResult: Result indicating success or failure with request ID.
  

**Raises**:

    SessionError: If the operation fails.
  

**Example**:

```python
labels = {"environment": "production", "version": "1.0"}
session.set_labels(labels)
```

### get\_labels

```python
def get_labels() -> OperationResult
```

Gets the labels for this session.

**Returns**:

    OperationResult: Result containing the labels as data and request ID.
  

**Raises**:

    SessionError: If the operation fails.
  

**Example**:

```python
result = session.get_labels()
print(result.data)
```

### info

```python
def info() -> OperationResult
```

Get detailed information about this session.

**Returns**:

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
  

**Raises**:

    SessionError: If the API request fails or response is invalid.
  
  Behavior:
  This method calls the GetMcpResource API to retrieve session metadata.
  The returned SessionInfo contains:
  - session_id: The session identifier
  - resource_url: URL for accessing the session
  - Desktop-specific fields (app_id, auth_code, connection_properties, etc.)
  are populated from the DesktopInfo section of the API response
  

**Example**:

```python
session = agent_bay.create().session
info_result = session.info()
print(info_result.data.session_id)
```


**Notes**:

- Session info is retrieved from the AgentBay API in real-time
- The resource_url can be used for browser-based access
- Desktop-specific fields (app_id, auth_code) are only populated for desktop sessions
- This method does not modify the session state


**See Also**:

AgentBay.create, Session.delete, Session.get_link

### get\_link

```python
def get_link(protocol_type: Optional[str] = None,
             port: Optional[int] = None,
             options: Optional[str] = None) -> OperationResult
```

Get an access link for this session.

**Arguments**:

- `protocol_type` _Optional[str], optional_ - The protocol type for the link.
  Defaults to None (uses session default).
- `port` _Optional[int], optional_ - The port number to expose. Must be in range [30100, 30199].
  Defaults to None.
- `options` _Optional[str], optional_ - Additional configuration as JSON string.
  Defaults to None.
  

**Returns**:

    OperationResult: Result containing the access URL and request ID.
  - success (bool): True if the operation succeeded
  - data (str): The access URL
  - request_id (str): Unique identifier for this API request
  

**Raises**:

    SessionError: If port is out of valid range [30100, 30199] or the API request fails.
  

**Example**:

```python
session = agent_bay.create().session
link_result = session.get_link()
port_link_result = session.get_link(port=30150)
```


**Notes**:

- Port must be in range [30100, 30199] if specified
- The returned URL format depends on the session configuration
- For mobile ADB connections, use session.mobile.get_adb_url() instead


**See Also**:

Session.info, Session.get_link_async, Mobile.get_adb_url

### get\_link\_async

```python
async def get_link_async(protocol_type: Optional[str] = None,
                         port: Optional[int] = None,
                         options: Optional[str] = None) -> OperationResult
```

Asynchronously get a link associated with the current session.

**Arguments**:

- `protocol_type` _Optional[str], optional_ - The protocol type to use for the
  link. Defaults to None.
- `port` _Optional[int], optional_ - The port to use for the link. Must be an integer in the range [30100, 30199].
  Defaults to None.
- `options` _Optional[str], optional_ - Additional options as a JSON string (e.g., for adb configuration).
  Defaults to None.
  

**Returns**:

    OperationResult: Result containing the link as data and request ID.
  

**Raises**:

    SessionError: If the request fails or the response is invalid.

### list\_mcp\_tools

```python
def list_mcp_tools(image_id: Optional[str] = None)
```

List MCP tools available for this session.

**Arguments**:

    image_id: Optional image ID, defaults to session's image_id or "linux_latest"
  

**Returns**:

  Result containing tools list and request ID
  

**Example**:

```python
session = agent_bay.create().session
tools_result = session.list_mcp_tools()
print(f"Available tools: {len(tools_result.tools)}")
```

### call\_mcp\_tool

```python
def call_mcp_tool(tool_name: str,
                  args: Dict[str, Any],
                  read_timeout: Optional[int] = None,
                  connect_timeout: Optional[int] = None,
                  auto_gen_session: bool = False)
```

Call an MCP tool directly.

This is the unified public API for calling MCP tools. All feature modules
(Command, Code, Agent, etc.) use this method internally.

**Arguments**:

    tool_name: Name of the MCP tool to call
    args: Arguments to pass to the tool as a dictionary
    read_timeout: Optional read timeout in seconds
    connect_timeout: Optional connection timeout in seconds
    auto_gen_session: Whether to automatically generate session if not exists (default: False)
  

**Returns**:

    McpToolResult: Result containing success status, data, and error message
  

**Example**:

```python
result = session.call_mcp_tool("shell", {"command": "echo 'Hello World'", "timeout_ms": 1000})
result = session.call_mcp_tool("shell", {"command": "pwd", "timeout_ms": 1000}, read_timeout=30, connect_timeout=10)
result = session.call_mcp_tool("shell", {"command": "invalid_command_12345", "timeout_ms": 1000})
```


**Notes**:

- For press_keys tool, key names are automatically normalized to correct case format
- This improves case compatibility (e.g., "CTRL" -> "Ctrl", "tab" -> "Tab")

### pause

```python
def pause(timeout: int = 600,
          poll_interval: float = 2.0) -> SessionPauseResult
```

Synchronously pause this session, putting it into a dormant state.

This method internally calls the PauseSessionAsync API and then polls the GetSession API
to check the session status until it becomes PAUSED or until timeout.

**Arguments**:

- `timeout` _int, optional_ - Timeout in seconds to wait for the session to pause.
  Defaults to 600 seconds.
- `poll_interval` _float, optional_ - Interval in seconds between status polls.
  Defaults to 2.0 seconds.
  

**Returns**:

    SessionPauseResult: Result containing the request ID, success status, and final session status.
  - success (bool): True if the session was successfully paused
  - request_id (str): Unique identifier for this API request
  - status (str): Final session status (should be "PAUSED" if successful)
  - error_message (str): Error description (if success is False)
  - code (str): API response code (if available)
  - message (str): API response message (if available)
  - http_status_code (int): HTTP status code (if available)
  

**Raises**:

    SessionError: If the API request fails or response is invalid.
  

**Example**:

```python
session = agent_bay.create().session
pause_result = session.pause()
session.resume()
session.delete()
```


**Notes**:

- The session state transitions from RUNNING -> PAUSING -> PAUSED
- Paused sessions consume fewer resources but maintain their state
- Use resume() or resume_async() to restore the session to RUNNING state
- The timeout parameter controls how long to wait for the PAUSED state
- If timeout is exceeded, the method returns with success=False


**See Also**:

Session.pause_async, Session.resume, Session.resume_async, AgentBay.pause, AgentBay.pause_async

### pause\_async

```python
async def pause_async(timeout: int = 600,
                      poll_interval: float = 2.0) -> SessionPauseResult
```

Asynchronously pause this session, putting it into a dormant state.

This method directly calls the PauseSessionAsync API and then polls the GetSession API
asynchronously to check the session status until it becomes PAUSED or until timeout.

**Arguments**:

- `timeout` _int, optional_ - Timeout in seconds to wait for the session to pause.
  Defaults to 600 seconds.
- `poll_interval` _float, optional_ - Interval in seconds between status polls.
  Defaults to 2.0 seconds.
  

**Returns**:

    SessionPauseResult: Result containing the request ID, success status, and final session status.
  - success (bool): True if the session was successfully paused
  - request_id (str): Unique identifier for this API request
  - status (str): Final session status (should be "PAUSED" if successful)
  - error_message (str): Error description (if success is False)
  - code (str): API response code (if available)
  - message (str): API response message (if available)
  - http_status_code (int): HTTP status code (if available)
  

**Raises**:

    SessionError: If the API request fails or response is invalid.
  

**Example**:

```python
import asyncio

session = agent_bay.create().session
pause_result = await session.pause_async()
await session.resume_async()
session.delete()
```


**Notes**:

- The session state transitions from RUNNING -> PAUSING -> PAUSED
- Paused sessions consume fewer resources but maintain their state
- Use resume() or resume_async() to restore the session to RUNNING state
- The timeout parameter controls how long to wait for the PAUSED state
- If timeout is exceeded, the method returns with success=False


**See Also**:

Session.pause, Session.resume, Session.resume_async, AgentBay.pause_async

### resume

```python
def resume(timeout: int = 600,
           poll_interval: float = 2.0) -> SessionResumeResult
```

Synchronously resume this session from a paused state.

This method internally calls the ResumeSessionAsync API and then polls the GetSession API
to check the session status until it becomes RUNNING or until timeout.

**Arguments**:

- `timeout` _int, optional_ - Timeout in seconds to wait for the session to resume.
  Defaults to 600 seconds.
- `poll_interval` _float, optional_ - Interval in seconds between status polls.
  Defaults to 2.0 seconds.
  

**Returns**:

    SessionResumeResult: Result containing the request ID, success status, and final session status.
  - success (bool): True if the session was successfully resumed
  - request_id (str): Unique identifier for this API request
  - status (str): Final session status (should be "RUNNING" if successful)
  - error_message (str): Error description (if success is False)
  - code (str): API response code (if available)
  - message (str): API response message (if available)
  - http_status_code (int): HTTP status code (if available)
  

**Raises**:

    SessionError: If the API request fails or response is invalid.
  

**Example**:

```python
session = agent_bay.create().session
session.pause()
resume_result = session.resume()
session.delete()
```


**Notes**:

- The session state transitions from PAUSED -> RESUMING -> RUNNING
- Only sessions in PAUSED state can be resumed
- Use pause() or pause_async() to put a session into PAUSED state
- The timeout parameter controls how long to wait for the RUNNING state
- If timeout is exceeded, the method returns with success=False


**See Also**:

Session.pause, Session.pause_async, Session.resume_async, AgentBay.resume, AgentBay.resume_async

### resume\_async

```python
async def resume_async(timeout: int = 600,
                       poll_interval: float = 2.0) -> SessionResumeResult
```

Asynchronously resume this session from a paused state.

This method directly calls the ResumeSessionAsync API and then polls the GetSession API
asynchronously to check the session status until it becomes RUNNING or until timeout.

**Arguments**:

- `timeout` _int, optional_ - Timeout in seconds to wait for the session to resume.
  Defaults to 600 seconds.
- `poll_interval` _float, optional_ - Interval in seconds between status polls.
  Defaults to 2.0 seconds.
  

**Returns**:

    SessionResumeResult: Result containing the request ID, success status, and final session status.
  - success (bool): True if the session was successfully resumed
  - request_id (str): Unique identifier for this API request
  - status (str): Final session status (should be "RUNNING" if successful)
  - error_message (str): Error description (if success is False)
  - code (str): API response code (if available)
  - message (str): API response message (if available)
  - http_status_code (int): HTTP status code (if available)
  

**Raises**:

    SessionError: If the API request fails or response is invalid.
  

**Example**:

```python
import asyncio

session = agent_bay.create().session
session.pause()
resume_result = await session.resume_async()
session.delete()
```


**Notes**:

- The session state transitions from PAUSED -> RESUMING -> RUNNING
- Only sessions in PAUSED state can be resumed
- Use pause() or pause_async() to put a session into PAUSED state
- The timeout parameter controls how long to wait for the RUNNING state
- If timeout is exceeded, the method returns with success=False


**See Also**:

Session.pause, Session.pause_async, Session.resume, AgentBay.resume_async

## Related Resources

- [FileSystem API Reference](filesystem.md)
- [Command API Reference](command.md)
- [Context API Reference](context.md)
- [Context Manager API Reference](context-manager.md)
- [OSS API Reference](../../common-features/advanced/oss.md)

---

*Documentation generated automatically from source code using pydoc-markdown.*
