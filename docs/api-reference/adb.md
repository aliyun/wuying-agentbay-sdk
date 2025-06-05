# Adb Class API Reference

The `Adb` class provides methods for executing ADB shell commands within a mobile environment (Android) in the AgentBay cloud environment.

## Methods

### shell / Shell

Executes an ADB shell command in the mobile environment.

#### Python

```python
shell(command: str) -> str
```

**Parameters:**
- `command` (str): The ADB shell command to execute.

**Returns:**
- `str`: The output of the command.

**Raises:**
- `AgentBayError`: If the command execution fails.

#### TypeScript

```typescript
shell(command: string): Promise<string>
```

**Parameters:**
- `command` (string): The ADB shell command to execute.

**Returns:**
- `Promise<string>`: A promise that resolves to the output of the command.

**Throws:**
- `Error`: If the command execution fails.

#### Golang

```go
Shell(command string) (string, error)
```

**Parameters:**
- `command` (string): The ADB shell command to execute.

**Returns:**
- `string`: The output of the command.
- `error`: An error if the command execution fails.

## Usage Examples

### Python

```python
# Create a session
session = agent_bay.create()

# Execute an ADB shell command
result = session.adb.shell("ls /sdcard")
print(f"ADB shell result: {result}")
```

### TypeScript

```typescript
// Create a session
const session = await agentBay.create();

// Execute an ADB shell command
const result = await session.adb.shell('ls /sdcard');
console.log(`ADB shell result: ${result}`);
```

### Golang

```go
// Create a session
session, err := client.Create(nil)
if err != nil {
    // Handle error
}

// Execute an ADB shell command
result, err := session.Adb.Shell("ls /sdcard")
if err != nil {
    // Handle error
}
fmt.Printf("ADB shell result: %s\n", result)
```

## Related Resources

- [Session Class](session.md): The session class that provides access to the Adb class.
- [Command Class](command.md): Provides methods for executing general commands within a session.
