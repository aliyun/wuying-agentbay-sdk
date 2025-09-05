# FileSystem Class API Reference

The `FileSystem` class provides methods for file operations within a session in the AgentBay cloud environment. This includes reading, writing, editing, and searching files, as well as directory operations.

## Methods

### create_directory / createDirectory / CreateDirectory

Creates a new directory at the specified path.


```go
CreateDirectory(path string) (*FileDirectoryResult, error)
```

**Parameters:**
- `path` (string): The path of the directory to create.

**Returns:**
- `*FileDirectoryResult`: A result object containing success status and RequestID.
- `error`: An error if the directory creation fails.


```go
EditFile(path string, edits []map[string]string, dryRun bool) (*FileWriteResult, error)
```

**Parameters:**
- `path` (string): The path of the file to edit.
- `edits` ([]map[string]string): Array of edit operations, each containing oldText and newText.
- `dryRun` (bool): If true, preview changes without applying them.

**Returns:**
- `*FileWriteResult`: A result object containing success status and RequestID.
- `error`: An error if the file editing fails.


```go
GetFileInfo(path string) (*FileInfoResult, error)
```

**Parameters:**
- `path` (string): The path of the file or directory to inspect.

**Returns:**
- `*FileInfoResult`: A result object containing file information and RequestID.
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
ReadFile(path string) (*FileReadResult, error)
```

**Parameters:**
- `path` (string): The path of the file to read.

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

**Note:**
This method automatically handles both small and large files. For large files, it uses internal chunking with a default chunk size of 50KB to overcome API size limitations. No manual chunk size configuration is needed.


Reads the contents of multiple files.


```go
ReadMultipleFiles(paths []string) (map[string]string, error)
```

**Parameters:**
- `paths` ([]string): Array of paths to the files to read.

**Returns:**
- `map[string]string`: A map with file paths as keys and their contents as values.
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

**Note:**
This method automatically handles both small and large content. For large content, it uses internal chunking with a default chunk size of 50KB to overcome API size limitations. No manual chunk size configuration is needed.


**Deprecated Methods:**

The following methods have been removed in favor of the unified `ReadFile` and `WriteFile` methods:
- `ReadLargeFile` - Use `ReadFile` instead (automatic chunking)
- `WriteLargeFile` - Use `WriteFile` instead (automatic chunking)

## Usage Examples

### Basic File Operations

```go
package main

import (
    "fmt"
    "log"
)

func main() {
    // Create a session
    agentBay := agentbay.NewAgentBay("your-api-key")
    sessionResult, err := agentBay.Create(nil)
    if err != nil {
        log.Fatal(err)
    }
    session := sessionResult.Session

    // Read a file
    readResult, err := session.FileSystem.ReadFile("/etc/hosts")
    if err != nil {
        log.Printf("Error reading file: %v", err)
    } else {
        fmt.Printf("File content: %s\n", readResult.Content)
    }

    // Create a directory
    createResult, err := session.FileSystem.CreateDirectory("/tmp/test")
    if err != nil {
        log.Printf("Error creating directory: %v", err)
    } else {
        fmt.Printf("Directory created: %t\n", createResult.Success)
    }

    // Write a file
    writeResult, err := session.FileSystem.WriteFile("/tmp/test/example.txt", "Hello, world!", "overwrite")
    if err != nil {
        log.Printf("Error writing file: %v", err)
    } else {
        fmt.Printf("File written successfully: %t\n", writeResult.Success)
    }

    // Edit a file
    edits := []map[string]string{
        {"oldText": "Hello", "newText": "Hi"},
    }
    editResult, err := session.FileSystem.EditFile("/tmp/test/example.txt", edits, false)
    if err != nil {
        log.Printf("Error editing file: %v", err)
    } else {
        fmt.Printf("File edited successfully: %t\n", editResult.Success)
    }

    // Get file info
    fileInfoResult, err := session.FileSystem.GetFileInfo("/tmp/test/example.txt")
    if err != nil {
        log.Printf("Error getting file info: %v", err)
    } else {
        fmt.Printf("File info: %+v\n", fileInfoResult.FileInfo)
    }

    // List directory
    listResult, err := session.FileSystem.ListDirectory("/tmp/test")
    if err != nil {
        log.Printf("Error listing directory: %v", err)
    } else {
        for _, entry := range listResult.Entries {
            entryType := "Directory"
            if !entry.IsDirectory {
                entryType = "File"
            }
            fmt.Printf("%s: %s\n", entryType, entry.Name)
        }
    }
}
```

## Related Resources

- [Session Class](session.md): The session class that provides access to the FileSystem class.
- [Command Class](command.md): Provides methods for executing commands within a session.