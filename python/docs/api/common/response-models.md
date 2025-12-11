# Response Models API Reference

API response models for AgentBay SDK.

## ApiResponse

```python
class ApiResponse()
```

Base class for all API responses, containing RequestID

### get\_request\_id

```python
def get_request_id() -> str
```

Returns the unique identifier for the API request.

## SessionPauseResult

```python
class SessionPauseResult(ApiResponse)
```

Result of session pause operations.

## SessionResumeResult

```python
class SessionResumeResult(ApiResponse)
```

Result of session resume operations.

## SessionResult

```python
class SessionResult(ApiResponse)
```

Result of operations returning a single Session.

## SessionListResult

```python
class SessionListResult(ApiResponse)
```

Result of operations returning a list of Sessions.

## DeleteResult

```python
class DeleteResult(ApiResponse)
```

Result of delete operations.

## GetSessionData

```python
class GetSessionData()
```

Data returned by GetSession API.

## GetSessionResult

```python
class GetSessionResult(ApiResponse)
```

Result of GetSession operations.

## OperationResult

```python
class OperationResult(ApiResponse)
```

Result of general operations.

## BoolResult

```python
class BoolResult(ApiResponse)
```

Result of operations returning a boolean value.

## AdbUrlResult

```python
class AdbUrlResult(ApiResponse)
```

Result of ADB URL retrieval operation.

### extract\_request\_id

```python
def extract_request_id(response) -> str
```

Extracts RequestID from API response.
This is a helper function used to extract RequestID in all API methods.

**Arguments**:

    response: The response object from the API call.
  

**Returns**:

    str: The request ID extracted from the response, or an empty string if not
  found.

## McpToolsResult

```python
class McpToolsResult(ApiResponse)
```

Result containing MCP tools list and request ID.

## McpToolResult

```python
class McpToolResult(ApiResponse)
```

Result of an MCP tool call.

#### Response

```python
Response = ApiResponse
```

## See Also

- [Synchronous vs Asynchronous API](../../../../docs/guides/async-programming/sync-vs-async.md)

---

*Documentation generated automatically from source code using pydoc-markdown.*
