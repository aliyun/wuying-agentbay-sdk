import unittest
import asyncio
from unittest.mock import MagicMock, patch, AsyncMock
from pydantic import BaseModel, Field
from typing import List, Optional

from agentbay.browser.browser import Browser, BrowserOption
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
        self.browser = Browser(self.mock_session)
        self.browser.agent = MagicMock()

    def test_initialize(self):
        """Test initialize method."""
        self.assertTrue(self.browser.initialize(BrowserOption()))

    def test_initialize_async(self):
        """Test initialize_async method."""
        self.assertTrue(self.browser.initialize_async(BrowserOption()))

    def test_is_initialized(self):
        """Test is_initialized method."""
        self.assertFalse(self.browser.is_initialized())

    def test_get_endpoint_url(self):
        """Test get_endpoint_url method."""
        self.browser.initialize(BrowserOption())
        self.assertIsNotNone(self.browser.get_endpoint_url())

    def test_get_option(self):
        """Test get_option method."""
        self.browser.initialize(BrowserOption())
        self.assertIsNotNone(self.browser.get_option())

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
