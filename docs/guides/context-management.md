# Context Management Documentation

This document provides comprehensive guidance on using the context management capabilities of the AgentBay SDK across all supported languages.

## Overview

Context management in the AgentBay SDK enables persistent data storage and synchronization across sessions. This feature allows developers to maintain state and share data between different execution environments, ensuring continuity of operations and efficient resource utilization.

The context management system provides two main services:
1. **ContextService**: Global service for context lifecycle management
2. **ContextManager**: Session-specific manager for context synchronization

## Getting Started

### Prerequisites

To use context management, you need:
1. AgentBay SDK installed for your preferred language
2. Valid API key
3. Understanding of session management concepts

### Creating a Context

Before using contexts, you need to create one:

```python
from agentbay import AgentBay

# Initialize the SDK
agent_bay = AgentBay(api_key="your_api_key")

# Create a context
context_result = agent_bay.context.create()
if context_result.success:
    context = context_result.context
    print(f"Context created with ID: {context.id}")
```

```typescript
import { AgentBay } from 'wuying-agentbay-sdk';

// Initialize the SDK
const agentBay = new AgentBay({ apiKey: 'your_api_key' });

// Create a context
async function createContext() {
  const contextResult = await agentBay.context.create();
  if (contextResult.success) {
    const context = contextResult.context;
    console.log(`Context created with ID: ${context.id}`);
    return context;
  }
}
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

    // Create a context
    contextResult, err := client.Context.Create()
    if err != nil {
        fmt.Printf("Error creating context: %v\n", err)
        os.Exit(1)
    }

    context := contextResult.Context
    fmt.Printf("Context created with ID: %s\n", context.ID)
}
```

## Context Synchronization

Context synchronization allows you to mount persistent contexts at specific paths within sessions, enabling data persistence across session lifecycles.

### Synchronizing a Context with a Session

```python
from agentbay.context_sync import ContextSync, SyncPolicy
from agentbay.session_params import CreateSessionParams

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
    
    print(f"Session created with ID: {session.session_id} and synchronized context at /mnt/data")
```

```typescript
import { AgentBay, ContextSync, SyncPolicy } from 'wuying-agentbay-sdk';

// Initialize the SDK
const agentBay = new AgentBay({ apiKey: 'your_api_key' });

// Get or create a persistent context
async function createSessionWithContextSync() {
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
    console.log(`Session created with ID: ${session.sessionId} and synchronized context at /mnt/data`);
    return session;
  }
}
```

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
    
    fmt.Printf("Session created with ID: %s and synchronized context at /mnt/data\n", session.SessionID)
}
```

## Listing Contexts with Pagination

The context service supports pagination for efficient handling of large numbers of contexts:

```python
from agentbay.context_params import ListContextParams

# List contexts with pagination
params = ListContextParams(
    max_results=10,  # Maximum results per page
    next_token="",   # Token for the next page, empty for the first page
)

# Get the first page of results
result = agent_bay.context.list(params)

# Process the results
if result.success:
    # Print the current page contexts
    for context in result.contexts:
        print(f"Context ID: {context.id}")

    # Print pagination information
    print(f"Total count: {result.total_count}")
    print(f"Max results per page: {result.max_results}")
    print(f"Next token: {result.next_token}")

    # If there is a next page, retrieve it
    if result.next_token:
        params.next_token = result.next_token
        next_page_result = agent_bay.context.list(params)
        # Process the next page...
```

```typescript
import { AgentBay, ListContextParams } from 'wuying-agentbay-sdk';

// Initialize the SDK
const agentBay = new AgentBay({ apiKey: 'your_api_key' });

// List contexts by labels with pagination
async function listContextsWithPagination() {
  // Create pagination parameters
  const params: ListContextParams = {
    maxResults: 10,  // Maximum results per page
    nextToken: '',   // Token for the next page, empty for the first page
  };
  
  // Get the first page of results
  const result = await agentBay.context.list(params);
  
  // Process the results
  if (result.success) {
    // Print the current page contexts
    console.log(`Found ${result.contexts.length} contexts:`);
    result.contexts.forEach(context => {
      console.log(`Context ID: ${context.id}`);
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
      const nextPageResult = await agentBay.context.list(nextParams);
      // Process the next page...
    }
  }
}

listContextsWithPagination();
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
    client, err := agentbay.NewAgentBay("your_api_key", nil)
    if err != nil {
        fmt.Printf("Error initializing AgentBay client: %v\n", err)
        os.Exit(1)
    }

    // Create pagination parameters
    params := &agentbay.ListContextParams{
        MaxResults: 10,
        NextToken:  "",
    }

    // Get the first page of results
    result, err := client.Context.List(params)
    if err != nil {
        fmt.Printf("Error listing contexts: %v\n", err)
        os.Exit(1)
    }

    // Process the results
    fmt.Printf("Found %d contexts:\n", len(result.Contexts))
    for _, context := range result.Contexts {
        fmt.Printf("Context ID: %s\n", context.ID)
    }

    // Print pagination information
    fmt.Printf("Total count: %d\n", result.TotalCount)
    fmt.Printf("Max results per page: %d\n", result.MaxResults)
    fmt.Printf("Next token: %s\n", result.NextToken)

    // If there is a next page, retrieve it
    if result.NextToken != "" {
        params.NextToken = result.NextToken
        nextPageResult, err := client.Context.List(params)
        if err != nil {
            fmt.Printf("Error retrieving next page: %v\n", err)
            os.Exit(1)
        }
        // Process the next page...
    }
}
```

## Managing Synchronized Contexts

Once a context is synchronized with a session, you can manage it using the ContextManager:

### Getting Context Information

```python
# Get information about a synchronized context
info_result = session.context.get_info("/mnt/data")
if info_result.success:
    context_info = info_result.data
    print(f"Context Information:")
    print(f"  Context ID: {context_info.context_id}")
    print(f"  Path: {context_info.path}")
    print(f"  State: {context_info.state}")
    print(f"Request ID: {info_result.request_id}")
