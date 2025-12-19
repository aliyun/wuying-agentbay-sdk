# Migration Guide

Migrate from AgentBay Python SDK v0.12.x to v0.13.0+ with sync/async separated architecture.

## Overview

**Version Change**: v0.12.0 → v0.13.0+

In v0.12.x and earlier, the SDK used async APIs extensively. Starting from v0.13.0, the SDK provides separate sync (`AgentBay`) and async (`AsyncAgentBay`) APIs.

**Migration scope**: 69 async methods across 26 files need updating.

## Quick Migration Steps

### 1. Import Changes

**Key Change**: The import structure has been completely refactored from a single API to a dual sync/async API system.

```python
# Before (v0.12.x) - Single API, flat module structure
from agentbay import AgentBay, Config, Session, Command
# Only one AgentBay class, was async-based

# After (v0.13.0+) - Dual API, unified imports
from agentbay import AgentBay, AsyncAgentBay  # Two separate APIs
from agentbay import Session, AsyncSession    # Separate sync/async classes
from agentbay import Browser, AsyncBrowser    # All modules have both versions
```

### 2. Choose Your API

**For scripts/CLI**: Use sync API
```python
# Before (v0.12.x)
from agentbay import AgentBay
async with AgentBay() as agent_bay:
    # operations

# After (v0.13.0+)
from agentbay import AgentBay
agent_bay = AgentBay(api_key="your_api_key")  # Or set AGENTBAY_API_KEY
# operations
```

**For web servers**: Use async API
```python
# Before (v0.12.x)
from agentbay import AgentBay
async with AgentBay() as agent_bay:
    # operations

# After (v0.13.0+)
from agentbay import AsyncAgentBay
agent_bay = AsyncAgentBay(api_key="your_api_key")  # Or set AGENTBAY_API_KEY
# operations (still async)
```

### 3. Method Name Changes

Remove `_async` suffix from all method names:

```python
# Before (v0.12.x)
await session.browser.agent.navigate_async(url)
await session.command.execute_command("ls")

# After (v0.13.0+ sync)
session.browser.agent.navigate(url)
session.command.execute_command("ls")

# After (v0.13.0+ async)
await session.browser.agent.navigate(url)
await session.command.execute_command("ls")
```

## Module Import Mapping

### Core Modules
```python
# v0.12.x (flat structure)
from agentbay import AgentBay, Session, Command, Computer, Mobile

# v0.13.0+ (unified imports with sync/async variants)
from agentbay import (
    AgentBay, AsyncAgentBay,           # Main client classes
    Session, AsyncSession,             # Session management
    Command, AsyncCommand,             # Command execution
    Computer, AsyncComputer,           # Computer automation
    Mobile, AsyncMobile,               # Mobile automation
    Browser, AsyncBrowser,             # Browser automation
    FileSystem, AsyncFileSystem,       # File operations
    Agent, AsyncAgent,                 # AI agent functionality
)
```

### Shared Components (No Change)
```python
# These imports remain the same
from agentbay import (
    Config, AgentBayError, APIError,
    CreateSessionParams, ListSessionParams,
    ContextSync, SyncPolicy, UploadPolicy
)
```

## Common Method Mapping

This section lists common renames. It is not an exhaustive list of all methods.

### Core Session Methods
```python
# v0.12.x → v0.13.0+
pause_async() → pause()
resume_async() → resume()
get_link_async() → get_link()
```

### Browser Methods
```python
# v0.12.x → v0.13.0+
initialize_async() → initialize()
navigate_async() → navigate()
screenshot_async() → screenshot()
act_async() → act()
observe_async() → observe()
extract_async() → extract()
close_async() → close()
```

### File System Methods
```python
# v0.12.x → v0.13.0+
upload_async() → upload()
download_async() → download()
```

## File Operations (Important Clarification)

In v0.13.0+, file APIs follow the same sync/async split as other modules:

- Sync: use `FileSystem` / `FileTransfer` without `await`
- Async: use `AsyncFileSystem` / `AsyncFileTransfer` with `await`

If you migrate an old async codebase, make sure you are not accidentally calling sync file APIs from an async server handler.



## Error Handling Changes

### Sync API
```python
# Current sync approach
result = session.command.execute_command("ls")
if result.success:
    print(result.output)
else:
    print(f"Error: {result.error_message}")
```

### Async API
```python
# Current async approach
result = await session.command.execute_command("ls")
if result.success:
    print(result.output)
else:
    print(f"Error: {result.error_message}")
```

## Context Manager Changes

### v0.12.x Version
```python
# Context manager approach (deprecated in v0.13.0+)
async with AgentBay() as agent_bay:
    session = await agent_bay.create(params)
```

### v0.13.0+ Version
```python
# Sync approach
agent_bay = AgentBay(api_key="your_api_key")  # Or set AGENTBAY_API_KEY
result = agent_bay.create(params)
session = result.session
# ... use session
session.delete()

# Async approach
agent_bay = AsyncAgentBay(api_key="your_api_key")  # Or set AGENTBAY_API_KEY
result = await agent_bay.create(params)
session = result.session
# ... use session
await session.delete()
```

## Common Migration Patterns

### Pattern 1: Simple Script Migration
```python
# Before (v0.12.x)
import asyncio
from agentbay import AgentBay

async def main():
    async with AgentBay() as agent_bay:
        session = await agent_bay.create(params)
        result = await session.command.execute_command("ls")
        print(result.output)

asyncio.run(main())

# After (v0.13.0+ sync)
from agentbay import AgentBay

agent_bay = AgentBay(api_key="your_api_key")  # Or set AGENTBAY_API_KEY
result = agent_bay.create(params)
session = result.session
result = session.command.execute_command("ls")
print(result.output)
session.delete()
```

### Pattern 2: Web Server Migration
```python
# Before (v0.12.x)
async def handle_request():
    async with AgentBay() as agent_bay:
        session = await agent_bay.create(params)
        result = await session.command.execute_command(cmd)
        return result.output

# After (v0.13.0+ async)
async def handle_request():
    agent_bay = AsyncAgentBay(api_key="your_api_key")  # Or set AGENTBAY_API_KEY
    result = await agent_bay.create(params)
    session = result.session
    result = await session.command.execute_command(cmd)
    await session.delete()
    return result.output
```

## Validation Steps

After migration:

1. **Remove all `_async` suffixes** from method names
2. **Update imports** (`AgentBay` for sync, `AsyncAgentBay` for async)
3. **Test basic operations** (create session, run command, delete session)
4. **Verify error handling** uses `result.success` pattern
5. **Check context management** follows new patterns

## Notes

- **Cleanup**: `session.delete()` / `await session.delete()` is the most direct cleanup path. `agent_bay.delete(session)` also exists, but it delegates to `session.delete()`.
- **API compatibility**: Most changes are mechanical (imports + `await` + removing `_async` suffix).
- **Performance**: behavior may differ slightly due to the new sync/async split.

For API comparison, see [Sync vs Async Guide](sync-vs-async.md).