# Browser Fingerprint Guide

Browser fingerprinting is a crucial feature for web automation that helps avoid detection by anti-bot systems. AgentBay provides comprehensive fingerprint management capabilities including generation, customization, and persistence across sessions.

## Overview

AgentBay supports advanced browser fingerprint management with the following key capabilities:

- **Multiple Generation Methods**: Random generation, local browser sync, and custom construction
- **Fingerprint Persistence**: Maintain consistent fingerprints across multiple sessions
- **Context Management**: Persistent storage using browser and fingerprint contexts

## 1. Fingerprint Generation Methods

### 1.1 Random Fingerprint Generation

Generate random fingerprints based on specified criteria such as device type, operating system, and locale.

#### Features
- Automatic randomization of browser characteristics
- Configurable device types (desktop/mobile)
- Operating system selection (Windows, macOS, Linux, Android, iOS)
- Locale and language customization

#### Python Example

```python
import os
from agentbay import AgentBay
from agentbay import CreateSessionParams
from agentbay import BrowserOption, BrowserFingerprint
from playwright.sync_api import sync_playwright

def random_fingerprint_example():
    # Initialize AgentBay client
    api_key = os.getenv("AGENTBAY_API_KEY")
    if not api_key:
        print("Error: AGENTBAY_API_KEY environment variable not set")
        return
    
    agent_bay = AgentBay(api_key=api_key)
    
    # Create session
    params = CreateSessionParams(image_id="browser_latest")
    session_result = agent_bay.create(params)
    
    if session_result.success:
        session = session_result.session
        print(f"Session created with ID: {session.session_id}")
        
        # Configure random fingerprint
        browser_fingerprint = BrowserFingerprint(
            devices=["desktop"],
            operating_systems=["windows"],
            locales=["zh-CN", "zh"]
        )
        
        # Enable stealth mode with random fingerprint
        browser_option = BrowserOption(
            use_stealth=True,
            fingerprint=browser_fingerprint
        )
        
        # Initialize browser
        if session.browser.initialize(browser_option):
            endpoint_url = session.browser.get_endpoint_url()
            print("endpoint_url =", endpoint_url)
            
            # Connect using Playwright
            with sync_playwright() as p:
                browser = p.chromium.connect_over_cdp(endpoint_url)
                context = browser.contexts[0]
                page = context.new_page()
                
                # Test fingerprint
                print("\n--- Check User Agent ---")
                page.goto("https://httpbin.org/user-agent")
                response = page.evaluate("() => JSON.parse(document.body.textContent)")
                user_agent = response.get("user-agent", "")
                print(f"User Agent: {user_agent}")
                
                # Check navigator properties
                print("\n--- Check Navigator Properties ---")
                nav_info = page.evaluate("""
                    () => ({
                        platform: navigator.platform,
                        language: navigator.language,
                        languages: navigator.languages,
                        webdriver: navigator.webdriver
                    })
                """)
                
                print(f"Platform: {nav_info.get('platform')}")
                print(f"Language: {nav_info.get('language')}")
                print(f"Languages: {nav_info.get('languages')}")
                print(f"WebDriver: {nav_info.get('webdriver')}")
                
                page.wait_for_timeout(3000)
                browser.close()
        
        # Clean up session
        agent_bay.delete(session)

if __name__ == "__main__":
    random_fingerprint_example()
```

#### TypeScript Example

```typescript
import { AgentBay, CreateSessionParams } from 'wuying-agentbay-sdk';
import { BrowserOption, BrowserFingerprint } from 'wuying-agentbay-sdk';
import { chromium } from 'playwright';

async function randomFingerprintExample(): Promise<void> {
    // Get API key from environment variable
    const apiKey = process.env.AGENTBAY_API_KEY;
    if (!apiKey) {
        console.log("Error: AGENTBAY_API_KEY environment variable not set");
        return;
    }

    try {
        // Initialize AgentBay client
        console.log("Initializing AgentBay client...");
        const agentBay = new AgentBay({ apiKey });
        
        // Create session
        console.log("Creating a new session...");
        const params: CreateSessionParams = {
            imageId: "browser_latest"
        };
        const sessionResult = await agentBay.create(params);
        
        if (!sessionResult.success) {
            console.log("Failed to create session");
            return;
        }

        const session = sessionResult.session;
        console.log(`Session created with ID: ${session.sessionId}`);
        
        // Configure random fingerprint
        const browserFingerprint: BrowserFingerprint = {
            devices: ["desktop"],
            operatingSystems: ["windows"],
            locales: ["zh-CN", "zh"]
        };
        
        // Enable stealth mode with random fingerprint
        const browserOption: BrowserOption = {
            useStealth: true,
            fingerprint: browserFingerprint
        };
        
        // Initialize browser
        const initialized = await session.browser.initializeAsync(browserOption);
        if (!initialized) {
            console.log("Failed to initialize browser");
            return;
        }

        const endpointUrl = await session.browser.getEndpointUrl();
        console.log("endpoint_url =", endpointUrl);
        
        // Connect using Playwright
        const browser = await chromium.connectOverCDP(endpointUrl);
        const context = browser.contexts()[0];
        const page = await context.newPage();
        
        // Test fingerprint
        console.log("\n--- Check User Agent ---");
        await page.goto("https://httpbin.org/user-agent");
        const response = await page.evaluate(() => JSON.parse(document.body.textContent));
        const userAgent = response["user-agent"] || "";
        console.log(`User Agent: ${userAgent}`);

        // Check navigator properties
        console.log("\n--- Check Navigator Properties ---");
        const navInfo = await page.evaluate(() => ({
            platform: navigator.platform,
            language: navigator.language,
            languages: navigator.languages,
            webdriver: navigator.webdriver
        }));

        console.log(`Platform: ${navInfo.platform}`);
        console.log(`Language: ${navInfo.language}`);
        console.log(`Languages: ${navInfo.languages}`);
        console.log(`WebDriver: ${navInfo.webdriver}`);

        await page.waitForTimeout(3000);
        await browser.close();
        
        // Clean up session
        await agentBay.delete(session);
        console.log("Session cleaned up successfully");

    } catch (error) {
        console.error("Error in main function:", error);
    }
}

randomFingerprintExample().catch(console.error);
```

