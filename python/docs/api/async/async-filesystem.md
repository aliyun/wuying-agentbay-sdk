# AsyncFileSystem API Reference

> **💡 Sync Version**: This documentation covers the asynchronous API. For synchronous operations, see [`FileSystem`](../sync/filesystem.md).
>
> ⚡ **Performance Advantage**: Async API enables concurrent operations with 4-6x performance improvements for parallel tasks.

## 📁 Related Tutorial

- [File Operations Guide](../../../../docs/guides/common-features/basics/file-operations.md) - Complete guide to file system operations



## AsyncFileTransfer

```python
class AsyncFileTransfer()
```

Provides pre-signed URL upload/download functionality between local and OSS,
with integration to Session Context synchronization.

Prerequisites and Constraints:
- Session must be associated with the corresponding context_id and path through
  CreateSessionParams.context_syncs, and remote_path should fall within that
  synchronization path (or conform to backend path rules).
- Requires available AgentBay context service (agent_bay.context) and session context.

### \_\_init\_\_

```python
def __init__(self, agent_bay,
             session,
             *,
             http_timeout: float = 60.0,
             follow_redirects: bool = True)
```

Initialize FileTransfer with AgentBay client and session.

**Arguments**:

    agent_bay: AgentBay instance for context service access
    session: Created session object for context operations
    http_timeout: HTTP request timeout in seconds (default: 60.0)
    follow_redirects: Whether to follow HTTP redirects (default: True)

### upload

```python
async def upload(
        local_path: str,
        remote_path: str,
        *,
        content_type: Optional[str] = None,
        wait: bool = True,
        wait_timeout: float = 30.0,
        poll_interval: float = 1.5,
        progress_cb: Optional[Callable[[int], None]] = None) -> UploadResult
```

Upload workflow:
1) Get OSS pre-signed URL via context.get_file_upload_url
2) Upload local file to OSS using the URL (HTTP PUT)
3) Trigger session.context.sync(mode="download") to sync cloud disk data from OSS
4) If wait=True, poll session.context.info until upload task reaches completion or timeout

Returns UploadResult containing request_ids, HTTP status, ETag and other information.

### download

```python
async def download(
        remote_path: str,
        local_path: str,
        *,
        overwrite: bool = True,
        wait: bool = True,
        wait_timeout: float = 300.0,
        poll_interval: float = 1.5,
        progress_cb: Optional[Callable[[int], None]] = None) -> DownloadResult
```

Download workflow:
1) Trigger session.context.sync(mode="upload") to sync cloud disk data to OSS
2) Get pre-signed download URL via context.get_file_download_url
3) Download the file and save to local local_path
4) If wait=True, wait for download task to reach completion after step 1
   (ensuring backend has prepared the download object)

Returns DownloadResult containing sync and download request_ids, HTTP status, byte count, etc.

## AsyncFileSystem

```python
class AsyncFileSystem(BaseService)
```

Handles file operations in the AgentBay cloud environment.

### \_\_init\_\_

```python
def __init__(self, *args, **kwargs)
```

Initialize FileSystem with FileTransfer capability.

**Arguments**:

    *args: Arguments to pass to BaseService
    **kwargs: Keyword arguments to pass to BaseService

### get\_file\_transfer\_context\_path

```python
async def get_file_transfer_context_path() -> Optional[str]
```

Get the context path for file transfer operations.

This method ensures the context ID is loaded and returns the associated
context path that was retrieved from GetAndLoadInternalContext API.

**Returns**:

    Optional[str]: The context path if available, None otherwise.
  

**Example**:

```python
session = (await agent_bay.create(params)).session
context_path = await session.file_system.get_file_transfer_context_path()
if context_path:
  print(f"Context path: {context_path}")
```

#### DEFAULT\_CHUNK\_SIZE

```python
DEFAULT_CHUNK_SIZE = 50 * 1024
```

### create\_directory

```python
async def create_directory(path: str) -> BoolResult
```

Create a new directory at the specified path.

