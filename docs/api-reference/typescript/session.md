# Session Class

The `Session` class represents a session in the AgentBay cloud environment. It provides methods for managing file systems, executing commands, and more.

## Properties

```typescript
agentBay  // The AgentBay instance that created this session
sessionId  // The ID of this session
resourceUrl  // The URL of the resource associated with this session
fileSystem  // The FileSystem instance for this session
command  // The Command instance for this session
oss  // The Oss instance for this session
application  // The Application instance for this session
window  // The WindowManager instance for this session
ui  // The UI instance for this session
context  // The ContextManager instance for this session
```

## Methods

### delete

Deletes this session.

```typescript
delete(): Promise<DeleteResult>
```

**Returns:**
- `Promise<DeleteResult>`: A promise that resolves to a result object containing success status, request ID, and error message if any.

**Example:**
```typescript
import { AgentBay } from 'wuying-agentbay-sdk';

// Initialize the SDK
const agentBay = new AgentBay({ apiKey: 'your_api_key' });

// Create and delete a session
async function createAndDeleteSession() {
  try {
    const result = await agentBay.create();
    if (result.success) {
      const session = result.session;
      console.log(`Session created with ID: ${session.sessionId}`);
      
      // Use the session...
      
      // Delete the session when done
      const deleteResult = await session.delete();
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

### setLabels

Sets labels for this session.

```typescript
setLabels(labels: Record<string, string>): Promise<OperationResult>
```

**Parameters:**
- `labels` (Record<string, string>): Key-value pairs representing the labels to set.

**Returns:**
- `Promise<OperationResult>`: A promise that resolves to a result object containing success status, request ID, and error message if any.

**Example:**
```typescript
// Set session labels
async function setSessionLabels(session) {
  try {
    const labels = {
      project: 'demo',
      environment: 'testing',
      version: '1.0.0'
    };
    
    const result = await session.setLabels(labels);
    console.log(`Labels set successfully, request ID: ${result.requestId}`);
    return result;
  } catch (error) {
    console.error(`Failed to set labels: ${error}`);
    throw error;
  }
}
```

### getLabels

Gets the labels for this session.

```typescript
getLabels(): Promise<LabelResult>
```

**Returns:**
- `Promise<LabelResult>`: A promise that resolves to a result object containing the session labels, request ID, and success status.

**Example:**
```typescript
// Get session labels
async function getSessionLabels(session) {
  try {
    const result = await session.getLabels();
    console.log(`Session labels: ${JSON.stringify(result.labels)}`);
    console.log(`Request ID: ${result.requestId}`);
    return result.labels;
  } catch (error) {
    console.error(`Failed to get labels: ${error}`);
    throw error;
  }
}
```

### info

Gets information about this session.

```typescript
info(): Promise<InfoResult>
```

**Returns:**
- `Promise<InfoResult>`: A promise that resolves to a result object containing session information, request ID, and success status.

**Example:**
```typescript
// Get session information
async function getSessionInfo(session) {
  try {
    const result = await session.info();
    console.log(`Session ID: ${result.data.sessionId}`);
    console.log(`Resource URL: ${result.data.resourceUrl}`);
    console.log(`Request ID: ${result.requestId}`);
    return result.data;
  } catch (error) {
    console.error(`Failed to get session info: ${error}`);
    throw error;
  }
}
```

### getLink

Gets a link for this session.

```typescript
getLink(protocolType?: string, port?: number): Promise<LinkResult>
```

**Parameters:**
- `protocolType` (string, optional): The protocol type for the link.
- `port` (number, optional): The port for the link.

**Returns:**
- `Promise<LinkResult>`: A promise that resolves to a result object containing the session link, request ID, and success status.

**Example:**
```typescript
// Get session link
async function getSessionLink(session) {
  try {
    const result = await session.getLink();
    console.log(`Session link: ${result.data}`);
    console.log(`Request ID: ${result.requestId}`);
    
    // Get link with specific protocol and port
    const customResult = await session.getLink('https', 8443);
    console.log(`Custom link: ${customResult.data}`);
    
    return result.data;
  } catch (error) {
    console.error(`Failed to get link: ${error}`);
    throw error;
  }
}
```

## Related Resources

- [FileSystem API Reference](filesystem.md)
- [Command API Reference](command.md)
- [UI API Reference](ui.md)
- [Window API Reference](window.md)
- [OSS API Reference](oss.md)
- [Application API Reference](application.md)
- [Context API Reference](context-manager.md) 