# MobileSimulate API Reference

## MobileSimulateService

```python
class MobileSimulateService()
```

Provides methods to manage persistent mobile dev info and sync to the mobile device.

### \_\_init\_\_

```python
def __init__(self, agent_bay: "AgentBay")
```

Initialize the MobileSimulateService.

**Arguments**:

- `agent_bay` _AgentBay_ - The AgentBay instance.

### set\_simulate\_enable

```python
def set_simulate_enable(enable: bool)
```

Set the simulate enable flag.

**Arguments**:

- `enable` _bool_ - The simulate feature enable flag.

### get\_simulate\_enable

```python
def get_simulate_enable() -> bool
```

Get the simulate enable flag.

**Returns**:

    bool: The simulate feature enable flag.

### set\_simulate\_mode

```python
def set_simulate_mode(mode: MobileSimulateMode)
```

Set the simulate mode.

**Arguments**:

- `mode` _MobileSimulateMode_ - The simulate mode.
  - PropertiesOnly: Simulate only device properties.
  - SensorsOnly: Simulate only device sensors.
  - PackagesOnly: Simulate only installed packages.
  - ServicesOnly: Simulate only system services.
  - All: Simulate all aspects of the device.

### get\_simulate\_mode

```python
def get_simulate_mode() -> MobileSimulateMode
```

Get the simulate mode.

**Returns**:

    MobileSimulateMode: The simulate mode.

### set\_simulate\_context\_id

```python
def set_simulate_context_id(context_id: str)
```

Set a previously saved simulate context id. Please make sure the context id is provided by MobileSimulateService
but not user side created context.

**Arguments**:

- `context_id` _str_ - The context ID of the previously saved mobile simulate context.

### get\_simulate\_context\_id

```python
def get_simulate_context_id() -> str
```

Get the simulate context id.

**Returns**:

    str: The context ID of the mobile simulate context.

### get\_simulate\_config

```python
def get_simulate_config() -> MobileSimulateConfig
```

Get the simulate config.

**Returns**:

    MobileSimulateConfig: The simulate config.
  - simulate (bool): The simulate feature enable flag.
  - simulate_path (str): The path of the mobile dev info file.
  - simulate_mode (MobileSimulateMode): The simulate mode.
  - simulated_context_id (str): The context ID of the mobile info.
  Defaults to "".

### has\_mobile\_info

```python
def has_mobile_info(context_sync: "ContextSync") -> bool
```

Check if the mobile dev info file exists in one context sync. (Only for user provided context sync)

**Arguments**:

- `context_sync` _ContextSync_ - The context sync to check.
  

**Returns**:

    bool: True if the mobile dev info file exists, False otherwise.
  

**Raises**:

    ValueError: If context_sync is not provided or context_sync.context_id or context_sync.path is not provided.
  

**Notes**:

  This method can only used when mobile simulate context sync is managed by user side. For internal mobile simulate
  context sync, this method will not work.

### upload\_mobile\_info

```python
def upload_mobile_info(
    mobile_dev_info_content: str,
    context_sync: Optional["ContextSync"] = None
) -> MobileSimulateUploadResult
```

Upload the mobile simulate dev info.

**Arguments**:

- `mobile_dev_info_content` _str_ - The mobile simulate dev info content to upload.
- `context_sync` _ContextSync_ - Optional
  - If not provided, a new context sync will be created for the mobile simulate service and this context id will
  return by the MobileSimulateUploadResult. User can use this context id to do persistent mobile simulate across sessions.
  - If provided, the mobile simulate dev info will be uploaded to the context sync in a specific path.
  

**Returns**:

    MobileSimulateUploadResult: The result of the upload operation.
  - success (bool): Whether the operation was successful.
  - mobile_simulate_context_id (str): The context ID of the mobile info.
  Defaults to "".
  - error_message (str): The error message if the operation failed.
  Defaults to "".
  

**Raises**:

    ValueError: If mobile_dev_info_content is not provided or not a valid JSON string.
    ValueError: If context_sync is provided but context_sync.context_id is missing.
  

**Notes**:

  If context_sync is not provided, a new context sync will be created for the mobile simulate.
  If context_sync is provided, the mobile simulate dev info will be uploaded to the context sync.
  If the mobile simulate dev info already exists in the context sync, the context sync will be updated.
  If the mobile simulate dev info does not exist in the context sync, the context sync will be created.
  If the upload operation fails, the error message will be returned.

## See Also

- [Synchronous vs Asynchronous API](../../../docs/guides/async-programming/sync-vs-async.md)

---

*Documentation generated automatically from source code using pydoc-markdown.*
