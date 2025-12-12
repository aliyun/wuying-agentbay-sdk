# AsyncExtension API Reference

> **💡 Sync Version**: This documentation covers the asynchronous API. For synchronous operations, see [`ExtensionsService`](../sync/extension.md).
>
> ⚡ **Performance Advantage**: Async API enables concurrent operations with 4-6x performance improvements for parallel tasks.

## 🧩 Related Tutorial

- [Browser Extensions Guide](../../../../docs/guides/browser-use/core-features/extension.md) - Learn how to use browser extensions



#### EXTENSIONS\_BASE\_PATH

```python
EXTENSIONS_BASE_PATH = "/tmp/extensions"
```

## Extension

```python
class Extension()
```

Represents a browser extension as a cloud resource.

### \_\_init\_\_

```python
def __init__(self, id: str, name: str, created_at: Optional[str] = None)
```

## ExtensionOption

```python
class ExtensionOption()
```

Configuration options for browser extension integration.

This class encapsulates the necessary parameters for setting up
browser extension synchronization and context management.

**Attributes**:

- `context_id` _str_ - ID of the extension context for browser extensions
- `extension_ids` _List[str]_ - List of extension IDs to be loaded/synchronized

### \_\_init\_\_

```python
def __init__(self, context_id: str, extension_ids: List[str])
```

Initialize ExtensionOption with context and extension configuration.

**Arguments**:

- `context_id` _str_ - ID of the extension context for browser extensions.
  This should match the context where extensions are stored.
- `extension_ids` _List[str]_ - List of extension IDs to be loaded in the browser session.
  Each ID should correspond to a valid extension in the context.
  

**Raises**:

    ValueError: If context_id is empty or extension_ids is empty.

### validate

```python
def validate() -> bool
```

Validate the extension option configuration.

**Returns**:

    bool: True if configuration is valid, False otherwise.
  

**Example**:

```python
ext_option = ExtensionOption("ctx-123", ["ext1.zip", "ext2.zip"])
is_valid = ext_option.validate()
print(f"Valid: {is_valid}")
```

## AsyncExtensionsService

```python
class AsyncExtensionsService()
```

Provides methods to manage user browser extensions asynchronously.
This service integrates with the existing context functionality for file operations.

**Usage** (Simplified - Auto-detection):
```python
# Service automatically detects if context exists and creates if needed
extensions_service = AsyncExtensionsService(agent_bay, "browser_extensions")

# Use the service immediately
extension = await extensions_service.create("/path/to/plugin.zip")
```

**Integration with ExtensionOption (Simplified)**:
```python
# Create extensions and configure for browser sessions
extensions_service = AsyncExtensionsService(agent_bay, "my_extensions")
ext1 = await extensions_service.create("/path/to/ext1.zip")
ext2 = await extensions_service.create("/path/to/ext2.zip")

# Create extension option for browser integration (no context_id needed!)
ext_option = await extensions_service.create_extension_option([ext1.id, ext2.id])

# Use with BrowserContext for session creation
browser_context = BrowserContext(
    context_id="browser_session",
    auto_upload=True,
    extension_option=ext_option  # All extension config encapsulated
)
```

**Context Management**:
- If context_id provided and exists: Uses the existing context
- If context_id provided but doesn't exist: Creates context with provided name
- If context_id empty or not provided: Generates default name and creates context
- No need to manually manage context creation

### \_\_init\_\_

```python
def __init__(self, agent_bay: "AsyncAgentBay", context_id: str = "")
```

Initializes the AsyncExtensionsService.

**Arguments**:

- `agent_bay` _AsyncAgentBay_ - The AgentBay client instance.
- `context_id` _str, optional_ - The context ID or name. If empty or not provided,
  a default context name will be generated automatically.
  If the context doesn't exist, it will be automatically created
  when needed.

### list

```python
async def list() -> List[Extension]
```

