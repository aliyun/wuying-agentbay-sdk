package com.aliyun.agentbay.test;

import com.aliyun.agentbay.AgentBay;
import com.aliyun.agentbay.browser.BrowserAgent;
import com.aliyun.agentbay.browser.BrowserOption;
import com.aliyun.agentbay.browser.ExtractOptions;
import com.aliyun.agentbay.exception.AgentBayException;
import com.aliyun.agentbay.model.SessionInfoResult;
import com.aliyun.agentbay.model.SessionResult;
import com.aliyun.agentbay.session.CreateSessionParams;
import com.aliyun.agentbay.session.Session;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.microsoft.playwright.*;
import org.junit.AfterClass;
import org.junit.BeforeClass;
import org.junit.Test;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.List;

import static org.junit.Assert.*;

/**
 * Test cases for Game2048Example functionality
 * Tests the SDK methods used in the Game2048 example including:
 * - AgentBay client initialization
 * - Session creation and management
 * - Browser initialization and control
 * - Browser agent data extraction
 */
public class TestGame2048Example {
    private static final Logger logger = LoggerFactory.getLogger(TestGame2048Example.class);
    private static AgentBay agentBay;
    private static Session session;
    private static String apiKey;

    public static class GameState {
        @JsonProperty("score")
        private Integer score;

        @JsonProperty("highestTile")
        private Integer highestTile;

        @JsonProperty("grid")
        private List<List<Integer>> grid;

        public Integer getScore() {
            return score;
        }

        public void setScore(Integer score) {
            this.score = score;
        }

        public Integer getHighestTile() {
            return highestTile;
        }

        public void setHighestTile(Integer highestTile) {
            this.highestTile = highestTile;
        }

        public List<List<Integer>> getGrid() {
            return grid;
        }

        public void setGrid(List<List<Integer>> grid) {
            this.grid = grid;
        }
    }

    @BeforeClass
    public static void setUp() throws AgentBayException {
        logger.info("=== Starting Game2048Example Test ===");
        apiKey = System.getenv("AGENTBAY_API_KEY");
        assertNotNull("AGENTBAY_API_KEY environment variable must be set", apiKey);
        assertFalse("AGENTBAY_API_KEY cannot be empty", apiKey.trim().isEmpty());
        
        // Initialize AgentBay client for each test
        agentBay = new AgentBay(apiKey);
        
        // Create session for tests that need it
        CreateSessionParams params = new CreateSessionParams();
        params.setImageId("browser_latest");
        SessionResult sessionResult = agentBay.create(params);
        
        if (sessionResult.isSuccess()) {
            session = sessionResult.getSession();
            logger.info("Session created with ID: {}", session.getSessionId());
        } else {
            fail("Failed to create session: " + sessionResult.getErrorMessage());
        }
    }

    @AfterClass
    public static void tearDown() {
        if (session != null) {
            try {
                logger.info("Cleaning up session: {}", session.getSessionId());
                // Note: Session cleanup is handled automatically by the SDK
            } catch (Exception e) {
                logger.error("Error in cleanup", e);
            }
        }
        logger.info("=== Game2048Example Test Completed ===");
    }

    @Test
    public void test01_AgentBayInitialization() {
        logger.info("Test 1: Testing AgentBay client initialization");
        
        assertNotNull("AgentBay client should not be null", agentBay);
        logger.info("✅ AgentBay client initialized successfully");
    }

    @Test
    public void test02_SessionCreation() {
        logger.info("Test 2: Testing session creation");
        
        assertNotNull("Session should not be null", session);
        assertNotNull("Session ID should not be null", session.getSessionId());
        assertFalse("Session ID should not be empty", session.getSessionId().isEmpty());
        
        logger.info("✅ Session created successfully with ID: {}", session.getSessionId());
    }

    @Test
    public void test03_SessionInfo() throws Exception {
        logger.info("Test 3: Testing session info retrieval");
        
        assertNotNull("Session must be created before testing info", session);
        
        SessionInfoResult result = session.info();
        
        assertNotNull("Session info result should not be null", result);
        assertTrue("Session info retrieval should succeed", result.isSuccess());
        assertNotNull("Session info should not be null", result.getSessionInfo());
        
        String desktopUrl = result.getSessionInfo().getResourceUrl();
        assertNotNull("Desktop URL should not be null", desktopUrl);
        assertFalse("Desktop URL should not be empty", desktopUrl.isEmpty());
        
        logger.info("✅ Session info retrieved successfully");
        logger.info("Session URL: {}", desktopUrl);
    }

