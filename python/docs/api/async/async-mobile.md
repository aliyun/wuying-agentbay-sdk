# AsyncMobile API Reference

> **💡 Sync Version**: This documentation covers the asynchronous API. For synchronous operations, see [`Mobile`](../sync/mobile.md).
>
> ⚡ **Performance Advantage**: Async API enables concurrent operations with 4-6x performance improvements for parallel tasks.

## 📱 Related Tutorial

- [Mobile Use Guide](../../../../docs/guides/mobile-use/README.md) - Automate mobile applications

## Overview

The Mobile module provides mobile device automation capabilities including touch gestures,
text input, app management, and screenshot capture. It supports Android device automation.


## Requirements

- Requires `mobile_latest` image for mobile automation features



Mobile module for mobile device UI automation and configuration.
Handles touch operations, UI element interactions, application management, screenshot capabilities,
and mobile environment configuration operations.

## AsyncMobile

```python
class AsyncMobile(AsyncBaseService)
```

Handles mobile UI automation operations and configuration in the AgentBay cloud environment.
Provides comprehensive mobile automation capabilities including touch operations,
UI element interactions, application management, screenshot capabilities,
and mobile environment configuration operations.

### \_\_init\_\_

```python
def __init__(self, session)
```

Initialize a Mobile object.

**Arguments**:

    session: The session object that provides access to the AgentBay API.

### tap

```python
async def tap(x: int, y: int) -> BoolResult
```

Taps on the mobile screen at the specified coordinates.

**Arguments**:

- `x` _int_ - X coordinate in pixels.
- `y` _int_ - Y coordinate in pixels.
  

**Returns**:

    BoolResult: Object with success status and error message if any.
  

**Example**:

```python
session = (await agent_bay.create(image="mobile_latest")).session
await session.mobile.tap(500, 800)
await session.delete()
```


**See Also**:

swipe, long_press

### swipe

```python
async def swipe(start_x: int,
                start_y: int,
                end_x: int,
                end_y: int,
                duration_ms: int = 300) -> BoolResult
```

Performs a swipe gesture from one point to another.

**Arguments**:

- `start_x` _int_ - Starting X coordinate.
- `start_y` _int_ - Starting Y coordinate.
- `end_x` _int_ - Ending X coordinate.
- `end_y` _int_ - Ending Y coordinate.
- `duration_ms` _int, optional_ - Duration of the swipe in milliseconds.
  Defaults to 300.
  

**Returns**:

    BoolResult: Result object containing success status and error message if any.
  

**Example**:

```python
session = (await agent_bay.create(image="mobile_latest")).session
await session.mobile.swipe(100, 1000, 100, 200, duration_ms=500)
await session.delete()
```

### input\_text

```python
async def input_text(text: str) -> BoolResult
```

Inputs text into the active field.

**Arguments**:

- `text` _str_ - The text to input.
  

**Returns**:

    BoolResult: Result object containing success status and error message if any.
  

**Example**:

```python
session = (await agent_bay.create(image="mobile_latest")).session
await session.mobile.input_text("Hello Mobile!")
await session.delete()
```

### send\_key

```python
async def send_key(key: int) -> BoolResult
```

Sends a key press event.

**Arguments**:

- `key` _int_ - The key code to send. Supported key codes are:
  - 3 : HOME
  - 4 : BACK
  - 24 : VOLUME UP
  - 25 : VOLUME DOWN
  - 26 : POWER
  - 82 : MENU
  

**Returns**:

    BoolResult: Result object containing success status and error message if any.
  

**Example**:

```python
session = (await agent_bay.create(image="mobile_latest")).session
await session.mobile.send_key(4)  # Press BACK button
await session.delete()
```

### get\_clickable\_ui\_elements

```python
async def get_clickable_ui_elements(
        timeout_ms: int = 2000) -> UIElementListResult
```

Retrieves all clickable UI elements within the specified timeout.

**Arguments**:

- `timeout_ms` _int, optional_ - Timeout in milliseconds. Defaults to 2000.
  

**Returns**:

    UIElementListResult: Result object containing clickable UI elements and
  error message if any.
  
> **Deprecated**
> - Each returned element may include `bounds` from backend which is not stable in type. Use `bounds_rect` (dict with left/top/right/bottom) instead.

  

**Example**:

```python
session = (await agent_bay.create(image="mobile_latest")).session
result = await session.mobile.get_clickable_ui_elements()
print(f"Found {len(result.elements)} clickable elements")
await session.delete()
```

