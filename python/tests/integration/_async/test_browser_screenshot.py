"""Integration tests for browser screenshots."""

import asyncio
import os
import time
import pytest
import pytest_asyncio
from playwright.async_api import async_playwright

# Ensure tmp directory exists for screenshots
os.makedirs("./tmp", exist_ok=True)

from agentbay import AsyncAgentBay
from agentbay import CreateSessionParams
from agentbay import BrowserOption
from agentbay import BrowserError


def get_test_api_key():
    """Get API key for testing"""
    api_key = os.environ.get("AGENTBAY_API_KEY")
    if not api_key:
        api_key = "akm-xxx"
        print(
            "Warning: Using default API key. Set AGENTBAY_API_KEY environment variable for testing."
        )
    return api_key


@pytest_asyncio.fixture
async def browser_session():
    api_key = get_test_api_key()
    agent_bay = AsyncAgentBay(api_key=api_key)
    params = CreateSessionParams(image_id="browser_latest")
    result = await agent_bay.create(params)
    assert result.success

    # Initialize browser for all tests (except the one testing initialization check)
    # But fixture should probably just provide session. Tests can initialize if needed.
    # However, most tests need initialized browser.

    yield result.session

    try:
        await result.session.delete()
    except Exception as e:
        print(f"Warning: Failed to delete session: {e}")


@pytest.mark.asyncio
async def test_screenshot_with_valid_page(browser_session):
    """Test taking screenshot with a valid page."""
    print("\n=== Testing screenshot with valid page ===")
    browser = browser_session.browser
    await browser.initialize(BrowserOption())

    endpoint_url = await browser.get_endpoint_url()

    async with async_playwright() as p:
        playwright_browser = await p.chromium.connect_over_cdp(endpoint_url)
        contexts = playwright_browser.contexts
        context = contexts[0] if contexts else await playwright_browser.new_context()
        pages = context.pages
        page = pages[0] if pages else await context.new_page()
        await page.goto("https://www.baidu.com", timeout=30000)

        try:
            # Take screenshot with default full_page=False
            screenshot_data = await browser.screenshot(page)

            # Verify screenshot data
            assert isinstance(screenshot_data, bytes), "Screenshot data should be bytes"
            assert len(screenshot_data) > 0, "Screenshot data should not be empty"

            # Save screenshot to local file
            filename = "./tmp/screenshot_valid_page_async.png"
            with open(filename, "wb") as f:
                f.write(screenshot_data)
            print(f"✅ Screenshot saved to {filename}")
            print(
                f"✅ Screenshot captured successfully. Size: {len(screenshot_data)} bytes"
            )

        finally:
            await page.close()
            await playwright_browser.close()


@pytest.mark.asyncio
async def test_screenshot_with_full_page(browser_session):
    """Test taking screenshot with full_page=True."""
    print("\n=== Testing screenshot with full_page=True ===")
    browser = browser_session.browser
    await browser.initialize(BrowserOption())

    endpoint_url = await browser.get_endpoint_url()

    async with async_playwright() as p:
        playwright_browser = await p.chromium.connect_over_cdp(endpoint_url)
        contexts = playwright_browser.contexts
        context = contexts[0] if contexts else await playwright_browser.new_context()
        pages = context.pages
        page = pages[0] if pages else await context.new_page()
        await page.goto("https://www.baidu.com", timeout=30000)

        try:
            # Take screenshot with full_page=True
            screenshot_data = await browser.screenshot(page, full_page=True)

            # Verify screenshot data
            assert isinstance(screenshot_data, bytes), "Screenshot data should be bytes"
            assert len(screenshot_data) > 0, "Screenshot data should not be empty"

            # Save screenshot to local file
            filename = "./tmp/screenshot_full_page_async.png"
            with open(filename, "wb") as f:
                f.write(screenshot_data)
            print(f"✅ Full page screenshot saved to {filename}")
            print(
                f"✅ Full page screenshot captured successfully. Size: {len(screenshot_data)} bytes"
            )

        finally:
            await page.close()
            await playwright_browser.close()