Lists all available browser extensions within this context from the cloud.
Uses the context service to list files under the extensions directory.

**Returns**:

    List[Extension]: List of all extensions in the context.
  

**Raises**:

    AgentBayError: If listing fails.
  

**Example**:

```python
extensions_service = AsyncExtensionsService(agent_bay, "my-extensions")
extensions = await extensions_service.list()
print(f"Found {len(extensions)} extensions")
```

### create

```python
async def create(local_path: str) -> Extension
```

Uploads a new browser extension from a local path into the current context.

**Arguments**:

- `local_path` _str_ - Path to the local extension ZIP file.
  

**Returns**:

    Extension: Extension object with generated ID and metadata.
  

**Raises**:

    FileNotFoundError: If the local file doesn't exist.
    ValueError: If the file format is not supported (only ZIP files allowed).
    AgentBayError: If upload fails.
  

**Example**:

```python
extensions_service = AsyncExtensionsService(agent_bay, "my-extensions")
extension = await extensions_service.create("/path/to/extension.zip")
print(f"Created extension: {extension.id}")
```

### update

```python
async def update(extension_id: str, new_local_path: str) -> Extension
```

Updates an existing browser extension in the current context with a new file.

**Arguments**:

- `extension_id` _str_ - ID of the extension to update.
- `new_local_path` _str_ - Path to the new extension ZIP file.
  

**Returns**:

    Extension: Updated extension object.
  

**Raises**:

    FileNotFoundError: If the new local file doesn't exist.
    ValueError: If the extension ID doesn't exist in the context.
    AgentBayError: If update fails.
  

**Example**:

```python
extensions_service = AsyncExtensionsService(agent_bay, "my-extensions")
updated = await extensions_service.update("ext_abc123.zip", "/path/to/new_version.zip")
print(f"Updated extension: {updated.id}")
```

### cleanup

```python
async def cleanup() -> bool
```

Cleans up the auto-created context if it was created by this service.

**Returns**:

    bool: True if cleanup was successful or not needed, False if cleanup failed.
  

**Notes**:

  This method only works if the context was auto-created by this service.
  For existing contexts, no cleanup is performed.
  

**Example**:

```python
extensions_service = AsyncExtensionsService(agent_bay)
success = await extensions_service.cleanup()
print(f"Cleanup success: {success}")
```

### delete

```python
async def delete(extension_id: str) -> bool
```

Deletes a browser extension from the current context.

**Arguments**:

- `extension_id` _str_ - ID of the extension to delete.
  

**Returns**:

    bool: True if deletion was successful, False otherwise.
  

**Example**:

```python
extensions_service = AsyncExtensionsService(agent_bay, "my-extensions")
success = await extensions_service.delete("ext_abc123.zip")
print(f"Delete success: {success}")
```

### create\_extension\_option

```python
async def create_extension_option(extension_ids: List[str]) -> ExtensionOption
```

Create an ExtensionOption for the current context with specified extension IDs.

This is a convenience method that creates an ExtensionOption using the current
service's context_id and the provided extension IDs. This option can then be
used with BrowserContext for browser session creation.

**Arguments**:

- `extension_ids` _List[str]_ - List of extension IDs to include in the option.
  These should be extensions that exist in the current context.
  

**Returns**:

    ExtensionOption: Configuration object for browser extension integration.
  

**Raises**:

    ValueError: If extension_ids is empty or invalid.
  

**Example**:

```python
extensions_service = AsyncExtensionsService(agent_bay, "my-extensions")
ext_option = await extensions_service.create_extension_option(["ext1.zip", "ext2.zip"])
print(f"Extension option: {ext_option}")
```

## See Also

- [Synchronous vs Asynchronous API](../../../docs/guides/async-programming/sync-vs-async.md)

**Related APIs:**
- [Browser API Reference](./async-browser.md)

---

*Documentation generated automatically from source code using pydoc-markdown.*