    @Test
    public void test04_BrowserInitialization() {
        logger.info("Test 4: Testing browser initialization");
        
        assertNotNull("Session must be created before testing browser", session);
        assertNotNull("Browser object should not be null", session.getBrowser());
        
        BrowserOption browserOption = new BrowserOption();
        boolean initResult = session.getBrowser().initialize(browserOption);
        
        assertTrue("Browser initialization should succeed", initResult);
        logger.info("✅ Browser initialized successfully");
    }

    @Test
    public void test05_BrowserEndpointUrl() throws Exception {
        logger.info("Test 5: Testing browser endpoint URL retrieval");
        
        assertNotNull("Session must be created before testing endpoint URL", session);
        assertNotNull("Browser object should not be null", session.getBrowser());
        
        // Initialize browser first
        session.getBrowser().initialize(new BrowserOption());
        
        String endpointUrl = session.getBrowser().getEndpointUrl();
        
        assertNotNull("Endpoint URL should not be null", endpointUrl);
        assertFalse("Endpoint URL should not be empty", endpointUrl.isEmpty());
        assertTrue("Endpoint URL should be a WebSocket URL", 
                   endpointUrl.startsWith("ws://") || endpointUrl.startsWith("wss://"));
        
        logger.info("✅ Browser endpoint URL retrieved successfully");
        logger.info("Endpoint URL: {}", endpointUrl);
    }

    @Test
    public void test06_BrowserAgentAccess() {
        logger.info("Test 6: Testing browser agent access");
        
        assertNotNull("Session must be created before testing agent", session);
        assertNotNull("Browser object should not be null", session.getBrowser());
        
        // Initialize browser first
        session.getBrowser().initialize(new BrowserOption());
        
        BrowserAgent agent = session.getBrowser().getAgent();
        
        assertNotNull("Browser agent should not be null", agent);
        logger.info("✅ Browser agent accessed successfully");
    }

    @Test
    public void test07_BrowserAgentExtract() {
        logger.info("Test 7: Testing browser agent extract functionality");
        
        assertNotNull("Session must be created before testing extract", session);
        
        try {
            // Initialize browser first
            session.getBrowser().initialize(new BrowserOption());
            
            try (Playwright playwright = Playwright.create()) {
                String endpointUrl = session.getBrowser().getEndpointUrl();
                com.microsoft.playwright.Browser browser = playwright.chromium().connectOverCDP(endpointUrl);
                BrowserContext context = browser.contexts().get(0);
                Page page = context.newPage();
                BrowserAgent agent = session.getBrowser().getAgent();
                
                logger.info("Navigating to 2048 game...");
                page.navigate("https://ovolve.github.io/2048-AI/",
                    new Page.NavigateOptions()
                        .setWaitUntil(com.microsoft.playwright.options.WaitUntilState.DOMCONTENTLOADED)
                        .setTimeout(180000));
                Thread.sleep(1000);
                
                logger.info("Waiting for game grid to load...");
                page.waitForSelector(".grid-container", new Page.WaitForSelectorOptions().setTimeout(10000));
                
                // Wait a bit for initial tiles to appear
                Thread.sleep(1000);
                
                String instruction = "Extract the current game state:\n" +
                    "1. Score from the score counter\n" +
                    "2. All tile values and their positions in the 4x4 grid must be extracted. \n" +
                    "    Each tile's value and position can be obtained from the tile-position-x-y class, where x (1 to 4) is the column and y (1 to 4) is the row.\n" +
                    "    For example, tile-position-4-1 means the tile is in column 4, row 1.\n" +
                    "    The value of the tile is given by the number in the tile's class.\n" +
                    "    For example, <div class='tile tile-2 tile-position-1-4 tile-new'>2</div> means a tile with value 2 at column 1, row 4;\n" +
                    "    and <div class='tile tile-2 tile-position-4-1 tile-new'>2</div> means a tile with value 2 at column 4, row 1.\n" +
                    "    Empty spaces should be represented as 0 in the grid.\n" +
                    "    For instance, if the only tiles present are the two above, the grid should be:[[0, 0, 0, 2], [0, 0, 0, 0], [0, 0, 0, 0], [2, 0, 0, 0]]\n" +
                    "3. Highest tile value present";
                
                logger.info("Extracting game state using agent...");
                ExtractOptions<GameState> extractOptions = new ExtractOptions<>(instruction, GameState.class);
                extractOptions.setUseTextExtract(false);
                
                BrowserAgent.ExtractResultTuple<GameState> extractResult = agent.extract(page, extractOptions);
                
                assertNotNull("Extract result should not be null", extractResult);
                assertTrue("Extract operation should succeed", extractResult.isSuccess());
                
                GameState gameState = extractResult.getData();
                assertNotNull("Game state should not be null", gameState);
                assertNotNull("Grid should not be null", gameState.getGrid());
                assertEquals("Grid should have 4 rows", 4, gameState.getGrid().size());
                
                for (List<Integer> row : gameState.getGrid()) {
                    assertEquals("Each row should have 4 columns", 4, row.size());
                }
                
                assertNotNull("Score should not be null", gameState.getScore());
                assertTrue("Score should be non-negative", gameState.getScore() >= 0);
                
                assertNotNull("Highest tile should not be null", gameState.getHighestTile());
                assertTrue("Highest tile should be positive", gameState.getHighestTile() > 0);
                
                logger.info("✅ Browser agent extract functionality working correctly");
                logger.info("Extracted game state - Score: {}, Highest Tile: {}", 
                           gameState.getScore(), gameState.getHighestTile());
                logger.info("Grid: {}", gameState.getGrid());
                
                page.close();
                browser.close();
            }
        } catch (Exception e) {
            fail("Extract operation should not throw exception: " + e.getMessage());
        }
    }