### 1.2 Local Browser Fingerprint Sync

Capture fingerprint characteristics from your local Chrome browser and apply them to remote sessions for consistent behavior.

#### Features
- Extract fingerprint from local Chrome installation
- Preserve exact browser characteristics
- Maintain consistency between local and remote environments
- Support for both headless and visible mode extraction

#### Python Example

```python
import os
from agentbay import AgentBay
from agentbay import CreateSessionParams
from agentbay import BrowserOption
from agentbay import BrowserFingerprintGenerator
from playwright.sync_api import sync_playwright

def local_sync_fingerprint_example():
    # Initialize AgentBay client
    api_key = os.getenv("AGENTBAY_API_KEY")
    if not api_key:
        print("Error: AGENTBAY_API_KEY environment variable not set")
        return
    
    print("Initializing AgentBay client...")
    agent_bay = AgentBay(api_key=api_key)
    
    # Create session
    print("Creating a new session...")
    params = CreateSessionParams(image_id="browser_latest")
    session_result = agent_bay.create(params)
    
    if session_result.success:
        session = session_result.session
        print(f"Session created with ID: {session.session_id}")
        
        # Generate fingerprint from local Chrome browser
        fingerprint_generator = BrowserFingerprintGenerator()
        fingerprint_format = fingerprint_generator.generate_fingerprint()
        
        if not fingerprint_format:
            print("Failed to generate local fingerprint")
            return
        
        print("Local fingerprint extracted successfully")
        
        # Apply local fingerprint to remote browser
        browser_option = BrowserOption(
            use_stealth=True,
            fingerprint_format=fingerprint_format
        )
        
        # Initialize browser
        if session.browser.initialize(browser_option):
            endpoint_url = session.browser.get_endpoint_url()
            print("endpoint_url =", endpoint_url)
            
            # Connect using Playwright
            with sync_playwright() as p:
                browser = p.chromium.connect_over_cdp(endpoint_url)
                context = browser.contexts[0]
                page = context.new_page()
                
                # Check user agent
                print("\n--- Check User Agent ---")
                page.goto("https://httpbin.org/user-agent")
                
                # Wait for page to load completely
                page.wait_for_load_state("networkidle")
                
                # Get the response text more safely
                try:
                    response_text = page.evaluate("() => document.body.innerText.trim()")
                    print(f"Raw response: {response_text}")
                    
                    import json
                    response = json.loads(response_text)
                    user_agent = response.get("user-agent", "")
                    print(f"User Agent: {user_agent}")
                except json.JSONDecodeError as e:
                    print(f"Failed to parse JSON response: {e}")
                    print(f"Raw response content: {response_text}")
                    # Fallback: try to get user agent directly
                    user_agent = page.evaluate("() => navigator.userAgent")
                    print(f"Fallback User Agent: {user_agent}")
                except Exception as e:
                    print(f"Error getting user agent: {e}")
                    user_agent = page.evaluate("() => navigator.userAgent")
                    print(f"Fallback User Agent: {user_agent}")
                
                print("Please check if User Agent is synced correctly by visiting https://httpbin.org/user-agent in local chrome browser.")
                
                page.wait_for_timeout(3000)
                browser.close()
        
        # Clean up session
        agent_bay.delete(session)

if __name__ == "__main__":
    local_sync_fingerprint_example()
```

#### TypeScript Example

