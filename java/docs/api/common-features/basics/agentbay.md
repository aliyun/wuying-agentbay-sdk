# AgentBay Client API Reference

## 🚀 Related Tutorial

- [First Session Tutorial](../../../../../docs/quickstart/first-session.md) - Get started with creating your first AgentBay session

## Overview

The AgentBay class is the main entry point for interacting with the AgentBay cloud runtime environment. It manages API authentication, session creation, and provides access to context services.

## AgentBay

```java
public class AgentBay
```

Main client for interacting with the AgentBay cloud runtime environment.

### Constructor

```java
public AgentBay(String apiKey) throws AgentBayException
public AgentBay(String apiKey, Config config) throws AgentBayException
```

Create an AgentBay client instance.

**Parameters:**
- `apiKey` (String): Your AgentBay API key. If null or empty, reads from `AGENTBAY_API_KEY` environment variable
- `config` (Config): Configuration object (optional)

**Throws:**
- `AgentBayException`: If initialization fails
- `AuthenticationException`: If API key is not provided or invalid

**Example:**

```java
// Using environment variable
AgentBay agentBay = new AgentBay(System.getenv("AGENTBAY_API_KEY"));

// With custom configuration
Config config = new Config();
config.setTimeoutMs(30000);
AgentBay agentBay = new AgentBay(System.getenv("AGENTBAY_API_KEY"), config);
```

## Session Management

### create

```java
public SessionResult create(CreateSessionParams params) throws AgentBayException
```

Create a new cloud session.

**Parameters:**
- `params` (CreateSessionParams): Session creation parameters. Cannot be null.

**Returns:**
- `SessionResult`: Result containing the created session

**Throws:**
- `AgentBayException`: If session creation fails

**Example:**

```java
// Create session with default parameters
CreateSessionParams params = new CreateSessionParams();
SessionResult result = agentBay.create(params);
if (result.isSuccess()) {
    Session session = result.getSession();
    // Use session...
}

// Create session with specific image and labels
CreateSessionParams params = new CreateSessionParams();
params.setImageId("browser_latest");
params.setLabels(Map.of("env", "production", "team", "backend"));

SessionResult result = agentBay.create(params);
if (result.isSuccess()) {
    Session session = result.getSession();
    System.out.println("Session created: " + session.getSessionId());
}
```

### delete

```java
public DeleteResult delete(Session session, boolean syncContext)
```

Delete a session and release its resources.

**Parameters:**
- `session` (Session): Session object to delete
- `syncContext` (boolean): Whether to sync context before deletion
  - `true`: Triggers context upload and waits for completion before deletion
  - `false`: Deletes session immediately without context sync

**Returns:**
- `DeleteResult`: Result containing success status

**Example:**

```java
// Create session
CreateSessionParams params = new CreateSessionParams();
SessionResult result = agentBay.create(params);
Session session = result.getSession();

// ... use session ...

// Delete without context sync
DeleteResult deleteResult = agentBay.delete(session, false);
if (deleteResult.isSuccess()) {
    System.out.println("Session deleted successfully");
}

// Or delete with context sync (saves data to context first)
DeleteResult syncDeleteResult = agentBay.delete(session, true);
```

**Note:** It's preferred to call `session.delete()` or `session.delete(true)` directly on the session object.

## Context Services

### getContext

```java
public ContextService getContext()
```

Get the context service for managing persistent storage contexts.

**Returns:**
- `ContextService`: Context service instance

**Example:**

```java
ContextService contextService = agentBay.getContext();
ContextResult result = contextService.get("my-context", true);
```

### getContextService

```java
public ContextService getContextService()
```

Get the context service (alias for `getContext()`).

**Returns:**
- `ContextService`: Context service instance

## Session Retrieval Methods

The AgentBay class provides three methods for retrieving sessions, each serving different use cases:

| Method | Data Source | Returns | Use Case |
|--------|-------------|---------|----------|
| `getSession(sessionId)` | Local cache only | `Session` or `null` | Quick access to sessions created by this AgentBay instance |
| `getSessionInfo(sessionId)` | Remote API | `GetSessionResult` | Get session metadata without creating Session object |
| `get(sessionId)` | Remote API | `SessionResult` | Recover sessions from server (restart, cross-process scenarios) |

