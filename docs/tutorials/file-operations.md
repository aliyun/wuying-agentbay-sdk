# File Operations Tutorial

AgentBay SDK provides comprehensive file operation capabilities, allowing you to read, write, and manage files in the cloud environment. This tutorial will cover basic file operations, as well as methods for handling large files and multiple files.

## Basic File Operations

### Reading Files

The following example demonstrates how to read file contents:

```python
from agentbay import AgentBay

# Initialize the SDK and create a session
agent_bay = AgentBay(api_key="your_api_key")
session_result = agent_bay.create()
session = session_result.session

# Read a file
file_path = "/etc/hostname"
result = session.filesystem.read_file(file_path)

if result.success:
    print(f"File content:\n{result.content}")
else:
    print(f"Failed to read file: {result.error_message}")

# Delete the session when done
agent_bay.delete(session)
```

```typescript
import { AgentBay } from 'wuying-agentbay-sdk';

// Initialize the SDK
const agentBay = new AgentBay({ apiKey: 'your_api_key' });

async function readFile() {
  try {
    // Create a session
    const createResponse = await agentBay.create();
    const session = createResponse.session;
    
    // Read a file
    const filePath = '/etc/hostname';
    const result = await session.fileSystem.readFile(filePath);
    console.log(`File content:\n${result.content}`);
    
    // Delete the session
    await agentBay.delete(session);
  } catch (error) {
    console.error('Error:', error);
  }
}

readFile();
```

```go
package main

import (
	"fmt"
	"os"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

func main() {
  // Initialize the SDK
  client, err := agentbay.NewAgentBay("your_api_key")
  if err != nil {
    fmt.Printf("Error initializing AgentBay client: %v\n", err)
    os.Exit(1)
  }

  // Create a session
  result, err := client.Create(nil)
  if err != nil {
    fmt.Printf("Error creating session: %v\n", err)
    os.Exit(1)
  }

  session := result.Session

  // Read a file
  filePath := "/etc/hostname"
  fileResult, err := session.FileSystem.ReadFile(filePath)
  if err != nil {
    fmt.Printf("Error reading file: %v\n", err)
    os.Exit(1)
  }
  fmt.Printf("File content:\n%s\n", fileResult.Content)

  // Delete the session
  _, err = client.Delete(session)
  if err != nil {
    fmt.Printf("Error deleting session: %v\n", err)
    os.Exit(1)
  }
}
```

### Writing Files

Here's how to create a file and write content to it:

```python
from agentbay import AgentBay

# Initialize the SDK and create a session
agent_bay = AgentBay(api_key="your_api_key")
session_result = agent_bay.create()
session = session_result.session

# Write to a file
file_path = "/tmp/test_file.txt"
content = "This is a test file.\nIt contains multiple lines.\nThis is the third line."

result = session.filesystem.write_file(file_path, content)
if result.success:
    print(f"File written successfully: {file_path}")
else:
    print(f"Failed to write file: {result.error_message}")

# Verify the file content
read_result = session.filesystem.read_file(file_path)
if read_result.success:
    print(f"Verification of file content:\n{read_result.content}")

# Delete the session when done
agent_bay.delete(session)
```

```typescript
import { AgentBay } from 'wuying-agentbay-sdk';

// Initialize the SDK
const agentBay = new AgentBay({ apiKey: 'your_api_key' });

async function writeFile() {
  try {
    // Create a session
    const createResponse = await agentBay.create();
    const session = createResponse.session;
    
    // Write to a file
    const filePath = '/tmp/test_file.txt';
    const content = 'This is a test file.\nIt contains multiple lines.\nThis is the third line.';
    
    const writeResult = await session.fileSystem.writeFile(filePath, content);
    console.log(`File written successfully: ${filePath}`);
    
    // Verify the file content
    const readResult = await session.fileSystem.readFile(filePath);
    console.log(`Verification of file content:\n${readResult.content}`);
    
    // Delete the session
    await agentBay.delete(session);
  } catch (error) {
    console.error('Error:', error);
  }
}

writeFile();
```

### Checking if a File Exists

Before performing file operations, you might want to check if a file exists:

```python
from agentbay import AgentBay

# Initialize the SDK and create a session
agent_bay = AgentBay(api_key="your_api_key")
session_result = agent_bay.create()
session = session_result.session

# Check if a file exists
file_path = "/etc/passwd"
result = session.filesystem.exists(file_path)

if result.success and result.exists:
    print(f"File exists: {file_path}")
else:
    print(f"File does not exist: {file_path}")

# Delete the session when done
agent_bay.delete(session)
```

## Large File Handling

AgentBay SDK provides specialized methods for handling large files, automatically performing chunked transfers.

### Reading Large Files

```python
from agentbay import AgentBay

# Initialize the SDK and create a session
agent_bay = AgentBay(api_key="your_api_key")
session_result = agent_bay.create()
session = session_result.session

# Read a large file
file_path = "/var/log/syslog"  # This is typically a large file
result = session.filesystem.read_large_file(file_path)

if result.success:
    print(f"Large file read successfully, size: {len(result.content)} bytes")
    print(f"First 100 characters of the file: {result.content[:100]}...")
else:
    print(f"Failed to read large file: {result.error_message}")

# Delete the session when done
agent_bay.delete(session)
```

