# OSS API Reference

The OSS (Object Storage Service) module provides functionality for interacting with cloud storage services.

## Go

### Initializing OSS Environment

```go
func (o *Oss) EnvInit(accessKeyId, accessKeySecret, securityToken, endpoint, region string) (*EnvInitResult, error)
```

Creates and initializes OSS environment variables with the specified credentials.

**Parameters:**
- `accessKeyId`: The Access Key ID for OSS authentication.
- `accessKeySecret`: The Access Key Secret for OSS authentication.
- `securityToken`: The security token for OSS authentication.
- `endpoint`: The OSS service endpoint. If not specified, the default is used.
- `region`: The OSS region. If not specified, the default is used.

**Returns:**
- `*EnvInitResult`: A result object containing the initialization result and RequestID.
- `error`: An error if the operation fails.

**EnvInitResult Structure:**
```go
type EnvInitResult struct {
    RequestID string // Unique request identifier for debugging
    Result    string // The result of the environment initialization operation
}
```

### Creating an OSS Client

```go
func (o *Oss) CreateClient(accessKeyId, accessKeySecret, endpoint, region string) (string, error)
```

Creates an OSS client with the provided credentials.

**Parameters:**
- `accessKeyId`: The Access Key ID for OSS authentication.
- `accessKeySecret`: The Access Key Secret for OSS authentication.
- `endpoint`: The OSS service endpoint. If not specified, the default is used.
- `region`: The OSS region. If not specified, the default is used.

**Returns:**
- `string`: The result of the client creation operation.
- `error`: An error if the operation fails.

### Uploading Files

```go
func (o *Oss) Upload(bucket, object, path string) (*UploadResult, error)
```

Uploads a local file or directory to OSS.

**Parameters:**
- `bucket`: OSS bucket name.
- `object`: Object key in OSS.
- `path`: Local file or directory path to upload.

**Returns:**
- `*UploadResult`: A result object containing the upload URL and RequestID.
- `error`: An error if the operation fails.

**UploadResult Structure:**
```go
type UploadResult struct {
    RequestID string // Unique request identifier for debugging
    URL       string // The URL of the uploaded file
}
```

### Anonymous Uploading

```go
func (o *Oss) UploadAnonymous(url, path string) (*UploadResult, error)
```

Uploads a local file or directory to a URL anonymously.

**Parameters:**
- `url`: The HTTP/HTTPS URL to upload the file to.
- `path`: Local file or directory path to upload.

**Returns:**
- `*UploadResult`: A result object containing the upload URL and RequestID.
- `error`: An error if the operation fails.

### Downloading Files

```go
func (o *Oss) Download(bucket, object, path string) (*DownloadResult, error)
```

Downloads an object from OSS to a local file.

**Parameters:**
- `bucket`: OSS bucket name.
- `object`: Object key in OSS.
- `path`: Local path to save the downloaded file.

**Returns:**
- `*DownloadResult`: A result object containing the local file path and RequestID.
- `error`: An error if the operation fails.

**DownloadResult Structure:**
```go
type DownloadResult struct {
    RequestID string // Unique request identifier for debugging
    LocalPath string // The local path where the file was downloaded
}
```

### Anonymous Downloading

```go
func (o *Oss) DownloadAnonymous(url, path string) (*DownloadResult, error)
```

Downloads a file from a URL anonymously to a local file.

**Parameters:**
- `url`: The HTTP/HTTPS URL to download the file from.
- `path`: The full local file path to save the downloaded file.

**Returns:**
- `*DownloadResult`: A result object containing the local file path and RequestID.
- `error`: An error if the operation fails.

## Python

### Initializing OSS Environment

```python
def env_init(self, access_key_id: str, access_key_secret: str, securityToken: Optional[str] = None,
                 endpoint: Optional[str] = None, region: Optional[str] = None) -> OSSClientResult
```

Creates and initializes OSS environment variables with the specified credentials.

**Parameters:**
- `access_key_id`: The Access Key ID for OSS authentication.
- `access_key_secret`: The Access Key Secret for OSS authentication.
- `securityToken`: The security token for OSS authentication. Optional.
- `endpoint`: The OSS service endpoint. If not specified, the default is used.
- `region`: The OSS region. If not specified, the default is used.

**Returns:**
- `OSSClientResult`: Result object containing client configuration, request ID, success status, and error message if any.

**OSSClientResult Structure:**
```python
class OSSClientResult(ApiResponse):
    def __init__(self, request_id: str = "", success: bool = False,
                 client_config: Optional[Dict[str, Any]] = None, error_message: str = "")
```

### Uploading Files

```python
def upload(self, bucket: str, object: str, path: str) -> OSSUploadResult
```

Uploads a local file or directory to OSS.

