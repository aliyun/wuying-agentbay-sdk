# Data Persistence with Contexts

This tutorial explains how to use AgentBay's context synchronization feature to persist data across sessions.

## Overview

AgentBay provides a powerful way to persist data across sessions using contexts. A context is a storage unit that can be attached to sessions, allowing data to be preserved even after a session is terminated.

## Context Synchronization Approaches

AgentBay provides two approaches for context synchronization:

1. **Simple Context Attachment** (Deprecated): Link a session to a persistent context
   ```python
   # Python - DEPRECATED APPROACH
   params = CreateSessionParams(context_id="your_context_id")
   session_result = agent_bay.create(params)
   ```
   Note: This approach is deprecated and will be removed in a future version.

2. **Advanced Context Synchronization** (Recommended): Mount a context at a specific path with synchronization policies
   ```python
   # Python - RECOMMENDED APPROACH
   context_sync = ContextSync.new(
       context_id="your_context_id",
       path="/mnt/persistent",
       policy=SyncPolicy.default()
   )
   params = CreateSessionParams(context_syncs=[context_sync])
   session_result = agent_bay.create(params)
   ```

## Benefits of Advanced Context Synchronization

Context synchronization provides more flexibility by allowing:
- Multiple contexts to be mounted in a single session
- Custom mount paths for each context
- Fine-grained synchronization policies

## Creating and Managing Contexts

Before you can synchronize a context, you need to create it:

### Python

```python
from agentbay import AgentBay

# Initialize the SDK
agent_bay = AgentBay(api_key="your_api_key")

# Create a new context or get an existing one
context_result = agent_bay.context.get("my-persistent-context", create=True)

if context_result.success:
    context = context_result.context
    print(f"Context ID: {context.id}")
```

### TypeScript

```typescript
import { AgentBay } from 'wuying-agentbay-sdk';

// Initialize the SDK
const agentBay = new AgentBay({ apiKey: 'your_api_key' });

async function getOrCreateContext() {
  // Create a new context or get an existing one
  const contextResult = await agentBay.context.get('my-persistent-context', true);
  
  if (contextResult.success) {
    const context = contextResult.context;
    console.log(`Context ID: ${context.id}`);
    return context;
  }
}
```

### Golang

```go
package main

import (
    "fmt"
    "github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

func main() {
    // Initialize the SDK
    client, _ := agentbay.NewAgentBay("your_api_key", nil)
    
    // Create a new context or get an existing one
    contextResult, _ := client.Context.Get("my-persistent-context", true)
    
    fmt.Printf("Context ID: %s\n", contextResult.Context.ID)
}
```

## Using Context Synchronization

Once you have a context, you can synchronize it with a session:

### Python

```python
from agentbay import AgentBay
from agentbay.context_sync import ContextSync, SyncPolicy
from agentbay.session_params import CreateSessionParams

# Initialize the SDK
agent_bay = AgentBay(api_key="your_api_key")

# Get or create a persistent context
context_result = agent_bay.context.get("my-persistent-context", create=True)

if context_result.success:
    # Configure context synchronization
    context_sync = ContextSync.new(
        context_id=context_result.context.id,
        path="/mnt/data",  # Mount path in the session
        policy=SyncPolicy.default()
    )
    
    # Create a session with context synchronization
    params = CreateSessionParams(context_syncs=[context_sync])
    session_result = agent_bay.create(params)
    session = session_result.session
    
    # Now you can access the persistent storage at /mnt/data
    result = session.command.execute("echo 'Hello, World!' > /mnt/data/hello.txt")
    if result.success:
        print("File created in persistent storage")
```

### TypeScript

```typescript
import { AgentBay, ContextSync, SyncPolicy } from 'wuying-agentbay-sdk';

// Initialize the SDK
const agentBay = new AgentBay({ apiKey: 'your_api_key' });

async function createSessionWithPersistence() {
  // Get or create a persistent context
  const contextResult = await agentBay.context.get('my-persistent-context', true);
  
  if (contextResult.success) {
    // Configure context synchronization
    const contextSync = new ContextSync({
      contextId: contextResult.context.id,
      path: '/mnt/data',  // Mount path in the session
      policy: SyncPolicy.default()
    });
    
    // Create a session with context synchronization
    const sessionResult = await agentBay.create({
      contextSync: [contextSync]
    });
    
    const session = sessionResult.session;
    
    // Now you can access the persistent storage at /mnt/data
    const result = await session.command.execute("echo 'Hello, World!' > /mnt/data/hello.txt");
    if (result.success) {
      console.log("File created in persistent storage");
    }
  }
}
```

