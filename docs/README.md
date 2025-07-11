# AgentBay SDK Documentation

Welcome to the documentation for the AgentBay SDK, a powerful toolkit for interacting with AgentBay cloud environment.

## Getting Started

- [Getting Started Guide](getting-started.md): Installation, authentication, and basic usage
- [Authentication Guide](guides/authentication.md): How to authenticate with the AgentBay API

## Tutorials

Our tutorials provide step-by-step instructions for using different features of the SDK:

- [Session Management](tutorials/session-management.md): Create, list, and manage sessions
- [Command Execution](tutorials/command-execution.md): Execute shell commands in the cloud environment
- [Code Execution](tutorials/code-execution.md): Run Python and JavaScript code in the cloud environment
- [File Operations](tutorials/file-operations.md): Work with files and directories in the cloud environment
- [UI Interaction](tutorials/ui-interaction.md): Interact with UI elements and capture screenshots
- [Window Management](tutorials/window-management.md): Manage application windows in the cloud environment
- [OSS Integration](tutorials/oss-integration.md): Work with Object Storage Service (OSS)
- [Application Management](tutorials/application-management.md): Launch and manage applications
- [SDK Configuration](tutorials/sdk-configuration.md): Configure SDK settings for different environments
- [Data Persistence](tutorials/data-persistence.md): Persist data across sessions using contexts

## API Reference

Detailed documentation for all classes and methods in the SDK:

- [AgentBay](api-reference/agentbay.md): The main entry point for the SDK
- [Session](api-reference/session.md): Represents a session in the cloud environment
- [Command](api-reference/command.md): Execute commands in the cloud environment
- [FileSystem](api-reference/filesystem.md): Work with files and directories
- [UI](api-reference/ui.md): Interact with UI elements
- [Window](api-reference/window.md): Manage application windows
- [OSS](api-reference/oss.md): Work with Object Storage Service
- [Application](api-reference/application.md): Launch and manage applications
- [Context](api-reference/context.md): Manage persistent contexts
- [ContextManager](api-reference/context-manager.md): Manage contexts within a session

## Examples

Code examples for different languages:

- [Python Examples](examples/python): Basic usage, session creation, file operations, context management, and more
- [TypeScript Examples](examples/typescript): Basic usage, session creation, context management, command execution, and more 
- [Golang Examples](examples/golang): Basic usage, session creation, context management, command execution, and more

## SDK Architecture

The AgentBay SDK follows a client-service architecture:

```
AgentBay
├── Session
│   ├── FileSystem
│   ├── Command
│   ├── UI
│   ├── Window
│   ├── Application
│   ├── OSS
│   └── Context
└── ContextService
```

1. The `AgentBay` class is the main entry point and client for the SDK
2. Use `AgentBay` to create `Session` instances
3. Each `Session` provides access to various services:
   - `FileSystem`: File and directory operations
   - `Command`: Command execution
   - `UI`: UI interaction
   - `Window`: Window management
   - `Application`: Application management
   - `OSS`: Object Storage Service
   - `Context`: Context management within a session
4. The `AgentBay` class also provides direct access to `ContextService` for managing persistent contexts

## Feedback and Support

If you encounter any issues or have questions about the SDK, please submit an issue on GitHub or contact our support team.