@pytest.mark.asyncio
async def test_screenshot_with_custom_options(browser_session):
    """Test taking screenshot with custom options."""
    print("\n=== Testing screenshot with custom options ===")
    browser = browser_session.browser
    await browser.initialize(BrowserOption())

    endpoint_url = await browser.get_endpoint_url()

    async with async_playwright() as p:
        playwright_browser = await p.chromium.connect_over_cdp(endpoint_url)
        contexts = playwright_browser.contexts
        context = contexts[0] if contexts else await playwright_browser.new_context()
        pages = context.pages
        page = pages[0] if pages else await context.new_page()
        await page.goto("https://www.baidu.com", timeout=30000)

        try:
            # Take screenshot with custom options
            screenshot_data = await browser.screenshot(
                page,
                full_page=False,  # Capture only viewport (explicitly set)
                type="jpeg",  # Use JPEG format
                quality=80,  # Set quality to 80%
            )

            # Verify screenshot data
            assert isinstance(screenshot_data, bytes), "Screenshot data should be bytes"
            assert len(screenshot_data) > 0, "Screenshot data should not be empty"

            # Save screenshot to local file
            filename = "./tmp/screenshot_custom_options_async.jpg"
            with open(filename, "wb") as f:
                f.write(screenshot_data)
            print(f"✅ Custom options screenshot saved to {filename}")
            print(
                f"✅ Screenshot with custom options captured successfully. Size: {len(screenshot_data)} bytes"
            )

        finally:
            await page.close()
            await playwright_browser.close()


@pytest.mark.asyncio
async def test_screenshot_function_parameter_priority(browser_session):
    """Test that function parameter full_page takes priority over options."""
    print("\n=== Testing function parameter priority ===")
    browser = browser_session.browser
    await browser.initialize(BrowserOption())

    endpoint_url = await browser.get_endpoint_url()

    async with async_playwright() as p:
        playwright_browser = await p.chromium.connect_over_cdp(endpoint_url)
        contexts = playwright_browser.contexts
        context = contexts[0] if contexts else await playwright_browser.new_context()
        pages = context.pages
        page = pages[0] if pages else await context.new_page()
        await page.goto("https://www.baidu.com", timeout=30000)

        try:
            # Take screenshot with function parameter full_page=False
            # The function parameter should take priority over options
            screenshot_data = await browser.screenshot(
                page,
                False,  # full_page parameter (should take priority)
                type="png",  # Add another option to test options handling
                timeout=30000,  # Add timeout option
            )

            # Verify screenshot data
            assert isinstance(screenshot_data, bytes), "Screenshot data should be bytes"
            assert len(screenshot_data) > 0, "Screenshot data should not be empty"

            # Save screenshot to local file
            filename = "./tmp/screenshot_function_priority_async.png"
            with open(filename, "wb") as f:
                f.write(screenshot_data)
            print(f"✅ Function priority screenshot saved to {filename}")
            print(
                f"✅ Screenshot with function parameter priority captured successfully. Size: {len(screenshot_data)} bytes"
            )

        finally:
            await page.close()
            await playwright_browser.close()


@pytest.mark.asyncio
async def test_screenshot_without_browser_initialization(browser_session):
    """Test taking screenshot without browser initialization."""
    print("\n=== Testing screenshot without browser initialization ===")

    # Use the browser from session (which is NOT initialized by default in fixture)
    # Wait, the fixture creates session. The session creates browser instance but does NOT initialize it unless called.
    # In previous tests we called initialize(). Here we won't.
    # But wait, previous tests called initialize(). The fixture yields session.
    # Session object is fresh each time if scope is function (default).

    browser = browser_session.browser
    # Ensure it's not initialized
    assert not browser.is_initialized()

    # Create a simple mock page object for testing
    class MockPage:
        pass

    mock_page = MockPage()

    try:
        # Attempt to take screenshot with uninitialized browser
        await browser.screenshot(mock_page)
        pytest.fail("Should have raised BrowserError")
    except BrowserError as e:
        # Verify the error message
        assert "Browser must be initialized" in str(e)
        print("✅ Uninitialized browser screenshot correctly raised BrowserError")
    except Exception as e:
        print(f"⚠️ Test encountered an issue: {e}")
        raise


