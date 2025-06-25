# Command Class API Reference

The `Command` class provides methods for executing commands within a session in the AgentBay cloud environment.

## Methods

### execute_command / ExecuteCommand

Executes a command in the cloud environment.

#### Python

```python
execute_command(command: str, timeout_ms: int = 1000) -> str
```

**Parameters:**
- `command` (str): The command to execute.
- `timeout_ms` (int, optional): The timeout for the command execution in milliseconds. Default is 1000ms.

**Returns:**
- `str`: The output of the command.

**Raises:**
- `AgentBayError`: If the command execution fails.

#### TypeScript

```typescript
executeCommand(command: string, timeoutMs: number = 1000): Promise<string>
```

**Parameters:**
- `command` (string): The command to execute.
- `timeoutMs` (number, optional): The timeout for the command execution in milliseconds. Default is 1000ms.

**Returns:**
- `Promise<string>`: A promise that resolves to the output of the command.

**Throws:**
- `Error`: If the command execution fails.

#### Golang

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

### Python

```python
# Create a session
session = agent_bay.create()

# Execute a command with default timeout (1000ms)
result = session.command.execute_command("ls -la")
print(f"Command result: {result}")

# Execute a command with custom timeout (2000ms)
result_with_timeout = session.command.execute_command("ls -la", timeout_ms=2000)
print(f"Command result with custom timeout: {result_with_timeout}")
```

### TypeScript

```typescript
// Create a session
const session = await agentBay.create();

// Execute a command with default timeout (1000ms)
const result = await session.command.executeCommand('ls -la');
log(`Command result: ${result}`);

// Execute a command with custom timeout (2000ms)
const resultWithTimeout = await session.command.executeCommand('ls -la', 2000);
log(`Command result with custom timeout: ${resultWithTimeout}`);
```

### Golang

```go
// Create a session
sessionResult, err := client.Create(nil)
if err != nil {
    // Handle error
}
session := sessionResult.Session

// Execute a command with default timeout (1000ms)
result, err := session.Command.ExecuteCommand("ls -la")
if err != nil {
    // Handle error
}
fmt.Printf("Command result: %s (RequestID: %s)\n", result.Output, result.RequestID)

// Execute a command with custom timeout (2000ms)
resultWithTimeout, err := session.Command.ExecuteCommand("ls -la", 2000)
if err != nil {
    // Handle error
}
fmt.Printf("Command result with custom timeout: %s (RequestID: %s)\n", 
    resultWithTimeout.Output, resultWithTimeout.RequestID)
```

### run_code / RunCode

Executes code in the specified programming language with a timeout.

#### Python

```python
run_code(code: str, language: str, timeout_s: int = 300) -> str
```

**Parameters:**
- `code` (str): The code to execute.
- `language` (str): The programming language of the code. Must be either 'python' or 'javascript'.
- `timeout_s` (int, optional): The timeout for the code execution in seconds. Default is 300s.

**Returns:**
- `str`: The output of the code execution.

**Raises:**
- `CommandError`: If the code execution fails or if an unsupported language is specified.

#### TypeScript

```typescript
runCode(code: string, language: string, timeoutS: number = 300): Promise<string>
```

**Parameters:**
- `code` (string): The code to execute.
- `language` (string): The programming language of the code. Must be either 'python' or 'javascript'.
- `timeoutS` (number, optional): The timeout for the code execution in seconds. Default is 300s.

**Returns:**
- `Promise<string>`: A promise that resolves to the output of the code execution.

**Throws:**
- `APIError`: If the code execution fails or if an unsupported language is specified.

#### Golang

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

### Python

```python
# Create a session
session = agent_bay.create()

# Execute Python code
python_code = """
print("Hello, world!")
x = 1 + 1
print(x)
"""
result = session.command.run_code(python_code, "python")
print(f"Python code execution result: {result}")

# Execute JavaScript code
js_code = """
log("Hello, world!");
const x = 1 + 1;
log(x);
"""
result_js = session.command.run_code(js_code, "javascript", timeout_s=600)
print(f"JavaScript code execution result: {result_js}")
```

### TypeScript

```typescript
// Create a session
const session = await agentBay.create();

// Execute Python code
const pythonCode = `
print("Hello, world!")
x = 1 + 1
print(x)
`;
const result = await session.command.runCode(pythonCode, 'python');
log(`Python code execution result: ${result}`);

// Execute JavaScript code
const jsCode = `
log("Hello, world!");
const x = 1 + 1;
log(x);
`;
const resultJs = await session.command.runCode(jsCode, 'javascript', 600);
log(`JavaScript code execution result: ${resultJs}`);
```

### Golang

```go
// Create a session
sessionResult, err := client.Create(nil)
if err != nil {
    // Handle error
}
session := sessionResult.Session

// Execute Python code
pythonCode := `
print("Hello, world!")
x = 1 + 1
print(x)
`
result, err := session.Command.RunCode(pythonCode, "python")
if err != nil {
    // Handle error
}
fmt.Printf("Python code execution result: %s (RequestID: %s)\n", result.Output, result.RequestID)

// Execute JavaScript code with custom timeout
jsCode := `
log("Hello, world!");
const x = 1 + 1;
log(x);
`
resultJs, err := session.Command.RunCode(jsCode, "javascript", 600)
if err != nil {
    // Handle error
}
fmt.Printf("JavaScript code execution result: %s (RequestID: %s)\n", resultJs.Output, resultJs.RequestID)
```

## Related Resources

- [Session Class](session.md): The session class that provides access to the Command class.
- [FileSystem Class](filesystem.md): Provides methods for reading files within a session.
