# AgentBay SDK for TypeScript

> 在云端环境中执行命令、操作文件、运行代码

## 📦 安装

```bash
npm install wuying-agentbay-sdk
```

## 🚀 准备工作

使用SDK前需要：

1. 注册阿里云账号：[https://aliyun.com](https://aliyun.com)
2. 获取API密钥：[AgentBay控制台](https://agentbay.console.aliyun.com/service-management)
3. 设置环境变量：`export AGENTBAY_API_KEY=your_api_key`

## 🚀 快速开始
```typescript
import { AgentBay } from 'wuying-agentbay-sdk';

async function main() {
    // 创建会话
    const agentBay = new AgentBay();
    const result = await agentBay.create();
    
    if (result.success) {
        const session = result.session;
        
        // 执行命令
        const cmdResult = await session.command.executeCommand("ls -la");
        console.log(cmdResult.output);
        
        // 操作文件
        await session.fileSystem.writeFile("/tmp/test.txt", "Hello World");
        const content = await session.fileSystem.readFile("/tmp/test.txt");
        console.log(content.data);
    }
}

main().catch(console.error);
```

## 📖 完整文档

### 🆕 新手用户
- [📚 快速开始教程](https://github.com/aliyun/wuying-agentbay-sdk/tree/main/docs/quickstart) - 5分钟快速上手
- [🎯 核心概念](https://github.com/aliyun/wuying-agentbay-sdk/tree/main/docs/quickstart/basic-concepts.md) - 理解云环境和会话
- [💡 最佳实践](https://github.com/aliyun/wuying-agentbay-sdk/tree/main/docs/quickstart/best-practices.md) - 常用模式和技巧

### 🚀 有经验的用户
- [📖 功能指南](https://github.com/aliyun/wuying-agentbay-sdk/tree/main/docs/guides) - 完整功能介绍
- [🔧 TypeScript API参考](docs/api/) - 详细API文档
- [💻 TypeScript示例](docs/examples/) - 完整示例代码

### 🆘 需要帮助
- [❓ 常见问题](https://github.com/aliyun/wuying-agentbay-sdk/tree/main/docs/quickstart/faq.md) - 快速解答
- [🔧 故障排除](https://github.com/aliyun/wuying-agentbay-sdk/tree/main/docs/quickstart/troubleshooting.md) - 问题诊断
- [🔧 TypeScript API参考](docs/api/README.md) - 本地API文档
- [💡 TypeScript示例](docs/examples/README.md) - 本地示例代码

## 🔧 核心功能速查

### 会话管理
```typescript
// 创建会话
const session = (await agentBay.create()).session;

// 列出会话
const sessions = await agentBay.list();

// 连接现有会话
const session = await agentBay.connect("session_id");
```

### 文件操作
```typescript
// 读写文件
await session.fileSystem.writeFile("/path/file.txt", "content");
const content = await session.fileSystem.readFile("/path/file.txt");

// 列出目录
const files = await session.fileSystem.listDirectory("/path");
```

### 命令执行
```typescript
// 执行命令
const result = await session.command.executeCommand("node script.js");
console.log(result.output);
```

### 数据持久化
```typescript
// 创建上下文
const context = (await agentBay.context.get("my-project", true)).context;

// 带上下文创建会话
import { ContextSync, SyncPolicy } from 'wuying-agentbay-sdk';
const contextSync = new ContextSync({
    contextId: context.id,
    path: "/mnt/data",
    policy: SyncPolicy.default()
});
const session = (await agentBay.create({ contextSync: [contextSync] })).session;
```

## 🆘 获取帮助

- [GitHub Issues](https://github.com/aliyun/wuying-agentbay-sdk/issues)
- [完整文档](https://github.com/aliyun/wuying-agentbay-sdk/tree/main/docs)

## 📄 许可证

本项目基于 Apache License 2.0 许可证 - 查看 [LICENSE](../LICENSE) 文件了解详情。