```typescript
import { AgentBay, CreateSessionParams } from 'wuying-agentbay-sdk';
import { BrowserOption, BrowserFingerprintGenerator } from 'wuying-agentbay-sdk';
import { chromium } from 'playwright';

async function localSyncFingerprintExample(): Promise<void> {
    const apiKey = process.env.AGENTBAY_API_KEY;
    if (!apiKey) {
        console.log("Error: AGENTBAY_API_KEY environment variable not set");
        return;
    }

    try {
        // Initialize AgentBay client
        console.log("Initializing AgentBay client...");
        const agentBay = new AgentBay({ apiKey });
        
        // Create session
        console.log("Creating a new session...");
        const params: CreateSessionParams = {
            imageId: "browser_latest"
        };
        const sessionResult = await agentBay.create(params);
        
        if (!sessionResult.success) {
            console.log("Failed to create session");
            return;
        }

        const session = sessionResult.session;
        console.log(`Session created with ID: ${session.sessionId}`);
        
        // Generate fingerprint from local Chrome browser
        console.log("Starting fingerprint generation");
        console.log("Extracting comprehensive browser fingerprint...");
        const fingerprintGenerator = new BrowserFingerprintGenerator();
        const fingerprintFormat = await fingerprintGenerator.generateFingerprint();
        
        if (!fingerprintFormat) {
            console.log("Failed to generate local fingerprint");
            return;
        }
        
        console.log("Fingerprint generation completed successfully!");
        console.log(`Fingerprint format: ${JSON.stringify(fingerprintFormat)}`);
        
        // Apply local fingerprint to remote browser
        const browserOption: BrowserOption = {
            useStealth: true,
            fingerprintFormat: fingerprintFormat
        };
        
        // Initialize browser
        const initialized = await session.browser.initializeAsync(browserOption);
        if (!initialized) {
            console.log("Failed to initialize browser");
            return;
        }

        const endpointUrl = await session.browser.getEndpointUrl();
        console.log("endpoint_url =", endpointUrl);
        
        // Connect using Playwright
        const browser = await chromium.connectOverCDP(endpointUrl);
        const context = browser.contexts()[0];
        const page = await context.newPage();
        
        // Verify fingerprint sync
        console.log("\n--- Check User Agent ---");
        await page.goto("https://httpbin.org/user-agent");
        const response = await page.evaluate(() => JSON.parse(document.body.textContent));
        const userAgent = response["user-agent"] || "";
        console.log(`User Agent: ${userAgent}`);

        console.log("Please check if User Agent is synced correctly by visiting https://httpbin.org/user-agent in local chrome browser.");

        await page.waitForTimeout(3000);
        await browser.close();
        
        // Clean up session
        await agentBay.delete(session);
        console.log("Session cleaned up successfully");

    } catch (error) {
        console.error("Error in main function:", error);
    }
}

localSyncFingerprintExample().catch(console.error);
```

### 1.3 Custom Fingerprint Construction

Load and apply custom fingerprint data from JSON files or construct fingerprints programmatically.

#### Features
- Load fingerprint from JSON files
- Construct fingerprints programmatically
- Full control over all fingerprint characteristics
- Reusable fingerprint configurations

#### Python Example

```python
import os
from agentbay import AgentBay
from agentbay import CreateSessionParams
from agentbay import BrowserOption
from agentbay import FingerprintFormat
from playwright.sync_api import sync_playwright

def generate_fingerprint_by_file() -> FingerprintFormat:
    """Generate fingerprint by file."""
    with open(os.path.join(os.path.dirname(__file__), "../../resource/fingerprint.example.json"), "r") as f:
        fingerprint_format = FingerprintFormat.load(f.read())
    return fingerprint_format

def custom_fingerprint_example():
    # Initialize AgentBay client
    api_key = os.getenv("AGENTBAY_API_KEY")
    if not api_key:
        print("Error: AGENTBAY_API_KEY environment variable not set")
        return
    
    print("Initializing AgentBay client...")
    agent_bay = AgentBay(api_key=api_key)
    
    # Create session
    print("Creating a new session...")
    params = CreateSessionParams(image_id="browser_latest")
    try:
        session_result = agent_bay.create(params)
    except Exception as e:
        print(f"Failed to create session: {e}")
        return
    
    if session_result.success:
        session = session_result.session
        print(f"Session created with ID: {session.session_id}")
        
        # You can generate fingerprint by file or construct FingerprintFormat by yourself totally.
        fingerprint_format = generate_fingerprint_by_file()
        
        # Apply custom fingerprint to browser
        browser_option = BrowserOption(
            use_stealth=True,
            fingerprint_format=fingerprint_format
        )
        
        # Initialize browser
        try:
            browser_init_result = session.browser.initialize(browser_option)
            if not browser_init_result:
                print("Failed to initialize browser")
                agent_bay.delete(session)
                return
        except Exception as e:
            print(f"Failed to initialize browser: {e}")
            agent_bay.delete(session)
            return
        
        endpoint_url = session.browser.get_endpoint_url()
        print("endpoint_url =", endpoint_url)
        
        # Connect using Playwright
        with sync_playwright() as p:
            browser = p.chromium.connect_over_cdp(endpoint_url)
            context = browser.contexts[0]
            page = context.new_page()
            
            # Check user agent
            print("\n--- Check User Agent ---")
            page.goto("https://httpbin.org/user-agent")
            
            # Wait for page to load completely
            page.wait_for_load_state("networkidle")
            
            # Get the response text more safely
            try:
                response_text = page.evaluate("() => document.body.innerText.trim()")
                print(f"Raw response: {response_text}")
                
                import json
                response = json.loads(response_text)
                user_agent = response.get("user-agent", "")
                print(f"User Agent: {user_agent}")
                assert user_agent == fingerprint_format.fingerprint.navigator.userAgent
                print("User Agent constructed correctly")
            except json.JSONDecodeError as e:
                print(f"Failed to parse JSON response: {e}")
                print(f"Raw response content: {response_text}")
                # Fallback: try to get user agent directly
                user_agent = page.evaluate("() => navigator.userAgent")
                print(f"Fallback User Agent: {user_agent}")
                assert user_agent == fingerprint_format.fingerprint.navigator.userAgent
                print("User Agent constructed correctly (fallback)")
            except Exception as e:
                print(f"Error getting user agent: {e}")
                user_agent = page.evaluate("() => navigator.userAgent")
                print(f"Fallback User Agent: {user_agent}")
                assert user_agent == fingerprint_format.fingerprint.navigator.userAgent
                print("User Agent constructed correctly (fallback)")
            
            page.wait_for_timeout(3000)
            browser.close()
        
        # Clean up session
        agent_bay.delete(session)
    else:
        print(f"Failed to create session: {session_result}")
        if hasattr(session_result, 'error_message'):
            print(f"Error message: {session_result.error_message}")

if __name__ == "__main__":
    custom_fingerprint_example()
```

