# SessionParams API Reference

## BrowserContext

```python
class BrowserContext()
```

Browser context configuration for session.

This class provides browser context configuration for cloud sessions, supports browser fingerprint
context persistence, supports automatic extension synchronization when ExtensionOption is provided.

Key Features:
- Browser context binding for sessions
- Automatic browser data upload on session end
- Optional browser fingerprint integration with automatic context sync generation
- Optional extension integration with automatic context sync generation
- Clean API with ExtensionOption encapsulation

**Attributes**:

- `context_id` _str_ - ID of the browser context to bind to the session
- `auto_upload` _bool_ - Whether to automatically upload browser data when session ends
  fingerprint_context (Optional[BrowserFingerprintContext]):
  Browser fingerprint context configuration object containing fingerprint_context_id.
- `extension_option` _Optional[ExtensionOption]_ - Extension configuration object containing
  context_id and extension_ids.
- `extension_context_id` _Optional[str]_ - ID of the extension context for browser extensions.
  Set automatically from extension_option.
- `extension_ids` _Optional[List[str]]_ - List of extension IDs to synchronize.
  Set automatically from extension_option.
- `extension_context_syncs` _Optional[List[ContextSync]]_ - Auto-generated context syncs for extensions.
  None if no extension configuration provided,
  or List[ContextSync] if extensions are configured.
  
  Extension Configuration:
  - **ExtensionOption**: Pass an ExtensionOption object with context_id and extension_ids
  - **No Extensions**: Don't provide extension_option parameter (extension_context_syncs will be None)
  
  Usage Examples:
    ```python
    # With extensions using ExtensionOption
    from agentbay.extension import ExtensionOption

    ext_option = ExtensionOption(
        context_id="my_extensions",
        extension_ids=["ext1", "ext2"]
    )

    browser_context = BrowserContext(
        context_id="browser_session",
        auto_upload=True,
        extension_option=ext_option
    )

    # Without extensions (minimal configuration)
    browser_context = BrowserContext(
        context_id="browser_session",
        auto_upload=True
    )
    # extension_context_syncs will be None
    ```

### \_\_init\_\_

```python
def __init__(self, 
        context_id: str,
        auto_upload: bool = True,
        extension_option: Optional["ExtensionOption"] = None,
        fingerprint_context: Optional["BrowserFingerprintContext"] = None)
```

Initialize BrowserContext with optional extension support.

**Arguments**:

- `context_id` _str_ - ID of the browser context to bind to the session.
  This identifies the browser instance for the session.
  
- `auto_upload` _bool, optional_ - Whether to automatically upload browser data
  when the session ends. Defaults to True.
  
  fingerprint_context (Optional[BrowserFingerprintContext], optional):
  Browser fingerprint context configuration object containing fingerprint_context_id.
  Defaults to None.
  
- `extension_option` _Optional[ExtensionOption], optional_ - Extension configuration object containing
  context_id and extension_ids. This encapsulates
  all extension-related configuration.
  Defaults to None.
  Fingerprint Configuration:
  - **BrowserFingerprintContext**: Use fingerprint_context parameter with a BrowserFingerprintContext object
  - **No Fingerprint**: Don't provide fingerprint_context parameter (fingerprint_context_sync will be None)
  
  Fingerprint Auto-generation:
  - fingerprint_context_sync is automatically generated when fingerprint_context is provided
  - fingerprint_context_sync will be None if no fingerprint_context is provided
  - fingerprint_context_sync will be a ContextSync if fingerprint_context is valid
  
  Extension Configuration:
  - **ExtensionOption**: Use extension_option parameter with an ExtensionOption object
  - **No Extensions**: Don't provide extension_option parameter
  
  Auto-generation:
  - extension_context_syncs is automatically generated when extension_option is provided
  - extension_context_syncs will be None if no extension_option is provided
  - extension_context_syncs will be a List[ContextSync] if extension_option is valid
  

**Examples**:

    ```python
    # With extensions using ExtensionOption
    from agentbay.extension import ExtensionOption

    ext_option = ExtensionOption(
        context_id="my_extensions",
        extension_ids=["ext1", "ext2"]
    )

    browser_context = BrowserContext(
        context_id="browser_session",
        auto_upload=True,
        extension_option=ext_option
    )

    # Without extensions (minimal configuration)
    browser_context = BrowserContext(
        context_id="browser_session",
        auto_upload=True
    )
    # extension_context_syncs will be None
    ```

