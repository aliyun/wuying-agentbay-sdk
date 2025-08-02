# OSS Integration Tutorial

AgentBay SDK provides integration with Alibaba Cloud Object Storage Service (OSS), allowing you to upload and download files between the cloud environment and OSS buckets. This tutorial will guide you through OSS operations.

## Overview

The OSS module allows you to:

- Initialize OSS environment with credentials
- Upload files to OSS buckets
- Download files from OSS buckets
- Upload and download files anonymously

## Setting Up OSS Environment

Before performing OSS operations, you need to initialize the OSS environment with your credentials.

### Initializing OSS Environment

```python
from agentbay import AgentBay

# Initialize the SDK and create a session
agent_bay = AgentBay(api_key="your_api_key")
session_result = agent_bay.create()
session = session_result.session

# Initialize OSS environment with credentials
access_key_id = "your_access_key_id"
access_key_secret = "your_access_key_secret"
endpoint = "oss-cn-hangzhou.aliyuncs.com"  # Use your region's endpoint
region = "cn-hangzhou"  # Use your region

result = session.oss.env_init(
    access_key_id=access_key_id,
    access_key_secret=access_key_secret,
    endpoint=endpoint,
    region=region
)

if result.success:
    print("OSS environment initialized successfully")
else:
    print(f"Failed to initialize OSS environment: {result.error_message}")

# Delete the session when done
agent_bay.delete(session)
```

```typescript
import { AgentBay } from 'wuying-agentbay-sdk';

// Initialize the SDK
const agentBay = new AgentBay({ apiKey: 'your_api_key' });

async function initOSSEnvironment() {
  try {
    // Create a session
    const createResponse = await agentBay.create();
    const session = createResponse.session;
    
    // Initialize OSS environment with credentials
    const accessKeyId = 'your_access_key_id';
    const accessKeySecret = 'your_access_key_secret';
    const endpoint = 'oss-cn-hangzhou.aliyuncs.com';  // Use your region's endpoint
    const region = 'cn-hangzhou';  // Use your region
    
    const result = await session.oss.envInit(
      accessKeyId,
      accessKeySecret,
      null,  // securityToken is optional
      endpoint,
      region
    );
    
    if (result.success) {
      console.log('OSS environment initialized successfully');
    } else {
      console.log(`Failed to initialize OSS environment: ${result.errorMessage}`);
    }
    
    // Delete the session
    await agentBay.delete(session);
  } catch (error) {
    console.error('Error:', error);
  }
}

initOSSEnvironment();
```

```go
package main

import (
	"fmt"
	"os"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

func main() {
  // Initialize the SDK
  client, err := agentbay.NewAgentBay("your_api_key")
  if err != nil {
    fmt.Printf("Error initializing AgentBay client: %v\n", err)
    os.Exit(1)
  }

  // Create a session
  result, err := client.Create(nil)
  if err != nil {
    fmt.Printf("Error creating session: %v\n", err)
    os.Exit(1)
  }

  session := result.Session

  // Initialize OSS environment with credentials
  accessKeyId := "your_access_key_id"
  accessKeySecret := "your_access_key_secret"
  endpoint := "oss-cn-hangzhou.aliyuncs.com"  // Use your region's endpoint
  region := "cn-hangzhou"  // Use your region
  securityToken := ""  // Optional

  ossResult, err := session.OSS.EnvInit(accessKeyId, accessKeySecret, securityToken, endpoint, region)
  if err != nil {
    fmt.Printf("Error initializing OSS environment: %v\n", err)
    os.Exit(1)
  }
  fmt.Printf("OSS environment initialized successfully, result: %s\n", ossResult.Result)

  // Delete the session
  _, err = client.Delete(session)
  if err != nil {
    fmt.Printf("Error deleting session: %v\n", err)
    os.Exit(1)
  }
}
```

## Uploading Files to OSS

### Uploading a File to OSS Bucket

The following example demonstrates how to upload a file from the cloud environment to an OSS bucket:

```python
from agentbay import AgentBay

# Initialize the SDK and create a session
agent_bay = AgentBay(api_key="your_api_key")
session_result = agent_bay.create()
session = session_result.session

# Initialize OSS environment (as shown in the previous example)
# ...

# Create a test file to upload
file_path = "/tmp/test_upload.txt"
file_content = "This is a test file for OSS upload."
session.filesystem.write_file(file_path, file_content)

# Upload the file to OSS
bucket_name = "your-bucket-name"
object_key = "test_upload.txt"

upload_result = session.oss.upload(
    bucket=bucket_name,
    object=object_key,
    path=file_path
)

if upload_result.success:
    print(f"File uploaded successfully to OSS. URL: {upload_result.content}")
else:
    print(f"Failed to upload file: {upload_result.error_message}")

# Delete the session when done
agent_bay.delete(session)
```

```typescript
import { AgentBay } from 'wuying-agentbay-sdk';

// Initialize the SDK
const agentBay = new AgentBay({ apiKey: 'your_api_key' });

async function uploadFileToOSS() {
  try {
    // Create a session
    const createResponse = await agentBay.create();
    const session = createResponse.session;
    
    // Initialize OSS environment (as shown in the previous example)
    // ...
    
    // Create a test file to upload
    const filePath = '/tmp/test_upload.txt';
    const fileContent = 'This is a test file for OSS upload.';
    await session.fileSystem.writeFile(filePath, fileContent);
    
    // Upload the file to OSS
    const bucketName = 'your-bucket-name';
    const objectKey = 'test_upload.txt';
    
    const uploadResult = await session.oss.upload(
      bucketName,
      objectKey,
      filePath
    );
    
    if (uploadResult.success) {
      console.log(`File uploaded successfully to OSS. URL: ${uploadResult.content}`);
    } else {
      console.log(`Failed to upload file: ${uploadResult.errorMessage}`);
    }
    
    // Delete the session
    await agentBay.delete(session);
  } catch (error) {
    console.error('Error:', error);
  }
}

uploadFileToOSS();
```

