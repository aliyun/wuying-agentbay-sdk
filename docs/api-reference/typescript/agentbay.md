# AgentBay Class API Reference

The `AgentBay` class is the main entry point for interacting with the AgentBay cloud environment. It provides methods for creating, retrieving, listing, and deleting sessions.

## Constructor

### new AgentBay()

```typescript
constructor(config: AgentBayConfig)
```

**Parameters:**
- `config` (AgentBayConfig): Configuration object containing the API key and optional settings.
  - `apiKey` (string): The API key for authentication. If not provided, the SDK will look for the `AGENTBAY_API_KEY` environment variable.
  - `regionId` (string, optional): The region ID for the service.
  - `endpoint` (string, optional): The service endpoint.
  - `timeoutMs` (number, optional): Request timeout in milliseconds.

**Throws:**
- `Error`: If no API key is provided and `AGENTBAY_API_KEY` environment variable is not set.

## Properties

### context

A `ContextService` instance for managing persistent contexts. See the [Context API Reference](context.md) for more details.

## Methods


Creates a new session in the AgentBay cloud environment.


```typescript
create(params?: CreateSessionParams): Promise<SessionResult>
```

**Parameters:**
- `params` (CreateSessionParams, optional): Parameters for session creation.

**Returns:**
- `Promise<SessionResult>`: A promise that resolves to a result object containing the new Session instance, success status, request ID, and error message if any.

**Behavior:**
- When `params` includes valid `PersistenceDataList`, after creating the session, the API will check `session.context.info` to retrieve ContextStatusData.
- It will continuously monitor all data items' Status in ContextStatusData until all items show either "Success" or "Failed" status, or until the maximum retry limit (150 times with 2-second intervals) is reached.
- Any "Failed" status items will have their error messages printed.
- The Create operation only returns after context status checking completes.

**Throws:**
- `Error`: If the session creation fails.

**Example:**
```typescript
import { AgentBay, CreateSessionParams } from 'wuying-agentbay-sdk';
import { ContextSync, SyncPolicy } from 'wuying-agentbay-sdk/context-sync';

// Initialize the SDK
const agentBay = new AgentBay({ apiKey: 'your_api_key' });

// Create a session with default parameters
async function createDefaultSession() {
  const result = await agentBay.create();
  if (result.success) {
    console.log(`Created session with ID: ${result.session.sessionId}`);
    return result.session;
  }
  throw new Error(`Failed to create session: ${result.errorMessage}`);
}

// Create a session with custom parameters
async function createCustomSession() {
  const params: CreateSessionParams = {
    imageId: 'linux_latest',
    labels: { project: 'demo', environment: 'testing' },
    contextId: 'your_context_id'  // DEPRECATED: Use contextSync instead
  };
  
  const result = await agentBay.create(params);
  if (result.success) {
    console.log(`Created custom session with ID: ${result.session.sessionId}`);
    return result.session;
  }
  throw new Error(`Failed to create session: ${result.errorMessage}`);
}

// RECOMMENDED: Create a session with context synchronization
async function createSessionWithSync() {
  const contextSync = new ContextSync({
    contextId: 'your_context_id',
    path: '/mnt/persistent',
    policy: SyncPolicy.default()
  });
  
  const params: CreateSessionParams = {
    imageId: 'linux_latest',
    contextSync: [contextSync]
  };
  
  const result = await agentBay.create(params);
  if (result.success) {
    console.log(`Created session with context sync: ${result.session.sessionId}`);
    return result.session;
  }
  throw new Error(`Failed to create session: ${result.errorMessage}`);
}
```


```typescript
list(): Promise<Session[]>
```

**Returns:**
- `Promise<Session[]>`: A promise that resolves to an array of Session instances.

**Throws:**
- `Error`: If the session listing fails.

