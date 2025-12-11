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

## BrowserProxy

```python
class BrowserProxy()
```

Browser proxy configuration.
Supports two types of proxy: custom proxy, wuying proxy.
wuying proxy support two strategies: restricted and polling.

## BrowserViewport

```python
class BrowserViewport()
```

Browser viewport options.

## BrowserScreen

```python
class BrowserScreen()
```

Browser screen options.

## BrowserFingerprint

```python
class BrowserFingerprint()
```

Browser fingerprint options.

## BrowserOption

```python
class BrowserOption()
```

browser initialization options.

## Best Practices

1. Wait for page load completion before interacting with elements
2. Use appropriate selectors (CSS, XPath) for reliable element identification
3. Handle navigation timeouts and errors gracefully
4. Take screenshots for debugging and verification
5. Clean up browser resources after automation tasks

## See Also

- [Synchronous vs Asynchronous API](../../../../python/docs/guides/async-programming/sync-vs-async.md)

**Related APIs:**
- [Session API Reference](../sync/session.md)

---

*Documentation generated automatically from source code using pydoc-markdown.*
