# OSS API Reference

The OSS (Object Storage Service) module provides functionality for interacting with cloud storage services.

## Go

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
func (o *Oss) Upload(bucket, object, path string) (string, error)
```

Uploads a local file or directory to OSS.

**Parameters:**
- `bucket`: OSS bucket name.
- `object`: Object key in OSS.
- `path`: Local file or directory path to upload.

**Returns:**
- `string`: The result of the upload operation.
- `error`: An error if the operation fails.

### Anonymous Uploading

```go
func (o *Oss) UploadAnonymous(url, path string) (string, error)
```

Uploads a local file or directory to a URL anonymously.

**Parameters:**
- `url`: The HTTP/HTTPS URL to upload the file to.
- `path`: Local file or directory path to upload.

**Returns:**
- `string`: The result of the upload operation.
- `error`: An error if the operation fails.

### Downloading Files

```go
func (o *Oss) Download(bucket, object, path string) (string, error)
```

Downloads an object from OSS to a local file.

**Parameters:**
- `bucket`: OSS bucket name.
- `object`: Object key in OSS.
- `path`: Local path to save the downloaded file.

**Returns:**
- `string`: The result of the download operation.
- `error`: An error if the operation fails.

### Anonymous Downloading

```go
func (o *Oss) DownloadAnonymous(url, path string) (string, error)
```

Downloads a file from a URL anonymously to a local file.

**Parameters:**
- `url`: The HTTP/HTTPS URL to download the file from.
- `path`: The full local file path to save the downloaded file.

**Returns:**
- `string`: The result of the download operation.
- `error`: An error if the operation fails.

## Python

### Creating an OSS Client

```python
def env_init(self, access_key_id: str, access_key_secret: str,
                 endpoint: Optional[str] = None, region: Optional[str] = None) -> str
```

Creates an OSS client with the provided credentials.

**Parameters:**
- `access_key_id`: The Access Key ID for OSS authentication.
- `access_key_secret`: The Access Key Secret for OSS authentication.
- `endpoint`: The OSS service endpoint. If not specified, the default is used.
- `region`: The OSS region. If not specified, the default is used.

**Returns:**
- `str`: The result of the client creation operation.

**Raises:**
- `OssError`: If the client creation fails.

### Uploading Files

```python
def upload(self, bucket: str, object: str, path: str) -> str
```

Uploads a local file or directory to OSS.

**Parameters:**
- `bucket`: OSS bucket name.
- `object`: Object key in OSS.
- `path`: Local file or directory path to upload.

**Returns:**
- `str`: The result of the upload operation.

**Raises:**
- `OssError`: If the upload fails.

### Anonymous Uploading

```python
def upload_anonymous(self, url: str, path: str) -> str
```

Uploads a local file or directory to a URL anonymously.

**Parameters:**
- `url`: The HTTP/HTTPS URL to upload the file to.
- `path`: Local file or directory path to upload.

**Returns:**
- `str`: The result of the upload operation.

**Raises:**
- `OssError`: If the upload fails.

### Downloading Files

```python
def download(self, bucket: str, object: str, path: str) -> str
```

Downloads an object from OSS to a local file.

**Parameters:**
- `bucket`: OSS bucket name.
- `object`: Object key in OSS.
- `path`: Local path to save the downloaded file.

**Returns:**
- `str`: The result of the download operation.

**Raises:**
- `OssError`: If the download fails.

### Anonymous Downloading

```python
def download_anonymous(self, url: str, path: str) -> str
```

Downloads a file from a URL anonymously to a local file.

**Parameters:**
- `url`: The HTTP/HTTPS URL to download the file from.
- `path`: The full local file path to save the downloaded file.

**Returns:**
- `str`: The result of the download operation.

**Raises:**
- `OssError`: If the download fails.

## TypeScript

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
