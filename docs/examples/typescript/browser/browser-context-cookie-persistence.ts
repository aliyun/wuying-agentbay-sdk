/**
 * Browser Context Cookie Persistence Example (TypeScript)
 * 
 * This example demonstrates how to use Browser Context to persist cookies
 * across multiple sessions in TypeScript. It shows the complete workflow of:
 * 1. Creating a session with Browser Context
 * 2. Setting cookies in the browser
 * 3. Deleting the session with context synchronization
 * 4. Creating a new session with the same Browser Context
 * 5. Verifying that cookies persist across sessions
 */

import { AgentBay, CreateSessionParams, BrowserContext, BrowserOption } from 'wuying-agentbay-sdk';
import { chromium } from 'playwright';

async function main(): Promise<void> {
    // Get API key from environment
    const apiKey = process.env.AGENTBAY_API_KEY;
    if (!apiKey) {
        console.error("Error: AGENTBAY_API_KEY environment variable not set");
        return;
    }

    // Initialize AgentBay client
    const agentBay = new AgentBay({ apiKey });
    console.log("AgentBay client initialized");

    // Create a unique context name for this demo
    const contextName = `browser-cookie-demo-${Date.now()}`;
    
    try {
        // Step 1: Create or get a persistent context for browser data
        console.log(`Step 1: Creating context '${contextName}'...`);
        const contextResult = await agentBay.context.get(contextName, true);
        
        if (!contextResult.success || !contextResult.context) {
            console.log(`Failed to create context: ${contextResult.errorMessage}`);
            return;
        }
            
        const context = contextResult.context;
        console.log(`Context created with ID: ${context.id}`);

        // Step 2: Create first session with Browser Context
        console.log("Step 2: Creating first session with Browser Context...");
        const browserContext: BrowserContext = {
            contextId: context.id,
            autoUpload: true
        };
        
        const params = new CreateSessionParams()
            .withImageId("imgc-wucyOiPmeV2Z753lq")  // Browser image ID
            .withBrowserContext(browserContext);
        
        const sessionResult = await agentBay.create(params);
        if (!sessionResult.success || !sessionResult.session) {
            console.log(`Failed to create first session: ${sessionResult.errorMessage}`);
            return;
        }
            
        const session1 = sessionResult.session;
        console.log(`First session created with ID: ${session1.sessionId}`);

        // Step 3: Initialize browser and set cookies
        console.log("Step 3: Initializing browser and setting test cookies...");
        
        // Initialize browser
        const initSuccess = await session1.browser.initializeAsync(new BrowserOption());
        if (!initSuccess) {
            console.log("Failed to initialize browser");
            return;
        }
            
        console.log("Browser initialized successfully");
        
        // Get endpoint URL
        const endpointUrl = session1.browser.getEndpointUrl();
        if (!endpointUrl) {
            console.log("Failed to get browser endpoint URL");
            return;
        }
            
        console.log(`Browser endpoint URL: ${endpointUrl}`);
        
        // Test data
        const testUrl = "https://www.aliyun.com";
        const testDomain = "aliyun.com";
        
        // Define test cookies
        const testCookies = [
            {
                name: "demo_cookie_1",
                value: "demo_value_1",
                domain: testDomain,
                path: "/",
                httpOnly: false,
                secure: false,
                expires: Math.floor(Date.now() / 1000) + 3600  // 1 hour from now
            },
            {
                name: "demo_cookie_2", 
                value: "demo_value_2",
                domain: testDomain,
                path: "/",
                httpOnly: false,
                secure: false,
                expires: Math.floor(Date.now() / 1000) + 3600  // 1 hour from now
            }
        ];
        
        // Connect with Playwright and set cookies
        const browser = await chromium.connectOverCDP(endpointUrl);
        const contextP = browser.contexts()[0] || await browser.newContext();
        const page = await contextP.newPage();
        
        // Navigate to test URL first (required before setting cookies)
        await page.goto(testUrl);
        console.log(`Navigated to ${testUrl}`);
        await page.waitForTimeout(2000);
        
        // Add test cookies
        await contextP.addCookies(testCookies);
        console.log(`Added ${testCookies.length} test cookies`);
        
        // Verify cookies were set
        const cookies = await contextP.cookies();
        const cookieDict: Record<string, string> = {};
        cookies.forEach((cookie: any) => {
            if (cookie.name) {
                cookieDict[cookie.name] = cookie.value || '';
            }
        });
        console.log(`Total cookies in first session: ${cookies.length}`);
        
        // Check our test cookies
        for (const testCookie of testCookies) {
            const cookieName = testCookie.name;
            if (cookieName in cookieDict) {
                console.log(`✓ Test cookie '${cookieName}' set successfully: ${cookieDict[cookieName]}`);
            } else {
                console.log(`✗ Test cookie '${cookieName}' not found`);
            }
        }
        
        await browser.close();
        console.log("First session browser operations completed");

        // Step 4: Delete first session with context synchronization
        console.log("Step 4: Deleting first session with context synchronization...");
        const deleteResult = await agentBay.delete(session1, true);  // syncContext = true
        
        if (!deleteResult.success) {
            console.log(`Failed to delete first session: ${deleteResult.errorMessage}`);
            return;
        }
            
        console.log(`First session deleted successfully (RequestID: ${deleteResult.requestId})`);
        
        // Wait for context sync to complete
        console.log("Waiting for context synchronization to complete...");
        await new Promise(resolve => setTimeout(resolve, 3000));

        // Step 5: Create second session with same Browser Context
        console.log("Step 5: Creating second session with same Browser Context...");
        const sessionResult2 = await agentBay.create(params);
        
        if (!sessionResult2.success || !sessionResult2.session) {
            console.log(`Failed to create second session: ${sessionResult2.errorMessage}`);
            return;
        }
            
        const session2 = sessionResult2.session;
        console.log(`Second session created with ID: ${session2.sessionId}`);

        // Step 6: Verify cookie persistence
        console.log("Step 6: Verifying cookie persistence in second session...");
        
        // Initialize browser in second session
        const initSuccess2 = await session2.browser.initializeAsync(new BrowserOption());
        if (!initSuccess2) {
            console.log("Failed to initialize browser in second session");
            return;
        }
            
        console.log("Second session browser initialized successfully");
        
        // Get endpoint URL for second session
        const endpointUrl2 = session2.browser.getEndpointUrl();
        if (!endpointUrl2) {
            console.log("Failed to get browser endpoint URL for second session");
            return;
        }
            
        console.log(`Second session browser endpoint URL: ${endpointUrl2}`);
        
        // Check cookies in second session
        const browser2 = await chromium.connectOverCDP(endpointUrl2);
        const context2 = browser2.contexts()[0] || await browser2.newContext();
        
        // Read cookies directly from context (without opening any page)
        const cookies2 = await context2.cookies();
        const cookieDict2: Record<string, string> = {};
        cookies2.forEach((cookie: any) => {
            if (cookie.name) {
                cookieDict2[cookie.name] = cookie.value || '';
            }
        });
        
        console.log(`Total cookies in second session: ${cookies2.length}`);
        
        // Check if our test cookies persisted
        const expectedCookieNames = new Set(["demo_cookie_1", "demo_cookie_2"]);
        const foundCookieNames = new Set(Object.keys(cookieDict2));
        
        console.log("Checking cookie persistence...");
        const missingCookies = [...expectedCookieNames].filter(name => !foundCookieNames.has(name));
        
        if (missingCookies.length > 0) {
            console.log(`✗ Missing test cookies: ${missingCookies.join(', ')}`);
            console.log("Cookie persistence test FAILED");
        } else {
            // Verify cookie values
            let allValuesMatch = true;
            for (const testCookie of testCookies) {
                const cookieName = testCookie.name;
                const expectedValue = testCookie.value;
                const actualValue = cookieDict2[cookieName] || "";
                
                if (expectedValue === actualValue) {
                    console.log(`✓ Cookie '${cookieName}' persisted correctly: ${actualValue}`);
                } else {
                    console.log(`✗ Cookie '${cookieName}' value mismatch. Expected: ${expectedValue}, Actual: ${actualValue}`);
                    allValuesMatch = false;
                }
            }
            
            if (allValuesMatch) {
                console.log("🎉 Cookie persistence test PASSED! All cookies persisted correctly across sessions.");
            } else {
                console.log("Cookie persistence test FAILED due to value mismatches");
            }
        }
        
        await browser2.close();
        console.log("Second session browser operations completed");

        // Step 7: Clean up second session
        console.log("Step 7: Cleaning up second session...");
        const deleteResult2 = await agentBay.delete(session2);
        
        if (deleteResult2.success) {
            console.log(`Second session deleted successfully (RequestID: ${deleteResult2.requestId})`);
        } else {
            console.log(`Failed to delete second session: ${deleteResult2.errorMessage}`);
        }

    } catch (error) {
        console.log(`Error during demo: ${error}`);
    } finally {
        // Clean up context
        try {
            const contextResult = await agentBay.context.get(contextName, false);
            if (contextResult.success && contextResult.context) {
                await agentBay.context.delete(contextResult.context);
                console.log(`Context '${contextName}' deleted`);
            }
        } catch (error) {
            console.log(`Warning: Failed to delete context: ${error}`);
        }
    }

    console.log("\nBrowser Context Cookie Persistence Demo completed!");
}

// Run the example
main().catch(console.error); 