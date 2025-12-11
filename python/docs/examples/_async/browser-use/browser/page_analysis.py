"""
Browser Page Analysis Example

This example demonstrates:
1. Extracting page metadata
2. Analyzing page structure
3. Finding specific elements
4. Extracting structured data
"""

import asyncio
import os
import sys

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))

from agentbay import AsyncAgentBay, CreateSessionParams
from agentbay import BrowserOption, ExtractOptions
from pydantic import BaseModel, Field


class TextContent(BaseModel):
    """Simple model to extract text content."""
    content: str = Field(description="The extracted text content")


async def main():
    """Demonstrate browser page analysis."""
    print("=== Browser Page Analysis Example ===\n")

    # Initialize AgentBay client
    client = AsyncAgentBay()
    session = None

    try:
        # Create a session with browser enabled
        print("Creating session with browser...")
        session_result = await client.create(
            CreateSessionParams(image_id="browser_latest")
        )
        if not session_result.success or not session_result.session:
            raise Exception(f"Failed to create session: {session_result.error_message}")
        session = session_result.session
        print(f"Session created: {session.session_id}")

        # Initialize browser
        print("Initializing browser...")
        if not await session.browser.initialize(BrowserOption()):
            raise Exception("Failed to initialize browser")
        print("Browser initialized")

        # Navigate to a page
        print("\n1. Navigating to example.com...")
        await session.browser.agent.navigate("https://example.com")

        # Extract page title
        print("\n2. Extracting page title...")
        success, title_result = await session.browser.agent.extract(ExtractOptions(instruction="What is the page title?", schema=TextContent,timeout=600))
        if success:
            print(f"Page title: {title_result.content}")
        else:
            print("Failed to extract page title")

        # Extract page description
        print("\n3. Extracting page description...")
        success, desc_result = await session.browser.agent.extract(ExtractOptions(instruction="What is the main content or description on this page?", schema=TextContent,timeout=600))
        if success:
            print(f"Page description: {desc_result.content}")
        else:
            print("Failed to extract page description")

        # Navigate to a more complex page
        print("\n4. Navigating to news.ycombinator.com...")
        await session.browser.agent.navigate("https://news.ycombinator.com")

        # Extract structured data
        print("\n5. Extracting top 5 story titles...")
        success, stories_result = await session.browser.agent.extract(ExtractOptions(
            instruction="List the titles of the top 5 stories on the page",
            schema=TextContent,
            timeout=600
        ))
        if success:
            print(f"Top stories:\n{stories_result.content}")
        else:
            print("Failed to extract top stories")

        # Analyze page structure
        print("\n6. Analyzing page structure...")
        success, structure_result = await session.browser.agent.extract(ExtractOptions(
            instruction="Describe the main sections and layout of this page",
            schema=TextContent,
            timeout=600
        ))
        if success:
            print(f"Page structure:\n{structure_result.content}")
        else:
            print("Failed to extract page structure")

        # Find specific elements
        print("\n7. Finding navigation elements...")
        success, nav_result = await session.browser.agent.extract(ExtractOptions(
            instruction="What navigation options are available on this page?",
            schema=TextContent,
            timeout=600
        ))
        if success:
            print(f"Navigation elements:\n{nav_result.content}")
        else:
            print("Failed to extract navigation elements")

        # Extract metadata
        print("\n8. Extracting page metadata...")
        success, meta_result = await session.browser.agent.extract(ExtractOptions(
            instruction="What is the page URL and any visible metadata?",
            schema=TextContent,
            timeout=600
        ))
        if success:
            print(f"Metadata:\n{meta_result.content}")
        else:
            print("Failed to extract metadata")

        print("\n=== Example completed successfully ===")

    except Exception as e:
        print(f"\nError occurred: {str(e)}")
        raise

    finally:
        # Clean up
        if session:
            print("\nCleaning up session...")
            await client.delete(session)
            print("Session closed")


if __name__ == "__main__":
    asyncio.run(main())

