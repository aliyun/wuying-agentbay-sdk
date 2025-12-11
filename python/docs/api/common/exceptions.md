# Exceptions API Reference

## AgentBayError

```python
class AgentBayError(Exception)
```

Base exception for all AgentBay SDK errors.

## AuthenticationError

```python
class AuthenticationError(AgentBayError)
```

Raised when there is an authentication error.

## APIError

```python
class APIError(AgentBayError)
```

Raised when there is an error with the API.

## FileError

```python
class FileError(AgentBayError)
```

Raised for errors related to file operations.

## CommandError

```python
class CommandError(AgentBayError)
```

Raised for errors related to command execution.

## SessionError

```python
class SessionError(AgentBayError)
```

Raised for errors related to session operations.

## OssError

```python
class OssError(AgentBayError)
```

Raised for errors related to OSS operations.

## BrowserError

```python
class BrowserError(AgentBayError)
```

Raised when there is an error with the browser.

## AgentError

```python
class AgentError(AgentBayError)
```

Raised for errors related to Agent actions.

## ClearanceTimeoutError

```python
class ClearanceTimeoutError(AgentBayError)
```

Raised when context clearing operation times out.

## See Also

- [Synchronous vs Asynchronous API](../../../../docs/guides/async-programming/sync-vs-async.md)

---

*Documentation generated automatically from source code using pydoc-markdown.*
