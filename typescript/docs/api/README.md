# AgentBay TypeScript SDK API Reference

Complete API reference documentation for the AgentBay TypeScript SDK.

## 📚 Core APIs

### Client & Session Management
- [**AgentBay**](agentbay.md) - Main client for creating and managing sessions
- [**Session**](session.md) - Session lifecycle and operations management
- [**Context**](context.md) - Data persistence and context management
- [**ContextManager**](context-manager.md) - Context operations and file synchronization

### Execution & Code Running
- [**Command**](command.md) - Execute shell commands in cloud environments
- [**Code**](code.md) - Run code in multiple programming languages

### File System
- [**FileSystem**](filesystem.md) - File and directory operations
- [**OSS**](oss.md) - Object Storage Service integration

### Use Case Specific APIs

#### Computer Use
- [**Computer**](computer.md) - Windows desktop environment automation
- [**UI**](ui.md) - UI automation (mouse, keyboard, screenshot)
- [**Window**](window.md) - Window management operations
- [**Application**](application.md) - Application lifecycle management

#### Mobile Use
- [**Mobile**](mobile.md) - Mobile device simulation and automation

#### Agent Integration
- [**Agent**](agent.md) - AI agent integration and MCP tools
- [**Extension**](extension.md) - Browser extension management

## 📖 API Organization

### By Feature Category

| Category | APIs | Description |
|----------|------|-------------|
| **Client** | AgentBay, Session | Session creation and management |
| **Execution** | Command, Code | Command and code execution |
| **Storage** | FileSystem, OSS, Context | File operations and data persistence |
| **Computer UI** | Computer, UI, Window, Application | Desktop automation |
| **Mobile** | Mobile | Mobile device automation |
| **Integration** | Agent, Extension | AI agent and browser extensions |

### By Use Case

| Use Case | Primary APIs | System Image |
|----------|--------------|--------------|
| **Computer Use** | Computer, UI, Window, Application | `windows_latest` |
| **Browser Automation** | Computer, UI, Extension | `browser_latest` |
| **Code Execution** | Code, Command, FileSystem | `code_latest` |
| **Mobile Automation** | Mobile | `mobile_latest` |

## 📘 Related Documentation

- [Feature Guides](../../../docs/guides/README.md) - Detailed usage guides and tutorials
- [Code Examples](../examples/README.md) - Complete example implementations
- [Quick Start](../../../docs/quickstart/README.md) - Get started in 5 minutes

---

**Need help?** Check out the [complete documentation](../../../docs/README.md) or [open an issue](https://github.com/aliyun/wuying-agentbay-sdk/issues).
