# AgentBay SDK for Golang

> Execute commands, manipulate files, and run code in cloud environments

## 📦 Installation

```bash
go get github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay
```

## 🚀 Prerequisites

Before using the SDK, you need to:

1. Register an Alibaba Cloud account: [https://aliyun.com](https://aliyun.com)
2. Get API credentials: [AgentBay Console](https://agentbay.console.aliyun.com/service-management)
3. Set environment variable: `export AGENTBAY_API_KEY=your_api_key`

## 🚀 Quick Start
```go
package main

import (
    "fmt"
    "github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

func main() {
    // Create session
    client, err := agentbay.NewAgentBay("", nil)
    if err != nil {
        fmt.Printf("Initialization failed: %v\n", err)
        return
    }
    
    result, err := client.Create(nil)
    if err != nil {
        fmt.Printf("Session creation failed: %v\n", err)
        return
    }
    
    session := result.Session
    
    // Execute command
    cmdResult, err := session.Command.ExecuteCommand("ls -la")
    if err == nil {
        fmt.Printf("Command output: %s\n", cmdResult.Output)
    }
    
    // File operations
    session.FileSystem.WriteFile("/tmp/test.txt", []byte("Hello World"))
    fileResult, err := session.FileSystem.ReadFile("/tmp/test.txt")
    if err == nil {
        fmt.Printf("File content: %s\n", string(fileResult.Data))
    }
}
```

## 📖 Complete Documentation

### 🆕 New Users
- [📚 Quick Start Tutorial](https://github.com/aliyun/wuying-agentbay-sdk/tree/main/docs/quickstart) - Get started in 5 minutes
- [🎯 Core Concepts](https://github.com/aliyun/wuying-agentbay-sdk/tree/main/docs/quickstart/basic-concepts.md) - Understanding cloud environments and sessions
- [💡 Best Practices](https://github.com/aliyun/wuying-agentbay-sdk/tree/main/docs/quickstart/best-practices.md) - Common patterns and techniques

### 🚀 Experienced Users
- [📖 Feature Guides](https://github.com/aliyun/wuying-agentbay-sdk/tree/main/docs/guides) - Complete feature introduction
- [🔧 Golang API Reference](docs/api/) - Detailed API documentation
- [💻 Golang Examples](docs/examples/) - Complete example code

### 🆘 Need Help
- [❓ FAQ](https://github.com/aliyun/wuying-agentbay-sdk/tree/main/docs/quickstart/faq.md) - Quick answers
- [🔧 Troubleshooting](https://github.com/aliyun/wuying-agentbay-sdk/tree/main/docs/quickstart/troubleshooting.md) - Problem diagnosis

## 🔧 Core Features Quick Reference

### Session Management
```go
// Create session
result, _ := client.Create(nil)
session := result.Session

// List sessions
sessions, _ := client.List()

// Connect to existing session
session, _ := client.Connect("session_id")
```

### File Operations
```go
// Read and write files
session.FileSystem.WriteFile("/path/file.txt", []byte("content"))
result, _ := session.FileSystem.ReadFile("/path/file.txt")
content := string(result.Data)

// List directory
files, _ := session.FileSystem.ListDirectory("/path")
```

### Command Execution
```go
// Execute command
result, _ := session.Command.ExecuteCommand("go run script.go")
fmt.Println(result.Output)
```

### Data Persistence
```go
// Create context
contextResult, _ := client.Context.Get("my-project", true)
context := contextResult.Context

// Create session with context
policy := agentbay.NewSyncPolicy()
contextSync := agentbay.NewContextSync(context.ID, "/tmp/data", policy)
params := agentbay.NewCreateSessionParams().AddContextSyncConfig(contextSync)
sessionResult, _ := client.Create(params)
```

## 🆘 Get Help

- [GitHub Issues](https://github.com/aliyun/wuying-agentbay-sdk/issues)
- [Complete Documentation](https://github.com/aliyun/wuying-agentbay-sdk/tree/main/docs)

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](../LICENSE) file for details.