# AgentBay Golang SDK API 参考

本文档提供了AgentBay Golang SDK的完整API参考。

## 📚 模块概览

| 模块 | 描述 | 主要结构体/接口 |
|------|------|----------------|
| [AgentBay](#agentbay) | 主客户端结构体 | `AgentBay` |
| [Session](#session) | 会话管理 | `Session` |
| [Command](#command) | 命令执行 | `CommandExecutor` |
| [Code](#code) | 代码执行 | `CodeExecutor` |
| [FileSystem](#filesystem) | 文件系统操作 | `FileSystemManager` |
| [UI](#ui) | UI自动化 | `UIAutomation` |
| [Context](#context) | 上下文管理 | `ContextManager` |

## 🚀 快速开始

```go
package main

import (
    "fmt"
    "log"
    
    "github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

func main() {
    // 初始化客户端
    client, err := agentbay.NewAgentBay("", nil)
    if err != nil {
        log.Fatalf("初始化失败: %v", err)
    }
    
    // 创建会话
    sessionResult, err := client.Create(agentbay.NewCreateSessionParams())
    if err != nil {
        log.Fatalf("创建会话失败: %v", err)
    }
    
    session := sessionResult.Session
    
    // 执行命令
    result, err := session.Command.ExecuteCommand("ls -la")
    if err == nil && !result.IsError {
        fmt.Printf("命令输出: %s\n", result.Data.Stdout)
    }
    
    // 清理会话
    client.Destroy(session.SessionID)
}
```

## AgentBay

主客户端结构体，提供会话管理和高级功能。

### 构造函数

#### NewAgentBay()

创建新的AgentBay客户端实例。

```go
func NewAgentBay(apiKey string, config *Config) (*AgentBay, error)
```

**参数:**
- `apiKey` (string): API密钥，空字符串时从环境变量`AGENTBAY_API_KEY`获取
- `config` (*Config): 客户端配置，nil时使用默认配置

**返回:**
- `*AgentBay`: 客户端实例
- `error`: 错误信息

**示例:**
```go
// 使用环境变量中的API密钥
client, err := agentbay.NewAgentBay("", nil)

// 显式指定API密钥
client, err := agentbay.NewAgentBay("your-api-key", nil)

// 带配置
config := &agentbay.Config{
    Timeout: 30000,
    Region:  "cn-hangzhou",
}
client, err := agentbay.NewAgentBay("your-api-key", config)
```

### 方法

#### Create()

创建新的会话。

```go
func (ab *AgentBay) Create(params *CreateSessionParams) (*CreateSessionResult, error)
```

**参数:**
- `params` (*CreateSessionParams): 会话创建参数

**返回:**
- `*CreateSessionResult`: 包含会话对象或错误信息
- `error`: 错误信息

**示例:**
```go
// 创建默认会话
result, err := client.Create(agentbay.NewCreateSessionParams())

// 创建带参数的会话
params := agentbay.NewCreateSessionParams().
    SetImage("ubuntu:20.04").
    AddLabel("project", "demo")
result, err := client.Create(params)
```

#### Destroy()

销毁指定会话。

```go
func (ab *AgentBay) Destroy(sessionID string) (*DestroySessionResult, error)
```

**参数:**
- `sessionID` (string): 会话ID

**返回:**
- `*DestroySessionResult`: 销毁结果
- `error`: 错误信息

#### List()

列出所有会话。

```go
func (ab *AgentBay) List(params *ListSessionParams) (*ListSessionResult, error)
```

**参数:**
- `params` (*ListSessionParams): 列表查询参数

**返回:**
- `*ListSessionResult`: 会话列表
- `error`: 错误信息

## Session

会话结构体，提供对各种功能模块的访问。

### 字段

- `SessionID` (string): 会话唯一标识符
- `Status` (string): 会话状态
- `CreatedAt` (time.Time): 创建时间
- `Command` (*CommandExecutor): 命令执行器
- `Code` (*CodeExecutor): 代码执行器
- `FileSystem` (*FileSystemManager): 文件系统管理器
- `UI` (*UIAutomation): UI自动化
- `ContextSync` (*ContextSync): 上下文同步

## CommandExecutor

命令执行功能。

### ExecuteCommand()

执行Shell命令。

```go
func (ce *CommandExecutor) ExecuteCommand(command string) (*CommandResult, error)
```

### ExecuteCommandWithOptions()

带选项执行Shell命令。

```go
func (ce *CommandExecutor) ExecuteCommandWithOptions(command string, options *CommandOptions) (*CommandResult, error)
```

**参数:**
- `command` (string): 要执行的命令
- `options` (*CommandOptions): 执行选项
  - `Timeout` (int): 超时时间（秒）
  - `InputData` (string): 输入数据

**返回:**
- `*CommandResult`: 命令执行结果
- `error`: 错误信息

**示例:**
```go
// 基本命令执行
result, err := session.Command.ExecuteCommand("ls -la")

// 带超时
options := &agentbay.CommandOptions{Timeout: 60}
result, err := session.Command.ExecuteCommandWithOptions("long_running_task", options)

// 交互式命令
options := &agentbay.CommandOptions{
    InputData: "print('hello')\nexit()\n",
}
result, err := session.Command.ExecuteCommandWithOptions("python3", options)
```

## CodeExecutor

代码执行功能。

### RunCode()

执行指定语言的代码。

```go
func (ce *CodeExecutor) RunCode(code string, language string) (*CodeResult, error)
```

### RunCodeWithOptions()

带选项执行指定语言的代码。

```go
func (ce *CodeExecutor) RunCodeWithOptions(code string, language string, options *CodeOptions) (*CodeResult, error)
```

**参数:**
- `code` (string): 要执行的代码
- `language` (string): 编程语言 ("python", "javascript", "go")
- `options` (*CodeOptions): 执行选项
  - `Timeout` (int): 超时时间（秒）

**返回:**
- `*CodeResult`: 代码执行结果
- `error`: 错误信息

**示例:**
```go
// Python代码
pythonCode := `
print("Hello from Python!")
result = 2 + 2
print(f"2 + 2 = {result}")
`
result, err := session.Code.RunCode(pythonCode, "python")

// JavaScript代码
jsCode := `
console.log("Hello from JavaScript!");
const result = 2 + 2;
console.log(\`2 + 2 = \${result}\`);
`
result, err := session.Code.RunCode(jsCode, "javascript")
```

## FileSystemManager

文件系统操作功能。

### ReadFile()

读取文件内容。

```go
func (fsm *FileSystemManager) ReadFile(filePath string) (*FileReadResult, error)
```

### WriteFile()

写入文件内容。

```go
func (fsm *FileSystemManager) WriteFile(filePath string, content string) (*FileWriteResult, error)
```

### DeleteFile()

删除文件。

```go
func (fsm *FileSystemManager) DeleteFile(filePath string) (*FileDeleteResult, error)
```

### ListDirectory()

列出目录内容。

```go
func (fsm *FileSystemManager) ListDirectory(directoryPath string) (*DirectoryListResult, error)
```

**示例:**
```go
// 写入文件
_, err := session.FileSystem.WriteFile("/tmp/test.txt", "Hello World!")

// 读取文件
result, err := session.FileSystem.ReadFile("/tmp/test.txt")
if err == nil && !result.IsError {
    fmt.Printf("文件内容: %s\n", result.Data) // "Hello World!"
}

// 列出目录
result, err := session.FileSystem.ListDirectory("/tmp")
if err == nil && !result.IsError {
    for _, file := range result.Data {
        fmt.Printf("%s (%d bytes)\n", file.Name, file.Size)
    }
}
```

## UIAutomation

UI自动化功能。

### Screenshot()

获取屏幕截图。

```go
func (ui *UIAutomation) Screenshot() (*ScreenshotResult, error)
```

### Click()

模拟鼠标点击。

```go
func (ui *UIAutomation) Click(x, y int) (*ClickResult, error)
```

### Type()

模拟键盘输入。

```go
func (ui *UIAutomation) Type(text string) (*TypeResult, error)
```

### Key()

模拟按键。

```go
func (ui *UIAutomation) Key(keyName string) (*KeyResult, error)
```

**示例:**
```go
// 截图
screenshot, err := session.UI.Screenshot()
if err == nil && !screenshot.IsError {
    // 保存截图到文件
    session.FileSystem.WriteFile("/tmp/screenshot.png", string(screenshot.Data))
}

// 鼠标和键盘操作
session.UI.Click(100, 200)
session.UI.Type("Hello AgentBay!")
session.UI.Key("Enter")
```

## ContextManager

上下文管理功能。

### Get()

获取或创建上下文。

```go
func (cm *ContextManager) Get(name string, create bool) (*ContextResult, error)
```

### UploadFile()

上传文件到上下文。

```go
func (cm *ContextManager) UploadFile(contextID, filePath, content string) (*UploadResult, error)
```

### DownloadFile()

从上下文下载文件。

```go
func (cm *ContextManager) DownloadFile(contextID, filePath string) (*DownloadResult, error)
```

**示例:**
```go
// 获取上下文
contextResult, err := client.Context.Get("my-project", true)
if err == nil && !contextResult.IsError {
    context := contextResult.Context
    
    // 上传文件
    client.Context.UploadFile(context.ID, "/config.json", `{"version": "1.0"}`)
    
    // 下载文件
    result, err := client.Context.DownloadFile(context.ID, "/config.json")
    if err == nil && !result.IsError {
        fmt.Printf("文件内容: %s\n", result.Data)
    }
}
```

## 错误处理

所有API调用都返回结果结构体，包含`IsError`字段和可能的错误信息。

```go
result, err := session.Command.ExecuteCommand("invalid_command")
if err != nil {
    fmt.Printf("调用失败: %v\n", err)
} else if result.IsError {
    fmt.Printf("命令失败: %s\n", result.Error)
    fmt.Printf("错误代码: %s\n", result.ErrorCode)
} else {
    fmt.Printf("成功: %s\n", result.Data.Stdout)
}
```

## 结构体定义

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

## 相关资源

- [功能指南](../../../docs/guides/) - 详细的功能使用指南
- [示例代码](../examples/) - 完整的示例代码
- [故障排除](../../../docs/quickstart/troubleshooting.md) - 常见问题解决

---

💡 **提示**: 这是Golang SDK的API参考。其他语言的API可能略有不同，请参考对应语言的文档。 