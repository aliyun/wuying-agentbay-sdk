# Wuying AgentBay SDK

Wuying AgentBay SDK provides APIs for Python, TypeScript, and Golang to interact with the Wuying AgentBay cloud runtime environment. This environment enables running commands, executing code, and manipulating files.

## Features

- **Session Management**: Create, retrieve, list, and delete sessions
- **File Management**: Read files in the cloud environment
- **Command Execution**: Run commands
- **ADB Operations**: Execute ADB shell commands in mobile environments (Android)
- **Application Management**: List, start, and stop applications
- **Window Management**: List, activate, and manipulate windows
- **Label Management**: Categorize and filter sessions using labels
- **Context Management**: Work with persistent storage contexts

## Installation

(Note: The following installation methods will be available in the future. Please refer to the current project documentation for setup instructions.)

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

# Execute an ADB shell command (for mobile environments)
adb_result = session.adb.shell("ls /sdcard")
print(f"ADB shell result: {adb_result}")
```

### TypeScript

```typescript
import { AgentBay } from 'wuying-agentbay-sdk';

// Initialize with API key
const agentBay = new AgentBay({ apiKey: 'your_api_key' });

// Create a session
async function main() {
  const session = await agentBay.create();
  
  // Execute a command
  const result = await session.command.executeCommand('ls -la');
  console.log(result);

  // Read a file
  const content = await session.filesystem.readFile('/path/to/file.txt');
  console.log(content);

  // Execute an ADB shell command (for mobile environments)
  const adbResult = await session.adb.shell('ls /sdcard');
  console.log(adbResult);
}

main().catch(console.error);
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
  
  // Create a session
  session, err := client.Create()
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

  // Execute an ADB shell command (for mobile environments)
  adbResult, err := session.Adb.Shell("ls /sdcard")
  if err != nil {
    fmt.Printf("Error executing ADB shell command: %v\n", err)
    os.Exit(1)
  }
  fmt.Printf("ADB shell result: %s\n", adbResult)
}
```

## Authentication

Authentication is done using an API key, which can be provided in several ways:

1. As a parameter when initializing the SDK
2. Through environment variables (`AGENTBAY_API_KEY`)

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Documentation

For more detailed documentation, examples, and advanced usage, please refer to the [docs](docs/) directory.
