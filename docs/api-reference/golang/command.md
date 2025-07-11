# Command Class API Reference

The `Command` class provides methods for executing commands within a session in the AgentBay cloud environment.

## Methods

### execute_command / ExecuteCommand

Executes a command in the cloud environment.


```go
ExecuteCommand(command string, timeoutMs ...int) (*CommandResult, error)
```

**Parameters:**
- `command` (string): The command to execute.
- `timeoutMs` (int, optional): The timeout for the command execution in milliseconds. Default is 1000ms.

**Returns:**
- `*CommandResult`: A result object containing the command output and RequestID.
- `error`: An error if the command execution fails.

**CommandResult Structure:**
```go
type CommandResult struct {
    RequestID string // Unique request identifier for debugging
    Output    string // The output of the command
}
```

## Usage Examples

###

```python
# Create a session
session_result = agent_bay.create()
if session_result.success:
    session = session_result.session

    # Execute a command with default timeout (1000ms)
    result = session.command.execute_command("ls -la")
    if result.success:
        print(f"Command result: {result.data}")
    else:
        print(f"Command failed: {result.error_message}")

    # Execute a command with custom timeout (2000ms)
    result_with_timeout = session.command.execute_command("ls -la", timeout_ms=2000)
    if result_with_timeout.success:
        print(f"Command result with custom timeout: {result_with_timeout.data}")
    else:
        print(f"Command failed: {result_with_timeout.error_message}")
```


Executes code in the specified programming language with a timeout.


```go
RunCode(code string, language string, timeoutS ...int) (*CommandResult, error)
```

**Parameters:**
- `code` (string): The code to execute.
- `language` (string): The programming language of the code. Must be either 'python' or 'javascript'.
- `timeoutS` (int, optional): The timeout for the code execution in seconds. Default is 300s.

**Returns:**
- `*CommandResult`: A result object containing the code execution output and RequestID.
- `error`: An error if the code execution fails or if an unsupported language is specified.

## Usage Examples

###

```python
# Create a session
session_result = agent_bay.create()
if session_result.success:
    session = session_result.session

    # Execute Python code
    python_code = """
    print("Hello, world!")
    x = 1 + 1
    print(x)
    """
    result = session.command.run_code(python_code, "python")
    if result.success:
        print(f"Python code execution result: {result.data}")
    else:
        print(f"Code execution failed: {result.error_message}")

    # Execute JavaScript code
    js_code = """
    log("Hello, world!");
    const x = 1 + 1;
    log(x);
    """
    result_js = session.command.run_code(js_code, "javascript", timeout_s=600)
    if result_js.success:
        print(f"JavaScript code execution result: {result_js.data}")
    else:
        print(f"Code execution failed: {result_js.error_message}")
```

## Related Resources

- [Session Class](session.md): The session class that provides access to the Command class.
- [FileSystem Class](filesystem.md): Provides methods for reading files within a session.