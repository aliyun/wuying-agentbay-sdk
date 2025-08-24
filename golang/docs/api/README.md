# AgentBay Golang SDK API Reference

This document provides a complete API reference for the AgentBay Golang SDK.

## 📚 Module Overview

| Module | Description | Main Structs/Interfaces |
|--------|-------------|-------------------------|
| [AgentBay](#agentbay) | Main client struct | `AgentBay` |
| [Session](#session) | Session management | `Session` |
| [Command](#command) | Command execution | `CommandExecutor` |
| [Code](#code) | Code execution | `CodeExecutor` |
| [FileSystem](#filesystem) | File system operations | `FileSystemManager` |
| [UI](#ui) | UI automation | `UIAutomation` |
| [Context](#context) | Context management | `ContextManager` |

## 🚀 Quick Start

```go
package main

import (
    "fmt"
    "log"
    
    "github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

func main() {
    // Initialize client
    client, err := agentbay.NewAgentBay("", nil)
    if err != nil {
        log.Fatalf("Initialization failed: %v", err)
    }
    
    // Create session
    sessionResult, err := client.Create(agentbay.NewCreateSessionParams())
    if err != nil {
        log.Fatalf("Session creation failed: %v", err)
    }
    
    session := sessionResult.Session
    
    // Execute command
    result, err := session.Command.ExecuteCommand("ls -la")
    if err == nil && !result.IsError {
        fmt.Printf("Command output: %s\n", result.Data.Stdout)
    }
    
    // Clean up session
    client.Destroy(session.SessionID)
}
```

## AgentBay

Main client struct that provides session management and advanced features.

### Constructor

#### NewAgentBay()

Create a new AgentBay client instance.

```go
func NewAgentBay(apiKey string, config *Config) (*AgentBay, error)
```

**Parameters:**
- `apiKey` (string): API key, empty string uses `AGENTBAY_API_KEY` environment variable
- `config` (*Config): Client configuration, nil uses default configuration

**Returns:**
- `*AgentBay`: Client instance
- `error`: Error information

**Examples:**
```go
// Use API key from environment variable
client, err := agentbay.NewAgentBay("", nil)

// Explicitly specify API key
client, err := agentbay.NewAgentBay("your-api-key", nil)

// With configuration
config := &agentbay.Config{
    Timeout: 30000,
    Region:  "cn-hangzhou",
}
client, err := agentbay.NewAgentBay("your-api-key", config)
```

### Methods

#### Create()

Create a new session.

```go
func (ab *AgentBay) Create(params *CreateSessionParams) (*CreateSessionResult, error)
```

**Parameters:**
- `params` (*CreateSessionParams): Session creation parameters

**Returns:**
- `*CreateSessionResult`: Contains session object or error information
- `error`: Error information

**Examples:**
```go
// Create default session
result, err := client.Create(agentbay.NewCreateSessionParams())

// Create session with parameters
params := agentbay.NewCreateSessionParams().
    SetImage("ubuntu:20.04").
    AddLabel("project", "demo")
result, err := client.Create(params)
```

#### Destroy()

Destroy the specified session.

```go
func (ab *AgentBay) Destroy(sessionID string) (*DestroySessionResult, error)
```

**Parameters:**
- `sessionID` (string): Session ID

**Returns:**
- `*DestroySessionResult`: Destruction result
- `error`: Error information

#### List()

List all sessions.

```go
func (ab *AgentBay) List(params *ListSessionParams) (*ListSessionResult, error)
```

**Parameters:**
- `params` (*ListSessionParams): List query parameters

**Returns:**
- `*ListSessionResult`: Session list
- `error`: Error information

## Session

Session struct that provides access to various functional modules.

### Fields

- `SessionID` (string): Unique session identifier
- `Status` (string): Session status
- `CreatedAt` (time.Time): Creation time
- `Command` (*CommandExecutor): Command executor
- `Code` (*CodeExecutor): Code executor
- `FileSystem` (*FileSystemManager): File system manager
- `UI` (*UIAutomation): UI automation
- `ContextSync` (*ContextSync): Context synchronization

## CommandExecutor

Command execution functionality.

### ExecuteCommand()

Execute Shell commands.

```go
func (ce *CommandExecutor) ExecuteCommand(command string) (*CommandResult, error)
```

### ExecuteCommandWithOptions()

Execute Shell commands with options.

```go
func (ce *CommandExecutor) ExecuteCommandWithOptions(command string, options *CommandOptions) (*CommandResult, error)
```

**Parameters:**
- `command` (string): Command to execute
- `options` (*CommandOptions): Execution options
  - `Timeout` (int): Timeout in seconds
  - `InputData` (string): Input data

**Returns:**
- `*CommandResult`: Command execution result
- `error`: Error information

**Examples:**
```go
// Basic command execution
result, err := session.Command.ExecuteCommand("ls -la")

// With timeout
options := &agentbay.CommandOptions{Timeout: 60}
result, err := session.Command.ExecuteCommandWithOptions("long_running_task", options)

// Interactive command
options := &agentbay.CommandOptions{
    InputData: "print('hello')\nexit()\n",
}
result, err := session.Command.ExecuteCommandWithOptions("python3", options)
```

## CodeExecutor

Code execution functionality.

### RunCode()

Execute code in the specified language.

```go
func (ce *CodeExecutor) RunCode(code string, language string) (*CodeResult, error)
```

### RunCodeWithOptions()

Execute code in the specified language with options.

```go
func (ce *CodeExecutor) RunCodeWithOptions(code string, language string, options *CodeOptions) (*CodeResult, error)
```

**Parameters:**
- `code` (string): Code to execute
- `language` (string): Programming language ("python", "javascript", "go")
- `options` (*CodeOptions): Execution options
  - `Timeout` (int): Timeout in seconds

**Returns:**
- `*CodeResult`: Code execution result
- `error`: Error information

**Examples:**
```go
// Python code
pythonCode := `
print("Hello from Python!")
result = 2 + 2
print(f"2 + 2 = {result}")
`
result, err := session.Code.RunCode(pythonCode, "python")

// JavaScript code
jsCode := `
console.log("Hello from JavaScript!");
const result = 2 + 2;
console.log(\`2 + 2 = \${result}\`);
`
result, err := session.Code.RunCode(jsCode, "javascript")
```

## FileSystemManager

File system operations functionality.

### ReadFile()

Read file content.

```go
func (fsm *FileSystemManager) ReadFile(filePath string) (*FileReadResult, error)
```

### WriteFile()

Write file content.

```go
func (fsm *FileSystemManager) WriteFile(filePath string, content string) (*FileWriteResult, error)
```

### DeleteFile()

Delete file.

```go
func (fsm *FileSystemManager) DeleteFile(filePath string) (*FileDeleteResult, error)
```

### ListDirectory()

List directory contents.

```go
func (fsm *FileSystemManager) ListDirectory(directoryPath string) (*DirectoryListResult, error)
```

**Examples:**
```go
// Write file
_, err := session.FileSystem.WriteFile("/tmp/test.txt", "Hello World!")

// Read file
result, err := session.FileSystem.ReadFile("/tmp/test.txt")
if err == nil && !result.IsError {
    fmt.Printf("File content: %s\n", result.Data) // "Hello World!"
}

// List directory
result, err := session.FileSystem.ListDirectory("/tmp")
if err == nil && !result.IsError {
    for _, file := range result.Data {
        fmt.Printf("%s (%d bytes)\n", file.Name, file.Size)
    }
}
```

## UIAutomation

UI automation functionality.

### Screenshot()

Take screenshot.

```go
func (ui *UIAutomation) Screenshot() (*ScreenshotResult, error)
```

### Click()

Simulate mouse click.

```go
func (ui *UIAutomation) Click(x, y int) (*ClickResult, error)
```

### Type()

Simulate keyboard input.

```go
func (ui *UIAutomation) Type(text string) (*TypeResult, error)
```

### Key()

Simulate key press.

```go
func (ui *UIAutomation) Key(keyName string) (*KeyResult, error)
```

**Examples:**
```go
// Screenshot
screenshot, err := session.UI.Screenshot()
if err == nil && !screenshot.IsError {
    // Save screenshot to file
    session.FileSystem.WriteFile("/tmp/screenshot.png", string(screenshot.Data))
}

// Mouse and keyboard operations
session.UI.Click(100, 200)
session.UI.Type("Hello AgentBay!")
session.UI.Key("Enter")
```

## ContextManager

Context management functionality.

### Get()

Get or create context.

```go
func (cm *ContextManager) Get(name string, create bool) (*ContextResult, error)
```

### UploadFile()

Upload file to context.

```go
func (cm *ContextManager) UploadFile(contextID, filePath, content string) (*UploadResult, error)
```

### DownloadFile()

Download file from context.

```go
func (cm *ContextManager) DownloadFile(contextID, filePath string) (*DownloadResult, error)
```

**Examples:**
```go
// Get context
contextResult, err := client.Context.Get("my-project", true)
if err == nil && !contextResult.IsError {
    context := contextResult.Context
    
    // Upload file
    client.Context.UploadFile(context.ID, "/config.json", `{"version": "1.0"}`)
    
    // Download file
    result, err := client.Context.DownloadFile(context.ID, "/config.json")
    if err == nil && !result.IsError {
        fmt.Printf("File content: %s\n", result.Data)
    }
}
```

## Error Handling

All API calls return result structs that contain `IsError` field and possible error information.

```go
result, err := session.Command.ExecuteCommand("invalid_command")
if err != nil {
    fmt.Printf("Call failed: %v\n", err)
} else if result.IsError {
    fmt.Printf("Command failed: %s\n", result.Error)
    fmt.Printf("Error code: %s\n", result.ErrorCode)
} else {
    fmt.Printf("Success: %s\n", result.Data.Stdout)
}
```

## Struct Definitions

### CreateSessionParams

```go
type CreateSessionParams struct {
    Image        string            `json:"image,omitempty"`
    Labels       map[string]string `json:"labels,omitempty"`
    ContextSyncs []ContextSync     `json:"context_syncs,omitempty"`
    SessionType  string            `json:"session_type,omitempty"`
    VPCConfig    *VPCConfig        `json:"vpc_config,omitempty"`
}
```

### CommandResult

```go
type CommandResult struct {
    IsError   bool         `json:"is_error"`
    Error     string       `json:"error,omitempty"`
    ErrorCode string       `json:"error_code,omitempty"`
    Data      *CommandData `json:"data,omitempty"`
}

type CommandData struct {
    Stdout   string `json:"stdout"`
    Stderr   string `json:"stderr"`
    ExitCode int    `json:"exit_code"`
}
```

### CodeResult

```go
type CodeResult struct {
    IsError bool      `json:"is_error"`
    Error   string    `json:"error,omitempty"`
    Data    *CodeData `json:"data,omitempty"`
}

type CodeData struct {
    Stdout        string  `json:"stdout"`
    Stderr        string  `json:"stderr"`
    ExecutionTime float64 `json:"execution_time"`
}
```

## Related Resources

- [Feature Guides](../../../docs/guides/) - Detailed feature usage guides
- [Example Code](../examples/) - Complete example code
- [Troubleshooting](../../../docs/quickstart/troubleshooting.md) - Common issue resolution

---

💡 **Tip**: This is the Golang SDK API reference. APIs for other languages may differ slightly, please refer to the documentation for the corresponding language.