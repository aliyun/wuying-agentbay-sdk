# AgentBay Class API Reference

The `AgentBay` class is the main entry point for interacting with the AgentBay cloud environment. It provides methods for creating, retrieving, listing, and deleting sessions.

## Constructor

### AgentBay

```python
AgentBay(api_key=None, cfg=None)
```

**Parameters:**
- `api_key` (str, optional): The API key for authentication. If not provided, the SDK will look for the `AGENTBAY_API_KEY` environment variable.
- `cfg` (Config, optional): Configuration object containing region_id, endpoint, and timeout_ms. If not provided, default configuration is used.

**Raises:**
- `ValueError`: If no API key is provided and `AGENTBAY_API_KEY` environment variable is not set.

## Properties

###

```python
context
```
A `ContextService` instance for managing persistent contexts. See the [Context API Reference](context.md) for more details.

## Methods


Creates a new session in the AgentBay cloud environment.


```python
create(params: Optional[CreateSessionParams] = None) -> SessionResult
```

**Parameters:**
- `params` (CreateSessionParams, optional): Parameters for session creation. If None, default parameters will be used.

**Returns:**
- `SessionResult`: A result object containing the new Session instance, success status, request ID, and error message if any.

**Behavior:**
- When `params` includes valid `persistence_data_list`, after creating the session, the API will check `session.context.info` to retrieve ContextStatusData.
- It will continuously monitor all data items' Status in ContextStatusData until all items show either "Success" or "Failed" status, or until the maximum retry limit (150 times with 2-second intervals) is reached.
- Any "Failed" status items will have their error messages printed.
- The create operation only returns after context status checking completes.

**Raises:**
- `AgentBayError`: If the session creation fails due to API errors or other issues.

**Example:**
```python
from agentbay import AgentBay, Config
from agentbay.session_params import CreateSessionParams
from agentbay.context_sync import ContextSync, SyncPolicy

# Initialize the SDK with default configuration
agent_bay = AgentBay(api_key="your_api_key")

# Or initialize with custom configuration
config = Config(
    region_id="us-west-1",
    endpoint="https://agentbay.example.com",
    timeout_ms=30000
)
agent_bay_with_config = AgentBay(api_key="your_api_key", cfg=config)

# Create a session with default parameters
default_result = agent_bay.create()
if default_result.success:
    default_session = default_result.session
    print(f"Created session with ID: {default_session.session_id}")

# Create a session with custom parameters
params = CreateSessionParams(
    image_id="linux_latest",
    labels={"project": "demo", "environment": "testing"},
    context_id="your_context_id"  # DEPRECATED: Use context_syncs instead
)
custom_result = agent_bay.create(params)
if custom_result.success:
    custom_session = custom_result.session
    print(f"Created custom session with ID: {custom_session.session_id}")

# RECOMMENDED: Create a session with context synchronization
context_sync = ContextSync.new(
    context_id="your_context_id",
    path="/mnt/persistent",
    policy=SyncPolicy.default()
)
sync_params = CreateSessionParams(
    image_id="linux_latest",
    context_syncs=[context_sync]
)
sync_result = agent_bay.create(sync_params)
if sync_result.success:
    sync_session = sync_result.session
    print(f"Created session with context sync: {sync_session.session_id}")
```


```python
list() -> List[Session]
```

**Returns:**
- `List[Session]`: A list of Session instances currently cached in the client.

**Raises:**
- `AgentBayError`: If the session listing fails.

**Example:**
```python
from agentbay import AgentBay

# Initialize the SDK
agent_bay = AgentBay(api_key="your_api_key")

# List all sessions
sessions = agent_bay.list()
print(f"Found {len(sessions)} sessions:")
for session in sessions:
    print(f"Session ID: {session.session_id}")
```


```python
list_by_labels(params: Optional[Union[ListSessionParams, Dict[str, str]]] = None) -> SessionListResult
```

**Parameters:**
- `params` (ListSessionParams or Dict[str, str], optional): Parameters for filtering sessions by labels. If a dictionary is provided, it will be treated as labels. If None, all sessions will be returned.

**Returns:**
- `SessionListResult`: A result object containing the filtered sessions, pagination information, and request ID.

**Raises:**
- `AgentBayError`: If the session listing fails.

**Example:**
```python
from agentbay import AgentBay
from agentbay.session_params import ListSessionParams

# Initialize the SDK
agent_bay = AgentBay(api_key="your_api_key")

# Create pagination parameters
params = ListSessionParams(
    max_results=10,  # Maximum results per page
    next_token="",   # Token for the next page, empty for the first page
    labels={"environment": "production", "project": "demo"}  # Filter labels
)

# Get the first page of results
result = agent_bay.list_by_labels(params)

# Process the results
if result.success:
    # Print the current page sessions
    for session in result.sessions:
        print(f"Session ID: {session.session_id}")

    # Print pagination information
    print(f"Total count: {result.total_count}")
    print(f"Max results per page: {result.max_results}")
    print(f"Next token: {result.next_token}")

    # If there is a next page, retrieve it
    if result.next_token:
        params.next_token = result.next_token
        next_page_result = agent_bay.list_by_labels(params)
        # Process the next page...
```


```python
delete(session: Session, sync_context: bool = False) -> DeleteResult
```

**Parameters:**
- `session` (Session): The session to delete.
- `sync_context` (bool, optional): If True, the API will trigger a file upload via `session.context.sync` before actually releasing the session. Default is False.

**Returns:**
- `DeleteResult`: A result object containing success status, request ID, and error message if any.

**Behavior:**
- When `sync_context` is True, the API will first call `session.context.sync` to trigger file upload.
- It will then check `session.context.info` to retrieve ContextStatusData and monitor all data items' Status.
- The API waits until all items show either "Success" or "Failed" status, or until the maximum retry limit (150 times with 2-second intervals) is reached.
- Any "Failed" status items will have their error messages printed.
- The session deletion only proceeds after context sync status checking completes.

**Raises:**
- `AgentBayError`: If the session deletion fails.

**Example:**
```python
from agentbay import AgentBay

# Initialize the SDK
agent_bay = AgentBay(api_key="your_api_key")

# Create a session
result = agent_bay.create()
if result.success:
    session = result.session
    print(f"Created session with ID: {session.session_id}")
    
    # Use the session for operations...
    
    # Delete the session when done
    delete_result = agent_bay.delete(session)
    if delete_result.success:
        print("Session deleted successfully")
    else:
        print(f"Failed to delete session: {delete_result.error_message}")
```
