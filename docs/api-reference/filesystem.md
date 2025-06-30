# FileSystem Class API Reference

The `FileSystem` class provides methods for file operations within a session in the AgentBay cloud environment. This includes reading, writing, editing, and searching files, as well as directory operations.

## Methods

### create_directory / createDirectory / CreateDirectory

Creates a new directory at the specified path.

#### TypeScript

```typescript
createDirectory(path: string): Promise<string>
```

**Parameters:**
- `path` (string): The path of the directory to create.

**Returns:**
- `Promise<string>`: A promise that resolves to the response text content if the directory was created successfully.

**Throws:**
- `APIError`: If the directory creation fails.

#### Golang

```go
CreateDirectory(path string) (bool, error)
```

**Parameters:**
- `path` (string): The path of the directory to create.

**Returns:**
- `bool`: True if the directory was created successfully.
- `error`: An error if the directory creation fails.

#### Python

```python
create_directory(path: str) -> BoolResult
```

**Parameters:**
- `path` (str): The path of the directory to create.

**Returns:**
- `BoolResult`: A result object containing success status, boolean data (True if successful), request ID, and error message if any.

**Note:**
The return type has been updated from boolean to a structured `BoolResult` object, which provides more detailed information about the operation result.

### edit_file / editFile / EditFile

Edits a file by replacing occurrences of oldText with newText.

#### TypeScript

```typescript
editFile(path: string, edits: Array<{oldText: string, newText: string}>, dryRun?: boolean): Promise<string>
```

**Parameters:**
- `path` (string): The path of the file to edit.
- `edits` (Array<{oldText: string, newText: string}>): Array of edit operations, each containing oldText and newText.
- `dryRun` (boolean, optional): If true, preview changes without applying them. Default is false.

**Returns:**
- `Promise<string>`: A promise that resolves to the response text content if the file was edited successfully.

**Throws:**
- `APIError`: If the file editing fails.

#### Golang

```go
EditFile(path string, edits []map[string]string, dryRun bool) (bool, error)
```

**Parameters:**
- `path` (string): The path of the file to edit.
- `edits` ([]map[string]string): Array of edit operations, each containing oldText and newText.
- `dryRun` (bool): If true, preview changes without applying them.

**Returns:**
- `bool`: True if the file was edited successfully.
- `error`: An error if the file editing fails.

#### Python

```python
edit_file(path: str, edits: List[Dict[str, str]], dry_run: bool = False) -> BoolResult
```

**Parameters:**
- `path` (str): The path of the file to edit.
- `edits` (List[Dict[str, str]]): List of edit operations, each containing oldText and newText.
- `dry_run` (bool, optional): If true, preview changes without applying them. Default is False.

**Returns:**
- `BoolResult`: A result object containing success status, boolean data (True if successful), request ID, and error message if any.

### get_file_info / getFileInfo / GetFileInfo

Gets information about a file or directory.

#### TypeScript

```typescript
getFileInfo(path: string): Promise<string>
```

**Parameters:**
- `path` (string): The path of the file or directory to inspect.

**Returns:**
- `Promise<string>`: A promise that resolves to textual information about the file or directory.

**Throws:**
- `APIError`: If getting the file information fails.

#### Golang

```go
GetFileInfo(path string) (string, error)
```

**Parameters:**
- `path` (string): The path of the file or directory to inspect.

**Returns:**
- `string`: Textual information about the file or directory.
- `error`: An error if getting the file information fails.

#### Python

```python
get_file_info(path: str) -> OperationResult
```

**Parameters:**
- `path` (str): The path of the file or directory to inspect.

**Returns:**
- `OperationResult`: A result object containing file information as data, success status, request ID, and error message if any.

### list_directory / listDirectory / ListDirectory

Lists the contents of a directory.

#### TypeScript

```typescript
listDirectory(path: string): Promise<any>
```

**Parameters:**
- `path` (string): The path of the directory to list.

**Returns:**
- `Promise<any>`: A promise that resolves to an array of directory entries if parsing is successful, or raw text content.

**Throws:**
- `APIError`: If listing the directory fails.

#### Golang

```go
ListDirectory(path string) (*DirectoryListResult, error)
```

**Parameters:**
- `path` (string): The path of the directory to list.

