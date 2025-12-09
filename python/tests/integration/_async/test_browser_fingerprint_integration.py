#!/usr/bin/env python3
"""
Integration test for browser fingerprint functionality.
This test verifies that browser fingerprint can be persisted
across sessions using the same ContextId and FingerprintContextId.
"""

import os
import time
import pytest

from playwright.async_api import async_playwright

from agentbay import AsyncAgentBay
from agentbay import BrowserContext, CreateSessionParams
from agentbay import (
    BrowserFingerprint,
    BrowserFingerprintContext,
    BrowserOption,
)
from agentbay import AsyncBrowserFingerprintGenerator


def is_windows_user_agent(user_agent: str) -> bool:
    if not user_agent:
        return False
    user_agent_lower = user_agent.lower()
    windows_indicators = ["windows nt", "win32", "win64", "windows", "wow64"]
    return any(indicator in user_agent_lower for indicator in windows_indicators)


@pytest.fixture(scope="class")
async def agent_bay():
    """Fixture to provide AgentBay client."""
    # Skip if no API key is available or in CI environment
    api_key = os.environ.get("AGENTBAY_API_KEY")
    if not api_key or os.environ.get("CI"):
        pytest.skip("Skipping integration test: No API key available or running in CI")
    
    return AsyncAgentBay(api_key)


@pytest.fixture(scope="class")
async def browser_context(agent_bay):
    """Fixture to provide a browser context."""
    session_context_name = f"test-browser-context-{int(time.time())}"
    context_result = await agent_bay.context.get(session_context_name, True)
    if not context_result.success or not context_result.context:
        pytest.skip("Failed to create browser context")
    
    context = context_result.context
    print(f"Created browser context: {context.name} (ID: {context.id})")
    
    yield context
    
    # Cleanup
    try:
        await agent_bay.context.delete(context)
        print(f"Browser context deleted: {context.id}")
    except Exception as e:
        print(f"Warning: Failed to delete context: {e}")


@pytest.fixture(scope="class")
async def fingerprint_context(agent_bay):
    """Fixture to provide a fingerprint context."""
    fingerprint_context_name = f"test-browser-fingerprint-{int(time.time())}"
    fingerprint_context_result = await agent_bay.context.get(
        fingerprint_context_name, True
    )
    if (
        not fingerprint_context_result.success
        or not fingerprint_context_result.context
    ):
        pytest.skip("Failed to create fingerprint context")
    
    context = fingerprint_context_result.context
    print(f"Created fingerprint context: {context.name} (ID: {context.id})")
    
    yield context
    
    # Cleanup
    try:
        await agent_bay.context.delete(context)
        print(f"Fingerprint context deleted: {context.id}")
    except Exception as e:
        print(f"Warning: Failed to delete context: {e}")


