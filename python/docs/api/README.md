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
api_key = os.getenv("AGENTBAY_API_KEY")
agent_bay = AgentBay(api_key)


# With configuration
from agentbay import Config
config = Config(region_id="cn-shanghai", endpoint="wuyingai.cn-shanghai.aliyuncs.com", timeout_ms=30000)
agent_bay = AgentBay(cfg=config)
```

### Methods

#### create()

Create a new session.

```python
create(params: Optional[CreateSessionParams] = None) -> SessionResult
```

**Parameters:**
- `params` (CreateSessionParams, optional): Session creation parameters

**Returns:**
- `SessionResult`: Contains session object or error information

**Examples:**
```python
# Create default session
result = agent_bay.create()

# Create session with parameters
params = CreateSessionParams(
    image_id="your_image_id",
    labels={"project": "demo"}
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

## Session

Session object that provides access to various functional modules.

### Properties

- `session_id` (str): Unique session identifier
- `command` (CommandExecutor): Command executor
- `code` (CodeExecutor): Code executor
- `file_system` (FileSystemManager): File system manager
- `ui` (UIAutomation): UI automation
- `context` (ContextManager): Context manager
- `browser` (BrowserAutomation): Browser automation
- `agent` (Agent): Agent functionality
- `application` (ApplicationManager): Application manager
- `window` (WindowManager): Window manager
- `oss` (Oss): OSS operations

## CommandExecutor

Command execution functionality.

### execute_command()

Execute a command in the cloud environment with a specified timeout.

```python
execute_command(command: str, timeout_ms: int = 1000) -> CommandResult
```

**Parameters:**
- `command` (str): Command to execute
- `timeout_ms` (int, optional): Timeout in milliseconds, defaults to 1000

**Returns:**
- `CommandResult`: Result object containing success status, command output,and error message if any.

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

Execute code in the specified language with a timeout.

```python
run_code(code: str, language: str, timeout_s: int = 300) -> CodeExecutionResult
```

**Parameters:**
- `code` (str): Code to execute
- `language` (str): Programming language ("python", "javascript")
- `timeout_s` (int, optional): Timeout in seconds, defaults to 300

**Returns:**
- `CodeExecutionResult`: Result object containing success status, execution result, and error message if any.

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
read_file(path: str,offset: int = 0, length: int = 0) -> FileContentResult
```
**Parameters:**
- `path` (str): The path of the file to read.
- `offset` (int): Byte offset to start reading from (0-based).
- `length` (int): Number of bytes to read. If 0, reads the entire file from offset.

**Returns:**
- `FileContentResult`: Result object containing file content and error message if any.

### write_file()

Write file content.

```python
write_file(path: str, content: str, mode: str = "overwrite") -> BoolResult
```
**Parameters:**
- `path` (str): The path of the file to write.
- `content` (str): The content to write to the file.
- `encoding` (str, optional): The write mode ("overwrite" or "append").
**Returns:**
- `BoolResult`: Result object containing success status and error message if any.



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
**Parameters:**
- `path` (str): The path of the directory to list.
**Returns:**
- `DirectoryListResult`: Result object containing directory entries and error message if any.

## UIAutomation

UI automation functionality.

### screenshot()

Takes a screenshot of the current screen using the system_screenshot tool.

```python
screenshot() -> OperationResult
```
**Returns:**
- `OperationResult`: Result object containing the path to the screenshot and error message if any.

### click()

Clicks on the screen at the specified coordinates.

```python
click(x: int, y: int, button: str = "left") -> BoolResult
```
**Parameters:**
- `x` (int): X coordinate of the click.
- `y` (int): Y coordinate of the click.
- `button` (str, optional):  Button type (left, middle, right), defaults to "left".
**Returns:**
- `BoolResult`: Result object containing success status and error message if any.


### key()

Simulate key press.

```python
send_key(key: int) -> BoolResult
```
**Parameters:**
- `key`(int): The key code to send. Supported key codes are:
    - 3 : HOME
    - 4 : BACK
    - 24 : VOLUME UP
    - 25 : VOLUME DOWN
    - 26 : POWER
    - 82 : MENU
**Returns**
- `BoolResult`: Result object containing success status and error message if any.

**Examples:**
```python
# Screenshot
 # Take screenshot
screenshot = session.ui.screenshot()
if screenshot.success:
    # Save screenshot locally
    with open("screenshot.png", "wb") as f:
        # Handle different data types
        if isinstance(screenshot.data, str):
            # Try to decode as base64 first (common for image data)
            try:
                import base64
                f.write(base64.b64decode(screenshot.data))
            except:
                # If not base64, encode as UTF-8
                f.write(screenshot.data.encode('utf-8'))
        else:
            # Already bytes
            f.write(screenshot.data)
else:
    print("Failed to take screenshot:", screenshot.error_message)

# Mouse and keyboard operations
result = session.ui.click(x=100, y=200,button="left")
if result.success:
    print("Click successful")
session.ui.type("Hello AgentBay!")

from agentbay.ui.ui import KeyCode
result = session.ui.send_key(KeyCode.MENU)
if result.success:
    print("Enter key pressed")
```

## ContextManager

Context management functionality.

### get()

Gets a context by name. Optionally creates it if it doesn't exist.

```python
get(name: str, create: bool = False) -> ContextResult
```
**Parameters:**
- `name` (str): The name of the context to get.
- `create` (bool, optional): Whether to create the context if it doesn't exist.
**Returns:**
- `ContextResult`: The ContextResult object containing the Context and request ID.

### update()

Upload file to context.

```python
update(context: Context) -> OperationResult
```
**Parameters:**
- `context` (Context): The context object to update.
**Returns:**
- `OperationResult`: Result object containing success status and request ID.

**Examples:**
```python
# Get context
context_result = agent_bay.context.get("my-project", create=True)
context = context_result.context

# update context
context.name = "renamed-test-context"
agent_bay.context.update(context)
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

Uploads a new browser extension from a local path into the current context.

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
if not result.success:
    print(f"Error: {result.error_message}")
    print(f"Error request_id: {result.request_id}")
else:
    print(f"Success: {result.output}")
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
```

### CommandResult

```python
@dataclass
class CommandResult:
    success: bool
    error_message: str = ""
    request_id:str = ""
    output:str = ""
```
### CodeResult

```python
@dataclass
class CodeExecutionResult:
    request_id: str = ""
    success: bool = False
    result: str = ""
    error_message: str = ""
```

## Related Resources

- [Feature Guides](../../../docs/guides/README.md) - Detailed feature usage guides
- [Example Code](../examples/) - Complete example code
- [Troubleshooting](../../../docs/quickstart/troubleshooting.md) - Common issue resolution

---

💡 **Tip**: This is the Python SDK API reference. APIs for other languages may differ slightly, please refer to the documentation for the corresponding language.
