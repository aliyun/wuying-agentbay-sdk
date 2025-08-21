# AgentBay SDK Examples

This directory contains code examples demonstrating how to use the AgentBay SDK in various programming languages. These examples cover different features and use cases to help you understand the SDK's capabilities.

## Python Examples

- [Basic Usage](python/basic_usage.py): Simple introduction to the SDK with session creation and command execution
- [Session Creation](python/session_creation): Creating sessions with different parameters
- [File System Operations](python/file_system/README.md): Working with files and directories
- [Context Management](python/context_management): Managing persistent contexts
- [Label Management](python/label_management): Working with session labels
- [Mobile System](python/mobile_system): Mobile-specific features
- [OSS Management](python/oss_management): Object Storage Service integration

## TypeScript Examples

- [Basic Usage](typescript/basic-usage.ts): Simple introduction to the SDK with session creation and command execution
- [Session Creation](typescript/session-creation): Creating sessions with different parameters
- [Context Management](typescript/context-management): Managing persistent contexts
- [Command Execution](typescript/command-example): Executing commands and running code
- [File System Operations](typescript/filesystem-example): Working with files and directories
- [UI Interaction](typescript/ui-example): Interacting with UI elements

## Golang Examples

- [Basic Usage](golang/basic_usage): Simple introduction to the SDK with session creation and command execution
- [Session Creation](golang/session_creation): Creating sessions with different parameters
- [Context Management](golang/context_management): Managing persistent contexts
- [Context Synchronization](golang/context_sync_example): Advanced context synchronization with policies
- [Command Execution](golang/command_example): Executing commands and running code
- [File System Operations](golang/filesystem_example): Working with files and directories

## Running the Examples

### Python

1. Install the SDK:
```bash
pip install wuying-agentbay-sdk
```

2. Set your API key:
```bash
export AGENTBAY_API_KEY=your_api_key_here
```

3. Run an example:
```bash
python basic_usage.py
```

### TypeScript

1. Install the SDK:
```bash
npm install wuying-agentbay-sdk
```

2. Set your API key:
```bash
export AGENTBAY_API_KEY=your_api_key_here
```

3. Compile and run an example:
```bash
cd ./docs/examples/typescript
npx ts-node basic-usage.ts
```

### Golang

1. Install the SDK:
```bash
go get github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay
```

2. Set your API key:
```bash
export AGENTBAY_API_KEY=your_api_key_here
```

3. Run an example:
```bash
go run main.go
```

## Common Features

All the examples demonstrate one or more of the following features:

- **Session Management**: Creating, listing, and deleting sessions
- **Command Execution**: Running shell commands or code in a cloud environment
- **File System Operations**: Reading, writing, and manipulating files
- **Context Management**: Working with persistent storage across sessions
- **Application Management**: Launching and controlling applications
- **UI Interaction**: Working with UI elements and capture screenshots
- **Label Management**: Organizing sessions with labels

For more detailed documentation, please refer to the [API Reference](../api-reference) and [Tutorials](../tutorials) directories.
