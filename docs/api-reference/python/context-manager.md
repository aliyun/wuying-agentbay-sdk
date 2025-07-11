# ContextManager API Reference

The `ContextManager` class provides functionality for managing contexts within a session. It enables you to interact with the contexts that are synchronized to the session, including reading and writing data, and managing file operations.

## Properties

###

```python
session  # The Session instance that this ContextManager belongs to
```

## Methods


Synchronizes a context with the session.


```python
sync_context(context_id: str, path: str, policy: Optional[SyncPolicy] = None) -> OperationResult
```

**Parameters:**
- `context_id` (str): The ID of the context to synchronize.
- `path` (str): The path where the context should be mounted.
- `policy` (SyncPolicy, optional): The synchronization policy. If None, default policy is used.

**Returns:**
- `OperationResult`: A result object containing success status, request ID, and error message if any.

**Example:**
```python
from agentbay import AgentBay
from agentbay.context_sync import SyncPolicy

# Initialize the SDK
agent_bay = AgentBay(api_key="your_api_key")

# Create a session
result = agent_bay.create()
if result.success:
    session = result.session
    
    # Get or create a context
    context_result = agent_bay.context.get("my-context", create=True)
    if context_result.success:
        # Synchronize the context with the session
        sync_result = session.context.sync_context(
            context_id=context_result.context.id,
            path="/mnt/persistent",
            policy=SyncPolicy.default()
        )
        
        if sync_result.success:
            print(f"Context synchronized successfully, request ID: {sync_result.request_id}")
        else:
            print(f"Failed to synchronize context: {sync_result.error_message}")
    else:
        print(f"Failed to get context: {context_result.error_message}")
else:
    print(f"Failed to create session: {result.error_message}")
```


```python
get_info(path: str) -> OperationResult
```

**Parameters:**
- `path` (str): The path where the context is mounted.

**Returns:**
- `OperationResult`: A result object containing the context information as data, success status, request ID, and error message if any.

**Example:**
```python
from agentbay import AgentBay

# Initialize the SDK
agent_bay = AgentBay(api_key="your_api_key")

# Create a session with a synchronized context
# ... (assume context is synchronized to '/mnt/persistent')

# Get information about the synchronized context
info_result = session.context.get_info("/mnt/persistent")
if info_result.success:
    context_info = info_result.data
    print(f"Context Information:")
    print(f"  Context ID: {context_info.context_id}")
    print(f"  Path: {context_info.path}")
    print(f"  State: {context_info.state}")
    print(f"Request ID: {info_result.request_id}")
else:
    print(f"Failed to get context info: {info_result.error_message}")
```


```python
delete_context(path: str) -> OperationResult
```

**Parameters:**
- `path` (str): The path where the context is mounted.

**Returns:**
- `OperationResult`: A result object containing success status, request ID, and error message if any.

**Example:**
```python
from agentbay import AgentBay

# Initialize the SDK
agent_bay = AgentBay(api_key="your_api_key")

# Create a session with a synchronized context
# ... (assume context is synchronized to '/mnt/persistent')

# Delete the synchronized context
delete_result = session.context.delete_context("/mnt/persistent")
if delete_result.success:
    print(f"Context deleted successfully, request ID: {delete_result.request_id}")
else:
    print(f"Failed to delete context: {delete_result.error_message}")
```


```python
list() -> OperationResult
```

**Returns:**
- `OperationResult`: A result object containing the list of synchronized contexts as data, success status, request ID, and error message if any.

**Example:**
```python
from agentbay import AgentBay

# Initialize the SDK
agent_bay = AgentBay(api_key="your_api_key")

# Create a session with synchronized contexts
# ...

# List all synchronized contexts
list_result = session.context.list()
if list_result.success:
    contexts = list_result.data
    print(f"Found {len(contexts)} synchronized contexts:")
    for context in contexts:
        print(f"  Context ID: {context.context_id}, Path: {context.path}, State: {context.state}")
    print(f"Request ID: {list_result.request_id}")
else:
    print(f"Failed to list contexts: {list_result.error_message}")
```