**Example:**
```typescript
import { AgentBay } from 'wuying-agentbay-sdk';

// Initialize the SDK
const agentBay = new AgentBay({ apiKey: 'your_api_key' });

// List all sessions
async function listSessions() {
  const sessions = await agentBay.list();
  console.log(`Found ${sessions.length} sessions:`);
  sessions.forEach(session => {
    console.log(`Session ID: ${session.sessionId}`);
  });
}

listSessions();
```


```typescript
listByLabels(params?: ListSessionParams | Record<string, string>): Promise<SessionListResult>
```

**Parameters:**
- `params` (ListSessionParams | Record<string, string>, optional): Parameters for filtering sessions by labels. If a dictionary is provided, it will be treated as labels. If not provided, all sessions will be returned.

**Returns:**
- `Promise<SessionListResult>`: A promise that resolves to a result object containing the filtered sessions, pagination information, and request ID.

**Throws:**
- `Error`: If the session listing fails.

**Example:**
```typescript
import { AgentBay, ListSessionParams } from 'wuying-agentbay-sdk';

// Initialize the SDK
const agentBay = new AgentBay({ apiKey: 'your_api_key' });

// List sessions by labels with pagination
async function listSessionsByLabels() {
  // Create pagination parameters
  const params: ListSessionParams = {
    maxResults: 10,  // Maximum results per page
    nextToken: '',   // Token for the next page, empty for the first page
    labels: { environment: 'production', project: 'demo' }  // Filter labels
  };
  
  // Get the first page of results
  const result = await agentBay.listByLabels(params);
  
  // Process the results
  if (result.success) {
    // Print the current page sessions
    console.log(`Found ${result.sessions.length} sessions:`);
    result.sessions.forEach(session => {
      console.log(`Session ID: ${session.sessionId}`);
    });
    
    // Print pagination information
    console.log(`Total count: ${result.totalCount}`);
    console.log(`Max results per page: ${result.maxResults}`);
    console.log(`Next token: ${result.nextToken}`);
    
    // If there is a next page, retrieve it
    if (result.nextToken) {
      const nextParams = {
        ...params,
        nextToken: result.nextToken
      };
      const nextPageResult = await agentBay.listByLabels(nextParams);
      // Process the next page...
    }
  }
}

listSessionsByLabels();
```


```typescript
delete(session: Session, syncContext?: boolean): Promise<DeleteResult>
```

**Parameters:**
- `session` (Session): The session to delete.
- `syncContext` (boolean, optional): If true, the API will trigger a file upload via `session.context.sync` before actually releasing the session. Default is false.

**Returns:**
- `Promise<DeleteResult>`: A promise that resolves to a result object containing success status, request ID, and error message if any.

**Behavior:**
- When `syncContext` is true, the API will first call `session.context.sync` to trigger file upload.
- It will then check `session.context.info` to retrieve ContextStatusData and monitor all data items' Status.
- The API waits until all items show either "Success" or "Failed" status, or until the maximum retry limit (150 times with 2-second intervals) is reached.
- Any "Failed" status items will have their error messages printed.
- The session deletion only proceeds after context sync status checking completes.

**Throws:**
- `Error`: If the session deletion fails.

**Example:**
```typescript
import { AgentBay } from 'wuying-agentbay-sdk';

// Initialize the SDK
const agentBay = new AgentBay({ apiKey: 'your_api_key' });

// Create and delete a session
async function createAndDeleteSession() {
  try {
    // Create a session
    const createResult = await agentBay.create();
    if (createResult.success) {
      const session = createResult.session;
      console.log(`Created session with ID: ${session.sessionId}`);
      
      // Use the session for operations...
      
      // Delete the session when done
      const deleteResult = await agentBay.delete(session);
      if (deleteResult.success) {
        console.log('Session deleted successfully');
      } else {
        console.log(`Failed to delete session: ${deleteResult.errorMessage}`);
      }
    }
  } catch (error) {
    console.error('Error:', error);
  }
}

createAndDeleteSession();
```
