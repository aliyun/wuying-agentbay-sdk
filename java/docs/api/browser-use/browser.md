# Browser API Reference

## 🌐 Related Tutorial

- [Browser Use Guide](../../../../../docs/guides/browser-use/README.md) - Complete guide to browser automation
- [Browser Core Features](../../../../../docs/guides/browser-use/core-features.md) - Core browser automation features

## Overview

The Browser module provides browser automation capabilities using Playwright integration. It enables web scraping, automated testing, form filling, and other browser-based automation tasks in a cloud environment.

## Browser

```java
public class Browser extends BaseService
```

Provides browser-related operations for the session.

### initialize

```java
public boolean initialize(BrowserOption option)
```

Initialize the browser instance with the given options.

**Parameters:**
- `option` (BrowserOption): Browser initialization options

**Returns:**
- `boolean`: True if initialization succeeded, false otherwise

**Example:**

```java
CreateSessionParams params = new CreateSessionParams();
params.setImageId("browser_latest");
Session session = agentBay.create(params).getSession();

// Create browser options
BrowserOption option = new BrowserOption();
option.setUseStealth(true);
option.setBehaviorSimulate(true);

// Initialize browser
boolean success = session.getBrowser().initialize(option);
if (success) {
    System.out.println("Browser initialized successfully");
}
```

### getEndpointUrl

```java
public String getEndpointUrl()
```

Get the browser endpoint URL for Playwright connection.

**Returns:**
- `String`: CDP (Chrome DevTools Protocol) endpoint URL

**Throws:**
- `BrowserException`: If browser is not initialized

**Example:**

```java
String endpointUrl = session.getBrowser().getEndpointUrl();
System.out.println("Browser endpoint: " + endpointUrl);
```

### isInitialized

```java
public boolean isInitialized()
```

Check if the browser has been initialized.

**Returns:**
- `boolean`: True if browser is initialized

## BrowserContext

```java
public class BrowserContext
```

Browser context configuration for session. Enables browser data persistence (cookies, localStorage) across multiple sessions using the same context ID.

### Constructors

#### Basic Constructor

```java
public BrowserContext(String contextId, boolean autoUpload)
```

Initialize BrowserContext with minimal configuration.

**Parameters:**
- `contextId` (String): ID of the browser context to bind to the session
- `autoUpload` (boolean): Whether to automatically upload browser data when session ends

**Example:**

```java
// Create a persistent context
ContextResult contextResult = agentBay.getContext().get("my-browser-context", true);
Context context = contextResult.getContext();

// Create BrowserContext with auto-upload
BrowserContext browserContext = new BrowserContext(context.getId(), true);

// Create session with BrowserContext
CreateSessionParams params = new CreateSessionParams();
params.setImageId("browser_latest");
params.setBrowserContext(browserContext);
Session session = agentBay.create(params).getSession();
```

#### Default Constructor

```java
public BrowserContext(String contextId)
```

Initialize BrowserContext with default `autoUpload=true`.

**Parameters:**
- `contextId` (String): ID of the browser context

#### Full Constructor

```java
public BrowserContext(String contextId, boolean autoUpload, 
                     ExtensionOption extensionOption,
                     BrowserFingerprintContext fingerprintContext)
```

Initialize BrowserContext with optional extension and fingerprint support.

**Parameters:**
- `contextId` (String): ID of the browser context
- `autoUpload` (boolean): Whether to automatically upload browser data
- `extensionOption` (ExtensionOption): Extension configuration (can be null)
- `fingerprintContext` (BrowserFingerprintContext): Browser fingerprint configuration (can be null)

**Example:**

```java
// With extensions
ExtensionOption extOption = new ExtensionOption(
    "my_extensions",
    Arrays.asList("ext1.zip", "ext2.zip")
);

BrowserContext browserContext = new BrowserContext(
    context.getId(),
    true,
    extOption,
    null
);
```

### Key Methods

#### getContextId

```java
public String getContextId()
```

Get the browser context ID.

#### isAutoUpload

```java
public boolean isAutoUpload()
```

Check if auto-upload is enabled.

