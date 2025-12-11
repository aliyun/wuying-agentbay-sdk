# Context Manager API Reference

> **💡 Async Version**: This documentation covers the synchronous API. For async/await support, see [`AsyncContextManager`](../async/async-context-manager.md) which provides the same functionality with async methods.



## ContextManager

```python
class ContextManager()
```

Manages context operations within a session in the AgentBay cloud environment.

The ContextManager provides methods to get information about context synchronization
status and to synchronize contexts with the session.

### info

```python
def info(context_id: Optional[str] = None,
         path: Optional[str] = None,
         task_type: Optional[str] = None) -> ContextInfoResult
```

Get information about context synchronization status synchronously.

**Arguments**:

    context_id: Optional ID of the context to get information for
    path: Optional path where the context is mounted
    task_type: Optional type of task to get information for (e.g., "upload", "download")
  

**Returns**:

    ContextInfoResult: Result object containing context status data and request ID

### sync

```python
def sync(context_id: Optional[str] = None,
         path: Optional[str] = None,
         mode: Optional[str] = None,
         max_retries: int = 150,
         retry_interval: int = 1500) -> ContextSyncResult
```

Synchronize a context with the session synchronously.

**Arguments**:

    context_id: Optional ID of the context to synchronize
    path: Optional path where the context should be mounted
    mode: Optional synchronization mode (e.g., "upload", "download")
    max_retries: Maximum number of retries for polling completion status (default: 150)
    retry_interval: Milliseconds to wait between retries (default: 1500)
  

**Returns**:

    ContextSyncResult: Result object containing success status and request ID

## See Also

- [Synchronous vs Asynchronous API](../../../../docs/guides/async-programming/sync-vs-async.md)

---

*Documentation generated automatically from source code using pydoc-markdown.*
