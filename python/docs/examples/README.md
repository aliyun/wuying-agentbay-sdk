# AgentBay Python SDK Examples

This directory contains comprehensive examples demonstrating various features of the AgentBay Python SDK.

## Directory Structure

```
examples/
├── _async/          # Async examples (Source of Truth)
│   ├── browser-use/
│   ├── codespace/
│   ├── common-features/
│   ├── computer-use/
│   └── mobile-use/
└── _sync/           # Sync examples (Auto-generated)
    ├── browser-use/
    ├── codespace/
    ├── common-features/
    ├── computer-use/
    └── mobile-use/
```

## About Async/Sync Versions

- **`_async/`**: Contains asynchronous examples using `AsyncAgentBay` and `async/await` syntax
- **`_sync/`**: Contains synchronous examples using `AgentBay` (auto-generated from async versions)

Both versions provide the same functionality. Choose based on your project requirements:
- Use **async** for modern async/await applications
- Use **sync** for traditional synchronous applications

## Example Categories (in _async/ and _sync/ directories)

### 1. Browser-use Examples

Located in `browser-use/browser/` and `browser-use/extension/`

**Basic Browser Operations:**
- `browser_screenshot.py` - Taking screenshots
- `browser_viewport.py` - Managing viewport sizes
- `browser_type_example.py` - Different browser types

**Navigation and Interaction:**
- `navigation_and_interaction.py` - Browser navigation and element interaction
- `page_analysis.py` - Page metadata and content extraction
- `multi_tab_management.py` - Managing multiple browser tabs

**Advanced Browser Features:**
- `javascript_execution.py` - Executing JavaScript in browser context
- `authentication_flow.py` - Handling authentication and login flows
- `responsive_testing.py` - Testing responsive design across viewports
- `network_monitoring.py` - Monitoring network requests and responses
- `popup_handling.py` - Managing popups and dialogs
- `iframe_handling.py` - Working with iframes

**File Operations:**
- `file_upload_download.py` - File upload/download operations

**Browser Automation:**
- `form_automation.py` - Automated form filling
- `web_scraping.py` - Web scraping techniques
- `cookies_management.py` - Cookie management
- `local_storage_management.py` - Local storage operations
- `screenshot_comparison.py` - Screenshot comparison

**Browser Configuration:**
- `browser_fingerprint_*.py` - Browser fingerprinting
- `browser_context_cookie_persistence.py` - Cookie persistence
- `browser-proxies.py` - Proxy configuration
- `browser_command_args.py` - Browser command arguments
- `browser_replay.py` - Browser session replay

**Extension Development:**
- `basic_extension_usage.py` - Basic extension usage
- `extension_development_workflow.py` - Extension development
- `extension_testing_automation.py` - Extension testing

**Real-world Examples:**
- `search_agentbay_doc*.py` - Documentation search examples
- `game_*.py` - Game automation examples
- Various domain-specific examples

### 2. Codespace Examples

Located in `codespace/`

**Development Environments:**
- `python_development.py` - Python environment setup and package management
- `nodejs_development.py` - Node.js environment and npm operations

**Version Control:**
- `git_operations.py` - Git repository initialization and commits

**Containerization:**
- `docker_operations.py` - Docker container management

**Data Management:**
- `database_operations.py` - SQLite database operations

**Text Processing:**
- `text_processing.py` - Text manipulation with grep/sed/awk

**System Operations:**
- `system_monitoring.py` - System resource monitoring
- `file_compression.py` - File compression and archiving

**Web Development:**
- `web_server_setup.py` - HTTP server setup and configuration

**Build Systems:**
- `build_automation.py` - Build automation with Makefiles

**Code Execution:**
- `code_execution_example.py` - Code execution patterns
- `jupyter_context_persistence.py` - Jupyter-like Python context persistence across consecutive `run_code()` calls within the same session

### 3. Common-features Examples

Located in `common-features/basics/` and `common-features/advanced/`

**Basic Operations:**
- `session_creation/` - Creating and managing sessions
- `command_execution_patterns.py` - Various command execution patterns
- `file_operations_patterns.py` - File operation patterns
- `file_system/` - File system operations
- `session_info.py` - Session information retrieval
- `working_directory.py` - Working directory management
- `environment_setup.py` - Environment variable configuration
- `process_management.py` - Process monitoring and management
- `data_transfer.py` - Data transfer operations

