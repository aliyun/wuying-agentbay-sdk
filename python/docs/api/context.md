# Context API Reference

The Context API provides functionality for managing persistent storage contexts in the AgentBay cloud environment. Contexts allow you to persist data across sessions and reuse it in future sessions.

## Context Class

The `Context` class represents a persistent storage context in the AgentBay cloud environment.

### Properties

```python
id  # The unique identifier of the context
name  # The name of the context
state  # The current state of the context (e.g., "available", "in-use")
created_at  # Date and time when the Context was created
last_used_at  # Date and time when the Context was last used
os_type  # The operating system type this context is bound to
```

## ContextService Class

The `ContextService` class provides methods for managing persistent contexts in the AgentBay cloud environment.

### list

Lists all available contexts.

```python
list() -> ContextListResult
```

**Returns:**
- `ContextListResult`: A result object containing the list of Context objects and request ID.

**Example:**
```python
from agentbay import AgentBay

# Initialize the SDK
agent_bay = AgentBay(api_key="your_api_key")

# List all contexts
result = agent_bay.context.list()
if result.success:
    print(f"Found {len(result.contexts)} contexts:")
    for context in result.contexts:
        print(f"Context ID: {context.id}, Name: {context.name}, State: {context.state}")
else:
    print("Failed to list contexts")
```

### get

Gets a context by name. Optionally creates it if it doesn't exist.

```python
get(name: str, create: bool = False) -> ContextResult
```

**Parameters:**
- `name` (str): The name of the context to get.
- `create` (bool, optional): Whether to create the context if it doesn't exist. Defaults to False.

**Returns:**
- `ContextResult`: A result object containing the Context object and request ID.

**Example:**
```python
from agentbay import AgentBay

# Initialize the SDK
agent_bay = AgentBay(api_key="your_api_key")

# Get a context, creating it if it doesn't exist
result = agent_bay.context.get("my-persistent-context", create=True)
if result.success:
    context = result.context
    print(f"Context ID: {context.id}, Name: {context.name}, State: {context.state}")
else:
    print(f"Failed to get context: {result.error_message}")
```

### create

Creates a new context.

```python
create(name: str) -> ContextResult
```

**Parameters:**
- `name` (str): The name of the context to create.

**Returns:**
- `ContextResult`: A result object containing the created Context object and request ID.

**Example:**
```python
from agentbay import AgentBay

# Initialize the SDK
agent_bay = AgentBay(api_key="your_api_key")

# Create a new context
result = agent_bay.context.create("my-new-context")
if result.success:
    context = result.context
    print(f"Created context with ID: {context.id}, Name: {context.name}")
else:
    print(f"Failed to create context: {result.error_message}")
```

### delete

Deletes a context.

```python
delete(context: Context) -> OperationResult
```

**Parameters:**
- `context` (Context): The Context object to delete.

**Returns:**
- `OperationResult`: A result object containing success status and request ID.

**Example:**
```python
from agentbay import AgentBay

# Initialize the SDK
agent_bay = AgentBay(api_key="your_api_key")

# Get a context first
result = agent_bay.context.get("my-context")
if result.success and result.context:
    # Delete the context
    delete_result = agent_bay.context.delete(result.context)
    if delete_result.success:
        print("Context deleted successfully")
    else:
        print(f"Failed to delete context: {delete_result.error_message}")
else:
    print(f"Failed to get context: {result.error_message}")
```

### update

Updates a context's properties.

```python
update(context: Context) -> OperationResult
```

**Parameters:**
- `context` (Context): The Context object with updated properties.

**Returns:**
- `OperationResult`: A result object containing success status and request ID.

**Example:**
```python
from agentbay import AgentBay

# Initialize the SDK
agent_bay = AgentBay(api_key="your_api_key")

# Get a context first
result = agent_bay.context.get("my-context")
if result.success and result.context:
    # Update the context name
    context = result.context
    context.name = "my-renamed-context"
    
    # Save the changes
    update_result = agent_bay.context.update(context)
    if update_result.success:
        print("Context updated successfully")
    else:
        print(f"Failed to update context: {update_result.error_message}")
else:
    print(f"Failed to get context: {result.error_message}")
```

## Related Resources

- [Session API Reference](session.md)
- [ContextManager API Reference](context-manager.md) 