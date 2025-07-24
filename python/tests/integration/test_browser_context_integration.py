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

    def __init__(self, methodName='runTest'):
        super().__init__(methodName)
        self.first_session_cookies: list = []
        self.first_session_cookie_dict: dict = {}

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
                # cls.agent_bay.context.delete(cls.context)
                print(f"Context deleted: {cls.context.id}")
            except Exception as e:
                print(f"Warning: Failed to delete context: {e}")

    def test_browser_context_cookie_persistence(self):
        """Test that cookies persist across sessions with the same browser context."""
        # Test data
        test_url = "https://www.aliyun.com"

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
            
            # Step 4: Connect with playwright, open aliyun.com and read cookies
            print("Step 4: Opening aliyun.com and reading cookies...")
            async with async_playwright() as p:
                browser = await p.chromium.connect_over_cdp(endpoint_url)
                self.assertIsNotNone(browser, "Failed to connect to browser")
                
                context = browser.contexts[0] if browser.contexts else await browser.new_context()
                page = await context.new_page()
                
                # Navigate to test URL
                await page.goto(test_url)
                print(f"Navigated to {test_url}")
                
                # Wait a bit for cookies to be set by the website
                await page.wait_for_timeout(3000)
                
                # Read cookies from the page
                cookies = await context.cookies()
                cookie_dict = {cookie['name']: cookie['value'] for cookie in cookies}
                
                print(f"Cookies found in first session: {list(cookie_dict.keys())}")
                print(f"Total cookies count: {len(cookies)}")
                
                # Store cookies for comparison in second session
                self.first_session_cookies = cookies
                self.first_session_cookie_dict = cookie_dict
                
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
        
        # Step 7: Get browser object and check if cookies exist without opening any page
        async def second_session_operations():
            print("Step 7: Getting browser object and checking cookie persistence without opening any page...")
            
            # Initialize browser
            init_success = await session2.browser.initialize_async(BrowserOption())
            self.assertTrue(init_success, "Failed to initialize browser in second session")
            print("Second session browser initialized successfully")
            
            # Get endpoint URL
            endpoint_url = session2.browser.get_endpoint_url()
            self.assertIsNotNone(endpoint_url, "Endpoint URL should not be None")
            print(f"Second session browser endpoint URL: {endpoint_url}")
            
            # Connect with playwright and read cookies directly from context without opening any page
            async with async_playwright() as p:
                browser = await p.chromium.connect_over_cdp(endpoint_url)
                self.assertIsNotNone(browser, "Failed to connect to browser in second session")
                
                context = browser.contexts[0] if browser.contexts else await browser.new_context()
                
                # Read cookies directly from context without opening any page
                cookies = await context.cookies()
                cookie_dict = {cookie['name']: cookie['value'] for cookie in cookies}
                
                print(f"Cookies found in second session (without opening page): {list(cookie_dict.keys())}")
                print(f"Total cookies count in second session: {len(cookies)}")
                
                # Compare cookies between sessions
                if self.first_session_cookies and self.first_session_cookie_dict:
                    print(f"First session cookies count: {len(self.first_session_cookies)}")
                    print(f"Second session cookies count: {len(cookies)}")
                    
                    # Check if cookie counts match
                    self.assertEqual(len(cookies), len(self.first_session_cookies), 
                                   f"Cookie count should match between sessions. First: {len(self.first_session_cookies)}, Second: {len(cookies)}")
                    
                    # Check if cookie names match
                    first_cookie_names = set(self.first_session_cookie_dict.keys())
                    second_cookie_names = set(cookie_dict.keys())
                    
                    self.assertEqual(first_cookie_names, second_cookie_names,
                                   f"Cookie names should match between sessions. First: {first_cookie_names}, Second: {second_cookie_names}")
                    
                    # Check if cookie values match for common cookies
                    common_cookies = first_cookie_names.intersection(second_cookie_names)
                    for cookie_name in common_cookies:
                        first_value = self.first_session_cookie_dict[cookie_name]
                        second_value = cookie_dict[cookie_name]
                        self.assertEqual(first_value, second_value,
                                       f"Cookie value for '{cookie_name}' should match between sessions. First: {first_value}, Second: {second_value}")
                    
                    print(f"SUCCESS: Cookies persisted correctly! Found {len(cookies)} cookies in both sessions")
                    print(f"Common cookies: {list(common_cookies)}")
                else:
                    self.fail("First session cookies not available for comparison")
                
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