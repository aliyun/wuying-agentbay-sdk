# AgentBay API Reference

## 🚀 Related Tutorial

- [First Session Tutorial](../../../../../docs/quickstart/first-session.md) - Get started with creating your first AgentBay session



## Config

```python
class Config()
```

## AgentBay

```python
class AgentBay()
```

AgentBay represents the main client for interacting with the AgentBay cloud runtime
environment.

### create

```python
def create(params: Optional[CreateSessionParams] = None) -> SessionResult
```

Create a new session in the AgentBay cloud environment.

**Arguments**:

- `params` _Optional[CreateSessionParams], optional_ - Parameters for creating the session.
  Defaults to None (uses default configuration).
  

**Returns**:

    SessionResult: Result containing the created session and request ID.
  - success (bool): True if the operation succeeded
  - session (Session): The created session object (if success is True)
  - request_id (str): Unique identifier for this API request
  - error_message (str): Error description (if success is False)
  

**Raises**:

    ValueError: If API key is not provided and AGENTBAY_API_KEY environment variable is not set.
    ClientException: If the API request fails due to network or authentication issues.
  

**Example**:

```python
result = agent_bay.create()
session = result.session
info_result = session.info()
print(f"Session ID: {info_result.session_id}")
session.delete()
```


**Notes**:

- A default file transfer context is automatically created for each session
- For VPC sessions, MCP tools information is automatically fetched
- If context_syncs are provided, the method waits for synchronization to complete
- Session is automatically cached in the AgentBay instance


**See Also**:

AgentBay.get, AgentBay.list, Session.delete, CreateSessionParams

### list

```python
def list(labels: Optional[Dict[str, str]] = None,
         page: Optional[int] = None,
         limit: Optional[int] = None) -> SessionListResult
```

Returns paginated list of session IDs filtered by labels.

**Arguments**:

- `labels` _Optional[Dict[str, str]], optional_ - Labels to filter sessions.
  Defaults to None (returns all sessions).
- `page` _Optional[int], optional_ - Page number for pagination (starting from 1).
  Defaults to None (returns first page).
- `limit` _Optional[int], optional_ - Maximum number of items per page.
  Defaults to None (uses default of 10).
  

**Returns**:

    SessionListResult: Paginated list of session IDs that match the labels.
  - success (bool): True if the operation succeeded
  - session_ids (List[str]): List of session IDs
  - request_id (str): Unique identifier for this API request
  - next_token (str): Token for fetching the next page (empty if no more pages)
  - max_results (int): Maximum number of results per page
  - total_count (int): Total number of sessions matching the filter
  - error_message (str): Error description (if success is False)
  

**Raises**:

    ClientException: If the API request fails due to network or authentication issues.
  

**Example**:

```python
result = agent_bay.list()
print(f"Total sessions: {result.total_count}")

result = agent_bay.list(labels={"project": "demo"}, page=1, limit=10)
print(f"Found {len(result.session_ids)} sessions")
```


**Notes**:

- Page numbers start from 1
- Returns error if page number is less than 1
- Returns error if requested page exceeds available pages
- Empty labels dict returns all sessions


**See Also**:

AgentBay.create, AgentBay.get, Session.info

### delete

```python
def delete(session: Session, sync_context: bool = False) -> DeleteResult
```

Delete a session by session object.

**Arguments**:

- `session` _Session_ - The session to delete.
- `sync_context` _bool_ - Whether to sync context data (trigger file uploads)
  before deleting the session. Defaults to False.
  

**Returns**:

    DeleteResult: Result indicating success or failure and request ID.
  - success (bool): True if deletion succeeded
  - request_id (str): Unique identifier for this API request
  - error_message (str): Error description (if success is False)
  

**Example**:

```python
result = agent_bay.create()
session = result.session
delete_result = agent_bay.delete(session)
print(f"Delete success: {delete_result.success}")
```


**Notes**:

- After deletion, the session object is removed from the AgentBay cache
- If sync_context=True, context data is uploaded to OSS before deletion
- Session cannot be used after deletion


**See Also**:

Session.delete, AgentBay.create, AgentBay.get

### get\_session

```python
def get_session(session_id: str) -> GetSessionResult
```

Get session information by session ID.

This method retrieves detailed session metadata from the API. Unlike `get()`,
this returns raw session data without creating a Session object.

**Arguments**:

- `session_id` _str_ - The ID of the session to retrieve.
  

**Returns**:

    GetSessionResult: Result containing session information.
  - success (bool): True if the operation succeeded
  - data (GetSessionData): Session information object with fields:
  - session_id (str): Session ID
  - app_instance_id (str): Application instance ID
  - resource_id (str): Resource ID
  - resource_url (str): Resource URL for accessing the session
  - vpc_resource (bool): Whether this is a VPC resource
  - network_interface_ip (str): Network interface IP (for VPC sessions)
  - http_port (str): HTTP port (for VPC sessions)
  - token (str): Authentication token (for VPC sessions)
  - request_id (str): Unique identifier for this API request
  - http_status_code (int): HTTP status code
  - code (str): API response code
  - error_message (str): Error description (if success is False)
  

**Example**:

```python
create_result = agent_bay.create()
session_id = create_result.session.session_id
get_result = agent_bay.get_session(session_id)
print(f"Session ID: {get_result.data.session_id}")
create_result.session.delete()
```


**Notes**:

- Returns session metadata without creating a Session object
- Use `get()` instead if you need a Session object for API calls
- Returns error if session does not exist or is no longer valid


**See Also**:

AgentBay.get, AgentBay.create, Session.info

### get

```python
def get(session_id: str) -> SessionResult
```

Get a session by its ID.

**Arguments**:

- `session_id` _str_ - The ID of the session to retrieve. Must be a non-empty string.
  

