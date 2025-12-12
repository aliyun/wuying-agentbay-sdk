# AgentBay API Reference

> **💡 Async Version**: This documentation covers the synchronous API. For async/await support, see [`AsyncAgentBay`](../async/async-agentbay.md) which provides the same functionality with async methods.

## 🚀 Related Tutorial

- [First Session Tutorial](../../../../docs/quickstart/first-session.md) - Get started with creating your first AgentBay session



## Config

```python
class Config()
```

### \_\_init\_\_

```python
def __init__(self, endpoint: str, timeout_ms: int)
```

## AgentBay

```python
class AgentBay()
```

AgentBay represents the main client for interacting with the AgentBay cloud runtime
environment asynchronously.

### \_\_init\_\_

```python
def __init__(self, api_key: str = "",
             cfg: Optional[Config] = None,
             env_file: Optional[str] = None)
```

Initialize AgentBay client.

**Arguments**:

    api_key: API key for authentication. If not provided, will read from AGENTBAY_API_KEY environment variable.
    cfg: Configuration object. If not provided, will load from environment variables and .env file.
    env_file: Custom path to .env file. If not provided, will search upward from current directory.

### create

```python
def create(params: Optional[CreateSessionParams] = None) -> SessionResult
```

Create a new session in the AgentBay cloud environment asynchronously.

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

### list

```python
def list(labels: Optional[Dict[str, str]] = None,
         page: Optional[int] = None,
         limit: Optional[int] = None) -> SessionListResult
```

Returns paginated list of session IDs filtered by labels asynchronously.

**Arguments**:

- `labels` _Optional[Dict[str, str]], optional_ - Labels to filter sessions.
  Defaults to None (returns all sessions).
- `page` _Optional[int], optional_ - Page number for pagination (starting from 1).
  Defaults to None (returns first page).
- `limit` _Optional[int], optional_ - Maximum number of items per page.
  Defaults to None (uses default of 10).
  

**Returns**:

    SessionListResult: Paginated list of session IDs that match the labels.

### delete

```python
def delete(session: Session, sync_context: bool = False) -> DeleteResult
```

Delete a session by session object asynchronously.

**Arguments**:

- `session` _Session_ - The session to delete.
- `sync_context` _bool_ - Whether to sync context data (trigger file uploads)
  before deleting the session. Defaults to False.
  

**Returns**:

    DeleteResult: Result indicating success or failure and request ID.

### get\_session

```python
def get_session(session_id: str) -> GetSessionResult
```

Get session information by session ID asynchronously.

This method retrieves detailed session metadata from the API. Unlike `get()`,
this returns raw session data without creating a Session object.

**Arguments**:

- `session_id` _str_ - The ID of the session to retrieve.
  

**Returns**:

    GetSessionResult: Result containing session information.

### get

```python
def get(session_id: str) -> SessionResult
```

Get a session by its ID asynchronously.

**Arguments**:

- `session_id` _str_ - The ID of the session to retrieve. Must be a non-empty string.
  

**Returns**:

    SessionResult: Result containing the Session instance, request ID, and success status.

### pause

```python
def pause(session: Session,
          timeout: int = 600,
          poll_interval: float = 2.0) -> SessionPauseResult
```

Asynchronously pause a session, putting it into a dormant state.

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

### pause\_async

```python
def pause_async(session: Session) -> SessionPauseResult
```

Fire-and-return pause: trigger PauseSessionAsync without waiting for PAUSED.

This method directly calls the PauseSessionAsync API without waiting for the session
to reach the PAUSED state. For behavior that waits for the PAUSED state,
use the pause() method instead.

**Arguments**:

- `session` _Session_ - The session to pause.
  

**Returns**:

    SessionPauseResult: Result containing the request ID and success status.

### resume

```python
def resume(session: Session,
           timeout: int = 600,
           poll_interval: float = 2.0) -> SessionResumeResult
```

Asynchronously resume a session from a paused state.

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

### resume\_async

```python
def resume_async(session: Session) -> SessionResumeResult
```

Fire-and-return resume: trigger ResumeSessionAsync without waiting for RUNNING.

This method directly calls the ResumeSessionAsync API without waiting for the session
to reach the RUNNING state. For behavior that waits for the RUNNING state,
use the resume() method instead.

**Arguments**:

- `session` _Session_ - The session to resume.
  

**Returns**:

    SessionResumeResult: Result containing the request ID and success status.

## See Also

- [Synchronous vs Asynchronous API](../../../docs/guides/async-programming/sync-vs-async.md)

**Related APIs:**
- [Session API Reference](./session.md)
- [Context API Reference](./context.md)

---

*Documentation generated automatically from source code using pydoc-markdown.*
