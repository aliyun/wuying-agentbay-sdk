# API Quick Reference

Quick lookup for AgentBay SDK core API interfaces. For complete API documentation, please refer to the detailed documentation for each language.

## 🚀 Quick Navigation

| Feature Module | Python | TypeScript | Golang |
|----------------|--------|------------|--------|
| Client Initialization | [AgentBay](#agentbay-client) | [AgentBay](#agentbay-client) | [NewAgentBay](#agentbay-client) |
| Session Management | [Session](#session-management) | [Session](#session-management) | [Session](#session-management) |
| Command Execution | [Command](#command-execution) | [Command](#command-execution) | [Command](#command-execution) |
| File Operations | [FileSystem](#file-operations) | [FileSystem](#file-operations) | [FileSystem](#file-operations) |
| Code Execution | [Code](#code-execution) | [Code](#code-execution) | [Code](#code-execution) |
| UI Automation | [UI](#ui-automation) | [UI](#ui-automation) | [UI](#ui-automation) |
| Context Management | [Context](#context-management) | [Context](#context-management) | [Context](#context-management) |

## 🔧 AgentBay Client

### Initialization

<details>
<summary><strong>Python</strong></summary>

```python
from agentbay import AgentBay

# Use API key from environment variables
agent_bay = AgentBay()

# Explicitly specify API key
agent_bay = AgentBay(api_key="your-api-key")

# With configuration options
agent_bay = AgentBay(
    api_key="your-api-key",
    timeout=30,
    proxies={"http": "proxy-url", "https": "proxy-url"}
)
```
</details>

<details>
<summary><strong>TypeScript</strong></summary>

```typescript
import { AgentBay } from 'wuying-agentbay-sdk';

// Use API key from environment variables
const agentBay = new AgentBay();

// Explicitly specify API key
const agentBay = new AgentBay({ apiKey: "your-api-key" });

// With configuration options
const agentBay = new AgentBay({
    apiKey: "your-api-key",
    timeout: 30000,
    baseURL: "https://custom-endpoint.com"
});
```
</details>

<details>
<summary><strong>Golang</strong></summary>

```go
import "github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"

// Use API key from environment variables
client, err := agentbay.NewAgentBay("", nil)

// Explicitly specify API key
client, err := agentbay.NewAgentBay("your-api-key", nil)

// With configuration options
config := &agentbay.Config{
    APIKey:  "your-api-key",
    Timeout: 30,
    BaseURL: "https://custom-endpoint.com",
}
client, err := agentbay.NewAgentBay("", config)
```
</details>

## 📱 Session Management

### Create Session

<details>
<summary><strong>Python</strong></summary>

```python
# Basic session creation
result = agent_bay.create()
if not result.is_error:
    session = result.session

# Create with parameters
from agentbay import CreateSessionParams
params = CreateSessionParams(
    labels={"project": "web-scraper", "env": "dev"},
    image_id="linux_latest",
    is_vpc=False
)
result = agent_bay.create(params)
session = result.session
```
</details>

<details>
<summary><strong>TypeScript</strong></summary>

```typescript
// Basic session creation
const result = await agentBay.create();
if (!result.isError) {
    const session = result.session;
}

// Create with parameters
import { CreateSessionParams } from 'wuying-agentbay-sdk';
const params = new CreateSessionParams({
    labels: { project: "web-scraper", env: "dev" },
    imageId: "linux_latest",
    isVpc: false
});
const result = await agentBay.create(params);
const session = result.session;
```
</details>

<details>
<summary><strong>Golang</strong></summary>

```go
// Basic session creation
result, err := client.Create(nil)
if err == nil && !result.IsError {
    session := result.Session
}

// Create with parameters
params := &agentbay.CreateSessionParams{
    Labels:  map[string]string{"project": "web-scraper", "env": "dev"},
    ImageID: "linux_latest",
    IsVPC:   false,
}
result, err := client.Create(params)
session := result.Session
```
</details>

### List Sessions

<details>
<summary><strong>Python</strong></summary>

```python
# List all sessions
sessions = agent_bay.list()
for session in sessions:
    print(f"Session: {session.session_id}")

# List with labels filter
from agentbay import ListSessionParams
params = ListSessionParams(labels={"project": "web-scraper"})
result = agent_bay.list_by_labels(params)
sessions = result.sessions
```
</details>

<details>
<summary><strong>TypeScript</strong></summary>

```typescript
// List all sessions
const sessions = await agentBay.list();
sessions.forEach(session => {
    console.log(`Session: ${session.sessionId}`);
});

// List with labels filter
import { ListSessionParams } from 'wuying-agentbay-sdk';
const params = new ListSessionParams({ labels: { project: "web-scraper" } });
const result = await agentBay.listByLabels(params);
const sessions = result.sessions;
```
</details>

<details>
<summary><strong>Golang</strong></summary>

```go
// List all sessions
sessions := client.List()
for _, session := range sessions {
    fmt.Printf("Session: %s\n", session.SessionID)
}

// List with labels filter
params := &agentbay.ListSessionParams{
    Labels: map[string]string{"project": "web-scraper"},
}
result, err := client.ListByLabels(params)
sessions := result.Sessions
```
</details>

### Delete Session

<details>
<summary><strong>Python</strong></summary>

```python
# Delete session
result = agent_bay.delete(session)
if not result.is_error:
    print("Session deleted successfully")

# Delete with context sync
result = agent_bay.delete(session, sync_context=True)
```
</details>

<details>
<summary><strong>TypeScript</strong></summary>

```typescript
// Delete session
const result = await agentBay.delete(session);
if (!result.isError) {
    console.log("Session deleted successfully");
}

// Delete with context sync
const result = await agentBay.delete(session, { syncContext: true });
```
</details>

<details>
<summary><strong>Golang</strong></summary>

```go
// Delete session
result, err := client.Delete(session)
if err == nil && !result.IsError {
    fmt.Println("Session deleted successfully")
}

// Delete with context sync
options := &agentbay.DeleteOptions{SyncContext: true}
result, err := client.DeleteWithOptions(session, options)
```
</details>

## 💻 Command Execution

### Execute Commands

<details>
<summary><strong>Python</strong></summary>

```python
# Basic command execution
result = session.command.execute("ls -la")
if not result.is_error:
    print("Output:", result.output)
    print("Exit code:", result.exit_code)

# Command with timeout
result = session.command.execute("long-running-command", timeout_ms=30000)

# Interactive command
result = session.command.execute("python3", input_data="print('Hello')\nexit()\n")
```
</details>

<details>
<summary><strong>TypeScript</strong></summary>

```typescript
// Basic command execution
const result = await session.command.executeCommand("ls -la");
if (!result.isError) {
    console.log("Output:", result.output);
    console.log("Exit code:", result.exitCode);
}

// Command with timeout
const result = await session.command.executeCommand("long-running-command", { timeoutMs: 30000 });

// Interactive command
const result = await session.command.executeCommand("python3", { 
    inputData: "print('Hello')\nexit()\n" 
});
```
</details>

<details>
<summary><strong>Golang</strong></summary>

```go
// Basic command execution
result, err := session.Command.ExecuteCommand("ls -la")
if err == nil && !result.IsError {
    fmt.Println("Output:", result.Output)
    fmt.Println("Exit code:", result.ExitCode)
}

// Command with timeout
options := &agentbay.CommandOptions{TimeoutMs: 30000}
result, err := session.Command.ExecuteCommandWithOptions("long-running-command", options)

// Interactive command
options := &agentbay.CommandOptions{InputData: "print('Hello')\nexit()\n"}
result, err := session.Command.ExecuteCommandWithOptions("python3", options)
```
</details>

## 📁 File Operations

### Basic File Operations

<details>
<summary><strong>Python</strong></summary>

```python
# Write file
result = session.filesystem.write("/tmp/hello.txt", "Hello World")
if not result.is_error:
    print("File written successfully")

# Read file
result = session.filesystem.read("/tmp/hello.txt")
if not result.is_error:
    print("File content:", result.data)

# List directory
result = session.filesystem.list("/tmp")
if not result.is_error:
    for item in result.data:
        print(f"{item.name} ({item.type})")

# Delete file
result = session.filesystem.delete("/tmp/hello.txt")
```
</details>

<details>
<summary><strong>TypeScript</strong></summary>

```typescript
// Write file
const result = await session.filesystem.write("/tmp/hello.txt", "Hello World");
if (!result.isError) {
    console.log("File written successfully");
}

// Read file
const result = await session.filesystem.read("/tmp/hello.txt");
if (!result.isError) {
    console.log("File content:", result.data);
}

// List directory
const result = await session.filesystem.list("/tmp");
if (!result.isError) {
    result.data.forEach(item => {
        console.log(`${item.name} (${item.type})`);
    });
}

// Delete file
const result = await session.filesystem.delete("/tmp/hello.txt");
```
</details>

<details>
<summary><strong>Golang</strong></summary>

```go
// Write file
result, err := session.FileSystem.Write("/tmp/hello.txt", "Hello World")
if err == nil && !result.IsError {
    fmt.Println("File written successfully")
}

// Read file
result, err := session.FileSystem.Read("/tmp/hello.txt")
if err == nil && !result.IsError {
    fmt.Println("File content:", result.Data)
}

// List directory
result, err := session.FileSystem.List("/tmp")
if err == nil && !result.IsError {
    for _, item := range result.Data {
        fmt.Printf("%s (%s)\n", item.Name, item.Type)
    }
}

// Delete file
result, err := session.FileSystem.Delete("/tmp/hello.txt")
```
</details>

### File Upload/Download

<details>
<summary><strong>Python</strong></summary>

```python
# Upload file
result = session.filesystem.upload_file("local_file.txt", "/remote/path/file.txt")
if not result.is_error:
    print("File uploaded successfully")

# Download file
result = session.filesystem.download_file("/remote/path/file.txt", "local_file.txt")
if not result.is_error:
    print("File downloaded successfully")

# Upload multiple files
files = ["file1.txt", "file2.txt", "file3.txt"]
result = session.filesystem.upload_files(files, "/remote/directory/")
```
</details>

<details>
<summary><strong>TypeScript</strong></summary>

```typescript
// Upload file
const result = await session.filesystem.uploadFile("local_file.txt", "/remote/path/file.txt");
if (!result.isError) {
    console.log("File uploaded successfully");
}

// Download file
const result = await session.filesystem.downloadFile("/remote/path/file.txt", "local_file.txt");
if (!result.isError) {
    console.log("File downloaded successfully");
}

// Upload multiple files
const files = ["file1.txt", "file2.txt", "file3.txt"];
const result = await session.filesystem.uploadFiles(files, "/remote/directory/");
```
</details>

<details>
<summary><strong>Golang</strong></summary>

```go
// Upload file
result, err := session.FileSystem.UploadFile("local_file.txt", "/remote/path/file.txt")
if err == nil && !result.IsError {
    fmt.Println("File uploaded successfully")
}

// Download file
result, err := session.FileSystem.DownloadFile("/remote/path/file.txt", "local_file.txt")
if err == nil && !result.IsError {
    fmt.Println("File downloaded successfully")
}

// Upload multiple files
files := []string{"file1.txt", "file2.txt", "file3.txt"}
result, err := session.FileSystem.UploadFiles(files, "/remote/directory/")
```
</details>

## 🐍 Code Execution

### Run Code

<details>
<summary><strong>Python</strong></summary>

```python
# Execute Python code
code = """
import os
print(f"Current directory: {os.getcwd()}")
print("Hello from Python!")
"""
result = session.code.run_code(code, "python")
if not result.is_error:
    print("Output:", result.output)

# Execute JavaScript code
js_code = """
console.log("Hello from JavaScript!");
console.log("Node.js version:", process.version);
"""
result = session.code.run_code(js_code, "javascript")
```
</details>

<details>
<summary><strong>TypeScript</strong></summary>

```typescript
// Execute Python code
const code = `
import os
print(f"Current directory: {os.getcwd()}")
print("Hello from Python!")
`;
const result = await session.code.runCode(code, "python");
if (!result.isError) {
    console.log("Output:", result.output);
}

// Execute JavaScript code
const jsCode = `
console.log("Hello from JavaScript!");
console.log("Node.js version:", process.version);
`;
const result = await session.code.runCode(jsCode, "javascript");
```
</details>

<details>
<summary><strong>Golang</strong></summary>

```go
// Execute Python code
code := `
import os
print(f"Current directory: {os.getcwd()}")
print("Hello from Python!")
`
result, err := session.Code.RunCode(code, "python")
if err == nil && !result.IsError {
    fmt.Println("Output:", result.Output)
}

// Execute JavaScript code
jsCode := `
console.log("Hello from JavaScript!");
console.log("Node.js version:", process.version);
`
result, err := session.Code.RunCode(jsCode, "javascript")
```
</details>

## 🖱️ UI Automation

### Screen Operations

<details>
<summary><strong>Python</strong></summary>

```python
# Take screenshot
result = session.ui.screenshot()
if not result.is_error:
    with open("screenshot.png", "wb") as f:
        f.write(result.data)

# Click at coordinates
result = session.ui.click(x=100, y=200)

# Type text
result = session.ui.type("Hello World")

# Press key
result = session.ui.key_press("Enter")
```
</details>

<details>
<summary><strong>TypeScript</strong></summary>

```typescript
// Take screenshot
const result = await session.ui.screenshot();
if (!result.isError) {
    // Save screenshot
    require('fs').writeFileSync("screenshot.png", result.data);
}

// Click at coordinates
const result = await session.ui.click({ x: 100, y: 200 });

// Type text
const result = await session.ui.type("Hello World");

// Press key
const result = await session.ui.keyPress("Enter");
```
</details>

<details>
<summary><strong>Golang</strong></summary>

```go
// Take screenshot
result, err := session.UI.Screenshot()
if err == nil && !result.IsError {
    // Save screenshot
    ioutil.WriteFile("screenshot.png", result.Data, 0644)
}

// Click at coordinates
result, err := session.UI.Click(100, 200)

// Type text
result, err := session.UI.Type("Hello World")

// Press key
result, err := session.UI.KeyPress("Enter")
```
</details>

## 🔄 Context Management

### Context Operations

<details>
<summary><strong>Python</strong></summary>

```python
# Get or create context
result = agent_bay.context.get("my-project", create=True)
if not result.is_error:
    context = result.context
    print(f"Context ID: {context.id}")

# List contexts
result = agent_bay.context.list()
if not result.is_error:
    for ctx in result.contexts:
        print(f"Context: {ctx.name}")

# Delete context
result = agent_bay.context.delete("my-project")
```
</details>

<details>
<summary><strong>TypeScript</strong></summary>

```typescript
// Get or create context
const result = await agentBay.context.get("my-project", { create: true });
if (!result.isError) {
    const context = result.context;
    console.log(`Context ID: ${context.id}`);
}

// List contexts
const result = await agentBay.context.list();
if (!result.isError) {
    result.contexts.forEach(ctx => {
        console.log(`Context: ${ctx.name}`);
    });
}

// Delete context
const result = await agentBay.context.delete("my-project");
```
</details>

<details>
<summary><strong>Golang</strong></summary>

```go
// Get or create context
result, err := client.Context.Get("my-project", true)
if err == nil && !result.IsError {
    context := result.Context
    fmt.Printf("Context ID: %s\n", context.ID)
}

// List contexts
result, err := client.Context.List()
if err == nil && !result.IsError {
    for _, ctx := range result.Contexts {
        fmt.Printf("Context: %s\n", ctx.Name)
    }
}

// Delete context
result, err := client.Context.Delete("my-project")
```
</details>

This API reference provides quick access to the most commonly used AgentBay SDK functions. For detailed documentation and advanced features, please refer to the complete documentation for each language. 