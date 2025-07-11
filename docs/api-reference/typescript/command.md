# Command Class API Reference

The `Command` class provides methods for executing commands within a session in the AgentBay cloud environment.

## Methods

### execute_command / ExecuteCommand

Executes a command in the cloud environment.


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