### get\_all\_ui\_elements

```python
async def get_all_ui_elements(timeout_ms: int = 2000) -> UIElementListResult
```

Retrieves all UI elements within the specified timeout.

**Arguments**:

- `timeout_ms` _int, optional_ - Timeout in milliseconds. Defaults to 2000.
  

**Returns**:

    UIElementListResult: Result object containing UI elements and error
  message if any.
  
> **Deprecated**
> - Each returned element may include `bounds` from backend which is not stable in type. Use `bounds_rect` (dict with left/top/right/bottom) instead.

  

**Example**:

```python
session = (await agent_bay.create(image="mobile_latest")).session
result = await session.mobile.get_all_ui_elements()
print(f"Found {len(result.elements)} UI elements")
await session.delete()
```

### get\_installed\_apps

```python
async def get_installed_apps(
        start_menu: bool, desktop: bool,
        ignore_system_apps: bool) -> InstalledAppListResult
```

Retrieves a list of installed applications.

**Arguments**:

- `start_menu` _bool_ - Whether to include start menu applications.
- `desktop` _bool_ - Whether to include desktop applications.
- `ignore_system_apps` _bool_ - Whether to ignore system applications.
  

**Returns**:

    InstalledAppListResult: The result containing the list of installed
  applications.
  

**Example**:

```python
session = (await agent_bay.create(image="mobile_latest")).session
apps = await session.mobile.get_installed_apps(True, False, True)
print(f"Found {len(apps.data)} apps")
await session.delete()
```

### start\_app

```python
async def start_app(start_cmd: str,
                    work_directory: str = "",
                    activity: str = "") -> ProcessListResult
```

Starts an application with the given command, optional working directory and
optional activity.

**Arguments**:

- `start_cmd` _str_ - The command to start the application.
- `work_directory` _str, optional_ - The working directory for the application.
- `activity` _str, optional_ - Activity name to launch (e.g. ".SettingsActivity"
  or "com.package/.Activity"). Defaults to "".
  

**Returns**:

    ProcessListResult: The result containing the list of processes started.
  

**Example**:

```python
session = (await agent_bay.create(image="mobile_latest")).session
processes = await session.mobile.start_app("monkey -p com.android.settings 1")
print(f"Started {len(processes.data)} process(es)")
await session.delete()
```

### stop\_app\_by\_cmd

```python
async def stop_app_by_cmd(stop_cmd: str) -> AppOperationResult
```

Stops an application by stop command.

**Arguments**:

- `stop_cmd` _str_ - The command to stop the application.
  

**Returns**:

    AppOperationResult: The result of the operation.
  

**Example**:

```python
session = (await agent_bay.create(image="mobile_latest")).session
result = await session.mobile.stop_app_by_cmd("com.android.settings")
print(f"Stop successful: {result.success}")
await session.delete()
```

### screenshot

```python
async def screenshot() -> OperationResult
```

Takes a screenshot of the current screen.

**Returns**:

    OperationResult: Result object containing the path to the screenshot
  and error message if any.
  

**Example**:

```python
session = (await agent_bay.create(image="mobile_latest")).session
result = await session.mobile.screenshot()
print(f"Screenshot URL: {result.data}")
await session.delete()
```

### configure

```python
async def configure(mobile_config)
```

Configure mobile settings from MobileExtraConfig.

This method is typically called automatically during session creation when
MobileExtraConfig is provided in CreateSessionParams. It can also be called
manually to reconfigure mobile settings during a session.

**Arguments**:

- `mobile_config` _MobileExtraConfig_ - Mobile configuration object with settings for:
  - lock_resolution (bool): Whether to lock device resolution
  - app_manager_rule (AppManagerRule): App whitelist/blacklist rules
  - hide_navigation_bar (bool): Whether to hide navigation bar
  - uninstall_blacklist (List[str]): Apps protected from uninstallation
  

**Example**:

```python
from agentbay import AsyncAgentBay, CreateSessionParams, MobileExtraConfig
agent_bay = AsyncAgentBay(api_key="your_api_key")
result = await agent_bay.create(CreateSessionParams(image_id="mobile_latest"))
session = result.session
mobile_config = MobileExtraConfig(lock_resolution=True)
await session.mobile.configure(mobile_config)
await agent_bay.delete(session)
```


**Notes**:

- This method is called automatically during session creation if MobileExtraConfig is provided
- Configuration changes are applied immediately
- Resolution lock prevents resolution changes
- App whitelist/blacklist affects app launching permissions
- Uninstall blacklist protects apps from being uninstalled