### getSession

```java
public Session getSession(String sessionId)
```

Get a cached session object by ID from local cache only.

**Important:** This method only retrieves sessions from the local cache (sessions created by this AgentBay instance). It does not fetch sessions from the server.

**When to use:**
- You need quick access to a session that was created by the current AgentBay instance
- You want to avoid network overhead
- The session is guaranteed to be in the local cache

**Parameters:**
- `sessionId` (String): Session ID

**Returns:**
- `Session`: Session object if found in cache, `null` otherwise

**Example:**

```java
// Create a session first
SessionResult createResult = agentBay.create(new CreateSessionParams());
Session session = createResult.getSession();
String sessionId = session.getSessionId();

// Later, retrieve from cache (fast, no network call)
Session cachedSession = agentBay.getSession(sessionId);
if (cachedSession != null) {
    // Use cached session
    System.out.println("Found session in cache: " + sessionId);
} else {
    System.out.println("Session not in cache");
}
```

### getSessionInfo

```java
public GetSessionResult getSessionInfo(String sessionId)
```

Get session information by session ID from remote server. This method retrieves detailed session metadata from the API without creating a Session object.

**When to use:**
- You only need session metadata (resource URL, etc.)
- You don't need a full Session object for API calls
- You want to check if a session exists on the server

**Parameters:**
- `sessionId` (String): The ID of the session to retrieve

**Returns:**
- `GetSessionResult`: Result containing session information:
  - `success` (boolean): True if the operation succeeded
  - `data` (GetSessionData): Session information object with fields:
    - `sessionId` (String): Session ID
    - `appInstanceId` (String): Application instance ID
    - `resourceId` (String): Resource ID
    - `resourceUrl` (String): Resource URL for accessing the session
    <!-- VPC-related fields temporarily disabled -->
    <!-- - `vpcResource` (boolean): Whether this is a VPC resource -->
    <!-- - `networkInterfaceIp` (String): Network interface IP (for VPC sessions) -->
    <!-- - `httpPort` (String): HTTP port (for VPC sessions) -->
    <!-- - `token` (String): Authentication token (for VPC sessions) -->
  - `requestId` (String): Unique identifier for this API request
  - `errorMessage` (String): Error description (if success is false)

**Example:**

```java
// Get session metadata without creating Session object
GetSessionResult result = agentBay.getSessionInfo(sessionId);
if (result.isSuccess() && result.getData() != null) {
    GetSessionData data = result.getData();
    System.out.println("Session ID: " + data.getSessionId());
    System.out.println("Resource URL: " + data.getResourceUrl());
    // VPC functionality temporarily disabled
    // System.out.println("Is VPC: " + data.isVpcResource());
} else {
    System.out.println("Failed to get session info: " + result.getErrorMessage());
}
```

### get

```java
public SessionResult get(String sessionId) throws AgentBayException
```

Get a session by its ID from remote server. This method calls the GetSession API to retrieve session information and creates a Session object.

**When to use:**
- You need to recover a session that was created in a previous program run (after restart)
- You need to access a session created by a different AgentBay instance (cross-process)
- The session exists on the server but not in local cache
- You need a full Session object for API calls

**Important:** Unlike `getSession()`, this method fetches from the remote server, enabling session recovery scenarios. The retrieved session is NOT automatically added to the local cache.

**Parameters:**
- `sessionId` (String): The ID of the session to retrieve. Must be a non-empty string.

**Returns:**
- `SessionResult`: Result containing the Session instance, request ID, and success status:
  - `success` (boolean): True if the operation succeeded
  - `session` (Session): The session object (if success is true)
  - `requestId` (String): Unique identifier for this API request
  - `errorMessage` (String): Error description (if success is false)

**Throws:**
- `AgentBayException`: If the API request fails

**Note:**
- A default file transfer context is automatically created for the retrieved session
- <!-- VPC-related information (network_interface_ip, http_port, token) is populated from the API response -->
- Returns an error if session_id is empty or the session does not exist

**Example:**