**Parameters:**
- `bucket`: OSS bucket name.
- `object`: Object key in OSS.
- `path`: Local file or directory path to upload.

**Returns:**
- `OSSUploadResult`: Result object containing upload result, request ID, success status, and error message if any.

**OSSUploadResult Structure:**
```python
class OSSUploadResult(ApiResponse):
    def __init__(self, request_id: str = "", success: bool = False,
                 content: str = "", error_message: str = "")
```

### Anonymous Uploading

```python
def upload_anonymous(self, url: str, path: str) -> OSSUploadResult
```

Uploads a local file or directory to a URL anonymously.

**Parameters:**
- `url`: The HTTP/HTTPS URL to upload the file to.
- `path`: Local file or directory path to upload.

**Returns:**
- `OSSUploadResult`: Result object containing upload result, request ID, success status, and error message if any.

### Downloading Files

```python
def download(self, bucket: str, object: str, path: str) -> OSSDownloadResult
```

Downloads an object from OSS to a local file or directory.

**Parameters:**
- `bucket`: OSS bucket name.
- `object`: Object key in OSS.
- `path`: Local path to save the downloaded file.

**Returns:**
- `OSSDownloadResult`: Result object containing download result, request ID, success status, and error message if any.

**OSSDownloadResult Structure:**
```python
class OSSDownloadResult(ApiResponse):
    def __init__(self, request_id: str = "", success: bool = False,
                 content: str = "", error_message: str = "")
```

### Anonymous Downloading

```python
def download_anonymous(self, url: str, path: str) -> OSSDownloadResult
```

Downloads a file from a URL anonymously to a local file path.

**Parameters:**
- `url`: The HTTP/HTTPS URL to download the file from.
- `path`: Local file or directory path to download to.

**Returns:**
- `OSSDownloadResult`: Result object containing download content, request ID, success status, and error message if any.

## TypeScript

### Initializing OSS Environment

```typescript
async envInit(
  accessKeyId: string,
  accessKeySecret: string,
  securityToken: string,
  endpoint?: string,
  region?: string
): Promise<string>
```

Initializes OSS environment variables with the specified credentials.

**Parameters:**
- `accessKeyId`: The Access Key ID for OSS authentication.
- `accessKeySecret`: The Access Key Secret for OSS authentication.
- `securityToken`: The security token for OSS authentication.
- `endpoint`: The OSS service endpoint. If not specified, the default is used.
- `region`: The OSS region. If not specified, the default is used.

**Returns:**
- `Promise<string>`: The result of the environment initialization operation.

**Throws:**
- `APIError`: If the environment initialization fails.

### Creating an OSS Client

```typescript
async createClient(
  accessKeyId: string,
  accessKeySecret: string,
  endpoint?: string,
  region?: string
): Promise<string>
```

Creates an OSS client with the provided credentials.

**Parameters:**
- `accessKeyId`: The Access Key ID for OSS authentication.
- `accessKeySecret`: The Access Key Secret for OSS authentication.
- `endpoint`: The OSS service endpoint. If not specified, the default is used.
- `region`: The OSS region. If not specified, the default is used.

**Returns:**
- `Promise<string>`: The result of the client creation operation.

**Throws:**
- `APIError`: If the client creation fails.

### Uploading Files

```typescript
async upload(bucket: string, object: string, path: string): Promise<string>
```

Uploads a local file or directory to OSS.

**Parameters:**
- `bucket`: OSS bucket name.
- `object`: Object key in OSS.
- `path`: Local file or directory path to upload.

**Returns:**
- `Promise<string>`: The result of the upload operation.

**Throws:**
- `APIError`: If the upload fails.

### Anonymous Uploading

```typescript
async uploadAnonymous(url: string, path: string): Promise<string>
```

Uploads a local file or directory to a URL anonymously.

**Parameters:**
- `url`: The HTTP/HTTPS URL to upload the file to.
- `path`: Local file or directory path to upload.

**Returns:**
- `Promise<string>`: The result of the upload operation.

**Throws:**
- `APIError`: If the upload fails.

### Downloading Files

```typescript
async download(bucket: string, object: string, path: string): Promise<string>
```

Downloads an object from OSS to a local file.

**Parameters:**
- `bucket`: OSS bucket name.
- `object`: Object key in OSS.
- `path`: Local path to save the downloaded file.

**Returns:**
- `Promise<string>`: The result of the download operation.

**Throws:**
- `APIError`: If the download fails.

### Anonymous Downloading

```typescript
async downloadAnonymous(url: string, path: string): Promise<string>
```

Downloads a file from a URL anonymously to a local file.

**Parameters:**
- `url`: The HTTP/HTTPS URL to download the file from.
- `path`: The full local file path to save the downloaded file.

**Returns:**
- `Promise<string>`: The result of the download operation.

**Throws:**
- `APIError`: If the download fails.