```typescript
import { AgentBay } from 'wuying-agentbay-sdk';

// Initialize the SDK
const agentBay = new AgentBay({ apiKey: 'your_api_key' });

async function readLargeFile() {
  try {
    // Create a session
    const createResponse = await agentBay.create();
    const session = createResponse.session;
    
    // Read a large file
    const filePath = '/var/log/syslog';  // This is typically a large file
    const result = await session.fileSystem.readLargeFile(filePath);
    
    console.log(`Large file read successfully, size: ${result.content.length} bytes`);
    console.log(`First 100 characters of the file: ${result.content.substring(0, 100)}...`);
    
    // Delete the session
    await agentBay.delete(session);
  } catch (error) {
    console.error('Error:', error);
  }
}

readLargeFile();
```

### Writing Large Files

```python
from agentbay import AgentBay
import random
import string

# Initialize the SDK and create a session
agent_bay = AgentBay(api_key="your_api_key")
session_result = agent_bay.create()
session = session_result.session

# Generate a large amount of content (approximately 1MB of random text)
content = ''.join(random.choice(string.ascii_letters) for _ in range(1024 * 1024))

# Write a large file
file_path = "/tmp/large_file.txt"
result = session.filesystem.write_large_file(file_path, content)

if result.success:
    print(f"Large file written successfully: {file_path}")
    
    # Verify the file size
    size_cmd = f"ls -l {file_path}"
    cmd_result = session.command.execute_command(size_cmd)
    if cmd_result.success:
        print(f"File size verification: {cmd_result.output}")
else:
    print(f"Failed to write large file: {result.error_message}")

# Delete the session when done
agent_bay.delete(session)
```

## Directory Operations

AgentBay SDK also supports creating, listing, and deleting directories.

### Creating Directories

```python
from agentbay import AgentBay

# Initialize the SDK and create a session
agent_bay = AgentBay(api_key="your_api_key")
session_result = agent_bay.create()
session = session_result.session

# Create a directory
dir_path = "/tmp/test_directory"
result = session.filesystem.mkdir(dir_path)

if result.success:
    print(f"Directory created: {dir_path}")
else:
    print(f"Failed to create directory: {result.error_message}")

# Delete the session when done
agent_bay.delete(session)
```

### Listing Directory Contents

```python
from agentbay import AgentBay

# Initialize the SDK and create a session
agent_bay = AgentBay(api_key="your_api_key")
session_result = agent_bay.create()
session = session_result.session

# List directory contents
dir_path = "/etc"
result = session.filesystem.list_directory(dir_path)

if result.success:
    print(f"Contents of {dir_path}:")
    for item in result.items:
        if item.is_dir:
            print(f"  Directory: {item.name}")
        else:
            print(f"  File: {item.name} ({item.size} bytes)")
else:
    print(f"Failed to list directory: {result.error_message}")

# Delete the session when done
agent_bay.delete(session)
```

## File Copying and Moving

### Copying Files

```python
from agentbay import AgentBay

# Initialize the SDK and create a session
agent_bay = AgentBay(api_key="your_api_key")
session_result = agent_bay.create()
session = session_result.session

# Create a source file
source_path = "/tmp/source_file.txt"
content = "This is the source file content"
session.filesystem.write_file(source_path, content)

# Copy the file
dest_path = "/tmp/dest_file.txt"
result = session.filesystem.copy(source_path, dest_path)

if result.success:
    print(f"File copied: {source_path} -> {dest_path}")
    
    # Verify the destination file content
    read_result = session.filesystem.read_file(dest_path)
    if read_result.success:
        print(f"Destination file content: {read_result.content}")
else:
    print(f"Failed to copy file: {result.error_message}")

# Delete the session when done
agent_bay.delete(session)
```

### Moving/Renaming Files

```python
from agentbay import AgentBay

# Initialize the SDK and create a session
agent_bay = AgentBay(api_key="your_api_key")
session_result = agent_bay.create()
session = session_result.session

# Create a source file
source_path = "/tmp/to_be_moved.txt"
content = "This file will be moved"
session.filesystem.write_file(source_path, content)

# Move/rename the file
dest_path = "/tmp/moved_file.txt"
result = session.filesystem.move(source_path, dest_path)

if result.success:
    print(f"File moved: {source_path} -> {dest_path}")
    
    # Check if the source file still exists
    exists_result = session.filesystem.exists(source_path)
    if exists_result.success:
        if exists_result.exists:
            print(f"Source file still exists: {source_path}")
        else:
            print(f"Source file no longer exists: {source_path}")
    
    # Verify the destination file content
    read_result = session.filesystem.read_file(dest_path)
    if read_result.success:
        print(f"Destination file content: {read_result.content}")
else:
    print(f"Failed to move file: {result.error_message}")

# Delete the session when done
agent_bay.delete(session)
```

## Best Practices

1. **Error Handling**: Always check the return result of file operations to ensure they completed successfully.
2. **Large File Handling**: For large files, use the specialized large file handling methods to avoid memory issues.
3. **Path Handling**: Use absolute paths to avoid confusion with relative paths.
4. **Permission Management**: Be aware of permission requirements for file operations, especially in sensitive system directories.
5. **Resource Cleanup**: After completing file operations, delete temporary files and sessions that are no longer needed.

## Related Resources

- [API Reference: FileSystem (Python)](../api-reference/python/filesystem.md)
- [API Reference: FileSystem (TypeScript)](../api-reference/typescript/filesystem.md)
- [API Reference: FileSystem (Golang)](../api-reference/golang/filesystem.md)
- [Examples: File System Operations](../examples/python/file_system) 