### Uploading Files Anonymously

You can also upload files to a URL anonymously:

```python
from agentbay import AgentBay

# Initialize the SDK and create a session
agent_bay = AgentBay(api_key="your_api_key")
session_result = agent_bay.create()
session = session_result.session

# Create a test file to upload
file_path = "/tmp/anonymous_upload.txt"
file_content = "This is an anonymous upload test."
session.filesystem.write_file(file_path, file_content)

# Upload the file anonymously
url = "https://example.com/upload-endpoint"  # Use a valid upload URL

upload_result = session.oss.upload_anonymous(
    url=url,
    path=file_path
)

if upload_result.success:
    print(f"File uploaded anonymously. Result: {upload_result.content}")
else:
    print(f"Failed to upload file anonymously: {upload_result.error_message}")

# Delete the session when done
agent_bay.delete(session)
```

## Downloading Files from OSS

### Downloading a File from OSS Bucket

The following example demonstrates how to download a file from an OSS bucket to the cloud environment:

```python
from agentbay import AgentBay

# Initialize the SDK and create a session
agent_bay = AgentBay(api_key="your_api_key")
session_result = agent_bay.create()
session = session_result.session

# Initialize OSS environment (as shown in the previous example)
# ...

# Download a file from OSS
bucket_name = "your-bucket-name"
object_key = "test_upload.txt"  # The object key in the OSS bucket
local_path = "/tmp/downloaded_file.txt"  # Where to save the file

download_result = session.oss.download(
    bucket=bucket_name,
    object=object_key,
    path=local_path
)

if download_result.success:
    print(f"File downloaded successfully to: {download_result.content}")
    
    # Verify the file content
    file_result = session.filesystem.read_file(local_path)
    if file_result.success:
        print(f"Downloaded file content: {file_result.content}")
else:
    print(f"Failed to download file: {download_result.error_message}")

# Delete the session when done
agent_bay.delete(session)
```

```typescript
import { AgentBay } from 'wuying-agentbay-sdk';

// Initialize the SDK
const agentBay = new AgentBay({ apiKey: 'your_api_key' });

async function downloadFileFromOSS() {
  try {
    // Create a session
    const createResponse = await agentBay.create();
    const session = createResponse.session;
    
    // Initialize OSS environment (as shown in the previous example)
    // ...
    
    // Download a file from OSS
    const bucketName = 'your-bucket-name';
    const objectKey = 'test_upload.txt';  // The object key in the OSS bucket
    const localPath = '/tmp/downloaded_file.txt';  // Where to save the file
    
    const downloadResult = await session.oss.download(
      bucketName,
      objectKey,
      localPath
    );
    
    if (downloadResult.success) {
      console.log(`File downloaded successfully to: ${downloadResult.content}`);
      
      // Verify the file content
      const fileResult = await session.fileSystem.readFile(localPath);
      console.log(`Downloaded file content: ${fileResult.content}`);
    } else {
      console.log(`Failed to download file: ${downloadResult.errorMessage}`);
    }
    
    // Delete the session
    await agentBay.delete(session);
  } catch (error) {
    console.error('Error:', error);
  }
}

downloadFileFromOSS();
```

### Downloading Files Anonymously

You can also download files from a URL anonymously:

```python
from agentbay import AgentBay

# Initialize the SDK and create a session
agent_bay = AgentBay(api_key="your_api_key")
session_result = agent_bay.create()
session = session_result.session

# Download a file anonymously from a URL
url = "https://example.com/sample.txt"  # Use a valid download URL
local_path = "/tmp/anonymous_download.txt"

download_result = session.oss.download_anonymous(
    url=url,
    path=local_path
)

if download_result.success:
    print(f"File downloaded anonymously to: {download_result.content}")
    
    # Verify the file content
    file_result = session.filesystem.read_file(local_path)
    if file_result.success:
        print(f"Downloaded file content: {file_result.content}")
else:
    print(f"Failed to download file anonymously: {download_result.error_message}")

# Delete the session when done
agent_bay.delete(session)
```

## OSS Client Creation

For more advanced OSS operations, you can create a dedicated OSS client:

```python
# Create an OSS client
client_result = session.oss.create_client(
    access_key_id=access_key_id,
    access_key_secret=access_key_secret,
    endpoint=endpoint,
    region=region
)

if client_result.success:
    print("OSS client created successfully")
else:
    print(f"Failed to create OSS client: {client_result.error_message}")
```

## Best Practices

1. **Credential Security**: Always handle OSS credentials securely. Don't hardcode them in your application.
2. **Error Handling**: Always check the return result of OSS operations to ensure they completed successfully.
3. **Resource Management**: After completing operations, make sure to delete temporary files and sessions that are no longer needed.
4. **Path Handling**: Use absolute paths for local files to avoid confusion with relative paths.
5. **Large Files**: For large files, consider implementing chunking or progress tracking.

## Related Resources

- [API Reference: OSS (Python)](../api-reference/python/oss.md)
- [API Reference: OSS (TypeScript)](../api-reference/typescript/oss.md)
- [API Reference: OSS (Golang)](../api-reference/golang/oss.md)
- [Examples: OSS Management](../examples/python/oss_management) 