#### TypeScript Example

```typescript
import { AgentBay, CreateSessionParams } from 'wuying-agentbay-sdk';
import { BrowserOption, FingerprintFormat } from 'wuying-agentbay-sdk';
import { chromium } from 'playwright';
import * as fs from 'fs';
import * as path from 'path';

async function generateFingerprintByFile(): Promise<FingerprintFormat> {
    /**
     * Generate fingerprint by file.
     */
    const fingerprintPath = path.join(__dirname, "../../../../../resource/fingerprint.example.json");
    const fingerprintData = fs.readFileSync(fingerprintPath, 'utf8');
    return FingerprintFormat.fromJson(fingerprintData);
}

async function customFingerprintExample(): Promise<void> {
    const apiKey = process.env.AGENTBAY_API_KEY;
    if (!apiKey) {
        console.log("Error: AGENTBAY_API_KEY environment variable not set");
        return;
    }

    try {
        // Initialize AgentBay client
        console.log("Initializing AgentBay client...");
        const agentBay = new AgentBay({ apiKey });
        
        // Create session
        console.log("Creating a new session...");
        const params: CreateSessionParams = {
            imageId: "browser_latest"
        };
        const sessionResult = await agentBay.create(params);
        
        if (!sessionResult.success) {
            console.log("Failed to create session");
            return;
        }

        const session = sessionResult.session;
        console.log(`Session created with ID: ${session.sessionId}`);
        
        // You can generate fingerprint by file or construct FingerprintFormat by yourself totally.
        const fingerprintFormat = await generateFingerprintByFile();
        
        // Apply custom fingerprint to browser
        const browserOption: BrowserOption = {
            useStealth: true,
            fingerprintFormat: fingerprintFormat
        };
        
        // Initialize browser
        const initialized = await session.browser.initializeAsync(browserOption);
        if (!initialized) {
            console.log("Failed to initialize browser");
            return;
        }

        const endpointUrl = await session.browser.getEndpointUrl();
        console.log("endpoint_url =", endpointUrl);
        
        // Connect using Playwright
        const browser = await chromium.connectOverCDP(endpointUrl);
        const context = browser.contexts()[0];
        const page = await context.newPage();
        
        // Verify custom fingerprint
        console.log("\n--- Check User Agent ---");
        await page.goto("https://httpbin.org/user-agent");
        const response = await page.evaluate(() => JSON.parse(document.body.textContent));
        const userAgent = response["user-agent"] || "";
        console.log(`User Agent: ${userAgent}`);
        
        // Verify that the user agent matches the fingerprint format
        if (fingerprintFormat.fingerprint?.navigator?.userAgent) {
            if (userAgent === fingerprintFormat.fingerprint.navigator.userAgent) {
                console.log("User Agent constructed correctly");
            } else {
                console.log("User Agent mismatch");
            }
        }

        await page.waitForTimeout(3000);
        await browser.close();
        
        // Clean up session
        await agentBay.delete(session);
        console.log("Session cleaned up successfully");

    } catch (error) {
        console.error("Error in main function:", error);
    }
}

customFingerprintExample().catch(console.error);
```

## 2. Fingerprint Persistence

Fingerprint persistence allows you to maintain consistent browser characteristics across multiple sessions by using browser contexts and fingerprint contexts.

### Features
- Persistent fingerprint storage across sessions
- Context-based fingerprint management
- Support for all fingerprint generation methods
- Automatic fingerprint loading and saving

### How It Works

1. **First Session**: Generate or apply a fingerprint with `fingerprint_persistent=True`
2. **Context Sync**: Save the session with `sync_context=True` to persist the fingerprint
3. **Subsequent Sessions**: Create new sessions with the same contexts to reuse the fingerprint

### Python Example (Random Fingerprint Persistence)