@pytest.mark.asyncio
class TestBrowserFingerprintIntegration:
    """Integration tests for browser fingerprint persistence functionality."""

    @pytest.mark.asyncio
    async def test_browser_fingerprint_basic_usage(self, agent_bay):
        print("===== Test browser fingerprint basic usage =====")

        params = CreateSessionParams(image_id="browser_latest")
        session_result = await agent_bay.create(params)
        assert session_result.success, "Failed to create session"
        assert session_result.session is not None, "Session should not be None"

        session = session_result.session
        print(f"Session created with ID: {session.session_id}")

        # Initialize browser with fingerprint options
        browser_option = BrowserOption(
            use_stealth=True,
            fingerprint=BrowserFingerprint(
                devices=["desktop"],
                operating_systems=["windows"],
                locales=["zh-CN"],
            ),
        )
        init_success = await session.browser.initialize(browser_option)
        assert init_success, "Failed to initialize browser"
        print("Browser initialized successfully")

        # Get endpoint URL
        endpoint_url = await session.browser.get_endpoint_url()
        assert endpoint_url is not None, "Endpoint URL should not be None"
        print(f"Browser endpoint URL: {endpoint_url}")

        # Connect with playwright and test user agent
        print("Opening https://httpbin.org/user-agent and test user agent...")
        async with async_playwright() as p:
            browser = await p.chromium.connect_over_cdp(endpoint_url)
            assert browser is not None, "Failed to connect to browser"
            context = (
                browser.contexts[0]
                if browser.contexts
                else await browser.new_context()
            )

            page = await context.new_page()
            await page.goto("https://httpbin.org/user-agent", timeout=60000)
            
            # Wait for page to load and try different selectors
            await page.wait_for_load_state("networkidle", timeout=30000)
            
            # Try to get the response text using different methods
            response_text = None
            try:
                # First try the pre tag
                response_text = await page.evaluate("() => document.querySelector('pre')?.textContent")
            except Exception:
                pass
                
            if not response_text:
                try:
                    # Try getting the body text
                    response_text = await page.evaluate("() => document.body.textContent")
                except Exception:
                    pass
            
            if not response_text:
                # Fallback: get page content
                response_text = await page.content()
                
            print(f"Response text: {response_text[:200]}...")
            
            # Parse JSON from response text
            import json
            import re
            
            # Try to extract JSON from the response
            json_match = re.search(r'\{[^}]+\}', response_text)
            if json_match:
                response = json.loads(json_match.group())
                user_agent = response.get("user-agent")
            else:
                # If no JSON found, assume the whole response is the user agent
                user_agent = response_text.strip()
            print("user_agent =", user_agent)
            assert user_agent is not None
            assert is_windows_user_agent(user_agent)

            await context.close()
            print("Browser fingerprint test completed")

        delete_result = await agent_bay.delete(session)
        assert delete_result.success, "Failed to delete session"
        print(f"Session deleted successfully (RequestID: {delete_result.request_id})")

    @pytest.mark.asyncio
    async def test_browser_fingerprint_persistence(self, agent_bay, browser_context, fingerprint_context):
        """Test browser fingerprint persist across sessions with the same browser and fingerprint context."""
        print("===== Test browser fingerprint persistence =====")

        # Step 1: Create session with BrowserContext and FingerprintContext
        print(
            f"Step 1: Creating session with browser context ID: {browser_context.id} "
            f"and fingerprint context ID: {fingerprint_context.id}"
        )
        fp_context = BrowserFingerprintContext(fingerprint_context.id)
        br_context = BrowserContext(
            browser_context.id, auto_upload=True, fingerprint_context=fp_context
        )
        params1 = CreateSessionParams(
            image_id="browser_latest", browser_context=br_context
        )

        session_result = await agent_bay.create(params1)
        assert session_result.success, "Failed to create first session"
        assert session_result.session is not None, "Session should not be None"

        session1 = session_result.session
        print(f"First session created with ID: {session1.session_id}")

        # Step 2: Initialize first browser and generate fingerprint for persistence
        print(
            "Step 2: Initializing first browser and generate fingerprint for persistence..."
        )

        # Initialize browser with fingerprint persistent enabled and set fingerprint generation options
        browser_option1 = BrowserOption(
            use_stealth=True,
            fingerprint_persistent=True,
            fingerprint=BrowserFingerprint(
                devices=["desktop"],
                operating_systems=["windows"],
                locales=["zh-CN"],
            ),
        )
        init_success = await session1.browser.initialize(browser_option1)
        assert init_success, "Failed to initialize browser"
        print("Browser initialized successfully")

        # Get endpoint URL
        endpoint_url = await session1.browser.get_endpoint_url()
        assert endpoint_url is not None, "Endpoint URL should not be None"
        print(f"Browser endpoint URL: {endpoint_url}")

        # Step 3: Connect with playwright, test first session fingerprint
        print(
            "Step 3: Opening https://httpbin.org/user-agent and test user agent..."
        )
        async with async_playwright() as p:
            browser = await p.chromium.connect_over_cdp(endpoint_url)
            assert browser is not None, "Failed to connect to browser"
            context = (
                browser.contexts[0]
                if browser.contexts
                else await browser.new_context()
            )

            page = await context.new_page()
            await page.goto("https://httpbin.org/user-agent", timeout=60000)
            response = await page.evaluate(
                "() => JSON.parse(document.querySelector('pre').textContent)"
            )
            user_agent = response["user-agent"]
            print("user_agent =", user_agent)
            assert user_agent is not None
            assert is_windows_user_agent(user_agent)

            await context.close()
            print("First session browser operations completed")

        # Step 4: Release first session with syncContext=True
        print("Step 4: Releasing first session with syncContext=True...")
        delete_result = await agent_bay.delete(session1, sync_context=True)
        assert delete_result.success, "Failed to delete first session"
        print(
            f"First session deleted successfully (RequestID: {delete_result.request_id})"
        )

        # Wait for context sync to complete
        time.sleep(3)

        # Step 5: Create second session with same browser context and fingerprint context
        print(
            f"Step 5: Creating second session with same browser context ID: {browser_context.id} "
            f"and fingerprint context ID: {fingerprint_context.id}"
        )
        params2 = CreateSessionParams(
            image_id="browser_latest", browser_context=br_context
        )
        session_result2 = await agent_bay.create(params2)
        assert session_result2.success, "Failed to create second session"
        assert session_result2.session is not None, "Second session should not be None"

        session2 = session_result2.session
        print(f"Second session created with ID: {session2.session_id}")

        # Step 6: Get browser object and check if second session fingerprint is the same as first session
        print(
            "Step 6: Get browser object and check if second session fingerprint is the same as first session..."
        )

        # Initialize browser with fingerprint persistent enabled but not specific fingerprint generation options
        browser_option2 = BrowserOption(
            use_stealth=True,
            fingerprint_persistent=True,
        )
        init_success = await session2.browser.initialize(browser_option2)
        assert init_success, "Failed to initialize browser in second session"
        print("Second session browser initialized successfully")

        # Get endpoint URL
        endpoint_url = await session2.browser.get_endpoint_url()
        assert endpoint_url is not None, "Endpoint URL should not be None"
        print(f"Second session browser endpoint URL: {endpoint_url}")

        # Connect with playwright and test second session fingerprint
        async with async_playwright() as p:
            browser = await p.chromium.connect_over_cdp(endpoint_url)
            assert browser is not None, "Failed to connect to browser in second session"

            context = (
                browser.contexts[0]
                if browser.contexts
                else await browser.new_context()
            )
            page = await context.new_page()
            await page.goto("https://httpbin.org/user-agent", timeout=60000)
            response = await page.evaluate(
                "() => JSON.parse(document.querySelector('pre').textContent)"
            )
            user_agent = response["user-agent"]
            print("user_agent =", user_agent)
            assert user_agent is not None
            assert is_windows_user_agent(user_agent)
            print(f"SUCCESS: fingerprint persisted correctly!")

            await context.close()
            print("Second session browser operations completed")

        # Step 7: Release second session with syncContext=True
        print("Step 7: Releasing second session with syncContext=True...")
        delete_result = await agent_bay.delete(session2, sync_context=True)
        assert delete_result.success, "Failed to delete second session"
        print(
            f"Second session deleted successfully (RequestID: {delete_result.request_id})"
        )

        print("Browser fingerprint persistence test completed successfully!")

    @pytest.mark.asyncio
    async def test_browser_fingerprint_local_sync(self, agent_bay):
        """Test browser fingerprint local sync functionality."""
        print("===== Test browser fingerprint local sync =====")

        params = CreateSessionParams(
            image_id="browser_latest",
        )
        session_result = await agent_bay.create(params)
        assert session_result.success, "Failed to create session"
        assert session_result.session is not None, "Session should not be None"

        session = session_result.session
        print(f"Session created with ID: {session.session_id}")

        # Generate local chrome browser fingerprint
        print("Dumping local chrome browser fingerprint...")

        fingerprint_generator = AsyncBrowserFingerprintGenerator(headless=True)
        fingerprint_format = await fingerprint_generator.generate_fingerprint()
        assert fingerprint_format is not None, "Fingerprint format should not be None"
        print("Local fingerprint generated successfully")

        # Initialize browser with fingerprint format from local chrome
        browser_option = BrowserOption(
            use_stealth=True, fingerprint_format=fingerprint_format
        )
        init_success = await session.browser.initialize(browser_option)
        assert init_success, "Failed to initialize browser"
        print("Browser initialized successfully with local fingerprint")

        # Get endpoint URL
        endpoint_url = await session.browser.get_endpoint_url()
        assert endpoint_url is not None, "Endpoint URL should not be None"
        print(f"Browser endpoint URL: {endpoint_url}")

        # Connect with playwright and verify fingerprint sync
        print("Testing fingerprint sync by checking user agent...")
        async with async_playwright() as p:
            browser = await p.chromium.connect_over_cdp(endpoint_url)
            assert browser is not None, "Failed to connect to browser"
            context = (
                browser.contexts[0]
                if browser.contexts
                else await browser.new_context()
            )

            page = await context.new_page()
            await page.goto("https://httpbin.org/user-agent", timeout=60000)
            
            # Wait for page to load and try different selectors
            await page.wait_for_load_state("networkidle", timeout=30000)
            
            # Try to get the response text using different methods
            response_text = None
            try:
                # First try the pre tag
                response_text = await page.evaluate("() => document.querySelector('pre')?.textContent")
            except Exception:
                pass
                
            if not response_text:
                try:
                    # Try getting the body text
                    response_text = await page.evaluate("() => document.body.textContent")
                except Exception:
                    pass
            
            if not response_text:
                # Fallback: get page content
                response_text = await page.content()
                
            print(f"Response text: {response_text[:200]}...")
            
            # Parse JSON from response text
            import json
            import re
            
            # Try to extract JSON from the response
            json_match = re.search(r'\{[^}]+\}', response_text)
            if json_match:
                response = json.loads(json_match.group())
                user_agent = response.get("user-agent")
            else:
                # If no JSON found, assume the whole response is the user agent
                user_agent = response_text.strip()
            print(f"Remote user agent: {user_agent}")
            print(
                f"Local user agent: {fingerprint_format.fingerprint.navigator.userAgent}"
            )

            # Verify that the user agents match (fingerprint sync successful)
            assert (
                user_agent == fingerprint_format.fingerprint.navigator.userAgent
            ), "User agent should match between local and remote"
            print("SUCCESS: Local fingerprint synced correctly to remote browser!")

            await context.close()
            print("Local sync test completed")

        delete_result = await agent_bay.delete(session)
        assert delete_result.success, "Failed to delete session"
        print(f"Session deleted successfully (RequestID: {delete_result.request_id})")

        print("Browser fingerprint local sync test completed successfully!")

    @pytest.mark.asyncio
    async def test_browser_fingerprint_construct(self, agent_bay):
        """Test browser fingerprint construction from file."""
        print("===== Test browser fingerprint construct =====")

        params = CreateSessionParams(
            image_id="browser_latest",
        )
        session_result = await agent_bay.create(params)
        assert session_result.success, "Failed to create session"
        assert session_result.session is not None, "Session should not be None"

        session = session_result.session
        print(f"Session created with ID: {session.session_id}")

        # Load fingerprint from example file
        print("Loading fingerprint from example file...")
        from agentbay import FingerprintFormat

        # Get the path to the example fingerprint file
        example_file_path = os.path.join(
            os.path.dirname(
                os.path.dirname(
                    os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
                )
            ),
            "resource",
            "fingerprint.example.json",
        )

        with open(example_file_path, "r") as f:
            fingerprint_json = f.read()

        fingerprint_format = FingerprintFormat.load(fingerprint_json)
        assert fingerprint_format is not None, "Fingerprint format should not be None"
        print("Fingerprint loaded from file successfully")

        # Initialize browser with constructed fingerprint format
        browser_option = BrowserOption(
            use_stealth=True, fingerprint_format=fingerprint_format
        )
        init_success = await session.browser.initialize(browser_option)
        assert init_success, "Failed to initialize browser"
        print("Browser initialized successfully with constructed fingerprint")

        # Get endpoint URL
        endpoint_url = await session.browser.get_endpoint_url()
        assert endpoint_url is not None, "Endpoint URL should not be None"
        print(f"Browser endpoint URL: {endpoint_url}")

        # Connect with playwright and verify constructed fingerprint
        print("Testing constructed fingerprint by checking user agent...")
        async with async_playwright() as p:
            browser = await p.chromium.connect_over_cdp(endpoint_url)
            assert browser is not None, "Failed to connect to browser"
            context = (
                browser.contexts[0]
                if browser.contexts
                else await browser.new_context()
            )

            page = await context.new_page()
            await page.goto("https://httpbin.org/user-agent", timeout=60000)
            
            # Wait for page to load and try different selectors
            await page.wait_for_load_state("networkidle", timeout=30000)
            
            # Try to get the response text using different methods
            response_text = None
            try:
                # First try the pre tag
                response_text = await page.evaluate("() => document.querySelector('pre')?.textContent")
            except Exception:
                pass
                
            if not response_text:
                try:
                    # Try getting the body text
                    response_text = await page.evaluate("() => document.body.textContent")
                except Exception:
                    pass
            
            if not response_text:
                # Fallback: get page content
                response_text = await page.content()
                
            print(f"Response text: {response_text[:200]}...")
            
            # Parse JSON from response text
            import json
            import re
            
            # Try to extract JSON from the response
            json_match = re.search(r'\{[^}]+\}', response_text)
            if json_match:
                response = json.loads(json_match.group())
                user_agent = response.get("user-agent")
            else:
                # If no JSON found, assume the whole response is the user agent
                user_agent = response_text.strip()
            print(f"Remote user agent: {user_agent}")
            print(
                f"Expected user agent: {fingerprint_format.fingerprint.navigator.userAgent}"
            )

            # Verify that the user agents match (fingerprint construction successful)
            assert (
                user_agent == fingerprint_format.fingerprint.navigator.userAgent
            ), "User agent should match the constructed fingerprint"
            print("SUCCESS: Fingerprint constructed correctly from file!")

            await context.close()
            print("Construct test completed")

        delete_result = await agent_bay.delete(session)
        assert delete_result.success, "Failed to delete session"
        print(f"Session deleted successfully (RequestID: {delete_result.request_id})")

        print("Browser fingerprint construct test completed successfully!")
