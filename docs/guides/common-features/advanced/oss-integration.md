# OSS Integration

Object Storage Service (OSS) integration enables file upload and download operations between AgentBay sessions and Alibaba Cloud OSS buckets.

## Overview

The OSS module provides:
- **Authenticated Operations**: Upload/download files using OSS STS temporary credentials
- **Anonymous Operations**: Upload/download files using presigned URLs
- **Session-scoped**: All OSS operations are executed within a cloud session environment
- **Security-first**: Only STS temporary credentials are supported for authenticated operations
- **Alternative**: For simple persistence, see [Context](../basics/data-persistence.md) which handles storage automatically.

## Prerequisites

Before using OSS operations, you need:
1. An active AgentBay session (preferably `code_latest` image)
2. Alibaba Cloud OSS temporary credentials from STS (Access Key ID, Secret, and Security Token)
   - See [Alibaba Cloud STS documentation](https://help.aliyun.com/zh/oss/developer-reference/use-temporary-access-credentials-provided-by-sts-to-access-oss) for obtaining temporary credentials
   - **Security Note**: For security reasons, only STS temporary credentials are supported. Permanent credentials are not allowed.
3. An OSS bucket (for authenticated operations)

## Basic Workflow

### 1. Initialize OSS Environment

Before performing any OSS operations, you must initialize the OSS environment with your STS temporary credentials:

```python
from agentbay import AgentBay
from agentbay import CreateSessionParams

agent_bay = AgentBay(api_key="your-agentbay-api-key")

params = CreateSessionParams(image_id="code_latest")
result = agent_bay.create(params)
session = result.session

init_result = session.oss.env_init(
    access_key_id="your-oss-access-key-id",
    access_key_secret="your-oss-access-key-secret",
    securityToken="your-security-token",  # Required when using temporary credentials (STS)
    endpoint="https://oss-cn-hangzhou.aliyuncs.com",  # Optional: defaults to OSS endpoint
    region="cn-hangzhou"  # Optional: defaults to OSS region
)

if init_result.success:
    print(f"OSS environment initialized successfully")
    print(f"Request ID: {init_result.request_id}")
else:
    print(f"Failed to initialize OSS: {init_result.error_message}")
```

**Parameters:**
- `access_key_id` (required): Your Alibaba Cloud Access Key ID from STS
- `access_key_secret` (required): Your Alibaba Cloud Access Key Secret from STS
- `securityToken` (required): Security token from [STS temporary credentials](https://help.aliyun.com/zh/oss/developer-reference/use-temporary-access-credentials-provided-by-sts-to-access-oss). **For security reasons, only temporary credentials are supported.**
- `endpoint` (optional): OSS service endpoint (e.g., `https://oss-cn-hangzhou.aliyuncs.com`)
- `region` (optional): OSS region (e.g., `cn-hangzhou`)

**Returns:**
- `OSSClientResult` with fields:
  - `success` (bool): Whether initialization succeeded
  - `request_id` (str): Unique request identifier
  - `client_config` (dict): OSS client configuration details
  - `error_message` (str): Error description if failed

### 2. Upload Files to OSS

After initialization, upload files from the session to your OSS bucket:

```python
upload_result = session.oss.upload(
    bucket="my-bucket-name",
    object="data/report.pdf",  # Object key in OSS
    path="/home/wuying/report.pdf"  # Local path in session
)

if upload_result.success:
    print(f"File uploaded successfully: {upload_result.content}")
    print(f"Request ID: {upload_result.request_id}")
else:
    print(f"Upload failed: {upload_result.error_message}")
```

**Parameters:**
- `bucket` (str): OSS bucket name
- `object` (str): Object key/path in OSS (e.g., `folder/file.txt`)
- `path` (str): Local file path in the session to upload

**Returns:**
- `OSSUploadResult` with fields:
  - `success` (bool): Whether upload succeeded
  - `request_id` (str): Unique request identifier
  - `content` (str): Upload result message
  - `error_message` (str): Error description if failed

### 3. Download Files from OSS

Download files from your OSS bucket to the session:

```python
download_result = session.oss.download(
    bucket="my-bucket-name",
    object="data/report.pdf",  # Object key in OSS
    path="/home/wuying/downloaded_report.pdf"  # Local path to save
)

if download_result.success:
    print(f"File downloaded successfully: {download_result.content}")
    print(f"Request ID: {download_result.request_id}")
    
    file_info = session.file_system.get_file_info("/home/wuying/downloaded_report.pdf")
    if file_info.success:
        print(f"Downloaded file size: {file_info.size} bytes")
else:
    print(f"Download failed: {download_result.error_message}")
```

**Parameters:**
- `bucket` (str): OSS bucket name
- `object` (str): Object key/path in OSS
- `path` (str): Local file path in the session to save the downloaded file

**Returns:**
- `OSSDownloadResult` with fields:
  - `success` (bool): Whether download succeeded
  - `request_id` (str): Unique request identifier
  - `content` (str): Download result message
  - `error_message` (str): Error description if failed

## Anonymous Operations

Anonymous operations allow uploading/downloading files using presigned URLs or public URLs without requiring OSS credential initialization (`env_init()`).

### Upload Anonymously

Upload a file to a presigned upload URL:

```python
upload_result = session.oss.upload_anonymous(
    url="https://example.com/upload/file.txt",  # Presigned upload URL
    path="/home/wuying/file.txt"  # Local file to upload
)

if upload_result.success:
    print(f"Anonymous upload successful: {upload_result.content}")
else:
    print(f"Anonymous upload failed: {upload_result.error_message}")
```

**Parameters:**
- `url` (str): HTTP/HTTPS URL to upload the file to (e.g., presigned OSS upload URL)
- `path` (str): Local file path in the session

**Returns:** Same as `upload()` - `OSSUploadResult`

### Download Anonymously

Download a file from a public URL or presigned download URL:

```python
download_result = session.oss.download_anonymous(
    url="https://example.com/files/document.pdf",  # Public or presigned URL
    path="/home/wuying/document.pdf"  # Local path to save
)

if download_result.success:
    print(f"Anonymous download successful: {download_result.content}")
else:
    print(f"Anonymous download failed: {download_result.error_message}")
```

**Parameters:**
- `url` (str): HTTP/HTTPS URL to download the file from
- `path` (str): Local file path in the session to save the downloaded file

**Returns:** Same as `download()` - `OSSDownloadResult`

## Complete Example

Here's a complete workflow demonstrating OSS integration:

```python
from agentbay import AgentBay
from agentbay import CreateSessionParams

agent_bay = AgentBay(api_key="your-agentbay-api-key")

params = CreateSessionParams(image_id="code_latest")
result = agent_bay.create(params)

if not result.success:
    print(f"Failed to create session: {result.error_message}")
    exit(1)

session = result.session

try:
    # Initialize OSS with STS temporary credentials
    init_result = session.oss.env_init(
        access_key_id="your-sts-access-key-id",
        access_key_secret="your-sts-access-key-secret",
        securityToken="your-sts-security-token",  # Required for STS credentials
        endpoint="https://oss-cn-hangzhou.aliyuncs.com",
        region="cn-hangzhou"
    )
    
    if not init_result.success:
        print(f"Failed to initialize OSS: {init_result.error_message}")
        exit(1)
    
    print("✓ OSS environment initialized")
    
    session.file_system.write_file(
        path="/home/wuying/data.txt",
        content="Hello from AgentBay!",
        mode="overwrite"
    )
    print("✓ Created local file")
    
    upload_result = session.oss.upload(
        bucket="my-bucket",
        object="agentbay/data.txt",
        path="/home/wuying/data.txt"
    )
    
    if upload_result.success:
        print(f"✓ File uploaded to OSS: {upload_result.content}")
    else:
        print(f"✗ Upload failed: {upload_result.error_message}")
    
    download_result = session.oss.download(
        bucket="my-bucket",
        object="agentbay/data.txt",
        path="/home/wuying/downloaded_data.txt"
    )
    
    if download_result.success:
        print(f"✓ File downloaded from OSS: {download_result.content}")
        
        content_result = session.file_system.read_file("/home/wuying/downloaded_data.txt")
        if content_result.success:
            print(f"✓ File content: {content_result.content}")
    else:
        print(f"✗ Download failed: {download_result.error_message}")

finally:
    agent_bay.delete(session)
    print("✓ Session deleted")
```

## Error Handling

All OSS operations return result objects with `success` field and `error_message` field. Always check these fields:

```python
result = session.oss.upload(bucket="my-bucket", object="file.txt", path="/tmp/file.txt")

if result.success:
    print(f"Success: {result.content}")
else:
    print(f"Error: {result.error_message}")
```

**Common Error Scenarios:**

1. **Authentication Errors**
   ```
   Error: The OSS Access Key Id you provided does not exist in our records.
   ```
   - Solution: Verify your Access Key ID and Secret

2. **Upload/Download Failures**
   - Check error_message field in result object for specific error details
   - Verify bucket name, object key, and file paths
   - Ensure OSS credentials have appropriate permissions
   - For authenticated operations, verify `env_init()` was called successfully

## Use Cases

### 1. Data Backup

Upload session data to OSS for long-term storage:

```python
import time

session.file_system.create_directory("/home/wuying/backup")

json_data = '{"key": "value"}'
session.file_system.write_file("/home/wuying/backup/data.json", json_data, "overwrite")

timestamp = int(time.time())
upload_result = session.oss.upload(
    bucket="backup-bucket",
    object=f"backups/{timestamp}/data.json",
    path="/home/wuying/backup/data.json"
)
```

### 2. Data Processing

Download data from OSS, process it, and upload results:

```python
session.oss.download(
    bucket="input-bucket",
    object="raw/data.csv",
    path="/home/wuying/input.csv"
)

result = session.code.run_code(
    language="python",
    code="""
with open('/home/wuying/input.csv', 'r') as f:
    lines = f.readlines()
    
processed_lines = [line.upper() for line in lines]

with open('/home/wuying/output.csv', 'w') as f:
    f.writelines(processed_lines)
"""
)

session.oss.upload(
    bucket="output-bucket",
    object="processed/data.csv",
    path="/home/wuying/output.csv"
)
```

### 3. File Distribution

Use anonymous download to access public files:

```python
download_result = session.oss.download_anonymous(
    url="https://public-bucket.oss-cn-hangzhou.aliyuncs.com/dataset.zip",
    path="/home/wuying/dataset.zip"
)

session.command.execute_command("unzip /home/wuying/dataset.zip -d /home/wuying/data/")
```

## Best Practices

1. **Use STS Temporary Credentials**: Always use STS temporary credentials with limited validity and minimal permissions
2. **Always Initialize First**: Call `env_init()` with all three required credentials (`access_key_id`, `access_key_secret`, `securityToken`) before any other OSS operations
3. **Handle Errors**: Check `success` field and handle `error_message` appropriately
4. **Use Absolute Paths**: Use absolute paths for file operations (e.g., `/home/wuying/file.txt`)
5. **Secure Credentials**: Never hardcode credentials; use environment variables or secure vaults
6. **Token Refresh**: Monitor STS token expiration and refresh tokens before they expire
7. **Clean Up**: Delete sessions after completing OSS operations to avoid charges
8. **Request IDs**: Log `request_id` from results for debugging and support

## Security Considerations

- **Mandatory Temporary Credentials**: For security reasons, AgentBay OSS integration **only supports STS temporary credentials**. You must provide a valid `securityToken` when calling `env_init()`.
- **Credential Management**: Store STS credentials securely (environment variables, secrets manager). Never hardcode credentials in source code.
- **Credential Lifecycle**: STS tokens have limited validity. Ensure you obtain fresh temporary credentials before they expire. Refer to [Alibaba Cloud STS documentation](https://help.aliyun.com/zh/oss/developer-reference/use-temporary-access-credentials-provided-by-sts-to-access-oss) for details.
- **Minimal Permissions**: Configure STS policies to grant only the minimum required OSS permissions (e.g., read-only for downloads, write-only for uploads)
- **Bucket Permissions**: Use bucket policies to restrict access to specific resources
- **Network Security**: Always use HTTPS endpoints for OSS operations
- **Session Cleanup**: Delete sessions after completing operations to prevent credential leakage

## Limitations

1. **Session Requirement**: OSS operations require an active session
2. **STS Credentials Only**: Only STS temporary credentials are supported; permanent credentials are not allowed
3. **Initialization Required**: `env_init()` must be called with `securityToken` before upload/download operations
4. **Path Restrictions**: File paths must be within the session filesystem
5. **Image Compatibility**: Works best with `code_latest` image

## Related Documentation

- [Session Management](../basics/session-management.md)
- [File Operations](../basics/file-operations.md)
- [Data Persistence](../basics/data-persistence.md)
- [Command Execution](../basics/command-execution.md)
