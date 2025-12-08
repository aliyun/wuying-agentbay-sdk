# Synchronous vs Asynchronous Guide

This guide explains the differences between synchronous and asynchronous programming patterns in the AgentBay Python SDK.

## Overview

The AgentBay Python SDK provides both synchronous and asynchronous APIs to accommodate different use cases and programming styles.

## When to Use Synchronous API

Use the synchronous API (`AgentBay`) for:
- Simple scripts and CLI tools
- Learning and experimentation
- Sequential operations where concurrency is not needed

## When to Use Asynchronous API

Use the asynchronous API (`AsyncAgentBay`) for:
- Web servers (FastAPI, Django)
- High-concurrency applications
- Applications that need to handle multiple sessions simultaneously

## Code Examples

### Synchronous Example

```python
from agentbay import AgentBay, CreateSessionParams

# Create client
agentbay = AgentBay(api_key="your_api_key")

# Create session
result = agentbay.create(CreateSessionParams())
session = result.session

# Use session
result = session.command.execute_command("echo 'Hello World'")
print(result.output)

# Cleanup
session.delete()
```

### Asynchronous Example

```python
import asyncio
from agentbay import AsyncAgentBay, CreateSessionParams

async def main():
    # Create client
    agentbay = AsyncAgentBay(api_key="your_api_key")
    
    # Create session
    result = await agentbay.create(CreateSessionParams())
    session = result.session
    
    # Use session
    result = await session.command.execute_command("echo 'Hello World'")
    print(result.output)
    
    # Cleanup
    await session.delete()

# Run async function
asyncio.run(main())
```

## Key Differences

| Aspect | Synchronous | Asynchronous |
|--------|-------------|--------------|
| Import | `from agentbay import AgentBay` | `from agentbay import AsyncAgentBay` |
| Method calls | `session.command.execute_command()` | `await session.command.execute_command()` |
| Error handling | Standard try/except | Async try/except |
| Concurrency | Sequential | Concurrent with asyncio |

## Migration Guide

To migrate from synchronous to asynchronous code:

1. Change imports from `AgentBay` to `AsyncAgentBay`
2. Add `async` keyword to function definitions
3. Add `await` keyword before SDK method calls
4. Use `asyncio.run()` to execute the main function

For migrating from backup versions or between sync/async, see [Migration Guide](migration-guide.md).