### Cookie Persistence Example

```java
import com.aliyun.agentbay.AgentBay;
import com.aliyun.agentbay.browser.BrowserContext;
import com.aliyun.agentbay.context.Context;
import com.aliyun.agentbay.session.Session;
import com.microsoft.playwright.*;
import com.microsoft.playwright.options.Cookie;

// Step 1: Create persistent context
ContextResult contextResult = agentBay.getContext().get("browser-context", true);
Context context = contextResult.getContext();

// Step 2: Create first session with BrowserContext
BrowserContext browserContext = new BrowserContext(context.getId(), true);
CreateSessionParams params = new CreateSessionParams();
params.setImageId("browser_latest");
params.setBrowserContext(browserContext);
Session session1 = agentBay.create(params).getSession();

// Step 3: Set cookies in first session
session1.getBrowser().initialize(new BrowserOption());
String endpointUrl = session1.getBrowser().getEndpointUrl();

try (Playwright playwright = Playwright.create()) {
    Browser browser = playwright.chromium().connectOverCDP(endpointUrl);
    BrowserContext context = browser.contexts().get(0);
    Page page = context.newPage();
    
    page.navigate("https://example.com");
    
    // Add cookies
    List<Cookie> cookies = new ArrayList<>();
    cookies.add(new Cookie("sessionId", "abc123")
        .setDomain("example.com")
        .setPath("/"));
    context.addCookies(cookies);
    
    browser.close();
}

// Step 4: Delete first session WITH context sync
agentBay.delete(session1, true);  // sync_context=true

// Wait for sync
Thread.sleep(3000);

// Step 5: Create second session with same context
Session session2 = agentBay.create(params).getSession();

// Cookies are automatically restored!
session2.getBrowser().initialize(new BrowserOption());
String endpointUrl2 = session2.getBrowser().getEndpointUrl();

try (Playwright playwright = Playwright.create()) {
    Browser browser = playwright.chromium().connectOverCDP(endpointUrl2);
    BrowserContext context = browser.contexts().get(0);
    
    // Cookies from first session are available
    List<Cookie> cookies = context.cookies();
    System.out.println("Restored cookies: " + cookies.size());
}

agentBay.delete(session2, false);
```

## ExtensionOption

```java
public class ExtensionOption
```

Configuration for browser extensions. Extensions are loaded from a cloud context.

### Constructor

```java
public ExtensionOption(String contextId, List<String> extensionIds)
```

**Parameters:**
- `contextId` (String): Context ID where extension files are stored
- `extensionIds` (List<String>): List of extension file names (e.g., "adblock.zip")

**Example:**

```java
ExtensionOption extOption = new ExtensionOption(
    "extensions-context",
    Arrays.asList("ublock.zip", "metamask.zip")
);

BrowserContext browserContext = new BrowserContext(
    "browser-session",
    true,
    extOption,
    null
);
```

## BrowserFingerprintContext

```java
public class BrowserFingerprintContext
```

Browser fingerprint context configuration for enhanced privacy and anti-detection.

### Constructor

```java
public BrowserFingerprintContext(String fingerprintContextId)
```

**Parameters:**
- `fingerprintContextId` (String): ID of the fingerprint context

**Example:**

```java
BrowserFingerprintContext fingerprintCtx = new BrowserFingerprintContext(
    "my-fingerprint"
);

BrowserContext browserContext = new BrowserContext(
    "browser-session",
    true,
    null,
    fingerprintCtx
);
```

## BrowserOption

```java
public class BrowserOption
```

Configuration options for browser initialization.

### Key Fields

#### useStealth

```java
public void setUseStealth(boolean useStealth)
public boolean getUseStealth()
```

Enable stealth mode to avoid bot detection.

**Default**: false

**Example:**

```java
BrowserOption option = new BrowserOption();
option.setUseStealth(true);
```

#### behaviorSimulate

```java
public void setBehaviorSimulate(boolean behaviorSimulate)
public boolean getBehaviorSimulate()
```

Simulate human-like behavior (mouse movements, typing delays).

**Default**: false

#### solveCaptchas