```python
import os
import time
from agentbay import AgentBay
from agentbay import CreateSessionParams, BrowserContext
from agentbay import BrowserOption, BrowserFingerprint, BrowserFingerprintContext
from playwright.sync_api import sync_playwright

# Global variables for persistent context and fingerprint context
persistent_context = None
persistent_fingerprint_context = None

def run_as_first_time():
    """Run as first time"""
    print("="*20)
    print("Run as first time")
    print("="*20)
    global persistent_context, persistent_fingerprint_context
    api_key = os.environ.get("AGENTBAY_API_KEY")
    if not api_key:
        print("Error: AGENTBAY_API_KEY environment variable not set")
        return

    agent_bay = AgentBay(api_key)

    # Create a browser context for first time
    session_context_name = f"test-browser-context-{int(time.time())}"
    context_result = agent_bay.context.get(session_context_name, True)
    if not context_result.success or not context_result.context:
        print("Failed to create browser context")
        return

    persistent_context = context_result.context
    print(f"Created browser context: {persistent_context.name} (ID: {persistent_context.id})")

    # Create a browser fingerprint context for first time
    fingerprint_context_name = f"test-browser-fingerprint-{int(time.time())}"
    fingerprint_context_result = agent_bay.context.get(fingerprint_context_name, True)
    if not fingerprint_context_result.success or not fingerprint_context_result.context:
        print("Failed to create fingerprint context")
        return
    
    persistent_fingerprint_context = fingerprint_context_result.context
    print(f"Created fingerprint context: {persistent_fingerprint_context.name} (ID: {persistent_fingerprint_context.id})")

    # Create session with BrowserContext and FingerprintContext
    print(f"Creating session with browser context ID: {persistent_context.id} "
            f"and fingerprint context ID: {persistent_fingerprint_context.id}")
    fingerprint_context = BrowserFingerprintContext(persistent_fingerprint_context.id)
    browser_context = BrowserContext(persistent_context.id, auto_upload=True, fingerprint_context=fingerprint_context)
    params = CreateSessionParams(
        image_id="browser_latest",
        browser_context=browser_context
    )

    session_result = agent_bay.create(params)
    if not session_result.success or not session_result.session:
        print(f"Failed to create first session: {session_result.error_message}")
        return

    session = session_result.session
    print(f"First session created with ID: {session.session_id}")

    # Initialize browser with fingerprint persistent enabled and set fingerprint generation options
    browser_option = BrowserOption(
        use_stealth=True,
        fingerprint_persistent=True,
        fingerprint=BrowserFingerprint(
            devices=["desktop"],
            operating_systems=["windows"],
            locales=["zh-CN"],
        ),
    )
    init_success = session.browser.initialize(browser_option)
    if not init_success:
        print("Failed to initialize browser")
        return
    print("First session browser initialized successfully")

    # Get endpoint URL
    endpoint_url = session.browser.get_endpoint_url()
    if not endpoint_url:
        print("Failed to get browser endpoint URL")
        return
    print(f"First session browser endpoint URL: {endpoint_url}")

    # Connect with playwright, test first session fingerprint
    print("Opening https://httpbin.org/user-agent and test user agent...")
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(endpoint_url)
        context = browser.contexts[0] if browser.contexts else browser.new_context()

        page = context.new_page()
        page.goto("https://httpbin.org/user-agent", timeout=60000)
        response = page.evaluate("() => JSON.parse(document.body.innerText)")
        user_agent = response["user-agent"]
        print("user_agent =", user_agent)

        context.close()
        print("First session browser fingerprint check completed")

    # Delete first session with syncContext=True
    print("Deleting first session with syncContext=True...")
    delete_result = agent_bay.delete(session, sync_context=True)
    print(f"First session deleted successfully (RequestID: {delete_result.request_id})")


def run_as_second_time():
    """Run as second time"""
    print("="*20)
    print("Run as second time")
    print("="*20)
    global persistent_context, persistent_fingerprint_context
    api_key = os.environ.get("AGENTBAY_API_KEY")
    if not api_key:
        print("Error: AGENTBAY_API_KEY environment variable not set")
        return

    agent_bay = AgentBay(api_key)

    # Create second session with same browser context and fingerprint context
    print(f"Creating second session with same browser context ID: {persistent_context.id} "
            f"and fingerprint context ID: {persistent_fingerprint_context.id}")
    fingerprint_context = BrowserFingerprintContext(persistent_fingerprint_context.id)
    browser_context = BrowserContext(persistent_context.id, auto_upload=True, fingerprint_context=fingerprint_context)
    params = CreateSessionParams(
        image_id="browser_latest",
        browser_context=browser_context
    )
    session_result = agent_bay.create(params)
    if not session_result.success or not session_result.session:
        print(f"Failed to create second session: {session_result.error_message}")
        return

    session = session_result.session
    print(f"Second session created with ID: {session.session_id}")

    # Initialize browser with fingerprint persistent enabled but not specific fingerprint generation options
    browser_option = BrowserOption(
        use_stealth=True,
        fingerprint_persistent=True,
    )
    init_success = session.browser.initialize(browser_option)
    if not init_success:
        print("Failed to initialize browser in second session")
        return
    print("Second session browser initialized successfully")

    # Get endpoint URL
    endpoint_url = session.browser.get_endpoint_url()
    if not endpoint_url:
        print("Failed to get browser endpoint URL in second session")
        return
    print(f"Second session browser endpoint URL: {endpoint_url}")

    # Connect with playwright and test second session fingerprint
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(endpoint_url)
        context = browser.contexts[0] if browser.contexts else browser.new_context()
        page = context.new_page()
        page.goto("https://httpbin.org/user-agent", timeout=60000)
        response = page.evaluate("() => JSON.parse(document.body.innerText)")
        user_agent = response["user-agent"]
        print("user_agent =", user_agent)
        print(f"SUCCESS: fingerprint persisted correctly!")

        context.close()
        print("Second session browser fingerprint check completed")

    # Delete second session with syncContext=True
    print("Deleting second session with syncContext=True...")
    delete_result = agent_bay.delete(session, sync_context=True)
    print(f"Second session deleted successfully (RequestID: {delete_result.request_id})")


def fingerprint_persistence_example():
    """Test browser fingerprint persist across sessions with the same browser and fingerprint context."""
    run_as_first_time()
    time.sleep(3)
    run_as_second_time()

if __name__ == "__main__":
    fingerprint_persistence_example()
```

