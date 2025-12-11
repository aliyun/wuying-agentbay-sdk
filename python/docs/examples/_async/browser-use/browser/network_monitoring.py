"""
Browser Network Monitoring Example

This example demonstrates:
1. Monitoring network requests
2. Analyzing request/response patterns
3. Detecting failed requests
4. Performance analysis
"""

import asyncio
import os
import sys

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))

from agentbay import AsyncAgentBay, CreateSessionParams
from agentbay import BrowserOption, ActOptions, ExtractOptions

from pydantic import BaseModel

class NetworkActivity(BaseModel):
    content: str
async def main():
    """Demonstrate browser network monitoring."""
    print("=== Browser Network Monitoring Example ===\n")

    # Initialize AgentBay client
    client = AsyncAgentBay()
    session = None

    try:
        # Create a session with browser enabled
        print("Creating session with browser...")
        session_result = await client.create(
            CreateSessionParams(image_id="browser_latest")
        )
        session = session_result.session
        print(f"Session created: {session.session_id}")

        # Initialize browser
        print("Initializing browser...")
        if not await session.browser.initialize(BrowserOption()):
            raise Exception("Failed to initialize browser")
        print("Browser initialized")

        # Navigate to a page and monitor network
        print("\n1. Navigating to example.com...")
        await session.browser.agent.navigate("https://example.com")
        print("Page loaded")

        # Analyze network activity
        print("\n2. Analyzing network activity...")
        network_result = await session.browser.agent.extract(
            ExtractOptions(instruction="What resources were loaded on this page? (images, scripts, stylesheets)", schema=NetworkActivity)
        )
        print(f"Network activity:\n{network_result.extracted_content.content}")

        # Navigate to a more complex page
        print("\n3. Navigating to news.ycombinator.com...")
        await session.browser.agent.navigate("https://news.ycombinator.com")

        # Check for API calls
        print("\n4. Checking for API calls...")
        api_result = await session.browser.agent.extract(
            ExtractOptions(instruction="Are there any API or AJAX requests being made?", schema=NetworkActivity)
        )
        print(f"API calls: {api_result.extracted_content.content}")

        # Test page with known resources
        print("\n5. Testing resource loading...")
        await session.browser.agent.navigate("https://httpbin.org/image/png")
        
        resource_result = await session.browser.agent.extract(
            ExtractOptions(instruction="What type of resource is displayed on this page?", schema=NetworkActivity)
        )
        print(f"Resource type: {resource_result.extracted_content.content}")

        # Navigate to JSON endpoint
        print("\n6. Testing JSON API endpoint...")
        await session.browser.agent.navigate("https://httpbin.org/json")
        
        json_result = await session.browser.agent.extract(
            ExtractOptions(instruction="What is the content type and structure of the response?", schema=NetworkActivity)
        )
        print(f"JSON response:\n{json_result.extracted_content.content}")

        # Test redirect
        print("\n7. Testing redirect behavior...")
        await session.browser.agent.navigate("https://httpbin.org/redirect/1")
        
        redirect_result = await session.browser.agent.extract(
            ExtractOptions(instruction="What is the final URL after redirect?", schema=NetworkActivity)
        )
        print(f"Redirect result: {redirect_result.extracted_content.content}")

        # Test status codes
        print("\n8. Testing different status codes...")
        await session.browser.agent.navigate("https://httpbin.org/status/200")
        
        status_result = await session.browser.agent.extract(
            ExtractOptions(instruction="What is displayed on this page?", schema=NetworkActivity)
        )
        print(f"Status 200 result: {status_result.extracted_content.content}")

        # Performance timing
        print("\n9. Analyzing page load performance...")
        await session.browser.agent.navigate("https://example.com")
        
        perf_result = await session.browser.agent.extract(
            ExtractOptions(instruction="How long did it take for the page to load? (if timing info is visible)", schema=NetworkActivity)
        )
        print(f"Performance: {perf_result.extracted_content.content}")

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