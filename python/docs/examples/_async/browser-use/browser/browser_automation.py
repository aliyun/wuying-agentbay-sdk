import asyncio
import os
import sys
from pydantic import BaseModel, Field

# Add parent dir to path to import agentbay
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from agentbay import AsyncAgentBay, CreateSessionParams
from agentbay import ActOptions, ExtractOptions, BrowserOption
from agentbay import AgentBayError

class SearchResult(BaseModel):
    title: str = Field(description="The title of the search result")
    url: str = Field(description="The URL of the search result")
    snippet: str = Field(description="A brief snippet of the search result")

async def main():
    api_key = os.environ.get("AGENTBAY_API_KEY") or "your_api_key_here"
    agent_bay = AsyncAgentBay(api_key=api_key)
    session = None

    try:
        print("Creating a new browser session (Async)...")
        params = CreateSessionParams(image_id="browser_latest")
        session_result = await agent_bay.create(params)
        session = session_result.session
        print(f"Session created: {session.session_id}")

        # Initialize Browser
        print("Initializing browser...")
        await session.browser.initialize(BrowserOption())

        # 1. Navigate
        url = "https://www.bing.com"
        print(f"Navigating to {url}...")
        nav_msg = await session.browser.agent.navigate(url)
        print(f"Navigation result: {nav_msg}")

        # 2. Act (Type search query)
        print("Typing search query...")
        search_box_act = ActOptions(
            action="type 'AgentBay SDK' into the search box and press Enter",
            use_vision=True
        )
        act_result = await session.browser.agent.act(search_box_act)
        print(f"Act result: {act_result.message}")

        # Wait for results to load
        await asyncio.sleep(5)

        # 3. Screenshot
        print("Taking screenshot...")
        screenshot_data = await session.browser.agent.screenshot(full_page=False)
        print(f"Screenshot taken (length: {len(screenshot_data)})")

        # 4. Extract
        print("Extracting search results...")
        extract_options = ExtractOptions(
            instruction="Extract the first 3 search results including title, url, and snippet",
            schema=SearchResult,
            use_text_extract=True
        )
        success, data = await session.browser.agent.extract(extract_options)
        if success:
            print(f"Extraction successful: {data}")
        else:
            print("Extraction failed")

    except AgentBayError as e:
        print(f"AgentBay error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        if session:
            print("Deleting session...")
            await session.delete()
            print("Session deleted")

if __name__ == "__main__":
    asyncio.run(main())

