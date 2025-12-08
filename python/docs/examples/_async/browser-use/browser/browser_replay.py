#!/usr/bin/env python3
"""
Browser Replay Example

This example demonstrates how to:
1. Create a browser session with browser replay enabled
2. Perform browser operations that will be captured
3. Access the replay video files
4. Clean up the session

The browser replay will capture all browser interactions and save them for internal processing
"""

import os
import asyncio
import time
from agentbay import AsyncAgentBay
from agentbay import CreateSessionParams
from agentbay import BrowserOption
from playwright.async_api import async_playwright


async def main():
    # Initialize AgentBay client
    api_key = os.getenv("AGENTBAY_API_KEY")
    if not api_key:
        print("❌ Please set AGENTBAY_API_KEY environment variable")
        return

    agent_bay = AsyncAgentBay(api_key=api_key)

    try:
        # Create a browser session with browser replay enabled
        print("🎬 Creating browser session with browser replay...")
        session_params = CreateSessionParams(
            image_id="browser_latest",
            enable_browser_replay=True,  # Enable browser replay
            labels={
                "example": "browser_replay",
                "session_type": "browser",
                "replay": "enabled"
            }
        )

        result = await agent_bay.create(session_params)
        if not result.success:
            print(f"❌ Failed to create session: {result.error_message}")
            return

        session = result.session
        print(f"✅ Session created: {session.session_id}")
        print(f"📹 Browser replay enabled: {session.enableBrowserReplay}")

        # Initialize browser
        print("\n🌐 Initializing browser...")
        browser = session.browser
        browser_option = BrowserOption()

        if not browser.initialize(browser_option):
            print("❌ Failed to initialize browser")
            return

        endpoint_url = await browser.get_endpoint_url()
        print(f"🔗 Browser endpoint: {endpoint_url}")

        # Wait for browser to be ready
        await asyncio.sleep(5)

        # Perform browser operations that will be captured
        print("\n🎥 Starting browser operations for replay...")

        async with async_playwright() as p:
            playwright_browser = await p.chromium.connect_over_cdp(endpoint_url)

            # Test multiple websites and operations
            test_scenarios = [
                {
                    "name": "Baidu Search",
                    "url": "https://www.baidu.com",
                    "actions": lambda page: perform_baidu_search(page)
                },
                {
                    "name": "Google Search",
                    "url": "https://www.google.com",
                    "actions": lambda page: perform_google_search(page)
                },
                {
                    "name": "AgentBay Documentation",
                    "url": "https://help.aliyun.com/zh/agentbay/",
                    "actions": lambda page: browse_documentation(page)
                }
            ]

            for i, scenario in enumerate(test_scenarios, 1):
                print(f"\n📋 Scenario {i}: {scenario['name']}")

                default_context = playwright_browser.contexts[0]
                # Create a new page
                page = await default_context.new_page()

                try:
                    # Navigate to the website
                    print(f"🔄 Navigating to {scenario['url']}")
                    await page.goto(scenario['url'], timeout=30000, wait_until="domcontentloaded")
                    await asyncio.sleep(2)

                    # Get page title
                    title = await page.title()
                    print(f"📄 Page title: {title}")

                    # Take a screenshot
                    screenshot_path = f"/tmp/replay_screenshot_{i}.png"
                    await page.screenshot(path=screenshot_path)
                    print(f"📸 Screenshot saved: {screenshot_path}")

                    # Perform specific actions for this scenario
                    await scenario['actions'](page)

                    # Wait to ensure the actions are captured
                    await asyncio.sleep(3)

                except Exception as e:
                    print(f"⚠️  Warning: Failed to complete scenario {scenario['name']}: {e}")

                finally:
                    await page.close()
                    await asyncio.sleep(1)

            # Close the browser
            await playwright_browser.close()

        print(f"\n🎬 Browser replay completed!")
        print("📁 Replay files are automatically generated and stored by the system")
        print("🎥 These files are used for internal processing and analysis")

    except Exception as e:
        print(f"❌ Error during browser replay demo: {e}")

    finally:
        # Clean up: delete the session
        print(f"\n🧹 Cleaning up session {session.session_id}...")
        try:
            delete_result = await agent_bay.delete(session)
            if delete_result.success:
                print("✅ Session deleted successfully")
            else:
                print(f"⚠️  Warning: Failed to delete session: {delete_result.error_message}")
        except Exception as e:
            print(f"⚠️  Warning: Error during cleanup: {e}")


async def perform_baidu_search(page):
    """Perform a search on Baidu"""
    try:
        # Find search input and enter search term
        search_input = await page.query_selector("#kw")
        if search_input:
            search_term = "AgentBay cloud automation"
            await search_input.fill(search_term)
            print(f"🔍 Searching for: {search_term}")
            await asyncio.sleep(1)

            # Click search button
            search_button = await page.query_selector("#su")
            if search_button:
                await search_button.click()
                print("🔄 Search submitted")
                await asyncio.sleep(3)  # Wait for results
    except Exception as e:
        print(f"⚠️  Search failed: {e}")


async def perform_google_search(page):
    """Perform a search on Google"""
    try:
        # Find search input and enter search term
        search_input = await page.query_selector("input[name='q']")
        if search_input:
            search_term = "AgentBay browser recording"
            await search_input.fill(search_term)
            print(f"🔍 Searching for: {search_term}")
            await asyncio.sleep(1)

            # Press Enter to search
            await search_input.press("Enter")
            print("🔄 Search submitted")
            await asyncio.sleep(3)  # Wait for results
    except Exception as e:
        print(f"⚠️  Search failed: {e}")


async def browse_documentation(page):
    """Browse documentation site"""
    try:
        # Wait for page to load
        await asyncio.sleep(2)

        # Try to find and click on a link
        links = await page.query_selector_all("a")
        if links and len(links) > 0:
            # Click on the first few links to demonstrate navigation
            for i, link in enumerate(links[:3]):
                try:
                    link_text = await link.text_content()
                    if link_text and len(link_text.strip()) > 0:
                        print(f"🔗 Clicking link: {link_text[:50]}...")
                        await link.click()
                        await asyncio.sleep(2)
                        break
                except:
                    continue
    except Exception as e:
        print(f"⚠️  Documentation browsing failed: {e}")


if __name__ == "__main__":
    print("🎬 AgentBay Browser Replay Demo")
    print("=" * 50)
    import asyncio
    asyncio.run(main())