**Returns:**
- `*DirectoryListResult`: A result object containing directory entries and RequestID.
- `error`: An error if listing the directory fails.

**DirectoryListResult Structure:**
```go
type DirectoryListResult struct {
    RequestID string           // Unique request identifier for debugging
    Entries   []*DirectoryEntry // Array of directory entries
}

type DirectoryEntry struct {
    Name        string // Name of the file or directory
    IsDirectory bool   // Whether this entry is a directory
}
```

#### Python

```python
list_directory(path: str) -> OperationResult
```

**Parameters:**
- `path` (str): The path of the directory to list.

**Returns:**
- `OperationResult`: A result object containing a list of directory entries as data, success status, request ID, and error message if any.

### move_file / moveFile / MoveFile

Moves a file or directory from source to destination.

#### TypeScript

```typescript
moveFile(source: string, destination: string): Promise<string>
```

**Parameters:**
- `source` (string): The path of the source file or directory.
- `destination` (string): The path of the destination file or directory.

**Returns:**
- `Promise<string>`: A promise that resolves to the response text content if the file was moved successfully.

**Throws:**
- `APIError`: If moving the file fails.

#### Golang

```go
MoveFile(source, destination string) (*FileDirectoryResult, error)
```

**Parameters:**
- `source` (string): The path of the source file or directory.
- `destination` (string): The path of the destination file or directory.

**Returns:**
- `*FileDirectoryResult`: A result object containing success status and RequestID.
- `error`: An error if moving the file fails.

**FileDirectoryResult Structure:**
```go
type FileDirectoryResult struct {
    RequestID string // Unique request identifier for debugging
    Success   bool   // Whether the operation was successful
}
```

#### Python

```python
move_file(source: str, destination: str) -> BoolResult
```

**Parameters:**
- `source` (str): The path of the source file or directory.
- `destination` (str): The path of the destination file or directory.

**Returns:**
- `BoolResult`: A result object containing success status, boolean data (True if successful), request ID, and error message if any.

### read_file / readFile / ReadFile

Reads the contents of a file in the cloud environment.

#### Python

```python
read_file(path: str, offset: int = 0, length: int = 0) -> OperationResult
```

**Parameters:**
- `path` (str): The path of the file to read.
- `offset` (int, optional): Start reading from this byte offset. Default is 0.
- `length` (int, optional): Number of bytes to read. If 0, read to end of file. Default is 0.

**Returns:**
- `OperationResult`: A result object containing file content as data, success status, request ID, and error message if any.

#### TypeScript

```typescript
readFile(path: string, offset?: number, length?: number): Promise<string>
```

**Parameters:**
- `path` (string): The path of the file to read.
- `offset` (number, optional): Start reading from this byte offset. Default is 0.
- `length` (number, optional): Number of bytes to read. If 0, read to end of file. Default is 0.

**Returns:**
- `Promise<string>`: A promise that resolves to the contents of the file.

**Throws:**
- `APIError`: If the file reading fails.

#### Golang

```go
ReadFile(path string, optionalParams ...int) (*FileReadResult, error)
```

**Parameters:**
- `path` (string): The path of the file to read.
- `optionalParams` (int, optional): Optional parameters for offset and length.

**Returns:**
- `*FileReadResult`: A result object containing the file content and RequestID.
- `error`: An error if the file reading fails.

**FileReadResult Structure:**
```go
type FileReadResult struct {
    RequestID string // Unique request identifier for debugging
    Content   string // The contents of the file
}
```

### read_multiple_files / readMultipleFiles / ReadMultipleFiles

Reads the contents of multiple files.

#### TypeScript

```typescript
readMultipleFiles(paths: string[]): Promise<string>
```

**Parameters:**
- `paths` (string[]): Array of paths to the files to read.

**Returns:**
- `Promise<string>`: A promise that resolves to the textual content mapping file paths to their contents.

**Throws:**
- `APIError`: If reading the files fails.

#### Golang

```go
ReadMultipleFiles(paths []string) (string, error)
```

**Parameters:**
- `paths` ([]string): Array of paths to the files to read.

**Returns:**
- `string`: Textual content mapping file paths to their contents.
- `error`: An error if reading the files fails.

#### Python

```python
read_multiple_files(paths: List[str]) -> OperationResult
```

**Parameters:**
- `paths` (List[str]): List of file paths to read.

