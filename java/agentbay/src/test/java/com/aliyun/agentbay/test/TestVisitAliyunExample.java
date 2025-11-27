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
 * JUnit 4 test cases for VisitAliyunExample functionality
 * Tests the integration of AgentBay SDK with Playwright to visit aliyun.com
 */
public class TestVisitAliyunExample {
    private static final Logger logger = LoggerFactory.getLogger(TestVisitAliyunExample.class);
    
    private AgentBay agentBay;
    private Session session;
    private String apiKey;

    @BeforeClass
    public static void setUpClass() {
        logger.info("Starting Visit Aliyun Example Tests");
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
                logger.error("Failed to clean up session", e);
            }
        }
    }

    @AfterClass
    public static void tearDownClass() {
        logger.info("Visit Aliyun Example Tests completed");
    }

    /**
     * Test successful AgentBay client initialization
     */
    @Test
    public void testAgentBayInitialization() throws AgentBayException {
        logger.info("Testing AgentBay initialization");
        agentBay = new AgentBay(apiKey);
        assertNotNull("AgentBay instance should not be null", agentBay);
        logger.info("AgentBay initialized successfully");
    }

    /**
     * Test successful session creation with browser_latest image
     */
    @Test
    public void testSessionCreation() throws AgentBayException {
        logger.info("Testing session creation");
        
        agentBay = new AgentBay(apiKey);
        
        CreateSessionParams params = new CreateSessionParams();
        params.setImageId("browser_latest");
        
        SessionResult sessionResult = agentBay.create(params);
        
        assertTrue("Session creation should be successful", sessionResult.isSuccess());
        assertNotNull("Session should not be null", sessionResult.getSession());
        
        session = sessionResult.getSession();
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
        assertTrue("Session creation should be successful", sessionResult.isSuccess());
        
        session = sessionResult.getSession();
        
        boolean browserInitialized = session.getBrowser().initialize(new BrowserOption());
        assertTrue("Browser should be initialized successfully", browserInitialized);
        
        String endpointUrl = session.getBrowser().getEndpointUrl();
        assertNotNull("Endpoint URL should not be null", endpointUrl);
        assertFalse("Endpoint URL should not be empty", endpointUrl.isEmpty());
//        assertTrue("Endpoint URL should start with ws://", endpointUrl.startsWith("ws://"));
        
        logger.info("Browser initialized successfully with endpoint: " + endpointUrl);
    }

    /**
     * Test visiting aliyun.com using Playwright
     */
    @Test
    public void testVisitAliyun() throws AgentBayException, BrowserException {
        logger.info("Testing visit to aliyun.com");
        
        agentBay = new AgentBay(apiKey);
        
        CreateSessionParams params = new CreateSessionParams();
        params.setImageId("browser_latest");
        
        SessionResult sessionResult = agentBay.create(params);
        assertTrue("Session creation should be successful", sessionResult.isSuccess());
        
        session = sessionResult.getSession();
        
        boolean browserInitialized = session.getBrowser().initialize(new BrowserOption());
        assertTrue("Browser should be initialized successfully", browserInitialized);
        
        String endpointUrl = session.getBrowser().getEndpointUrl();
        
        try (Playwright playwright = Playwright.create()) {
            Browser browser = playwright.chromium().connectOverCDP(endpointUrl);
            assertNotNull("Browser should not be null", browser);
            
            BrowserContext context = browser.contexts().get(0);
            assertNotNull("Browser context should not be null", context);
            
            Page page = context.newPage();
            assertNotNull("Page should not be null", page);
            
            page.navigate("https://www.aliyun.com",
                new Page.NavigateOptions()
                    .setWaitUntil(com.microsoft.playwright.options.WaitUntilState.DOMCONTENTLOADED)
                    .setTimeout(60000));
            
            String pageTitle = page.title();
            assertNotNull("Page title should not be null", pageTitle);
            assertFalse("Page title should not be empty", pageTitle.isEmpty());
            
            logger.info("Page title: " + pageTitle);
            
            page.waitForTimeout(5000);
            
            browser.close();
            logger.info("Successfully visited aliyun.com");
        }
    }

    /**
     * Test page manipulation with font family change
     */
    @Test
    public void testPageFontManipulation() throws AgentBayException, BrowserException {
        logger.info("Testing page font manipulation");
        
        agentBay = new AgentBay(apiKey);
        
        CreateSessionParams params = new CreateSessionParams();
        params.setImageId("browser_latest");
        
        SessionResult sessionResult = agentBay.create(params);
        assertTrue("Session creation should be successful", sessionResult.isSuccess());
        
        session = sessionResult.getSession();
        
        boolean browserInitialized = session.getBrowser().initialize(new BrowserOption());
        assertTrue("Browser should be initialized successfully", browserInitialized);
        
        String endpointUrl = session.getBrowser().getEndpointUrl();
        
        try (Playwright playwright = Playwright.create()) {
            Browser browser = playwright.chromium().connectOverCDP(endpointUrl);
            BrowserContext context = browser.contexts().get(0);
            Page page = context.newPage();
            
            page.navigate("https://www.aliyun.com",
                new Page.NavigateOptions()
                    .setWaitUntil(com.microsoft.playwright.options.WaitUntilState.DOMCONTENTLOADED)
                    .setTimeout(60000));
            page.waitForTimeout(5000);
            
            // Change font family
            Object result = page.evaluate("document.body.style.fontFamily = 'Microsoft YaHei';");
            logger.info("Font family changed successfully");
            
            page.waitForTimeout(5000);
            
            browser.close();
            logger.info("Page font manipulation test completed");
        }
    }

    /**
     * Test page transformation with scaling
     */
    @Test
    public void testPageTransformation() throws AgentBayException, BrowserException {
        logger.info("Testing page transformation");
        
        agentBay = new AgentBay(apiKey);
        
        CreateSessionParams params = new CreateSessionParams();
        params.setImageId("browser_latest");
        
        SessionResult sessionResult = agentBay.create(params);
        assertTrue("Session creation should be successful", sessionResult.isSuccess());
        
        session = sessionResult.getSession();
        
        boolean browserInitialized = session.getBrowser().initialize(new BrowserOption());
        assertTrue("Browser should be initialized successfully", browserInitialized);
        
        String endpointUrl = session.getBrowser().getEndpointUrl();
        
        try (Playwright playwright = Playwright.create()) {
            Browser browser = playwright.chromium().connectOverCDP(endpointUrl);
            BrowserContext context = browser.contexts().get(0);
            Page page = context.newPage();
            
            page.navigate("https://www.aliyun.com",
                new Page.NavigateOptions()
                    .setWaitUntil(com.microsoft.playwright.options.WaitUntilState.DOMCONTENTLOADED)
                    .setTimeout(60000));
            page.waitForTimeout(5000);
            
            // Change font family
            page.evaluate("document.body.style.fontFamily = 'Microsoft YaHei';");
            page.waitForTimeout(5000);
            
            // Apply transformation
            page.evaluate(
                "document.body.style.transform = 'scale(2)';" +
                "document.body.style.transformOrigin = 'top left';"
            );
            
            logger.info("Page transformation applied successfully");
            
            page.waitForTimeout(10000);
            
            browser.close();
            logger.info("Page transformation test completed");
        }
    }

    /**
     * Test complete workflow from session creation to deletion
     */
    @Test
    public void testCompleteWorkflow() throws AgentBayException, BrowserException {
        logger.info("Testing complete workflow");
        
        agentBay = new AgentBay(apiKey);
        assertNotNull("AgentBay instance should not be null", agentBay);
        
        CreateSessionParams params = new CreateSessionParams();
        params.setImageId("browser_latest");
        
        SessionResult sessionResult = agentBay.create(params);
        assertTrue("Session creation should be successful", sessionResult.isSuccess());
        
        session = sessionResult.getSession();
        String sessionId = session.getSessionId();
        assertNotNull("Session ID should not be null", sessionId);
        logger.info("Session created with ID: " + sessionId);
        
        boolean browserInitialized = session.getBrowser().initialize(new BrowserOption());
        assertTrue("Browser should be initialized successfully", browserInitialized);
        
        String endpointUrl = session.getBrowser().getEndpointUrl();
        assertNotNull("Endpoint URL should not be null", endpointUrl);
        logger.info("Endpoint URL: " + endpointUrl);
        
        try (Playwright playwright = Playwright.create()) {
            Browser browser = playwright.chromium().connectOverCDP(endpointUrl);
            BrowserContext context = browser.contexts().get(0);
            Page page = context.newPage();
            
            page.navigate("https://www.aliyun.com",
                new Page.NavigateOptions()
                    .setWaitUntil(com.microsoft.playwright.options.WaitUntilState.DOMCONTENTLOADED)
                    .setTimeout(60000));
            String pageTitle = page.title();
            logger.info("Page title: " + pageTitle);
            
            page.waitForTimeout(5000);
            
            page.evaluate("document.body.style.fontFamily = 'Microsoft YaHei';");
            page.waitForTimeout(5000);
            
            page.evaluate(
                "document.body.style.transform = 'scale(2)';" +
                "document.body.style.transformOrigin = 'top left';"
            );
            
            page.waitForTimeout(10000);
            browser.close();
        }
        
        agentBay.delete(session, false);
        logger.info("Session deleted successfully");
        
        // Prevent duplicate cleanup in tearDown
        session = null;
        
        logger.info("Complete workflow test finished successfully");
    }

    /**
     * Test session creation failure with invalid session result
     */
    @Test
    public void testSessionCreationFailureHandling() throws AgentBayException {
        logger.info("Testing session creation failure handling");
        
        agentBay = new AgentBay(apiKey);
        
        CreateSessionParams params = new CreateSessionParams();
        params.setImageId("browser_latest");
        
        SessionResult sessionResult = agentBay.create(params);
        
        if (!sessionResult.isSuccess()) {
            assertNotNull("Error message should be provided", sessionResult.getErrorMessage());
            assertFalse("Error message should not be empty", sessionResult.getErrorMessage().isEmpty());
            logger.info("Session creation failed as expected: " + sessionResult.getErrorMessage());
        } else {
            session = sessionResult.getSession();
            logger.info("Session created successfully");
        }
    }

    /**
     * Test browser initialization failure handling
     */
    @Test
    public void testBrowserInitializationFailureHandling() throws AgentBayException, BrowserException {
        logger.info("Testing browser initialization failure handling");
        
        agentBay = new AgentBay(apiKey);
        
        CreateSessionParams params = new CreateSessionParams();
        params.setImageId("browser_latest");
        
        SessionResult sessionResult = agentBay.create(params);
        assertTrue("Session creation should be successful", sessionResult.isSuccess());
        
        session = sessionResult.getSession();
        
        boolean browserInitialized = session.getBrowser().initialize(new BrowserOption());
        
        if (!browserInitialized) {
            logger.warn("Browser initialization failed");
        } else {
            logger.info("Browser initialized successfully");
        }
    }
}

