# AgentBay Python SDK API Reference

This document provides a complete API reference for the AgentBay Python SDK.

## 📚 Module Overview

| Module | Description | Main Classes/Functions |
|--------|-------------|------------------------|
| [agentbay](#agentbay) | Main client class | `AgentBay` |
| [session](#session) | Session management | `Session` |
| [command](#command) | Command execution | `CommandExecutor` |
| [code](#code) | Code execution | `CodeExecutor` |
| [filesystem](#filesystem) | File system operations | `FileSystemManager` |
| [ui](#ui) | UI automation | `UIAutomation` |
| [context](#context) | Context management | `ContextManager` |
| [extension](extension.md) | Browser extension management | `ExtensionsService`, `ExtensionOption` |
| [browser](#browser) | Browser automation | `BrowserAutomation` |

## 🚀 Quick Start

```python
from agentbay import AgentBay

# Initialize client
agent_bay = AgentBay()

# Create session
session_result = agent_bay.create()
session = session_result.session

# Execute command
result = session.command.execute_command("ls -la")
print(result.output)

# Clean up session
agent_bay.delete(session)
```

## AgentBay

Main client class that provides session management and advanced features.

### Constructor

```python
AgentBay(api_key: str = "", cfg: Optional[Config] = None)
```

**Parameters:**
- `api_key` (str, optional): API key, defaults to `AGENTBAY_API_KEY` environment variable
- `cfg` (Config, optional): Client configuration object

**Examples:**
```python
# Use API key from environment variable
agent_bay = AgentBay()

# Explicitly specify API key
agent_bay = AgentBay(api_key="your-api-key")

# With configuration
from agentbay import Config
config = Config(region_id="cn-shanghai", endpoint="wuyingai.cn-shanghai.aliyuncs.com", timeout_ms=30000)
agent_bay = AgentBay(cfg=config)
```

### Methods

#### create()

Create a new session.

```python
create(params: Optional[CreateSessionParams] = None) -> CreateSessionResult
```

**Parameters:**
- `params` (CreateSessionParams, optional): Session creation parameters

**Returns:**
- `CreateSessionResult`: Contains session object or error information

**Examples:**
```python
# Create default session
result = agent_bay.create()

# Create session with parameters
params = CreateSessionParams(
    image_id="ubuntu:20.04",
    labels={"project": "demo"}
)
result = agent_bay.create(params)

# Create session with network_id
params = CreateSessionParams(
    image_id="ubuntu:20.04",
    labels={"project": "demo"},
    network_id="net-123456"
)
result = agent_bay.create(params)
```

#### delete()

Delete the specified session.

```python
delete(session: Session, sync_context: bool = False) -> DeleteResult
```

**Parameters:**
- `session` (Session): The session object to delete
- `sync_context` (bool, optional): Whether to synchronize context before deletion, defaults to False

**Returns:**
- `DeleteResult`: Deletion result

#### list()

List all locally cached sessions.

```python
list() -> List[Session]
```

**Returns:**
- `List[Session]`: List of locally cached sessions

#### list_by_labels()

List sessions from the server filtered by labels with pagination support.

```python
list_by_labels(params: Optional[Union[ListSessionParams, Dict[str, str]]] = None) -> SessionListResult
```

**Parameters:**
- `params` (Union[ListSessionParams, Dict[str, str]], optional): List query parameters or a dictionary of labels

**Returns:**
- `SessionListResult`: Session list with pagination information

## Session

Session object that provides access to various functional modules.

### Properties

- `session_id` (str): Unique session identifier
- `status` (str): Session status
- `created_at` (datetime): Creation time
- `command` (CommandExecutor): Command executor
- `code` (CodeExecutor): Code executor
- `file_system` (FileSystemManager): File system manager
- `ui` (UIAutomation): UI automation
- `context_sync` (ContextSync): Context synchronization
- `browser` (BrowserAutomation): Browser automation

## CommandExecutor

Command execution functionality.

### execute_command()

Execute Shell commands.

```python
execute_command(command: str, timeout_ms: int = 1000) -> CommandResult
```

**Parameters:**
- `command` (str): Command to execute
- `timeout_ms` (int, optional): Timeout in milliseconds, defaults to 1000

**Returns:**
- `CommandResult`: Command execution result

**Examples:**
```python
# Basic command execution
result = session.command.execute_command("ls -la")

# With timeout (60 seconds = 60000ms)
result = session.command.execute_command("long_running_task", timeout_ms=60000)

```

## CodeExecutor

Code execution functionality.

### run_code()

Execute code in the specified language.

```python
run_code(code: str, language: str, timeout_s: int = 300) -> CodeExecutionResult
```

**Parameters:**
- `code` (str): Code to execute
- `language` (str): Programming language ("python", "javascript")
- `timeout_s` (int, optional): Timeout in seconds, defaults to 300

**Returns:**
- `CodeExecutionResult`: Code execution result

**Examples:**
```python
# Python code
python_code = """
print("Hello from Python!")
result = 2 + 2
print(f"2 + 2 = {result}")
"""
result = session.code.run_code(python_code, "python")

# JavaScript code
js_code = """
console.log("Hello from JavaScript!");
const result = 2 + 2;
console.log(`2 + 2 = ${result}`);
"""
result = session.code.run_code(js_code, "javascript")
```

## FileSystemManager

File system operations functionality.

### read_file()

Read file content.

```python
read_file(path: str) -> FileContentResult
```

### write_file()

Write file content.

```python
write_file(path: str, content: str, encoding: str = "utf-8") -> BoolResult
```


### list_directory()

List directory contents.

```python
list_directory(path: str) -> DirectoryListResult
```

**Examples:**
```python
# Write file
result = session.file_system.write_file("/tmp/test.txt", "Hello World!")

# Read file
result = session.file_system.read_file("/tmp/test.txt")
print(result.content)  # "Hello World!"

# List directory
result = session.file_system.list_directory("/tmp")
for file in result.entries:
    print(f"{file['name']} ({file['size']} bytes)")
```

## UIAutomation

UI automation functionality.

### screenshot()

Take screenshot.

```python
screenshot() -> ScreenshotResult
```

### click()

Simulate mouse click.

```python
click(x: int, y: int, button: str = "left") -> BoolResult
```

### type()

Simulate keyboard input.

```python
type(text: str) -> TypeResult
```

### key()

Simulate key press.

```python
key(key_name: str) -> KeyResult
```

**Examples:**
```python
# Screenshot
screenshot = session.ui.screenshot()
with open("screenshot.png", "wb") as f:
    f.write(screenshot.data)

# Mouse and keyboard operations
session.ui.click(100, 200)
session.ui.type("Hello AgentBay!")
session.ui.key("Enter")
```

## ContextManager

Context management functionality.

### get()

Get or create context.

```python
get(name: str, create: bool = False) -> ContextResult
```

### upload_file()

Upload file to context.

```python
upload_file(context_id: str, file_path: str, content: str) -> UploadResult
```

### download_file()

Download file from context.

```python
download_file(context_id: str, file_path: str) -> DownloadResult
```

**Examples:**
```python
# Get context
context_result = agent_bay.context.get("my-project", create=True)
context = context_result.context

# Upload file
agent_bay.context.upload_file(context.id, "/config.json", '{"version": "1.0"}')

# Download file
result = agent_bay.context.download_file(context.id, "/config.json")
print(result.data)
```

## ExtensionsService

Browser extension management functionality.

### Constructor

Create an extensions service instance.

```python
ExtensionsService(agent_bay: AgentBay, context_id: str = "")
```

**Parameters:**
- `agent_bay` (AgentBay): AgentBay client instance
- `context_id` (str, optional): Context ID or name for extension storage

### create()

Upload a browser extension.

```python
create(local_path: str) -> Extension
```

### list()

List all extensions in the current context.

```python
list() -> List[Extension]
```

### create_extension_option()

Create extension configuration for browser sessions.

```python
create_extension_option(extension_ids: List[str]) -> ExtensionOption
```

**Examples:**
```python
from agentbay.extension import ExtensionsService
from agentbay.session_params import CreateSessionParams, BrowserContext

# Initialize extensions service
extensions_service = ExtensionsService(agent_bay)

# Upload extension
extension = extensions_service.create("/path/to/extension.zip")

# Create browser session with extension
ext_option = extensions_service.create_extension_option([extension.id])
session_params = CreateSessionParams(
    browser_context=BrowserContext(
        context_id="browser_session",
        extension_option=ext_option
    )
)
session = agent_bay.create(session_params).session

# Cleanup
extensions_service.cleanup()
```

**Related Documentation:**
- [Extension API Reference](./extension.md) - Complete API documentation
- [Extension Examples](../examples/extension/) - Practical code examples
- [Browser Extensions Guide](../../../docs/guides/browser-extensions.md) - Tutorial and best practices

## Error Handling

All API calls return result objects that contain `is_error` property and possible error information.

```python
result = session.command.execute_command("invalid_command")
if result.is_error:
    print(f"Error: {result.error}")
    print(f"Error code: {result.error_code}")
else:
    print(f"Success: {result.data}")
```

## Type Definitions

### CreateSessionParams

```python
@dataclass
class CreateSessionParams:
    image_id: Optional[str] = None
    labels: Optional[Dict[str, str]] = None
    context_syncs: Optional[List[ContextSync]] = None
    browser_context: Optional[BrowserContext] = None
    is_vpc: Optional[bool] = None
    mcp_policy_id: Optional[str] = None
    network_id: Optional[str] = None
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

## Related Resources

- [Feature Guides](../../../docs/guides/) - Detailed feature usage guides
- [Example Code](../examples/) - Complete example code
- [Troubleshooting](../../../docs/quickstart/troubleshooting.md) - Common issue resolution

---

💡 **Tip**: This is the Python SDK API reference. APIs for other languages may differ slightly, please refer to the documentation for the corresponding language.