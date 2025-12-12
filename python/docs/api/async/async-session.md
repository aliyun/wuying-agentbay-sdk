# AsyncSession API Reference

> **💡 Sync Version**: This documentation covers the asynchronous API. For synchronous operations, see [`Session`](../sync/session.md).
>
> ⚡ **Performance Advantage**: Async API enables concurrent operations with 4-6x performance improvements for parallel tasks.

## 🔧 Related Tutorial

- [Session Management Guide](../../../../docs/guides/common-features/basics/session-management.md) - Detailed tutorial on session lifecycle and management



### \_\_init\_\_

```python
def __init__(self, session_id: str = "",
             resource_url: str = "",
             app_id: str = "",
             auth_code: str = "",
             connection_properties: str = "",
             resource_id: str = "",
             resource_type: str = "",
             ticket: str = "")
```

## AsyncSession

```python
class AsyncSession()
```

AsyncSession represents a session in the AgentBay cloud environment.

### \_\_init\_\_

```python
def __init__(self, agent_bay: "AsyncAgentBay", session_id: str)
```

### delete

```python
async def delete(sync_context: bool = False) -> DeleteResult
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

### set\_labels

```python
async def set_labels(labels: Dict[str, str]) -> OperationResult
```

Sets the labels for this session asynchronously.

### get\_labels

```python
async def get_labels() -> OperationResult
```

Gets the labels for this session asynchronously.

### info

```python
async def info() -> OperationResult
```

Get detailed information about this session asynchronously.

### get\_link

```python
async def get_link(protocol_type: Optional[str] = None,
                   port: Optional[int] = None,
                   options: Optional[str] = None) -> OperationResult
```

Asynchronously get a link associated with the current session.

### list\_mcp\_tools

```python
async def list_mcp_tools(image_id: Optional[str] = None)
```

List MCP tools available for this session asynchronously.

### call\_mcp\_tool

```python
async def call_mcp_tool(tool_name: str,
                        args: Dict[str, Any],
                        read_timeout: Optional[int] = None,
                        connect_timeout: Optional[int] = None,
                        auto_gen_session: bool = False)
```

Call an MCP tool directly asynchronously.

### pause

```python
async def pause(timeout: int = 600,
                poll_interval: float = 2.0) -> SessionPauseResult
```

Asynchronously pause this session, putting it into a dormant state.
This method waits until the session enters the PAUSED state.

### pause\_async

```python
async def pause_async() -> SessionPauseResult
```

Asynchronously initiate the pause session operation without waiting for completion.

### resume

```python
async def resume(timeout: int = 600,
                 poll_interval: float = 2.0) -> SessionResumeResult
```

Asynchronously resume this session from a paused state.
This method waits until the session enters the RUNNING state.

### resume\_async

```python
async def resume_async() -> SessionResumeResult
```

Asynchronously initiate the resume session operation without waiting for completion.

## See Also

- [Synchronous vs Asynchronous API](../../../docs/guides/async-programming/sync-vs-async.md)

**Related APIs:**
- [FileSystem API Reference](./async-filesystem.md)
- [Command API Reference](./async-command.md)
- [Context API Reference](./async-context.md)
- [Context Manager API Reference](./async-context-manager.md)
- [OSS API Reference](./async-oss.md)

---

*Documentation generated automatically from source code using pydoc-markdown.*
