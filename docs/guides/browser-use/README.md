# Agentbay AIBrowser Guide

Welcome to the AgentBay AIBrowser Guides! This provides complete functionality introduction and best practices for experienced developers.

## 🎯 Quick Navigation

### Core Features
- [Example](code-example.md) - Index for examples demonstrating core & advance features
- [Core Features](core-features.md) - Essential browser features and typical workflows
- [Advance Features](advance-features.md) - Advanced configuration and capabilities
- [API](api.md) - Detailed Python API for Browser, Options, and Agents
- [Change Log](changelog.md) - Version history, new features, fixes, and breaking changes

## 🚀 What is Agentbay AIBrowser?

Agentbay AIBrowser is a managed platform for running headless/non-headless browsers at scale. It provides infrastructure to create and manage sessions, initialize browser instances, and allocate the underlying hardware resources on demand. It is designed for webpage automation scenarios such as filling out forms, simulating user actions, and orchestrating complex multi-step tasks across modern, dynamic websites.

The Agentbay AIBrowser API offers simple primitives to control browsers, practical utilities to create/manage sessions, and advanced AI capabilities to execute tasks described in natural language.

### Key Features

- Automation framework compatibility: Highly compatible with Playwright and Puppeteer via CDP
- Secure and scalable infrastructure: Managed sessions, isolation, and elastic resource allocation
- Observability: Session Replay, Session Inspector, and Live Mode for real-time debugging
- Advanced capabilities: Context management, IP proxy, and stealth/fingerprinting options
- AI-powered PageUseAgent: Execute natural-language tasks for complex web workflows
- Rich APIs: Clean primitives for sessions, browser lifecycle, and agent operations

### Quick Start (Python)

Below is a minimal, runnable example showing how to initialize the browser via the AgentBay Python SDK and drive it using Playwright over CDP. It follows the same flow as the reference example in `python/docs/examples/browser/visit_aliyun.py`.

Prerequisites:
- Set your API key: `export AGENTBAY_API_KEY=your_api_key`
- Install dependencies: `pip install wuying-agentbay-sdk playwright`
- Install Playwright browsers: `python -m playwright install chromium`

```python
import os
import asyncio
from agentbay import AgentBay
from agentbay.session_params import CreateSessionParams
from agentbay.browser.browser import BrowserOption
from playwright.async_api import async_playwright

async def main():
    api_key = os.getenv("AGENTBAY_API_KEY")
    if not api_key:
        raise RuntimeError("AGENTBAY_API_KEY environment variable not set")

    agent_bay = AgentBay(api_key=api_key)

    # Create a session (use an image with browser preinstalled)
    params = CreateSessionParams(image_id="browser_latest")
    session_result = agent_bay.create(params)
    if not session_result.success:
        raise RuntimeError(f"Failed to create session: {session_result.error_message}")

    session = session_result.session

    # Initialize browser (supports stealth, proxy, fingerprint, etc. via BrowserOption)
    ok = await session.browser.initialize_async(BrowserOption())
    if not ok:
        raise RuntimeError("Browser initialization failed")

    endpoint_url = session.browser.get_endpoint_url()

    # Connect Playwright over CDP and automate
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(endpoint_url)
        page = await browser.new_page()
        await page.goto("https://www.aliyun.com")
        print("Title:", await page.title())
        await browser.close()

    session.delete()

if __name__ == "__main__":
    asyncio.run(main())
```

First, the script authenticates by building an `AgentBay` client with your API key, establishing a trusted channel to the platform. 

Then it provisions a fresh execution environment by creating a session with a browser-enabled image, ensuring the necessary runtime is available. 

After that, the session’s browser is initialized with `BrowserOption()`, bringing up a remote browser instance ready for automation. 

Next, it retrieves the CDP endpoint URL via `get_endpoint_url()` and connects to it using Playwright’s `connect_over_cdp`, bridging your local code to the remote browser. 

Now, with a live connection established, the code opens a new page, navigates to a website, and can freely inspect or manipulate the DOM just like a local browser. 

Finally, when all work is complete, the session is explicitly deleted to release the allocated resources.

Key Browser APIs:
- `Browser.initialize(option: BrowserOption) -> bool` / `initialize_async(...)`: Start the browser instance for a session
- `Browser.get_endpoint_url() -> str`: Return CDP WebSocket endpoint; use with Playwright `connect_over_cdp`
- `Browser.is_initialized() -> bool`: Check if the browser is ready


