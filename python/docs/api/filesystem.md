# FileSystem Class API Reference

The `FileSystem` class provides methods for file operations within a session in the AgentBay cloud environment. This includes reading, writing, editing, and searching files, as well as directory operations and real-time directory monitoring.

## Methods

### create_directory / createDirectory / CreateDirectory

Creates a new directory at the specified path.


```python
create_directory(path: str) -> BoolResult
```

**Parameters:**
- `path` (str): The path of the directory to create.

**Returns:**
- `BoolResult`: A result object containing success status, boolean data (True if successful), request ID, and error message if any.

**Note:**
The return type has been updated from boolean to a structured `BoolResult` object, which provides more detailed information about the operation result.


Edits a file by replacing occurrences of oldText with newText.


```python
edit_file(path: str, edits: List[Dict[str, str]], dry_run: bool = False) -> BoolResult
```

**Parameters:**
- `path` (str): The path of the file to edit.
- `edits` (List[Dict[str, str]]): List of edit operations, each containing oldText and newText.
- `dry_run` (bool, optional): If true, preview changes without applying them. Default is False.

**Returns:**
- `BoolResult`: A result object containing success status, boolean data (True if successful), request ID, and error message if any.


Gets information about a file or directory.


```python
get_file_info(path: str) -> OperationResult
```

**Parameters:**
- `path` (str): The path of the file or directory to inspect.

**Returns:**
- `OperationResult`: A result object containing file information as data, success status, request ID, and error message if any.


Lists the contents of a directory.


```python
list_directory(path: str) -> OperationResult
```

**Parameters:**
- `path` (str): The path of the directory to list.

**Returns:**
- `OperationResult`: A result object containing a list of directory entries as data, success status, request ID, and error message if any.


Moves a file or directory from source to destination.


```python
move_file(source: str, destination: str) -> BoolResult
```

**Parameters:**
- `source` (str): The path of the source file or directory.
- `destination` (str): The path of the destination file or directory.

**Returns:**
- `BoolResult`: A result object containing success status, boolean data (True if successful), request ID, and error message if any.


Reads the contents of a file. Automatically handles large files by chunking.


```python
read_file(path: str) -> FileContentResult
```

**Parameters:**
- `path` (str): The path of the file to read.

**Returns:**
- `FileContentResult`: A result object containing file content, success status, request ID, and error message if any.

**Note:**
This method automatically handles both small and large files. For large files, it uses internal chunking with a default chunk size of 50KB to overcome API size limitations. No manual chunk size configuration is needed.


```python
read_multiple_files(paths: List[str]) -> OperationResult
```

**Parameters:**
- `paths` (List[str]): List of file paths to read.

**Returns:**
- `OperationResult`: A result object containing a dictionary mapping file paths to their contents as data, success status, request ID, and error message if any.


Searches for files matching a pattern in a directory.


```python
search_files(path: str, pattern: str, exclude_patterns: Optional[List[str]] = None) -> OperationResult
```

**Parameters:**
- `path` (str): The path of the directory to start the search.
- `pattern` (str): The pattern to match.
- `exclude_patterns` (List[str], optional): Patterns to exclude. Default is None.

**Returns:**
- `OperationResult`: A result object containing search results as data, success status, request ID, and error message if any.


Writes content to a file. Automatically handles large files by chunking.


```python
write_file(path: str, content: str, mode: str = "overwrite") -> BoolResult
```

**Parameters:**
- `path` (str): The path of the file to write.
- `content` (str): Content to write to the file.
- `mode` (str, optional): "overwrite" (default) or "append".

**Returns:**
- `BoolResult`: A result object containing success status, boolean data (True if successful), request ID, and error message if any.

**Note:**
This method automatically handles both small and large content. For large content, it uses internal chunking with a default chunk size of 50KB to overcome API size limitations. No manual chunk size configuration is needed.

## Directory Monitoring

### watch_directory

Watches a directory for file changes and calls a callback function when changes occur.

```python
watch_directory(
    path: str,
    callback: Callable[[List[FileChangeEvent]], None],
    interval: float = 0.5,
    stop_event: Optional[threading.Event] = None
) -> threading.Thread
```

**Parameters:**
- `path` (str): The directory path to monitor for file changes.
- `callback` (Callable): Callback function that will be called with a list of FileChangeEvent objects when changes are detected.
- `interval` (float, optional): Polling interval in seconds. Default is 0.5.
- `stop_event` (threading.Event, optional): Optional threading.Event to stop the monitoring. If not provided, a new Event will be created and attached to the returned thread.

**Returns:**
- `threading.Thread`: The monitoring thread. Call `thread.start()` to begin monitoring. Use `thread.stop_event.set()` to stop monitoring.

**Example:**
```python
import threading
import time

def on_file_change(events):
    for event in events:
        print(f"{event.event_type}: {event.path} ({event.path_type})")

# Start monitoring
monitor_thread = session.file_system.watch_directory(
    path="/tmp/my_directory",
    callback=on_file_change,
    interval=0.5  # Check every 0.5 seconds
)
monitor_thread.start()

# Do some work...
time.sleep(10)

# Stop monitoring
monitor_thread.stop_event.set()
monitor_thread.join()
```

### FileChangeEvent

Represents a single file change event.

**Attributes:**
- `event_type` (str): Type of the file change event ("create", "modify", "delete").
- `path` (str): Path of the file or directory that changed.
- `path_type` (str): Type of the path ("file" or "directory").

**Methods:**
- `to_dict()`: Convert to dictionary representation.
- `from_dict(data)`: Create FileChangeEvent from dictionary (class method).

### FileChangeResult

Result of file change detection operations.

**Attributes:**
- `success` (bool): Whether the operation was successful.
- `events` (List[FileChangeEvent]): List of file change events.
- `raw_data` (str): Raw response data for debugging.
- `error_message` (str): Error message if the operation failed.

**Methods:**
- `has_changes()`: Check if there are any file changes.
- `get_modified_files()`: Get list of modified file paths.
- `get_created_files()`: Get list of created file paths.
- `get_deleted_files()`: Get list of deleted file paths.
