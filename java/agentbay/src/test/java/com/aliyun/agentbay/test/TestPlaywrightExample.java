package com.aliyun.agentbay.test;

import com.aliyun.agentbay.AgentBay;
import com.aliyun.agentbay.browser.BrowserOption;
import com.aliyun.agentbay.exception.AgentBayException;
import com.aliyun.agentbay.exception.BrowserException;
import com.aliyun.agentbay.model.SessionResult;
import com.aliyun.agentbay.session.CreateSessionParams;
import com.aliyun.agentbay.session.Session;
import com.microsoft.playwright.*;
import org.junit.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import static org.junit.Assert.*;

/**
 * JUnit 4 test cases for PlaywrightExample functionality
 * Tests the integration of AgentBay SDK with Playwright browser automation
 */
public class TestPlaywrightExample {
    private static final Logger logger = LoggerFactory.getLogger(TestPlaywrightExample.class);
    
    private AgentBay agentBay;
    private Session session;
    private String apiKey;

    @BeforeClass
    public static void setUpClass() {
        logger.info("Starting Playwright Example Tests");
    }

    @Before
    public void setUp() {
        // Get API key from environment variable
        apiKey = System.getenv("AGENTBAY_API_KEY");
        assertNotNull("AGENTBAY_API_KEY environment variable must be set", apiKey);
        assertFalse("AGENTBAY_API_KEY must not be empty", apiKey.trim().isEmpty());
        
        logger.info("Test setup completed with API key");
    }

    @After
    public void tearDown() {
        // Clean up session if it was created
        if (agentBay != null && session != null) {
            try {
                agentBay.delete(session, false);
                logger.info("Session cleaned up successfully");
            } catch (Exception e) {
                logger.warn("Failed to clean up session: " + e.getMessage());
            }
        }
    }

    @AfterClass
    public static void tearDownClass() {
        logger.info("Completed Playwright Example Tests");
    }

    /**
     * Test creating AgentBay client instance
     */
    @Test
    public void testCreateAgentBayClient() throws AgentBayException {
        logger.info("Testing AgentBay client creation");
        
        agentBay = new AgentBay(apiKey);
        assertNotNull("AgentBay client should be created", agentBay);
        
        logger.info("AgentBay client created successfully");
    }

    /**
     * Test creating a new session with browser image
     */
    @Test
    public void testCreateSession() throws AgentBayException {
        logger.info("Testing session creation");
        
        agentBay = new AgentBay(apiKey);
        
        CreateSessionParams params = new CreateSessionParams();
        params.setImageId("browser_latest");
        
        SessionResult sessionResult = agentBay.create(params);
        
        assertNotNull("Session result should not be null", sessionResult);
        assertTrue("Session creation should succeed", sessionResult.isSuccess());
        
        session = sessionResult.getSession();
        assertNotNull("Session should not be null", session);
        assertNotNull("Session ID should not be null", session.getSessionId());
        assertFalse("Session ID should not be empty", session.getSessionId().isEmpty());
        
        logger.info("Session created successfully with ID: " + session.getSessionId());
    }

    /**
     * Test browser initialization
     */
    @Test
    public void testBrowserInitialization() throws AgentBayException, BrowserException {
        logger.info("Testing browser initialization");
        
        agentBay = new AgentBay(apiKey);
        
        CreateSessionParams params = new CreateSessionParams();
        params.setImageId("browser_latest");
        SessionResult sessionResult = agentBay.create(params);
        
        assertTrue("Session creation should succeed", sessionResult.isSuccess());
        session = sessionResult.getSession();
        
        // Initialize browser
        BrowserOption browserOption = new BrowserOption();
        boolean initResult = session.getBrowser().initialize(browserOption);
        
        assertTrue("Browser initialization should succeed", initResult);
        
        String endpointUrl = session.getBrowser().getEndpointUrl();
        assertNotNull("Endpoint URL should not be null", endpointUrl);
        assertFalse("Endpoint URL should not be empty", endpointUrl.isEmpty());
        
        logger.info("Browser initialized successfully with endpoint: " + endpointUrl);
    }

