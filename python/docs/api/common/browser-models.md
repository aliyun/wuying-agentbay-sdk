# Browser Models API Reference

> **💡 Async Version**: This documentation covers the synchronous API. For async/await support, see [`AsyncBrowser`](../async/async-browser.md) which provides the same functionality with async methods.

## 🌐 Related Tutorial

- [Browser Use Guide](../../../../docs/guides/browser-use/README.md) - Complete guide to browser automation

## Overview

The Browser module provides comprehensive browser automation capabilities including navigation, element interaction,
screenshot capture, and content extraction. It enables automated testing and web scraping workflows.


## Requirements

- Requires `browser_latest` image for browser automation features



Browser module data models.

## BrowserFingerprintContext

```python
class BrowserFingerprintContext()
```

Browser fingerprint context configuration.

### \_\_init\_\_

```python
def __init__(self, fingerprint_context_id: str)
```

Initialize FingerprintContext with context id.

**Arguments**:

- `fingerprint_context_id` _str_ - ID of the fingerprint context for browser fingerprint.
  

**Raises**:

    ValueError: If fingerprint_context_id is empty.

## BrowserProxy

```python
class BrowserProxy()
```

Browser proxy configuration.
Supports two types of proxy: custom proxy, wuying proxy.
wuying proxy support two strategies: restricted and polling.

### \_\_init\_\_

```python
def __init__(self, proxy_type: Literal["custom", "wuying"],
             server: Optional[str] = None,
             username: Optional[str] = None,
             password: Optional[str] = None,
             strategy: Optional[Literal["restricted", "polling"]] = None,
             pollsize: int = 10)
```

Initialize a BrowserProxy.

**Arguments**:

    proxy_type: Type of proxy - "custom" or "wuying"
    server: Proxy server address (required for custom type)
    username: Proxy username (optional for custom type)
    password: Proxy password (optional for custom type)
    strategy: Strategy for wuying support "restricted" and "polling"
    pollsize: Pool size (optional for proxy_type wuying and strategy polling)
  
  example:
  # custom proxy
    proxy_type: custom
    server: "127.0.0.1:9090"
    username: "username"
    password: "password"
  
  # wuying proxy with polling strategy
    proxy_type: wuying
    strategy: "polling"
    pollsize: 10
  
  # wuying proxy with restricted strategy
    proxy_type: wuying
    strategy: "restricted"

## BrowserViewport

```python
class BrowserViewport()
```

Browser viewport options.

### \_\_init\_\_

```python
def __init__(self, width: int = 1920, height: int = 1080)
```

## BrowserScreen

```python
class BrowserScreen()
```

Browser screen options.

### \_\_init\_\_

```python
def __init__(self, width: int = 1920, height: int = 1080)
```

## BrowserFingerprint

```python
class BrowserFingerprint()
```

Browser fingerprint options.

### \_\_init\_\_

```python
def __init__(self, devices: list[Literal["desktop", "mobile"]] = None,
             operating_systems: list[Literal["windows", "macos", "linux",
                                             "android", "ios"]] = None,
             locales: list[str] = None)
```

## BrowserOption

```python
class BrowserOption()
```

browser initialization options.

### \_\_init\_\_

```python
def __init__(self, use_stealth: bool = False,
             user_agent: str = None,
             viewport: BrowserViewport = None,
             screen: BrowserScreen = None,
             fingerprint: BrowserFingerprint = None,
             fingerprint_format: Optional["FingerprintFormat"] = None,
             fingerprint_persistent: bool = False,
             solve_captchas: bool = False,
             proxies: Optional[list[BrowserProxy]] = None,
             extension_path: Optional[str] = "/tmp/extensions/",
             cmd_args: Optional[list[str]] = None,
             default_navigate_url: Optional[str] = None,
             browser_type: Optional[Literal["chrome", "chromium"]] = None)
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
- [Session API Reference](../sync/session.md)

---

*Documentation generated automatically from source code using pydoc-markdown.*