### TypeScript Example (Random Fingerprint Persistence)

```typescript
import { AgentBay, CreateSessionParams } from 'wuying-agentbay-sdk';
import { BrowserOption, BrowserFingerprint, BrowserContext, BrowserFingerprintContext } from 'wuying-agentbay-sdk';
import { chromium } from 'playwright';

// Global variables for persistent context and fingerprint context
let persistentContext: any = null;
let persistentFingerprintContext: any = null;

function getTestApiKey(): string {
    const apiKey = process.env.AGENTBAY_API_KEY;
    if (!apiKey) {
        throw new Error("AGENTBAY_API_KEY environment variable not set");
    }
    return apiKey;
}

function isWindowsUserAgent(userAgent: string): boolean {
    if (!userAgent) {
        return false;
    }
    const userAgentLower = userAgent.toLowerCase();
    const windowsIndicators = [
        'windows nt',
        'win32',
        'win64',
        'windows',
        'wow64'
    ];
    return windowsIndicators.some(indicator => userAgentLower.includes(indicator));
}

async function runAsFirstTime(): Promise<void> {
    console.log("====================");
    console.log("Run as first time");
    console.log("====================");

    const apiKey = getTestApiKey();
    const agentBay = new AgentBay({ apiKey });

    // Create a browser context for first time
    const sessionContextName = `test-browser-context-${Date.now()}`;
    const contextResult = await agentBay.context.get(sessionContextName, true);
    if (!contextResult.success || !contextResult.context) {
        console.log("Failed to create browser context");
        return;
    }

    persistentContext = contextResult.context;
    console.log(`Created browser context: ${persistentContext.name} (ID: ${persistentContext.id})`);

    // Create a browser fingerprint context for first time
    const fingerprintContextName = `test-browser-fingerprint-${Date.now()}`;
    const fingerprintContextResult = await agentBay.context.get(fingerprintContextName, true);
    if (!fingerprintContextResult.success || !fingerprintContextResult.context) {
        console.log("Failed to create fingerprint context");
        return;
    }

    persistentFingerprintContext = fingerprintContextResult.context;
    console.log(`Created fingerprint context: ${persistentFingerprintContext.name} (ID: ${persistentFingerprintContext.id})`);

    // Create session with BrowserContext and FingerprintContext
    console.log(`Creating session with browser context ID: ${persistentContext.id} ` +
                `and fingerprint context ID: ${persistentFingerprintContext.id}`);
    
    const fingerprintContext = new BrowserFingerprintContext(persistentFingerprintContext.id);
    const browserContext = new BrowserContext(persistentContext.id, true, undefined, fingerprintContext);
    
    const params = new CreateSessionParams()
        .withImageId("browser_latest")
        .withBrowserContext(browserContext);

    const sessionResult = await agentBay.create(params);
    if (!sessionResult.success || !sessionResult.session) {
        console.log(`Failed to create first session: ${sessionResult.errorMessage}`);
        return;
    }

    const session = sessionResult.session;
    console.log(`First session created with ID: ${session.sessionId}`);

    // Initialize browser with fingerprint persistent enabled and set fingerprint generation options
    const browserOption: BrowserOption = {
        useStealth: true,
        fingerprintPersistent: true,
        fingerprint: {
            devices: ["desktop"],
            operatingSystems: ["windows"],
            locales: ["zh-CN"]
        } as BrowserFingerprint
    };

    const initSuccess = await session.browser.initializeAsync(browserOption);
    if (!initSuccess) {
        console.log("Failed to initialize browser");
        return;
    }
    console.log("First session browser initialized successfully");

    // Get endpoint URL and test fingerprint
    const endpointUrl = await session.browser.getEndpointUrl();
    if (!endpointUrl) {
        console.log("Failed to get browser endpoint URL");
        return;
    }
    console.log(`First session browser endpoint URL: ${endpointUrl}`);

    // Connect with playwright, test first session fingerprint
    console.log("Opening https://httpbin.org/user-agent and test user agent...");
    const browser = await chromium.connectOverCDP(endpointUrl);
    const context = browser.contexts().length > 0 ? browser.contexts()[0] : await browser.newContext();

    const page = await context.newPage();
    await page.goto("https://httpbin.org/user-agent", { timeout: 60000 });
    const response = await page.evaluate(() => JSON.parse(document.body.textContent));
    const userAgent = response["user-agent"];
    console.log("user_agent =", userAgent);
    
    const isWindows = isWindowsUserAgent(userAgent);
    if (!isWindows) {
        console.log("Failed to get windows user agent");
        return;
    }

    await context.close();
    console.log("First session browser fingerprint check completed");

    // Delete first session with syncContext=true
    console.log("Deleting first session with syncContext=true...");
    const deleteResult = await agentBay.delete(session, { syncContext: true });
    console.log(`First session deleted successfully (RequestID: ${deleteResult.requestId})`);
}

async function runAsSecondTime(): Promise<void> {
    console.log("====================");
    console.log("Run as second time");
    console.log("====================");

    const apiKey = getTestApiKey();
    const agentBay = new AgentBay({ apiKey });

    // Create second session with same browser context and fingerprint context
    console.log(`Creating second session with same browser context ID: ${persistentContext.id} ` +
                `and fingerprint context ID: ${persistentFingerprintContext.id}`);
    
    const fingerprintContext = new BrowserFingerprintContext(persistentFingerprintContext.id);
    const browserContext = new BrowserContext(persistentContext.id, true, undefined, fingerprintContext);
    
    const params = new CreateSessionParams()
        .withImageId("browser_latest")
        .withBrowserContext(browserContext);

    const sessionResult = await agentBay.create(params);
    if (!sessionResult.success || !sessionResult.session) {
        console.log(`Failed to create second session: ${sessionResult.errorMessage}`);
        return;
    }

    const session = sessionResult.session;
    console.log(`Second session created with ID: ${session.sessionId}`);

    // Initialize browser with fingerprint persistent enabled but not specific fingerprint generation options
    const browserOption: BrowserOption = {
        useStealth: true,
        fingerprintPersistent: true
    };

    const initSuccess = await session.browser.initializeAsync(browserOption);
    if (!initSuccess) {
        console.log("Failed to initialize browser in second session");
        return;
    }
    console.log("Second session browser initialized successfully");

    // Get endpoint URL and test fingerprint persistence
    const endpointUrl = await session.browser.getEndpointUrl();
    if (!endpointUrl) {
        console.log("Failed to get browser endpoint URL in second session");
        return;
    }
    console.log(`Second session browser endpoint URL: ${endpointUrl}`);

    // Connect with playwright and test second session fingerprint
    const browser = await chromium.connectOverCDP(endpointUrl);
    const context = browser.contexts().length > 0 ? browser.contexts()[0] : await browser.newContext();
    const page = await context.newPage();
    await page.goto("https://httpbin.org/user-agent", { timeout: 60000 });
    const response = await page.evaluate(() => JSON.parse(document.body.textContent));
    const userAgent = response["user-agent"];
    console.log("user_agent =", userAgent);
    
    const isWindows = isWindowsUserAgent(userAgent);
    if (!isWindows) {
        console.log("Failed to get windows user agent in second session");
        return;
    }
    console.log("SUCCESS: fingerprint persisted correctly!");

    await context.close();
    console.log("Second session browser fingerprint check completed");

    // Delete second session with syncContext=true
    console.log("Deleting second session with syncContext=true...");
    const deleteResult = await agentBay.delete(session, { syncContext: true });
    console.log(`Second session deleted successfully (RequestID: ${deleteResult.requestId})`);
}

async function fingerprintPersistenceExample(): Promise<void> {
    /**
     * Test browser fingerprint persist across sessions with the same browser and fingerprint context.
     */
    try {
        await runAsFirstTime();
        await new Promise(resolve => setTimeout(resolve, 3000)); // Wait 3 seconds
        await runAsSecondTime();
    } catch (error) {
        console.error("Error in main function:", error);
    }
}

fingerprintPersistenceExample().catch(console.error);
```

