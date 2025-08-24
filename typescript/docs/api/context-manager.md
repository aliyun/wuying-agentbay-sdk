# ContextManager API Reference

The `ContextManager` class provides functionality for managing contexts within a session. It enables you to interact with the contexts that are synchronized to the session, including reading and writing data, and managing file operations.

## Overview

The `ContextManager` is accessed through a session instance and provides functionality for managing contexts within that session.

## Methods


Synchronizes a context with the session.


```typescript
syncContext(contextId: string, path: string, policy?: SyncPolicy): Promise<OperationResult>
```

**Parameters:**
- `contextId` (string): The ID of the context to synchronize.
- `path` (string): The path where the context should be mounted.
- `policy` (SyncPolicy, optional): The synchronization policy. If not provided, default policy is used.

**Returns:**
- `Promise<OperationResult>`: A promise that resolves to a result object containing success status, request ID, and error message if any.

**Example:**
```typescript
import { AgentBay } from 'wuying-agentbay-sdk';
import { SyncPolicy } from 'wuying-agentbay-sdk/context-sync';

// Initialize the SDK
const agentBay = new AgentBay({ apiKey: 'your_api_key' });

// Create a session and synchronize a context
async function syncContextInSession() {
  try {
    // Create a session
    const result = await agentBay.create();
    if (result.success) {
      const session = result.session;
      
      // Get or create a context
      const contextResult = await agentBay.context.get('my-context', true);
      if (contextResult.success) {
        // Synchronize the context with the session
        const syncResult = await session.context.syncContext(
          contextResult.context.id,
          '/mnt/persistent',
          SyncPolicy.default()
        );
        
        if (syncResult.success) {
          console.log(`Context synchronized successfully, request ID: ${syncResult.requestId}`);
        } else {
          console.log(`Failed to synchronize context: ${syncResult.errorMessage}`);
        }
      } else {
        console.log(`Failed to get context: ${contextResult.errorMessage}`);
      }
    } else {
      console.log(`Failed to create session: ${result.errorMessage}`);
    }
  } catch (error) {
    console.error('Error:', error);
  }
}

syncContextInSession();
```


```typescript
getInfo(path: string): Promise<OperationResult>
```

**Parameters:**
- `path` (string): The path where the context is mounted.

**Returns:**
- `Promise<OperationResult>`: A promise that resolves to a result object containing the context information as data, success status, request ID, and error message if any.

**Example:**
```typescript
import { AgentBay } from 'wuying-agentbay-sdk';

// Initialize the SDK
const agentBay = new AgentBay({ apiKey: 'your_api_key' });

// Create a session with a synchronized context
// ... (assume context is synchronized to '/mnt/persistent')

// Get information about the synchronized context
async function getContextInfo() {
  try {
    const infoResult = await session.context.getInfo('/mnt/persistent');
    if (infoResult.success) {
      const contextInfo = infoResult.data;
      console.log('Context Information:');
      console.log(`  Context ID: ${contextInfo.contextId}`);
      console.log(`  Path: ${contextInfo.path}`);
      console.log(`  State: ${contextInfo.state}`);
      console.log(`Request ID: ${infoResult.requestId}`);
    } else {
      console.log(`Failed to get context info: ${infoResult.errorMessage}`);
    }
  } catch (error) {
    console.error('Error:', error);
  }
}

getContextInfo();
```


```typescript
deleteContext(path: string): Promise<OperationResult>
```

**Parameters:**
- `path` (string): The path where the context is mounted.

**Returns:**
- `Promise<OperationResult>`: A promise that resolves to a result object containing success status, request ID, and error message if any.

**Example:**
```typescript
import { AgentBay } from 'wuying-agentbay-sdk';

// Initialize the SDK
const agentBay = new AgentBay({ apiKey: 'your_api_key' });

// Create a session with a synchronized context
// ... (assume context is synchronized to '/mnt/persistent')

// Delete the synchronized context
async function deleteContext() {
  try {
    const deleteResult = await session.context.deleteContext('/mnt/persistent');
    if (deleteResult.success) {
      console.log(`Context deleted successfully, request ID: ${deleteResult.requestId}`);
    } else {
      console.log(`Failed to delete context: ${deleteResult.errorMessage}`);
    }
  } catch (error) {
    console.error('Error:', error);
  }
}

deleteContext();
```


```typescript
list(): Promise<OperationResult>
```

**Returns:**
- `Promise<OperationResult>`: A promise that resolves to a result object containing the list of synchronized contexts as data, success status, request ID, and error message if any.

**Example:**
```typescript
import { AgentBay } from 'wuying-agentbay-sdk';

// Initialize the SDK
const agentBay = new AgentBay({ apiKey: 'your_api_key' });

// Create a session with synchronized contexts
// ...

// List all synchronized contexts
async function listSynchronizedContexts() {
  try {
    const listResult = await session.context.list();
    if (listResult.success) {
      const contexts = listResult.data;
      console.log(`Found ${contexts.length} synchronized contexts:`);
      contexts.forEach(context => {
        console.log(`  Context ID: ${context.contextId}, Path: ${context.path}, State: ${context.state}`);
      });
      console.log(`Request ID: ${listResult.requestId}`);
    } else {
      console.log(`Failed to list contexts: ${listResult.errorMessage}`);
    }
  } catch (error) {
    console.error('Error:', error);
  }
}

listSynchronizedContexts();
```
