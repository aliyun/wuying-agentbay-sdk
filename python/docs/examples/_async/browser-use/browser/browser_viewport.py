import os
import asyncio
from agentbay import AsyncAgentBay
from agentbay import CreateSessionParams
from agentbay import BrowserOption, BrowserViewport, BrowserScreen
from playwright.async_api import async_playwright
import json

async def main():
    """Main function demonstrating stealth mode."""
    # Get API key from environment variable
    api_key = os.getenv("AGENTBAY_API_KEY")
    if not api_key:
        print("Error: AGENTBAY_API_KEY environment variable not set")
        return

    # Initialize AgentBay client
    print("Initializing AgentBay client...")
    agent_bay = AsyncAgentBay(api_key=api_key)

    # Create a session
    print("Creating a new session...")
    params = CreateSessionParams(
        image_id="browser_latest",
    )
    session_result = await agent_bay.create(params)

    if session_result.success:
        session = session_result.session
        print(f"Session created with ID: {session.session_id}")

        # Create browser option with viewport and user-agent.
        browser_option = BrowserOption(
            user_agent="Mozilla/5.0 (Mocked Windows Desktop)",
            viewport=BrowserViewport(width=1920, height=1080),
            # screen=BrowserScreen(width=1920, height=1080),
        )

        if await session.browser.initialize(browser_option):
            endpoint_url = await session.browser.get_endpoint_url()
            print("endpoint_url =", endpoint_url)

            async with async_playwright() as p:
                browser = await p.chromium.connect_over_cdp(endpoint_url)
                context = browser.contexts[0]
                page = await context.new_page()

                # Check custom viewport and screen size.
                print("\n--- Check window Properties ---")
                window_info = await page.evaluate("""
                    () => {                
                        const screenInfo = window.screen ? {
                            outerWidth: window.outerWidth,
                            outerHeight: window.outerHeight,
                            innerWidth: window.innerWidth,
                            innerHeight: window.innerHeight,
                            width: window.screen.width,
                            height: window.screen.height,
                            availWidth: window.screen.availWidth,
                            availHeight: window.screen.availHeight,
                            colorDepth: window.screen.colorDepth,
                            pixelDepth: window.screen.pixelDepth
                        } : null;
                        
                        return {
                            screen: screenInfo
                        };
                    }
                """)
                print(f"Screen Info: {window_info.get('screen')}")

                # Check custom user agent.
                print("\n--- Check User Agent ---")
                try:
                    # Increase the timeout to 60 seconds
                    await page.goto("https://httpbin.org/user-agent", timeout=60000)
                    
                    # Wait for page to load completely
                    await page.wait_for_load_state('networkidle')
                    
                    # Get the text content and try to parse it as JSON
                    body_text = await page.evaluate("() => document.body.textContent")
                    print(f"Raw body content: {body_text}")
                    
                    # Try to extract JSON from the text
                    response = json.loads(body_text.strip())
                    user_agent = response.get("user-agent", "")
                    print(f"User Agent: {user_agent}")
                except json.JSONDecodeError as e:
                    print(f"JSON parsing error: {e}")
                    print("Falling back to get user agent from navigator")
                    user_agent = await page.evaluate("() => navigator.userAgent")
                    print(f"User Agent: {user_agent}")
                except Exception as e:
                    print(f"An error occurred: {e}")

                await page.wait_for_timeout(3000)
                await browser.close()

        # Clean up session
        await agent_bay.delete(session)

if __name__ == "__main__":
    asyncio.run(main())