```

### Listing Synchronized Contexts

```python
# List all synchronized contexts
list_result = session.context.list()
if list_result.success:
    contexts = list_result.data
    print(f"Found {len(contexts)} synchronized contexts:")
    for context in contexts:
        print(f"  Context ID: {context.context_id}, Path: {context.path}, State: {context.state}")
    print(f"Request ID: {list_result.request_id}")
```

### Deleting a Synchronized Context

```python
# Delete a synchronized context
delete_result = session.context.delete_context("/mnt/data")
if delete_result.success:
    print(f"Context deleted successfully, request ID: {delete_result.request_id}")
```

## Browser Context Synchronization

For web automation workflows, you can use specialized browser contexts that persist browser data across sessions:

```python
from agentbay.session_params import CreateSessionParams, BrowserContext

# Get or create a persistent context for browser data
context_result = agent_bay.context.get("my-browser-context", create=True)

if context_result.success:
    # Create a Browser Context configuration
    browser_context = BrowserContext(
        context_id=context_result.context.id,
        auto_upload=True  # Automatically upload browser data when session ends
    )
    
    # Create a session with Browser Context
    params = CreateSessionParams()
    params.browser_context = browser_context
    
    # Create a session with Browser Context
    session_result = agent_bay.create(params)
```

```typescript
import { AgentBay, BrowserContext } from 'wuying-agentbay-sdk';

// Initialize the SDK
const agentBay = new AgentBay({ apiKey: 'your_api_key' });

async function createSessionWithBrowserContext() {
  // Get or create a persistent context for browser data
  const contextResult = await agentBay.context.get('my-browser-context', true);
  
  if (contextResult.success) {
    // Create a Browser Context configuration
    const browserContext: BrowserContext = {
      contextId: contextResult.context.id,
      autoUpload: true  // Automatically upload browser data when session ends
    };
    
    // Create a session with Browser Context
    const sessionResult = await agentBay.create({
      browserContext: browserContext
    });
    
    const session = sessionResult.session;
    console.log(`Session created with ID: ${session.sessionId} and Browser Context`);
  }
}
```

## Best Practices

1. **Resource Management**:
   - Always delete contexts that are no longer needed to free up storage resources
   - Use descriptive context IDs to make them easier to identify and manage

2. **Error Handling**:
   - Always check the return results of context operations
   - Handle potential errors gracefully, especially during synchronization

3. **Synchronization Policies**:
   - Choose appropriate synchronization policies based on your use case
   - Consider the trade-offs between data consistency and performance

4. **Pagination**:
   - Use pagination when listing large numbers of contexts
   - Implement proper pagination handling in your applications

5. **Security**:
   - Protect context data with appropriate access controls
   - Avoid storing sensitive information in contexts without encryption

6. **Performance Optimization**:
   - Minimize the number of synchronized contexts per session
   - Use efficient synchronization policies to reduce overhead
   - Monitor context sizes to prevent excessive storage usage

## Limitations

1. **Storage Limits**: Context storage is subject to quota limits
2. **Synchronization Time**: Context synchronization may take time for large datasets
3. **Conflict Resolution**: Concurrent modifications to the same context may cause conflicts
4. **Network Dependencies**: Context operations require network connectivity

## Troubleshooting

### Common Issues

1. **Context Not Found**:
   - Verify the context ID is correct
   - Check if the context was properly created
   - Ensure you're using the correct AgentBay client instance

2. **Synchronization Failures**:
   - Check network connectivity
   - Verify the mount path is valid and accessible
   - Review synchronization policy settings

3. **Pagination Issues**:
   - Ensure next tokens are properly handled
   - Check max results parameter is within allowed limits
   - Verify label filters are correctly specified

4. **Browser Context Issues**:
   - Confirm browser contexts are supported in your SDK version
   - Check that browser sessions are properly configured
   - Verify browser data is being correctly persisted

## API Reference

For detailed API documentation, see:
- [Python Context API](../api-reference/python/context.md)
- [Python ContextManager API](../api-reference/python/context-manager.md)
- [TypeScript Context API](../api-reference/typescript/context.md)
- [TypeScript ContextManager API](../api-reference/typescript/context-manager.md)
- [Golang Context API](../api-reference/golang/context.md)
- [Golang ContextManager API](../api-reference/golang/context-manager.md)