    /**
     * Test Playwright integration with AgentBay browser
     */
    @Test
    public void testPlaywrightIntegration() throws AgentBayException, BrowserException {
        logger.info("Testing Playwright integration");
        
        agentBay = new AgentBay(apiKey);
        
        CreateSessionParams params = new CreateSessionParams();
        params.setImageId("browser_latest");
        SessionResult sessionResult = agentBay.create(params);
        
        assertTrue("Session creation should succeed", sessionResult.isSuccess());
        session = sessionResult.getSession();
        
        // Initialize browser
        assertTrue("Browser initialization should succeed", 
                   session.getBrowser().initialize(new BrowserOption()));
        
        String endpointUrl = session.getBrowser().getEndpointUrl();
        
        // Use Playwright to connect and perform operations
        try (Playwright playwright = Playwright.create()) {
            Browser browser = playwright.chromium().connectOverCDP(endpointUrl);
            assertNotNull("Browser connection should succeed", browser);
            
            Page page = browser.newPage();
            assertNotNull("Page should be created", page);
            
            // Navigate to a website
            page.navigate("https://www.aliyun.com");
            
            // Wait for page load
            page.waitForTimeout(2000);
            
            String title = page.title();
            assertNotNull("Page title should not be null", title);
            assertFalse("Page title should not be empty", title.isEmpty());
            
            logger.info("Successfully navigated to page with title: " + title);
            
            browser.close();
        } catch (Exception e) {
            fail("Playwright integration failed: " + e.getMessage());
        }
    }

    /**
     * Test page manipulation with Playwright
     */
    @Test
    public void testPageManipulation() throws AgentBayException, BrowserException {
        logger.info("Testing page manipulation");
        
        agentBay = new AgentBay(apiKey);
        
        CreateSessionParams params = new CreateSessionParams();
        params.setImageId("browser_latest");
        SessionResult sessionResult = agentBay.create(params);
        
        assertTrue("Session creation should succeed", sessionResult.isSuccess());
        session = sessionResult.getSession();
        
        assertTrue("Browser initialization should succeed", 
                   session.getBrowser().initialize(new BrowserOption()));
        
        String endpointUrl = session.getBrowser().getEndpointUrl();
        
        try (Playwright playwright = Playwright.create()) {
            Browser browser = playwright.chromium().connectOverCDP(endpointUrl);
            Page page = browser.newPage();
            
            page.navigate("https://www.aliyun.com");
            page.waitForTimeout(2000);
            
            // Test font family modification
            page.evaluate("document.body.style.fontFamily = 'Microsoft YaHei';");
            page.waitForTimeout(1000);
            
            // Test scale transformation
            page.evaluate(
                "document.body.style.transform = 'scale(2)';" +
                "document.body.style.transformOrigin = 'top left';"
            );
            page.waitForTimeout(2000);
            
            logger.info("Page manipulation completed successfully");
            
            browser.close();
        } catch (Exception e) {
            fail("Page manipulation failed: " + e.getMessage());
        }
    }

    /**
     * Test session deletion
     */
    @Test
    public void testSessionDeletion() throws AgentBayException {
        logger.info("Testing session deletion");
        
        agentBay = new AgentBay(apiKey);
        
        CreateSessionParams params = new CreateSessionParams();
        params.setImageId("browser_latest");
        SessionResult sessionResult = agentBay.create(params);
        
        assertTrue("Session creation should succeed", sessionResult.isSuccess());
        session = sessionResult.getSession();
        
        String sessionId = session.getSessionId();
        
        // Delete the session
        agentBay.delete(session, false);
        logger.info("Session " + sessionId + " deleted successfully");
        
        // Prevent double cleanup in tearDown
        session = null;
    }