**See Also**:

set_resolution_lock, set_app_whitelist, set_app_blacklist,
set_navigation_bar_visibility, set_uninstall_blacklist

### set\_resolution\_lock

```python
async def set_resolution_lock(enable: bool)
```

Set display resolution lock for mobile devices.

**Arguments**:

- `enable` _bool_ - True to enable, False to disable.
  

**Example**:

```python
session = (await agent_bay.create(image="mobile_latest")).session
await session.mobile.set_resolution_lock(True)
await session.mobile.set_resolution_lock(False)
await session.delete()
```

### set\_app\_whitelist

```python
async def set_app_whitelist(package_names: List[str])
```

Set application whitelist.

**Arguments**:

- `package_names` _List[str]_ - List of Android package names to whitelist.
  

**Example**:

```python
session = (await agent_bay.create(image="mobile_latest")).session
whitelist = ["com.android.settings", "com.android.chrome"]
await session.mobile.set_app_whitelist(whitelist)
await session.delete()
```


**Notes**:

- Only apps in the whitelist will be allowed to run
- System apps may be affected depending on the configuration
- Whitelist takes precedence over blacklist if both are set

### set\_app\_blacklist

```python
async def set_app_blacklist(package_names: List[str])
```

Set application blacklist.

**Arguments**:

- `package_names` _List[str]_ - List of Android package names to blacklist.
  

**Example**:

```python
session = (await agent_bay.create(image="mobile_latest")).session
blacklist = ["com.example.app1", "com.example.app2"]
await session.mobile.set_app_blacklist(blacklist)
await session.delete()
```


**Notes**:

- Apps in the blacklist will be blocked from running
- Whitelist takes precedence over blacklist if both are set

### set\_navigation\_bar\_visibility

```python
async def set_navigation_bar_visibility(hide: bool)
```

Set navigation bar visibility for mobile devices.

**Arguments**:

- `hide` _bool_ - True to hide navigation bar, False to show navigation bar.
  

**Example**:

```python
session = (await agent_bay.create(image="mobile_latest")).session
await session.mobile.set_navigation_bar_visibility(hide=True)
await session.mobile.set_navigation_bar_visibility(hide=False)
await session.delete()
```


**Notes**:

- Hiding the navigation bar provides a fullscreen experience
- The navigation bar can still be accessed by swiping from the edge

### set\_uninstall\_blacklist

```python
async def set_uninstall_blacklist(package_names: List[str])
```

Set uninstall protection blacklist for mobile devices.

**Arguments**:

- `package_names` _List[str]_ - List of Android package names to protect from uninstallation.
  

**Example**:

```python
session = (await agent_bay.create(image="mobile_latest")).session
protected_apps = ["com.android.settings", "com.android.chrome"]
await session.mobile.set_uninstall_blacklist(protected_apps)
await session.delete()
```


**Notes**:

- Apps in the uninstall blacklist cannot be uninstalled
- This is useful for protecting critical applications
- The protection persists for the session lifetime

### get\_adb\_url

```python
async def get_adb_url(adbkey_pub: str) -> AdbUrlResult
```

Retrieves the ADB connection URL for the mobile environment.

This method is only supported in mobile environments (mobile_latest image).
It uses the provided ADB public key to establish the connection and returns
the ADB connect URL.

**Arguments**:

- `adbkey_pub` _str_ - The ADB public key for connection authentication.
  

**Returns**:

    AdbUrlResult: Result object containing the ADB connection URL
    (format: "adb connect <IP>:<Port>") and request ID.
  Returns error if not in mobile environment.
  

**Raises**:

    SessionError: If the session is not in mobile environment.
  

**Example**:

```python
session = (await agent_bay.create(image="mobile_latest")).session
adbkey_pub = "your_adb_public_key"
adb_result = await session.mobile.get_adb_url(adbkey_pub)
print(f"ADB URL: {adb_result.data}")
await session.delete()
```

## Best Practices

1. Verify element coordinates before tap operations
2. Use appropriate swipe durations for smooth gestures
3. Wait for UI elements to load before interaction
4. Take screenshots for verification and debugging
5. Handle app installation and uninstallation properly
6. Configure app whitelists/blacklists for security

## See Also

- [Synchronous vs Asynchronous API](../../../docs/guides/async-programming/sync-vs-async.md)

**Related APIs:**
- [Session API Reference](./async-session.md)

---

*Documentation generated automatically from source code using pydoc-markdown.*