    @Test
    public void test08_KeyboardInteraction() {
        logger.info("Test 8: Testing keyboard interaction");
        
        assertNotNull("Session must be created before testing keyboard", session);
        
        try {
            // Initialize browser first
            session.getBrowser().initialize(new BrowserOption());
            
            try (Playwright playwright = Playwright.create()) {
                String endpointUrl = session.getBrowser().getEndpointUrl();
                com.microsoft.playwright.Browser browser = playwright.chromium().connectOverCDP(endpointUrl);
                BrowserContext context = browser.contexts().get(0);
                Page page = context.newPage();
                
                logger.info("Navigating to 2048 game for keyboard test...");
                page.navigate("https://ovolve.github.io/2048-AI/",
                    new Page.NavigateOptions()
                        .setWaitUntil(com.microsoft.playwright.options.WaitUntilState.DOMCONTENTLOADED)
                        .setTimeout(180000));

                Thread.sleep(1000);
                
                page.waitForSelector(".grid-container", new Page.WaitForSelectorOptions().setTimeout(10000));
                Thread.sleep(1000);
                
                logger.info("Testing keyboard arrow key press...");
                page.keyboard().press("ArrowLeft");
                Thread.sleep(1000);
                
                page.keyboard().press("ArrowUp");
                Thread.sleep(1000);
                
                logger.info("✅ Keyboard interaction working correctly");
                
                page.close();
                browser.close();
            }
        } catch (Exception e) {
            fail("Keyboard interaction should not throw exception: " + e.getMessage());
        }
    }

    @Test
    public void test09_InvalidApiKey() {
        logger.info("Test 9: Testing error handling with invalid API key");
        
        try {
            AgentBay invalidClient = new AgentBay("invalid_api_key");
            CreateSessionParams params = new CreateSessionParams();
            params.setImageId("browser_latest");
            SessionResult result = invalidClient.create(params);
            
            assertFalse("Invalid API key should not create session successfully", result.isSuccess());
            assertNotNull("Error message should be present", result.getErrorMessage());
            
            logger.info("✅ Error handling for invalid API key working correctly");
        } catch (AgentBayException e) {
            logger.info("✅ AgentBayException thrown as expected: {}", e.getMessage());
            // This is expected behavior
        } catch (Exception e) {
            logger.info("✅ Exception thrown as expected: {}", e.getMessage());
            // This is also acceptable
        }
    }

    @Test
    public void test10_ExtractOptionsConfiguration() {
        logger.info("Test 10: Testing extract options configuration");
        
        String instruction = "Extract game state";
        ExtractOptions<GameState> extractOptions = new ExtractOptions<>(instruction, GameState.class);
        
        assertNotNull("Extract options should not be null", extractOptions);
        
        // Test setting useTextExtract
        extractOptions.setUseTextExtract(false);
        // Note: If there's no getter, we can't verify but we can ensure no exception is thrown
        
        extractOptions.setUseTextExtract(true);
        // Note: If there's no getter, we can't verify but we can ensure no exception is thrown
        
        logger.info("✅ Extract options configuration working correctly");
    }
}

