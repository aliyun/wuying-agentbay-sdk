# Command Class API Reference

The `Command` class provides methods for executing commands within a session in the AgentBay cloud environment.

## Methods

### execute_command

Executes a shell command in the cloud environment.

```python
execute_command(command: str, timeout_ms: int = 1000) -> OperationResult
```

**Parameters:**
- `command` (str): The command to execute.
- `timeout_ms` (int, optional): The timeout for the command execution in milliseconds. Default is 1000ms.

**Returns:**
- `OperationResult`: A result object containing the command output as data, success status, request ID, and error message if any.

**Usage Example:**

```python
import os
from agentbay import AgentBay

# Initialize AgentBay with API key
api_key = os.getenv("AGENTBAY_API_KEY")
ab = AgentBay(api_key=api_key)

# Create a session
session_result = ab.create()
session = session_result.session

# Execute a command
result = session.command.execute_command("ls -la")
if result.success:
    print(f"Command output:\n{result.output}")
    print(f"Request ID: {result.request_id}")
else:
    print(f"Command execution failed: {result.error_message}")

# Execute a command with custom timeout
result_with_timeout = session.command.execute_command("sleep 2 && echo 'Done'", timeout_ms=5000)
if result_with_timeout.success:
    print(f"Command output: {result_with_timeout.output}")
else:
    print(f"Command execution failed: {result_with_timeout.error_message}")
```

## Related Resources

- [Session Class](session.md): The session class that provides access to the Command class.
- [Code Class](code.md): For executing Python and JavaScript code.
- [FileSystem Class](filesystem.md): Provides methods for file operations within a session.
