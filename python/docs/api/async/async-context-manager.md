# AsyncContextManager API Reference

> **💡 Sync Version**: This documentation covers the asynchronous API. For synchronous operations, see [`ContextManager`](../sync/context-manager.md).
>
> ⚡ **Performance Advantage**: Async API enables concurrent operations with 4-6x performance improvements for parallel tasks.



## AsyncContextManager

```python
class AsyncContextManager()
```

Manages context operations within a session in the AgentBay cloud environment.

The AsyncContextManager provides methods to get information about context synchronization
status and to synchronize contexts with the session.

### \_\_init\_\_

```python
def __init__(self, session)
```

### info

```python
async def info(context_id: Optional[str] = None,
               path: Optional[str] = None,
               task_type: Optional[str] = None) -> ContextInfoResult
```

Get information about context synchronization status asynchronously.

**Arguments**:

    context_id: Optional ID of the context to get information for
    path: Optional path where the context is mounted
    task_type: Optional type of task to get information for (e.g., "upload", "download")
  

**Returns**:

    ContextInfoResult: Result object containing context status data and request ID
  

**Example**:

session_result = await agent_bay.create()
if session_result.success:
session = session_result.session
result = await session.context_manager.info(
context_id="project-data",
path="/mnt/shared",
task_type="upload",
)
for status in result.context_status_data:
    print(f"{status.context_id}: {status.status}")
await session.delete()

### sync

```python
async def sync(context_id: Optional[str] = None,
               path: Optional[str] = None,
               mode: Optional[str] = None,
               max_retries: int = 150,
               retry_interval: int = 1500) -> ContextSyncResult
```

Synchronize a context with the session asynchronously.

**Arguments**:

    context_id: Optional ID of the context to synchronize
    path: Optional path where the context should be mounted
    mode: Optional synchronization mode (e.g., "upload", "download")
    max_retries: Maximum number of retries for polling completion status (default: 150)
    retry_interval: Milliseconds to wait between retries (default: 1500)
  

**Returns**:

    ContextSyncResult: Result object containing success status and request ID
  

**Example**:

session_result = await agent_bay.create()
if session_result.success:
session = session_result.session
sync_result = await session.context_manager.sync(
context_id="project-data",
path="/mnt/shared",
mode="upload",
max_retries=60,
retry_interval=1000,
)
print(f"Sync completed: {sync_result.success}")
await session.delete()


**Example**:

session_result = await agent_bay.create()
if session_result.success:
session = session_result.session
async def on_sync_complete(result):
print(f"Callback received: {result.success}")
sync_result = await session.context_manager.sync(
context_id="reports",
path="/mnt/reports",
mode="download",
max_retries=80,
retry_interval=500,
)
await on_sync_complete(sync_result)
await session.delete()

## See Also

- [Synchronous vs Asynchronous API](../../../docs/guides/async-programming/sync-vs-async.md)

---

*Documentation generated automatically from source code using pydoc-markdown.*
