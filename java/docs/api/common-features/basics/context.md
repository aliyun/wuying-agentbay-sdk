# Context API Reference

## 💾 Related Tutorial

- [First Session Tutorial](../../../../../docs/quickstart/first-session.md) - Get started with creating your first AgentBay session

## Overview

The Context module provides persistent storage capabilities across sessions. Contexts allow you to store and retrieve data that persists beyond individual session lifecycles, making them ideal for workflows that require data continuity.

## Context

```java
public class Context
```

Represents a persistent storage context.

**Fields:**
- `contextId` (String): Unique context identifier
- `name` (String): Context name
- `description` (String): Context description
- `metadata` (Map<String, Object>): Additional metadata
- `state` (String): Context state
- `osType` (String): Operating system type
- `createdAt` (String): Creation timestamp
- `updatedAt` (String): Last update timestamp

**Methods:**
- `getId()`: Returns the context ID
- `getContextId()`: Returns the context ID
- `getName()`: Returns the context name

## Context Service

### get

```java
public ContextResult get(String name, boolean create) throws AgentBayException
```

Get or create a context by name.

**Parameters:**
- `name` (String): Context name
- `create` (boolean): Whether to create if not exists

**Returns:**
- `ContextResult`: Result containing the context

**Example:**

```java
// Get existing context or create new one
ContextResult result = agentBay.getContext().get("my-project", true);
if (result.isSuccess()) {
    Context context = result.getContext();
    System.out.println("Context ID: " + context.getId());
}
```

## Context Manager

The ContextManager is accessed via `session.getContext()` and provides session-level context operations.

### sync

```java
public ContextSyncResult sync()
public ContextSyncResult sync(String contextId, String path, String mode)
public ContextSyncResult sync(Consumer<Boolean> callback)
public ContextSyncResult sync(String contextId, String path, String mode, Consumer<Boolean> callback)
public ContextSyncResult sync(String contextId, String path, String mode, Consumer<Boolean> callback, int maxRetries, int retryInterval)
```

Trigger context synchronization. Multiple overloads are available for different use cases:

1. **Basic sync** (trigger only, non-blocking): Returns immediately after triggering sync
2. **Sync with callback** (async mode): Returns immediately, callback is invoked when sync completes
3. **Sync and wait** (blocking mode): Blocks until sync completes

**Parameters:**
- `contextId` (String): Context ID to sync (optional, null for all contexts)
- `path` (String): Path to sync (optional, null for all paths)
- `mode` (String): Sync mode - "upload" or "download" (optional)
- `callback` (Consumer<Boolean>): Callback function that receives success status (true if successful, false otherwise)
- `maxRetries` (int): Maximum number of retries for polling completion status (default: 150)
- `retryInterval` (int): Milliseconds to wait between retries (default: 1500)

**Returns:**
- `ContextSyncResult`: Result containing sync status. Note: For callback mode, this indicates initial trigger success, not final completion.

**Example:**

```java
// Example 1: Basic sync (trigger only, non-blocking)
ContextSyncResult result = session.getContext().sync();
if (result.isSuccess()) {
    System.out.println("Context sync initiated for all contexts");
    // Sync is now running in the background
}

// Example 2: Sync with specific context and path
ContextSyncResult specificResult = session.getContext().sync(
    "context-id-123", 
    "/workspace",
    "upload"
);
if (specificResult.isSuccess()) {
    System.out.println("Specific context sync initiated");
}

// Example 3: Sync with callback (async mode)
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.TimeUnit;

CompletableFuture<Boolean> callbackFuture = new CompletableFuture<>();

ContextSyncResult callbackResult = session.getContext().sync(success -> {
    System.out.println("Sync completed: " + (success ? "SUCCESS" : "FAILED"));
    callbackFuture.complete(success);
});

if (callbackResult.isSuccess()) {
    System.out.println("Sync initiated, waiting for callback...");
    // Wait for callback (max 5 minutes)
    Boolean success = callbackFuture.get(5, TimeUnit.MINUTES);
    if (success) {
        System.out.println("All files synchronized successfully");
    }
}

// Example 4: Sync with callback and custom retry parameters
session.getContext().sync(
    "context-id-123",
    "/workspace",
    "upload",
    success -> {
        System.out.println("Sync completed: " + success);
    },
    200,  // maxRetries
    2000  // retryInterval (2 seconds)
);
```

