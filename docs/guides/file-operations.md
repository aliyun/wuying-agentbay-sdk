# Complete Guide to File Operations

This guide provides a complete introduction to file operations in the AgentBay SDK, including basic file operations, directory management, batch operations, permission management, and performance optimization.

## 📋 Table of Contents

- [Basic Concepts](#basic-concepts)
- [API Quick Reference](#api-quick-reference)
- [Basic File Operations](#basic-file-operations)
- [Directory Management](#directory-management)
- [Batch Operations](#batch-operations)
- [File Editing Operations](#file-editing-operations)
- [File Permissions and Attributes](#file-permissions-and-attributes)
- [Large File Handling](#large-file-handling)
- [Advanced Usage Examples](#advanced-usage-examples)
- [Performance Optimization](#performance-optimization)
- [Error Handling](#error-handling)
- [Best Practices](#best-practices)

<a id="basic-concepts"></a>
## 🎯 Basic Concepts

### File System Structure

AgentBay sessions provide complete file system access, supporting different operating systems:

#### Linux Environment (Default)
```
/
├── tmp/          # Temporary files (recommended for testing)
├── home/         # User directory
├── mnt/          # Mount points (for context synchronization)
├── etc/          # System configuration
├── var/          # Variable data
└── usr/          # User programs
```

#### Windows Environment
```
C:\
├── temp\         # Temporary files
├── Users\        # User directory
├── Program Files\ # Program files
└── Windows\      # System files
```

### Path Conventions

- **Linux/Android**: Use forward slash `/tmp/file.txt`
- **Windows**: Use backslash `C:\temp\file.txt` or forward slash `C:/temp/file.txt`
- **Recommendation**: Prefer absolute paths to avoid ambiguity

<a id="api-quick-reference"></a>
## 🚀 API Quick Reference

### Python
```python
# Create session
session = agent_bay.create().session
 #Create Directory
session.file_system.create_directory("/path/to")
print("✅ Directory created successfully")


# Write file
result = session.file_system.write_file("/path/to/file.txt", "content")
if result.success:
    print("File written successfully")
# Read file
result = session.file_system.read_file("/path/to/file.txt")
if result.success:
    content = result.content
    print(f"File content: {content}")

# List directory
result = session.file_system.list_directory("/path/to")
if result.success:
    entries = result.entries
    for entry in entries:
        print(f"Name: {entry['name']}")

# Get file info
result = session.file_system.get_file_info("/path/to/file.txt")

if result.success:
    info = result.file_info
    print(f"File info: {info}")
agent_bay.delete(session)
```


<a id="basic-file-operations"></a>
## 📝 Basic File Operations

**File Size Support**: Both `read_file()` and `write_file()` methods support files of any size through automatic chunked transfer. You don't need to worry about file size limitations - the SDK handles large files transparently.

### Reading Files

```python
from agentbay import AgentBay

session = agent_bay.create().session
# Write file
result = session.file_system.write_file("/tmp/file.txt", "content")
if result.success:
    print("File written successfully")
# Read text file
try:
    result = session.file_system.read_file("/tmp/file.txt")
    if result.success:
        content = result.content
        print(f"File content: {content}")
    else:
        print(f"Failed to read file: {result.error_message}")
except Exception as e:
    print(f"Exception reading file: {e}")
```


### Writing Files

```python
from agentbay import AgentBay

session = agent_bay.create().session

# Write text file
content = "Hello, AgentBay!"
result = session.file_system.write_file("/tmp/hello.txt", content)
if result.success:
    print("File written successfully")
else:
    print(f"Failed to write file: {result.error_message}")

# Append to file
result = session.file_system.write_file("/tmp/hello.txt", "New log entry\n", mode="append")
if result.success:
    print("File appended successfully")
result = session.file_system.read_file("/tmp/hello.txt")
if result.success:
    content = result.content
    print(f"File content: {content}")
agent_bay.delete(session)
```


<a id="directory-management"></a>
## 📁 Directory Management

### Creating and moving Directories

```python
from agentbay import AgentBay

agent_bay = self.common_code()
session = agent_bay.create().session

# Create directory
result = session.file_system.create_directory("/tmp/data/my_project")
if result.success:
    print("Directory created successfully")
else:
    print(f"Failed to create directory: {result.error_message}")

# Remove directory with parent directories
result = session.file_system.move_file("/tmp/data", "/tmp/test/")
if result.success:
    print("Directory moved successfully")
#List direction
result = session.file_system.list_directory("/tmp/")
if result.success:
    entries = result.entries
    for entry in entries:
        print(f"Name: {entry['name']}")
agent_bay.delete(session)
```

### Listing Directory Contents

```python
from agentbay import AgentBay

agent_bay = AgentBay()
session = agent_bay.create().session

# List directory contents
result = session.file_system.list_directory("/tmp")
if result.success:
    entries = result.entries
    for entry in entries:
        print(f"Name: {entry['name']}")
        print(f"Is Directory: {entry['isDirectory']}")
        print("---")
else:
    print(f"Failed to list directory: {result.error_message}")
```

<a id="batch-operations"></a>
## 📦 Batch Operations

### Batch File Operations

```python
from agentbay import AgentBay

agent_bay = AgentBay()
session = agent_bay.create().session

# Batch write files
files_to_write = [
    ("/tmp/file1.txt", "Content of file 1"),
    ("/tmp/file2.txt", "Content of file 2"),
    ("/tmp/file3.txt", "Content of file 3")
]

results = []
for file_path, content in files_to_write:
    result = session.file_system.write_file(file_path, content)
    results.append((file_path, result))

# Check results
for file_path, result in results:
    if result.success:
        print(f"✅ {file_path} written successfully")
    else:
        print(f"❌ {file_path} failed: {result.error_message}")

# Batch read files using read_multiple_files
files_to_read = ["/tmp/file1.txt", "/tmp/file2.txt", "/tmp/file3.txt"]
result = session.file_system.read_multiple_files(files_to_read)

if result.success:
    for file_path, content in result.contents.items():
        print(f"✅ {file_path}: {content[:50]}...")  # First 50 chars
else:
    print(f"❌ Failed to read multiple files: {result.error_message}")
```

### File Search Operations

```python
from agentbay import AgentBay

session = agent_bay.create().session

# Search for files with pattern (partial name matching, NOT wildcards)
result = session.file_system.search_files("/tmp", "systemd")
if result.success:
    print(f"Found {len(result.matches)} files containing 'test':")
    for match in result.matches:
        print(f"  - {match}")
else:
    print(f"Search failed: {result.error_message}")

# Search with exclusion patterns
result = session.file_system.search_files(
    "/tmp",
    "systemd",
    exclude_patterns=["geoclue"]
)
if result.success:
    print(f"Found {len(result.matches)} files containing 'config' (excluding 'backup' and 'temp'):")
    for match in result.matches:
        print(f"  - {match}")
```

#### ⚠️ Important: Search Rules and Limitations

**Pattern Matching Rules:**
- **NOT wildcard-based**: Patterns like `*.txt` or `test*` are NOT supported
- **Partial name matching**: The pattern matches any part of the file/directory name
- **Recursive search**: Searches through all subdirectories from the starting path
- **Case sensitivity**:
  - **Windows**: Case-insensitive matching
  - **Linux/Unix**: Case-sensitive matching

**Examples of Pattern Matching:**

```python
# ✅ CORRECT: Partial name matching
session.file_system.search_files("/tmp", "test")
# Matches: test.txt, my_test_file.py, testing.log, etc.

session.file_system.search_files("/tmp", "config")
# Matches: config.json, app_config.xml, configuration.ini, etc.

# ❌ INCORRECT: Wildcard patterns (NOT supported)
session.file_system.search_files("/tmp", "*.txt")     # Won't work as expected
session.file_system.search_files("/tmp", "test*")     # Won't work as expected
session.file_system.search_files("/tmp", "?.log")     # Won't work as expected
```

**Platform-Specific Behavior:**

```python
# On Windows (case-insensitive)
result = session.file_system.search_files("/tmp", "TEST")
# Matches: TEST.txt, TEST.log, TEST.config, MyTEST.py

# On Linux/Unix (case-sensitive)
result = session.file_system.search_files("/tmp", "TEST")
# Matches only: TEST.config, MyTEST.py (exact case match)
result = session.file_system.search_files("/tmp", "test")
# Matches only: test.txt, my_test.py (exact case match)
```

**Best Practices for File Search:**

```python
from agentbay import AgentBay

agent_bay = AgentBay()
params = CreateSessionParams(image_id="linux_latest")
session = agent_bay.create(params).session

def search_files_by_extension(base_path, extension):
        """
        Search for files by extension using partial matching.
        Note: This is a workaround since wildcards are not supported.
        """
        # Search for the extension pattern
        result = session.file_system.search_files(base_path, f".{extension}")

        if result.success:
            # Filter results to ensure they actually end with the extension
            filtered_matches = [
                match for match in result.matches
                if match.lower().endswith(f".{extension.lower()}")
            ]
            return filtered_matches
        return []

def case_insensitive_search(base_path, pattern):
    """
    Perform case-insensitive search on case-sensitive systems.
    """
    # Try both lowercase and uppercase variations
    patterns = [pattern.lower(), pattern.upper(), pattern.capitalize()]
    for p in patterns:
        print(f"Searching for {p}")
    all_matches = set()

    for p in patterns:
        result = session.file_system.search_files(base_path, p)
        if result.success:
            all_matches.update(result.matches)

    return list(all_matches)

# Example usage
files = [
    ("/tmp/test.txt", "content"),
    ("/tmp/config.log", "content"),
    ("/tmp/MyConfig.py", "content")
]
results = []
for file_path, content in files:
    result =session.file_system.write_file(file_path, content)
    results.append((file_path, result))
# Check results
for file_path, result in results:
    if result.success:
        print(f"✅ {file_path} written successfully")
    else:
        print(f"❌ {file_path} failed: {result.error_message}")

txt_files = search_files_by_extension("/tmp", "txt")
print(f"Found .txt files: {txt_files}")

config_files = case_insensitive_search("/tmp", "config")
print(f"Found config files: {config_files}")
```

### File Transfer Operations

```python
session = agent_bay.create().session
# Write file
result = session.file_system.write_file("/tmp/source.txt", "content")
if result.success:
    print("File written successfully")

# Copy file (read source and write to destination)
source_result = session.file_system.read_file("/tmp/source.txt")
if source_result.success:
    result = session.file_system.write_file("/tmp/destination.txt", source_result.content)
    if result.success:
        print("File copied successfully")
    else:
        print(f"Failed to copy file: {result.error_message}")

# Move/rename file using move_file method
result = session.file_system.move_file("/tmp/destination.txt", "/tmp/new_name.txt")
if result.success:
    print("File moved successfully")
else:
    print(f"Failed to move file: {result.error_message}")
result = session.file_system.read_file("/tmp/new_name.txt")
if result.success:
    content = result.content
    print(f"File content: {content}")
agent_bay.delete(session)
```

<a id="file-editing-operations"></a>
## ✏️ File Editing Operations

### Text Find and Replace

```python
from agentbay import AgentBay

agent_bay = AgentBay()
session = agent_bay.create().session

# Create a test file
initial_content = "This is old1 text with old2 content.\nAnother line with old1 data."
result = session.file_system.write_file("/tmp/edit_test.txt", initial_content)

# Edit file with multiple find-replace operations
edits = [
    {"oldText": "old1", "newText": "new1"},
    {"oldText": "old2", "newText": "new2"}
]

result = session.file_system.edit_file("/tmp/edit_test.txt", edits, dry_run=False)
if result.success:
    print("File edited successfully")

    # Verify changes
    read_result = session.file_system.read_file("/tmp/edit_test.txt")
    if read_result.success:
        print(f"Updated content: {read_result.content}")
else:
    print(f"Edit failed: {result.error_message}")
```

### Dry Run Mode

```python
from agentbay import AgentBay

agent_bay = AgentBay()
session = agent_bay.create().session
    # Create a test file
initial_content = "This is oldText text with newText content.\nAnother line with newText data."
result = session.file_system.write_file("/tmp/test.txt", initial_content)

# Preview changes without applying them
edits = [
    {"oldText": "newText", "newText": "modified"}
]

# Use dry_run=True to preview changes
result = session.file_system.edit_file("/tmp/test.txt", edits, dry_run=True)
if result.success:
    print("Dry run completed - changes would be applied")
    result = session.file_system.read_file("/tmp/test.txt")
    if result.success:
        print(f"Preview content: {result.content}")

    # Apply changes if preview looks good
    actual_result = session.file_system.edit_file("/tmp/test.txt", edits, dry_run=False)
    if actual_result.success:
        print("Changes applied successfully")
        result = session.file_system.read_file("/tmp/test.txt")
        if result.success:
            print(f"updated content: {result.content}")
else:
    print(f"Dry run failed: {result.error_message}")
```

<a id="file-permissions-and-attributes"></a>
## 🔐 File Permissions and Attributes

### Getting File Permissions Info

```python
from agentbay import AgentBay

agent_bay = AgentBay()
session = agent_bay.create().session

# Get file info
result = session.file_system.get_file_info("/tmp/example.txt")
if result.success:
    info = result.file_info
    print(f"Size: {info.get('size', 'N/A')} bytes")
    print(f"Created: {info.get('created', 'N/A')}")
    print(f"Modified: {info.get('modified', 'N/A')}")
    print(f"Is Directory: {info.get('isDirectory', 'N/A')}")
```
<a id="large-file-handling"></a>
## 📏 Large File Handling

**Note**: Starting from the latest version, `read_file()` and `write_file()` methods automatically handle large files through internal chunked transfer. For most use cases, you can simply use these methods directly without manual chunking.

The following examples show manual chunking approaches for special scenarios where you need custom chunk processing or progress tracking.

### Manual Chunked File Operations

```python
from agentbay import AgentBay
import base64

def encode_bytes_to_base64(data: bytes) -> str:
    """Encode bytes data to a base64 string."""
    return base64.b64encode(data).decode('utf-8')

def decode_base64_to_bytes(encoded_str: str) -> bytes:
    """Decode a base64 string back to bytes data."""
    return base64.b64decode(encoded_str)

def upload_large_file_manual(session, local_path, remote_path, chunk_size=1024*1024):  # 1MB chunks
    """Upload large file in chunks manually"""
    try:
        with open(local_path, 'rb') as f:
            chunk_number = 0
            first_chunk = True
            while True:
                file_content  = f.read(chunk_size)
                chunk = encode_bytes_to_base64(file_content)
                if not chunk:
                    break
                print(f"Uploading chunk {chunk}")
                # Write chunk to remote file
                mode = "overwrite" if first_chunk else "append"
                write_result = session.file_system.write_file(remote_path, chunk, mode=mode)
                if not write_result.success:
                    print(f"Failed to upload chunk {chunk_number}: {write_result.error_message}")
                    return False

                first_chunk = False
                chunk_number += 1

            print(f"Uploaded {chunk_number} chunks successfully")
            return True
    except Exception as e:
        print(f"Large file upload failed: {e}")
        return False

# Usage
agent_bay = AgentBay(api_key=api_key)
session = agent_bay.create().session
upload_large_file_manual(session, "./large_file.txt", "/tmp/large_file.txt")
agent_bay.delete(session)
```
### Progress Tracking

```python
import os
from agentbay import AgentBay

def upload_with_progress(session, local_path, remote_path):
    """Upload file with progress tracking"""
    file_size = os.path.getsize(local_path)
    chunk_size = 1024 * 1024  # 1MB chunks
    uploaded_bytes = 0

    try:
        with open(local_path, 'rb') as f:
            first_chunk = True
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break

                # Write chunk
                mode = "overwrite" if first_chunk else "append"
                write_result = session.file_system.write_file(remote_path, chunk, mode=mode)
                if not write_result.success:
                    print(f"Failed to upload chunk")
                    return False

                # Update progress
                uploaded_bytes += len(chunk)
                progress = (uploaded_bytes / file_size) * 100
                print(f"Progress: {progress:.1f}% ({uploaded_bytes}/{file_size} bytes)")

                chunk_number += 1

        # Combine chunks
        combine_cmd = f"cat {remote_path}.part* > {remote_path}"
        session.command.execute_command(combine_cmd)

        # Clean up
        cleanup_cmd = f"rm {remote_path}.part*"
        session.command.execute_command(cleanup_cmd)

        print("Upload completed successfully!")
        return True
    except Exception as e:
        print(f"Upload failed: {e}")
        return False
    # Usage
    session = agent_bay.create().session
    upload_with_progress(session, "./your_file.txt", "/tmp/your_file.txt")
```

<a id="advanced-usage-examples"></a>
## 🚀 Advanced Usage Examples

### Concurrent File Operations

```python
import concurrent.futures
from agentbay import AgentBay

agent_bay = AgentBay()
session = agent_bay.create().session

def write_file_task(index):
    """Task function for concurrent file writing"""
    file_path = f"/tmp/concurrent_{index}.txt"
    content = f"Concurrent content {index}"
    return session.file_system.write_file(file_path, content, "overwrite")

def read_file_task(file_path):
    """Task function for concurrent file reading"""
    return session.file_system.read_file(file_path)

# Concurrent write operations
print("Starting concurrent write operations...")
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    write_futures = [executor.submit(write_file_task, i) for i in range(10)]
    write_results = [future.result() for future in concurrent.futures.as_completed(write_futures)]

# Check write results
successful_writes = [r for r in write_results if r.success]
print(f"Successfully wrote {len(successful_writes)} files concurrently")

# Concurrent read operations
file_paths = [f"/tmp/concurrent_{i}.txt" for i in range(10)]
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    read_futures = [executor.submit(read_file_task, path) for path in file_paths]
    read_results = [future.result() for future in concurrent.futures.as_completed(read_futures)]

successful_reads = [r for r in read_results if r.success]
print(f"Successfully read {len(successful_reads)} files concurrently")
```

### Advanced File Search and Processing

```python
from agentbay import AgentBay
import re

agent_bay = AgentBay(api_key=api_key)
session = agent_bay.create().session

def process_files_by_pattern(base_path, pattern, processor_func):
    """Search and process files matching a pattern"""
    # Search for files
    search_result = session.file_system.search_files(base_path, pattern)
    if not search_result.success:
        print(f"Search failed: {search_result.error_message}")
        return []

    processed_files = []
    for file_path in search_result.matches:
        print(f"Processing file: {file_path}")
        # Read file content
        read_result = session.file_system.read_file(file_path)
        if read_result.success:
            # Process content
            processed_content = processor_func(read_result.content)
            processed_files.append({
                'path': file_path,
                'original_content': read_result.content,
                'processed_content': processed_content
            })

    return processed_files

# Example processor: count lines and words
def analyze_text(content):
    lines = content.split('\n')
    words = content.split()
    return {
        'line_count': len(lines),
        'word_count': len(words),
        'char_count': len(content)
    }
# Create a test file
initial_content = "This is oldText text with newText content.\nAnother line with newText data."
result = session.file_system.write_file("/tmp/example.txt", initial_content)
if result.success:
    print("Test file created successfully")
# Process all txt files in /tmp
results = process_files_by_pattern("/tmp", "txt", analyze_text)
for result in results:
    print(f"File: {result['path']}")
    print(f"Original content: {result['original_content']}")
    print(f"  Lines: {result['processed_content']['line_count']}")
    print(f"  Words: {result['processed_content']['word_count']}")
    print(f"  Characters: {result['processed_content']['char_count']}")
agent_bay.delete(session)
```

### Batch File Processing with Error Recovery

```python
from agentbay import AgentBay
import time

agent_bay = AgentBay(api_key=api_key)
session = agent_bay.create().session

def batch_process_with_retry(file_operations, max_retries=3):
    """Process multiple file operations with retry logic"""
    results = []

    for operation in file_operations:
        operation_type = operation['type']
        operation_args = operation['args']

        for attempt in range(max_retries):
            try:
                if operation_type == 'write':
                    result = session.file_system.write_file(**operation_args)
                elif operation_type == 'read':
                    result = session.file_system.read_file(**operation_args)
                elif operation_type == 'move':
                    result = session.file_system.move_file(**operation_args)
                elif operation_type == 'edit':
                    result = session.file_system.edit_file(**operation_args)
                else:
                    result = type('Result', (), {'success': False, 'error_message': f'Unknown operation: {operation_type}'})()

                if result.success:
                    results.append({
                        'operation': operation,
                        'result': result,
                        'attempts': attempt + 1,
                        'success': True
                    })
                    break
                else:
                    if attempt < max_retries - 1:
                        wait_time = 2 ** attempt  # Exponential backoff
                        print(f"Operation failed (attempt {attempt + 1}), retrying in {wait_time}s...")
                        time.sleep(wait_time)
                    else:
                        results.append({
                            'operation': operation,
                            'result': result,
                            'attempts': attempt + 1,
                            'success': False
                        })

            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"Exception occurred (attempt {attempt + 1}): {e}")
                    time.sleep(1)
                else:
                    results.append({
                        'operation': operation,
                        'result': type('Result', (), {'success': False, 'error_message': str(e)})(),
                        'attempts': attempt + 1,
                        'success': False
                    })

    return results

# Example batch operations
operations = [
    {
        'type': 'write',
        'args': {'path': '/tmp/batch1.txt', 'content': 'Content 1', 'mode': 'overwrite'}
    },
    {
        'type': 'write',
        'args': {'path': '/tmp/batch2.txt', 'content': 'Content 2', 'mode': 'overwrite'}
    },
    {
        'type': 'edit',
        'args': {'path': '/tmp/batch1.txt', 'edits': [{'oldText': 'Content 1', 'newText': 'Modified Content 1'}], 'dry_run': False}
    },
    {
        'type': 'move',
        'args': {'source': '/tmp/batch2.txt', 'destination': '/tmp/batch2_moved.txt'}
    }
]

# Execute batch operations
batch_results = batch_process_with_retry(operations)

# Report results
successful_ops = [r for r in batch_results if r['success']]
failed_ops = [r for r in batch_results if not r['success']]

print(f"Batch processing completed:")
print(f"  Successful operations: {len(successful_ops)}")
print(f"  Failed operations: {len(failed_ops)}")

for failed_op in failed_ops:
    print(f"  Failed: {failed_op['operation']['type']} - {failed_op['result'].error_message}")
agent_bay.delete(session)
```

### File Content Validation and Processing

```python
from agentbay import AgentBay
import json

agent_bay = AgentBay()
session = agent_bay.create().session

def validate_and_process_files(file_configs):
    """Validate file content and process based on type"""
    results = []

    for config in file_configs:
        file_path = config['path']
        expected_type = config['type']

        # Read file
        read_result = session.file_system.read_file(file_path)
        if not read_result.success:
            results.append({
                'path': file_path,
                'valid': False,
                'error': f"Failed to read file: {read_result.error_message}"
            })
            continue

        content = read_result.content
        validation_result = {'path': file_path, 'valid': True, 'processed_data': None}

        try:
            if expected_type == 'json':
                # Validate and parse JSON
                data = json.loads(content)
                validation_result['processed_data'] = data
                validation_result['type'] = 'json'

            elif expected_type == 'csv':
                # Basic CSV validation
                lines = content.strip().split('\n')
                if len(lines) > 0:
                    headers = lines[0].split(',')
                    rows = [line.split(',') for line in lines[1:]]
                    validation_result['processed_data'] = {
                        'headers': headers,
                        'row_count': len(rows),
                        'column_count': len(headers)
                    }
                    validation_result['type'] = 'csv'

            elif expected_type == 'text':
                # Text file analysis
                lines = content.split('\n')
                words = content.split()
                validation_result['processed_data'] = {
                    'line_count': len(lines),
                    'word_count': len(words),
                    'char_count': len(content),
                    'empty_lines': len([line for line in lines if not line.strip()])
                }
                validation_result['type'] = 'text'

        except Exception as e:
            validation_result['valid'] = False
            validation_result['error'] = f"Validation failed: {str(e)}"

        results.append(validation_result)

    return results

# Example usage
file_configs = [
    {'path': '/tmp/data.json', 'type': 'json'},
    {'path': '/tmp/report.csv', 'type': 'csv'},
    {'path': '/tmp/readme.txt', 'type': 'text'}
]

# Create test files first
session.file_system.write_file('/tmp/data.json', '{"name": "test", "value": 123}')
session.file_system.write_file('/tmp/report.csv', 'name,age,city\nJohn,25,NYC\nJane,30,LA')
session.file_system.write_file('/tmp/readme.txt', 'This is a test file.\nIt has multiple lines.\n\nAnd some empty lines.')

# Validate and process
validation_results = validate_and_process_files(file_configs)

for result in validation_results:
    print(f"File: {result['path']}")
    if result['valid']:
        print(f"  ✅ Valid {result['type']} file")
        if result['processed_data']:
            print(f"  Data: {result['processed_data']}")
    else:
        print(f"  ❌ Invalid: {result['error']}")
agent_bay.delete(session)
```

<a id="performance-optimization"></a>
## ⚡ Performance Optimization

### Connection Reuse

```python
from agentbay import AgentBay

class FileManager:
    def __init__(self):
        self.agent_bay = AgentBay()
        self.session = None

    def get_session(self):
        if not self.session:
            result = self.agent_bay.create()
            if result.success:
                self.session = result.session
        return self.session

    def read_file(self, file_path):
        session = self.get_session()
        return session.file_system.read_file(file_path)

    def write_file(self, file_path, content):
        session = self.get_session()
        return session.file_system.write_file(file_path, content)

    def close(self):
        if self.session:
            self.agent_bay.delete(self.session)

# Usage
file_manager = FileManager()
result = file_manager.read_file("/tmp/example.txt")
if result.success:
    content = result.content
file_manager.write_file("/tmp/output.txt", "Hello World")
file_manager.close()
```

<a id="error-handling"></a>
## ❌ Error Handling

### Common Error Types

1. **FileNotFound**: File or directory doesn't exist
2. **PermissionDenied**: Insufficient permissions
3. **DiskFull**: Insufficient disk space
4. **Timeout**: Operation timed out
5. **NetworkError**: Network connectivity issues

### Robust Error Handling

```python
from agentbay import AgentBay
import time

def robust_file_operation(session, file_path, max_retries=3):
    """Perform file operation with retry logic"""
    for attempt in range(max_retries):
        try:
            result = session.file_system.read_file(file_path)
            if result.success:
                return result.content
            else:
                print(f"Attempt {attempt + 1} failed: {result.error_message}")

                # Specific error handling
                if "not found" in str(result.error_message).lower():
                    print("File not found, cannot retry")
                    break
                elif "permission" in str(result.error_message).lower():
                    print("Permission denied, check access rights")
                    break

                # Retry for transient errors
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt  # Exponential backoff
                    print(f"Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)

        except Exception as e:
            print(f"Exception on attempt {attempt + 1}: {e}")
            if attempt < max_retries - 1:
                time.sleep(1)

    return None

# Usage
agent_bay = AgentBay()
session = agent_bay.create().session
content = robust_file_operation(session, "/tmp/example.txt")
```

<a id="best-practices"></a>
## 🏆 Best Practices

### 1. Path Management
- Always use absolute paths to avoid ambiguity
- Validate paths before operations
- Use appropriate path separators for the target OS
- Handle paths with special characters properly

### 2. Resource Management
- Always close sessions when done
- Clean up temporary files
- Monitor disk space usage
- Use connection pooling for multiple operations

### 3. Error Handling
- Implement comprehensive error handling
- Use retry logic for transient failures
- Log errors for debugging
- Validate file operations before proceeding

### 4. Performance
- Reuse sessions for multiple operations
- Use batch operations when possible (read_multiple_files)
- Implement caching for frequently accessed files
- Consider concurrent operations for independent file tasks

### 5. Security
- Validate file paths to prevent directory traversal
- Sanitize user input
- Use appropriate file permissions
- Be cautious with file editing operations

### 6. File Operations Strategy
- **Reading**: Use `read_file()` for any file size (automatic chunked transfer for large files)
- **Writing**: Use `write_file()` for any content size (automatic chunked transfer for large content)
- **Batch Reading**: Use `read_multiple_files()` instead of multiple individual reads
- **File Search**: Use `search_files()` with partial name patterns (NOT wildcards) and exclusions
- **Text Editing**: Use `edit_file()` for find-replace operations instead of read-modify-write

### 7. Advanced Usage Guidelines
- **Concurrent Operations**: Limit thread pool size to avoid overwhelming the API
- **Retry Logic**: Implement exponential backoff for failed operations
- **Content Validation**: Validate file content before processing
- **Progress Tracking**: Implement progress reporting for long-running operations

### 8. API Method Selection Guide

| Use Case | Recommended Method | Notes |
|----------|-------------------|-------|
| Read single file | `read_file()` | Supports files of any size via chunked transfer |
| Read multiple files | `read_multiple_files()` | More efficient than individual reads |
| Write file content | `write_file()` | Supports content of any size via chunked transfer |
| Find and replace text | `edit_file()` | Better than read-modify-write |
| Search for files | `search_files()` | Partial name matching, NO wildcards |
| Move/rename files | `move_file()` | Atomic operation |
| Get file metadata | `get_file_info()` | File size, type, timestamps |
| List directory | `list_directory()` | Directory contents |
| Create directories | `create_directory()` | Supports nested creation |

## 📚 Related Resources

- [Session Management Guide](session-management.md)
- [Command Execution Guide](command-execution.md)
- [Data Persistence Guide](data-persistence.md)
- [API Reference](../api-reference.md)

## 🆘 Getting Help

If you encounter issues with file operations:

1. Check file paths and permissions
2. Verify available disk space
3. Review error messages for specific details
4. Consult the [Documentation](../README.md) for detailed information
5. Search [GitHub Issues](https://github.com/aliyun/wuying-agentbay-sdk/issues) for similar problems

Remember: File operations are fundamental to most cloud workflows. Master these concepts to build robust and efficient applications! 🚀
