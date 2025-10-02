# Basic Features

Basic features provide the fundamental capabilities you need to get started with AgentBay SDK. These features are essential for most use cases and available across all AgentBay environments.

## 📚 Documentation

- [Session Management](session-management.md) - Create, connect, and manage cloud sessions
- [Command Execution](command-execution.md) - Execute shell commands and scripts in sessions
- [File Operations](file-operations.md) - Upload, download, and manipulate files
- [Data Persistence](data-persistence.md) - Persistent data storage across sessions
- [UI Automation](ui-automation.md) - User interface interaction and automation

## 🎯 What are Basic Features?

Basic features provide the core building blocks for working with AgentBay:

### 🔧 Session Management
Manage the lifecycle of cloud sessions:
- Create and configure sessions
- Connect to existing sessions
- Monitor session status
- Clean up resources

### 💻 Command Execution
Execute commands in cloud environments:
- Run shell commands
- Stream output in real-time
- Handle command errors
- Control execution timeout

### 📁 File Operations
Handle files in cloud environments:
- Upload and download files
- Read and write file content
- Directory operations
- File system navigation

### 💾 Data Persistence
Persist data across sessions:
- Context-based storage
- Cross-session data sharing
- Sync policies and strategies
- Data synchronization

### 🖱️ UI Automation
Programmatic UI control:
- Mouse and keyboard simulation
- Screen capture and screenshots
- Element detection
- Click and input operations

## 🚀 Quick Start

```python
from agentbay import AgentBay
from agentbay.session_params import CreateSessionParams

# Initialize SDK
agent_bay = AgentBay(api_key="your-api-key")

# Create session
result = agent_bay.create()
if result.success:
    session = result.session
    
    # Execute command
    cmd_result = session.command.execute_command("echo 'Hello World'")
    print(cmd_result.output)
    
    # File operations
    session.file_system.write_file("/tmp/test.txt", "Hello World")
    content = session.file_system.read_file("/tmp/test.txt")
    
    # Clean up
    agent_bay.delete(session)
```

## 📖 Next Steps

After mastering the basic features, you can explore:

- [Advanced Features](../advanced/README.md) - VPC sessions, session link access, and agent modules
- [Configuration Guide](../configuration/sdk-configuration.md) - SDK configuration options
- [Use Cases](../../use-cases/README.md) - Real-world implementation examples

## 🆘 Getting Help

- [GitHub Issues](https://github.com/aliyun/wuying-agentbay-sdk/issues)
- [API Reference](../../api-reference.md)
- [Main Documentation](../../README.md)
