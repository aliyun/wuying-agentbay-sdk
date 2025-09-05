# FileSystem Class API Reference

The `FileSystem` class provides methods for file operations within a session in the AgentBay cloud environment. This includes reading, writing, editing, and searching files, as well as directory operations.

## Methods

### create_directory / createDirectory / CreateDirectory

Creates a new directory at the specified path.


```typescript
createDirectory(path: string): Promise<string>
```

**Parameters:**
- `path` (string): The path of the directory to create.

**Returns:**
- `Promise<string>`: A promise that resolves to the response text content if the directory was created successfully.

**Throws:**
- `APIError`: If the directory creation fails.


```typescript
editFile(path: string, edits: Array<{oldText: string, newText: string}>, dryRun?: boolean): Promise<BoolResult>
```

**Parameters:**
- `path` (string): The path of the file to edit.
- `edits` (Array<{oldText: string, newText: string}>): Array of edit operations, each containing oldText and newText.
- `dryRun` (boolean, optional): If true, preview changes without applying them. Default is false.

**Returns:**
- `Promise<BoolResult>`: A promise that resolves to a result object containing success status, boolean data (true if successful), request ID, and error message if any.

**Throws:**
- `APIError`: If the file editing fails.


```typescript
getFileInfo(path: string): Promise<string>
```

**Parameters:**
- `path` (string): The path of the file or directory to inspect.

**Returns:**
- `Promise<string>`: A promise that resolves to textual information about the file or directory.

**Throws:**
- `APIError`: If getting the file information fails.


```typescript
listDirectory(path: string): Promise<any>
```

**Parameters:**
- `path` (string): The path of the directory to list.

**Returns:**
- `Promise<any>`: A promise that resolves to an array of directory entries if parsing is successful, or raw text content.

**Throws:**
- `APIError`: If listing the directory fails.


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


```typescript
readFile(path: string): Promise<FileContentResult>
```

**Parameters:**
- `path` (string): The path of the file to read.

**Returns:**
- `Promise<FileContentResult>`: A promise that resolves to a result object containing file content, success status, request ID, and error message if any.

**Throws:**
- `APIError`: If the file reading fails.

**Note:**
This method automatically handles both small and large files. For large files, it uses internal chunking with a default chunk size of 50KB to overcome API size limitations. No manual chunk size configuration is needed.


```typescript
readMultipleFiles(paths: string[]): Promise<string>
```

**Parameters:**
- `paths` (string[]): Array of paths to the files to read.

**Returns:**
- `Promise<string>`: A promise that resolves to the textual content mapping file paths to their contents.

**Throws:**
- `APIError`: If reading the files fails.


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


```typescript
writeFile(path: string, content: string, mode?: string): Promise<BoolResult>
```

**Parameters:**
- `path` (string): The path of the file to write.
- `content` (string): Content to write to the file.
- `mode` (string, optional): "overwrite" (default), "append", or "create_new".

**Returns:**
- `Promise<BoolResult>`: A promise that resolves to a result object containing success status, boolean data (true if successful), request ID, and error message if any.

**Throws:**
- `APIError`: If writing the file fails.

**Note:**
This method automatically handles both small and large content. For large content, it uses internal chunking with a default chunk size of 50KB to overcome API size limitations. No manual chunk size configuration is needed.


**Deprecated Methods:**

The following methods have been removed in favor of the unified `readFile` and `writeFile` methods:
- `readLargeFile` - Use `readFile` instead (automatic chunking)
- `writeLargeFile` - Use `writeFile` instead (automatic chunking)