```java
// Recover a session from server (e.g., after restart)
String sessionId = "your-session-id-from-previous-run";
SessionResult result = agentBay.get(sessionId);

if (result.isSuccess()) {
    Session session = result.getSession();
    System.out.println("Successfully recovered session: " + session.getSessionId());
    
    // Use the session normally
    session.getFileSystem().writeFile("/tmp/test.txt", "Hello");
    session.delete();
} else {
    System.out.println("Failed to recover session: " + result.getErrorMessage());
}
```

**Comparison Example:**

```java
// Scenario 1: Session created by current AgentBay instance - use getSession()
SessionResult createResult = agentBay.create(new CreateSessionParams());
String sessionId = createResult.getSession().getSessionId();

Session cachedSession = agentBay.getSession(sessionId);  // Fast, from cache
assert cachedSession != null;  // Will succeed

// Scenario 2: Session recovery after restart - use get()
// (In a new program run, sessionId is known but not in cache)
SessionResult recoveredResult = agentBay.get(sessionId);  // Network call
if (recoveredResult.isSuccess()) {
    Session recoveredSession = recoveredResult.getSession();
    // Use recovered session
}

// Scenario 3: Only need metadata - use getSessionInfo()
GetSessionResult infoResult = agentBay.getSessionInfo(sessionId);
if (infoResult.isSuccess()) {
    GetSessionData data = infoResult.getData();
    // Access metadata without creating Session object
    System.out.println("Resource URL: " + data.getResourceUrl());
}
```

### removeSession

```java
public void removeSession(String sessionId)
```

Remove a session from the internal cache.

**Parameters:**
- `sessionId` (String): Session ID to remove

**Note:** This only removes the session from the local cache; it does not delete the session from the server. Use `delete()` to actually terminate the session.

### getApiKey

```java
public String getApiKey()
```

Get the API key used by this client.

**Returns:**
- `String`: API key

### getRegionId

```java
public String getRegionId()
```

Get the region ID.

**Returns:**
- `String`: Region ID

## CreateSessionParams

```java
public class CreateSessionParams
```

Parameters for creating a new session.

### Fields and Methods

#### imageId

```java
public String getImageId()
public void setImageId(String imageId)
```

Set the environment image to use.

**Common Image IDs:**
- `linux_latest` - Linux environment (default)
- `browser_latest` - Browser automation environment
- `windows_latest` - Windows desktop environment
- `mobile_latest` - Mobile Android environment
- `code_latest` - Code execution environment

**Example:**

```java
CreateSessionParams params = new CreateSessionParams();
params.setImageId("browser_latest");
```

#### labels

```java
public Map<String, String> getLabels()
public void setLabels(Map<String, String> labels)
```

Set labels for organizing and filtering sessions.

**Example:**

```java
Map<String, String> labels = new HashMap<>();
labels.put("environment", "production");
labels.put("team", "backend");
labels.put("project", "data-pipeline");
params.setLabels(labels);
```

#### contextSyncs

```java
public List<ContextSync> getContextSyncs()
public void setContextSyncs(List<ContextSync> contextSyncs)
```

Set context synchronization configurations for data persistence.

**Example:**

```java
ContextSync contextSync = ContextSync.create(
    "context-id-123",
    "/data",
    SyncPolicy.defaultPolicy()
);
params.setContextSyncs(Arrays.asList(contextSync));
```

## SessionResult

```java
public class SessionResult extends ApiResponse
```

Result of session creation operations.

**Fields:**
- `success` (boolean): True if operation succeeded
- `session` (Session): The session object
- `sessionId` (String): Session identifier
- `requestId` (String): Request identifier
- `errorMessage` (String): Error description if failed

**Example:**

```java
CreateSessionParams params = new CreateSessionParams();
SessionResult result = agentBay.create(params);
if (result.isSuccess()) {
    Session session = result.getSession();
    String sessionId = result.getSessionId();
    System.out.println("Created session: " + sessionId);
} else {
    System.err.println("Failed: " + result.getErrorMessage());
}
```

## Config

```java
public class Config
```

Configuration for AgentBay client.

**Fields:**
- `regionId` (String): Region ID
- `endpoint` (String): API endpoint
- `timeoutMs` (int): Request timeout in milliseconds (default: 60000)

**Example:**

```java
Config config = new Config();
config.setTimeoutMs(120000); // 2 minutes
AgentBay agentBay = new AgentBay(System.getenv("AGENTBAY_API_KEY"), config);
```

