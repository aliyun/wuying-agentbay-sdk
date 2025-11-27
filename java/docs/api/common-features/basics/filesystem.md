# File System API Reference

## 📁 Related Tutorial

- [File Operations Guide](../../../../../docs/guides/common-features/basics/file-operations.md) - Complete guide to file system operations

## Overview

The FileSystem module provides comprehensive file and directory operations in the AgentBay cloud environment, including reading, writing, listing, searching, and transferring files.

## Result Types

### FileContentResult

```java
public class FileContentResult extends ApiResponse
```

Result of file read operations.

**Fields:**
- `success` (boolean): True if operation succeeded
- `content` (String): File content
- `requestId` (String): Request identifier
- `errorMessage` (String): Error description if failed

### BoolResult

```java
public class BoolResult extends ApiResponse
```

Result of boolean operations like write, create directory, edit.

**Fields:**
- `success` (boolean): True if operation succeeded
- `result` (boolean): Operation result value
- `requestId` (String): Request identifier
- `errorMessage` (String): Error description if failed

### DirectoryListResult

```java
public class DirectoryListResult extends ApiResponse
```

Result of directory listing operations.

**Fields:**
- `success` (boolean): True if operation succeeded
- `entries` (List<Map<String, Object>>): List of directory entries with fields:
  - `name` (String): File or directory name
  - `isDirectory` (boolean): True if entry is a directory
- `requestId` (String): Request identifier
- `errorMessage` (String): Error description if failed

### FileInfoResult

```java
public class FileInfoResult extends ApiResponse
```

Result of file info operations.

**Fields:**
- `success` (boolean): True if operation succeeded
- `fileInfo` (Map<String, Object>): File information map
- `requestId` (String): Request identifier
- `errorMessage` (String): Error description if failed

### UploadResult

```java
public class UploadResult extends ApiResponse
```

Result of file upload operations.

### DownloadResult

```java
public class DownloadResult extends ApiResponse
```

Result of file download operations.

## FileSystem

```java
public class FileSystem extends BaseService
```

Provides file system operations for a session.

### readFile

```java
public FileContentResult readFile(String path)
```

Read file content from the cloud environment.

**Parameters:**
- `path` (String): File path

**Returns:**
- `FileContentResult`: Result containing file content and success status

**Example:**

```java
FileContentResult result = session.getFileSystem().readFile("/tmp/test.txt");
if (result.isSuccess()) {
    System.out.println(result.getContent());
}
```

### writeFile

```java
public BoolResult writeFile(String path, String content)
public BoolResult writeFile(String path, String content, String mode)
public BoolResult writeFile(String path, String content, String mode, boolean createParentDir)
```

Write content to a file. Automatically handles large files by chunking.

**Parameters:**
- `path` (String): File path
- `content` (String): Content to write
- `mode` (String): Write mode - "overwrite" (default) or "append"
- `createParentDir` (boolean): Whether to create parent directories (default: false)

**Returns:**
- `BoolResult`: Result containing success status

**Example:**

```java
// Simple write (overwrites file)
BoolResult result = session.getFileSystem().writeFile("/tmp/test.txt", "Hello World");

// Append to file
BoolResult appendResult = session.getFileSystem().writeFile("/tmp/test.txt", "\nNew line", "append");

// Create parent directories if needed
BoolResult dirResult = session.getFileSystem().writeFile("/tmp/nested/dir/file.txt", "content", "overwrite", true);
```

### createDirectory

```java
public BoolResult createDirectory(String path)
```

Create a directory (including parent directories if needed).

**Parameters:**
- `path` (String): Directory path

**Returns:**
- `BoolResult`: Result containing success status

**Example:**

```java
BoolResult result = session.getFileSystem().createDirectory("/tmp/my/nested/dir");
if (result.isSuccess()) {
    System.out.println("Directory created successfully");
}
```

### listDirectory

```java
public DirectoryListResult listDirectory(String path)
```

