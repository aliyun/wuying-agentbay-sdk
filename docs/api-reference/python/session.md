# Session Class

The `Session` class represents a session in the AgentBay cloud environment. It provides methods for managing file systems, executing commands, and more.

## Properties

```python
agent_bay  # The AgentBay instance that created this session
session_id  # The ID of this session
resource_url  # The URL of the resource associated with this session
file_system  # The FileSystem instance for this session
command  # The Command instance for this session
code  # The Code instance for this session
oss  # The Oss instance for this session
application  # The ApplicationManager instance for this session
window  # The WindowManager instance for this session
ui  # The UI instance for this session
context  # The ContextManager instance for this session
browser  # The Browser instance for this session
agent  # The Agent instance for this session
is_vpc  # Whether this session uses VPC resources
network_interface_ip  # Network interface IP for VPC sessions
http_port  # HTTP port for VPC sessions
mcp_tools  # MCP tools available for this session
```

## Methods

### delete

Deletes this session.

```python
delete(sync_context: bool = False) -> DeleteResult
```

**Parameters:**
- `sync_context` (bool, optional): If True, the API will trigger a file upload via `self.context.sync` before actually releasing the session. Default is False.

**Returns:**
- `DeleteResult`: A result object containing success status, request ID, and error message if any.

**Behavior:**
- When `sync_context` is True, the API will first call `context.sync` to trigger file upload.
- It will then check `context.info` to retrieve ContextStatusData and monitor only upload task items' Status.
- The API waits until all upload tasks show either "Success" or "Failed" status, or until the maximum retry limit (150 times with 2-second intervals) is reached.
- Any "Failed" status upload tasks will have their error messages printed.
- The session deletion only proceeds after context sync status checking for upload tasks completes.

**Example:**
```python
from agentbay import AgentBay

# Initialize the SDK
agent_bay = AgentBay(api_key="your_api_key")

# Create a session
result = agent_bay.create()
if result.success:
    session = result.session
    print(f"Session created with ID: {session.session_id}")
    
    # Use the session...
    
    # Delete the session with context synchronization
    delete_result = session.delete(sync_context=True)
    if delete_result.success:
        print(f"Session deleted successfully with synchronized context")
    else:
        print(f"Failed to delete session: {delete_result.error_message}")
```

### set_labels

Sets labels for this session.

```python
set_labels(labels: Dict[str, str]) -> OperationResult
```

**Parameters:**
- `labels` (Dict[str, str]): Key-value pairs representing the labels to set.

**Returns:**
- `OperationResult`: A result object containing success status, request ID, and error message if any.

**Raises:**
- `AgentBayError`: If setting labels fails due to API errors or other issues.

**Example:**
```python
# Set session labels
labels = {
    "project": "demo",
    "environment": "testing",
    "version": "1.0.0"
}
result = session.set_labels(labels)
if result.success:
    print("Labels set successfully")
else:
    print(f"Failed to set labels: {result.error_message}")
```

### get_labels

Gets the labels for this session.

```python
get_labels() -> OperationResult
```

**Returns:**
- `OperationResult`: A result object containing success status, request ID, error message if any, and the labels data.

**Raises:**
- `AgentBayError`: If getting labels fails due to API errors or other issues.

**Example:**
```python
# Get session labels
try:
    result = session.get_labels()
    if result.success:
        print(f"Session labels: {result.data}")
    else:
        print(f"Failed to get labels: {result.error_message}")
except AgentBayError as e:
    print(f"Failed to get labels: {e}")
```

### info

Gets information about this session.

```python
info() -> SessionInfo
```

**Returns:**
- `SessionInfo`: An object containing information about the session.

**Raises:**
- `AgentBayError`: If getting session information fails due to API errors or other issues.

**Example:**
```python
# Get session information
try:
    info = session.info()
    print(f"Session ID: {info.session_id}")
    print(f"Resource URL: {info.resource_url}")
    print(f"App ID: {info.app_id}")
except AgentBayError as e:
    print(f"Failed to get session info: {e}")
```

### get_link

Gets a link for this session.

```python
get_link(protocol_type: Optional[str] = None, port: Optional[int] = None) -> str
```

**Parameters:**
- `protocol_type` (str, optional): The protocol type for the link.
- `port` (int, optional): The port for the link.

**Returns:**
- `str`: The link for the session.

**Raises:**
- `AgentBayError`: If getting the link fails due to API errors or other issues.

**Example:**
```python
# Get session link
try:
    link = session.get_link()
    print(f"Session link: {link}")
    
    # Get link with specific protocol and port
    custom_link = session.get_link("https", 8443)
    print(f"Custom link: {custom_link}")
except AgentBayError as e:
    print(f"Failed to get link: {e}")
```

## Related Resources

- [FileSystem API Reference](filesystem.md)
- [Command API Reference](command.md)
- [UI API Reference](ui.md)
- [Window API Reference](window.md)
- [OSS API Reference](oss.md)
- [Application API Reference](application.md)
- [Context API Reference](context-manager.md) 