**Returns:**
- `OperationResult`: A result object containing a dictionary mapping file paths to their contents as data, success status, request ID, and error message if any.

### search_files / searchFiles / SearchFiles

Searches for files matching a pattern in a directory.

#### TypeScript

```typescript
searchFiles(path: string, pattern: string, excludePatterns?: string[]): Promise<any[]>
```

**Parameters:**
- `path` (string): The path of the directory to start the search.
- `pattern` (string): Pattern to match.
- `excludePatterns` (string[], optional): Patterns to exclude. Default is an empty array.

**Returns:**
- `Promise<any[]>`: A promise that resolves to an array of search results.

**Throws:**
- `APIError`: If the search fails.

#### Golang

```go
SearchFiles(path, pattern string, excludePatterns []string) (*SearchFilesResult, error)
```

**Parameters:**
- `path` (string): The path of the directory to start the search.
- `pattern` (string): Pattern to match.
- `excludePatterns` ([]string): Patterns to exclude.

**Returns:**
- `*SearchFilesResult`: A result object containing search results and RequestID.
- `error`: An error if the search fails.

**SearchFilesResult Structure:**
```go
type SearchFilesResult struct {
    RequestID string   // Unique request identifier for debugging
    Results   []string // Array of search results
}
```

#### Python

```python
search_files(path: str, pattern: str, exclude_patterns: Optional[List[str]] = None) -> OperationResult
```

**Parameters:**
- `path` (str): The path of the directory to start the search.
- `pattern` (str): The pattern to match.
- `exclude_patterns` (List[str], optional): Patterns to exclude. Default is None.

**Returns:**
- `OperationResult`: A result object containing search results as data, success status, request ID, and error message if any.

### write_file / writeFile / WriteFile

Writes content to a file.

#### TypeScript

```typescript
writeFile(path: string, content: string, mode?: string): Promise<string>
```

**Parameters:**
- `path` (string): The path of the file to write.
- `content` (string): Content to write to the file.
- `mode` (string, optional): "overwrite" (default), "append", or "create_new".

**Returns:**
- `Promise<string>`: A promise that resolves to the response text content if the file was written successfully.

**Throws:**
- `APIError`: If writing the file fails.

#### Golang

```go
WriteFile(path, content string, mode string) (*FileWriteResult, error)
```

**Parameters:**
- `path` (string): The path of the file to write.
- `content` (string): Content to write to the file.
- `mode` (string): "overwrite" (default), "append", or "create_new".

**Returns:**
- `*FileWriteResult`: A result object containing success status and RequestID.
- `error`: An error if writing the file fails.

**FileWriteResult Structure:**
```go
type FileWriteResult struct {
    RequestID string // Unique request identifier for debugging
    Success   bool   // Whether the file was written successfully
}
```

#### Python

```python
write_file(path: str, content: str, mode: str = "overwrite") -> bool
```

**Parameters:**
- `path` (str): The path of the file to write.
- `content` (str): Content to write to the file.
- `mode` (str, optional): "overwrite" (default) or "append".

**Returns:**
- `bool`: True if the file was written successfully.

**Raises:**
- `FileError`: If writing the file fails.

### read_large_file / readLargeFile / ReadLargeFile

Reads a large file in chunks to handle size limitations of the underlying API.

#### TypeScript

```typescript
readLargeFile(path: string, chunkSize?: number): Promise<string>
```

**Parameters:**
- `path` (string): The path of the file to read.
- `chunkSize` (number, optional): Size of each chunk in bytes. Default is 60KB.

**Returns:**
- `Promise<string>`: A promise that resolves to the complete file content.

**Throws:**
- `APIError`: If reading the file fails.

#### Golang

```go
ReadLargeFile(path string, chunkSize int) (string, error)
```

**Parameters:**
- `path` (string): The path of the file to read.
- `chunkSize` (int): Size of each chunk in bytes.

**Returns:**
- `string`: The complete file content.
- `error`: An error if reading the file fails.

### write_large_file / writeLargeFile / WriteLargeFile

Writes a large file in chunks to handle size limitations of the underlying API.

#### TypeScript

```typescript
writeLargeFile(path: string, content: string, chunkSize?: number): Promise<boolean>
```

**Parameters:**
- `path` (string): The path of the file to write.
- `content` (string): Content to write to the file.
- `chunkSize` (number, optional): Size of each chunk in bytes. Default is 60KB.

