# Session API Reference

## 🎯 Related Tutorial

- [Session Management Guide](../../../../../docs/guides/common-features/basics/session-management.md) - Learn about session lifecycle and management

## Overview

The Session class represents an active cloud environment instance in AgentBay. It provides access to all service modules (filesystem, command, browser, code, etc.) and manages the lifecycle of the cloud environment.

## Session

```java
public class Session
```

Represents a session in the AgentBay cloud environment.

### Constructor

```java
public Session(String sessionId, AgentBay agentBay, SessionParams params)
public Session(AgentBay agentBay, String sessionId)
```

Create a Session object. Typically you don't create sessions directly; use `AgentBay.create()` instead.

### Key Methods

### getSessionId

```java
public String getSessionId()
```

Get the session ID.

**Returns:**
- `String`: The unique session identifier

**Example:**

```java
Session session = agentBay.create().getSession();
String sessionId = session.getSessionId();
System.out.println("Session ID: " + sessionId);
```

### getFileSystem

```java
public FileSystem getFileSystem()
```

Get the file system service for this session.

**Returns:**
- `FileSystem`: File system service instance

**Example:**

```java
FileSystem fs = session.getFileSystem();
fs.writeFile("/tmp/test.txt", "Hello World");
```

### getCommand

```java
public Command getCommand()
```

Get the command execution service for this session.

**Returns:**
- `Command`: Command service instance

**Example:**

```java
Command cmd = session.getCommand();
CommandResult result = cmd.executeCommand("ls -la", 1000);
```

### getOss

```java
public OSS getOss()
```

Get the OSS service for this session.

**Returns:**
- `OSS`: OSS service instance

**Example:**

```java
OSS oss = session.getOss();
oss.envInit(accessKeyId, accessKeySecret, securityToken, endpoint, region);
oss.upload("bucket", "key", "/local/path");
```

### getCode

```java
public Code getCode()
```

Get the code execution service for this session.

**Returns:**
- `Code`: Code service instance

**Example:**

```java
Code code = session.getCode();
CodeExecutionResult result = code.runCode("print('Hello')", "python");
```

### getBrowser

```java
public Browser getBrowser()
```

Get the browser automation service for this session.

**Returns:**
- `Browser`: Browser service instance

**Example:**

```java
Browser browser = session.getBrowser();
BrowserOption option = new BrowserOption();
browser.initialize(option);
```

### getContext

```java
public ContextManager getContext()
```

Get the context manager for this session. The ContextManager provides methods for context synchronization and status monitoring.

**Returns:**
- `ContextManager`: Context manager instance

**Available Methods:**
- `sync()` - Trigger context sync (non-blocking)
- `sync(Consumer<Boolean> callback)` - Sync with callback (async mode)
- `syncAndWait()` - Sync and wait for completion (blocking mode)
- `info()` - Get context synchronization status

**Example:**

```java
ContextManager context = session.getContext();

// Basic sync (trigger only)
ContextSyncResult result = context.sync();

// Sync with callback (async)
context.sync(success -> {
    System.out.println("Sync completed: " + success);
});

// Sync and wait (blocking)
ContextSyncResult waitResult = context.syncAndWait();
if (waitResult.isSuccess()) {
    System.out.println("Sync completed successfully");
}

// Get sync status
ContextInfoResult info = context.info();
for (ContextStatusData status : info.getContextStatusData()) {
    System.out.println("Status: " + status.getStatus());
}
```

**See Also:**
- [Context API Reference](context.md) - Complete context management documentation
- [Context Sync Lifecycle Example](../../../../agentbay/src/main/java/com/aliyun/agentbay/examples/ContextSyncLifecycleExample.java) - Complete example demonstrating all sync modes

### info

```java
public SessionInfoResult info() throws AgentBayException
```

Get detailed information about this session.

**Returns:**
- `SessionInfoResult`: Result containing session information

**Throws:**
- `AgentBayException`: If the operation fails

**Example:**

```java
SessionInfoResult infoResult = session.info();
if (infoResult.isSuccess()) {
    SessionInfo info = infoResult.getSessionInfo();
    System.out.println("Resource URL: " + info.getResourceUrl());
    System.out.println("Session ID: " + info.getSessionId());
}
```

### delete

```java
public DeleteResult delete()
public DeleteResult delete(boolean syncContext)
```

Delete this session and release all associated resources.

**Parameters:**
- `syncContext` (boolean): Whether to sync context before deletion (default: false)

**Returns:**
- `DeleteResult`: Result containing success status

**Example:**

```java
// Simple delete
DeleteResult result = session.delete();

// Delete with context sync
DeleteResult syncResult = session.delete(true);
if (syncResult.isSuccess()) {
    System.out.println("Session deleted successfully");
}
```

**Note:** When `syncContext` is true, the method will:
1. Trigger context upload synchronization
2. Wait for all upload tasks to complete (up to 5 minutes)
3. Delete the session

This ensures all data is saved to context before the session is terminated.

### dumpState

```java
public String dumpState() throws AgentBayException
```

Dump session state to a JSON string for persistence and later restoration.

**Returns:**
- `String`: JSON string containing session state

**Throws:**
- `AgentBayException`: If serialization fails

**Example:**

```java
String stateJson = session.dumpState();
// Save stateJson for later restoration
Files.writeString(Path.of("/tmp/session-state.json"), stateJson);
```

### restoreState

```java
public static Session restoreState(AgentBay agentBay, String stateJson) throws AgentBayException
```

Restore a session from a previously dumped state JSON string.

**Parameters:**
- `agentBay` (AgentBay): AgentBay client instance
- `stateJson` (String): JSON string containing session state

