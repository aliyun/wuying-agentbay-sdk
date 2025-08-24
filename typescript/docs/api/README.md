# AgentBay TypeScript SDK API 参考

本文档提供了AgentBay TypeScript SDK的完整API参考。

## 📚 模块概览

| 模块 | 描述 | 主要类/接口 |
|------|------|-------------|
| [AgentBay](#agentbay) | 主客户端类 | `AgentBay` |
| [Session](#session) | 会话管理 | `Session` |
| [Command](#command) | 命令执行 | `CommandExecutor` |
| [Code](#code) | 代码执行 | `CodeExecutor` |
| [FileSystem](#filesystem) | 文件系统操作 | `FileSystemManager` |
| [UI](#ui) | UI自动化 | `UIAutomation` |
| [Context](#context) | 上下文管理 | `ContextManager` |
| [Browser](#browser) | 浏览器自动化 | `BrowserAutomation` |

## 🚀 快速开始

```typescript
import { AgentBay } from 'wuying-agentbay-sdk';

async function main() {
    // 初始化客户端
    const agentBay = new AgentBay();
    
    // 创建会话
    const sessionResult = await agentBay.create();
    const session = sessionResult.session;
    
    // 执行命令
    const result = await session.command.execute("ls -la");
    console.log(result.data.stdout);
    
    // 清理会话
    await agentBay.destroy(session.sessionId);
}

main().catch(console.error);
```

## AgentBay

主客户端类，提供会话管理和高级功能。

### 构造函数

```typescript
constructor(apiKey?: string, config?: AgentBayConfig)
```

**参数:**
- `apiKey` (string, optional): API密钥，默认从环境变量`AGENTBAY_API_KEY`获取
- `config` (AgentBayConfig, optional): 客户端配置

**示例:**
```typescript
// 使用环境变量中的API密钥
const agentBay = new AgentBay();

// 显式指定API密钥
const agentBay = new AgentBay("your-api-key");

// 带配置
const agentBay = new AgentBay("your-api-key", { timeout: 30000 });
```

### 方法

#### create()

创建新的会话。

```typescript
async create(params?: CreateSessionParams): Promise<CreateSessionResult>
```

**参数:**
- `params` (CreateSessionParams, optional): 会话创建参数

**返回:**
- `Promise<CreateSessionResult>`: 包含会话对象或错误信息

**示例:**
```typescript
// 创建默认会话
const result = await agentBay.create();

// 创建带参数的会话
const params = {
    image: "ubuntu:20.04",
    labels: { project: "demo" }
};
const result = await agentBay.create(params);
```

#### destroy()

销毁指定会话。

```typescript
async destroy(sessionId: string): Promise<DestroySessionResult>
```

**参数:**
- `sessionId` (string): 会话ID

**返回:**
- `Promise<DestroySessionResult>`: 销毁结果

#### list()

列出所有会话。

```typescript
async list(params?: ListSessionParams): Promise<ListSessionResult>
```

**参数:**
- `params` (ListSessionParams, optional): 列表查询参数

**返回:**
- `Promise<ListSessionResult>`: 会话列表

## Session

会话对象，提供对各种功能模块的访问。

### 属性

- `sessionId` (string): 会话唯一标识符
- `status` (string): 会话状态
- `createdAt` (Date): 创建时间
- `command` (CommandExecutor): 命令执行器
- `code` (CodeExecutor): 代码执行器
- `fileSystem` (FileSystemManager): 文件系统管理器
- `ui` (UIAutomation): UI自动化
- `contextSync` (ContextSync): 上下文同步
- `browser` (BrowserAutomation): 浏览器自动化

## CommandExecutor

命令执行功能。

### execute()

执行Shell命令。

```typescript
async execute(command: string, options?: CommandOptions): Promise<CommandResult>
```

**参数:**
- `command` (string): 要执行的命令
- `options` (CommandOptions, optional): 执行选项
  - `timeout` (number): 超时时间（毫秒）
  - `inputData` (string): 输入数据

**返回:**
- `Promise<CommandResult>`: 命令执行结果

**示例:**
```typescript
// 基本命令执行
const result = await session.command.execute("ls -la");

// 带超时
const result = await session.command.execute("long_running_task", { timeout: 60000 });

// 交互式命令
const result = await session.command.execute("python3", {
    inputData: "print('hello')\nexit()\n"
});
```

## CodeExecutor

代码执行功能。

### runCode()

执行指定语言的代码。

```typescript
async runCode(code: string, language: string, options?: CodeOptions): Promise<CodeResult>
```

**参数:**
- `code` (string): 要执行的代码
- `language` (string): 编程语言 ("python", "javascript", "go")
- `options` (CodeOptions, optional): 执行选项
  - `timeout` (number): 超时时间（毫秒）

**返回:**
- `Promise<CodeResult>`: 代码执行结果

**示例:**
```typescript
// Python代码
const pythonCode = `
print("Hello from Python!")
result = 2 + 2
print(f"2 + 2 = {result}")
`;
const result = await session.code.runCode(pythonCode, "python");

// JavaScript代码
const jsCode = `
console.log("Hello from JavaScript!");
const result = 2 + 2;
console.log(\`2 + 2 = \${result}\`);
`;
const result = await session.code.runCode(jsCode, "javascript");
```

## FileSystemManager

文件系统操作功能。

### readFile()

读取文件内容。

```typescript
async readFile(filePath: string): Promise<FileReadResult>
```

### writeFile()

写入文件内容。

```typescript
async writeFile(filePath: string, content: string, encoding?: string): Promise<FileWriteResult>
```

### deleteFile()

删除文件。

```typescript
async deleteFile(filePath: string): Promise<FileDeleteResult>
```

### listDirectory()

列出目录内容。

```typescript
async listDirectory(directoryPath: string): Promise<DirectoryListResult>
```

**示例:**
```typescript
// 写入文件
await session.fileSystem.writeFile("/tmp/test.txt", "Hello World!");

// 读取文件
const result = await session.fileSystem.readFile("/tmp/test.txt");
console.log(result.data); // "Hello World!"

// 列出目录
const result = await session.fileSystem.listDirectory("/tmp");
result.data.forEach(file => {
    console.log(`${file.name} (${file.size} bytes)`);
});
```

## UIAutomation

UI自动化功能。

### screenshot()

获取屏幕截图。

```typescript
async screenshot(): Promise<ScreenshotResult>
```

### click()

模拟鼠标点击。

```typescript
async click(options: ClickOptions): Promise<ClickResult>
```

### type()

模拟键盘输入。

```typescript
async type(text: string): Promise<TypeResult>
```

### key()

模拟按键。

```typescript
async key(keyName: string): Promise<KeyResult>
```

**示例:**
```typescript
// 截图
const screenshot = await session.ui.screenshot();
// 保存截图到文件
await session.fileSystem.writeFile("/tmp/screenshot.png", screenshot.data);

// 鼠标和键盘操作
await session.ui.click({ x: 100, y: 200 });
await session.ui.type("Hello AgentBay!");
await session.ui.key("Enter");
```

## ContextManager

上下文管理功能。

### get()

获取或创建上下文。

```typescript
async get(name: string, options?: ContextOptions): Promise<ContextResult>
```

### uploadFile()

上传文件到上下文。

```typescript
async uploadFile(contextId: string, filePath: string, content: string): Promise<UploadResult>
```

### downloadFile()

从上下文下载文件。

```typescript
async downloadFile(contextId: string, filePath: string): Promise<DownloadResult>
```

**示例:**
```typescript
// 获取上下文
const contextResult = await agentBay.context.get("my-project", { create: true });
const context = contextResult.context;

// 上传文件
await agentBay.context.uploadFile(context.id, "/config.json", '{"version": "1.0"}');

// 下载文件
const result = await agentBay.context.downloadFile(context.id, "/config.json");
console.log(result.data);
```

## 错误处理

所有API调用都返回结果对象，包含`isError`属性和可能的错误信息。

```typescript
const result = await session.command.execute("invalid_command");
if (result.isError) {
    console.log(`错误: ${result.error}`);
    console.log(`错误代码: ${result.errorCode}`);
} else {
    console.log(`成功: ${result.data}`);
}
```

## 类型定义

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

## 相关资源

- [功能指南](../../../docs/guides/) - 详细的功能使用指南
- [示例代码](../examples/) - 完整的示例代码
- [故障排除](../../../docs/quickstart/troubleshooting.md) - 常见问题解决

---

💡 **提示**: 这是TypeScript SDK的API参考。其他语言的API可能略有不同，请参考对应语言的文档。 