**Returns:**
- `Promise<boolean>`: A promise that resolves to true if the file was written successfully.

**Throws:**
- `APIError`: If writing the file fails.

#### Golang

```go
WriteLargeFile(path, content string, chunkSize int) (bool, error)
```

**Parameters:**
- `path` (string): The path of the file to write.
- `content` (string): Content to write to the file.
- `chunkSize` (int): Size of each chunk in bytes.

**Returns:**
- `bool`: True if the file was written successfully.
- `error`: An error if writing the file fails.

## Usage Examples

### Python

```python
# Create a session
session = agent_bay.create()

# Read a file
content = session.filesystem.read_file("/etc/hosts")
print(f"File content: {content}")

# Create a directory
session.filesystem.create_directory('/tmp/test')

# Write a file
session.filesystem.write_file('/tmp/test/example.txt', 'Hello, world!')

# Edit a file
session.filesystem.edit_file('/tmp/test/example.txt', [
    {'oldText': 'Hello', 'newText': 'Hi'}
])

# Get file info
file_info = session.filesystem.get_file_info('/tmp/test/example.txt')
print(f"File size: {file_info['size']}")

# List directory
entries = session.filesystem.list_directory('/tmp/test')
for entry in entries:
    entry_type = "Directory" if entry["isDirectory"] else "File"
    print(f"{entry_type}: {entry['name']}")
```

### TypeScript

```typescript
// Create a session
const session = await agentBay.create();

// Read a file
const content = await session.filesystem.readFile('/etc/hosts');
log(`File content: ${content}`);

// Create a directory
await session.filesystem.createDirectory('/tmp/test');

// Write a file
await session.filesystem.writeFile('/tmp/test/example.txt', 'Hello, world!');

// Edit a file
await session.filesystem.editFile('/tmp/test/example.txt', [
  { oldText: 'Hello', newText: 'Hi' }
]);

// Get file info
const fileInfo = await session.filesystem.getFileInfo('/tmp/test/example.txt');
log(`File info: ${fileInfo}`);

// List directory
const entries = await session.filesystem.listDirectory('/tmp/test');
log(`Directory entries: ${JSON.stringify(entries)}`);

// Move a file
await session.filesystem.moveFile('/tmp/test/example.txt', '/tmp/test/moved.txt');

// Read multiple files
const files = await session.filesystem.readMultipleFiles([
  '/tmp/test/moved.txt',
  '/etc/hosts'
]);
log(`Multiple files content: ${files}`);

// Search files
const results = await session.filesystem.searchFiles('/tmp', 'world', ['node_modules']);
for (const result of results) {
  log(`Found in ${result}`);
}

// Read a large file
const largeContent = await session.filesystem.readLargeFile('/path/to/large/file.log');
log(`Large file content length: ${largeContent.length}`);

// Write a large file
await session.filesystem.writeLargeFile('/path/to/large/output.log', largeContent);
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

// Create a directory
success, err := session.FileSystem.CreateDirectory("/tmp/test")
if err != nil {
    // Handle error
}

// Write a file
success, err = session.FileSystem.WriteFile("/tmp/test/example.txt", "Hello, world!", "overwrite")
if err != nil {
    // Handle error
}

// Edit a file
edits := []map[string]string{
    {
        "oldText": "Hello",
        "newText": "Hi",
    },
}
success, err = session.FileSystem.EditFile("/tmp/test/example.txt", edits, false)
if err != nil {
    // Handle error
}

// Get file info
fileInfo, err := session.FileSystem.GetFileInfo("/tmp/test/example.txt")
if err != nil {
    // Handle error
}
fmt.Printf("File info: %s\n", fileInfo)

// Read a large file
largeContent, err := session.FileSystem.ReadLargeFile("/path/to/large/file.log", 1024*60)
if err != nil {
    // Handle error
}
fmt.Printf("Large file content length: %d\n", len(largeContent))

// Write a large file
success, err = session.FileSystem.WriteLargeFile("/path/to/large/output.log", largeContent, 1024*60)
if err != nil {
    // Handle error
}
```

## Related Resources

- [Session Class](session.md): The session class that provides access to the FileSystem class.
- [Command Class](command.md): Provides methods for executing commands within a session.