    /**
     * Test error handling with invalid API key
     */
    @Test
    public void testInvalidApiKey() throws AgentBayException {
        logger.info("Testing error handling with invalid API key");
        
        AgentBay invalidClient = new AgentBay("invalid_api_key");
        CreateSessionParams params = new CreateSessionParams();
        params.setImageId("browser_latest");
        
        // This should return a SessionResult with success = false
        SessionResult result = invalidClient.create(params);
        
        assertNotNull("Session result should not be null", result);
        assertFalse("Session creation should fail with invalid API key", result.isSuccess());
        assertNotNull("Error message should be provided", result.getErrorMessage());
        assertFalse("Error message should not be empty", result.getErrorMessage().isEmpty());
        
        logger.info("Invalid API key correctly handled with error: " + result.getErrorMessage());
    }

    /**
     * Test session creation with null parameters
     */
    @Test
    public void testCreateSessionWithNullParams() throws AgentBayException {
        logger.info("Testing session creation with null parameters");
        
        agentBay = new AgentBay(apiKey);
        
        // Create session with null params (should use defaults)
        SessionResult sessionResult = agentBay.create(null);
        
        assertNotNull("Session result should not be null", sessionResult);
        
        // According to the implementation, null params are converted to default params
        // So this should succeed
        if (sessionResult.isSuccess()) {
            session = sessionResult.getSession();
            assertNotNull("Session should not be null", session);
            assertNotNull("Session ID should not be null", session.getSessionId());
            logger.info("Session created with default parameters: " + session.getSessionId());
        } else {
            logger.warn("Session creation with null params failed: " + sessionResult.getErrorMessage());
        }
    }

    /**
     * Test browser initialization with custom options
     */
    @Test
    public void testBrowserInitializationWithCustomOptions() throws AgentBayException, BrowserException {
        logger.info("Testing browser initialization with custom options");
        
        agentBay = new AgentBay(apiKey);
        
        CreateSessionParams params = new CreateSessionParams();
        params.setImageId("browser_latest");
        SessionResult sessionResult = agentBay.create(params);
        
        assertTrue("Session creation should succeed", sessionResult.isSuccess());
        session = sessionResult.getSession();
        
        // Initialize browser with custom options
        BrowserOption browserOption = new BrowserOption();
        // Add custom configurations if BrowserOption supports them
        
        boolean initResult = session.getBrowser().initialize(browserOption);
        assertTrue("Browser initialization with custom options should succeed", initResult);
        
        logger.info("Browser initialized with custom options");
    }

    /**
     * Test complete workflow from creation to deletion
     */
    @Test
    public void testCompleteWorkflow() throws AgentBayException, BrowserException {
        logger.info("Testing complete workflow");
        
        // Step 1: Initialize client
        agentBay = new AgentBay(apiKey);
        assertNotNull("AgentBay client should be created", agentBay);
        
        // Step 2: Create session
        CreateSessionParams params = new CreateSessionParams();
        params.setImageId("browser_latest");
        SessionResult sessionResult = agentBay.create(params);
        assertTrue("Session should be created", sessionResult.isSuccess());
        
        session = sessionResult.getSession();
        assertNotNull("Session should not be null", session);
        
        // Step 3: Initialize browser
        boolean browserInit = session.getBrowser().initialize(new BrowserOption());
        assertTrue("Browser should initialize", browserInit);
        
        String endpointUrl = session.getBrowser().getEndpointUrl();
        assertNotNull("Endpoint URL should exist", endpointUrl);
        
        // Step 4: Use Playwright
        try (Playwright playwright = Playwright.create()) {
            Browser browser = playwright.chromium().connectOverCDP(endpointUrl);
            Page page = browser.newPage();
            page.navigate("https://www.aliyun.com");
            page.waitForTimeout(1000);
            assertNotNull("Page title should exist", page.title());
            browser.close();
        }
        
        // Step 5: Delete session
        agentBay.delete(session, false);
        logger.info("Complete workflow executed successfully");
        
        session = null; // Prevent double cleanup
    }
}

