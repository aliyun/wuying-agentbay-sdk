# AI-Powered Web Interactions Tutorial

This tutorial demonstrates how to use the AgentBay SDK's Agent module for AI-powered web interactions, combining browser automation with natural language task execution.

## Overview

In this tutorial, we'll build a web automation solution that uses the Agent module to perform complex web tasks described in natural language. We'll create a system that can navigate websites, extract information, and perform multi-step operations without explicit programming for each task.

## Prerequisites

- AgentBay SDK installed
- Valid API key
- Playwright library installed (for Python examples)
- Basic understanding of browser automation concepts

## Tutorial Structure

1. Setting up a browser session with Agent capabilities
2. Executing simple web tasks using the Agent module
3. Combining browser automation with Agent tasks
4. Handling complex multi-step web operations
5. Error handling and task monitoring

## 1. Setting up a Browser Session

First, let's create a browser session that has both browser automation and Agent capabilities:

```python
import os
import asyncio
from agentbay import AgentBay
from agentbay.session_params import CreateSessionParams

async def setup_browser_session():
    """Set up a browser session with Agent capabilities."""
    # Get API key from environment variable
    api_key = os.getenv("AGENTBAY_API_KEY")
    if not api_key:
        raise ValueError("AGENTBAY_API_KEY environment variable not set")
    
    # Initialize AgentBay client
    agent_bay = AgentBay(api_key=api_key)
    
    # Create a session with browser image
    params = CreateSessionParams(image_id="browser_latest")
    session_result = agent_bay.create(params)
    
    if not session_result.success:
        raise Exception(f"Failed to create session: {session_result.error_message}")
    
    session = session_result.session
    print(f"Session created with ID: {session.session_id}")
    
    # Initialize browser
    if not await session.browser.initialize_async():
        raise Exception("Failed to initialize browser")
    
    print("Browser initialized successfully")
    return agent_bay, session

# Run the setup
# agent_bay, session = asyncio.run(setup_browser_session())
```

## 2. Executing Simple Web Tasks

Let's start with simple web tasks using the Agent module:

```python
async def simple_web_task_example(session):
    """Execute a simple web task using the Agent module."""
    # Task: Find the current weather in New York City
    task_description = "Go to weather.com and find the current weather in New York City. Return only the temperature and weather condition."
    
    print("Executing simple web task...")
    execution_result = session.agent.execute_task(task_description, max_try_times=10)
    
    if execution_result.success:
        print(f"Task completed successfully!")
        print(f"Task status: {execution_result.task_status}")
        print(f"Task output: {execution_result.output}")
    else:
        print(f"Task failed: {execution_result.error_message}")

# Run the example
# asyncio.run(simple_web_task_example(session))
```

## 3. Combining Browser Automation with Agent Tasks

Now let's combine traditional browser automation with Agent tasks:

```python
from playwright.async_api import async_playwright

async def combined_automation_example(agent_bay, session):
    """Combine browser automation with Agent tasks."""
    # Get browser endpoint for Playwright connection
    endpoint_url = session.browser.get_endpoint_url()
    print(f"Browser endpoint URL: {endpoint_url}")
    
    async with async_playwright() as p:
        # Connect to the browser
        browser = await p.chromium.connect_over_cdp(endpoint_url)
        page = await browser.new_page()
        
        try:
            # Navigate to a website using Playwright
            await page.goto("https://www.wikipedia.org")
            print("Navigated to Wikipedia")
            
            # Use Agent to perform a search
            search_task = "Search for 'Machine Learning' on this Wikipedia page"
            search_result = session.agent.execute_task(search_task, max_try_times=5)
            
            if search_result.success:
                print(f"Search task completed: {search_result.output}")
                
                # Navigate to the search results page
                await page.goto("https://en.wikipedia.org/wiki/Machine_learning")
                
                # Use Agent to extract key information
                extract_task = "Extract the definition of Machine Learning from this page"
                extract_result = session.agent.execute_task(extract_task, max_try_times=5)
                
                if extract_result.success:
                    print(f"Definition: {extract_result.output}")
                else:
                    print(f"Extraction failed: {extract_result.error_message}")
            else:
                print(f"Search task failed: {search_result.error_message}")
                
        finally:
            await browser.close()

# Run the example
# asyncio.run(combined_automation_example(agent_bay, session))
```