**Returns**:

    SessionResult: Result containing the Session instance, request ID, and success status.
  - success (bool): True if the operation succeeded
  - session (Session): The session object (if success is True)
  - request_id (str): Unique identifier for this API request
  - error_message (str): Error description (if success is False)
  

**Raises**:

    ClientException: If the API request fails due to network or authentication issues.
  

**Example**:

```python
create_result = agent_bay.create()
session_id = create_result.session.session_id
get_result = agent_bay.get(session_id)
session = get_result.session
info_result = session.info()
session.delete()
```


**Notes**:

- A default file transfer context is automatically created for the retrieved session
- VPC-related information (network_interface_ip, http_port, token) is populated from the API response
- Returns an error if session_id is empty or the session does not exist


**See Also**:

AgentBay.create, AgentBay.list, Session.info

### pause

```python
def pause(session: Session,
          timeout: int = 600,
          poll_interval: float = 2.0) -> SessionPauseResult
```

Synchronously pause a session, putting it into a dormant state.

This method internally calls the PauseSessionAsync API and then polls the GetSession API
to check the session status until it becomes PAUSED or until timeout.

**Arguments**:

- `session` _Session_ - The session to pause.
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

    ClientException: If the API request fails due to network or authentication issues.
  

**Example**:

```python
session = agent_bay.create().session
pause_result = agent_bay.pause(session)
agent_bay.resume(session)
session.delete()
```


**Notes**:

- The session state transitions from RUNNING -> PAUSING -> PAUSED
- Paused sessions consume fewer resources but maintain their state
- Use resume() or resume_async() to restore the session to RUNNING state
- The timeout parameter controls how long to wait for the PAUSED state
- If timeout is exceeded, the method returns with success=False


**See Also**:

AgentBay.pause_async, AgentBay.resume, AgentBay.resume_async, Session.pause, Session.pause_async

### pause\_async

```python
async def pause_async(session: Session) -> SessionPauseResult
```

Asynchronously pause a session, putting it into a dormant state.

This method directly calls the PauseSessionAsync API without waiting for the session
to reach the PAUSED state. For synchronous behavior that waits for the PAUSED state,
use the pause() method instead.

**Arguments**:

- `session` _Session_ - The session to pause.
  

**Returns**:

    SessionPauseResult: Result containing the request ID and success status.
  - success (bool): True if the pause request was accepted by the API
  - request_id (str): Unique identifier for this API request
  - error_message (str): Error description (if success is False)
  - code (str): API response code (if available)
  - message (str): API response message (if available)
  - http_status_code (int): HTTP status code (if available)
  

**Raises**:

    ClientException: If the API request fails due to network or authentication issues.
  

**Example**:

```python
import asyncio

session = agent_bay.create().session
pause_result = await agent_bay.pause_async(session)
await agent_bay.resume_async(session)
session.delete()
```


**Notes**:

- This method does not wait for the session to reach the PAUSED state
- It only submits the pause request to the API
- Use pause() for synchronous behavior that waits for completion
- The session state transitions from RUNNING -> PAUSING -> PAUSED
- Paused sessions consume fewer resources but maintain their state


**See Also**:

AgentBay.pause, AgentBay.resume, AgentBay.resume_async, Session.pause_async

### resume

```python
def resume(session: Session,
           timeout: int = 600,
           poll_interval: float = 2.0) -> SessionResumeResult
```

Synchronously resume a session from a paused state.

This method internally calls the ResumeSessionAsync API and then polls the GetSession API
to check the session status until it becomes RUNNING or until timeout.

**Arguments**:

- `session` _Session_ - The session to resume.
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

    ClientException: If the API request fails due to network or authentication issues.
  

**Example**:

```python
session = agent_bay.create().session
agent_bay.pause(session)
resume_result = agent_bay.resume(session)
session.delete()
```


**Notes**:

- The session state transitions from PAUSED -> RESUMING -> RUNNING
- Only sessions in PAUSED state can be resumed
- Use pause() or pause_async() to put a session into PAUSED state
- The timeout parameter controls how long to wait for the RUNNING state
- If timeout is exceeded, the method returns with success=False


**See Also**:

AgentBay.pause, AgentBay.pause_async, AgentBay.resume_async, Session.resume, Session.resume_async

### resume\_async

```python
async def resume_async(session: Session) -> SessionResumeResult
```

Asynchronously resume a session from a paused state.

This method directly calls the ResumeSessionAsync API without waiting for the session
to reach the RUNNING state. For synchronous behavior that waits for the RUNNING state,
use the resume() method instead.

**Arguments**:

- `session` _Session_ - The session to resume.
  

**Returns**:

    SessionResumeResult: Result containing the request ID and success status.
  - success (bool): True if the resume request was accepted by the API
  - request_id (str): Unique identifier for this API request
  - error_message (str): Error description (if success is False)
  - code (str): API response code (if available)
  - message (str): API response message (if available)
  - http_status_code (int): HTTP status code (if available)
  

**Raises**:

    ClientException: If the API request fails due to network or authentication issues.
  

**Example**:

```python
import asyncio

session = agent_bay.create().session
agent_bay.pause(session)
resume_result = await agent_bay.resume_async(session)
session.delete()
```


**Notes**:

- This method does not wait for the session to reach the RUNNING state
- It only submits the resume request to the API
- Use resume() for synchronous behavior that waits for completion
- The session state transitions from PAUSED -> RESUMING -> RUNNING
- Only sessions in PAUSED state can be resumed


**See Also**:

AgentBay.pause, AgentBay.pause_async, AgentBay.resume, Session.resume_async

## Related Resources

- [Session API Reference](session.md)
- [Context API Reference](context.md)

---

*Documentation generated automatically from source code using pydoc-markdown.*