### syncAndWait

```java
public ContextSyncResult syncAndWait()
public ContextSyncResult syncAndWait(String contextId, String path, String mode)
public ContextSyncResult syncAndWait(String contextId, String path, String mode, int maxRetries, int retryInterval)
```

Sync context data and wait for completion (blocking mode). This method will block until all sync tasks complete or timeout occurs.

**Parameters:**
- `contextId` (String): Context ID to sync (optional, null for all contexts)
- `path` (String): Path to sync (optional, null for all paths)
- `mode` (String): Sync mode - "upload" or "download" (optional)
- `maxRetries` (int): Maximum number of retries for polling completion status (default: 150)
- `retryInterval` (int): Milliseconds to wait between retries (default: 1500)

**Returns:**
- `ContextSyncResult`: Result containing sync status after waiting for completion

**Example:**

```java
// Example 1: Sync and wait for all contexts
ContextSyncResult result = session.getContext().syncAndWait();
if (result.isSuccess()) {
    System.out.println("All contexts synchronized successfully");
} else {
    System.err.println("Sync failed: " + result.getErrorMessage());
}

// Example 2: Sync specific context and wait
ContextSyncResult specificResult = session.getContext().syncAndWait(
    "context-id-123",
    "/workspace",
    "upload"
);
if (specificResult.isSuccess()) {
    System.out.println("Context synchronized successfully");
}

// Example 3: Sync with custom timeout parameters
ContextSyncResult customResult = session.getContext().syncAndWait(
    "context-id-123",
    "/workspace",
    "upload",
    200,  // maxRetries (200 * 2s = 400 seconds max wait)
    2000  // retryInterval (2 seconds)
);
```

### info

```java
public ContextInfoResult info()
public ContextInfoResult info(String contextId, String path, String taskType)
```

Get information about context synchronization status.

**Parameters:**
- `contextId` (String): Context ID filter (optional)
- `path` (String): Path filter (optional)
- `taskType` (String): Task type filter - "upload" or "download" (optional)

**Returns:**
- `ContextInfoResult`: Result containing context status information

**Example:**

```java
// Example 1: Get info for all contexts
ContextInfoResult infoResult = session.getContext().info();
if (infoResult.isSuccess()) {
    for (ContextStatusData status : infoResult.getContextStatusData()) {
        System.out.println("Context: " + status.getContextId());
        System.out.println("Status: " + status.getStatus());
        System.out.println("Path: " + status.getPath());
        System.out.println("Task Type: " + status.getTaskType());
    }
}

// Example 2: Get info for specific context and path
ContextInfoResult filteredResult = session.getContext().info(
    "context-id-123",
    "/workspace",
    "upload"
);
if (filteredResult.isSuccess()) {
    for (ContextStatusData status : filteredResult.getContextStatusData()) {
        if ("Success".equals(status.getStatus())) {
            System.out.println("Upload completed for: " + status.getPath());
        } else if ("Failed".equals(status.getStatus())) {
            System.err.println("Upload failed: " + status.getErrorMessage());
        }
    }
}
```

## Result Types

### ContextResult

```java
public class ContextResult extends ApiResponse
```

Result of context retrieval/creation operations.

**Fields:**
- `success` (boolean): True if operation succeeded
- `context` (Context): The context object
- `requestId` (String): Request identifier
- `errorMessage` (String): Error description if failed

### ContextSyncResult

```java
public class ContextSyncResult extends ApiResponse
```

Result of context synchronization operations.

**Fields:**
- `success` (boolean): True if operation succeeded
- `requestId` (String): Request identifier
- `errorMessage` (String): Error description if failed

