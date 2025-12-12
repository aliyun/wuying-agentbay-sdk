# AgentBay AIBrowser Guide

Welcome to the AgentBay AIBrowser Guides! This provides complete functionality introduction and best practices for experienced developers.

> **💡 Async API Support**: This guide uses synchronous API examples. For async patterns, refer to the `_async` directory in the examples folder.

## 🎯 Quick Navigation

- [Example](code-example.md) - Index for examples demonstrating core & advance features
- [Core Features](core-features.md) - Essential browser features and typical workflows
- [Advance Features](advance-features.md) - Advanced configuration and capabilities
- [Integrations](integrations.md) - Seamlessly weave with community tools and frameworks, extending your automation reach

## 🚀 What is AgentBay AIBrowser?

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

Below is a minimal, runnable example showing how to initialize the browser via the AgentBay Python SDK and drive it using Playwright over CDP. It follows the same flow as the reference example in `python/docs/examples/_sync/browser-use/browser/visit_aliyun.py`.

Prerequisites:
- Set your API key: `export AGENTBAY_API_KEY=your_api_key`
- Install dependencies: `pip install wuying-agentbay-sdk playwright`
- Install Playwright browsers: `python -m playwright install chromium`

```python
import os
from agentbay import AgentBay
from agentbay import CreateSessionParams
from agentbay import BrowserOption
from playwright.sync_api import sync_playwright

def main():
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
    ok = session.browser.initialize(BrowserOption())
    if not ok:
        raise RuntimeError("Browser initialization failed")

    endpoint_url = session.browser.get_endpoint_url()

    # Connect Playwright over CDP and automate
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(endpoint_url)
        context = browser.contexts[0]
        page = context.new_page()
        page.goto("https://www.aliyun.com")
        print("Title:", page.title())
        browser.close()

    session.delete()

if __name__ == "__main__":
    main()
```

### Quick Start (Golang)

Below is a minimal, runnable example showing how to initialize the browser via the AgentBay Golang SDK and drive it using Playwright over CDP.

Prerequisites:
- Set your API key: `export AGENTBAY_API_KEY=your_api_key`
- Install Golang SDK: `go get github.com/aliyun/wuying-agentbay-sdk/golang`
- Install Playwright for Go: `go get github.com/playwright-community/playwright-go`
- Install Playwright browsers: `go run github.com/playwright-community/playwright-go/cmd/playwright@latest install chromium`

```go
package main

import (
	"fmt"
	"log"
	"os"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/browser"
	"github.com/playwright-community/playwright-go"
)

func main() {
	apiKey := os.Getenv("AGENTBAY_API_KEY")
	if apiKey == "" {
		log.Fatal("AGENTBAY_API_KEY environment variable not set")
	}

	// Authenticate with API key
	agentBay := agentbay.NewAgentBay(apiKey)

	// Create a session (use an image with browser preinstalled)
	params := &agentbay.CreateSessionParams{
		ImageId: "browser_latest",
	}
	sessionResult, err := agentBay.Create(params)
	if err != nil {
		log.Fatalf("Failed to create session: %v", err)
	}
	if !sessionResult.Success {
		log.Fatalf("Failed to create session: %s", sessionResult.ErrorMessage)
	}

	session := sessionResult.Session
	defer session.Delete()

	// Initialize browser (supports stealth, proxy, fingerprint, etc. via BrowserOption)
	ok, err := session.Browser.Initialize(browser.NewBrowserOption())
	if err != nil || !ok {
		log.Fatalf("Browser initialization failed: %v", err)
	}

	endpointURL, err := session.Browser.GetEndpointURL()
	if err != nil {
		log.Fatalf("Failed to get endpoint URL: %v", err)
	}

	// Connect Playwright over CDP and automate
	pw, err := playwright.Run()
	if err != nil {
		log.Fatalf("Failed to start Playwright: %v", err)
	}
	defer pw.Stop()

	browser, err := pw.Chromium.ConnectOverCDP(endpointURL)
	if err != nil {
		log.Fatalf("Failed to connect over CDP: %v", err)
	}
	defer browser.Close()

	contexts := browser.Contexts()
	if len(contexts) == 0 {
		log.Fatal("No browser contexts available")
	}
	context := contexts[0]

	page, err := context.NewPage()
	if err != nil {
		log.Fatalf("Failed to create new page: %v", err)
	}

	_, err = page.Goto("https://www.aliyun.com")
	if err != nil {
		log.Fatalf("Failed to navigate: %v", err)
	}

	title, err := page.Title()
	if err != nil {
		log.Fatalf("Failed to get title: %v", err)
	}
	fmt.Println("Title:", title)
}
```

