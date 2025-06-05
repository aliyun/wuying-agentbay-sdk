# FileSystem Class API Reference

The `FileSystem` class provides methods for reading files within a session in the AgentBay cloud environment.

## Methods

### read_file / ReadFile

Reads the contents of a file in the cloud environment.

#### Python

```python
read_file(path: str) -> str
```

**Parameters:**
- `path` (str): The path of the file to read.

**Returns:**
- `str`: The contents of the file.

**Raises:**
- `AgentBayError`: If the file reading fails.

#### TypeScript

```typescript
readFile(filePath: string): Promise<string>
```

**Parameters:**
- `filePath` (string): The path of the file to read.

**Returns:**
- `Promise<string>`: A promise that resolves to the contents of the file.

**Throws:**
- `Error`: If the file reading fails.

#### Golang

```go
ReadFile(path string) (string, error)
```

**Parameters:**
- `path` (string): The path of the file to read.

**Returns:**
- `string`: The contents of the file.
- `error`: An error if the file reading fails.

## Usage Examples

### Python

```python
# Create a session
session = agent_bay.create()

# Read a file
content = session.filesystem.read_file("/etc/hosts")
print(f"File content: {content}")
```

### TypeScript

```typescript
// Create a session
const session = await agentBay.create();

// Read a file
const content = await session.filesystem.readFile('/etc/hosts');
console.log(`File content: ${content}`);
```

### Golang

```go
// Create a session
session, err := client.Create(nil)
if err != nil {
    // Handle error
}

// Read a file
content, err := session.FileSystem.ReadFile("/etc/hosts")
if err != nil {
    // Handle error
}
fmt.Printf("File content: %s\n", content)
```

## Related Resources

- [Session Class](session.md): The session class that provides access to the FileSystem class.
- [Command Class](command.md): Provides methods for executing commands within a session.
