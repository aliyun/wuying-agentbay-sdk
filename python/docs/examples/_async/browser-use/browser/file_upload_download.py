"""
Browser File Upload and Download Example

This example demonstrates:
1. Uploading files through browser
2. Downloading files
3. Managing file operations
4. Verifying file transfers
"""

import asyncio
import os
import sys

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))

from agentbay import AsyncAgentBay, CreateSessionParams
from agentbay import BrowserOption, ActOptions, ExtractOptions
from pydantic import BaseModel, Field


class TextContent(BaseModel):
    """Simple model to extract text content."""
    content: str = Field(description="The extracted text content")


async def main():
    """Demonstrate browser file upload and download."""
    print("=== Browser File Upload and Download Example ===\n")

    # Initialize AgentBay client
    client = AsyncAgentBay()
    session = None

    try:
        # Create a session with browser enabled
        print("Creating session with browser...")
        session_result = await client.create(
            CreateSessionParams(image_id="browser_latest")
        )
        print(f"Session result: {session_result}")
        print(f"Session result success: {session_result.success}")
        if not session_result.success:
            print(f"Session creation failed: {session_result}")
            return
        session = session_result.session
        print(f"Session created: {session.session_id}")

        # Initialize browser
        print("Initializing browser...")
        if not await session.browser.initialize(BrowserOption()):
            raise Exception("Failed to initialize browser")
        print("Browser initialized")

        # Create a test file to upload
        print("\n1. Creating test file...")
        test_content = "This is a test file for upload demonstration."
        await session.file_system.write_file("/tmp/test_upload.txt", test_content)
        print("Test file created: /tmp/test_upload.txt")

        # Navigate to file upload test page
        print("\n2. Navigating to file upload test page...")
        await session.browser.agent.navigate("https://httpbin.org/forms/post")

        # Upload file (note: actual file upload may require specific handling)
        print("\n3. Preparing file for upload...")
        # In a real scenario, you would use the browser's file upload mechanism
        # This is a demonstration of the workflow
        await session.browser.agent.act(ActOptions(action="Locate the file upload input field"))
        print("File upload field located")

        # Download a file
        print("\n4. Navigating to download test page...")
        await session.browser.agent.navigate("https://httpbin.org/image/png")
        print("Navigated to image download page")

        # Take screenshot of the downloaded content
        print("\n5. Taking screenshot of downloaded content...")
        screenshot_path = await session.browser.agent.screenshot()
        print(f"Screenshot saved: {screenshot_path}")

        # Verify file operations
        print("\n6. Verifying file operations...")
        files_result = await session.file_system.list_directory("/tmp")
        print(f"Files in /tmp: {files_result}")

        # Test downloading text content
        print("\n7. Testing text content download...")
        await session.browser.agent.navigate("https://httpbin.org/robots.txt")
        extract_options = ExtractOptions(
            instruction="What is the content of this page?", 
            schema=TextContent
        )
        success, content_result = await session.browser.agent.extract(extract_options)
        if success:
            print(f"Downloaded content:\n{content_result.content}")
            content_to_save = content_result.content
        else:
            print("Failed to extract content")
            content_to_save = "Failed to extract content"

        # Save extracted content to file
        print("\n8. Saving extracted content to file...")
        await session.file_system.write_file(
            "/tmp/downloaded_robots.txt",
            content_to_save
        )
        print("Content saved to: /tmp/downloaded_robots.txt")

        # Verify saved file
        saved_content = await session.file_system.read_file("/tmp/downloaded_robots.txt")
        print(f"Verified saved content length: {len(saved_content.content)} bytes")

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

