# Wuying AgentBay SDK

[English](README.md) | [中文](README-CN.md)

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

## Preparation

Before using the SDK, you need to:

1. Register an Alibaba Cloud account at [https://aliyun.com](https://aliyun.com)
2. Register an API key at [AgentBay Console](https://agentbay.console.aliyun.com/service-management)

## Quick Start

### Python

```python
from agentbay import AgentBay
from agentbay.session_params import CreateSessionParams

# Initialize with API key
agent_bay = AgentBay(api_key="your_api_key")

# Create a session
session_param = CreateSessionParams()
session_param.image_id = "code_latest"
session_result = agent_bay.create(session_param)
session = session_result.session

# Execute a simple echo command
result = session.command.execute_command("echo 'Hello, AgentBay!'")
if result.success:
    print(f"Command output: {result.output}")

# Don't forget to delete the session when done
delete_result = agent_bay.delete(session)
```

### TypeScript

```typescript
import { AgentBay } from 'wuying-agentbay-sdk';

// Initialize with API key
const agentBay = new AgentBay({ apiKey: 'your_api_key' });

// Create a session and run a command
async function main() {
  try {
    // Create a session
    const createResponse = await agentBay.create({imageId:'code_latest'});
    const session = createResponse.session;

    // Execute a simple echo command
    const result = await session.command.executeCommand("echo 'Hello, AgentBay!'");
    console.log(`Command output: ${result.output}`);

    // Delete the session when done
    await agentBay.delete(session);
    console.log('Session deleted successfully');
  } catch (error) {
    console.error('Error:', error);
  }
}

main();
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
  params := agentbay.NewCreateSessionParams().WithImageId("code_latest")
  result, err := client.Create(params)
  if err != nil {
    fmt.Printf("Error creating session: %v\n", err)
    os.Exit(1)
  }

  session := result.Session

  // Execute a simple echo command
  cmdResult, err := session.Command.ExecuteCommand("echo 'Hello, AgentBay!'")
  if err != nil {
    fmt.Printf("Error executing command: %v\n", err)
    os.Exit(1)
  }
  fmt.Printf("Command output: %s\n", cmdResult.Output)

  // Delete the session when done
  _, err = client.Delete(session)
  if err != nil {
    fmt.Printf("Error deleting session: %v\n", err)
    os.Exit(1)
  }
  fmt.Println("Session deleted successfully")
}
```

For more detailed examples and advanced usage, please refer to the [docs](docs/) directory.

## What's New

For details on the latest features and improvements, please see the [Changelog](CHANGELOG.md).

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Documentation

For more detailed documentation, examples, and advanced usage, please refer to the [docs](docs/) directory.