```java
public void setSolveCaptchas(boolean solveCaptchas)
public boolean getSolveCaptchas()
```

Enable automatic CAPTCHA solving.

**Default**: false

#### viewport

```java
public void setViewport(BrowserViewport viewport)
public BrowserViewport getViewport()
```

Set browser viewport size.

**Example:**

```java
BrowserViewport viewport = new BrowserViewport();
viewport.setWidth(1920);
viewport.setHeight(1080);
option.setViewport(viewport);
```

#### screen

```java
public void setScreen(BrowserScreen screen)
public BrowserScreen getScreen()
```

Set screen resolution.

**Example:**

```java
BrowserScreen screen = new BrowserScreen();
screen.setWidth(1920);
screen.setHeight(1080);
option.setScreen(screen);
```

#### proxies

```java
public void setProxies(List<BrowserProxy> proxies)
public List<BrowserProxy> getProxies()
```

Set proxy configuration for browser requests.

**Example:**

```java
BrowserProxy proxy = new BrowserProxy();
proxy.setType("http");
proxy.setServer("proxy.example.com:8080");
proxy.setUsername("user");
proxy.setPassword("pass");

option.setProxies(Arrays.asList(proxy));
```

#### fingerprint

```java
public void setFingerprint(BrowserFingerprint fingerprint)
public BrowserFingerprint getFingerprint()
```

Set browser fingerprint configuration for enhanced privacy.

#### userAgent

```java
public void setUserAgent(String userAgent)
public String getUserAgent()
```

Set custom user agent string.

## Complete Playwright Integration Example

```java
import com.aliyun.agentbay.AgentBay;
import com.aliyun.agentbay.session.Session;
import com.aliyun.agentbay.session.CreateSessionParams;
import com.aliyun.agentbay.browser.BrowserOption;
import com.microsoft.playwright.*;

public class PlaywrightExample {
    public static void main(String[] args) throws Exception {
        AgentBay agentBay = new AgentBay(System.getenv("AGENTBAY_API_KEY"));
        
        // Create browser session
        CreateSessionParams params = new CreateSessionParams();
        params.setImageId("browser_latest");
        Session session = agentBay.create(params).getSession();
        
        // Initialize browser with options
        BrowserOption option = new BrowserOption();
        option.setUseStealth(true);
        option.setBehaviorSimulate(true);
        
        session.getBrowser().initialize(option);
        
        // Get endpoint for Playwright
        String endpointUrl = session.getBrowser().getEndpointUrl();
        
        // Connect Playwright
        try (Playwright playwright = Playwright.create()) {
            BrowserType chromium = playwright.chromium();
            Browser browser = chromium.connectOverCDP(endpointUrl);
            
            // Get or create context
            BrowserContext context = browser.contexts().isEmpty() 
                ? browser.newContext()
                : browser.contexts().get(0);
            
            Page page = context.newPage();
            
            // Navigate and interact
            page.navigate("https://example.com");
            System.out.println("Page title: " + page.title());
            
            // Take screenshot
            page.screenshot(new Page.ScreenshotOptions()
                .setPath(java.nio.file.Paths.get("screenshot.png")));
            
            // Close
            browser.close();
        }
        
        // Clean up
        session.delete();
    }
}
```

## Browser Agent (AI-Powered Automation)

The Browser module also includes an AI-powered agent for natural language automation:

```java
BrowserAgent agent = session.getBrowser().getAgent();
```

### act

```java
public ActResult act(Page page, Object actionInput) throws BrowserException
```

Perform a browser action using natural language or structured action.

**Parameters:**
- `page` (Page): Playwright Page object
- `actionInput` (Object): Either ActOptions or ObserveResult
  - `ActOptions`: Contains action description and options
  - `ObserveResult`: Result from previous observe() call

**Returns:**
- `ActResult`: Result containing action outcome

**Throws:**
- `BrowserException`: If browser is not initialized or action fails

**Example:**

