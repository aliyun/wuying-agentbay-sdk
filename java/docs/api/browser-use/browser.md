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
- **Automated Testing**: Test web applications end-to-end
- **Form Automation**: Fill and submit forms automatically
- **Screenshot Capture**: Take screenshots of web pages
- **Data Extraction**: Extract structured data from websites
- **E-commerce Automation**: Automate online shopping tasks
- **Social Media Automation**: Automate social media interactions
- **AI-Powered Testing**: Use natural language to describe test scenarios

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

- [Playwright Example](../../../agentbay/src/main/java/com/aliyun/agentbay/examples/PlaywrightExample.java)
- [Visit Aliyun Example](../../../agentbay/src/main/java/com/aliyun/agentbay/examples/VisitAliyunExample.java)
- [Game 2048 Example](../../../agentbay/src/main/java/com/aliyun/agentbay/examples/Game2048Example.java)
- [Playwright Java Documentation](https://playwright.dev/java/)

---

*Documentation for AgentBay Java SDK*
