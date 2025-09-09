# AgentBay SDK for Python

> Execute commands, operate files, and run code in cloud environments

## 📦 Installation

```bash
pip install wuying-agentbay-sdk
```

## 🚀 Prerequisites

Before using the SDK, you need to:

1. Register an Alibaba Cloud account: [https://aliyun.com](https://aliyun.com)
2. Get API credentials: [AgentBay Console](https://agentbay.console.aliyun.com/service-management)
3. Set environment variable: `export AGENTBAY_API_KEY=your_api_key`

## 🚀 Quick Start
```python
from agentbay import AgentBay

# Create session
agent_bay = AgentBay()
result = agent_bay.create()

if result.success:
    session = result.session

    # Execute command
    cmd_result = session.command.execute_command("ls -la")
    print(cmd_result.output)

    # File operations
    session.file_system.write_file("/tmp/test.txt", "Hello World")
    content = session.file_system.read_file("/tmp/test.txt")
    print(content.content)
```

## 📖 Complete Documentation

### 🆕 New Users
- [📚 Quick Start Tutorial](https://github.com/aliyun/wuying-agentbay-sdk/tree/main/docs/quickstart/README.md) - Get started in 5 minutes
- [🎯 Core Concepts](https://github.com/aliyun/wuying-agentbay-sdk/tree/main/docs/quickstart/basic-concepts.md) - Understand cloud environments and sessions
- [💡 Best Practices](https://github.com/aliyun/wuying-agentbay-sdk/tree/main/docs/quickstart/best-practices.md) - Common patterns and tips

### 🚀 Experienced Users
- [📖 Feature Guides](https://github.com/aliyun/wuying-agentbay-sdk/tree/main/docs/guides/README.md) - Complete feature introduction
- [🔧 Python API Reference](docs/api/README.md) - Detailed API documentation
- [💻 Python Examples](docs/examples/) - Complete example code

### 🆘 Need Help
- [🔧 Troubleshooting](https://github.com/aliyun/wuying-agentbay-sdk/tree/main/docs/quickstart/troubleshooting.md) - Problem diagnosis

## 🔧 Core Features Quick Reference

### Session Management
```python
# Create session
result = agent_bay.create()
if result.success:
    session = result.session

# List sessions
sessions = agent_bay.list()

# Connect to existing session
session = agent_bay.connect("session_id")
```

### File Operations
```python
# Read/write files
session.file_system.write_file("/path/file.txt", "content")
content = session.file_system.read_file("/path/file.txt")

# List directory
files = session.file_system.list_directory("/path")
```

### Command Execution
```python
# Execute command
result = session.command.execute_command("python script.py")
print(result.output)
```

### Data Persistence
```python
# Create context
context = agent_bay.context.get("my-project", create=True).context

# Create session with context
from agentbay.session_params import CreateSessionParams
from agentbay.context_sync import ContextSync, SyncPolicy
context_sync = ContextSync.new(context.id, "/tmp/data", SyncPolicy.default())
session = agent_bay.create(CreateSessionParams(context_syncs=[context_sync])).session
```

## 🆘 Get Help

- [GitHub Issues](https://github.com/aliyun/wuying-agentbay-sdk/issues)
- [Documentation](https://github.com/aliyun/wuying-agentbay-sdk/tree/main/docs/README.md)

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](../LICENSE) file for details.
