# Wuying AgentBay SDK

Wuying AgentBay SDK provides APIs for Python, TypeScript, and Golang to interact with the Wuying AgentBay cloud runtime environment. This environment enables running commands, executing code, and manipulating files.

## Features

- **Session Management**: Create, retrieve, list, and delete sessions
- **File Management**:
  - Basic file operations (read, write, edit)
  - Large file support with automatic chunking
  - Multi-file operations
- **Command Execution**: Run commands and execute code
- **Application Management**: List, start, and stop applications
- **Window Management**: List, activate, and manipulate windows
- **Label Management**: Categorize and filter sessions using labels
- **Context Management**: Work with persistent storage contexts
- **Port Forwarding**: Forward ports between local and remote environments
- **Process Management**: Monitor and control processes
- **OSS Integration**: Work with Object Storage Service for cloud storage
- **Mobile Tools Support**: Use mobile-specific APIs and tools
- **CodeSpace Compatibility**: Work seamlessly with CodeSpace environments

## Installation

### Python

```bash
pip install wuying-agentbay-sdk
```

### TypeScript

```bash
npm install wuying-agentbay-sdk
```

### Golang

```bash
go get github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay
```

## Usage

### Python

```python
from agentbay import AgentBay
from agentbay.session_params import CreateSessionParams

# Initialize with API key
agent_bay = AgentBay(api_key="your_api_key")

# Create a session
params = CreateSessionParams(image_id="linux_latest")
session_result = agent_bay.create(params)
session = session_result.session
print(f"Session created with ID: {session.session_id}")

# Execute a command
result = session.command.execute_command("ls -la")
if result.success:
    print(f"Command output: {result.output}")

# Read a file
result = session.file_system.read_file("/path/to/file.txt")
if result.success:
    print(f"File content: {result.content}")

# Read/write large files
large_content = "x" * (100 * 1024)  # 100KB content
write_result = session.file_system.write_large_file("/path/to/large_file.txt", large_content)
read_result = session.file_system.read_large_file("/path/to/large_file.txt")
retrieved_content = read_result.content if read_result.success else None

# Work with OSS
upload_result = session.oss.upload_file("/local/path/file.txt", "bucket-name", "remote/path/file.txt")
download_result = session.oss.download_file("bucket-name", "remote/path/file.txt", "/local/path/downloaded.txt")

# Session labels
session.set_labels({"project": "demo", "environment": "testing"})
labels_result = session.get_labels()
all_labels = labels_result.data

# Delete the session when done
delete_result = agent_bay.delete(session)
```

### TypeScript

```typescript
import { AgentBay } from 'wuying-agentbay-sdk';

// Initialize with API key
const agentBay = new AgentBay({ apiKey: 'your_api_key' });

// Create a session
async function main() {
  const session = await agentBay.create({ imageId: 'linux_latest' });

  // Execute a command
  const result = await session.command.executeCommand('ls -la');
  log(result);

  // Read a file
  const content = await session.filesystem.readFile('/path/to/file.txt');
  log(content);

  // Execute code
  const codeResult = await session.command.runCode('console.log("Hello, World!");', 'javascript');
  log(`Code execution result: ${codeResult}`);

  // Work with large files
  const largeContent = 'x'.repeat(100 * 1024); // 100KB
  await session.filesystem.writeLargeFile('/path/to/large_file.txt', largeContent);

  // Delete the session when done
  await agentBay.delete(session);
}

main().catch(logError);
```

### Golang

```go
package main

import (
	"fmt"
	"os"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

func main() {
  // Initialize with API key
  client, err := agentbay.NewAgentBay("your_api_key")
  if err != nil {
    fmt.Printf("Error initializing AgentBay client: %v\n", err)
    os.Exit(1)
  }

  // Create a session with default parameters
  result, err := client.Create(nil)
  if err != nil {
    fmt.Printf("Error creating session: %v\n", err)
    os.Exit(1)
  }

  // Access the session and RequestID
  session := result.Session
  fmt.Printf("Session created with ID: %s (RequestID: %s)\n",
    session.SessionID, result.RequestID)

  // Execute a command
  cmdResult, err := session.Command.ExecuteCommand("ls -la")
  if err != nil {
    fmt.Printf("Error executing command: %v\n", err)
    os.Exit(1)
  }
  fmt.Printf("Command result: %s (RequestID: %s)\n",
    cmdResult.Output, cmdResult.RequestID)

  // Read a file
  fileResult, err := session.FileSystem.ReadFile("/path/to/file.txt")
  if err != nil {
    fmt.Printf("Error reading file: %v\n", err)
    os.Exit(1)
  }
  fmt.Printf("File content: %s (RequestID: %s)\n",
    fileResult.Content, fileResult.RequestID)

  // Delete the session when done
  deleteResult, err := client.Delete(session)
  if err != nil {
    fmt.Printf("Error deleting session: %v\n", err)
    os.Exit(1)
  }
  fmt.Printf("Session deleted successfully (RequestID: %s)\n", deleteResult.RequestID)
}
```

## Authentication

Authentication is done using an API key, which can be provided in several ways:

1. As a parameter when initializing the SDK
2. Through environment variables (`AGENTBAY_API_KEY`)

## RequestID Standardization

The SDK provides standardized RequestID in all API responses, which can be used for:

- Debugging API calls
- Correlating client requests with server-side logs
- Tracking request history
- Providing better support through detailed logging

### Golang

All API responses include a RequestID field embedded from the base `ApiResponse` type. This makes it easy to trace and debug operations throughout the SDK.

```go
// Example showing RequestID usage
result, err := client.Create(nil)
if err != nil {
  // Handle error
}
fmt.Printf("Operation completed with RequestID: %s\n", result.RequestID)
```

## What's New

For details on the latest features and improvements, please see the [Changelog](CHANGELOG.md).

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Documentation

For more detailed documentation, examples, and advanced usage, please refer to the [docs](docs/) directory.

## Development

### CI/CD Workflows

This project uses GitHub Actions for continuous integration and testing. For information about the available workflows and how to configure them, see [GitHub Workflows](.github/WORKFLOWS.md).
