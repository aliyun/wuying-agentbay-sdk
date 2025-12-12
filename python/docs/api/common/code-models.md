# Code Execution Models API Reference

## Overview

The Code Execution Models define data structures for code execution results, logs, and errors.
These models provide enhanced support for multi-format outputs and detailed execution information.




Code module data models.

## ExecutionResult

```python
@dataclass
class ExecutionResult()
```

Single execution result supporting multiple formats

### formats

```python
def formats() -> List[str]
```

Returns all available formats

## ExecutionLogs

```python
@dataclass
class ExecutionLogs()
```

Execution logs

#### stdout: `List[str]`

```python
stdout = field(default_factory=list)
```

#### stderr: `List[str]`

```python
stderr = field(default_factory=list)
```

## ExecutionError

```python
@dataclass
class ExecutionError()
```

Detailed error information

#### name: `str`

```python
name = None
```

#### value: `str`

```python
value = None
```

#### traceback: `str`

```python
traceback = None
```

## EnhancedCodeExecutionResult

```python
@dataclass
class EnhancedCodeExecutionResult(ApiResponse)
```

Enhanced code execution result

### result

```python
@property
def result() -> str
```

Backward compatible text result

## CodeExecutionResult

```python
class CodeExecutionResult(ApiResponse)
```

Result of code execution operations. Kept for backward compatibility but users should transition to EnhancedCodeExecutionResult.

### \_\_init\_\_

```python
def __init__(self, request_id: str = "",
             success: bool = False,
             result: str = "",
             error_message: str = "")
```

Initialize a CodeExecutionResult.

**Arguments**:

- `request_id` _str, optional_ - Unique identifier for the API request.
- `success` _bool, optional_ - Whether the operation was successful.
- `result` _str, optional_ - The execution result.
- `error_message` _str, optional_ - Error message if the operation failed.

## See Also

- [Synchronous vs Asynchronous API](../../../docs/guides/async-programming/sync-vs-async.md)

**Related APIs:**
- [Session API Reference](../sync/session.md)
- [Code API Reference](../sync/code.md)

---

*Documentation generated automatically from source code using pydoc-markdown.*
