# Complete Guide to File Operations

This guide provides a complete introduction to file operations in the AgentBay SDK, including basic file operations, directory management, batch operations, permission management, and performance optimization.

## 📋 Table of Contents

- [Basic Concepts](#basic-concepts)
- [API Quick Reference](#api-quick-reference)
- [Basic File Operations](#basic-file-operations)
- [Directory Management](#directory-management)
- [Batch Operations](#batch-operations)
- [File Permissions and Attributes](#file-permissions-and-attributes)
- [Large File Handling](#large-file-handling)
- [Performance Optimization](#performance-optimization)
- [Error Handling](#error-handling)
- [Best Practices](#best-practices)

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

## 🚀 API Quick Reference

### Python
```python
# Read file
content = session.file_system.read_file("/path/to/file.txt")

# Write file
session.file_system.write_file("/path/to/file.txt", "content")

# List directory
files = session.file_system.list_directory("/path/to/directory")

# Get file info
info = session.file_system.get_file_info("/path/to/file.txt")
```


## 📝 Basic File Operations

### Reading Files

```python
from agentbay import AgentBay

agent_bay = AgentBay()
session = agent_bay.create().session

# Read text file
try:
    result = session.file_system.read_file("/tmp/example.txt")
    if result.success:
        content = result.content
        print(f"File content: {content}")
    else:
        print(f"Failed to read file: {result.error_message}")
except Exception as e:
    print(f"Exception reading file: {e}")

# Read file
result = session.file_system.read_file("/tmp/example.txt")

# Read file
result = session.file_system.read_file("/tmp/image.png")
if result.success:
    binary_data = result.content
    # Process binary data
```


### Writing Files

```python
from agentbay import AgentBay

agent_bay = AgentBay()
session = agent_bay.create().session

# Write text file
content = "Hello, AgentBay!"
result = session.file_system.write_file("/tmp/hello.txt", content)
if result.success:
    print("File written successfully")
else:
    print(f"Failed to write file: {result.error_message}")

# Write file
result = session.file_system.write_file("/tmp/hello.txt", content)

# Write binary file
binary_data = b"\x89PNG\r\n\x1a\n..."  # PNG header example
result = session.file_system.write_file("/tmp/image.png", binary_data)

# Append to file
result = session.file_system.write_file("/tmp/log.txt", "New log entry\n", mode="append")
```


## 📁 Directory Management

### Creating and Removing Directories

```python
from agentbay import AgentBay

agent_bay = AgentBay()
session = agent_bay.create().session

# Create directory
result = session.file_system.create_directory("/tmp/my_project")
if result.success:
    print("Directory created successfully")
else:
    print(f"Failed to create directory: {result.error_message}")

# Create directory with parent directories
result = session.file_system.create_directory("/tmp/parent/child/grandchild")
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

# Batch read files
files_to_read = ["/tmp/file1.txt", "/tmp/file2.txt", "/tmp/file3.txt"]
read_results = []
for file_path in files_to_read:
    result = session.file_system.read_file(file_path)
    read_results.append((file_path, result))

# Process read results
for file_path, result in read_results:
    if result.success:
        print(f"✅ {file_path}: {result.content[:50]}...")  # First 50 chars
    else:
        print(f"❌ {file_path} failed: {result.error_message}")
```

### File Transfer Operations

```python
from agentbay import AgentBay

agent_bay = AgentBay()
session = agent_bay.create().session

# Copy file
result = session.file_system.write_file("/tmp/destination.txt", "content from source file")
if result.success:
    print("File copied successfully")
else:
    print(f"Failed to copy file: {result.error_message}")

# Move/rename file
result = session.file_system.write_file("/tmp/new_name.txt", "content from old file")
```

## 🔐 File Permissions and Attributes

### Managing File Permissions

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

## 📏 Large File Handling

### Chunked File Operations

```python
from agentbay import AgentBay

def upload_large_file(session, local_path, remote_path, chunk_size=1024*1024):  # 1MB chunks
    """Upload large file in chunks"""
    try:
        with open(local_path, 'rb') as f:
            chunk_number = 0
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                
                # Write chunk to remote file
                chunk_path = f"{remote_path}.part{chunk_number}"
                write_result = session.file_system.write_file(chunk_path, chunk)
                if not write_result.success:
                    print(f"Failed to upload chunk {chunk_number}: {write_result.error_message}")
                    return False
                
                chunk_number += 1
            
            # Combine chunks (this would require a command execution)
            combine_cmd = f"cat {remote_path}.part* > {remote_path}"
            cmd_result = session.command.execute(combine_cmd)
            if not cmd_result.success:
                print(f"Failed to combine chunks: {cmd_result.error_message}")
                return False
            
            # Clean up chunk files
            cleanup_cmd = f"rm {remote_path}.part*"
            session.command.execute(cleanup_cmd)
            
            print(f"Uploaded {chunk_number} chunks successfully")
            return True
    except Exception as e:
        print(f"Large file upload failed: {e}")
        return False

# Usage
agent_bay = AgentBay()
session = agent_bay.create().session
upload_large_file(session, "/local/large_file.zip", "/tmp/large_file.zip")
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
            chunk_number = 0
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                
                # Write chunk
                chunk_path = f"{remote_path}.part{chunk_number}"
                write_result = session.file_system.write_file(chunk_path, chunk)
                if not write_result.success:
                    print(f"Failed to upload chunk {chunk_number}")
                    return False
                
                # Update progress
                uploaded_bytes += len(chunk)
                progress = (uploaded_bytes / file_size) * 100
                print(f"Progress: {progress:.1f}% ({uploaded_bytes}/{file_size} bytes)")
                
                chunk_number += 1
        
        # Combine chunks
        combine_cmd = f"cat {remote_path}.part* > {remote_path}"
        session.command.execute(combine_cmd)
        
        # Clean up
        cleanup_cmd = f"rm {remote_path}.part*"
        session.command.execute(cleanup_cmd)
        
        print("Upload completed successfully!")
        return True
    except Exception as e:
        print(f"Upload failed: {e}")
        return False
```

## ⚡ Performance Optimization

### Caching Strategies

```python
import time
from agentbay import AgentBay

class FileCache:
    def __init__(self, session, cache_timeout=300):  # 5 minutes
        self.session = session
        self.cache = {}
        self.cache_timeout = cache_timeout
    
    def read_file(self, file_path):
        # Check if file is cached and not expired
        if file_path in self.cache:
            cached_data, timestamp = self.cache[file_path]
            if time.time() - timestamp < self.cache_timeout:
                print(f"Cache hit for {file_path}")
                return cached_data
        
        # Read from remote and cache
        print(f"Cache miss for {file_path}, reading from remote")
        result = self.session.file_system.read_file(file_path)
        if result.success:
            self.cache[file_path] = (result.content, time.time())
            return result.content
        else:
            return None

# Usage
agent_bay = AgentBay()
session = agent_bay.create().session
file_cache = FileCache(session)

# First read - cache miss
content1 = file_cache.read_file("/tmp/example.txt")

# Second read - cache hit (if within 5 minutes)
content2 = file_cache.read_file("/tmp/example.txt")
```

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
content = file_manager.read_file("/tmp/example.txt")
file_manager.write_file("/tmp/output.txt", "Hello World")
file_manager.close()
```

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

## 🏆 Best Practices

### 1. Path Management
- Always use absolute paths to avoid ambiguity
- Validate paths before operations
- Use appropriate path separators for the target OS

### 2. Resource Management
- Always close sessions when done
- Clean up temporary files
- Monitor disk space usage

### 3. Error Handling
- Implement comprehensive error handling
- Use retry logic for transient failures
- Log errors for debugging

### 4. Performance
- Reuse sessions for multiple operations
- Use batch operations when possible
- Implement caching for frequently accessed files

### 5. Security
- Validate file paths to prevent directory traversal
- Sanitize user input
- Use appropriate file permissions

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