First, the script authenticates by building an `AgentBay` client with your API key, establishing a trusted channel to the platform. 

Then it provisions a fresh execution environment by creating a session with a browser-enabled image, ensuring the necessary runtime is available. 

After that, the session's browser is initialized with `BrowserOption()`, bringing up a remote browser instance ready for automation. 

Next, it retrieves the CDP endpoint URL via `get_endpoint_url()` and connects to it using Playwright's `connect_over_cdp`, bridging your local code to the remote browser. 

Now, with a live connection established, the code opens a new page, navigates to a website, and can freely inspect or manipulate the DOM just like a local browser. 

Finally, when all work is complete, the session is explicitly deleted to release the allocated resources.

Key Browser APIs:
- `Browser.initialize(option: BrowserOption) -> bool`: Start the browser instance for a session (synchronous)
- `Browser.initialize_async(option: BrowserOption) -> bool`: Start the browser instance for a session (asynchronous)
- `Browser.get_endpoint_url() -> str`: Return CDP WebSocket endpoint; use with Playwright `connect_over_cdp`
- `Browser.is_initialized() -> bool`: Check if the browser is ready

## Basic Configurations

Sometimes the web needs a different mask and a different stage. By shaping the browser's identity and canvas, you can coax sites to reveal the experience meant for a specific device class or audience. Here we'll set a custom user agent and a precise viewport, then watch the page respond.

```python
import os
from agentbay import AgentBay
from agentbay import CreateSessionParams
from agentbay import BrowserOption, BrowserViewport
from playwright.sync_api import sync_playwright

CUSTOM_UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"

def main():
    agent_bay = AgentBay(api_key=os.environ["AGENTBAY_API_KEY"])  # first, authenticate

    params = CreateSessionParams(image_id="browser_latest")       # then, provision a browser-ready session
    result = agent_bay.create(params)
    if not result.success:
        raise RuntimeError(result.error_message)

    session = result.session

    # after that, define how the browser should look and feel
    option = BrowserOption(
        user_agent=CUSTOM_UA,                    # present ourselves with a custom identity
        viewport=BrowserViewport(width=1366, height=768),  # and stand on a stage sized like a common laptop
    )

    ok = session.browser.initialize(option)
    if not ok:
        raise RuntimeError("Browser initialization failed")

    endpoint_url = session.browser.get_endpoint_url()      # now, discover the CDP doorway

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(endpoint_url)  # step through and take control
        context = browser.contexts[0]
        page = context.new_page()

        page.goto("https://www.whatismybrowser.com/detect/what-is-my-user-agent")
        # verify our new voice and our new stage
        ua = page.evaluate("navigator.userAgent")
        w = page.evaluate("window.innerWidth")
        h = page.evaluate("window.innerHeight")
        print("Effective UA:", ua)
        print("Viewport:", w, "x", h)

        browser.close()

    session.delete()  # finally, bow out and free the stage

if __name__ == "__main__":
    main()
```

**Golang:**