**Arguments**:

    path: The path of the directory to create.
  

**Returns**:

    BoolResult: Result object containing success status and error message if
  any.
  

**Example**:

```python
session = (await agent_bay.create()).session
create_result = await session.file_system.create_directory("/tmp/mydir")
nested_result = await session.file_system.create_directory("/tmp/parent/child/grandchild")
await session.delete()
```

### delete\_file

```python
async def delete_file(path: str) -> BoolResult
```

Delete a file at the specified path.

**Arguments**:

    path: The path of the file to delete.
  

**Returns**:

    BoolResult: Result object containing success status and error message if any.
  

**Example**:

```python
session = (await agent_bay.create()).session
await session.file_system.write_file("/tmp/to_delete.txt", "hello")
delete_result = await session.file_system.delete_file("/tmp/to_delete.txt")
await session.delete()
```

### edit\_file

```python
async def edit_file(path: str,
                    edits: List[Dict[str, str]],
                    dry_run: bool = False) -> BoolResult
```

Edit a file by replacing occurrences of oldText with newText.

**Arguments**:

    path: The path of the file to edit.
    edits: A list of dictionaries specifying oldText and newText.
    dry_run: If True, preview changes without applying them.
  

**Returns**:

    BoolResult: Result object containing success status and error message if
  any.
  

**Example**:

```python
session = (await agent_bay.create()).session
await session.file_system.write_file("/tmp/config.txt", "DEBUG=false\nLOG_LEVEL=info")
edits = [{"oldText": "false", "newText": "true"}]
edit_result = await session.file_system.edit_file("/tmp/config.txt", edits)
await session.delete()
```

### get\_file\_info

```python
async def get_file_info(path: str) -> FileInfoResult
```

Get information about a file or directory.

**Arguments**:

    path: The path of the file or directory to inspect.
  

**Returns**:

    FileInfoResult: Result object containing file info and error message if any.
  

**Example**:

```python
session = (await agent_bay.create()).session
await session.file_system.write_file("/tmp/test.txt", "Sample content")
info_result = await session.file_system.get_file_info("/tmp/test.txt")
print(info_result.file_info)
await session.delete()
```

### list\_directory

```python
async def list_directory(path: str) -> DirectoryListResult
```

List the contents of a directory.

**Arguments**:

- `path` _str_ - The path of the directory to list.
  

**Returns**:

    DirectoryListResult: Result object containing directory entries and error message if any.
  - success (bool): True if the operation succeeded
  - entries (List[Dict[str, Union[str, bool]]]): List of directory entries (if success is True)
  Each entry contains:
  - name (str): Name of the file or directory
  - isDirectory (bool): True if entry is a directory, False if file
  - request_id (str): Unique identifier for this API request
  - error_message (str): Error description (if success is False)
  

**Raises**:

    FileError: If the directory does not exist or cannot be accessed.
  

**Example**:

```python
session = (await agent_bay.create()).session
await session.file_system.create_directory("/tmp/testdir")
await session.file_system.write_file("/tmp/testdir/file1.txt", "Content 1")
list_result = await session.file_system.list_directory("/tmp/testdir")
print(f"Found {len(list_result.entries)} entries")
await session.delete()
```


**Notes**:

- Returns empty list for empty directories
- Each entry includes name and isDirectory flag
- Does not recursively list subdirectories


**See Also**:

FileSystem.create_directory, FileSystem.get_file_info, FileSystem.read_file

### move\_file

```python
async def move_file(source: str, destination: str) -> BoolResult
```

Move a file or directory from source path to destination path.

**Arguments**:

    source: The source path of the file or directory.
    destination: The destination path.
  

**Returns**:

    BoolResult: Result object containing success status and error message if
  any.
  

**Example**:

```python
session = (await agent_bay.create()).session
await session.file_system.write_file("/tmp/original.txt", "Test content")
move_result = await session.file_system.move_file("/tmp/original.txt", "/tmp/moved.txt")
read_result = await session.file_system.read_file("/tmp/moved.txt")
await session.delete()
```

