# Contexts

Contexts are a fundamental concept in the Wuying AgentBay SDK that provide persistent storage capabilities across different sessions.

## Overview

Contexts are persistent storage resources that can be attached to sessions. They allow data to persist across different sessions, making them ideal for storing various types of data that need to be preserved, such as file systems (volumes), cookies, and potentially other types in the future.

## Context Properties

Contexts have the following main properties:

- **ID**: A string that uniquely identifies the context.
- **Name**: A human-readable name for the context.
- **State**: The current state of the context (e.g., "available", "in-use").
- **OSType**: The operating system type this context is bound to.
- **CreatedAt**: The date and time when the context was created.
- **LastUsedAt**: The date and time when the context was last used.

## Important Limitations

1. **One session at a time**: A context can only be used by one session at a time. If you try to create a session with a context ID that is already in use by another active session, the session creation will fail.

2. **OS binding**: A context is bound to the operating system of the first session that uses it. When a context is first used with a session, it becomes bound to that session's OS. Any attempt to use the context with a session running on a different OS will fail. For example, if a context is first used with a Linux session, it cannot later be used with a Windows or Android session.

## Context Lifecycle

1. **Creation**: Contexts are created using the `Create` method of the `ContextService` or implicitly when using the `Get` method with the `create` parameter set to `true`.

2. **Usage**: Contexts can be attached to sessions using the `WithContextID` method of the `CreateSessionParams` when creating a new session.

3. **State Changes**: When a context is attached to a session, its state changes from "available" to "in-use". When the session is deleted, the context's state changes back to "available".

4. **Update**: Context properties like name can be updated using the `Update` method.

5. **Deletion**: Contexts can be deleted using the `Delete` method when they are no longer needed.

## Usage Examples

### Golang

```go
// List all contexts
contexts, err := agentBay.Context.List()
if err != nil {
    fmt.Printf("Error listing contexts: %v\n", err)
}
for _, context := range contexts {
    fmt.Printf("Context: %s (%s), State: %s, OS: %s\n", 
               context.Name, context.ID, context.State, context.OSType)
}

// Get a context (create if it doesn't exist)
contextName := "my-test-context"
context, err := agentBay.Context.Get(contextName, true)
if err != nil {
    fmt.Printf("Error getting context: %v\n", err)
    return
}

// Create a session with the context
params := agentbay.NewCreateSessionParams().WithContextID(context.ID)
session, err := agentBay.Create(params)
if err != nil {
    fmt.Printf("Error creating session: %v\n", err)
    return
}

// Update the context
context.Name = "renamed-test-context"
success, err := agentBay.Context.Update(context)
if err != nil {
    fmt.Printf("Error updating context: %v\n", err)
}

// Clean up
err = agentBay.Delete(session)
if err != nil {
    fmt.Printf("Error deleting session: %v\n", err)
}

err = agentBay.Context.Delete(context)
if err != nil {
    fmt.Printf("Error deleting context: %v\n", err)
}
```

## Common Use Cases

1. **Persistent File Storage**: Store files that need to be accessed across multiple sessions.
2. **Configuration Storage**: Store configuration data that needs to persist between sessions.
3. **State Preservation**: Maintain state information across session restarts.

## Related Resources

- [Sessions](sessions.md)
- [Applications](applications.md)
- [Context Management Example](../../golang/examples/context_management/README.md)