**Returns:**
- `Session`: Restored session object

**Throws:**
- `AgentBayException`: If deserialization or restoration fails

**Example:**

```java
// Load saved state
String stateJson = Files.readString(Path.of("/tmp/session-state.json"));

// Restore session
Session restoredSession = Session.restoreState(agentBay, stateJson);
System.out.println("Session restored: " + restoredSession.getSessionId());
```

### getLink

```java
public OperationResult getLink() throws AgentBayException
public OperationResult getLink(String protocolType, Integer port) throws AgentBayException
```

Get a link URL for accessing the session environment (useful for VPC sessions or web services).

**Parameters:**
- `protocolType` (String): Protocol type (e.g., "https") - optional
- `port` (Integer): Port number - optional

**Returns:**
- `OperationResult`: Result containing the link URL
  - `getData()` returns the URL as a String

**Throws:**
- `AgentBayException`: If the request fails

**Example:**

```java
// Get default link
OperationResult linkResult = session.getLink();
if (linkResult.isSuccess()) {
    String url = (String) linkResult.getData();
    System.out.println("Session URL: " + url);
}

// Get link for specific port
OperationResult customLink = session.getLink("https", 8080);
if (customLink.isSuccess()) {
    String customUrl = (String) customLink.getData();
    System.out.println("Custom URL: " + customUrl);
}
```

### MCP Tool Operations

### listTools

```java
public List<Object> listTools() throws AgentBayException
```

List all available MCP tools for this session.

**Returns:**
- `List<Object>`: List of available tool definitions

**Throws:**
- `AgentBayException`: If the operation fails

### callTool

```java
public CallMcpToolResponse callTool(String toolName, Object args) throws AgentBayException
```

Call an MCP tool directly.

**Parameters:**
- `toolName` (String): Name of the tool to call
- `args` (Object): Tool arguments (typically a Map or custom object)

**Returns:**
- `CallMcpToolResponse`: Tool execution response containing:
  - `content` (List<Object>): Response content from the tool
  - `isError` (boolean): Whether the call resulted in an error
  - Other tool-specific fields

**Throws:**
- `AgentBayException`: If the call fails

**Example:**

```java
// List available tools first
List<Object> tools = session.listTools();
System.out.println("Available tools: " + tools);

// Call a tool with arguments
Map<String, Object> args = new HashMap<>();
args.put("path", "/tmp");
CallMcpToolResponse response = session.callTool("list_directory", args);

if (!response.isError()) {
    System.out.println("Tool result: " + response.getContent());
} else {
    System.err.println("Tool call failed");
}
```

## SessionInfo

```java
public class SessionInfo
```

Contains detailed information about a session.

**Fields:**
- `sessionId` (String): Session identifier
- `resourceUrl` (String): Resource URL for accessing the session
- `appId` (String): Application ID
- `authCode` (String): Authentication code
- `resourceId` (String): Resource identifier
- `resourceType` (String): Type of resource
- `ticket` (String): Access ticket
- `connectionProperties` (Map<String, Object>): Connection properties

## Session State Management

Sessions can be persisted and restored using the dump/restore mechanism:

```java
// Save session state
Session session = agentBay.create().getSession();
String state = session.dumpState();
Files.writeString(Path.of("session.json"), state);

// ... Later, restore the session
String savedState = Files.readString(Path.of("session.json"));
Session restored = Session.restoreState(agentBay, savedState);

// Continue using restored session
FileContentResult result = restored.getFileSystem().readFile("/tmp/test.txt");
```

## VPC Sessions

For sessions created with VPC networking:

```java
// Check if session is VPC-enabled
boolean isVpc = session.isVpcEnabled();

// Get VPC link (auto-refreshes if expired)
String vpcUrl = session.getVpcLinkUrl();

// Manually update VPC link
session.updateVpcLinkUrl();
```

## Best Practices

1. **Always Delete Sessions**: Call `session.delete()` when done to free resources
2. **Context Sync on Delete**: Use `session.delete(true)` if you need to preserve data
3. **Error Handling**: Check result success status before using data
4. **Resource Management**: Minimize concurrent sessions to stay within quotas
5. **State Persistence**: Use dump/restore for long-running workflows that span multiple runs
6. **Timeout Configuration**: Set appropriate timeouts for long-running operations

## Common Patterns

### Basic Session Usage

```java
// Create and use session
SessionResult result = agentBay.create();
if (result.isSuccess()) {
    Session session = result.getSession();
    
    // Use session services
    session.getFileSystem().writeFile("/tmp/data.txt", "content");
    CommandResult cmdResult = session.getCommand().execute("ls -la");
    
    // Clean up
    session.delete();
}
```

### Session with Context Sync

```java
// Create session with context
ContextSync contextSync = ContextSync.create(contextId, "/data", SyncPolicy.defaultPolicy());
CreateSessionParams params = new CreateSessionParams();
params.setContextSyncs(Arrays.asList(contextSync));

Session session = agentBay.create(params).getSession();

// Work with files - they'll be synced to context
session.getFileSystem().writeFile("/data/output.txt", "results");

// Delete with sync to save data
session.delete(true);
```

## Related Resources

- [AgentBay API Reference](agentbay.md)
- [FileSystem API Reference](filesystem.md)
- [Command API Reference](command.md)
- [Context API Reference](context.md)
- [Session Context Example](../../../../agentbay/src/main/java/com/aliyun/agentbay/examples/SessionContextExample.java)
- [Browser Context Example](../../../../agentbay/src/main/java/com/aliyun/agentbay/examples/BrowserContextExample.java)

---

*Documentation for AgentBay Java SDK*