### Persistence with Other Fingerprint Types

The fingerprint persistence feature works with all three generation methods:

#### Local Sync Persistence
```python
# First session: Generate from local browser and persist
fingerprint_generator = BrowserFingerprintGenerator()
fingerprint_format = fingerprint_generator.generate_fingerprint()

browser_option = BrowserOption(
    use_stealth=True,
    fingerprint_persistent=True,
    fingerprint_format=fingerprint_format  # From BrowserFingerprintGenerator
)
```

#### Custom Fingerprint Persistence
```python
# First session: Load custom fingerprint and persist
with open("path/to/fingerprint.json", "r") as f:
    fingerprint_format = FingerprintFormat.load(f.read())

browser_option = BrowserOption(
    use_stealth=True,
    fingerprint_persistent=True,
    fingerprint_format=fingerprint_format  # From JSON file or constructed
)
```

## Best Practices

### 1. Browser Context Usage

**💡 Important**: Always use the pre-created browser context provided by AgentBay SDK.

```python
# ✅ Correct - Use the existing context
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(endpoint_url)
    context = browser.contexts[0]  # Use the default context
    page = context.new_page()
```

```python
# ❌ Incorrect - Creating new context breaks stealth features
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(endpoint_url)
    context = browser.new_context()  # Don't do this
    page = context.new_page()
```

### 2. Important Notice

All fingerprint generation methods require `use_stealth=True` configuration, otherwise fingerprint settings will not take effect. This is because fingerprint functionality depends on stealth mode to properly apply browser feature masking.

