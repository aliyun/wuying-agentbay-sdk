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
from wuying_agentbay import AgentBay

# Initialize with API key
agent_bay = AgentBay(api_key="your_api_key")

# Create a session
session = agent_bay.create()
print(f"Session created with ID: {session.session_id}")

# Execute a command
result = session.command.execute_command("ls -la")
print(f"Command result: {result}")

# Read a file
content = session.filesystem.read_file("/path/to/file.txt")
print(f"File content: {content}")

# Read/write large files
large_content = "x" * (100 * 1024)  # 100KB content
session.filesystem.write_large_file("/path/to/large_file.txt", large_content)
retrieved_content = session.filesystem.read_large_file("/path/to/large_file.txt")

# Work with OSS
session.oss.upload_file("/local/path/file.txt", "bucket-name", "remote/path/file.txt")
session.oss.download_file("bucket-name", "remote/path/file.txt", "/local/path/downloaded.txt")

# Delete the session when done
agent_bay.delete(session)
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

  // Create a session with specific image
  params := &agentbay.SessionParams{
    ImageID: "linux_latest",
  }
  session, err := client.Create(params)
  if err != nil {
    fmt.Printf("Error creating session: %v\n", err)
    os.Exit(1)
  }

  // Execute a command
  result, err := session.Command.ExecuteCommand("ls -la")
  if err != nil {
    fmt.Printf("Error executing command: %v\n", err)
    os.Exit(1)
  }
  fmt.Printf("Command result: %v\n", result)

  // Read a file
  content, err := session.FileSystem.ReadFile("/path/to/file.txt")
  if err != nil {
    fmt.Printf("Error reading file: %v\n", err)
    os.Exit(1)
  }
  fmt.Printf("File content: %s\n", content)

  // Execute code
  codeResult, err := session.Command.RunCode(`print("Hello, World!")`, "python")
  if err != nil {
    fmt.Printf("Error executing code: %v\n", err)
    os.Exit(1)
  }
  fmt.Printf("Code execution result: %s\n", codeResult)

  // Delete the session when done
  err = client.Delete(session)
  if err != nil {
    fmt.Printf("Error deleting session: %v\n", err)
    os.Exit(1)
  }
}
```

## Authentication

Authentication is done using an API key, which can be provided in several ways:

1. As a parameter when initializing the SDK
2. Through environment variables (`AGENTBAY_API_KEY`)

## What's New

For details on the latest features and improvements, please see the [Changelog](CHANGELOG.md).

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Documentation

For more detailed documentation, examples, and advanced usage, please refer to the [docs](docs/) directory.
