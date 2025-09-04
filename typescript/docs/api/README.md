# AgentBay TypeScript SDK API Reference

This document provides a complete API reference for the AgentBay TypeScript SDK.

## 📚 Module Overview

| Module | Description | Main Classes/Interfaces |
|--------|-------------|-------------------------|
| [AgentBay](#agentbay) | Main client class | `AgentBay` |
| [Session](#session) | Session management | `Session` |
| [Command](#command) | Command execution | `CommandExecutor` |
| [Code](#code) | Code execution | `CodeExecutor` |
| [FileSystem](#filesystem) | File system operations | `FileSystemManager` |
| [UI](#ui) | UI automation | `UIAutomation` |
| [Context](#context) | Context management | `ContextManager` |
| [Extension](extension.md) | Browser extension management | `ExtensionsService`, `Extension`, `ExtensionOption` |
| [Browser](#browser) | Browser automation | `BrowserAutomation` |

## 🚀 Quick Start

```typescript
import { AgentBay } from 'wuying-agentbay-sdk';

async function main() {
    // Initialize client
    const agentBay = new AgentBay();
    
    // Create session
    const sessionResult = await agentBay.create();
    const session = sessionResult.session;
    
    // Execute command
    const result = await session.command.executeCommand("ls -la");
    console.log(result.output);
    
    // Clean up session
    await agentBay.delete(session);
}

main().catch(console.error);
```

## AgentBay

Main client class that provides session management and advanced features.

### Constructor

```typescript
constructor(options: { apiKey?: string; config?: Config; } = {})
```

**Parameters:**
- `options.apiKey` (string, optional): API key, defaults to `AGENTBAY_API_KEY` environment variable
- `options.config` (Config, optional): Client configuration object

**Examples:**
```typescript
// Use API key from environment variable
const agentBay = new AgentBay();

// Explicitly specify API key
const agentBay = new AgentBay({ apiKey: "your-api-key" });

// With configuration
const agentBay = new AgentBay({ 
    apiKey: "your-api-key", 
    config: { timeout_ms: 30000, region_id: "cn-shanghai", endpoint: "wuyingai.cn-shanghai.aliyuncs.com" } 
});
```

### Methods

#### create()

Create a new session.

```typescript
async create(params?: CreateSessionParams): Promise<CreateSessionResult>
```

**Parameters:**
- `params` (CreateSessionParams, optional): Session creation parameters

**Returns:**
- `Promise<CreateSessionResult>`: Contains session object or error information

**Examples:**
```typescript
// Create default session
const result = await agentBay.create();

// Create session with parameters
const params = {
    imageId: "ubuntu:20.04",
    labels: { project: "demo" }
};
const result = await agentBay.create(params);
```

#### delete()

Delete the specified session.

```typescript
async delete(session: Session, syncContext?: boolean): Promise<DeleteResult>
```

**Parameters:**
- `session` (Session): The session object to delete
- `syncContext` (boolean, optional): Whether to synchronize context before deletion, defaults to false

**Returns:**
- `Promise<DeleteResult>`: Deletion result

#### list()

List all locally cached sessions.

```typescript
list(): Session[]
```

**Returns:**
- `Session[]`: Array of locally cached sessions

#### listByLabels()

List sessions from the server filtered by labels with pagination support.

```typescript
async listByLabels(params?: ListSessionParams | Record<string, string>): Promise<SessionListResult>
```

**Parameters:**
- `params` (ListSessionParams | Record<string, string>, optional): List query parameters or labels object

**Returns:**
- `Promise<SessionListResult>`: Session list with pagination information

## Session

Session object that provides access to various functional modules.

### Properties

- `sessionId` (string): Unique session identifier
- `status` (string): Session status
- `createdAt` (Date): Creation time
- `command` (CommandExecutor): Command executor
- `code` (CodeExecutor): Code executor
- `fileSystem` (FileSystem): File system manager
- `ui` (UIAutomation): UI automation
- `contextSync` (ContextSync): Context synchronization
- `browser` (BrowserAutomation): Browser automation

## CommandExecutor

Command execution functionality.

### executeCommand()

Execute Shell commands.

```typescript
async executeCommand(command: string, timeoutMs?: number): Promise<CommandResult>
```

**Parameters:**
- `command` (string): Command to execute
- `timeoutMs` (number, optional): Timeout in milliseconds, defaults to 1000

**Returns:**
- `Promise<CommandResult>`: Command execution result

**Examples:**
```typescript
// Basic command execution
const result = await session.command.executeCommand("ls -la");

// With timeout (60 seconds)
const result = await session.command.executeCommand("long_running_task", 60000);
```

## CodeExecutor

Code execution functionality.

### runCode()

Execute code in the specified language.

```typescript
async runCode(code: string, language: string, timeoutS?: number): Promise<CodeExecutionResult>
```

**Parameters:**
- `code` (string): Code to execute
- `language` (string): Programming language ("python", "javascript")
- `timeoutS` (number, optional): Timeout in seconds, defaults to 300

**Returns:**
- `Promise<CodeExecutionResult>`: Code execution result

**Examples:**
```typescript
// Python code
const pythonCode = `
print("Hello from Python!")
result = 2 + 2
print(f"2 + 2 = {result}")
`;
const result = await session.code.runCode(pythonCode, "python");

// JavaScript code
const jsCode = `
console.log("Hello from JavaScript!");
const result = 2 + 2;
console.log(\`2 + 2 = \${result}\`);
`;
const result = await session.code.runCode(jsCode, "javascript");
```

## FileSystemManager

File system operations functionality.

### readFile()

Read file content.

```typescript
async readFile(path: string): Promise<FileContentResult>
```

### writeFile()

Write file content.

```typescript
async writeFile(path: string, content: string, mode?: string): Promise<BoolResult>
```


### listDirectory()

List directory contents.

```typescript
async listDirectory(path: string): Promise<DirectoryListResult>
```

**Examples:**
```typescript
// Write file
await session.fileSystem.writeFile("/tmp/test.txt", "Hello World!");

// Read file
const result = await session.fileSystem.readFile("/tmp/test.txt");
console.log(result.content); // "Hello World!"

// List directory
const listResult = await session.fileSystem.listDirectory("/tmp");
listResult.entries.forEach(file => {
    console.log(`${file.name} (${file.size} bytes)`);
});
```

## UIAutomation

UI automation functionality.

### screenshot()

Take screenshot.

```typescript
async screenshot(): Promise<ScreenshotResult>
```

### click()

Simulate mouse click.

```typescript
async click(options: ClickOptions): Promise<ClickResult>
```

### type()

Simulate keyboard input.

```typescript
async type(text: string): Promise<TypeResult>
```

### key()

Simulate key press.

```typescript
async key(keyName: string): Promise<KeyResult>
```

**Examples:**
```typescript
// Screenshot
const screenshot = await session.ui.screenshot();
// Save screenshot to file
await session.fileSystem.writeFile("/tmp/screenshot.png", screenshot.data);

// Mouse and keyboard operations
await session.ui.click({ x: 100, y: 200 });
await session.ui.type("Hello AgentBay!");
await session.ui.key("Enter");
```

## ContextManager

Context management functionality.

### get()

Get or create context.

```typescript
async get(name: string, options?: ContextOptions): Promise<ContextResult>
```

### uploadFile()

Upload file to context.

```typescript
async uploadFile(contextId: string, filePath: string, content: string): Promise<UploadResult>
```

### downloadFile()

Download file from context.

```typescript
async downloadFile(contextId: string, filePath: string): Promise<DownloadResult>
```

**Examples:**
```typescript
// Get context
const contextResult = await agentBay.context.get("my-project", { create: true });
const context = contextResult.context;

// Upload file
await agentBay.context.uploadFile(context.id, "/config.json", '{"version": "1.0"}');

// Download file
const result = await agentBay.context.downloadFile(context.id, "/config.json");
console.log(result.data);
```

## Error Handling

All API calls return result objects that contain `isError` property and possible error information.

```typescript
const result = await session.command.executeCommand("invalid_command");
if (result.isError) {
    console.log(`Error: ${result.error}`);
    console.log(`Error code: ${result.errorCode}`);
} else {
    console.log(`Success: ${result.data}`);
}
```

## Type Definitions

### CreateSessionParams

```typescript
interface CreateSessionParams {
    imageId?: string;
    labels?: Record<string, string>;
    contextSync?: ContextSync[];
    browserContext?: BrowserContext;
    isVpc?: boolean;
    mcpPolicyId?: string;
}
```

### CommandResult

```typescript
interface CommandResult {
    isError: boolean;
    error?: string;
    errorCode?: string;
    data?: CommandData;
}

interface CommandData {
    stdout: string;
    stderr: string;
    exitCode: number;
}
```

### CodeResult

```typescript
interface CodeResult {
    isError: boolean;
    error?: string;
    data?: CodeData;
}

interface CodeData {
    stdout: string;
    stderr: string;
    executionTime: number;
}
```

## Related Resources

- [Feature Guides](../../../docs/guides/) - Detailed feature usage guides
- [Example Code](../examples/) - Complete example code
- [Troubleshooting](../../../docs/quickstart/troubleshooting.md) - Common issue resolution

---

💡 **Tip**: This is the TypeScript SDK API reference. APIs for other languages may differ slightly, please refer to the documentation for the corresponding language.