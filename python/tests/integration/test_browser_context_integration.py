#!/usr/bin/env python3
"""
Integration test for browser context functionality.
This test verifies that browser context (cookies, localStorage, etc.) can be persisted 
across sessions using the same ContextId.
"""

import asyncio
import os
import time
import unittest
from agentbay import AgentBay
from agentbay.session_params import CreateSessionParams, BrowserContext
from agentbay.browser.browser import BrowserOption
from playwright.async_api import async_playwright


def get_test_api_key():
    """Get API key for testing"""
    api_key = os.environ.get("AGENTBAY_API_KEY")
    if not api_key:
        raise unittest.SkipTest("AGENTBAY_API_KEY environment variable not set")
    return api_key


class TestBrowserContextIntegration(unittest.TestCase):
    """Integration tests for browser context persistence functionality."""

    @classmethod
    def setUpClass(cls):
        # Skip if no API key is available or in CI environment
        api_key = os.environ.get("AGENTBAY_API_KEY")
        if not api_key or os.environ.get("CI"):
            raise unittest.SkipTest(
                "Skipping integration test: No API key available or running in CI"
            )

        # Initialize AgentBay client
        cls.agent_bay = AgentBay(api_key)

        # Create a unique context name for this test
        cls.context_name = f"test-browser-context-{int(time.time())}"

        # Create a context
        context_result = cls.agent_bay.context.get(cls.context_name, True)
        if not context_result.success or not context_result.context:
            raise unittest.SkipTest("Failed to create context")

        cls.context = context_result.context
        print(f"Created context: {cls.context.name} (ID: {cls.context.id})")

    @classmethod
    def tearDownClass(cls):
        # Clean up context
        if hasattr(cls, "context"):
            try:
                cls.agent_bay.context.delete(cls.context)
                print(f"Context deleted: {cls.context.id}")
            except Exception as e:
                print(f"Warning: Failed to delete context: {e}")

    def test_browser_context_cookie_persistence(self):
        """Test that cookies persist across sessions with the same browser context."""
        # Test data
        test_cookie_name = "test_cookie"
        test_cookie_value = f"test_value_{int(time.time())}"
        test_url = "https://www.example.com"

        # Step 1 & 2: Create ContextId and create session with BrowserContext
        print(f"Step 1-2: Creating session with browser context ID: {self.context.id}")
        browser_context = BrowserContext(self.context.id, auto_upload=True)
        params = CreateSessionParams(
            image_id="imgc-wucyOiPmeV2Z753lq",
            browser_context=browser_context
        )
        
        session_result = self.agent_bay.create(params)
        self.assertTrue(session_result.success, "Failed to create first session")
        self.assertIsNotNone(session_result.session, "Session should not be None")
        
        session1 = session_result.session
        assert session1 is not None  # Type narrowing for linter
        print(f"First session created with ID: {session1.session_id}")

        # Step 3: Get browser object through initialize_async and get_endpoint_url
        async def first_session_operations():
            print("Step 3: Initializing browser and getting browser object...")
            
            # Initialize browser
            init_success = await session1.browser.initialize_async(BrowserOption())
            self.assertTrue(init_success, "Failed to initialize browser")
            print("Browser initialized successfully")
            
            # Get endpoint URL
            endpoint_url = session1.browser.get_endpoint_url()
            self.assertIsNotNone(endpoint_url, "Endpoint URL should not be None")
            print(f"Browser endpoint URL: {endpoint_url}")
            
            # Step 4: Connect with playwright and write cookies
            print("Step 4: Writing cookies to browser...")
            async with async_playwright() as p:
                browser = await p.chromium.connect_over_cdp(endpoint_url)
                self.assertIsNotNone(browser, "Failed to connect to browser")
                
                context = browser.contexts[0] if browser.contexts else await browser.new_context()
                page = await context.new_page()
                
                # Navigate to test URL
                await page.goto(test_url)
                print(f"Navigated to {test_url}")
                
                # Add test cookie
                await context.add_cookies([{
                    'name': test_cookie_name,
                    'value': test_cookie_value,
                    'domain': '.example.com',
                    'path': '/',
                }])
                print(f"Added cookie: {test_cookie_name}={test_cookie_value}")
                
                # Verify cookie was added
                cookies = await context.cookies()
                cookie_names = [cookie['name'] for cookie in cookies]
                self.assertIn(test_cookie_name, cookie_names, "Test cookie should be present")
                
                await browser.close()
                print("First session browser operations completed")

        # Run first session operations
        asyncio.run(first_session_operations())
        
        # Step 5: Release session with syncContext=True
        print("Step 5: Releasing first session with syncContext=True...")
        delete_result = self.agent_bay.delete(session1, sync_context=True)
        self.assertTrue(delete_result.success, "Failed to delete first session")
        print(f"First session deleted successfully (RequestID: {delete_result.request_id})")
        
        # Wait for context sync to complete
        time.sleep(3)
        
        # Step 6: Create second session with same ContextId
        print(f"Step 6: Creating second session with same context ID: {self.context.id}")
        session_result2 = self.agent_bay.create(params)
        self.assertTrue(session_result2.success, "Failed to create second session")
        self.assertIsNotNone(session_result2.session, "Second session should not be None")
        
        session2 = session_result2.session
        assert session2 is not None  # Type narrowing for linter
        print(f"Second session created with ID: {session2.session_id}")
        
        # Step 7: Get browser object and check if cookies exist
        async def second_session_operations():
            print("Step 7: Getting browser object and checking cookie persistence...")
            
            # Initialize browser
            init_success = await session2.browser.initialize_async(BrowserOption())
            self.assertTrue(init_success, "Failed to initialize browser in second session")
            print("Second session browser initialized successfully")
            
            # Get endpoint URL
            endpoint_url = session2.browser.get_endpoint_url()
            self.assertIsNotNone(endpoint_url, "Endpoint URL should not be None")
            print(f"Second session browser endpoint URL: {endpoint_url}")
            
            # Connect with playwright and check cookies
            async with async_playwright() as p:
                browser = await p.chromium.connect_over_cdp(endpoint_url)
                self.assertIsNotNone(browser, "Failed to connect to browser in second session")
                
                context = browser.contexts[0] if browser.contexts else await browser.new_context()
                page = await context.new_page()
                
                # Navigate to test URL
                await page.goto(test_url)
                print(f"Navigated to {test_url} in second session")
                
                # Check if cookie exists
                cookies = await context.cookies()
                cookie_dict = {cookie['name']: cookie['value'] for cookie in cookies}
                
                print(f"Cookies found in second session: {list(cookie_dict.keys())}")
                
                # Verify our test cookie persisted
                self.assertIn(test_cookie_name, cookie_dict, 
                            f"Cookie '{test_cookie_name}' should persist across sessions")
                self.assertEqual(cookie_dict[test_cookie_name], test_cookie_value,
                               f"Cookie value should be '{test_cookie_value}'")
                
                print(f"SUCCESS: Cookie persisted! {test_cookie_name}={cookie_dict[test_cookie_name]}")
                
                await browser.close()
                print("Second session browser operations completed")

        # Run second session operations
        asyncio.run(second_session_operations())
        
        # Clean up second session
        print("Cleaning up second session...")
        delete_result2 = self.agent_bay.delete(session2)
        self.assertTrue(delete_result2.success, "Failed to delete second session")
        print(f"Second session deleted successfully (RequestID: {delete_result2.request_id})")
        
        print("Browser context persistence test completed successfully!")


if __name__ == "__main__":
    unittest.main() 