### read\_multiple\_files

```python
async def read_multiple_files(paths: List[str]) -> MultipleFileContentResult
```

Read the contents of multiple files at once.

**Arguments**:

    paths: A list of file paths to read.
  

**Returns**:

    MultipleFileContentResult: Result object containing a dictionary mapping
  file paths to contents,
  and error message if any.
  

**Example**:

```python
session = (await agent_bay.create()).session
await session.file_system.write_file("/tmp/file1.txt", "Content of file 1")
await session.file_system.write_file("/tmp/file2.txt", "Content of file 2")
await session.file_system.write_file("/tmp/file3.txt", "Content of file 3")
paths = ["/tmp/file1.txt", "/tmp/file2.txt", "/tmp/file3.txt"]
read_result = await session.file_system.read_multiple_files(paths)
await session.delete()
```

### search\_files

```python
async def search_files(
        path: str,
        pattern: str,
        exclude_patterns: Optional[List[str]] = None) -> FileSearchResult
```

Search for files in the specified path using a wildcard pattern.

**Arguments**:

    path: The base directory path to search in.
    pattern: Wildcard pattern to match against file names. Supports * (any characters)
  and ? (single character). Examples: "*.py", "test_*", "*config*".
    exclude_patterns: Optional list of wildcard patterns to exclude from the search.
  

**Returns**:

    FileSearchResult: Result object containing matching file paths and error
  message if any.
  

**Example**:

```python
session = (await agent_bay.create()).session
await session.file_system.write_file("/tmp/test/test_file1.py", "print('hello')")
await session.file_system.write_file("/tmp/test/test_file2.py", "print('world')")
await session.file_system.write_file("/tmp/test/other.txt", "text content")
search_result = await session.file_system.search_files("/tmp/test", "test_*")
await session.delete()
```

### read\_file

```python
async def read_file(path: str) -> FileContentResult
```

Read the contents of a file. Automatically handles large files by chunking.

**Arguments**:

- `path` _str_ - The path of the file to read.
  

**Returns**:

    FileContentResult: Result object containing file content and error message if any.
  - success (bool): True if the operation succeeded
  - content (str): The file content (if success is True)
  - request_id (str): Unique identifier for this API request
  - error_message (str): Error description (if success is False)
  

**Raises**:

    FileError: If the file does not exist or is a directory.
  

**Example**:

```python
session = (await agent_bay.create()).session
write_result = await session.file_system.write_file("/tmp/test.txt", "Hello, World!")
read_result = await session.file_system.read_file("/tmp/test.txt")
print(read_result.content)
await session.delete()
```


**Notes**:

- Automatically handles large files by reading in chunks (default 50KB per chunk)
- Returns empty string for empty files
- Returns error if path is a directory


**See Also**:

FileSystem.write_file, FileSystem.list_directory, FileSystem.get_file_info

### write\_file

```python
async def write_file(path: str,
                     content: str,
                     mode: str = "overwrite") -> BoolResult
```

Write content to a file. Automatically handles large files by chunking.

**Arguments**:

- `path` _str_ - The path of the file to write.
- `content` _str_ - The content to write to the file.
- `mode` _str, optional_ - The write mode. Defaults to "overwrite".
  - "overwrite": Replace file content
  - "append": Append to existing content
  

**Returns**:

    BoolResult: Result object containing success status and error message if any.
  - success (bool): True if the operation succeeded
  - data (bool): True if the file was written successfully
  - request_id (str): Unique identifier for this API request
  - error_message (str): Error description (if success is False)
  

**Raises**:

    FileError: If the write operation fails.
  

**Example**:

```python
session = (await agent_bay.create()).session
write_result = await session.file_system.write_file("/tmp/test.txt", "Hello, World!")
append_result = await session.file_system.write_file("/tmp/test.txt", "\nNew line", mode="append")
read_result = await session.file_system.read_file("/tmp/test.txt")
await session.delete()
```


**Notes**:

- Automatically handles large files by writing in chunks (default 50KB per chunk)
- Creates parent directories if they don't exist
- In "overwrite" mode, replaces the entire file content
- In "append" mode, adds content to the end of the file


**See Also**:

FileSystem.read_file, FileSystem.create_directory, FileSystem.edit_file

### upload\_file

```python
async def upload_file(
        local_path: str,
        remote_path: str,
        *,
        content_type: Optional[str] = None,
        wait: bool = True,
        wait_timeout: float = 30.0,
        poll_interval: float = 1.5,
        progress_cb: Optional[Callable[[int], None]] = None) -> UploadResult
```

Upload a file from local to remote path using pre-signed URLs.

**Arguments**:

    local_path: Local file path to upload
    remote_path: Remote file path to upload to
    content_type: Optional content type for the file
    wait: Whether to wait for the sync operation to complete
    wait_timeout: Timeout for waiting for sync completion
    poll_interval: Interval between polling for sync completion
    progress_cb: Callback for upload progress updates
  

**Returns**:

    UploadResult: Result of the upload operation
  

**Example**:

```python
params = CreateSessionParams(context_syncs=[ContextSync(context_id="ctx-xxx", path="/workspace")])
session = (await agent_bay.create(params)).session
upload_result = await session.file_system.upload_file("/local/file.txt", "/workspace/file.txt")
await session.delete()
```

### download\_file

```python
async def download_file(
        remote_path: str,
        local_path: str,
        *,
        overwrite: bool = True,
        wait: bool = True,
        wait_timeout: float = 30.0,
        poll_interval: float = 1.5,
        progress_cb: Optional[Callable[[int], None]] = None) -> DownloadResult
```

Download a file from remote path to local path using pre-signed URLs.

**Arguments**:

    remote_path: Remote file path to download from
    local_path: Local file path to download to
    overwrite: Whether to overwrite existing local file
    wait: Whether to wait for the sync operation to complete
    wait_timeout: Timeout for waiting for sync completion
    poll_interval: Interval between polling for sync completion
    progress_cb: Callback for download progress updates
  

**Returns**:

    DownloadResult: Result of the download operation
  

**Example**:

```python
params = CreateSessionParams(context_syncs=[ContextSync(context_id="ctx-xxx", path="/workspace")])
session = (await agent_bay.create(params)).session
download_result = await session.file_system.download_file("/workspace/file.txt", "/local/file.txt")
await session.delete()
```

### watch\_directory

```python
def watch_directory(
        path: str,
        callback: Callable[[List[FileChangeEvent]], None],
        interval: float = 0.5,
        stop_event: Optional[threading.Event] = None) -> threading.Thread
```

Watch a directory for file changes and call the callback function when changes occur.

**Arguments**:

    path: The directory path to monitor for file changes.
    callback: Callback function that will be called with a list of FileChangeEvent
  objects when changes are detected.
    interval: Polling interval in seconds. Defaults to 0.5.
    stop_event: Optional threading.Event to stop the monitoring. If not provided,
  a new Event will be created and returned via the thread object.
  

**Returns**:

    threading.Thread: The monitoring thread. Call thread.start() to begin monitoring.
  Use the thread's stop_event attribute to stop monitoring.
  

**Example**:

```python
def on_changes(events):
  print(f"Detected {len(events)} changes")
session = (await agent_bay.create()).session
await session.file_system.create_directory("/tmp/watch_test")
monitor_thread = session.file_system.watch_directory("/tmp/watch_test", on_changes)
monitor_thread.start()
await session.file_system.write_file("/tmp/watch_test/test1.txt", "content 1")
await session.file_system.write_file("/tmp/watch_test/test2.txt", "content 2")
await session.delete()
```

## See Also

- [Synchronous vs Asynchronous API](../../../docs/guides/async-programming/sync-vs-async.md)

**Related APIs:**
- [Session API Reference](./async-session.md)
- [Command API Reference](./async-command.md)

---

*Documentation generated automatically from source code using pydoc-markdown.*
