# Wuying AgentBay SDK

[English](README.md) | [中文](README-CN.md)

Wuying AgentBay SDK 为 Python、TypeScript 和 Golang 提供 API，用于与 Wuying AgentBay 云运行时环境进行交互。该环境支持运行命令、执行代码和操作文件。

## 功能特性

- **会话管理**：创建、检索、列出和删除会话
- **文件管理**：
  - 基本文件操作（读取、写入、编辑）
  - 大文件支持，自动分块处理
  - 多文件操作
- **命令执行**：运行命令和执行代码
- **应用管理**：列出、启动和停止应用程序
- **窗口管理**：列出、激活和操作窗口
- **标签管理**：使用标签对会话进行分类和过滤
- **上下文管理**：使用持久化存储上下文
- **端口转发**：在本地和远程环境之间转发端口
- **进程管理**：监控和控制进程
- **OSS 集成**：与对象存储服务配合使用云存储
- **移动工具支持**：使用移动端特定的 API 和工具
- **CodeSpace 兼容性**：与 CodeSpace 环境无缝协作

## 安装

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

## 使用方法

### Python

```python
from agentbay import AgentBay

# 使用 API 密钥初始化
agent_bay = AgentBay(api_key="your_api_key")

# 创建会话
session_result = agent_bay.create()
session = session_result.session

# 执行简单的 echo 命令
result = session.command.execute_command("echo 'Hello, AgentBay!'")
if result.success:
    print(f"命令输出: {result.output}")

# 完成后记得删除会话
delete_result = agent_bay.delete(session)
```

### TypeScript

```typescript
import { AgentBay } from 'wuying-agentbay-sdk';

// 使用 API 密钥初始化
const agentBay = new AgentBay({ apiKey: 'your_api_key' });

// 创建会话并运行命令
async function main() {
  try {
    // 创建会话
    const createResponse = await agentBay.create();
    const session = createResponse.session;
    
    // 执行简单的 echo 命令
    const result = await session.command.executeCommand("echo 'Hello, AgentBay!'");
    console.log(`命令输出: ${result.output}`);
    
    // 完成后删除会话
    await agentBay.delete(session);
    console.log('会话删除成功');
  } catch (error) {
    console.error('错误:', error);
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
  // 使用 API 密钥初始化
  client, err := agentbay.NewAgentBay("your_api_key")
  if err != nil {
    fmt.Printf("初始化 AgentBay 客户端时出错: %v\n", err)
    os.Exit(1)
  }

  // 创建会话
  result, err := client.Create(nil)
  if err != nil {
    fmt.Printf("创建会话时出错: %v\n", err)
    os.Exit(1)
  }

  session := result.Session

  // 执行简单的 echo 命令
  cmdResult, err := session.Command.ExecuteCommand("echo 'Hello, AgentBay!'")
  if err != nil {
    fmt.Printf("执行命令时出错: %v\n", err)
    os.Exit(1)
  }
  fmt.Printf("命令输出: %s\n", cmdResult.Output)

  // 完成后删除会话
  _, err = client.Delete(session)
  if err != nil {
    fmt.Printf("删除会话时出错: %v\n", err)
    os.Exit(1)
  }
  fmt.Println("会话删除成功")
}
```

如需更详细的示例和高级用法，请参考 [docs](docs/) 目录。

## 最新动态

有关最新功能和改进的详细信息，请参阅 [更新日志](CHANGELOG.md)。

## 许可证

本项目采用 Apache License 2.0 许可证 - 详情请参阅 [LICENSE](LICENSE) 文件。

## 文档

有关更详细的文档、示例和高级用法，请参阅 [docs](docs/) 目录。