# FileSystem Class API Reference

The `FileSystem` class provides methods for file operations within a session in the AgentBay cloud environment. This includes reading, writing, editing, and searching files, as well as directory operations.

## Methods

### create_directory / createDirectory / CreateDirectory

Creates a new directory at the specified path.


```go
CreateDirectory(path string) (bool, error)
```

**Parameters:**
- `path` (string): The path of the directory to create.

**Returns:**
- `bool`: True if the directory was created successfully.
- `error`: An error if the directory creation fails.


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


```go
GetFileInfo(path string) (string, error)
```

**Parameters:**
- `path` (string): The path of the file or directory to inspect.

**Returns:**
- `string`: Textual information about the file or directory.
- `error`: An error if getting the file information fails.


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


Reads the contents of multiple files.


```go
ReadMultipleFiles(paths []string) (string, error)
```

**Parameters:**
- `paths` ([]string): Array of paths to the files to read.

**Returns:**
- `string`: Textual content mapping file paths to their contents.
- `error`: An error if reading the files fails.


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


```go
ReadLargeFile(path string, chunkSize int) (string, error)
```

**Parameters:**
- `path` (string): The path of the file to read.
- `chunkSize` (int): Size of each chunk in bytes.

**Returns:**
- `string`: The complete file content.
- `error`: An error if reading the file fails.


Writes a large file in chunks to handle size limitations of the underlying API.


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

###

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

## Related Resources

- [Session Class](session.md): The session class that provides access to the FileSystem class.
- [Command Class](command.md): Provides methods for executing commands within a session.