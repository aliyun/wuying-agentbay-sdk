# Command API Reference

> **💡 Async Version**: This documentation covers the synchronous API. For async/await support, see [`AsyncCommand`](../async/async-command.md) which provides the same functionality with async methods.

## ⚡ Related Tutorial

- [Command Execution Guide](../../../../docs/guides/common-features/basics/command-execution.md) - Learn how to execute commands in sessions

## Overview

The Command module provides methods for executing shell commands within a session in the AgentBay cloud environment.
Commands support configurable timeouts and optional working directory or environment settings.




## Command

```python
class Command(BaseService)
```

Async command execution service for session shells in the AgentBay cloud environment.

Use this class for non-blocking command execution; for blocking/synchronous usage,
refer to the `Command` service in the sync API.

### execute\_command

```python
def execute_command(command: str,
                    timeout_ms: int = 50000,
                    cwd: Optional[str] = None,
                    envs: Optional[Dict[str, str]] = None) -> CommandResult
```

Execute a shell command with optional working directory and environment variables.

Executes a shell command in the session environment with configurable timeout,
working directory, and environment variables. The command runs with session
user permissions in a Linux shell environment.

**Arguments**:

    command: The shell command to execute
    timeout_ms: Timeout in milliseconds (default: 50000ms/50s). Maximum allowed
  timeout is 50000ms (50s). If a larger value is provided, it will be
  automatically limited to 50000ms
    cwd: The working directory for command execution. If not specified,
  the command runs in the default session directory
    envs: Environment variables as a dictionary of key-value pairs.
  These variables are set for the command execution only
  

**Returns**:

    CommandResult: Result object containing:
  - success: Whether the command executed successfully (exit_code == 0)
  - output: Command output for backward compatibility (stdout + stderr)
  - exit_code: The exit code of the command execution (0 for success)
  - stdout: Standard output from the command execution
  - stderr: Standard error from the command execution
  - trace_id: Trace ID for error tracking (only present when exit_code != 0)
  - request_id: Unique identifier for this API request
  - error_message: Error description if execution failed
  

**Raises**:

    CommandError: If the command execution fails due to system errors
  

**Example**:

session = agent_bay.create().session
result = session.command.execute_command("echo 'Hello, World!'")
print(result.output)
print(result.exit_code)
session.delete()


**Example**:

result = session.command.execute_command(
"pwd",
timeout_ms=5000,
cwd="/tmp",
    envs={"TEST_VAR": "test_value"}
)
print(result.stdout)
session.delete()

## Best Practices

1. Always specify appropriate timeout values based on expected command duration
2. Handle command execution errors gracefully
3. Use absolute paths when referencing files in commands
4. Be aware that commands run with session user permissions
5. Clean up temporary files created by commands

## See Also

- [Synchronous vs Asynchronous API](../../../docs/guides/async-programming/sync-vs-async.md)

**Related APIs:**
- [Session API Reference](./session.md)
- [FileSystem API Reference](./filesystem.md)

---

*Documentation generated automatically from source code using pydoc-markdown.*
