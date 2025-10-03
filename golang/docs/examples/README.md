# Golang SDK Examples

This directory contains Go examples demonstrating various features and capabilities of the Wuying AgentBay SDK.

## Quick Start

### [basic_usage/](./basic_usage)
Getting started with the AgentBay SDK:
- Initializing the AgentBay client
- Creating sessions
- Executing commands
- Reading files
- Session management

## Core Features

### [session_creation/](./session_creation)
Session creation and configuration:
- Creating sessions with different image types
- Session parameter configuration
- Session lifecycle management

### [session_params/](./session_params)
Advanced session parameters:
- Custom session configuration
- Image type selection
- Environment setup

### [command_example/](./command_example)
Command execution capabilities:
- Running shell commands in cloud environments
- Capturing command output
- Command execution patterns

### [filesystem_example/](./filesystem_example)
File system operations:
- File upload and download
- Directory operations
- File manipulation

### [watch_directory_example/](./watch_directory_example)
Directory monitoring:
- Watching directory changes
- File system events
- Change notifications

### [code_example/](./code_example)
Code execution in cloud environments:
- Running code snippets
- Development environment usage
- Code execution workflows

### [ui_example/](./ui_example)
UI automation:
- User interface interactions
- Screen automation
- UI element manipulation

## Advanced Features

### [context_management/](./context_management)
Data persistence across sessions:
- Context creation and management
- Data storage and retrieval
- Cross-session data sharing

### [context_sync_example/](./context_sync_example)
Context synchronization:
- Synchronizing data between sessions
- Context update mechanisms
- Data consistency management

### [context_sync_demo/](./context_sync_demo)
Context synchronization demonstration:
- Practical context sync examples
- Real-world usage patterns
- Context sync workflows

### [data_persistence/](./data_persistence)
Persistent data storage:
- Storing data across sessions
- Data retrieval patterns
- Persistent storage management

### [application_window/](./application_window)
Application and window management:
- Application lifecycle control
- Window operations
- Desktop automation

### [agent_module/](./agent_module)
Agent module integration:
- Using AI-powered automation
- Agent-based task execution
- Intelligent automation workflows

### [vpc_session/](./vpc_session)
VPC network configuration:
- Creating sessions in VPC environments
- Network security groups
- Private network access

### [automation/](./automation)
Automation workflows:
- End-to-end automation examples
- Complex automation patterns
- Workflow orchestration

## Running the Examples

1. Set your API key:
```bash
export AGENTBAY_API_KEY=your_api_key_here
```

2. Navigate to any example directory:
```bash
cd basic_usage
```

3. Run the example:
```bash
go run main.go
```

## Prerequisites

- Go 1.19 or later
- Valid AgentBay API key
- Internet connection

## Getting Help

For more information, see:
- [Golang SDK Documentation](../../)
- [API Reference](../api/)
- [Quick Start Guide](../../../docs/quickstart/)