## 4. Complex Multi-Step Web Operations

Let's handle more complex multi-step operations:

```python
async def complex_web_operation(agent_bay, session):
    """Handle complex multi-step web operations."""
    # Task: Research and summarize information about a technology
    research_task = """
    Research the Python programming language by:
    1. Visiting the official Python website (python.org)
    2. Finding the 'About' page
    3. Extracting key information about Python's features and philosophy
    4. Visiting the Python documentation page
    5. Finding information about the latest Python version
    6. Creating a summary that includes Python's philosophy, key features, and latest version
    """
    
    print("Starting complex research task...")
    execution_result = session.agent.execute_task(research_task, max_try_times=20)
    
    if execution_result.success:
        print("Research completed successfully!")
        print(f"Research summary:\n{execution_result.output}")
    else:
        print(f"Research task failed: {execution_result.error_message}")

# Run the example
# asyncio.run(complex_web_operation(agent_bay, session))
```

## 5. Error Handling and Task Monitoring

Let's implement proper error handling and task monitoring:

```python
import time

async def monitored_task_execution(session, task_description, max_try_times=10):
    """Execute a task with monitoring and error handling."""
    try:
        # Start task execution
        execution_result = session.agent.execute_task(task_description, max_try_times)
        
        # Monitor task progress
        if not execution_result.success and execution_result.task_id:
            task_id = execution_result.task_id
            print(f"Task started with ID: {task_id}")
            
            # Monitor task status
            for i in range(max_try_times):
                status_result = session.agent.get_task_status(task_id)
                if status_result.success:
                    print(f"Task status check {i+1}: {status_result.output}")
                else:
                    print(f"Failed to get task status: {status_result.error_message}")
                
                # Wait before next check
                time.sleep(3)
                
                # Check if task is completed
                if "finished" in status_result.output.lower() or "failed" in status_result.output.lower():
                    break
        elif execution_result.success:
            print("Task completed successfully!")
            print(f"Result: {execution_result.output}")
        else:
            print(f"Task failed to start: {execution_result.error_message}")
            
    except Exception as e:
        print(f"Error during task execution: {e}")

# Example usage
# task_desc = "Find the current stock price of Apple Inc. and compare it with Microsoft's stock price"
# asyncio.run(monitored_task_execution(session, task_desc))
```

## 6. Complete Example: Automated Research Assistant

Let's put everything together in a complete example:

```python
import os
import asyncio
from agentbay import AgentBay
from agentbay.session_params import CreateSessionParams
from playwright.async_api import async_playwright

class AIResearchAssistant:
    """AI-powered research assistant using AgentBay SDK."""
    
    def __init__(self, api_key):
        self.agent_bay = AgentBay(api_key=api_key)
        self.session = None
        self.page = None
        
    async def setup(self):
        """Set up the research environment."""
        # Create a browser session
        params = CreateSessionParams(image_id="browser_latest")
        session_result = self.agent_bay.create(params)
        
        if not session_result.success:
            raise Exception(f"Failed to create session: {session_result.error_message}")
            
        self.session = session_result.session
        
        # Initialize browser
        if not await self.session.browser.initialize_async():
            raise Exception("Failed to initialize browser")
            
        # Connect with Playwright
        endpoint_url = self.session.browser.get_endpoint_url()
        playwright = await async_playwright().start()
        browser = await playwright.chromium.connect_over_cdp(endpoint_url)
        self.page = await browser.new_page()
        
        print("AI Research Assistant initialized successfully!")
        return browser, playwright
    
    async def research_topic(self, topic):
        """Research a topic using both browser automation and Agent tasks."""
        try:
            print(f"Starting research on: {topic}")
            
            # Navigate to a search engine
            await self.page.goto("https://www.google.com")
            
            # Use Agent to perform the search
            search_task = f"Search for '{topic}' on Google and find the most authoritative source"
            search_result = self.session.agent.execute_task(search_task, max_try_times=5)
            
            if search_result.success:
                print(f"Search completed: {search_result.output}")
                
                # Extract detailed information
                extract_task = f"From the search results, go to the best source and extract comprehensive information about {topic}"
                extract_result = self.session.agent.execute_task(extract_task, max_try_times=10)
                
                if extract_result.success:
                    return extract_result.output
                else:
                    raise Exception(f"Extraction failed: {extract_result.error_message}")
            else:
                raise Exception(f"Search failed: {search_result.error_message}")
                
        except Exception as e:
            print(f"Research error: {e}")
            return None
    
    async def close(self, browser, playwright):
        """Clean up resources."""
        if browser:
            await browser.close()
        if playwright:
            await playwright.stop()
        if self.session:
            delete_result = self.agent_bay.delete(self.session)
            if delete_result.success:
                print("Session deleted successfully")
            else:
                print(f"Failed to delete session: {delete_result.error_message}")

# Usage example
async def main():
    """Main function to demonstrate the AI Research Assistant."""
    api_key = os.getenv("AGENTBAY_API_KEY")
    if not api_key:
        print("Error: AGENTBAY_API_KEY environment variable not set")
        return
    
    assistant = AIResearchAssistant(api_key)
    browser = None
    playwright = None
    
    try:
        # Set up the assistant
        browser, playwright = await assistant.setup()
        
        # Research a topic
        topic = "quantum computing applications in cryptography"
        result = await assistant.research_topic(topic)
        
        if result:
            print(f"\nResearch Results for '{topic}':")
            print("=" * 50)
            print(result)
        else:
            print("Research failed to produce results")
            
    finally:
        # Clean up
        await assistant.close(browser, playwright)

# Run the complete example
# asyncio.run(main())
```

## Best Practices

1. **Task Descriptions**: Write clear, specific task descriptions for better results
2. **Error Handling**: Always implement proper error handling for both Agent tasks and browser operations
3. **Resource Management**: Clean up browser connections and sessions when done
4. **Monitoring**: Monitor long-running tasks and implement appropriate timeouts
5. **Security**: Never expose API keys in code; use environment variables
6. **Testing**: Test tasks with various inputs to ensure reliability

## Common Use Cases

1. **Research Automation**: Automatically gather information on topics from multiple sources
2. **Price Comparison**: Compare prices across different e-commerce websites
3. **Content Aggregation**: Collect and summarize content from news sites
4. **Social Media Monitoring**: Track mentions and sentiment on social platforms
5. **Competitive Analysis**: Analyze competitor websites and offerings
6. **Data Extraction**: Extract structured data from unstructured web content

## Limitations and Considerations

1. **Task Complexity**: Very complex tasks may require breaking into smaller subtasks
2. **Website Changes**: Websites frequently change, which may affect task execution
3. **Rate Limiting**: Be mindful of website rate limits and terms of service
4. **Execution Time**: Complex tasks may take significant time to complete
5. **Accuracy**: Verify critical information obtained from AI tasks

## Next Steps

1. Experiment with different types of web tasks
2. Implement more sophisticated error handling and retry mechanisms
3. Add logging and monitoring for production use
4. Explore integration with other AgentBay session capabilities
5. Build a web interface for your AI Research Assistant

This tutorial demonstrated how to combine browser automation with AI-powered task execution using the AgentBay SDK's Agent module. By leveraging natural language task descriptions, you can create powerful web automation solutions that adapt to changing requirements without extensive reprogramming.