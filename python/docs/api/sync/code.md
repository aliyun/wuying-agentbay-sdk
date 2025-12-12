# Code API Reference

> **💡 Async Version**: This documentation covers the synchronous API. For async/await support, see [`AsyncCode`](../async/async-code.md) which provides the same functionality with async methods.

## 💻 Related Tutorial

- [Code Execution Guide](../../../../docs/guides/codespace/code-execution.md) - Execute code in isolated environments

## Overview

The Code module provides secure code execution capabilities in isolated environments.
It supports multiple programming languages including Python, JavaScript, and more.


## Requirements

- Requires `code_latest` image for code execution features



## Code

```python
class Code(BaseService)
```

Handles code execution operations in the AgentBay cloud environment.

### run\_code

```python
def run_code(code: str,
             language: str,
             timeout_s: int = 60) -> EnhancedCodeExecutionResult
```

Execute code in the specified language with a timeout.

**Arguments**:

    code: The code to execute.
    language: The programming language of the code. Must be either 'python'
  or 'javascript'.
    timeout_s: The timeout for the code execution in seconds. Default is 60s.
    Note: Due to gateway limitations, each request cannot exceed 60 seconds.
  

**Returns**:

    EnhancedCodeExecutionResult: Result object containing success status, execution
  result, and error message if any.
  

**Raises**:

    CommandError: If the code execution fails or if an unsupported language is
  specified.
  
  Important:
  The `run_code` method requires a session created with the `code_latest`
  image to function properly. If you encounter errors indicating that the
  tool is not found, make sure to create your session with
  `image_id="code_latest"` in the `CreateSessionParams`.
  

**Example**:

Execute Python code in a code execution environment

```python
from agentbay import AgentBay, CreateSessionParams

agent_bay = AgentBay(api_key="your_api_key")
result = agent_bay.create(CreateSessionParams(image_id="code_latest"))
code_result = result.session.code.run_code("print('Hello')", "python")
print(code_result.result)
result.session.delete()
```

## Best Practices

1. Validate code syntax before execution
2. Set appropriate execution timeouts
3. Handle execution errors and exceptions
4. Use proper resource limits to prevent resource exhaustion
5. Clean up temporary files after code execution

## See Also

- [Synchronous vs Asynchronous API](../../../docs/guides/async-programming/sync-vs-async.md)

**Related APIs:**
- [Session API Reference](./session.md)

---

*Documentation generated automatically from source code using pydoc-markdown.*
