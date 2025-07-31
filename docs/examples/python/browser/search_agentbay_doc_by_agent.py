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
from agentbay.browser.browser_agent import ActOptions, ObserveOptions

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
                browser = await p.chromium.connect_over_cdp(endpoint_url)
                page = await browser.new_page()
                await page.goto("https://www.aliyun.com")

                # 1. Input search keyword
                await session.browser.agent.act_async(page, ActOptions(
                    action="在搜索框中输入'AgentBay帮助文档'",
                ))

                # 2. Press Enter
                await page.keyboard.press("Enter")

                # 3. Click the first search result
                await session.browser.agent.act_async(page, ActOptions(
                    action="点击搜索结果中的第一项",
                ))

                # 4. Click '帮助文档'
                await session.browser.agent.act_async(page, ActOptions(
                    action="点击'帮助文档'",
                ))

                # 5. Wait for 10 seconds
                await page.wait_for_timeout(10000)

                await browser.close()
        else:
            print("Failed to initialize browser")

if __name__ == "__main__":
    asyncio.run(main())