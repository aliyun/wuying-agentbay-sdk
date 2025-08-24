# AgentBay SDK for Golang

> 在云端环境中执行命令、操作文件、运行代码

## 📦 安装

```bash
go get github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay
```

## 🚀 准备工作

使用SDK前需要：

1. 注册阿里云账号：[https://aliyun.com](https://aliyun.com)
2. 获取API密钥：[AgentBay控制台](https://agentbay.console.aliyun.com/service-management)
3. 设置环境变量：`export AGENTBAY_API_KEY=your_api_key`

## 🚀 快速开始
```go
package main

import (
    "fmt"
    "github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

func main() {
    // 创建会话
    client, err := agentbay.NewAgentBay("", nil)
    if err != nil {
        fmt.Printf("初始化失败: %v\n", err)
        return
    }
    
    result, err := client.Create(nil)
    if err != nil {
        fmt.Printf("创建会话失败: %v\n", err)
        return
    }
    
    session := result.Session
    
    // 执行命令
    cmdResult, err := session.Command.ExecuteCommand("ls -la")
    if err == nil {
        fmt.Printf("命令输出: %s\n", cmdResult.Output)
    }
    
    // 操作文件
    session.FileSystem.WriteFile("/tmp/test.txt", []byte("Hello World"))
    fileResult, err := session.FileSystem.ReadFile("/tmp/test.txt")
    if err == nil {
        fmt.Printf("文件内容: %s\n", string(fileResult.Data))
    }
}
```

## 📖 完整文档

### 🆕 新手用户
- [📚 快速开始教程](https://github.com/aliyun/wuying-agentbay-sdk/tree/main/docs/quickstart) - 5分钟快速上手
- [🎯 核心概念](https://github.com/aliyun/wuying-agentbay-sdk/tree/main/docs/quickstart/basic-concepts.md) - 理解云环境和会话
- [💡 最佳实践](https://github.com/aliyun/wuying-agentbay-sdk/tree/main/docs/quickstart/best-practices.md) - 常用模式和技巧

### 🚀 有经验的用户
- [📖 功能指南](https://github.com/aliyun/wuying-agentbay-sdk/tree/main/docs/guides) - 完整功能介绍
- [🔧 Golang API参考](docs/api/) - 详细API文档
- [💻 Golang示例](docs/examples/) - 完整示例代码

### 🆘 需要帮助
- [❓ 常见问题](https://github.com/aliyun/wuying-agentbay-sdk/tree/main/docs/quickstart/faq.md) - 快速解答
- [🔧 故障排除](https://github.com/aliyun/wuying-agentbay-sdk/tree/main/docs/quickstart/troubleshooting.md) - 问题诊断

## 🔧 核心功能速查

### 会话管理
```go
// 创建会话
result, _ := client.Create(nil)
session := result.Session

// 列出会话
sessions, _ := client.List()

// 连接现有会话
session, _ := client.Connect("session_id")
```

### 文件操作
```go
// 读写文件
session.FileSystem.WriteFile("/path/file.txt", []byte("content"))
result, _ := session.FileSystem.ReadFile("/path/file.txt")
content := string(result.Data)

// 列出目录
files, _ := session.FileSystem.ListDirectory("/path")
```

### 命令执行
```go
// 执行命令
result, _ := session.Command.ExecuteCommand("go run script.go")
fmt.Println(result.Output)
```

### 数据持久化
```go
// 创建上下文
contextResult, _ := client.Context.Get("my-project", true)
context := contextResult.Context

// 带上下文创建会话
policy := agentbay.NewSyncPolicy()
contextSync := agentbay.NewContextSync(context.ID, "/mnt/data", policy)
params := agentbay.NewCreateSessionParams().AddContextSyncConfig(contextSync)
sessionResult, _ := client.Create(params)
```

## 🆘 获取帮助

- [GitHub Issues](https://github.com/aliyun/wuying-agentbay-sdk/issues)
- [完整文档](https://github.com/aliyun/wuying-agentbay-sdk/tree/main/docs)

## 📄 许可证

本项目基于 Apache License 2.0 许可证 - 查看 [LICENSE](../LICENSE) 文件了解详情。
