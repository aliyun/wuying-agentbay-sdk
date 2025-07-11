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

Deletes a context by name or ID.

```python
delete(context_id_or_name: str) -> DeleteResult
```

**Parameters:**
- `context_id_or_name` (str): The ID or name of the context to delete.

**Returns:**
- `DeleteResult`: A result object containing success status and request ID.

**Example:**
```python
from agentbay import AgentBay

# Initialize the SDK
agent_bay = AgentBay(api_key="your_api_key")

# Delete a context by name
result = agent_bay.context.delete("my-context")
if result.success:
    print("Context deleted successfully")
else:
    print(f"Failed to delete context: {result.error_message}")

# Delete a context by ID
result = agent_bay.context.delete("ctx-1234567890abcdef")
if result.success:
    print("Context deleted successfully")
else:
    print(f"Failed to delete context: {result.error_message}")
```

### modify

Modifies a context's properties.

```python
modify(context_id_or_name: str, **kwargs) -> ContextResult
```

**Parameters:**
- `context_id_or_name` (str): The ID or name of the context to modify.
- `**kwargs`: Key-value pairs of properties to modify.

**Returns:**
- `ContextResult`: A result object containing the modified Context object and request ID.

**Example:**
```python
from agentbay import AgentBay

# Initialize the SDK
agent_bay = AgentBay(api_key="your_api_key")

# Modify a context
result = agent_bay.context.modify("my-context", name="my-renamed-context")
if result.success:
    context = result.context
    print(f"Modified context: {context.name}")
else:
    print(f"Failed to modify context: {result.error_message}")
```

## Related Resources

- [Session API Reference](session.md)
- [ContextManager API Reference](context-manager.md) 