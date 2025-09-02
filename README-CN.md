# AgentBay SDK

> AgentBay SDK提供了一整套全面的工具，以便与AgentBay云环境进行高效交互，使您能够创建和管理云会话、执行命令、操作文件以及与用户界面进行交互。

[English](README.md) | [中文](README-CN.md)

## 📦 安装

| 语言 | 安装命令 | 文档 |
|------|----------|------|
| Python | `pip install wuying-agentbay-sdk` | [Python文档](python/README.md) |
| TypeScript | `npm install wuying-agentbay-sdk` | [TypeScript文档](typescript/README.md) |
| Golang | `go get github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay` | [Golang文档](golang/README.md) |

## 🚀 准备工作

使用SDK前需要：

1. 注册阿里云账号：[https://aliyun.com](https://aliyun.com)
2. 获取API密钥：[AgentBay控制台](https://agentbay.console.aliyun.com/service-management)
3. 设置环境变量：
   - 对于Linux/MacOS：
```bash
    export AGENTBAY_API_KEY=your_api_key_here
```
   - 对于Windows：
```cmd
    setx AGENTBAY_API_KEY your_api_key_here
```

## 🚀 快速开始

### Python
```python
from agentbay import AgentBay

# 创建会话并执行命令
agent_bay = AgentBay()
session_result = agent_bay.create()
session = session_result.session
result = session.command.execute_command("echo 'Hello AgentBay'")
print(result.output)  # Hello AgentBay

# 清理资源
agent_bay.delete(session)
```

### TypeScript
```typescript
import { AgentBay } from 'wuying-agentbay-sdk';

// 创建会话并执行命令
const agentBay = new AgentBay();
const sessionResult = await agentBay.create();
const session = sessionResult.session;
const result = await session.command.executeCommand("echo 'Hello AgentBay'");
console.log(result.output);  // Hello AgentBay

// 清理资源
await agentBay.delete(session);
```

### Golang
```go
import "github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"

// 创建会话并执行命令
client, err := agentbay.NewAgentBay("", nil)
if err != nil {
    fmt.Printf("初始化AgentBay客户端失败: %v\n", err)
    return
}

sessionResult, err := client.Create(nil)
if err != nil {
    fmt.Printf("创建会话失败: %v\n", err)
    return
}

session := sessionResult.Session
result, err := session.Command.ExecuteCommand("echo 'Hello AgentBay'")
if err != nil {
    fmt.Printf("执行命令失败: %v\n", err)
    return
}
fmt.Println(result.Output)  // Hello AgentBay

// 清理资源
_, err = client.Delete(session, false)
if err != nil {
    fmt.Printf("删除会话失败: %v\n", err)
    return
}
```

## 👋 选择你的学习路径

### 🆕 新手用户
如果你是第一次接触AgentBay或云端开发：
- [快速开始教程](docs/quickstart/README.md) - 5分钟上手
- [核心概念](docs/quickstart/basic-concepts.md) - 理解云环境和会话

### 🚀 有经验的用户  
如果你熟悉Docker、云服务或类似产品：
- [功能指南](docs/guides/README.md) - 完整功能介绍
- [API参考](docs/api-reference.md) - 核心API快速查找

## 🔧 核心功能

- **会话管理** - 创建和管理云端环境
- **命令执行** - 在云端执行Shell命令
- **文件操作** - 上传、下载、编辑云端文件
- **代码执行** - 运行Python、JavaScript代码
- **UI自动化** - 与云端应用界面交互
- **数据持久化** - 跨会话保存数据

## 🆘 获取帮助

- [GitHub Issues](https://github.com/aliyun/wuying-agentbay-sdk/issues)
- [完整文档](docs/README.md)
- [更新日志](CHANGELOG.md)

## 📄 许可证

本项目基于 Apache License 2.0 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。