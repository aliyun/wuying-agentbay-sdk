# AsyncBrowserFingerprint API Reference

## AsyncBrowserFingerprintGenerator

```python
class AsyncBrowserFingerprintGenerator()
```

Browser fingerprint generator class.

**Arguments**:

    headless: Whether to run browser in headless mode.
    use_chrome_channel: Whether to launch via the Chrome channel.

### \_\_init\_\_

```python
def __init__(self, headless: bool = False, use_chrome_channel: bool = True)
```

Initialize the fingerprint generator.

**Arguments**:

    headless: Whether to run browser in headless mode
    use_chrome_channel: Whether to use Chrome channel

### generate\_fingerprint

```python
async def generate_fingerprint() -> Optional[FingerprintFormat]
```

Extract comprehensive browser fingerprint using Playwright.

**Returns**:

    Optional[FingerprintFormat]: FingerprintFormat object containing fingerprint and headers, or None if generation failed
  

**Example**:

generator = AsyncBrowserFingerprintGenerator(headless=True)
fingerprint = await generator.generate_fingerprint()
if fingerprint:
print(fingerprint.headers.get("user-agent"))

### generate\_fingerprint\_to\_file

```python
async def generate_fingerprint_to_file(
        output_filename: str = "fingerprint_output.json") -> bool
```

Extract comprehensive browser fingerprint and save to file.

**Arguments**:

    output_filename: Name of the file to save fingerprint data
  

**Returns**:

    bool: True if fingerprint generation and saving succeeded, False otherwise
  

**Example**:

generator = AsyncBrowserFingerprintGenerator(use_chrome_channel=False)
success = await generator.generate_fingerprint_to_file("browser_fp.json")
print(f"Saved fingerprint: {success}")

## See Also

- [Synchronous vs Asynchronous API](../../../docs/guides/async-programming/sync-vs-async.md)

---

*Documentation generated automatically from source code using pydoc-markdown.*