List contents of a directory.

**Parameters:**
- `path` (String): Directory path

**Returns:**
- `DirectoryListResult`: Result containing list of directory entries

**Example:**

```java
DirectoryListResult result = session.getFileSystem().listDirectory("/tmp");
if (result.isSuccess()) {
    for (Map<String, Object> entry : result.getEntries()) {
        String name = (String) entry.get("name");
        boolean isDir = (Boolean) entry.get("isDirectory");
        System.out.println((isDir ? "[DIR] " : "[FILE] ") + name);
    }
}
```

### getFileInfo

```java
public FileInfoResult getFileInfo(String path)
```

Get detailed information about a file or directory.

**Parameters:**
- `path` (String): File or directory path

**Returns:**
- `FileInfoResult`: Result containing file information

**Example:**

```java
FileInfoResult result = session.getFileSystem().getFileInfo("/tmp/test.txt");
if (result.isSuccess()) {
    Map<String, Object> info = result.getFileInfo();
    System.out.println("File info: " + info);
}
```

### editFile

```java
public BoolResult editFile(String path, List<Map<String, String>> edits)
public BoolResult editFile(String path, List<Map<String, String>> edits, boolean dryRun)
```

Edit a file by replacing specific text portions.

**Parameters:**
- `path` (String): File path
- `edits` (List<Map<String, String>>): List of edit operations, each containing:
  - `oldText` (String): Text to search for and replace
  - `newText` (String): Replacement text
- `dryRun` (boolean): If true, preview changes without applying (default: false)

**Returns:**
- `BoolResult`: Result containing success status

**Example:**

```java
List<Map<String, String>> edits = new ArrayList<>();
Map<String, String> edit = new HashMap<>();
edit.put("oldText", "old value");
edit.put("newText", "new value");
edits.add(edit);

BoolResult result = session.getFileSystem().editFile("/tmp/config.txt", edits);
```

### searchFiles

```java
public FileSearchResult searchFiles(String directory, String pattern)
public FileSearchResult searchFiles(String directory, String pattern, List<String> excludePatterns)
```

Search for files matching a pattern.

**Parameters:**
- `directory` (String): Directory to search in
- `pattern` (String): Search pattern (supports glob patterns: *, ?, [abc])
- `excludePatterns` (List<String>): Patterns to exclude (optional)

**Returns:**
- `FileSearchResult`: Result containing list of matching file paths

**Example:**

```java
FileSearchResult result = session.getFileSystem().searchFiles("/tmp", "*.txt");
if (result.isSuccess()) {
    for (String filePath : result.getMatches()) {
        System.out.println(filePath);
    }
}
```

### readMultipleFiles

```java
public MultipleFileContentResult readMultipleFiles(List<String> paths)
```

Read multiple files at once.

**Parameters:**
- `paths` (List<String>): List of file paths to read

**Returns:**
- `MultipleFileContentResult`: Result containing map of file paths to contents

**Example:**

```java
List<String> paths = Arrays.asList("/tmp/file1.txt", "/tmp/file2.txt");
MultipleFileContentResult result = session.getFileSystem().readMultipleFiles(paths);
if (result.isSuccess()) {
    Map<String, String> filesContent = result.getFilesContent();
    for (Map.Entry<String, String> entry : filesContent.entrySet()) {
        System.out.println(entry.getKey() + ": " + entry.getValue());
    }
}
```

### moveFile

```java
public BoolResult moveFile(String source, String destination)
```

Move or rename a file or directory.

**Parameters:**
- `source` (String): Source path
- `destination` (String): Destination path

**Returns:**
- `BoolResult`: Result containing success status

**Example:**

```java
BoolResult result = session.getFileSystem().moveFile("/tmp/old.txt", "/tmp/new.txt");
```

### deleteFile

```java
public DeleteResult deleteFile(String path)
```

Delete a file or directory.

**Parameters:**
- `path` (String): Path to delete

**Returns:**
- `DeleteResult`: Result containing success status

