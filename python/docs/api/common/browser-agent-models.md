# Browser Agent Models API Reference

BrowserAgent module data models.

#### T

```python
T = TypeVar("T", bound=BaseModel)
```

## ActOptions

```python
class ActOptions()
```

Options for configuring the behavior of the act method.

### \_\_init\_\_

```python
def __init__(self, action: str,
             variables: Optional[Dict[str, str]] = None,
             use_vision: Optional[bool] = None,
             timeout: Optional[int] = None)
```

## ActResult

```python
class ActResult()
```

Result of the act method.

### \_\_init\_\_

```python
def __init__(self, success: bool, message: str)
```

## ObserveOptions

```python
class ObserveOptions()
```

Options for configuring the behavior of the observe method.

### \_\_init\_\_

```python
def __init__(self, instruction: str,
             use_vision: Optional[bool] = None,
             selector: Optional[str] = None,
             timeout: Optional[int] = None)
```

## ObserveResult

```python
class ObserveResult()
```

Result of the observe method.

### \_\_init\_\_

```python
def __init__(self, selector: str, description: str, method: str, arguments: dict)
```

## ExtractOptions

```python
class ExtractOptions(Generic[T])
```

Options for configuring the behavior of the extract method.

### \_\_init\_\_

```python
def __init__(self, instruction: str,
             schema: Type[T],
             use_text_extract: Optional[bool] = None,
             use_vision: Optional[bool] = None,
             selector: Optional[str] = None,
             timeout: Optional[int] = None)
```

## See Also

- [Synchronous vs Asynchronous API](../../../docs/guides/async-programming/sync-vs-async.md)

---

*Documentation generated automatically from source code using pydoc-markdown.*
