# Command Class API Reference

The `Command` class provides methods for executing commands within a session in the AgentBay cloud environment.

## Methods

### execute_command / ExecuteCommand

Executes a command in the cloud environment.

#### Python

```python
execute_command(command: str) -> str
```

**Parameters:**
- `command` (str): The command to execute.

**Returns:**
- `str`: The output of the command.

**Raises:**
- `AgentBayError`: If the command execution fails.

#### TypeScript

```typescript
executeCommand(command: string): Promise<string>
```

**Parameters:**
- `command` (string): The command to execute.

**Returns:**
- `Promise<string>`: A promise that resolves to the output of the command.

**Throws:**
- `Error`: If the command execution fails.

#### Golang

```go
ExecuteCommand(command string) (string, error)
```

**Parameters:**
- `command` (string): The command to execute.

**Returns:**
- `string`: The output of the command.
- `error`: An error if the command execution fails.

## Usage Examples

### Python

```python
# Create a session
session = agent_bay.create()

# Execute a command
result = session.command.execute_command("ls -la")
print(f"Command result: {result}")
```

### TypeScript

```typescript
// Create a session
const session = await agentBay.create();

// Execute a command
const result = await session.command.executeCommand('ls -la');
console.log(`Command result: ${result}`);
```

### Golang

```go
// Create a session
session, err := client.Create(nil)
if err != nil {
    // Handle error
}

// Execute a command
result, err := session.Command.ExecuteCommand("ls -la")
if err != nil {
    // Handle error
}
fmt.Printf("Command result: %s\n", result)
```

## Related Resources

- [Session Class](session.md): The session class that provides access to the Command class.
- [FileSystem Class](filesystem.md): Provides methods for reading files within a session.
