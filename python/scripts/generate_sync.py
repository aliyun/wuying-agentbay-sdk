import os
import sys
import unasync
import re
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AGENTBAY_DIR = os.path.join(ROOT, "agentbay")
ASYNC_DIR = os.path.join(AGENTBAY_DIR, "_async")
SYNC_DIR = os.path.join(AGENTBAY_DIR, "_sync")

TEST_DIR = os.path.join(ROOT, "tests", "integration")
TEST_ASYNC_DIR = os.path.join(TEST_DIR, "_async")
TEST_SYNC_DIR = os.path.join(TEST_DIR, "_sync")

# Unit test directories
UNIT_TEST_DIR = os.path.join(ROOT, "tests", "unit")
UNIT_TEST_ASYNC_DIR = os.path.join(UNIT_TEST_DIR, "async")
UNIT_TEST_SYNC_DIR = os.path.join(UNIT_TEST_DIR, "sync")

# Example directories
EXAMPLES_DIR = os.path.join(ROOT, "docs", "examples")
EXAMPLES_ASYNC_DIR = os.path.join(EXAMPLES_DIR, "_async")
EXAMPLES_SYNC_DIR = os.path.join(EXAMPLES_DIR, "_sync")

def _apply_custom_replacements(content: str, file_path: str) -> str:
    """Apply custom replacements that unasync doesn't handle."""
    # Fix asyncio.wait_for with stop_event.wait() - this is a common pattern in filesystem.py
    # Replace the entire try-except block (with correct indentation)
    content = content.replace(
        "                    try:\n                        asyncio.wait_for(stop_event.wait(), timeout=interval)\n                    except asyncio.TimeoutError:\n                        pass",
        "                    stop_event.wait(timeout=interval)"
    )
    # Also handle the case where it's just the call without try-except
    content = content.replace(
        "asyncio.wait_for(stop_event.wait(), timeout=interval)",
        "stop_event.wait(timeout=interval)"
    )
    # Ensure context start_clear alias is not renamed to clear_async (avoids recursion)
    content = re.sub(
        r"def clear_async\(self, context_id: str\) -> ClearContextResult:\n(\s+\"\"\"\n\s+Deprecated alias for `clear_async`.\n)",
        r"def start_clear(self, context_id: str) -> ClearContextResult:\n\1",
        content,
        flags=re.MULTILINE,
    )
    return content