### get\_extension\_context\_syncs

```python
def get_extension_context_syncs() -> List[ContextSync]
```

Get context syncs for extensions.

**Returns**:

    List[ContextSync]: Context sync configurations for extensions.
  Returns empty list if no extensions configured.

### get\_fingerprint\_context\_sync

```python
def get_fingerprint_context_sync() -> Optional[ContextSync]
```

Get context sync for fingerprint.

**Returns**:

    Optional[ContextSync]: Context sync configurations for fingerprint.
  Returns None if fingerprint configuration is invalid.

## CreateSessionParams

```python
class CreateSessionParams()
```

Parameters for creating a new session in the AgentBay cloud environment.

**Attributes**:

- `labels` _Optional[Dict[str, str]]_ - Custom labels for the Session. These can be
  used for organizing and filtering sessions.
- `image_id` _Optional[str]_ - ID of the image to use for the session.
- `context_syncs` _Optional[List[ContextSync]]_ - List of context synchronization
  configurations that define how contexts should be synchronized and mounted.
- `browser_context` _Optional[BrowserContext]_ - Optional configuration for browser data synchronization.
- `is_vpc` _Optional[bool]_ - Whether to create a VPC-based session. Defaults to False.
- `policy_id` _Optional[str]_ - Policy id to apply when creating the session.
- `enable_browser_replay` _Optional[bool]_ - Whether to enable browser recording for the session. It is enabled by default, so if enable_browser_replay is False, set enable_record to False
- `extra_configs` _Optional[ExtraConfigs]_ - Advanced configuration parameters for mobile environments.
- `framework` _Optional[str]_ - Framework name for tracking (e.g., "langchain"). Defaults to empty string (direct call).

### \_\_init\_\_

```python
def __init__(self, labels: Optional[Dict[str, str]] = None,
             image_id: Optional[str] = None,
             context_syncs: Optional[List[ContextSync]] = None,
             browser_context: Optional[BrowserContext] = None,
             is_vpc: Optional[bool] = None,
             policy_id: Optional[str] = None,
             enable_browser_replay: Optional[bool] = None,
             extra_configs: Optional[ExtraConfigs] = None,
             framework: Optional[str] = None)
```

Initialize CreateSessionParams.

**Arguments**:

- `labels` _Optional[Dict[str, str]], optional_ - Custom labels for the Session.
  Defaults to None.
- `image_id` _Optional[str], optional_ - ID of the image to use for the session.
  Defaults to None.
- `context_syncs` _Optional[List[ContextSync]], optional_ - List of context
  synchronization configurations. Defaults to None.
- `browser_context` _Optional[BrowserContext], optional_ - Browser context configuration.
  If extension_ids are provided in BrowserContext, extension syncs will be
  automatically added. Defaults to None.
- `is_vpc` _Optional[bool], optional_ - Whether to create a VPC-based session.
  Defaults to False.
- `policy_id` _Optional[str], optional_ - Policy id to apply when creating the session.
  Defaults to None.
- `enable_browser_replay` _Optional[bool], optional_ - Whether to enable browser recording for the session.
  Defaults to False.
- `extra_configs` _Optional[ExtraConfigs], optional_ - Advanced configuration parameters for mobile environments.
  Defaults to None.
- `framework` _Optional[str], optional_ - Framework name for tracking (e.g., "langchain").
  Defaults to None (empty string in tracking, indicating direct call).

## ListSessionParams

```python
class ListSessionParams()
```

Parameters for listing sessions with pagination support.

**Attributes**:

- `max_results` _int_ - Number of results per page.
- `next_token` _str_ - Token for the next page.
- `labels` _Dict[str, str]_ - Labels to filter by.

### \_\_init\_\_

```python
def __init__(self, max_results: int = 10,
             next_token: str = "",
             labels: Optional[Dict[str, str]] = None)
```

Initialize ListSessionParams with default values.

**Arguments**:

- `max_results` _int, optional_ - Number of results per page. Defaults to 10.
- `next_token` _str, optional_ - Token for the next page. Defaults to "".
- `labels` _Optional[Dict[str, str]], optional_ - Labels to filter by.
  Defaults to None.

## See Also

- [Synchronous vs Asynchronous API](../../../docs/guides/async-programming/sync-vs-async.md)

---

*Documentation generated automatically from source code using pydoc-markdown.*