### Golang

```go
package main

import (
    "fmt"
    "github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

func main() {
    // Initialize the SDK
    client, _ := agentbay.NewAgentBay("your_api_key", nil)
    
    // Get or create a persistent context
    contextResult, _ := client.Context.Get("my-persistent-context", true)
    
    // Configure context synchronization
    policy := agentbay.NewSyncPolicy()
    contextSync := agentbay.NewContextSync(
        contextResult.Context.ID,
        "/mnt/data",  // Mount path in the session
        policy,
    )
    
    // Create a session with context synchronization
    params := agentbay.NewCreateSessionParams().
        AddContextSyncConfig(contextSync)
    
    sessionResult, _ := client.Create(params)
    session := sessionResult.Session
    
    // Now you can access the persistent storage at /mnt/data
    result, _ := session.Command.Execute("echo 'Hello, World!' > /mnt/data/hello.txt")
    if result.Success {
        fmt.Println("File created in persistent storage")
    }
}
```

## Customizing Synchronization Policies

You can customize the synchronization policy to control how and when data is synchronized:

### Python

```python
from agentbay.context_sync import SyncPolicy, UploadPolicy, DownloadPolicy

# Create a custom sync policy
policy = SyncPolicy(
    upload_policy=UploadPolicy(
        auto_upload=True,
        upload_strategy="BeforeResourceRelease",
        period=30  # Upload every 30 seconds
    ),
    download_policy=DownloadPolicy(
        auto_download=True,
        download_strategy="Async"
    )
)

# Use this policy in context synchronization
context_sync = ContextSync.new(
    context_id="your_context_id",
    path="/mnt/data",
    policy=policy
)
```

### TypeScript

```typescript
import { SyncPolicy, UploadPolicy, DownloadPolicy } from 'wuying-agentbay-sdk';

// Create a custom sync policy
const policy = new SyncPolicy({
  uploadPolicy: new UploadPolicy({
    autoUpload: true,
    uploadStrategy: "BeforeResourceRelease",
    period: 30  // Upload every 30 seconds
  }),
  downloadPolicy: new DownloadPolicy({
    autoDownload: true,
    downloadStrategy: "Async"
  })
});

// Use this policy in context synchronization
const contextSync = new ContextSync({
  contextId: "your_context_id",
  path: "/mnt/data",
  policy: policy
});
```

### Golang

```go
// Create a custom sync policy
policy := agentbay.SyncPolicy{
    UploadPolicy: &agentbay.UploadPolicy{
        AutoUpload:     true,
        UploadStrategy: agentbay.UploadBeforeResourceRelease,
        Period:         30,  // Upload every 30 seconds
    },
    DownloadPolicy: &agentbay.DownloadPolicy{
        AutoDownload:     true,
        DownloadStrategy: agentbay.DownloadAsync,
    },
}

// Use this policy in context synchronization
contextSync := agentbay.NewContextSync(
    "your_context_id",
    "/mnt/data",
    &policy,
)
```

## Best Practices

1. **Use Multiple Contexts**: For complex applications, use multiple contexts to separate different types of data (e.g., code, configuration, user data).

2. **Choose Appropriate Mount Paths**: Mount contexts at paths that make sense for your application's structure.

3. **Optimize Synchronization Policies**: Configure upload and download policies based on your application's needs:
   - For critical data, use frequent auto-uploads.
   - For large datasets, consider manual synchronization to avoid performance issues.

4. **Clean Up Unused Contexts**: Delete contexts that are no longer needed to free up resources.

## Related Resources

- [Context API Reference](../api-reference/context.md)
- [Context Manager API Reference](../api-reference/context-manager.md)
- [Session Management Tutorial](session-management.md) 