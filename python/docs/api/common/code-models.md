# Code Execution Models API Reference

> **💡 Async Version**: This documentation covers the synchronous API. For async/await support, see [`AsyncCode`](../async/async-code.md) which provides the same functionality with async methods.

## 💻 Related Tutorial

- [Code Execution Guide](../../../../docs/guides/codespace/code-execution.md) - Execute code in isolated environments

## Overview

The Code module provides secure code execution capabilities in isolated environments.
It supports multiple programming languages including Python, JavaScript, and more.


## Requirements

- Requires `code_latest` image for code execution features



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

## Best Practices

1. Validate code syntax before execution
2. Set appropriate execution timeouts
3. Handle execution errors and exceptions
4. Use proper resource limits to prevent resource exhaustion
5. Clean up temporary files after code execution

## See Also

- [Synchronous vs Asynchronous API](../../../../python/docs/guides/async-programming/sync-vs-async.md)

**Related APIs:**
- [Session API Reference](./session.md)

---

*Documentation generated automatically from source code using pydoc-markdown.*
