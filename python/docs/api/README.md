# AgentBay Python SDK API Reference

This directory contains auto-generated API reference documentation.

## Quick Links

- [📁 Synchronous API (`sync/`)](#synchronous-api)
- [⚡ Asynchronous API (`async/`)](#asynchronous-api)
- [📦 Common Classes (`common/`)](#common-classes)

## Synchronous vs Asynchronous

AgentBay provides both synchronous and asynchronous APIs with identical interfaces:

| Feature | Sync API | Async API |
|-|-|-|
| **Use Case** | Simple scripts, linear workflows | Concurrent operations, high performance |
| **Performance** | Sequential execution | 4-6x faster for parallel tasks |
| **Syntax** | `result = agent.create()` | `result = await agent.create()` |
| **Import** | `from agentbay import AgentBay` | `from agentbay import AsyncAgentBay` |

See [Synchronous vs Asynchronous Guide](../guides/async-programming/sync-vs-async.md) for detailed comparison.

---

## Synchronous API

All synchronous API classes are in the `sync/` directory:

- [AgentBay](sync/agentbay.md) - `agentbay.agentbay`
- [Session](sync/session.md) - `agentbay.session`
- [Command](sync/command.md) - `agentbay.command`
- [Context](sync/context.md) - `agentbay.context`
- [Context Manager](sync/context-manager.md) - `agentbay.context_manager`
- [File System](sync/filesystem.md) - `agentbay.filesystem`
- [Agent](sync/agent.md) - `agentbay.agent`
- [OSS](sync/oss.md) - `agentbay.oss`
- [Browser](sync/browser.md) - `agentbay.browser`
- [BrowserAgent](sync/browser-agent.md) - `agentbay.browser_agent`
- [Extension](sync/extension.md) - `agentbay.extension`
- [Code](sync/code.md) - `agentbay.code`
- [Computer](sync/computer.md) - `agentbay.computer`
- [Mobile](sync/mobile.md) - `agentbay.mobile`
- [BrowserFingerprint](sync/fingerprint.md) - `agentbay.fingerprint`
- [MobileSimulate](sync/mobile-simulate.md) - `agentbay.mobile_simulate`
- [SessionParams](sync/session-params.md) - `agentbay.session_params`

## Asynchronous API

All asynchronous API classes are in the `async/` directory:

- [AsyncAgentBay](async/async-agentbay.md) - `agentbay.agentbay`
- [AsyncSession](async/async-session.md) - `agentbay.session`
- [AsyncCommand](async/async-command.md) - `agentbay.command`
- [AsyncContext](async/async-context.md) - `agentbay.context`
- [AsyncContextManager](async/async-context-manager.md) - `agentbay.context_manager`
- [AsyncFileSystem](async/async-filesystem.md) - `agentbay.filesystem`
- [AsyncAgent](async/async-agent.md) - `agentbay.agent`
- [AsyncOss](async/async-oss.md) - `agentbay.oss`
- [AsyncBrowser](async/async-browser.md) - `agentbay.browser`
- [AsyncBrowserAgent](async/async-browser-agent.md) - `agentbay.browser_agent`
- [AsyncExtension](async/async-extension.md) - `agentbay.extension`
- [AsyncCode](async/async-code.md) - `agentbay.code`
- [AsyncComputer](async/async-computer.md) - `agentbay.computer`
- [AsyncMobile](async/async-mobile.md) - `agentbay.mobile`
- [AsyncBrowserFingerprint](async/async-fingerprint.md) - `agentbay.fingerprint`
- [AsyncMobileSimulate](async/async-mobile-simulate.md) - `agentbay.mobile_simulate`
- [AsyncSessionParams](async/async-session-params.md) - `agentbay.session_params`

## Common Classes

Shared classes used by both sync and async APIs are in the `common/` directory:

- [Configuration](common/config.md) - `agentbay._common.config`
- [Exceptions](common/exceptions.md) - `agentbay._common.exceptions`
- [Logging](common/logging.md) - `agentbay._common.logger`
- [Context Sync](common/context-sync.md) - `agentbay._common.params.context_sync`
- [Code Execution Models](common/code-models.md) - `agentbay._common.models.code`
- [Browser Models](common/browser-models.md) - `agentbay._common.models.browser`
- [Response Models](common/response-models.md) - `agentbay._common.models.response`
- [Browser Agent Models](common/browser-agent-models.md) - `agentbay._common.models.browser_agent`

---

**Note**: This documentation is auto-generated from source code. Run `python scripts/generate_api_docs.py` to regenerate.