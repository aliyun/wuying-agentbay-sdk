# FileSystem Class API Reference

The `FileSystem` class provides methods for file operations within a session in the AgentBay cloud environment. This includes reading, writing, editing, and searching files, as well as directory operations.

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


Reads the contents of a file in the cloud environment.


```python
read_file(path: str, offset: int = 0, length: int = 0) -> OperationResult
```

**Parameters:**
- `path` (str): The path of the file to read.
- `offset` (int, optional): Start reading from this byte offset. Default is 0.
- `length` (int, optional): Number of bytes to read. If 0, read to end of file. Default is 0.

**Returns:**
- `OperationResult`: A result object containing file content as data, success status, request ID, and error message if any.


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


Writes content to a file.


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


Reads a large file in chunks to handle size limitations of the underlying API.