```java
import com.microsoft.playwright.*;

// Initialize browser
BrowserOption option = new BrowserOption();
option.setUseStealth(true);
session.getBrowser().initialize(option);

// Get Playwright page
String endpointUrl = session.getBrowser().getEndpointUrl();
try (Playwright playwright = Playwright.create()) {
    Browser browser = playwright.chromium().connectOverCDP(endpointUrl);
    Page page = browser.contexts().get(0).newPage();
    
    // Get browser agent
    BrowserAgent agent = session.getBrowser().getAgent();
    
    // Perform actions using natural language
    ActOptions options = new ActOptions();
    options.setAction("Go to google.com");
    ActResult result = agent.act(page, options);
    
    if (result.isSuccess()) {
        System.out.println("Navigation successful");
    }
    
    // Perform another action
    ActOptions searchOptions = new ActOptions();
    searchOptions.setAction("Search for 'AgentBay SDK'");
    ActResult searchResult = agent.act(page, searchOptions);
}
```

### observe

```java
public ObserveResult observe(Page page, Object observeInput) throws BrowserException
```

Extract information from the page using natural language.

**Parameters:**
- `page` (Page): Playwright Page object
- `observeInput` (Object): ObserveOptions containing extraction instructions

**Returns:**
- `ObserveResult`: Result containing extracted data

**Throws:**
- `BrowserException`: If browser is not initialized or observation fails

**Example:**

```java
try (Playwright playwright = Playwright.create()) {
    Browser browser = playwright.chromium().connectOverCDP(endpointUrl);
    Page page = browser.contexts().get(0).newPage();
    
    BrowserAgent agent = session.getBrowser().getAgent();
    
    ObserveOptions options = new ObserveOptions();
    options.setInstruction("Extract all product names and prices");
    ObserveResult result = agent.observe(page, options);
    
    if (result.isSuccess()) {
        System.out.println("Extracted data: " + result.getData());
    }
}
```

## Common Patterns

### Basic Browser Automation

```java
// Create and initialize browser
CreateSessionParams params = new CreateSessionParams();
params.setImageId("browser_latest");
Session session = agentBay.create(params).getSession();

BrowserOption option = new BrowserOption();
option.setUseStealth(true);
session.getBrowser().initialize(option);

// Connect Playwright and automate
String endpoint = session.getBrowser().getEndpointUrl();
try (Playwright pw = Playwright.create()) {
    Browser browser = pw.chromium().connectOverCDP(endpoint);
    Page page = browser.contexts().get(0).newPage();
    
    page.navigate("https://example.com");
    page.click("button#submit");
    page.fill("input#email", "user@example.com");
    
    browser.close();
}

session.delete();
```

### Browser Context with Persistence

```java
// Create persistent context
ContextResult ctxResult = agentBay.getContext().get("my-browser-ctx", true);
Context context = ctxResult.getContext();

// Create BrowserContext
BrowserContext browserContext = new BrowserContext(context.getId(), true);

// Create session with context
CreateSessionParams params = new CreateSessionParams();
params.setImageId("browser_latest");
params.setBrowserContext(browserContext);
Session session = agentBay.create(params).getSession();

// Use browser (cookies will be persisted)
BrowserOption option = new BrowserOption();
session.getBrowser().initialize(option);

// Delete session WITH context sync to save browser data
agentBay.delete(session, true);

// Next session with same context will have cookies restored
Session session2 = agentBay.create(params).getSession();
session2.getBrowser().initialize(option);
// Cookies from first session are available!
agentBay.delete(session2, false);
```

### Stealth Mode with Human Behavior

```java
BrowserOption option = new BrowserOption();
option.setUseStealth(true);           // Avoid bot detection
option.setBehaviorSimulate(true);     // Human-like behavior
option.setSolveCaptchas(true);        // Auto-solve CAPTCHAs

session.getBrowser().initialize(option);
```

### Proxy Configuration

```java
BrowserProxy proxy = new BrowserProxy();
proxy.setType("http");
proxy.setServer("proxy.example.com:8080");
proxy.setUsername("user");
proxy.setPassword("password");

BrowserOption option = new BrowserOption();
option.setProxies(Arrays.asList(proxy));

session.getBrowser().initialize(option);
```

### Custom Viewport