```go
package main

import (
	"fmt"
	"log"
	"os"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/browser"
	"github.com/playwright-community/playwright-go"
)

const CUSTOM_UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"

func main() {
	// First, authenticate
	agentBay := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"))

	// Then, provision a browser-ready session
	params := &agentbay.CreateSessionParams{
		ImageId: "browser_latest",
	}
	result, err := agentBay.Create(params)
	if err != nil || !result.Success {
		log.Fatalf("Failed to create session: %v", err)
	}
	session := result.Session
	defer session.Delete()

	// After that, define how the browser should look and feel
	option := browser.NewBrowserOption()
	option.UserAgent = &CUSTOM_UA                     // present ourselves with a custom identity
	option.Viewport = &browser.BrowserViewport{       // and stand on a stage sized like a common laptop
		Width:  1366,
		Height: 768,
	}

	ok, err := session.Browser.Initialize(option)
	if err != nil || !ok {
		log.Fatalf("Browser initialization failed: %v", err)
	}

	// Now, discover the CDP doorway
	endpointURL, err := session.Browser.GetEndpointURL()
	if err != nil {
		log.Fatalf("Failed to get endpoint URL: %v", err)
	}

	// Step through and take control
	pw, err := playwright.Run()
	if err != nil {
		log.Fatalf("Failed to start Playwright: %v", err)
	}
	defer pw.Stop()

	browserInstance, err := pw.Chromium.ConnectOverCDP(endpointURL)
	if err != nil {
		log.Fatalf("Failed to connect over CDP: %v", err)
	}
	defer browserInstance.Close()

	context := browserInstance.Contexts()[0]
	page, err := context.NewPage()
	if err != nil {
		log.Fatalf("Failed to create page: %v", err)
	}

	_, err = page.Goto("https://www.whatismybrowser.com/detect/what-is-my-user-agent")
	if err != nil {
		log.Fatalf("Failed to navigate: %v", err)
	}

	// Verify our new voice and our new stage
	ua, err := page.Evaluate("navigator.userAgent")
	if err != nil {
		log.Fatalf("Failed to get user agent: %v", err)
	}
	w, err := page.Evaluate("window.innerWidth")
	if err != nil {
		log.Fatalf("Failed to get window width: %v", err)
	}
	h, err := page.Evaluate("window.innerHeight")
	if err != nil {
		log.Fatalf("Failed to get window height: %v", err)
	}

	fmt.Printf("Effective UA: %v\n", ua)
	fmt.Printf("Viewport: %v x %v\n", w, h)
}
```

First we authenticate and create a session that knows how to host a browser. Then, instead of accepting the default identity, we dress the browser in a chosen user agent and set a viewport that mirrors a familiar laptop screen. After that, we breathe life into the browser with `initialize_async`, request the CDP endpoint, and cross the bridge with Playwright. Now the page loads under our chosen disguise and dimensions; a quick glance at `navigator.userAgent` and the window size confirms the transformation. And when the scene is over, we close the curtain by deleting the session, returning the resources so another performance can begin.

### Browser Type Selection

> **Note:** The `browser_type` / `browserType` option is only available for **computer use images**. For standard browser images, Chromium is used by default.

By default, the browser initializes with Chromium, but when using computer use images, you can choose to use Chrome instead. This is useful when you need specific Chrome features or want to match a particular browser environment. Simply set the `browser_type` parameter in `BrowserOption`:

**Python:**
```python
from agentbay import BrowserOption
from agentbay import CreateSessionParams

# Create session with computer use image
params = CreateSessionParams(image_id="browser_latest")
result = agent_bay.create(params)
session = result.session

# Use Chrome instead of Chromium
option = BrowserOption(browser_type="chrome")
session.browser.initialize(option)

# Or explicitly use Chromium (default)
option = BrowserOption(browser_type="chromium")
session.browser.initialize(option)
```

**TypeScript:**
```typescript
import { CreateSessionParams } from '@wuying-org/agentbay-sdk';

// Create session with computer use image
const params = new CreateSessionParams({ imageId: 'browser_latest' });
const result = await agentBay.create(params);
const session = result.session;

// Use Chrome instead of Chromium (simple approach)
await session.browser.initializeAsync({ browserType: 'chrome' });

// Or explicitly use Chromium
await session.browser.initializeAsync({ browserType: 'chromium' });

// Or use default (undefined - let browser image decide)
await session.browser.initializeAsync({});
```