## Complete Example

```java
import com.aliyun.agentbay.AgentBay;
import com.aliyun.agentbay.session.Session;
import com.aliyun.agentbay.session.CreateSessionParams;
import com.aliyun.agentbay.model.SessionResult;
import com.aliyun.agentbay.model.DeleteResult;
import java.util.Map;

public class AgentBayExample {
    public static void main(String[] args) throws Exception {
        // Initialize client
        AgentBay agentBay = new AgentBay(System.getenv("AGENTBAY_API_KEY"));
        
        // Create session with labels
        CreateSessionParams params = new CreateSessionParams();
        params.setImageId("linux_latest");
        params.setLabels(Map.of("env", "production"));
        
        SessionResult result = agentBay.create(params);
        if (result.isSuccess()) {
            Session session = result.getSession();
            System.out.println("Session created: " + session.getSessionId());
            
            // Use session
            session.getFileSystem().writeFile("/tmp/test.txt", "Hello World", "overwrite", false);
            
            // Clean up - delete with context sync
            DeleteResult deleteResult = agentBay.delete(session, false);
            if (deleteResult.isSuccess()) {
                System.out.println("Session deleted successfully");
            }
        }
    }
}
```

## Best Practices

1. **API Key Security**: Never hardcode API keys; use environment variables
2. **Resource Cleanup**: Always delete sessions when done to free resources
3. **Error Handling**: Check `result.isSuccess()` for all operations
4. **Labels**: Use labels to organize sessions by environment, team, or project
5. **Connection Pooling**: Reuse AgentBay client instances when possible
6. **Timeout Configuration**: Adjust timeouts based on expected operation duration
7. **Context Sync**: Use `delete(session, true)` when you need to preserve data

## Common Patterns

### Session Lifecycle

```java
// Create with required parameters
CreateSessionParams params = new CreateSessionParams();
params.setImageId("linux_latest");
SessionResult result = agentBay.create(params);
Session session = result.getSession();

// Use
session.getFileSystem().writeFile("/tmp/data.txt", "content", "overwrite", false);

// Delete
session.delete();
```

### Session with Context

```java
// Get or create context
ContextResult contextResult = agentBay.getContext().get("my-project", true);
Context context = contextResult.getContext();

// Create session with context sync
ContextSync sync = ContextSync.create(
    context.getId(),
    "/workspace",
    SyncPolicy.defaultPolicy()
);

CreateSessionParams params = new CreateSessionParams();
params.setContextSyncs(Arrays.asList(sync));

Session session = agentBay.create(params).getSession();

// Work with persistent data
session.getFileSystem().writeFile("/workspace/data.txt", "persistent data", "overwrite", false);

// Delete with sync to save data
session.delete(true);
```

### Working with Multiple Sessions

```java
AgentBay agentBay = new AgentBay(System.getenv("AGENTBAY_API_KEY"));

// Create multiple sessions
CreateSessionParams params1 = new CreateSessionParams();
params1.setLabels(Map.of("task", "processing"));
Session session1 = agentBay.create(params1).getSession();

CreateSessionParams params2 = new CreateSessionParams();
params2.setLabels(Map.of("task", "analysis"));
Session session2 = agentBay.create(params2).getSession();

// Use sessions independently
session1.getCommand().execute("echo 'Task 1'");
session2.getCommand().execute("echo 'Task 2'");

// Clean up
agentBay.delete(session1, false);
agentBay.delete(session2, false);
```

## Limitations and Notes

1. **Session Listing**: The current SDK version does not support listing all sessions across the platform. You can only access sessions created by the current AgentBay instance through `getSession()`.

2. **Session Retrieval**: There is no method to retrieve a session by ID from the server. Once a session is created, you must keep the Session object reference or retrieve it from the local cache.

3. **Cache Management**: The AgentBay client maintains an internal cache of created sessions. Use `removeSession()` to manually clean up the cache if needed.

## Related Resources

- [Session API Reference](session.md)
- [Context API Reference](context.md)
- [FileSystem API Reference](filesystem.md)
- [Quick Start Examples](../../../../agentbay/src/main/java/com/aliyun/agentbay/examples/)

---

*Documentation for AgentBay Java SDK*