**Example:**

```java
DeleteResult result = session.getFileSystem().deleteFile("/tmp/test.txt");
```

## File Transfer Operations

### uploadFile

```java
public UploadResult uploadFile(String localPath, String remotePath)
public UploadResult uploadFile(String localPath, String remotePath, String contentType, boolean wait, float waitTimeout, float pollInterval)
```

Upload a local file to the cloud environment.

**Parameters:**
- `localPath` (String): Local file path
- `remotePath` (String): Remote file path in cloud environment
- `contentType` (String): Content type (optional)
- `wait` (boolean): Whether to wait for upload completion (default: true)
- `waitTimeout` (float): Wait timeout in seconds (default: 30.0)
- `pollInterval` (float): Poll interval in seconds (default: 1.5)

**Returns:**
- `UploadResult`: Result containing upload status

**Example:**

```java
// Simple upload
UploadResult result = session.getFileSystem().uploadFile("/local/file.txt", "/tmp/remote.txt");

// Upload with custom parameters
UploadResult customResult = session.getFileSystem().uploadFile(
    "/local/large.zip", "/tmp/data.zip", "application/zip", true, 60.0f, 2.0f
);
```

### downloadFile

```java
public DownloadResult downloadFile(String remotePath)
public DownloadResult downloadFile(String remotePath, String localPath)
public DownloadResult downloadFile(String remotePath, String localPath, boolean overwrite, boolean wait, float waitTimeout, float pollInterval)
```

Download a file from the cloud environment to local system.

**Parameters:**
- `remotePath` (String): Remote file path in cloud environment
- `localPath` (String): Local file path (optional)
- `overwrite` (boolean): Whether to overwrite existing file (default: true)
- `wait` (boolean): Whether to wait for download completion (default: true)
- `waitTimeout` (float): Wait timeout in seconds (default: 30.0)
- `pollInterval` (float): Poll interval in seconds (default: 1.5)

**Returns:**
- `DownloadResult`: Result containing download status

**Example:**

```java
// Simple download (generates local filename)
DownloadResult result = session.getFileSystem().downloadFile("/tmp/remote.txt");

// Download to specific location
DownloadResult customResult = session.getFileSystem().downloadFile("/tmp/data.zip", "/local/data.zip");
```

## Legacy Methods (Deprecated)

The following methods are available but use simplified command-based implementations:

- `read(String path)` - Use `readFile()` instead
- `write(String path, String content)` - Use `writeFile()` instead
- `list(String path)` - Use `listDirectory()` instead
- `mkdir(String path)` - Use `createDirectory()` instead
- `remove(String path)` - Use `deleteFile()` instead
- `copy(String source, String destination)` - **Note**: This method uses shell command (`cp -r`) for implementation, which may not work in all environments. For reliable file transfer, use `uploadFile()` and `downloadFile()` methods instead, or consider using context synchronization.
- `move(String source, String destination)` - Use `moveFile()` instead
- `getInfo(String path)` - Use `getFileInfo()` instead

## Best Practices

1. Always check `result.isSuccess()` before using operation results
2. Use absolute paths for reliability
3. Handle large files appropriately (SDK automatically chunks large writes)
4. Clean up temporary files when no longer needed
5. Use context synchronization for persistent data across sessions
6. Check file existence before operations when needed

## Notes

- File operations are performed in the cloud environment, not locally
- Large files are automatically chunked during write operations
- File transfer operations require context synchronization setup
- Paths use Linux-style forward slashes
- File permissions are managed by the session user

## Related Resources

- [Session API Reference](session.md)
- [Context Sync API Reference](context-sync.md)
- [File System Example](../../../../agentbay/src/main/java/com/aliyun/agentbay/examples/FileSystemExample.java)
- [File Transfer Example](../../../../agentbay/src/main/java/com/aliyun/agentbay/examples/FileTransferExample.java)

---

*Documentation for AgentBay Java SDK*

