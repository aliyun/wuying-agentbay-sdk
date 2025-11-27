package com.aliyun.agentbay.test;

import com.aliyun.agentbay.AgentBay;
import com.aliyun.agentbay.browser.BrowserOption;
import com.aliyun.agentbay.context.Context;
import com.aliyun.agentbay.context.ContextResult;
import com.aliyun.agentbay.exception.AgentBayException;
import com.aliyun.agentbay.model.DeleteResult;
import com.aliyun.agentbay.model.SessionResult;
import com.aliyun.agentbay.session.CreateSessionParams;
import com.aliyun.agentbay.session.Session;
import com.microsoft.playwright.*;
import com.microsoft.playwright.options.Cookie;
import org.junit.*;

import java.util.*;

import static org.junit.Assert.*;

/**
 * Integration test for browser context functionality.
 * This test verifies that browser context (cookies, localStorage, etc.) can be persisted
 * across sessions using the same ContextId.
 */
public class TestBrowserContextIntegration {
    
    private static AgentBay agentBay;
    private static String contextName;
    private static Context context;
    
    @BeforeClass
    public static void setUpClass() throws AgentBayException {
        // Skip if no API key is available or in CI environment
        String apiKey = System.getenv("AGENTBAY_API_KEY");
        String ci = System.getenv("CI");
        if (apiKey == null || apiKey.trim().isEmpty() || "true".equals(ci)) {
            throw new IllegalStateException(
                "Skipping integration test: No API key available or running in CI"
            );
        }
        
        // Initialize AgentBay client
        agentBay = new AgentBay(apiKey);
        
        // Create a unique context name for this test
        contextName = "test-browser-context-" + System.currentTimeMillis();
        
        // Create a context
        ContextResult contextResult = agentBay.getContext().get(contextName, true);
        if (!contextResult.isSuccess() || contextResult.getContext() == null) {
            throw new IllegalStateException("Failed to create context");
        }
        
        context = contextResult.getContext();
        System.out.println("Created context: " + context.getName() + " (ID: " + context.getId() + ")");
    }
    
    @AfterClass
    public static void tearDownClass() {
        // Clean up context
        if (context != null && agentBay != null) {
            try {
                agentBay.getContext().delete(context);
                System.out.println("Context deleted: " + context.getId());
            } catch (Exception e) {
                System.out.println("Warning: Failed to delete context: " + e.getMessage());
            }
        }
    }
    
