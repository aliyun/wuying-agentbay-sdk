"""
Example demonstrating AIBrowser capabilites with AgentBay SDK.
This example shows how to use AIBrowser to visit aliyun.com, including:
- Create AIBrowser session
- Use playwright to connect to AIBrowser instance through CDP protocol
- Utilize playwright to visit aliyun.com
"""

import os
import time
import asyncio

from agentbay import AgentBay
from agentbay.session_params import CreateSessionParams
from agentbay.browser.browser import BrowserOption

from playwright.async_api import async_playwright

async def main():
    # Get API key from environment variable
    api_key = os.getenv("AGENTBAY_API_KEY")
    if not api_key:
        print("Error: AGENTBAY_API_KEY environment variable not set")
        return

    # Initialize AgentBay client
    print("Initializing AgentBay client...")
    agent_bay = AgentBay(api_key=api_key)

    # Create a session
    print("Creating a new session...")
    params = CreateSessionParams(
        image_id="browser_latest",  # Specify the image ID
    )
    session_result = agent_bay.create(params)

    if session_result.success:
        session = session_result.session
        print(f"Session created with ID: {session.session_id}")

        if await session.browser.initialize_async(BrowserOption()):
            print("Browser initialized successfully")
            endpoint_url = session.browser.get_endpoint_url()
            print("endpoint_url =", endpoint_url)

            async with async_playwright() as p:
                # Step 1: Connect to the browser
                browser = await p.chromium.connect_over_cdp(endpoint_url)

                # Step 2: Open the website
                page = await browser.new_page()
                await page.goto("https://www.aliyun.com")
                print("page.title() =", await page.title())

                # Step 3: Search for the keyword
                search_input = await page.wait_for_selector("//input[contains(@class, 'search-input')]")
                await search_input.click()
                await search_input.fill("Agentbay帮助文档")
                await page.keyboard.press("Enter")

                # Step 4: Get the search results
                await page.wait_for_selector("//a[contains(@class, 'search-result-title')]")
                search_results = await page.locator("//a[contains(@class, 'search-result-title')]").all()

                # Step 5: Click the search result
                for result in search_results:
                    text = await result.text_content()
                    print("result =", text)
                    if "无影AgentBay" == text:
                        await result.click()
                        break

                # Step 6: Click the helper button
                await page.wait_for_selector("a >> text=帮助文档")
                helper_link = page.locator("a >> text=帮助文档").first
                await helper_link.click()

                await page.wait_for_timeout(10000)

                await browser.close()
        else:
            print("Failed to initialize browser")

if __name__ == "__main__":
    asyncio.run(main())