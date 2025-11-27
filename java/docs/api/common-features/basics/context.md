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
```

Trigger context synchronization.

**Parameters:**
- `contextId` (String): Context ID to sync (optional, null for all contexts)
- `path` (String): Path to sync (optional, null for all paths)
- `mode` (String): Sync mode - "upload" or "download" (optional)

**Returns:**
- `ContextSyncResult`: Result containing sync status

**Example:**

```java
// Trigger upload sync for all contexts
ContextSyncResult result = session.getContext().sync();
if (result.isSuccess()) {
    System.out.println("Context sync initiated for all contexts");
}

// Trigger upload sync for specific context and path
ContextSyncResult specificResult = session.getContext().sync(
    "context-id-123", 
    "/workspace",
    "upload"
);
if (specificResult.isSuccess()) {
    System.out.println("Specific context sync initiated");
}
```

### info

```java
public ContextInfoResult info() throws AgentBayException
```

Get information about context synchronization status.

**Returns:**
- `ContextInfoResult`: Result containing context status information

**Example:**

```java
ContextInfoResult infoResult = session.getContext().info();
if (infoResult.isSuccess()) {
    for (ContextStatusData status : infoResult.getContextStatusData()) {
        System.out.println("Context: " + status.getContextId());
        System.out.println("Status: " + status.getStatus());
        System.out.println("Path: " + status.getPath());
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
// Trigger sync
session.getContext().sync("upload");

// Wait and check status
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
- [Data Persistence Guide](../../../../../docs/guides/common-features/basics/data-persistence.md)

---

*Documentation for AgentBay Java SDK*