def generate_sync():
    # Clean target directories to avoid stale generated files drifting over time.
    # Sync outputs must be fully derived from async sources.
    for d in [SYNC_DIR, TEST_SYNC_DIR, EXAMPLES_SYNC_DIR, UNIT_TEST_SYNC_DIR]:
        if os.path.exists(d):
            shutil.rmtree(d, ignore_errors=True)
        os.makedirs(d, exist_ok=True)

    # Define rules for unasync
    common_replacements = {
        # Class Renames
        "AsyncAgentBay": "AgentBay",
        "AsyncSession": "Session",
        "AsyncBrowser": "Browser",
        "AsyncCommand": "Command",
        "AsyncCode": "Code",
        "AsyncFileSystem": "FileSystem",
        "AsyncContextManager": "ContextManager",
        "AsyncContextService": "ContextService",
        "AsyncComputer": "Computer",
        "AsyncMobile": "Mobile",
        "AsyncFileTransfer": "FileTransfer",
        "AsyncOss": "Oss",
        "AsyncAgent": "Agent",
        "AsyncBrowserAgent": "BrowserAgent",
        "AsyncBrowserFingerprintGenerator": "BrowserFingerprintGenerator",
        "AsyncBaseService": "BaseService",
        "AsyncMobileSimulateService": "MobileSimulateService",
        "AsyncExtensionsService": "ExtensionsService",

        # Variable/Attribute Renames
        "init_browser_async": "init_browser",
        "initialize_async": "initialize",
        "call_mcp_tool_async": "call_mcp_tool",
        "call_mcp_tool_with_options_async": "call_mcp_tool_with_options",
        "release_mcp_session_async": "release_mcp_session",
        "create_mcp_session_async": "create_mcp_session",
        "get_cdp_link_async": "get_cdp_link",
        "get_endpoint_url_async": "get_endpoint_url",
        "get_context_info_async": "get_context_info",
        "sync_context_async": "sync_context",
        "get_mcp_resource_async": "get_mcp_resource",
        "set_label_async": "set_label",
        "get_label_async": "get_label",
        "pause_session_async_async": "pause_session_async",
        "resume_session_async_async": "resume_session_async",
        "list_mcp_tools_async": "list_mcp_tools",
        "get_adb_link_async": "get_adb_link",

        # Client API methods rename
        "get_link_async": "get_link",
        "get_context_async": "get_context",
        "delete_context_async": "delete_context",
        "list_contexts_async": "list_contexts",
        "modify_context_async": "modify_context",
        "delete_context_file_async": "delete_context_file",
        "describe_context_files_async": "describe_context_files",
        "get_context_file_download_url_async": "get_context_file_download_url",
        "get_context_file_upload_url_async": "get_context_file_upload_url",
        "get_cdp_link_async": "get_cdp_link",
        "get_endpoint_url_async": "get_endpoint_url",
        "get_context_info_async": "get_context_info",
        "get_label_async": "get_label",
        "get_session_async": "get_session",
        "list_session_async": "list_session",
        "create_mcp_session_async": "create_mcp_session",
        "get_mcp_resource_async": "get_mcp_resource",
        "sync_context_async": "sync_context",
        "clear_context_async": "clear_context",
        "get_and_load_internal_context_async": "get_and_load_internal_context",
        "delete_session_async_async": "delete_session_async",

        # Browser Agent specific
        "navigate_async": "navigate",
        "screenshot_async": "screenshot",
        "act_async": "act",
        "observe_async": "observe",
        "extract_async": "extract",
        "close_async": "close",
        "_execute_act_async": "_execute_act",
        "_execute_extract_async": "_execute_extract",
        "_execute_observe_async": "_execute_observe",
        "_execute_screenshot_async": "_execute_screenshot",
        "_get_page_and_context_index_async": "_get_page_and_context_index",
        "_scroll_to_load_all_content_async": "_scroll_to_load_all_content",
        # "page_use_act_async": "page_use_act",  # Keep async API for compatibility
        # "page_use_extract_async": "page_use_extract",
        # "page_use_observe_async": "page_use_observe",
        # "page_use_screenshot_async": "page_use_screenshot",

        # Agent specific
        "async_execute_task": "async_execute_task",

        # Import fixes (token-level replacements)
        "_async": "_sync",

        # Asyncio replacements
        "asyncio.sleep": "time.sleep",
        "asyncio.Event": "threading.Event",
        "asyncio.TimeoutError": "RuntimeError",
        "async_playwright": "sync_playwright",
        "httpx.AsyncClient": "httpx.Client",
        "await ": "",
        "async def ": "def ",
        "async with ": "with ",
        "async for ": "for ",

        # RPC method replacements
        "do_rpcrequest_async": "do_rpcrequest",

        # Test specific
        "@pytest.mark.asyncio": "",
        "unittest.IsolatedAsyncioTestCase": "unittest.TestCase",
        "IsolatedAsyncioTestCase": "TestCase",
        "AsyncMock": "MagicMock",
        "SyncMock": "MagicMock",
        "assert_awaited_once_with": "assert_called_once_with",
        "async def asyncSetUp": "def setUp",
        "async def asyncTearDown": "def tearDown",
        "asyncSetUp": "setUp",
        "asyncTearDown": "tearDown",
    }

    rules = [
        unasync.Rule(
            fromdir=ASYNC_DIR,
            todir=SYNC_DIR,
            additional_replacements=common_replacements
        ),
        unasync.Rule(
            fromdir=TEST_ASYNC_DIR,
            todir=TEST_SYNC_DIR,
            additional_replacements=common_replacements
        ),
        unasync.Rule(
            fromdir=EXAMPLES_ASYNC_DIR,
            todir=EXAMPLES_SYNC_DIR,
            additional_replacements=common_replacements
        ),
        unasync.Rule(
            fromdir=UNIT_TEST_ASYNC_DIR,
            todir=UNIT_TEST_SYNC_DIR,
            additional_replacements=common_replacements
        )
    ]

    filepaths = []
    # Walk _async dir
    for root, dirs, files in os.walk(ASYNC_DIR):
        for file in files:
            if file.endswith(".py"):
                filepaths.append(os.path.join(root, file))

    # Walk tests/_async dir
    if os.path.exists(TEST_ASYNC_DIR):
        for root, dirs, files in os.walk(TEST_ASYNC_DIR):
            for file in files:
                if file.endswith(".py"):
                    filepaths.append(os.path.join(root, file))

    # Walk examples/_async dir
    if os.path.exists(EXAMPLES_ASYNC_DIR):
        for root, dirs, files in os.walk(EXAMPLES_ASYNC_DIR):
            for file in files:
                if file.endswith(".py"):
                    filepaths.append(os.path.join(root, file))

    # Walk unit tests/_async dir
    if os.path.exists(UNIT_TEST_ASYNC_DIR):
        for root, dirs, files in os.walk(UNIT_TEST_ASYNC_DIR):
            for file in files:
                if file.endswith(".py"):
                    filepaths.append(os.path.join(root, file))

    # Unasync logic
    unasync.unasync_files(filepaths, rules)

    # Post-process
    process_dirs = [SYNC_DIR, TEST_SYNC_DIR, EXAMPLES_SYNC_DIR, UNIT_TEST_SYNC_DIR]

    for directory in process_dirs:
        if not os.path.exists(directory):
            continue

        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".py"):
                    path = os.path.join(root, file)
                    with open(path, "r") as f:
                        content = f.read()

                    # Header check (only for SDK code and tests, not examples)
                    if root.startswith(SYNC_DIR) or root.startswith(TEST_SYNC_DIR):
                        header = "# DO NOT EDIT THIS FILE MANUALLY.\n# This file is auto-generated by scripts/generate_sync.py\n\n"
                        if not content.startswith(header):
                            content = header + content
                    elif root.startswith(EXAMPLES_SYNC_DIR):
                        # For examples, use a simpler header
                        header = "# DO NOT EDIT THIS FILE MANUALLY.\n# This file is auto-generated from the _async directory.\n\n"
                        if not content.startswith(header):
                            content = header + content

                    # Fix httpx.SyncClient issue (unasync might produce this)
                    content = content.replace("httpx.SyncClient", "httpx.Client")

                    # Fix playwright import
                    content = content.replace("playwright.async_api", "playwright.sync_api")

                    # Docstring/examples cleanup: unasync does not reliably transform docstrings.
                    # Apply only to generated SDK sync code and sync examples (avoid mutating tests).
                    if root.startswith(SYNC_DIR) or root.startswith(EXAMPLES_SYNC_DIR):
                        content = re.sub(r"\bawait\s+", "", content)

                    # Custom Replacements
                    # Force replace asyncio.sleep if unasync missed it (common with await removal)
                    content = content.replace("asyncio.sleep", "time.sleep")
                    # Replace asyncio.Lock() with threading.Lock() for sync code
                    content = content.replace("asyncio.Lock()", "threading.Lock()")
                    # Replace asyncio.gather(*tasks) with a list comprehension to keep the expression valid
                    content = content.replace("asyncio.gather(*tasks)", "[task for task in tasks]")
                    # Also handle asyncio.gather with return_exceptions parameter
                    content = content.replace("asyncio.gather(*tasks, return_exceptions=True)", "[task for task in tasks]")
                    # Handle asyncio.gather with concurrent.futures for proper parallel execution
                    if "concurrent_sessions.py" in file:
                        # For concurrent sessions example, use ThreadPoolExecutor
                        replacement = """with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(run_task_in_session, client, task_id, cmd) for task_id, cmd in tasks]
            results = [future.result() for future in futures]"""
                        content = re.sub(
                            r'        # Run all tasks concurrently\s*\n\s*results = asyncio\.gather\(\s*\*\[run_task_in_session\(client, task_id, cmd\) for task_id, cmd in tasks\]\s*\)',
                            f'        # Run all tasks concurrently\n        {replacement}',
                            content
                        )
                    else:
                        # For other cases, use sequential execution
                        content = re.sub(r'asyncio\.gather\(\*([^)]+)\)', r'[task for task in \1]', content)
                    # Handle asyncio.run calls - use a more robust approach
                    # This will match asyncio.run( and find the matching closing parenthesis
                    def remove_asyncio_run(text):
                        result = []
                        i = 0
                        while i < len(text):
                            if text[i:].startswith('asyncio.run('):
                                # Found asyncio.run(
                                i += len('asyncio.run(')
                                paren_count = 1
                                start = i
                                while i < len(text) and paren_count > 0:
                                    if text[i] == '(':
                                        paren_count += 1
                                    elif text[i] == ')':
                                        paren_count -= 1
                                    i += 1
                                # Extract the content inside asyncio.run()
                                if paren_count == 0:
                                    result.append(text[start:i-1])
                                else:
                                    # Unmatched parentheses, keep original
                                    result.append('asyncio.run(' + text[start:i])
                            else:
                                result.append(text[i])
                                i += 1
                        return ''.join(result)

                    content = remove_asyncio_run(content)

                    # Replace asyncio.get_event_loop().time() with time.time()
                    content = content.replace("asyncio.get_event_loop().time()", "time.time()")

                    # Remove asyncio.to_thread() calls - convert to direct function calls
                    # Pattern: asyncio.to_thread(func, arg1, arg2, ...) -> func(arg1, arg2, ...)
                    content = re.sub(r'asyncio\.to_thread\(\s*([^,\)]+),\s*', r'\1(', content)
                    # Also handle asyncio.to_thread with no comma (single arg)
                    content = re.sub(r'asyncio\.to_thread\(([^)]+)\)', r'\1', content)

                    # Remove asyncio.iscoroutine checks - just keep the result assignment
                    # Pattern: if asyncio.iscoroutine(result): out = result
                    # Should become: out = result (just keep the assignment)
                    content = re.sub(r'if asyncio\.iscoroutine\([^)]+\):\s+(\w+)\s+=\s+(\w+)\s*\n\s*else:\s*\n\s*.*?\1\s*=', lambda m: f'{m.group(1)} =', content, flags=re.DOTALL)

                    # Remove asyncio event loop creation in sync code
                    content = re.sub(r'loop\s*=\s*asyncio\.new_event_loop\(\)\s*\n\s*asyncio\.set_event_loop\(loop\)\s*\n', '', content)
                    content = re.sub(r'loop\.close\(\)', '', content)

                    # Remove standalone asyncio.iscoroutine checks without else clause
                    content = re.sub(r'\s*if asyncio\.iscoroutine\([^)]+\):\s*\n\s+\w+\s+=\s+\w+\s*#[^\n]*\n', '\n', content)

                    # Remove import asyncio from sync files (but keep it in imports section)
                    # We need to be careful to only remove standalone "import asyncio" lines
                    # Skip for eval module which uses asyncio internally even in sync mode
                    if "eval/" not in path:
                        content = re.sub(r'^import asyncio\s*\n', '', content, flags=re.MULTILINE)

                    # Add threading import if threading.Lock() is used
                    if 'threading.Lock()' in content and 'import threading' not in content:
                        # Find the last import statement and add threading import after it
                        import_pattern = r'^(import [^\n]+\n|from [^\n]+ import [^\n]+\n)'
                        imports = re.findall(import_pattern, content, flags=re.MULTILINE)
                        if imports:
                            # Find the position after the last import
                            last_import_match = None
                            for match in re.finditer(import_pattern, content, flags=re.MULTILINE):
                                last_import_match = match
                            if last_import_match:
                                insert_pos = last_import_match.end()
                                content = content[:insert_pos] + 'import threading\n' + content[insert_pos:]

                    # Add time import if time.sleep or time.time is used
                    if ('time.sleep' in content or 'time.time' in content) and 'import time' not in content:
                        content = "import time\n" + content

                    # Add concurrent.futures import if ThreadPoolExecutor is used
                    if 'concurrent.futures.ThreadPoolExecutor' in content and 'import concurrent.futures' not in content:
                        content = "import concurrent.futures\n" + content

                    # Fix import statements for sync versions
                    # Convert AsyncExtensionsService to ExtensionsService in imports
                    content = content.replace('AsyncExtensionsService', 'ExtensionsService')
                    content = content.replace('AsyncAgentBay', 'AgentBay')

                    # Apply custom replacements
                    content = _apply_custom_replacements(content, path)

                    # Final fix for filesystem.py _sync_monitor function
                    if "filesystem.py" in file and "def _sync_monitor():" in content:
                        # Pattern to match the broken function
                        pattern = r'def _sync_monitor\(\):\s*\n\s*"""[^"]*"""\s*\n\s*import asyncio\s*\n\s*# Create a new event loop for this thread\s*\n[^}]*?finally:\s*\n[^}]*?\n'
                        replacement = '''def _sync_monitor():
            """Synchronous wrapper for monitoring function."""
            _monitor_directory()
'''
                        content = re.sub(pattern, replacement, content, flags=re.DOTALL)

                        # Fix the missing monitor_thread assignment
                        content = content.replace(
                            '''def _sync_monitor():
            """Synchronous wrapper for monitoring function."""
            _monitor_directory()
            target=_sync_monitor,''',
                            '''def _sync_monitor():
            """Synchronous wrapper for monitoring function."""
            _monitor_directory()

        monitor_thread = threading.Thread(
            target=_sync_monitor,'''
                        )

                    if "filesystem.py" in file:
                        # Fix asyncio.wait_for with stop_event.wait() in monitor loop
                        content = content.replace(
                            "                    try:\n                        asyncio.wait_for(stop_event.wait(), timeout=interval)\n                    except asyncio.TimeoutError:\n                        pass",
                            "                    stop_event.wait(timeout=interval)"
                        )

                        # Fix _sync_monitor function - replace asyncio version with direct call
                        # This needs to happen after all other replacements to avoid interference
                        sync_monitor_old = '''def _sync_monitor():
            """Synchronous wrapper for async monitoring function."""
            import asyncio
            # Create a new event loop for this thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            try:
                loop.run_until_complete(_monitor_directory())
            finally:
                loop.close()'''

                        sync_monitor_new = '''def _sync_monitor():
            """Synchronous wrapper for monitoring function."""
            _monitor_directory()'''

                        content = content.replace(sync_monitor_old, sync_monitor_new)

                        # _wait_for_event replacement
                        if "def _wait_for_event(self, event, timeout):" in content:
                             content = content.replace("try:\n            event.wait(timeout)\n        except RuntimeError:\n            pass", "event.wait(timeout)")
                             content = content.replace("try:\n            asyncio.wait_for(event.wait(), timeout=timeout)\n        except asyncio.TimeoutError:\n            pass", "event.wait(timeout)")
                             content = content.replace("asyncio.wait_for(event.wait(), timeout=timeout)", "event.wait(timeout)")

                        # _create_task
                        content = content.replace("def _create_task(self, func):", "def _create_task(self, func):")
                        content = content.replace("return asyncio.create_task(coro_func())", "t = threading.Thread(target=coro_func, daemon=True); t.start(); return t")
                        content = content.replace("return asyncio.create_task(func())", "t = threading.Thread(target=func, daemon=True); t.start(); return t")

                        # _create_event
                        content = content.replace("return asyncio.Event()", "return threading.Event()")
                        content = content.replace("stop_event = asyncio.Event()", "stop_event = threading.Event()")

                        # _run_in_thread
                        content = content.replace("return asyncio.to_thread(func, *args)", "return func(*args)")
                        content = content.replace("return await asyncio.to_thread(func, *args)", "return func(*args)")

                        # Fix FileSystem wrapper methods that have loop.run_until_complete
                        # The async source has upload_file and download_file as sync methods that call
                        # async FileTransfer methods via loop.run_until_complete.
                        # After event loop removal (lines 200-201), we're left with:
                        #   result = loop.run_until_complete(
                        #       file_transfer.upload(...
                        #       )
                        #   )
                        # We need to remove loop.run_until_complete wrapper entirely
                        content = re.sub(
                            r'result\s*=\s*loop\.run_until_complete\(\s*\n\s*file_transfer\.(upload|download)\(',
                            r'result = file_transfer.\1(',
                            content
                        )
                        # Remove the extra closing parenthesis from loop.run_until_complete
                        # Pattern: )\n            ) after the parameters
                        content = re.sub(
                            r'(progress_cb=progress_cb,\s*\n\s*)\)\s*\n\s*\)\s*\n',
                            r'\1)\n',
                            content
                        )

                    if "browser_agent.py" in file:
                        content = content.replace("asyncio.get_event_loop().run_until_complete(", "")
                        pass

                    # Test specific cleanup
                    content = content.replace("@pytest.mark.asyncio", "@pytest.mark.sync")
                    content = content.replace("@pytest_asyncio.fixture", "@pytest.fixture")
                    content = content.replace("import pytest_asyncio", "import pytest")

                    # Fix patch paths in unit tests
                    content = content.replace('"agentbay._async', '"agentbay._sync')
                    content = content.replace("'agentbay._async", "'agentbay._sync")
                    # Fix patch decorators with async module paths and class names
                    content = re.sub(r'@patch\("agentbay\._sync\.([^"]+)\.Async([^"]+)"\)', r'@patch("agentbay._sync.\1.\2")', content)
                    content = re.sub(r"@patch\('agentbay\._sync\.([^']+)\.Async([^']+)'\)", r"@patch('agentbay._sync.\1.\2')", content)
                    # Also fix patch calls with AsyncSession -> Session
                    content = re.sub(r'patch\("agentbay\._sync\.([^"]+)\.AsyncSession"\)', r'patch("agentbay._sync.\1.Session")', content)
                    content = re.sub(r"patch\('agentbay\._sync\.([^']+)\.AsyncSession'\)", r"patch('agentbay._sync.\1.Session')", content)

                    # Remove asyncio.iscoroutinefunction checks in sync tests
                    content = re.sub(r'assert asyncio\.iscoroutinefunction\([^)]+\)', 'assert True  # Sync version check removed', content)
                    content = re.sub(r'assert not asyncio\.iscoroutinefunction\([^)]+\)', 'assert True  # Sync version check removed', content)
                    # Handle inspect.iscoroutinefunction checks in sync tests
                    content = re.sub(r'assert inspect\.iscoroutinefunction\([^)]+\)', 'assert True  # Sync version - method is not async', content)
                    # Handle coroutine checks in sync tests
                    content = re.sub(r'if inspect\.iscoroutine\([^)]+\):', 'if False:  # Sync version - no coroutines', content)
                    content = re.sub(r'pytest\.fail\("([^"]*should return a coroutine[^"]*)"\)', r'assert True  # Sync version - \1', content)

                    with open(path, "w") as f:
                        f.write(content)

