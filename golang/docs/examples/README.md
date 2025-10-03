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

## Common Features

Examples available across all environment types.

### Basics

**[session_creation/](./session_creation)**
- Creating sessions with different image types
- Session parameter configuration
- Session lifecycle management

**[session_params/](./session_params)**
- Custom session configuration
- Image type selection
- Environment setup

**[command_example/](./command_example)**
- Running shell commands in cloud environments
- Capturing command output
- Command execution patterns

**[filesystem_example/](./filesystem_example)**
- File upload and download
- Directory operations
- File manipulation

**[watch_directory_example/](./watch_directory_example)**
- Watching directory changes
- File system events
- Change notifications

**[context_management/](./context_management)**
- Context creation and management
- Data storage and retrieval
- Cross-session data sharing

**[context_sync_example/](./context_sync_example)**
- Synchronizing data between sessions
- Context update mechanisms
- Data consistency management

**[context_sync_demo/](./context_sync_demo)**
- Practical context sync examples
- Real-world usage patterns
- Context sync workflows

**[data_persistence/](./data_persistence)**
- Storing data across sessions
- Data retrieval patterns
- Persistent storage management

### Advanced Features

**[agent_module/](./agent_module)**
- Using AI-powered automation
- Agent-based task execution
- Intelligent automation workflows

**[vpc_session/](./vpc_session)**
- Creating sessions in VPC environments
- Network security groups
- Private network access

## Environment-Specific Features

### Browser Use (`browser_latest`)

> **Note**: Browser Use APIs are not yet available in Golang SDK. Use Python or TypeScript SDK for browser automation.

### Computer Use (`windows_latest`, `linux_latest`)

**[application_window/](./application_window)**
- Application lifecycle control
- Window operations
- Desktop automation

**[automation/](./automation)**
- Desktop automation workflows
- Complex automation patterns
- Workflow orchestration

**[ui_example/](./ui_example)**
- User interface interactions
- Screen automation
- UI element manipulation

### Mobile Use (`mobile_latest`)

Mobile automation examples are available through the Mobile API. Refer to the API documentation for usage.

### CodeSpace (`code_latest`)

**[code_example/](./code_example)**
- Running code snippets
- Development environment usage
- Code execution workflows

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

## Best Practices

1. **Error handling**: Always check error returns
2. **Proper cleanup**: Delete sessions when done
3. **Resource management**: Close connections properly
4. **API key security**: Never commit API keys to version control

## Getting Help

For more information, see:
- [Golang SDK Documentation](../../)
- [API Reference](../api/)
- [Quick Start Guide](../../../docs/quickstart/)
- [Feature Guides](../../../docs/guides/)
