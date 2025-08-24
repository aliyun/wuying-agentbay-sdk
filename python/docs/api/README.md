# AgentBay Python SDK API 参考

本文档提供了AgentBay Python SDK的完整API参考。

## 📚 模块概览

| 模块 | 描述 | 主要类/函数 |
|------|------|-------------|
| [agentbay](#agentbay) | 主客户端类 | `AgentBay` |
| [session](#session) | 会话管理 | `Session` |
| [command](#command) | 命令执行 | `CommandExecutor` |
| [code](#code) | 代码执行 | `CodeExecutor` |
| [filesystem](#filesystem) | 文件系统操作 | `FileSystemManager` |
| [ui](#ui) | UI自动化 | `UIAutomation` |
| [context](#context) | 上下文管理 | `ContextManager` |
| [browser](#browser) | 浏览器自动化 | `BrowserAutomation` |

## 🚀 快速开始

```python
from agentbay import AgentBay

# 初始化客户端
agent_bay = AgentBay()

# 创建会话
session_result = agent_bay.create()
session = session_result.session

# 执行命令
result = session.command.execute("ls -la")
print(result.data.stdout)

# 清理会话
agent_bay.destroy(session.session_id)
```

## AgentBay

主客户端类，提供会话管理和高级功能。

### 构造函数

```python
AgentBay(api_key: Optional[str] = None, config: Optional[Dict] = None)
```

**参数:**
- `api_key` (str, optional): API密钥，默认从环境变量`AGENTBAY_API_KEY`获取
- `config` (dict, optional): 客户端配置

**示例:**
```python
# 使用环境变量中的API密钥
agent_bay = AgentBay()

# 显式指定API密钥
agent_bay = AgentBay(api_key="your-api-key")

# 带配置
agent_bay = AgentBay(config={"timeout": 30})
```

### 方法

#### create()

创建新的会话。

```python
create(params: Optional[CreateSessionParams] = None) -> CreateSessionResult
```

**参数:**
- `params` (CreateSessionParams, optional): 会话创建参数

**返回:**
- `CreateSessionResult`: 包含会话对象或错误信息

**示例:**
```python
# 创建默认会话
result = agent_bay.create()

# 创建带参数的会话
params = CreateSessionParams(
    image="ubuntu:20.04",
    labels={"project": "demo"}
)
result = agent_bay.create(params)
```

#### destroy()

销毁指定会话。

```python
destroy(session_id: str) -> DestroySessionResult
```

**参数:**
- `session_id` (str): 会话ID

**返回:**
- `DestroySessionResult`: 销毁结果

#### list()

列出所有会话。

```python
list(params: Optional[ListSessionParams] = None) -> ListSessionResult
```

**参数:**
- `params` (ListSessionParams, optional): 列表查询参数

**返回:**
- `ListSessionResult`: 会话列表

## Session

会话对象，提供对各种功能模块的访问。

### 属性

- `session_id` (str): 会话唯一标识符
- `status` (str): 会话状态
- `created_at` (datetime): 创建时间
- `command` (CommandExecutor): 命令执行器
- `code` (CodeExecutor): 代码执行器
- `file_system` (FileSystemManager): 文件系统管理器
- `ui` (UIAutomation): UI自动化
- `context_sync` (ContextSync): 上下文同步
- `browser` (BrowserAutomation): 浏览器自动化

## CommandExecutor

命令执行功能。

### execute()

执行Shell命令。

```python
execute(command: str, timeout: Optional[int] = None, input_data: Optional[str] = None) -> CommandResult
```

**参数:**
- `command` (str): 要执行的命令
- `timeout` (int, optional): 超时时间（秒）
- `input_data` (str, optional): 输入数据

**返回:**
- `CommandResult`: 命令执行结果

**示例:**
```python
# 基本命令执行
result = session.command.execute("ls -la")

# 带超时
result = session.command.execute("long_running_task", timeout=60)

# 交互式命令
result = session.command.execute("python3", input_data="print('hello')\nexit()\n")
```

## CodeExecutor

代码执行功能。

### run_code()

执行指定语言的代码。

```python
run_code(code: str, language: str, timeout: Optional[int] = None) -> CodeResult
```

**参数:**
- `code` (str): 要执行的代码
- `language` (str): 编程语言 ("python", "javascript", "go")
- `timeout` (int, optional): 超时时间（秒）

**返回:**
- `CodeResult`: 代码执行结果

**示例:**
```python
# Python代码
python_code = """
print("Hello from Python!")
result = 2 + 2
print(f"2 + 2 = {result}")
"""
result = session.code.run_code(python_code, "python")

# JavaScript代码
js_code = """
console.log("Hello from JavaScript!");
const result = 2 + 2;
console.log(`2 + 2 = ${result}`);
"""
result = session.code.run_code(js_code, "javascript")
```

## FileSystemManager

文件系统操作功能。

### read_file()

读取文件内容。

```python
read_file(file_path: str) -> FileReadResult
```

### write_file()

写入文件内容。

```python
write_file(file_path: str, content: str, encoding: str = "utf-8") -> FileWriteResult
```

### delete_file()

删除文件。

```python
delete_file(file_path: str) -> FileDeleteResult
```

### list_directory()

列出目录内容。

```python
list_directory(directory_path: str) -> DirectoryListResult
```

**示例:**
```python
# 写入文件
result = session.file_system.write_file("/tmp/test.txt", "Hello World!")

# 读取文件
result = session.file_system.read_file("/tmp/test.txt")
print(result.data)  # "Hello World!"

# 列出目录
result = session.file_system.list_directory("/tmp")
for file in result.data:
    print(f"{file.name} ({file.size} bytes)")
```

## UIAutomation

UI自动化功能。

### screenshot()

获取屏幕截图。

```python
screenshot() -> ScreenshotResult
```

### click()

模拟鼠标点击。

```python
click(x: int, y: int) -> ClickResult
```

### type()

模拟键盘输入。

```python
type(text: str) -> TypeResult
```

### key()

模拟按键。

```python
key(key_name: str) -> KeyResult
```

**示例:**
```python
# 截图
screenshot = session.ui.screenshot()
with open("screenshot.png", "wb") as f:
    f.write(screenshot.data)

# 鼠标和键盘操作
session.ui.click(100, 200)
session.ui.type("Hello AgentBay!")
session.ui.key("Enter")
```

## ContextManager

上下文管理功能。

### get()

获取或创建上下文。

```python
get(name: str, create: bool = False) -> ContextResult
```

### upload_file()

上传文件到上下文。

```python
upload_file(context_id: str, file_path: str, content: str) -> UploadResult
```

### download_file()

从上下文下载文件。

```python
download_file(context_id: str, file_path: str) -> DownloadResult
```

**示例:**
```python
# 获取上下文
context_result = agent_bay.context.get("my-project", create=True)
context = context_result.context

# 上传文件
agent_bay.context.upload_file(context.id, "/config.json", '{"version": "1.0"}')

# 下载文件
result = agent_bay.context.download_file(context.id, "/config.json")
print(result.data)
```

## 错误处理

所有API调用都返回结果对象，包含`is_error`属性和可能的错误信息。

```python
result = session.command.execute("invalid_command")
if result.is_error:
    print(f"错误: {result.error}")
    print(f"错误代码: {result.error_code}")
else:
    print(f"成功: {result.data}")
```

## 类型定义

### CreateSessionParams

```python
@dataclass
class CreateSessionParams:
    image: Optional[str] = None
    labels: Optional[Dict[str, str]] = None
    context_syncs: Optional[List[ContextSync]] = None
    session_type: Optional[str] = None
    vpc_config: Optional[Dict] = None
```

### CommandResult

```python
@dataclass
class CommandResult:
    is_error: bool
    error: Optional[str] = None
    error_code: Optional[str] = None
    data: Optional[CommandData] = None

@dataclass
class CommandData:
    stdout: str
    stderr: str
    exit_code: int
```

### CodeResult

```python
@dataclass
class CodeResult:
    is_error: bool
    error: Optional[str] = None
    data: Optional[CodeData] = None

@dataclass
class CodeData:
    stdout: str
    stderr: str
    execution_time: float
```

## 相关资源

- [功能指南](../../../docs/guides/) - 详细的功能使用指南
- [示例代码](../examples/) - 完整的示例代码
- [故障排除](../../../docs/quickstart/troubleshooting.md) - 常见问题解决

---

💡 **提示**: 这是Python SDK的API参考。其他语言的API可能略有不同，请参考对应语言的文档。 