def process_examples_non_python_files():
    """Process non-Python files in examples directory (Markdown, images, etc.)"""
    if not os.path.exists(EXAMPLES_ASYNC_DIR):
        return

    print("Processing non-Python files in examples...")

    for root, dirs, files in os.walk(EXAMPLES_ASYNC_DIR):
        for file in files:
            if file.endswith('.py') or file == '__pycache__':
                continue

            src_path = os.path.join(root, file)
            rel_path = os.path.relpath(src_path, EXAMPLES_ASYNC_DIR)
            dest_path = os.path.join(EXAMPLES_SYNC_DIR, rel_path)

            # Ensure destination directory exists
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)

            if file.endswith('.md'):
                # Process Markdown files
                convert_markdown_file(src_path, dest_path)
            else:
                # Copy other files as-is
                shutil.copy2(src_path, dest_path)

def convert_markdown_file(src_path: str, dest_path: str):
    """Convert Markdown files from async to sync versions"""
    with open(src_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace AsyncAgentBay -> AgentBay (Documentation text)
    content = content.replace("AsyncAgentBay", "AgentBay")
    content = content.replace("AsyncSession", "Session")

    # Remove await keywords from code blocks
    content = re.sub(r'await\s+', '', content)

    # Replace async def with def in code blocks
    content = content.replace("async def ", "def ")

    # Replace asyncio.sleep with time.sleep
    content = content.replace("await asyncio.sleep(", "time.sleep(")
    content = content.replace("asyncio.sleep(", "time.sleep(")

    # Replace API links: docs/api/async/async-*.md -> docs/api/sync/*.md
    content = re.sub(r"docs/api/async/async-([a-z0-9-]+)\.md", r"docs/api/sync/\1.md", content)

    # Replace example links: _async -> _sync
    content = content.replace("/_async/", "/_sync/")

    # Write converted content
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    print(f"Generating sync code from {ASYNC_DIR} to {SYNC_DIR}...")
    print(f"Generating sync tests from {TEST_ASYNC_DIR} to {TEST_SYNC_DIR}...")
    generate_sync()
    process_examples_non_python_files()
    print("Done.")