```python
# ✅ Correct - Always enable stealth mode for fingerprints
browser_option = BrowserOption(
    use_stealth=True,  # Required for fingerprint to work
    fingerprint=BrowserFingerprint(
        devices=["desktop"],
        operating_systems=["windows"],
        locales=["en-US"]
    )
)

# Initialize browser with fingerprint
session.browser.initialize(browser_option)
```

```python
# ❌ Incorrect - Missing use_stealth=True
browser_option = BrowserOption(
    # use_stealth=True is missing!
    fingerprint=BrowserFingerprint(
        devices=["desktop"],
        operating_systems=["windows"],
        locales=["en-US"]
    )
)
# Fingerprint configuration will be ignored
```

### 3. Fingerprint Generation Strategy

#### Parameter Priority
When multiple fingerprint parameters are provided, the priority is:
1. `fingerprint_format` (customized generation)
2. `fingerprint` (random generation)

```python
# ✅ Correct - Use fingerprint_format for specific fingerprints
browser_option = BrowserOption(
    use_stealth=True,
    fingerprint_format=my_fingerprint_format
    # fingerprint parameter will be ignored
)
```

```python
# ❌ Avoid - user_agent disables fingerprint features
browser_option = BrowserOption(
    use_stealth=True,
    user_agent="Custom User Agent",
    fingerprint=BrowserFingerprint(...)  # Will be ignored
)
```

### 4. Fingerprint Persistence Behavior

When fingerprint persistence is enabled (`fingerprint_persistent=True`), the system behaves differently based on the fingerprint configuration type:

#### Using `fingerprint` Parameter
When configured with the `fingerprint` parameter, the system will **prioritize persisted fingerprints** over generating new random ones:

```python
# First run - generates and persists a random fingerprint
browser_option = BrowserOption(
    use_stealth=True,
    fingerprint_persistent=True,
    fingerprint=BrowserFingerprint(
        devices=["desktop"],
        operating_systems=["windows"],
        locales=["en-US"]
    )
)

# Subsequent runs - uses the same persisted fingerprint
# The fingerprint parameter serves as a template but won't generate new random values
```

#### Using `fingerprint_format` Parameter
When configured with the `fingerprint_format` parameter, the system will **override existing persisted fingerprints** because the user has explicitly configured the fingerprint parameters :

```python
# This will replace any existing persisted fingerprint
browser_option = BrowserOption(
    use_stealth=True,
    fingerprint_persistent=True,
    fingerprint_format=custom_fingerprint_format  # Overrides persisted data
)
```

#### Behavior Summary

| Configuration Type | Persistence Behavior |
|-------------------|---------------------|
| `fingerprint` | Uses persisted fingerprint if exists, otherwise generates and persists new random fingerprint |
| `fingerprint_format` | Always uses provided fingerprint and overwrites any existing persisted data |

```python
# ✅ Correct - Consistent fingerprint across sessions
browser_option = BrowserOption(
    use_stealth=True,
    fingerprint_persistent=True,
    fingerprint=BrowserFingerprint(devices=["desktop"])
)
# Will use the same fingerprint in all sessions

# ✅ Correct - Force update persisted fingerprint
browser_option = BrowserOption(
    use_stealth=True,
    fingerprint_persistent=True,
    fingerprint_format=new_fingerprint_data
)
# Will replace existing fingerprint with new data
```

### 5. Device and OS Compatibility

Ensure device types match operating systems:

```python
# ✅ Correct configurations
desktop_fingerprint = BrowserFingerprint(
    devices=["desktop"],
    operating_systems=["windows", "macos", "linux"]
)

mobile_fingerprint = BrowserFingerprint(
    devices=["mobile"],
    operating_systems=["android", "ios"]
)
```

```python
# ❌ Incorrect - mismatched device and OS
wrong_fingerprint = BrowserFingerprint(
    devices=["desktop"],
    operating_systems=["android", "ios"]  # Mobile OS with desktop device
)
```

### 6. Context Management for Persistence

- Create unique context names to avoid conflicts
- Use `sync_context=True` when deleting sessions to save fingerprints
- Clean up contexts after use to prevent resource leaks
- Wait for context sync to complete before creating new sessions

## Troubleshooting

### Common Issues

1. **Fingerprint Not Persisting**
   - Ensure `fingerprint_persistent=True` is set
   - Verify browser and fingerprint contexts are properly configured
   - Use `sync_context=True` when deleting sessions
   - Wait for context sync to complete

2. **Local Fingerprint Generation Fails**
   - Check if Chrome is installed and accessible
   - Try running with `headless=False` for debugging
   - Ensure sufficient permissions for browser automation

3. **Custom Fingerprint Loading Errors**
   - Verify JSON file format matches FingerprintFormat schema
   - Check file permissions and path accessibility
   - Validate fingerprint data completeness

## 📚 Related Guides

- [Browser Proxies](browser-proxies.md) - IP rotation and proxy configuration
- [CAPTCHA Resolution](captcha.md) - Automatic CAPTCHA handling
- [Browser Context](browser-context.md) - Cookie and session management
- [Browser Use Overview](../README.md) - Complete browser automation features

## 🆘 Getting Help

- [GitHub Issues](https://github.com/aliyun/wuying-agentbay-sdk/issues)
- [Documentation Home](../../README.md)