    /**
     * Test that manually set cookies persist across sessions with the same browser context.
     * 
     * This test verifies the complete browser context persistence workflow:
     * 1. Create a session with BrowserContext
     * 2. Initialize browser and add test cookies
     * 3. Delete session with context sync
     * 4. Create a new session with the same context
     * 5. Verify cookies are persisted
     */
    @Test
    public void testBrowserContextCookiePersistence() throws Exception {
        // Test data
        String testUrl = "https://www.aliyun.com";
        String testDomain = "aliyun.com";
        
        // Calculate expiration time (1 hour from now)
        double expirationTime = (System.currentTimeMillis() / 1000.0) + 3600;
        
        // Create test cookies using Playwright's Cookie builder
        List<Cookie> testCookies = new ArrayList<>();
        testCookies.add(new Cookie("myCookie", "cookieValue")
            .setDomain(testDomain)
            .setPath("/")
            .setExpires(expirationTime)
            .setHttpOnly(false)
            .setSecure(false));
        testCookies.add(new Cookie("test_cookie_2", "test_value_2")
            .setDomain(testDomain)
            .setPath("/")
            .setExpires(expirationTime)
            .setHttpOnly(false)
            .setSecure(false));
        
        // Step 1 & 2: Create ContextId and create session with BrowserContext
        System.out.println("Step 1-2: Creating session with browser context ID: " + context.getId());
        com.aliyun.agentbay.browser.BrowserContext browserContext = 
            new com.aliyun.agentbay.browser.BrowserContext(context.getId(), true);
        CreateSessionParams params = new CreateSessionParams();
        params.setImageId("browser_latest");
        params.setBrowserContext(browserContext);
        
        SessionResult sessionResult = agentBay.create(params);
        assertTrue("Failed to create first session", sessionResult.isSuccess());
        assertNotNull("Session should not be null", sessionResult.getSession());
        
        Session session1 = sessionResult.getSession();
        System.out.println("First session created with ID: " + session1.getSessionId());
        
        // Step 3: Get browser object through initialize and get_endpoint_url
        System.out.println("Step 3: Initializing browser and getting browser object...");
        
        // Initialize browser
        boolean initSuccess = session1.getBrowser().initialize(new BrowserOption());
        assertTrue("Failed to initialize browser", initSuccess);
        System.out.println("Browser initialized successfully");
        
        // Get endpoint URL
        String endpointUrl = session1.getBrowser().getEndpointUrl();
        assertNotNull("Endpoint URL should not be null", endpointUrl);
        System.out.println("Browser endpoint URL: " + endpointUrl);
        
        // Step 4: Connect with playwright, open aliyun.com and then add test cookies
        System.out.println("Step 4: Opening aliyun.com and then adding test cookies...");
        
        try (Playwright playwright = Playwright.create()) {
            Browser browser = playwright.chromium().connectOverCDP(endpointUrl);
            assertNotNull("Failed to connect to browser", browser);
            
            // Create CDP session for proper browser control
            CDPSession cdpSession = browser.newBrowserCDPSession();
            
            com.microsoft.playwright.BrowserContext pwContext = browser.contexts().isEmpty() 
                ? browser.newContext() 
                : browser.contexts().get(0);
            Page page = pwContext.newPage();
            
            // Navigate to test URL first
            page.navigate(testUrl);
            System.out.println("Navigated to " + testUrl);
            
            // Wait a bit for the page to load
            page.waitForTimeout(3000);
            
            // Add test cookies after navigating to the page
            pwContext.addCookies(testCookies);
            System.out.println("Added " + testCookies.size() + " test cookies after navigating to " + testUrl);
            
            // Read cookies to verify they were set correctly
            List<Cookie> cookies = pwContext.cookies();
            Map<String, String> cookieMap = new HashMap<>();
            for (Cookie cookie : cookies) {
                cookieMap.put(cookie.name, cookie.value);
            }
            
            System.out.println("Cookies found in first session: " + cookieMap.keySet());
            System.out.println("Total cookies count: " + cookies.size());
            
            // Close the browser using CDP session (same as Python version)
            cdpSession.send("Browser.close");
            System.out.println("First session browser operations completed");
            
            // Wait for browser to save cookies to file
            System.out.println("Waiting for browser to save cookies to file...");
            Thread.sleep(2000);
            System.out.println("Wait completed");
        }
        
        // Step 5: Release session with syncContext=true
        System.out.println("Step 5: Releasing first session with syncContext=true...");
        DeleteResult deleteResult = agentBay.delete(session1, true);
        assertTrue("Failed to delete first session", deleteResult.isSuccess());
        System.out.println("First session deleted successfully (RequestID: " + deleteResult.getRequestId() + ")");
        
        // Wait for context sync to complete
        Thread.sleep(3000);
        
        // Step 6: Create second session with same ContextId
        System.out.println("Step 6: Creating second session with same context ID: " + context.getId());
        SessionResult sessionResult2 = agentBay.create(params);
        assertTrue("Failed to create second session", sessionResult2.isSuccess());
        assertNotNull("Second session should not be null", sessionResult2.getSession());
        
        Session session2 = sessionResult2.getSession();
        System.out.println("Second session created with ID: " + session2.getSessionId());
        
        // Step 7: Get browser object and check if test cookies exist without opening any page
        System.out.println("Step 7: Getting browser object and checking test cookie persistence without opening any page...");
        
        // Initialize browser
        boolean initSuccess2 = session2.getBrowser().initialize(new BrowserOption());
        assertTrue("Failed to initialize browser in second session", initSuccess2);
        System.out.println("Second session browser initialized successfully");
        
        // Get endpoint URL
        String endpointUrl2 = session2.getBrowser().getEndpointUrl();
        assertNotNull("Endpoint URL should not be null", endpointUrl2);
        System.out.println("Second session browser endpoint URL: " + endpointUrl2);
        
        // Connect with playwright and read cookies directly from context without opening any page
        try (Playwright playwright = Playwright.create()) {
            Browser browser = playwright.chromium().connectOverCDP(endpointUrl2);
            assertNotNull("Failed to connect to browser in second session", browser);
            
            com.microsoft.playwright.BrowserContext pwContext = browser.contexts().isEmpty() 
                ? browser.newContext() 
                : browser.contexts().get(0);
            
            // Read cookies directly from context without opening any page
            List<Cookie> cookies = pwContext.cookies();
            Map<String, String> cookieMap = new HashMap<>();
            for (Cookie cookie : cookies) {
                cookieMap.put(cookie.name, cookie.value);
            }
            
            System.out.println("Cookies found in second session (without opening page): " + cookieMap.keySet());
            System.out.println("Total cookies count in second session: " + cookies.size());
            
            // Check if our test cookies exist in the second session
            Set<String> expectedCookieNames = new HashSet<>(Arrays.asList("myCookie", "test_cookie_2"));
            Set<String> foundCookieNames = cookieMap.keySet();
            
            System.out.println("Expected test cookies: " + expectedCookieNames);
            System.out.println("Found cookies: " + foundCookieNames);
            
            // Check if all expected test cookies are present
            Set<String> missingCookies = new HashSet<>(expectedCookieNames);
            missingCookies.removeAll(foundCookieNames);
            
            if (!missingCookies.isEmpty()) {
                fail("Missing expected test cookies in second session: " + missingCookies);
            }
            
            // Check if test cookie values match what we set
            Map<String, String> expectedValues = new HashMap<>();
            expectedValues.put("myCookie", "cookieValue");
            expectedValues.put("test_cookie_2", "test_value_2");
            
            for (String cookieName : expectedCookieNames) {
                if (cookieMap.containsKey(cookieName)) {
                    String expectedValue = expectedValues.get(cookieName);
                    String actualValue = cookieMap.get(cookieName);
                    assertEquals(
                        "Test cookie '" + cookieName + "' value should match. Expected: " + 
                        expectedValue + ", Actual: " + actualValue,
                        expectedValue,
                        actualValue
                    );
                    System.out.println("✓ Test cookie '" + cookieName + "' value matches: " + actualValue);
                }
            }
            
            System.out.println("SUCCESS: All " + expectedCookieNames.size() + " test cookies persisted correctly!");
            System.out.println("Test cookies found: " + expectedCookieNames);
            
            // Close context and browser
            pwContext.close();
            System.out.println("Second session browser operations completed");
        }
        
        // Clean up second session
        DeleteResult deleteResult2 = agentBay.delete(session2, false);
        assertTrue("Failed to delete second session", deleteResult2.isSuccess());
        System.out.println("Second session deleted successfully");
        
        System.out.println("Browser context manual cookie persistence test completed successfully!");
    }
    
    
    /**
     * Test that browser context can be created with minimal configuration
     */
    @Test
    public void testBrowserContextMinimalConfiguration() throws AgentBayException {
        System.out.println("Testing minimal browser context configuration...");
        
        // Create browser context with minimal config
        com.aliyun.agentbay.browser.BrowserContext browserContext = 
            new com.aliyun.agentbay.browser.BrowserContext(context.getId());
        
        // Verify default values
        assertEquals(context.getId(), browserContext.getContextId());
        assertTrue("Default auto_upload should be true", browserContext.isAutoUpload());
        
        // Create session with this context
        CreateSessionParams params = new CreateSessionParams();
        params.setImageId("browser_latest");
        params.setBrowserContext(browserContext);
        
        SessionResult sessionResult = agentBay.create(params);
        assertTrue("Failed to create session", sessionResult.isSuccess());
        assertNotNull("Session should not be null", sessionResult.getSession());
        
        Session session = sessionResult.getSession();
        System.out.println("Session created with minimal config: " + session.getSessionId());
        
        // Clean up
        DeleteResult deleteResult = agentBay.delete(session, false);
        assertTrue("Failed to delete session", deleteResult.isSuccess());
        System.out.println("Minimal configuration test completed successfully!");
    }
    
    /**
     * Test that browser context with auto_upload=false works correctly
     */
    @Test
    public void testBrowserContextNoAutoUpload() throws AgentBayException {
        System.out.println("Testing browser context with auto_upload=false...");
        
        // Create browser context with auto_upload=false
        com.aliyun.agentbay.browser.BrowserContext browserContext = 
            new com.aliyun.agentbay.browser.BrowserContext(context.getId(), false);
        
        // Verify configuration
        assertEquals(context.getId(), browserContext.getContextId());
        assertFalse("auto_upload should be false", browserContext.isAutoUpload());
        
        // Create session with this context
        CreateSessionParams params = new CreateSessionParams();
        params.setImageId("browser_latest");
        params.setBrowserContext(browserContext);
        
        SessionResult sessionResult = agentBay.create(params);
        assertTrue("Failed to create session", sessionResult.isSuccess());
        assertNotNull("Session should not be null", sessionResult.getSession());
        
        Session session = sessionResult.getSession();
        System.out.println("Session created with auto_upload=false: " + session.getSessionId());
        
        // Clean up
        DeleteResult deleteResult = agentBay.delete(session, false);
        assertTrue("Failed to delete session", deleteResult.isSuccess());
        System.out.println("No auto-upload test completed successfully!");
    }
}

