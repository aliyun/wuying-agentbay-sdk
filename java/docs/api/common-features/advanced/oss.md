# OSS API Reference

## ☁️ Related Tutorial

- [OSS Integration Guide](../../../../../docs/guides/common-features/advanced/oss-integration.md) - Integrate with Alibaba Cloud OSS for file storage

## Result Types

### OSSClientResult

```java
public class OSSClientResult extends ApiResponse
```

Result of OSS client initialization operations.

**Fields:**
- `success` (boolean): True if operation succeeded
- `data` (String): Client configuration data
- `requestId` (String): Request identifier
- `errorMessage` (String): Error description if failed

### OSSUploadResult

```java
public class OSSUploadResult extends ApiResponse
```

Result of OSS upload operations.

**Fields:**
- `success` (boolean): True if operation succeeded
- `data` (String): Upload result data
- `requestId` (String): Request identifier
- `errorMessage` (String): Error description if failed

### OSSDownloadResult

```java
public class OSSDownloadResult extends ApiResponse
```

Result of OSS download operations.

**Fields:**
- `success` (boolean): True if operation succeeded
- `data` (String): Download result data
- `requestId` (String): Request identifier
- `errorMessage` (String): Error description if failed

## OSS

```java
public class OSS extends BaseService
```

Handles Object Storage Service operations in the AgentBay cloud environment.

### envInit

```java
public OSSClientResult envInit(String accessKeyId, String accessKeySecret, String securityToken, String endpoint, String region)
```

Initialize OSS environment with the provided STS temporary credentials.

**Parameters:**
- `accessKeyId` (String): The Access Key ID from STS temporary credentials
- `accessKeySecret` (String): The Access Key Secret from STS temporary credentials
- `securityToken` (String): Security token from STS temporary credentials. Required for security.
- `endpoint` (String): The OSS service endpoint. If not specified, the default is used.
- `region` (String): The OSS region. If not specified, the default is used.

**Returns:**
- `OSSClientResult`: Result containing client configuration and error message if any

**Example:**

```java
Session session = agentBay.create().getSession();
OSSClientResult result = session.getOss().envInit(
    "stsAccessKeyId",
    "stsAccessKeySecret",
    "stsToken",
    "endpoint",
    "region"
);
```

**Note:** Before calling upload/download operations, you must call this method to initialize the OSS environment.

### upload

```java
public OSSUploadResult upload(String bucket, String object, String path)
```

Upload a local file or directory to OSS.

**Parameters:**
- `bucket` (String): OSS bucket name
- `object` (String): Object key in OSS
- `path` (String): Local file or directory path to upload

**Returns:**
- `OSSUploadResult`: Result containing upload status and error message if any

**Example:**

```java
Session session = agentBay.create().getSession();
session.getOss().envInit("accessKeyId", "accessKeySecret", "token", "endpoint", "region");
OSSUploadResult result = session.getOss().upload("my-bucket", "my-object", "/tmp/file.txt");
```

**Note:** Before calling this API, you must call envInit to initialize the OSS environment.

### download

```java
public OSSDownloadResult download(String bucket, String object, String path)
```

Download an object from OSS to a local file or directory.

**Parameters:**
- `bucket` (String): OSS bucket name
- `object` (String): Object key in OSS
- `path` (String): Local file or directory path to download to

**Returns:**
- `OSSDownloadResult`: Result containing download status and error message if any

**Example:**

```java
Session session = agentBay.create().getSession();
session.getOss().envInit("accessKeyId", "accessKeySecret", "token", "endpoint", "region");
OSSDownloadResult result = session.getOss().download("my-bucket", "my-object", "/tmp/file.txt");
```

**Note:** Before calling this API, you must call envInit to initialize the OSS environment.

### uploadAnonymous

```java
public OSSUploadResult uploadAnonymous(String url, String path)
```

Upload a local file or directory to a URL anonymously.

**Parameters:**
- `url` (String): The HTTP/HTTPS URL to upload the file to
- `path` (String): Local file or directory path to upload

**Returns:**
- `OSSUploadResult`: Result containing upload status and error message if any

**Example:**

```java
Session session = agentBay.create().getSession();
OSSUploadResult result = session.getOss().uploadAnonymous(
    "https://example.com/upload",
    "/tmp/file.txt"
);
```

### downloadAnonymous

```java
public OSSDownloadResult downloadAnonymous(String url, String path)
```

Download a file from a URL anonymously to a local file path.

**Parameters:**
- `url` (String): The HTTP/HTTPS URL to download the file from
- `path` (String): Local file or directory path to download to

**Returns:**
- `OSSDownloadResult`: Result containing download status and error message if any

**Example:**

```java
Session session = agentBay.create().getSession();
OSSDownloadResult result = session.getOss().downloadAnonymous(
    "https://example.com/file.txt",
    "/tmp/file.txt"
);
```

## Related Resources

- [Session API Reference](../basics/session.md)
- [FileSystem API Reference](../basics/filesystem.md)

---

*Documentation for AgentBay Java SDK*

