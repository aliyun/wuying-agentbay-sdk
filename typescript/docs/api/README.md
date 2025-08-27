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
    await agentBay.destroy(session.sessionId);
}

main().catch(console.error);
```

## AgentBay

Main client class that provides session management and advanced features.

### Constructor

```typescript
constructor(apiKey?: string, config?: AgentBayConfig)
```

**Parameters:**
- `apiKey` (string, optional): API key, defaults to `AGENTBAY_API_KEY` environment variable
- `config` (AgentBayConfig, optional): Client configuration

**Examples:**
```typescript
// Use API key from environment variable
const agentBay = new AgentBay();

// Explicitly specify API key
const agentBay = new AgentBay("your-api-key");

// With configuration
const agentBay = new AgentBay("your-api-key", { timeout: 30000 });
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
    image: "ubuntu:20.04",
    labels: { project: "demo" }
};
const result = await agentBay.create(params);
```

#### destroy()

Destroy the specified session.

```typescript
async destroy(sessionId: string): Promise<DestroySessionResult>
```

**Parameters:**
- `sessionId` (string): Session ID

**Returns:**
- `Promise<DestroySessionResult>`: Destruction result

#### list()

List all sessions.

```typescript
async list(params?: ListSessionParams): Promise<ListSessionResult>
```

**Parameters:**
- `params` (ListSessionParams, optional): List query parameters

**Returns:**
- `Promise<ListSessionResult>`: Session list

## Session

Session object that provides access to various functional modules.

### Properties

- `sessionId` (string): Unique session identifier
- `status` (string): Session status
- `createdAt` (Date): Creation time
- `command` (CommandExecutor): Command executor
- `code` (CodeExecutor): Code executor
- `fileSystem` (FileSystemManager): File system manager
- `ui` (UIAutomation): UI automation
- `contextSync` (ContextSync): Context synchronization
- `browser` (BrowserAutomation): Browser automation

## CommandExecutor

Command execution functionality.

### execute()

Execute Shell commands.

```typescript
async execute(command: string, options?: CommandOptions): Promise<CommandResult>
```

**Parameters:**
- `command` (string): Command to execute
- `options` (CommandOptions, optional): Execution options
  - `timeout` (number): Timeout in milliseconds
  - `inputData` (string): Input data

**Returns:**
- `Promise<CommandResult>`: Command execution result

**Examples:**
```typescript
// Basic command execution
const result = await session.command.executeCommand("ls -la");

// With timeout
const result = await session.command.executeCommand("long_running_task", { timeout: 60000 });

// Interactive command
const result = await session.command.executeCommand("python3", {
    inputData: "print('hello')\nexit()\n"
});
```

## CodeExecutor

Code execution functionality.

### runCode()

Execute code in the specified language.

```typescript
async runCode(code: string, language: string, options?: CodeOptions): Promise<CodeResult>
```

**Parameters:**
- `code` (string): Code to execute
- `language` (string): Programming language ("python", "javascript", "go")
- `options` (CodeOptions, optional): Execution options
  - `timeout` (number): Timeout in milliseconds

**Returns:**
- `Promise<CodeResult>`: Code execution result

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
async readFile(filePath: string): Promise<FileReadResult>
```

### writeFile()

Write file content.

```typescript
async writeFile(filePath: string, content: string, encoding?: string): Promise<FileWriteResult>
```

### deleteFile()

Delete file.

```typescript
async deleteFile(filePath: string): Promise<FileDeleteResult>
```

### listDirectory()

List directory contents.

```typescript
async listDirectory(directoryPath: string): Promise<DirectoryListResult>
```

**Examples:**
```typescript
// Write file
await session.fileSystem.writeFile("/tmp/test.txt", "Hello World!");

// Read file
const result = await session.fileSystem.readFile("/tmp/test.txt");
console.log(result.data); // "Hello World!"

// List directory
const result = await session.fileSystem.listDirectory("/tmp");
result.data.forEach(file => {
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
    image?: string;
    labels?: Record<string, string>;
    contextSyncs?: ContextSync[];
    sessionType?: string;
    vpcConfig?: VPCConfig;
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