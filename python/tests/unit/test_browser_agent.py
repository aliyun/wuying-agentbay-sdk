import unittest
import asyncio
from unittest.mock import MagicMock, patch, AsyncMock
from pydantic import BaseModel, Field
from typing import List, Optional

from agentbay.browser.browser import (
    Browser,
    BrowserOption,
    BrowserViewport,
    BrowserScreen,
    BrowserFingerprint
)
from agentbay.browser.browser_agent import (
    BrowserAgent, 
    ActOptions, 
    ActResult, 
    ObserveOptions, 
    ObserveResult, 
    ExtractOptions, 
    BrowserError
)


class TestSchema(BaseModel):
    title: str = Field(..., description="Page title")
    content: Optional[str] = Field(None, description="Page content")


class TestBrowser(unittest.TestCase):
    def setUp(self):
        """Set up test browser."""
        self.mock_session = MagicMock()
        # Configure async mock for init_browser_async
        self.mock_session.get_client().init_browser_async = AsyncMock()
        self.mock_session.get_client().init_browser_async.return_value = MagicMock()
        self.mock_session.get_client().init_browser_async.return_value.to_map.return_value = {
            "body": {"Data": {"Port": 9333}}
        }
        self.browser = Browser(self.mock_session)
        self.browser.agent = MagicMock()

    def test_initialize(self):
        """Test initialize method."""
        self.assertTrue(self.browser.initialize(BrowserOption()))

    def test_initialize_async(self):
        """Test initialize_async method."""
        result = asyncio.run(self.browser.initialize_async(BrowserOption()))
        self.assertTrue(result)

    def test_is_initialized(self):
        """Test is_initialized method."""
        self.assertFalse(self.browser.is_initialized())

    def test_get_endpoint_url(self):
        """Test get_endpoint_url method."""
        self.browser.initialize(BrowserOption())
        self.assertIsNotNone(self.browser.get_endpoint_url())

    def test_get_option(self):
        """Test get_option method."""
        browser_option = BrowserOption(
            use_stealth=True,
            user_agent="User-Agent(By Mock)",
            viewport=BrowserViewport(width=1920, height=1080),
            screen=BrowserScreen(width=1920, height=1080),
            fingerprint=BrowserFingerprint(
                devices=["desktop"],
                operating_systems=["windows", "macos"],
                locales=["zh-CN"],
            )
        )
        self.browser.initialize(browser_option)
        option = self.browser.get_option()
        self.assertIsNotNone(option)
        self.assertEqual(option.use_stealth, True)
        self.assertEqual(option.user_agent, "User-Agent(By Mock)")
        self.assertEqual(option.viewport.width, 1920)
        self.assertEqual(option.viewport.height, 1080)
        self.assertEqual(option.screen.width, 1920)
        self.assertEqual(option.screen.height, 1080)
        self.assertEqual(option.fingerprint.devices, ["desktop"])
        self.assertEqual(option.fingerprint.operating_systems, ["windows", "macos"])
        self.assertEqual(option.fingerprint.locales, ["zh-CN"])

    def test_act(self):
        """Test act method."""
        page = MagicMock()
        self.browser.initialize(BrowserOption())
        self.browser.agent.act(page, ActOptions(action="Click search button"))

    def test_observe(self):
        """Test observe method."""
        page = MagicMock()
        self.browser.initialize(BrowserOption())
        self.browser.agent.observe(page, ObserveOptions(instruction="Find the search button"))

    def test_extract(self):
        """Test extract method."""
        page = MagicMock()
        self.browser.initialize(BrowserOption())
        self.browser.agent.extract(page, ExtractOptions(instruction="Extract the title", schema=TestSchema))

    def test_act_async(self):
        """Test act_async method."""
        page = MagicMock()
        self.browser.initialize(BrowserOption())
        self.browser.agent.act_async(page, ActOptions(action="Click search button"))

    def test_observe_async(self):
        """Test observe_async method."""
        page = MagicMock()
        self.browser.initialize(BrowserOption())
        self.browser.agent.observe_async(page, ObserveOptions(instruction="Find the search button"))

    def test_extract_async(self):
        """Test extract_async method."""
        page = MagicMock()
        self.browser.initialize(BrowserOption())
        self.browser.agent.extract_async(page, ExtractOptions(instruction="Extract the title", schema=TestSchema))

if __name__ == '__main__':
    unittest.main()
