# Command Class API Reference

The `Command` class provides methods for executing commands within a session in the AgentBay cloud environment.

## Methods

### execute_command / ExecuteCommand

Executes a command in the cloud environment.


```python
execute_command(command: str, timeout_ms: int = 1000) -> OperationResult
```

**Parameters:**
- `command` (str): The command to execute.
- `timeout_ms` (int, optional): The timeout for the command execution in milliseconds. Default is 1000ms.

**Returns:**
- `OperationResult`: A result object containing the command output as data, success status, request ID, and error message if any.


```python
run_code(code: str, language: str, timeout_s: int = 300) -> OperationResult
```

**Parameters:**
- `code` (str): The code to execute.
- `language` (str): The programming language of the code. Must be either 'python' or 'javascript'.
- `timeout_s` (int, optional): The timeout for the code execution in seconds. Default is 300s.

**Returns:**
- `OperationResult`: A result object containing the code execution output as data, success status, request ID, and error message if any.
