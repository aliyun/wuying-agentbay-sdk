# Browser API Reference

> **💡 Async Version**: This documentation covers the synchronous API. For async/await support, see [`AsyncBrowser`](../async/async-browser.md) which provides the same functionality with async methods.

## 🌐 Related Tutorial

- [Browser Use Guide](../../../../docs/guides/browser-use/README.md) - Complete guide to browser automation

## Overview

The Browser module provides comprehensive browser automation capabilities including navigation, element interaction,
screenshot capture, and content extraction. It enables automated testing and web scraping workflows.


## Requirements

- Requires `browser_latest` image for browser automation features



## Browser

```python
class Browser(BaseService)
```

Browser provides browser-related operations for the session.

### \_\_init\_\_

```python
def __init__(self, session: "Session")
```

### initialize

```python
def initialize(option: Optional["BrowserOption"] = None) -> bool
```

Initialize the browser instance with the given options asynchronously.
Returns True if successful, False otherwise.

**Arguments**:

- `option` _BrowserOption, optional_ - Browser configuration options. If None, default options are used.
  

**Returns**:

    bool: True if initialization was successful, False otherwise.
  

**Example**:

```python
create_result = agent_bay.create()
session = create_result.session
# Use default options
session.browser.initialize()
# Or with specific options
browser_option = BrowserOption(use_stealth=True)
session.browser.initialize(browser_option)
session.delete()
```

### init

```python
def init(option: Optional["BrowserOption"] = None) -> bool
```

Alias for initialize.

### destroy

```python
def destroy()
```

Destroy the browser instance manually.

### screenshot

```python
def screenshot(page, full_page: bool = False, **options) -> bytes
```

Takes a screenshot of the specified page with enhanced options and error handling.

**Arguments**:

- `page` _Page_ - The Playwright Page object to take a screenshot of. This is a required parameter.
- `full_page` _bool_ - Whether to capture the full scrollable page. Defaults to False.
    **options: Additional screenshot options that will override defaults.
  Common options include:
  - type (str): Image type, either 'png' or 'jpeg' (default: 'png')
  - quality (int): Quality of the image, between 0-100 (jpeg only)
  - timeout (int): Maximum time in milliseconds (default: 60000)
  - animations (str): How to handle animations (default: 'disabled')
  - caret (str): How to handle the caret (default: 'hide')
  - scale (str): Scale setting (default: 'css')
  

**Returns**:

    bytes: Screenshot data as bytes.
  

**Raises**:

    BrowserError: If browser is not initialized.
    RuntimeError: If screenshot capture fails.

### get\_endpoint\_url

```python
def get_endpoint_url() -> str
```

Returns the endpoint URL if the browser is initialized, otherwise raises an exception.
When initialized, always fetches the latest CDP url from session.get_link().

**Returns**:

    str: The browser CDP endpoint URL.
  

**Raises**:

    BrowserError: If browser is not initialized or endpoint URL cannot be retrieved.
  

**Example**:

```python
create_result = agent_bay.create()
session = create_result.session
browser_option = BrowserOption()
session.browser.initialize(browser_option)
endpoint_url = session.browser.get_endpoint_url()
print(f"CDP Endpoint: {endpoint_url}")
session.delete()
```

### get\_option

```python
def get_option() -> Optional["BrowserOption"]
```

Returns the current BrowserOption used to initialize the browser, or None if not set.

**Returns**:

    Optional[BrowserOption]: The browser options if initialized, None otherwise.
  

**Example**:

```python
create_result = agent_bay.create()
session = create_result.session
browser_option = BrowserOption(use_stealth=True)
session.browser.initialize(browser_option)
current_options = session.browser.get_option()
print(f"Stealth mode: {current_options.use_stealth}")
session.delete()
```

### is\_initialized

```python
def is_initialized() -> bool
```

Returns True if the browser was initialized, False otherwise.

**Returns**:

    bool: True if browser is initialized, False otherwise.
  

**Example**:

```python
create_result = agent_bay.create()
session = create_result.session
print(f"Initialized: {session.browser.is_initialized()}")
browser_option = BrowserOption()
session.browser.initialize(browser_option)
print(f"Initialized: {session.browser.is_initialized()}")
session.delete()
```

## Best Practices

1. Wait for page load completion before interacting with elements
2. Use appropriate selectors (CSS, XPath) for reliable element identification
3. Handle navigation timeouts and errors gracefully
4. Take screenshots for debugging and verification
5. Clean up browser resources after automation tasks

## See Also

- [Synchronous vs Asynchronous API](../../../docs/guides/async-programming/sync-vs-async.md)

**Related APIs:**
- [Session API Reference](./session.md)

---

*Documentation generated automatically from source code using pydoc-markdown.*