```java
BrowserViewport viewport = new BrowserViewport();
viewport.setWidth(1920);
viewport.setHeight(1080);

BrowserOption option = new BrowserOption();
option.setViewport(viewport);

session.getBrowser().initialize(option);
```

### AI-Powered Automation with Agent

```java
// Initialize browser
CreateSessionParams params = new CreateSessionParams();
params.setImageId("browser_latest");
Session session = agentBay.create(params).getSession();

BrowserOption option = new BrowserOption();
option.setUseStealth(true);
session.getBrowser().initialize(option);

// Get Playwright page
String endpointUrl = session.getBrowser().getEndpointUrl();
try (Playwright playwright = Playwright.create()) {
    Browser browser = playwright.chromium().connectOverCDP(endpointUrl);
    Page page = browser.contexts().get(0).newPage();
    
    // Use AI agent for natural language automation
    BrowserAgent agent = session.getBrowser().getAgent();
    
    // Navigate
    ActOptions navOptions = new ActOptions();
    navOptions.setAction("Go to https://example.com");
    agent.act(page, navOptions);
    
    // Fill form
    ActOptions fillOptions = new ActOptions();
    fillOptions.setAction("Fill the email field with test@example.com");
    agent.act(page, fillOptions);
    
    // Submit
    ActOptions submitOptions = new ActOptions();
    submitOptions.setAction("Click the submit button");
    agent.act(page, submitOptions);
    
    browser.close();
}

session.delete();
```

## Best Practices

1. **Stealth Mode**: Enable stealth mode for web scraping to avoid detection
2. **Behavior Simulation**: Use behavior simulation for more realistic interactions
3. **Resource Cleanup**: Always close browser and delete session when done
4. **Error Handling**: Check initialization success before using browser
5. **Session Image**: Use `browser_latest` image for optimal browser support
6. **Timeouts**: Set appropriate timeouts for page loads and interactions
7. **Context Reuse**: Reuse browser contexts for better performance
8. **Agent Usage**: Use BrowserAgent for complex, natural language-driven automation

## Use Cases

- **Web Scraping**: Extract data from websites with stealth mode
- **Automated Testing**: Test web applications end-to-end with persistent sessions
- **Form Automation**: Fill and submit forms automatically
- **Screenshot Capture**: Take screenshots of web pages
- **Data Extraction**: Extract structured data from websites
- **E-commerce Automation**: Automate online shopping with persistent login sessions
- **Social Media Automation**: Automate social media interactions with cookie persistence
- **AI-Powered Testing**: Use natural language to describe test scenarios
- **Multi-Session Workflows**: Persist browser state across multiple automation sessions
- **Extension Integration**: Use browser extensions for enhanced functionality

## Limitations

- Browser automation requires `browser_latest` image
- AI-powered agent features may have additional latency
- CAPTCHA solving success rate depends on CAPTCHA type
- Some websites may still detect and block automation
- BrowserAgent requires Playwright Page object for all operations

## Important Notes

1. **Method Name**: Use `initialize()` method to set up the browser, not `init()`.
2. **Page Requirement**: BrowserAgent methods require a Playwright `Page` object.
3. **Error Handling**: Always check `isInitialized()` before calling `getEndpointUrl()`.
4. **Resource Management**: Proper cleanup is essential to avoid resource leaks.

## Related Resources

- [Browser Context Example](../../../agentbay/src/main/java/com/aliyun/agentbay/examples/BrowserContextExample.java) - Complete browser context usage examples
- [Playwright Example](../../../agentbay/src/main/java/com/aliyun/agentbay/examples/PlaywrightExample.java) - Basic Playwright integration
- [Visit Aliyun Example](../../../agentbay/src/main/java/com/aliyun/agentbay/examples/VisitAliyunExample.java) - Real-world automation
- [Game 2048 Example](../../../agentbay/src/main/java/com/aliyun/agentbay/examples/Game2048Example.java) - AI-powered automation
- [Playwright Java Documentation](https://playwright.dev/java/) - Official Playwright docs

---

*Documentation for AgentBay Java SDK*