**Session Management:**
- `list_sessions/` - Listing sessions
- `get/` - Getting session information
- `session_pause_resume/` - Pausing and resuming sessions
- `label_management/` - Managing session labels

**Data Persistence:**
- `data_persistence/` - Context synchronization and data persistence
- `context_management/` - Context management
- `archive-upload-mode-example/` - Archive upload modes

**Advanced Features:**
- `concurrent_sessions.py` - Managing multiple sessions concurrently
- `resource_cleanup.py` - Proper resource cleanup patterns
- `error_recovery.py` - Error handling and recovery
- `error_handling/` - Comprehensive error handling
- `batch_operations/` - Batch operations
- `parallel_execution/` - Parallel execution patterns
- `multi_session_management/` - Multi-session coordination

**Testing and Monitoring:**
- `api_testing/` - API testing patterns
- `network_testing/` - Network diagnostics
- `logging_monitoring/` - Logging and monitoring
- `performance_monitoring/` - Performance monitoring
- `screenshot_download/` - Screenshot operations

**Infrastructure:**
- `environment_variables/` - Environment variable management
- `retry_mechanism/` - Retry patterns with circuit breaker
- `session_pooling/` - Session pooling for efficiency
- `vpc_session/` - VPC session management
- `oss_management/` - OSS operations

**Filesystem:**
- `filesystem_example/` - Advanced filesystem operations
- `mcp_tool_direct_call/` - MCP tool direct calls

**Agent Integration:**
- `agent_module/` - Agent module usage

### 4. Computer-use Examples

Located in `computer-use/computer/`

- `windows_app_management_example.py` - Windows application management

### 5. Mobile-use Examples

Located in `mobile-use/`

- `mobile_get_adb_url_example.py` - Getting ADB connection URL
- `mobile_system/` - Mobile system operations

## Getting Started

### Prerequisites

```bash
pip install agentbay
```

### Running Examples

**Async version:**
```bash
python python/docs/examples/_async/codespace/python_development.py
```

**Sync version:**
```bash
python python/docs/examples/_sync/codespace/python_development.py
```

### Environment Variables

Most examples require the `AGENTBAY_API_KEY` environment variable:

```bash
export AGENTBAY_API_KEY="your_api_key_here"
```

## Example Template

### Async Example Template

```python
import asyncio
from agentbay import AsyncAgentBay
from agentbay import CreateSessionParams

async def main():
    client = AsyncAgentBay()
    session = None

    try:
        # Create session
        session_result = await client.create(
            CreateSessionParams(image_id="linux_latest")
        )
        session = session_result.session

        # Your code here
        result = await session.command.execute_command("echo 'Hello'")
        print(result.output)

    finally:
        if session:
            await client.delete(session)

if __name__ == "__main__":
    asyncio.run(main())
```

### Sync Example Template

```python
from agentbay import AgentBay
from agentbay import CreateSessionParams

def main():
    client = AgentBay()
    session = None

    try:
        # Create session
        session_result = client.create(
            CreateSessionParams(image_id="linux_latest")
        )
        session = session_result.session

        # Your code here
        result = session.command.execute_command("echo 'Hello'")
        print(result.output)

    finally:
        if session:
            client.delete(session)

if __name__ == "__main__":
    main()
```

## Contributing

When adding new examples:

1. **Always create async version first** in `_async/` directory
2. **Run the generation script** to create sync version:
   ```bash
   cd python
   make generate-examples-sync
   ```
3. **Verify both versions** work correctly
4. **Update this README** with the new example

## Maintenance

The sync examples are auto-generated from async examples. To regenerate:

```bash
cd python
python scripts/generate_sync.py
```

Or use the Makefile:

```bash
cd python
make generate-examples-sync
```

## Need Help?

- Check the [API Documentation](../api/)
- Visit the [Guides](../../../docs/guides/)
- See the [Quickstart](../../../docs/quickstart/)

## License

These examples are part of the AgentBay SDK and follow the same license.
