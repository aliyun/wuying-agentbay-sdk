# AsyncBrowserAgent API Reference

#### T

```python
T = TypeVar("T", bound=BaseModel)
```

## AsyncBrowserAgent

```python
class AsyncBrowserAgent(BaseService)
```

BrowserAgent handles browser automation and agent logic.

### \_\_init\_\_

```python
def __init__(self, session, browser)
```

### navigate

```python
async def navigate(url: str) -> str
```

Navigates a specific page to the given URL.

**Arguments**:

    url: The URL to navigate to.
  

**Returns**:

  A string indicating the result of the navigation.

### screenshot

```python
async def screenshot(page=None,
                     full_page: bool = True,
                     quality: int = 80,
                     clip: Optional[Dict[str, float]] = None,
                     timeout: Optional[int] = None) -> str
```

Asynchronously takes a screenshot of the specified page.

**Arguments**:

- `page` _Optional[Page]_ - The Playwright Page object to take a screenshot of. If None,
  the agent's currently focused page will be used.
- `full_page` _bool_ - Whether to capture the full scrollable page.
- `quality` _int_ - The quality of the image (0-100), for JPEG format.
- `clip` _Optional[Dict[str, float]]_ - An object specifying the clipping region {x, y, width, height}.
- `timeout` _Optional[int]_ - Custom timeout for the operation in seconds.
  

**Returns**:

    str: A base64 encoded data URL of the screenshot, or an error message.

### close

```python
async def close() -> bool
```

Asynchronously closes the remote browser agent session.
This will terminate the browser process managed by the agent.

### act

```python
async def act(action_input: Union[ObserveResult, ActOptions],
              page=None) -> "ActResult"
```

Asynchronously perform an action on a web page.

**Arguments**:

- `page` _Optional[Page]_ - The Playwright Page object to act on. If None, the agent's
  currently focused page will be used automatically.
- `action_input` _Union[ObserveResult, ActOptions]_ - The action to perform.
  

**Returns**:

    ActResult: The result of the action.

### observe

```python
async def observe(options: ObserveOptions,
                  page=None) -> Tuple[bool, List[ObserveResult]]
```

Asynchronously observe elements or state on a web page.

**Arguments**:

- `page` _Optional[Page]_ - The Playwright Page object to observe. If None, the agent's
  currently focused page will be used.
- `options` _ObserveOptions_ - Options to configure the observation behavior.
  

**Returns**:

  Tuple[bool, List[ObserveResult]]: A tuple containing a success boolean and a list
  of observation results.

### extract

```python
async def extract(options: ExtractOptions, page=None) -> Tuple[bool, T]
```

Asynchronously extract information from a web page.

**Arguments**:

- `page` _Optional[Page]_ - The Playwright Page object to extract from. If None, the agent's
  currently focused page will be used.
- `options` _ExtractOptions_ - Options to configure the extraction, including schema.
  

**Returns**:

  Tuple[bool, T]: A tuple containing a success boolean and the extracted data as a
  Pydantic model instance, or None on failure.

## See Also

- [Synchronous vs Asynchronous API](../../../docs/guides/async-programming/sync-vs-async.md)

---

*Documentation generated automatically from source code using pydoc-markdown.*
