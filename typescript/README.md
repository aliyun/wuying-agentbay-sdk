# AgentBay SDK for TypeScript

> Execute commands, manipulate files, and run code in cloud environments

## 📦 Installation

```bash
npm install wuying-agentbay-sdk
```

## 🚀 Prerequisites

Before using the SDK, you need to:

1. Register an Alibaba Cloud account: [https://aliyun.com](https://aliyun.com)
2. Get API credentials: [AgentBay Console](https://agentbay.console.aliyun.com/service-management)
3. Set environment variable: `export AGENTBAY_API_KEY=your_api_key`

## 🚀 Quick Start
```typescript
import { AgentBay } from 'wuying-agentbay-sdk';

async function main() {
    // Create session
    const agentBay = new AgentBay();
    const result = await agentBay.create();

    if (result.success) {
        const session = result.session;

        // Execute command
        const cmdResult = await session.command.executeCommand("ls -la");
        console.log(cmdResult.output);

        // File operations
        await session.fileSystem.writeFile("/tmp/test.txt", "Hello World");
        const content = await session.fileSystem.readFile("/tmp/test.txt");
        console.log(content.data);
    }
}

main().catch(console.error);
```

## 📖 Complete Documentation

### 🆕 New Users
- [📚 Quick Start Tutorial](https://github.com/aliyun/wuying-agentbay-sdk/tree/main/docs/quickstart/README.md) - Get started in 5 minutes
- [🎯 Core Concepts](https://github.com/aliyun/wuying-agentbay-sdk/tree/main/docs/quickstart/basic-concepts.md) - Understanding cloud environments and sessions
- [💡 Best Practices](https://github.com/aliyun/wuying-agentbay-sdk/tree/main/docs/quickstart/best-practices.md) - Common patterns and techniques

### 🚀 Experienced Users
- [📖 Feature Guides](https://github.com/aliyun/wuying-agentbay-sdk/tree/main/docs/guides/README.md) - Complete feature introduction
- [🔧 TypeScript API Reference](docs/api/README.md) - Detailed API documentation
- [💻 TypeScript Examples](docs/examples/) - Complete example code

### 🆘 Need Help
- [🔧 Troubleshooting](https://github.com/aliyun/wuying-agentbay-sdk/tree/main/docs/quickstart/troubleshooting.md) - Problem diagnosis
- [🔧 TypeScript API Reference](docs/api/README.md) - Local API documentation
- [💡 TypeScript Examples](docs/examples/README.md) - Local example code

## 🔧 Core Features Quick Reference

### Session Management
```typescript
// Create session
const session = (await agentBay.create()).session;

// List sessions
const sessions = await agentBay.list();

// Connect to existing session
const session = await agentBay.connect("session_id");
```

### File Operations
```typescript
// Read and write files
await session.fileSystem.writeFile("/path/file.txt", "content");
const content = await session.fileSystem.readFile("/path/file.txt");

// List directory
const files = await session.fileSystem.listDirectory("/path");
```

### Command Execution
```typescript
// Execute command
const result = await session.command.executeCommand("node script.js");
console.log(result.output);
```

### Data Persistence
```typescript
// Create context
const context = (await agentBay.context.get("my-project", true)).context;

// Create session with context
import { ContextSync, SyncPolicy } from 'wuying-agentbay-sdk';
const contextSync = new ContextSync({
    contextId: context.id,
    path: "/tmp/data",
    policy: SyncPolicy.default()
});
const session = (await agentBay.create({ contextSync: [contextSync] })).session;
```

## 🆘 Get Help

- [GitHub Issues](https://github.com/aliyun/wuying-agentbay-sdk/issues)
- [Complete Documentation](https://github.com/aliyun/wuying-agentbay-sdk/tree/main/docs/README.md)

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](../LICENSE) file for details.
