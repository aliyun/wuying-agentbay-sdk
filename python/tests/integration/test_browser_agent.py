import json
import os
import random
import sys
import time
import unittest
from agentbay.browser import Browser, BrowserOption, BrowserFingerprint
from agentbay.browser.browser_agent import ActOptions, ExtractOptions, ObserveOptions, ActResult, ObserveResult
from playwright.sync_api import sync_playwright
from pydantic import BaseModel
from agentbay.model.response import SessionResult

# Add the parent directory to the path so we can import the agentbay package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agentbay import AgentBay
from agentbay.exceptions import AgentBayError
from agentbay.session_params import CreateSessionParams

class DummySchema(BaseModel):
    title: str

def get_test_api_key():
    """Get API key for testing"""
    api_key = os.environ.get("AGENTBAY_API_KEY")
    if not api_key:
        api_key = "akm-xxx"  # Replace with your test API key
        print(
            "Warning: Using default API key. Set AGENTBAY_API_KEY environment variable for testing."
        )
    return api_key

def is_windows_user_agent(user_agent: str) -> bool:
    if not user_agent:
        return False
    user_agent_lower = user_agent.lower()
    windows_indicators = [
        'windows nt',
        'win32',
        'win64',
        'windows',
        'wow64'
    ]
    return any(indicator in user_agent_lower for indicator in windows_indicators)

class TestBrowserAgentIntegration(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        api_key = get_test_api_key()
        print("api_key =", api_key)
        self.agent_bay = AgentBay(api_key=api_key)

        # Create a session
        print("Creating a new session for browser agent testing...")
        session_param = CreateSessionParams()
        session_param.image_id = "browser_latest"
        result = self.agent_bay.create(session_param)
        self.assertTrue(result.success)
        self.session = result.session
        print(f"Session created with ID: {self.session.session_id}")

    def tearDown(self):
        """Tear down test fixtures."""
        print("Cleaning up: Deleting the session...")
        try:
            self.agent_bay.delete(self.session)
        except Exception as e:
            print(f"Warning: Error deleting session: {e}")

    def test_initialize_browser(self):
        browser = self.session.browser
        self.assertIsNotNone(browser)
        self.assertIsInstance(browser, Browser)

        self.assertTrue(browser.initialize(BrowserOption()))

        endpoint_url = browser.get_endpoint_url()
        print("endpoint_url =", endpoint_url)
        self.assertTrue(endpoint_url is not None)

        time.sleep(10)

        from playwright.sync_api import sync_playwright
        p = sync_playwright().start()
        playwright_browser = p.chromium.connect_over_cdp(endpoint_url)
        self.assertTrue(playwright_browser is not None)

        page = playwright_browser.new_page()
        page.goto("http://www.baidu.com")
        print("page.title() =", page.title())

        self.assertTrue(page.title() is not None)
        page.close()

    def test_initialize_browser_with_fingerprint(self):
        browser = self.session.browser
        self.assertIsNotNone(browser)
        self.assertIsInstance(browser, Browser)
        option = BrowserOption(
            use_stealth=True,
            fingerprint=BrowserFingerprint(
                devices=["desktop"],
                operating_systems=["windows"],
                locales=["zh-CN"],
            )
        )
        self.assertTrue(browser.initialize(option))

        endpoint_url = browser.get_endpoint_url()
        print("endpoint_url =", endpoint_url)
        self.assertTrue(endpoint_url is not None)

        time.sleep(10)

        from playwright.sync_api import sync_playwright
        p = sync_playwright().start()
        playwright_browser = p.chromium.connect_over_cdp(endpoint_url)
        self.assertTrue(playwright_browser is not None)
        default_context = playwright_browser.contexts[0]
        self.assertTrue(default_context is not None)

        page = default_context.new_page()
        page.goto("https://httpbin.org/user-agent", timeout=60000)
        response = page.evaluate("() => JSON.parse(document.body.textContent)")
        user_agent = response["user-agent"]
        print("user_agent =", user_agent)
        self.assertTrue(user_agent is not None)
        is_windows = is_windows_user_agent(user_agent)
        self.assertTrue(is_windows)

        page.close()

    def test_act_success(self):
        browser = self.session.browser
        self.assertIsNotNone(browser)
        self.assertIsInstance(browser, Browser)

        self.assertTrue(browser.initialize(BrowserOption()))

        endpoint_url = browser.get_endpoint_url()
        print("endpoint_url =", endpoint_url)
        self.assertTrue(endpoint_url is not None)

        from playwright.sync_api import sync_playwright
        p = sync_playwright().start()
        playwright_browser = p.chromium.connect_over_cdp(endpoint_url)
        self.assertTrue(playwright_browser is not None)

        page = playwright_browser.new_page()
        page.goto("http://www.baidu.com")
        self.assertTrue(page.title() is not None)

        result = browser.agent.act(page, ActOptions(action="Click search button"))
        print("result =", result)

        self.assertTrue(result.success)
        self.assertIsInstance(result, ActResult)

        page.close()

    def test_observe_success(self):
        browser = self.session.browser
        self.assertIsNotNone(browser)
        self.assertIsInstance(browser, Browser)

        self.assertTrue(browser.initialize(BrowserOption()))

        endpoint_url = browser.get_endpoint_url()
        print("endpoint_url =", endpoint_url)
        self.assertTrue(endpoint_url is not None)

        from playwright.sync_api import sync_playwright
        p = sync_playwright().start()
        playwright_browser = p.chromium.connect_over_cdp(endpoint_url)
        self.assertTrue(playwright_browser is not None)

        page = playwright_browser.new_page()
        page.goto("http://www.baidu.com")
        self.assertTrue(page.title() is not None)

        result, observe_results = browser.agent.observe(page, ObserveOptions(instruction="Find the search button"))
        print("result =", result)
        print("observe_results =", observe_results)

        self.assertTrue(result)
        self.assertIsInstance(observe_results[0], ObserveResult)

        page.close()

    def test_extract_success(self):
        browser = self.session.browser
        self.assertIsNotNone(browser)
        self.assertIsInstance(browser, Browser)

        self.assertTrue(browser.initialize(BrowserOption()))

        endpoint_url = browser.get_endpoint_url()
        print("endpoint_url =", endpoint_url)
        self.assertTrue(endpoint_url is not None)

        from playwright.sync_api import sync_playwright
        p = sync_playwright().start()
        playwrigt_browser = p.chromium.connect_over_cdp(endpoint_url)
        self.assertTrue(playwrigt_browser is not None)

        page = playwrigt_browser.new_page()
        page.goto("http://www.baidu.com")
        self.assertTrue(page.title() is not None)

        result, objs = browser.agent.extract(page, ExtractOptions(instruction="Extract the title", schema=DummySchema))
        print("result =", result)
        print("objs =", objs)
        self.assertTrue(result)
        self.assertIsInstance(objs[0], DummySchema)

        page.close()

if __name__ == "__main__":
    unittest.main() 