**Golang:**
```go
import (
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/browser"
)

// Create session with computer use image
params := &agentbay.CreateSessionParams{
	ImageId: "browser_latest",
}
result, err := agentBay.Create(params)
if err != nil {
	// handle error
}
session := result.Session

// Use Chrome instead of Chromium
option := browser.NewBrowserOption()
chromeType := "chrome"
option.BrowserType = &chromeType

success, err := session.Browser.Initialize(option)
if err != nil || !success {
	// handle error
}

// Or explicitly use Chromium
chromiumType := "chromium"
option2 := browser.NewBrowserOption()
option2.BrowserType = &chromiumType

success, err = session.Browser.Initialize(option2)

// Or leave as default (nil, browser decides)
option3 := browser.NewBrowserOption()
// option3.BrowserType is nil by default

success, err = session.Browser.Initialize(option3)
```

The `browser_type` (Python), `browserType` (TypeScript), or `BrowserType` (Golang) option accepts:
- `"chromium"`: Uses the open-source Chromium browser
- `"chrome"`: Uses Google Chrome browser (only available in computer use images)
- `None`/`undefined`/`nil` (default): Lets the browser image decide which browser to use

If you want to explore more configurable capabilities, see Core Features: [core-features.md](core-features.md).

## Utilizing PageUseAgent

PageUseAgent lets you speak to the browser in natural language and have it carry out intent-driven actions. Instead of meticulously crafting selectors and sequences, you describe the goal; the agent interprets it, maps it to DOM operations, and executes the steps reliably—with optional timeouts, iframe awareness, and variable injection for dynamic prompts.

Below we'll demonstrate how to use PageUseAgent without Playwright. The agent can directly control the browser through natural language commands.

```python
import os
from agentbay import AgentBay
from agentbay import CreateSessionParams
from agentbay import BrowserOption
from agentbay import SyncActOptions as ActOptions

BOOK_QUERY = "The Pragmatic Programmer"

def main():
    agent_bay = AgentBay(api_key=os.environ["AGENTBAY_API_KEY"])  # authenticate

    params = CreateSessionParams(image_id="browser_latest")       # provision session with browser image
    result = agent_bay.create(params)
    if not result.success:
        raise RuntimeError(result.error_message)
    session = result.session

    # initialize the remote browser
    if not session.browser.initialize(BrowserOption()):
        raise RuntimeError("Browser initialization failed")

    # navigate to Google
    nav_msg = session.browser.agent.navigate("https://www.google.com")
    print("Navigation result:", nav_msg)

    # ask the agent to act: type the book name into the search box
    act_result = session.browser.agent.act(ActOptions(
        action=f"Type '{BOOK_QUERY}' into the search box and submit",
        use_vision=True
    ))
    print("act_result:", act_result.success, act_result.message)

    # let the agent open the first result
    open_first = session.browser.agent.act(ActOptions(
        action="Click the first result in the search results",
        use_vision=True
    ))
    print("open_first:", open_first.success, open_first.message)

    session.delete()

if __name__ == "__main__":
    main()
```

First we create and initialize a browser session as before; then, rather than hand-writing selectors, we simply tell the agent what to do—navigate to a URL, type a query and proceed to the first result. After that, the agent translates our intent into concrete interactions on the page. Now the browser flows from search box to results like a guided hand. Finally, we release the session.

About `PageUseAgent.act`:
- Can interpolate dynamic values using `variables` for reusable prompts
- Works directly without Playwright by using the browser's internal context
- Returns a structured `ActResult` with `success`, `message`, useful for logging and recovery flows
- Use `SyncActOptions` for synchronous code, `ActOptions` for asynchronous code

If you want to explore full capability of PageUseAgent, or other more advance features, see Advance Features: [advance-features.md](advance-features.md).

### Limitations

PageUseAgent does not include a long-horizon planner and won’t orchestrate multi-step schedules by itself. It relies on your invoker (or a higher-level agent) to break a project into steps and call `act` or other PageUseAgent method for each one. Its strength is in precise, atomic web operations—clicking, filling, scrolling, etc.—executed quickly and consistently. This narrow focus is deliberate: it prioritizes throughput and accuracy of each step while leaving complex task planning and branching logic to external controllers.