### ContextInfoResult

```java
public class ContextInfoResult extends ApiResponse
```

Result of context info operations.

**Fields:**
- `success` (boolean): True if operation succeeded
- `contextStatusData` (List<ContextStatusData>): List of context status information
- `requestId` (String): Request identifier
- `errorMessage` (String): Error description if failed

### ContextStatusData

```java
public class ContextStatusData
```

Contains status information for a context sync operation.

**Fields:**
- `contextId` (String): Context identifier
- `path` (String): Synchronized path
- `taskType` (String): Task type ("upload" or "download")
- `status` (String): Status ("Success", "Failed", "InProgress", etc.)
- `errorMessage` (String): Error message if failed

## Usage Patterns

### Basic Context Usage

```java
// Get or create context
ContextResult contextResult = agentBay.getContext().get("my-project", true);
Context context = contextResult.getContext();

// Create session with context sync
ContextSync contextSync = ContextSync.create(
    context.getId(),
    "/data",
    SyncPolicy.defaultPolicy()
);

CreateSessionParams params = new CreateSessionParams();
params.setContextSyncs(Arrays.asList(contextSync));

Session session = agentBay.create(params).getSession();

// Work with files - they'll be synced to context
session.getFileSystem().writeFile("/data/output.txt", "results");

// Delete session with context sync
session.delete(true);
```

### Checking Sync Status

```java
// Method 1: Using syncAndWait (recommended for blocking operations)
ContextSyncResult result = session.getContext().syncAndWait();
if (result.isSuccess()) {
    System.out.println("Sync completed successfully");
} else {
    System.err.println("Sync failed: " + result.getErrorMessage());
}

// Method 2: Using sync with callback (recommended for async operations)
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.TimeUnit;

CompletableFuture<Boolean> future = new CompletableFuture<>();
session.getContext().sync(success -> {
    if (success) {
        System.out.println("Sync completed successfully");
    } else {
        System.err.println("Sync failed");
    }
    future.complete(success);
});

// Do other work while sync is in progress...
Boolean syncSuccess = future.get(5, TimeUnit.MINUTES);

// Method 3: Manual polling (for custom control)
session.getContext().sync();
Thread.sleep(2000);
ContextInfoResult info = session.getContext().info();

for (ContextStatusData status : info.getContextStatusData()) {
    if ("upload".equals(status.getTaskType())) {
        System.out.println("Upload status: " + status.getStatus());
        if ("Failed".equals(status.getStatus())) {
            System.err.println("Error: " + status.getErrorMessage());
        }
    }
}
```

### Multi-Context Session

```java
// Create multiple context syncs
ContextSync dataSync = ContextSync.create(dataContext.getId(), "/data", SyncPolicy.defaultPolicy());
ContextSync configSync = ContextSync.create(configContext.getId(), "/config", SyncPolicy.defaultPolicy());

CreateSessionParams params = new CreateSessionParams();
params.setContextSyncs(Arrays.asList(dataSync, configSync));

Session session = agentBay.create(params).getSession();
```

## Best Practices

1. **Naming Conventions**: Use descriptive, project-specific context names
2. **Context Reuse**: Reuse contexts across related sessions for data continuity
3. **Sync on Delete**: Always use `session.delete(true)` to ensure data is saved
4. **Error Handling**: Check sync status after operations to catch failures
5. **Path Organization**: Use clear directory structures within contexts
6. **Context Lifecycle**: Manage context lifecycle separately from sessions

## Related Resources

- [Context Sync API Reference](context-sync.md)
- [Session API Reference](session.md)
- [Session Context Example](../../../../agentbay/src/main/java/com/aliyun/agentbay/examples/SessionContextExample.java)
- [Context Sync Lifecycle Example](../../../../agentbay/src/main/java/com/aliyun/agentbay/examples/ContextSyncLifecycleExample.java)
- [Data Persistence Guide](../../../../../docs/guides/common-features/basics/data-persistence.md)

---

*Documentation for AgentBay Java SDK*

