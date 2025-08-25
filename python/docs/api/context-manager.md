# ContextManager API Reference

The `ContextManager` class provides functionality for managing contexts within a session. It enables you to interact with the contexts that are synchronized to the session, including reading and writing data, and managing file operations.

## Properties

### 

```python
session  # The Session instance that this ContextManager belongs to
```

## Methods

### info

Gets information about context synchronization status.

```python
info(context_id: Optional[str] = None, path: Optional[str] = None, task_type: Optional[str] = None) -> ContextInfoResult
```

**Parameters:**
- `context_id` (str, optional): The ID of the context to get information for.
- `path` (str, optional): The path where the context is mounted.
- `task_type` (str, optional): The type of task to get information for.

**Returns:**
- `ContextInfoResult`: A result object containing the context status data, success status, and request ID. This class inherits from `ApiResponse`.
  - `context_status_data` (List[ContextStatusData]): A list of context status data objects.

**Example:**
```python
from agentbay import AgentBay

# Initialize the SDK
agent_bay = AgentBay(api_key="your_api_key")

# Create a session
result = agent_bay.create()
if result.success:
    session = result.session
    
    # Get context synchronization information
    info_result = session.context.info()
    if info_result.context_status_data:
        for item in info_result.context_status_data:
            print(f"Context {item.context_id} status: {item.status}")
    else:
        print("No context synchronization tasks found")
```

### sync

Synchronizes a context with the session.

```python
sync(context_id: Optional[str] = None, path: Optional[str] = None, mode: Optional[str] = None) -> ContextSyncResult
```

**Parameters:**
- `context_id` (str, optional): The ID of the context to synchronize.
- `path` (str, optional): The path where the context should be mounted.
- `mode` (str, optional): The synchronization mode.

**Returns:**
- `ContextSyncResult`: A result object containing success status and request ID.
  - `success` (bool): Indicates whether the synchronization was successful.

**Example:**
```python
from agentbay import AgentBay

# Initialize the SDK
agent_bay = AgentBay(api_key="your_api_key")

# Create a session
result = agent_bay.create()
if result.success:
    session = result.session
    
    # Trigger context synchronization
    sync_result = session.context.sync()
    
    if sync_result.success:
        print(f"Context synchronization triggered successfully, request ID: {sync_result.request_id}")
    else:
        print(f"Failed to trigger context synchronization")