@pytest.mark.asyncio
async def test_screenshot_with_multiple_pages(browser_session):
    """Test taking screenshots with multiple pages."""
    print("\n=== Testing screenshot with multiple pages ===")
    browser = browser_session.browser
    await browser.initialize(BrowserOption())

    endpoint_url = await browser.get_endpoint_url()

    urls = ["https://www.baidu.com", "https://www.taobao.com"]

    async with async_playwright() as p:
        playwright_browser = await p.chromium.connect_over_cdp(endpoint_url)

        screenshot_sizes = []

        for i, url in enumerate(urls):
            try:
                contexts = playwright_browser.contexts
                context = contexts[0] if contexts else await playwright_browser.new_context()
                pages = context.pages
                page = pages[0] if pages else await context.new_page()
                await page.goto(url, timeout=30000)

                try:
                    # Take screenshot with default settings
                    screenshot_data = await browser.screenshot(page, timeout=10000)

                    # Verify screenshot data
                    assert isinstance(
                        screenshot_data, bytes
                    ), f"Screenshot {i+1} data should be bytes"
                    assert (
                        len(screenshot_data) > 0
                    ), f"Screenshot {i+1} data should not be empty"

                    # Save screenshot to local file
                    filename = f"./tmp/screenshot_page_{i+1}_async.png"
                    with open(filename, "wb") as f:
                        f.write(screenshot_data)
                    print(f"✅ Screenshot {i+1} saved to {filename}")

                    screenshot_sizes.append(len(screenshot_data))
                    print(
                        f"✅ Screenshot {i+1} captured successfully. Size: {len(screenshot_data)} bytes"
                    )
                finally:
                    await page.close()
            except Exception as e:
                print(f"⚠️ Warning: Failed to capture screenshot for {url}: {e}")
                # Continue with other URLs
                continue

        # Verify we got at least one screenshot
        assert (
            len(screenshot_sizes) > 0
        ), "Should have at least one successful screenshot"
        await playwright_browser.close()


@pytest.mark.asyncio
async def test_screenshot_performance(browser_session):
    """Test screenshot performance."""
    print("\n=== Testing screenshot performance ===")
    browser = browser_session.browser
    await browser.initialize(BrowserOption())

    endpoint_url = await browser.get_endpoint_url()

    async with async_playwright() as p:
        playwright_browser = await p.chromium.connect_over_cdp(endpoint_url)
        contexts = playwright_browser.contexts
        context = contexts[0] if contexts else await playwright_browser.new_context()
        pages = context.pages
        page = pages[0] if pages else await context.new_page()
        await page.goto("https://www.baidu.com", timeout=30000)

        try:
            # Measure screenshot time
            start_time = time.time()

            # Use a shorter timeout for testing
            screenshot_data = await browser.screenshot(page, timeout=10000)

            end_time = time.time()

            # Calculate duration
            duration = end_time - start_time

            # Verify screenshot data
            assert isinstance(screenshot_data, bytes), "Screenshot data should be bytes"
            assert len(screenshot_data) > 0, "Screenshot data should not be empty"

            # Save screenshot to local file
            filename = "./tmp/screenshot_performance_test_async.png"
            with open(filename, "wb") as f:
                f.write(screenshot_data)
            print(f"✅ Performance test screenshot saved to {filename}")
            print(
                f"✅ Screenshot captured in {duration:.2f} seconds. Size: {len(screenshot_data)} bytes"
            )

            # Performance check (should complete within reasonable time)
            assert duration < 30.0, "Screenshot should complete within 30 seconds"

        except Exception as e:
            print(f"⚠️ Performance test encountered an issue: {e}")
            # Don't fail the test entirely, but note the issue
            raise
        finally:
            await page.close()
            await playwright_browser.close()
