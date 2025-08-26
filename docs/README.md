# AgentBay SDK Documentation

> Multi-language SDK for executing commands, operating files, and running code in cloud environments

## 📦 Installation

| Language | Install Command | Documentation |
|----------|----------------|---------------|
| Python | `pip install wuying-agentbay-sdk` | [Python Docs](../python/README.md) |
| TypeScript | `npm install wuying-agentbay-sdk` | [TypeScript Docs](../typescript/README.md) |
| Golang | `go get github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay` | [Golang Docs](../golang/README.md) |

## 🚀 Prerequisites

Before using the SDK, you need to:

1. Register an Alibaba Cloud account: [https://aliyun.com](https://aliyun.com)
2. Get API credentials: [AgentBay Console](https://agentbay.console.aliyun.com/service-management)

## 🚀 Quick Start

### Python
```python
from agentbay import AgentBay

# Create session and execute command
agent_bay = AgentBay()
session = agent_bay.create().session
result = session.command.execute_command("echo 'Hello AgentBay'")
print(result.output)  # Hello AgentBay
```

### TypeScript
```typescript
import { AgentBay } from 'wuying-agentbay-sdk';

// Create session and execute command
const agentBay = new AgentBay();
const session = (await agentBay.create()).session;
const result = await session.command.executeCommand("echo 'Hello AgentBay'");
console.log(result.output);  // Hello AgentBay
```

### Golang
```go
import "github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"

// Create session and execute command
client, _ := agentbay.NewAgentBay("", nil)
sessionResult, _ := client.Create(nil)
session := sessionResult.Session
result, _ := session.Command.ExecuteCommand("echo 'Hello AgentBay'")
fmt.Println(result.Output)  // Hello AgentBay
```

## 👋 Choose Your Learning Path

### 🆕 New Users
If you're new to AgentBay or cloud development:
- [Quick Start Tutorial](quickstart/README.md) - Get started in 5 minutes
- [Core Concepts](quickstart/basic-concepts.md) - Understand cloud environments and sessions

### 🚀 Experienced Users  
If you're familiar with Docker, cloud services, or similar products:
- [Feature Guides](guides/README.md) - Complete feature introduction
- [API Reference](api-reference.md) - Core API quick lookup

## 🔧 Core Features

- **Session Management** - Create and manage cloud environments
- **Command Execution** - Execute Shell commands in the cloud
- **File Operations** - Upload, download, and edit cloud files
- **Code Execution** - Run Python, JavaScript code
- **UI Automation** - Interact with cloud application interfaces
- **Data Persistence** - Save data across sessions

## 🆘 Get Help

- [GitHub Issues](https://github.com/aliyun/wuying-agentbay-sdk/issues)
- [Complete Documentation](README.md)
- [Changelog](../CHANGELOG.md)

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](../LICENSE) file for details.