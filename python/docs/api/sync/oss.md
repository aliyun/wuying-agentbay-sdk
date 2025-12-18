# OSS API Reference

> **💡 Async Version**: This documentation covers the synchronous API. For async/await support, see [`AsyncOss`](../async/async-oss.md) which provides the same functionality with async methods.

## ☁️ Related Tutorial

- [OSS Integration Guide](../../../../docs/guides/common-features/advanced/oss-integration.md) - Integrate with Alibaba Cloud OSS for file storage



## OSSClientResult

```python
class OSSClientResult(ApiResponse)
```

Result of OSS client creation operations.

### \_\_init\_\_

```python
def __init__(self, request_id: str = "",
             success: bool = False,
             client_config: Optional[Dict[str, Any]] = None,
             error_message: str = "")
```

Initialize an OSSClientResult.

**Arguments**:

- `request_id` _str, optional_ - Unique identifier for the API request.
  Defaults to "".
- `success` _bool, optional_ - Whether the operation was successful.
  Defaults to False.
- `client_config` _Dict[str, Any], optional_ - OSS client configuration.
  Defaults to None.
- `error_message` _str, optional_ - Error message if the operation failed.
  Defaults to "".

## OSSUploadResult

```python
class OSSUploadResult(ApiResponse)
```

Result of OSS upload operations.

### \_\_init\_\_

```python
def __init__(self, request_id: str = "",
             success: bool = False,
             content: str = "",
             error_message: str = "")
```

Initialize an OSSUploadResult.

**Arguments**:

- `request_id` _str, optional_ - Unique identifier for the API request.
  Defaults to "".
- `success` _bool, optional_ - Whether the operation was successful.
  Defaults to False.
- `content` _str, optional_ - Result of the upload operation. Defaults to "".
- `error_message` _str, optional_ - Error message if the operation failed.
  Defaults to "".

## OSSDownloadResult

```python
class OSSDownloadResult(ApiResponse)
```

Result of OSS download operations.

### \_\_init\_\_

```python
def __init__(self, request_id: str = "",
             success: bool = False,
             content: str = "",
             error_message: str = "")
```

Initialize an OSSDownloadResult.

**Arguments**:

- `request_id` _str, optional_ - Unique identifier for the API request.
  Defaults to "".
- `success` _bool, optional_ - Whether the operation was successful.
  Defaults to False.
- `content` _string, optional_ - Defaults to "Download success"
- `error_message` _str, optional_ - Error message if the operation failed.
  Defaults to "".

## Oss

```python
class Oss(BaseService)
```

Handles Object Storage Service operations in the AgentBay cloud environment.

### \_\_init\_\_

```python
def __init__(self, session)
```

Initialize an Oss object.

**Arguments**:

    session: The Session instance that this Oss belongs to.

### env\_init

```python
def env_init(access_key_id: str,
             access_key_secret: str,
             security_token: str,
             endpoint: Optional[str] = None,
             region: Optional[str] = None) -> OSSClientResult
```

Create an OSS client with the provided STS temporary credentials.

**Arguments**:

    access_key_id: The Access Key ID from STS temporary credentials.
    access_key_secret: The Access Key Secret from STS temporary credentials.
    security_token: Security token from STS temporary credentials. Required for security.
    endpoint: The OSS service endpoint. If not specified, the default is used.
    region: The OSS region. If not specified, the default is used.
  

**Returns**:

    OSSClientResult: Result object containing client configuration and error
  message if any.
  

**Example**:

```python
session = agent_bay.create().session
session.oss.env_init(
  access_key_id="your_sts_access_key_id",
  access_key_secret="your_sts_access_key_secret",
  security_token="your_sts_security_token"
)
session.delete()
```

### upload

```python
def upload(bucket: str, object: str, path: str) -> OSSUploadResult
```

Upload a local file or directory to OSS.

Note: Before calling this API, you must first call env_init to initialize
the OSS environment.

**Arguments**:

    bucket: OSS bucket name.
    object: Object key in OSS.
    path: Local file or directory path to upload.
  

**Returns**:

    OSSUploadResult: Result object containing upload result and error message
  if any.
  

**Example**:

```python
session = agent_bay.create().session
session.oss.env_init(
  access_key_id="your_access_key_id",
  access_key_secret="your_access_key_secret",
  security_token="your_sts_security_token",
)
result = session.oss.upload("my-bucket", "file.txt", "/local/path/file.txt")
print(f"Upload result: {result.content}")
session.delete()
```

### upload\_anonymous

```python
def upload_anonymous(url: str, path: str) -> OSSUploadResult
```

Upload a local file or directory to a URL anonymously.

**Arguments**:

    url: The HTTP/HTTPS URL to upload the file to.
    path: Local file or directory path to upload.
  

**Returns**:

    OSSUploadResult: Result object containing upload result and error message
  if any.
  

**Example**:

```python
session = agent_bay.create().session
result = session.oss.upload_anonymous(
  "https://example.com/upload",
  "/local/path/file.txt"
)
print(f"Upload result: {result.content}")
session.delete()
```

### download

```python
def download(bucket: str, object: str, path: str) -> OSSDownloadResult
```

Download an object from OSS to a local file or directory.

Note: Before calling this API, you must first call env_init to initialize
the OSS environment.

**Arguments**:

    bucket: OSS bucket name.
    object: Object key in OSS.
    path: Local file or directory path to download to.
  

**Returns**:

    OSSDownloadResult: Result object containing download status and error
  message if any.
  

**Example**:

```python
session = agent_bay.create().session
session.oss.env_init(
  access_key_id="your_access_key_id",
  access_key_secret="your_access_key_secret",
  security_token="your_sts_security_token",
)
result = session.oss.download("my-bucket", "file.txt", "/local/path/file.txt")
print(f"Download result: {result.content}")
session.delete()
```

### download\_anonymous

```python
def download_anonymous(url: str, path: str) -> OSSDownloadResult
```

Download a file from a URL anonymously to a local file path.

**Arguments**:

    url: The HTTP/HTTPS URL to download the file from.
    path: Local file or directory path to download to.
  

**Returns**:

    OSSDownloadResult: Result object containing download status and error
  message if any.
  

**Example**:

```python
session = agent_bay.create().session
result = session.oss.download_anonymous(
  "https://example.com/file.txt",
  "/local/path/file.txt"
)
print(f"Download result: {result.content}")
session.delete()
```

## See Also

- [Synchronous vs Asynchronous API](../../../docs/guides/async-programming/sync-vs-async.md)

**Related APIs:**
- [Session API Reference](./session.md)
- [FileSystem API Reference](./filesystem.md)

---

*Documentation generated automatically from source code using pydoc-markdown.*
