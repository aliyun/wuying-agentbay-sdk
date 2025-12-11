# Cross-Platform Data Persistence

This guide explains how to use the MappingPolicy feature to enable cross-platform data persistence, allowing context data created on one operating system to be accessible on another.

## Overview

By default, context data persistence is tied to the operating system where it was created. For example, data created in a Windows session (at `c:\Users\Administrator\Downloads`) can only be reused in other Windows sessions at the same path.

The **MappingPolicy** feature solves this limitation by allowing you to map paths from one operating system to another, enabling true cross-platform data persistence.

## Use Case

Consider this scenario:

1. You create a session on Windows and save files to `c:\Users\Administrator\Downloads`
2. The files are persisted to a context
3. Later, you create a Linux session and want to access those same files at `/home/wuying/下载`

Without MappingPolicy, this wouldn't work because the paths are OS-specific. With MappingPolicy, you can map the Windows path to the Linux path, making the data accessible across platforms.

## How It Works

When you create a context sync configuration with a MappingPolicy:

1. The `path` in MappingPolicy specifies the original OS path where data was stored
2. The `path` in ContextSync specifies where you want to access that data in the current session
3. The system automatically maps between these paths, making cross-platform access seamless

## Implementation

### Golang

```go
package main

import (
    "github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

func main() {
    // Initialize AgentBay client
    ab, err := agentbay.NewAgentBay("your-api-key")
    if err != nil {
        panic(err)
    }

    // Get or create a context
    contextResult, err := ab.Context.Get("my-cross-platform-context", true)
    if err != nil {
        panic(err)
    }
    context := contextResult.Context

    // Define the original Windows path and target Linux path
    windowsPath := "c:\\Users\\Administrator\\Downloads"
    linuxPath := "/home/wuying/下载"

    // Create mapping policy with the original Windows path
    mappingPolicy := &agentbay.MappingPolicy{
        Path: windowsPath,
    }

    // Create sync policy with mapping policy
    syncPolicy := &agentbay.SyncPolicy{
        UploadPolicy:   agentbay.NewUploadPolicy(),
        DownloadPolicy: agentbay.NewDownloadPolicy(),
        DeletePolicy:   agentbay.NewDeletePolicy(),
        ExtractPolicy:  agentbay.NewExtractPolicy(),
        MappingPolicy:  mappingPolicy,
    }

    // Create session with context sync
    sessionParams := agentbay.NewCreateSessionParams()
    sessionParams.AddContextSync(context.ID, linuxPath, syncPolicy)
    sessionParams.WithImageId("linux_latest")

    // Create session
    sessionResult, err := ab.Create(sessionParams)
    if err != nil {
        panic(err)
    }

    session := sessionResult.Session
    // Now you can access Windows files at /home/wuying/下载 in Linux
}
```

### Python

```python
from agentbay import (
    AgentBay,
    MappingPolicy,
    SyncPolicy,
    UploadPolicy,
    DownloadPolicy,
    DeletePolicy,
    ExtractPolicy,
    ContextSync,
    CreateSessionParams,
)

# Initialize AgentBay client
ab = AgentBay("your-api-key")

# Get or create a context (use create=True to auto-create)
context_result = ab.context.get(name="my-cross-platform-context", create=True)
context = context_result.context

# Define the original Windows path and target Linux path
windows_path = r"c:\Users\Administrator\Downloads"
linux_path = "/home/wuying/下载"

# Create mapping policy with the original Windows path
mapping_policy = MappingPolicy(path=windows_path)

# Create sync policy with mapping policy
sync_policy = SyncPolicy(
    upload_policy=UploadPolicy(),
    download_policy=DownloadPolicy(),
    delete_policy=DeletePolicy(),
    extract_policy=ExtractPolicy(),
    mapping_policy=mapping_policy,
)

# Build context sync config
context_sync = ContextSync.new(context.id, linux_path, sync_policy)

# Create session with context sync and target image
session_params = CreateSessionParams(
    image_id="linux_latest",
    context_syncs=[context_sync],
)

# Create session
session_result = ab.create(session_params)
session = session_result.session
# Now you can access Windows files at /home/wuying/下载 in Linux
```

### TypeScript

```typescript
import { AgentBay, CreateSessionParams } from "wuying-agentbay-sdk";
import {
  MappingPolicy,
  SyncPolicy,
  newUploadPolicy,
  newDownloadPolicy,
  newDeletePolicy,
  newExtractPolicy,
} from "wuying-agentbay-sdk";

// Initialize AgentBay client
const ab = new AgentBay({ apiKey: "your-api-key" });

// Get or create a context
const contextResult = await ab.context.get("my-cross-platform-context", true);
const context = contextResult.context!;

// Define the original Windows path and target Linux path
const windowsPath = "c:\\Users\\Administrator\\Downloads";
const linuxPath = "/home/wuying/下载";

// Create mapping policy with the original Windows path
const mappingPolicy: MappingPolicy = {
  path: windowsPath,
};

// Create sync policy with mapping policy
const syncPolicy: SyncPolicy = {
  uploadPolicy: newUploadPolicy(),
  downloadPolicy: newDownloadPolicy(),
  deletePolicy: newDeletePolicy(),
  extractPolicy: newExtractPolicy(),
  mappingPolicy: mappingPolicy,
};

// Create session with context sync
const sessionParams = new CreateSessionParams();
sessionParams.addContextSync(context.id, linuxPath, syncPolicy);
sessionParams.withImageId("linux_latest");

// Create session
const sessionResult = await ab.create(sessionParams);
const session = sessionResult.session!;
// Now you can access Windows files at /home/wuying/下载 in Linux
```

## Common Scenarios

### Windows to Linux

```
Original: c:\Users\Administrator\Downloads
Target:   /home/wuying/下载
```

### Linux to Windows

```
Original: /home/wuying/下载
Target:   c:\Users\Administrator\Downloads
```

### macOS to Linux

```
Original: /Users/username/Downloads
Target:   /home/wuying/下载
```

## Best Practices

1. **Consistent Context IDs**: Use the same context ID across sessions to ensure data continuity
2. **Path Validation**: Ensure target paths exist or can be created in the new environment
3. **Character Encoding**: Be aware of path character encoding differences between operating systems
4. **Testing**: Test cross-platform scenarios in your development environment before production use

## Important Notes

- The MappingPolicy `path` should contain the original OS path where data was first stored
- The ContextSync `path` should contain where you want to access the data in the current session
- Path mapping is handled automatically by the system
- All other sync policies (upload, download, delete, extract) work the same way with MappingPolicy

## Related Resources

- [Data Persistence Guide](../basics/data-persistence.md)
- [Session Management](../basics/session-management.md)

