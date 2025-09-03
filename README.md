# AgentBay SDK

> The AgentBay SDK provides a comprehensive suite of tools for efficient interaction with AgentBay cloud environments, enabling you to create and manage cloud sessions, execute commands, operate files, and interact with user interfaces.

[English](README.md) | [中文](README-CN.md)

## 📦 Installation

| Language | Install Command | Documentation |
|----------|----------------|---------------|
| Python | `pip install wuying-agentbay-sdk` | [Python Docs](python/README.md) |
| TypeScript | `npm install wuying-agentbay-sdk` | [TypeScript Docs](typescript/README.md) |
| Golang | `go get github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay` | [Golang Docs](golang/README.md) |

## 🚀 Prerequisites

Before using the SDK, you need to:

1. Register an Alibaba Cloud account: [https://aliyun.com](https://aliyun.com)
2. Get APIKEY credentials: [AgentBay Console](https://agentbay.console.aliyun.com/service-management)
3. Set environment variable:
   - For Linux/MacOS:
```bash
    export AGENTBAY_API_KEY=your_api_key_here
```
   - For Windows:
```cmd
    setx AGENTBAY_API_KEY your_api_key_here
```

## 🚀 Quick Start

### Python
```python
from agentbay import AgentBay

# Create session and execute command
agent_bay = AgentBay()
session_result = agent_bay.create()
session = session_result.session
result = session.command.execute_command("echo 'Hello AgentBay'")
print(result.output)  # Hello AgentBay

# Clean up
agent_bay.delete(session)
```

### TypeScript
```typescript
import { AgentBay } from 'wuying-agentbay-sdk';

// Create session and execute command
const agentBay = new AgentBay();
const sessionResult = await agentBay.create();
const session = sessionResult.session;
const result = await session.command.executeCommand("echo 'Hello AgentBay'");
console.log(result.output);  // Hello AgentBay

// Clean up
await agentBay.delete(session);
```

### Golang
```go
import "github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"

// Create session and execute command
client, err := agentbay.NewAgentBay("", nil)
if err != nil {
    fmt.Printf("Failed to initialize AgentBay client: %v\n", err)
    return
}

sessionResult, err := client.Create(nil)
if err != nil {
    fmt.Printf("Failed to create session: %v\n", err)
    return
}

session := sessionResult.Session
result, err := session.Command.ExecuteCommand("echo 'Hello AgentBay'")
if err != nil {
    fmt.Printf("Failed to execute command: %v\n", err)
    return
}
fmt.Println(result.Output)  // Hello AgentBay

// Clean up
_, err = client.Delete(session, false)
if err != nil {
    fmt.Printf("Failed to delete session: %v\n", err)
    return
}
```

## 👋 Choose Your Learning Path

### 🆕 New Users
If you're new to AgentBay or cloud development:
- [Quick Start Tutorial](docs/quickstart/README.md) - Get started in 5 minutes
- [Core Concepts](docs/quickstart/basic-concepts.md) - Understand cloud environments and sessions

### 🚀 Experienced Users
If you're familiar with Docker, cloud services, or similar products:
- [Feature Guides](docs/guides/README.md) - Complete feature introduction
- [API Reference](docs/api-reference.md) - Core API quick lookup

## 🔧 Core Features

- **Session Management** - Create and manage cloud environments
- **Command Execution** - Execute Shell commands in the cloud
- **File Operations** - Upload, download, and edit cloud files
- **Code Execution** - Run Python, JavaScript code
- **UI Automation** - Interact with cloud application interfaces
- **Data Persistence** - Save data across sessions

## 🆘 Get Help

- [GitHub Issues](https://github.com/aliyun/wuying-agentbay-sdk/issues)
- [Complete Documentation](docs/README.md)
- [Changelog](CHANGELOG.md)

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.
