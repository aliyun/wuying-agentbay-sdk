package com.aliyun.agentbay.test;

import com.aliyun.agentbay.AgentBay;
import com.aliyun.agentbay.browser.*;
import com.aliyun.agentbay.exception.AgentBayException;
import com.aliyun.agentbay.model.SessionResult;
import com.aliyun.agentbay.session.CreateSessionParams;
import com.aliyun.agentbay.session.Session;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.microsoft.playwright.Browser;
import com.microsoft.playwright.Page;
import com.microsoft.playwright.Playwright;
import org.junit.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.List;

import static org.junit.Assert.*;

/**
 * Test cases for BrowserAgent async methods (actAsync and extractAsync)
 * Tests the async variants that use page_use_act_async and page_use_extract_async
 */
public class TestBrowserAgentAsync {
    private static final Logger logger = LoggerFactory.getLogger(TestBrowserAgentAsync.class);
    private static AgentBay agentBay;
    private static Session session;
    private static String apiKey;

    /**
     * Simple product data model for testing extraction
     */
    public static class ProductInfo {
        @JsonProperty("title")
        private String title;

        @JsonProperty("price")
        private String price;

        @JsonProperty("description")
        private String description;

        public String getTitle() {
            return title;
        }

        public void setTitle(String title) {
            this.title = title;
        }

        public String getPrice() {
            return price;
        }

        public void setPrice(String price) {
            this.price = price;
        }

        public String getDescription() {
            return description;
        }

        public void setDescription(String description) {
            this.description = description;
        }
    }

    /**
     * Game state model for 2048 game
     */
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
        logger.info("=== Starting BrowserAgent Async Test ===");
        apiKey = System.getenv("AGENTBAY_API_KEY");
        assertNotNull("AGENTBAY_API_KEY environment variable must be set", apiKey);
        assertFalse("AGENTBAY_API_KEY cannot be empty", apiKey.trim().isEmpty());

        agentBay = new AgentBay(apiKey);

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
            } catch (Exception e) {
                logger.error("Error in cleanup", e);
            }
        }
        logger.info("=== BrowserAgent Async Test Completed ===");
    }

    @Test
    public void test01_ActAsyncBasicNavigation() {
        logger.info("Test 1: Testing actAsync with basic navigation");

        assertNotNull("Session must be created", session);

        try {
            session.getBrowser().initialize(new BrowserOption());

            try (Playwright playwright = Playwright.create()) {
                String endpointUrl = session.getBrowser().getEndpointUrl();
                Browser browser = playwright.chromium().connectOverCDP(endpointUrl);
                com.microsoft.playwright.BrowserContext context = browser.contexts().get(0);
                Page page = context.newPage();
                BrowserAgent agent = session.getBrowser().getAgent();

                logger.info("Testing async navigation...");
                ActOptions options = new ActOptions("goto('https://www.baidu.com')");
                ActResult result = agent.actAsync(options, page);

                assertNotNull("ActResult should not be null", result);
                assertTrue("Navigation should succeed", result.isSuccess());
                logger.info("✅ Async navigation completed: {}", result.getMessage());

                page.close();
                browser.close();
            }
        } catch (Exception e) {
            fail("Async act navigation should not throw exception: " + e.getMessage());
        }
    }

    @Test
    public void test02_ActAsyncClickOperation() {
        logger.info("Test 2: Testing actAsync with click operation");

        assertNotNull("Session must be created", session);

        try {
            session.getBrowser().initialize(new BrowserOption());

            try (Playwright playwright = Playwright.create()) {
                String endpointUrl = session.getBrowser().getEndpointUrl();
                Browser browser = playwright.chromium().connectOverCDP(endpointUrl);
                com.microsoft.playwright.BrowserContext context = browser.contexts().get(0);
                Page page = context.newPage();
                BrowserAgent agent = session.getBrowser().getAgent();

                logger.info("Navigating to test page...");
                page.navigate("https://example.com",
                    new Page.NavigateOptions()
                        .setWaitUntil(com.microsoft.playwright.options.WaitUntilState.DOMCONTENTLOADED)
                        .setTimeout(60000));
                Thread.sleep(1000);

                logger.info("Testing async click operation...");
                ActOptions options = new ActOptions("click('a')");
                ActResult result = agent.actAsync(options, page);

                assertNotNull("ActResult should not be null", result);
                logger.info("Async click result: success={}, message={}",
                           result.isSuccess(), result.getMessage());

                page.close();
                browser.close();
            }
        } catch (Exception e) {
            logger.warn("Click operation may fail if element not found: {}", e.getMessage());
        }
    }

    @Test
    public void test03_ExtractAsyncGameState() {
        logger.info("Test 3: Testing extractAsync with game state extraction");

        assertNotNull("Session must be created", session);

        try {
            session.getBrowser().initialize(new BrowserOption());

            try (Playwright playwright = Playwright.create()) {
                String endpointUrl = session.getBrowser().getEndpointUrl();
                Browser browser = playwright.chromium().connectOverCDP(endpointUrl);
                com.microsoft.playwright.BrowserContext context = browser.contexts().get(0);
                Page page = context.newPage();
                BrowserAgent agent = session.getBrowser().getAgent();

                logger.info("Navigating to 2048 game...");
                page.navigate("https://ovolve.github.io/2048-AI/",
                    new Page.NavigateOptions()
                        .setWaitUntil(com.microsoft.playwright.options.WaitUntilState.DOMCONTENTLOADED)
                        .setTimeout(180000));
                Thread.sleep(2000);

                logger.info("Waiting for game grid to load...");
                page.waitForSelector(".grid-container",
                    new Page.WaitForSelectorOptions().setTimeout(10000));
                Thread.sleep(1000);

                String instruction = "Extract the current game state:\n" +
                    "1. Score from the score counter\n" +
                    "2. All tile values and their positions in the 4x4 grid\n" +
                    "3. Highest tile value present";

                logger.info("Extracting game state using async method...");
                ExtractOptions<GameState> extractOptions = new ExtractOptions<>(instruction, GameState.class);
                extractOptions.setUseTextExtract(false);

                BrowserAgent.ExtractResultTuple<GameState> extractResult =
                    agent.extractAsync(extractOptions, page);

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

                logger.info("✅ Async extract completed successfully");
                logger.info("Extracted game state - Score: {}, Highest Tile: {}",
                           gameState.getScore(), gameState.getHighestTile());
                logger.info("Grid: {}", gameState.getGrid());

                page.close();
                browser.close();
            }
        } catch (Exception e) {
            fail("Async extract operation should not throw exception: " + e.getMessage());
        }
    }

    @Test
    public void test04_ExtractAsyncProductInfo() {
        logger.info("Test 4: Testing extractAsync with product information extraction");

        assertNotNull("Session must be created", session);

        try {
            session.getBrowser().initialize(new BrowserOption());

            try (Playwright playwright = Playwright.create()) {
                String endpointUrl = session.getBrowser().getEndpointUrl();
                Browser browser = playwright.chromium().connectOverCDP(endpointUrl);
                com.microsoft.playwright.BrowserContext context = browser.contexts().get(0);
                Page page = context.newPage();
                BrowserAgent agent = session.getBrowser().getAgent();

                logger.info("Navigating to test page...");
                page.navigate("https://example.com",
                    new Page.NavigateOptions()
                        .setWaitUntil(com.microsoft.playwright.options.WaitUntilState.DOMCONTENTLOADED)
                        .setTimeout(60000));
                Thread.sleep(1000);

                String instruction = "Extract information from the page:\n" +
                    "1. Page title as 'title'\n" +
                    "2. Any price information as 'price' (use 'N/A' if not found)\n" +
                    "3. Main content description as 'description'";

                logger.info("Extracting page info using async method...");
                ExtractOptions<ProductInfo> extractOptions =
                    new ExtractOptions<>(instruction, ProductInfo.class);
                extractOptions.setUseTextExtract(true);

                BrowserAgent.ExtractResultTuple<ProductInfo> extractResult =
                    agent.extractAsync(extractOptions, page);

                assertNotNull("Extract result should not be null", extractResult);
                assertTrue("Extract operation should succeed", extractResult.isSuccess());

                ProductInfo info = extractResult.getData();
                assertNotNull("Product info should not be null", info);
                assertNotNull("Title should not be null", info.getTitle());

                logger.info("✅ Async product extraction completed successfully");
                logger.info("Extracted info - Title: {}, Price: {}, Description: {}",
                           info.getTitle(), info.getPrice(), info.getDescription());

                page.close();
                browser.close();
            }
        } catch (Exception e) {
            fail("Async extract operation should not throw exception: " + e.getMessage());
        }
    }

    @Test
    public void test05_ActAsyncWithObserveResult() {
        logger.info("Test 5: Testing actAsync with ObserveResult input");

        assertNotNull("Session must be created", session);

        try {
            session.getBrowser().initialize(new BrowserOption());

            try (Playwright playwright = Playwright.create()) {
                String endpointUrl = session.getBrowser().getEndpointUrl();
                Browser browser = playwright.chromium().connectOverCDP(endpointUrl);
                com.microsoft.playwright.BrowserContext context = browser.contexts().get(0);
                Page page = context.newPage();
                BrowserAgent agent = session.getBrowser().getAgent();

                logger.info("Navigating to test page...");
                page.navigate("https://example.com",
                    new Page.NavigateOptions()
                        .setWaitUntil(com.microsoft.playwright.options.WaitUntilState.DOMCONTENTLOADED)
                        .setTimeout(60000));
                Thread.sleep(1000);

                logger.info("First observe elements on the page...");
                ObserveOptions observeOptions = new ObserveOptions("Find all links on the page");
                BrowserAgent.ObserveResultTuple observeResult = agent.observe(page, observeOptions);

                if (observeResult.isSuccess() && !observeResult.getResults().isEmpty()) {
                    ObserveResult firstResult = observeResult.getResults().get(0);

                    logger.info("Testing actAsync with observed element...");
                    ActResult actResult = agent.actAsync(firstResult, page);

                    assertNotNull("ActResult should not be null", actResult);
                    logger.info("Async act with ObserveResult: success={}, message={}",
                               actResult.isSuccess(), actResult.getMessage());
                } else {
                    logger.warn("No elements observed, skipping actAsync test");
                }

                page.close();
                browser.close();
            }
        } catch (Exception e) {
            logger.warn("Act with ObserveResult may fail: {}", e.getMessage());
        }
    }

    @Test
    public void test06_ExtractAsyncWithCustomOptions() {
        logger.info("Test 6: Testing extractAsync with custom extraction options");

        assertNotNull("Session must be created", session);

        try {
            session.getBrowser().initialize(new BrowserOption());

            try (Playwright playwright = Playwright.create()) {
                String endpointUrl = session.getBrowser().getEndpointUrl();
                Browser browser = playwright.chromium().connectOverCDP(endpointUrl);
                com.microsoft.playwright.BrowserContext context = browser.contexts().get(0);
                Page page = context.newPage();
                BrowserAgent agent = session.getBrowser().getAgent();

                logger.info("Navigating to test page...");
                page.navigate("https://example.com",
                    new Page.NavigateOptions()
                        .setWaitUntil(com.microsoft.playwright.options.WaitUntilState.DOMCONTENTLOADED)
                        .setTimeout(60000));
                Thread.sleep(1000);

                String instruction = "Extract page title and main heading";
                ExtractOptions<ProductInfo> extractOptions =
                    new ExtractOptions<>(instruction, ProductInfo.class);
                extractOptions.setUseTextExtract(true);
                extractOptions.setUseVision(false);
                extractOptions.setSelector("body");
                extractOptions.setDomSettleTimeoutMs(2000);

                logger.info("Extracting with custom options using async method...");
                BrowserAgent.ExtractResultTuple<ProductInfo> extractResult =
                    agent.extractAsync(extractOptions, page);

                assertNotNull("Extract result should not be null", extractResult);
                assertTrue("Extract operation should succeed", extractResult.isSuccess());

                ProductInfo info = extractResult.getData();
                assertNotNull("Product info should not be null", info);

                logger.info("✅ Async extract with custom options completed");
                logger.info("Extracted info: {}", info.getTitle());

                page.close();
                browser.close();
            }
        } catch (Exception e) {
            fail("Async extract with custom options should not throw exception: " + e.getMessage());
        }
    }

    @Test
    public void test07_ActAsyncWithTimeout() {
        logger.info("Test 7: Testing actAsync with custom timeout");

        assertNotNull("Session must be created", session);

        try {
            session.getBrowser().initialize(new BrowserOption());

            try (Playwright playwright = Playwright.create()) {
                String endpointUrl = session.getBrowser().getEndpointUrl();
                Browser browser = playwright.chromium().connectOverCDP(endpointUrl);
                com.microsoft.playwright.BrowserContext context = browser.contexts().get(0);
                Page page = context.newPage();
                BrowserAgent agent = session.getBrowser().getAgent();

                logger.info("Testing async act with custom timeout...");
                ActOptions options = new ActOptions("goto('https://example.com')");
                options.setTimeoutMS(30000);
                options.setDomSettleTimeoutMs(3000);

                ActResult result = agent.actAsync(options, page);

                assertNotNull("ActResult should not be null", result);
                assertTrue("Navigation with timeout should succeed", result.isSuccess());
                logger.info("✅ Async act with timeout completed: {}", result.getMessage());

                page.close();
                browser.close();
            }
        } catch (Exception e) {
            fail("Async act with timeout should not throw exception: " + e.getMessage());
        }
    }

    @Test
    public void test08_CompareAsyncVsSyncAct() {
        logger.info("Test 8: Comparing actAsync vs act performance");

        assertNotNull("Session must be created", session);

        try {
            session.getBrowser().initialize(new BrowserOption());

            try (Playwright playwright = Playwright.create()) {
                String endpointUrl = session.getBrowser().getEndpointUrl();
                Browser browser = playwright.chromium().connectOverCDP(endpointUrl);
                com.microsoft.playwright.BrowserContext context = browser.contexts().get(0);
                Page page = context.newPage();
                BrowserAgent agent = session.getBrowser().getAgent();

                ActOptions options = new ActOptions("goto('https://example.com')");

                logger.info("Testing synchronous act...");
                long startSync = System.currentTimeMillis();
                ActResult syncResult = agent.act(page, options);
                long syncDuration = System.currentTimeMillis() - startSync;

                Thread.sleep(2000);

                logger.info("Testing asynchronous actAsync...");
                long startAsync = System.currentTimeMillis();
                ActResult asyncResult = agent.actAsync(options, page);
                long asyncDuration = System.currentTimeMillis() - startAsync;

                assertNotNull("Sync result should not be null", syncResult);
                assertNotNull("Async result should not be null", asyncResult);

                logger.info("✅ Performance comparison completed");
                logger.info("Sync act duration: {}ms, success: {}", syncDuration, syncResult.isSuccess());
                logger.info("Async act duration: {}ms, success: {}", asyncDuration, asyncResult.isSuccess());

                page.close();
                browser.close();
            }
        } catch (Exception e) {
            logger.warn("Performance comparison test: {}", e.getMessage());
        }
    }

    @Test
    public void test09_CompareAsyncVsSyncExtract() {
        logger.info("Test 9: Comparing extractAsync vs extract performance");

        assertNotNull("Session must be created", session);

        try {
            session.getBrowser().initialize(new BrowserOption());

            try (Playwright playwright = Playwright.create()) {
                String endpointUrl = session.getBrowser().getEndpointUrl();
                Browser browser = playwright.chromium().connectOverCDP(endpointUrl);
                com.microsoft.playwright.BrowserContext context = browser.contexts().get(0);
                Page page = context.newPage();
                BrowserAgent agent = session.getBrowser().getAgent();

                page.navigate("https://example.com",
                    new Page.NavigateOptions()
                        .setWaitUntil(com.microsoft.playwright.options.WaitUntilState.DOMCONTENTLOADED)
                        .setTimeout(60000));
                Thread.sleep(1000);

                String instruction = "Extract page title";
                ExtractOptions<ProductInfo> options = new ExtractOptions<>(instruction, ProductInfo.class);
                options.setUseTextExtract(true);

                logger.info("Testing synchronous extract...");
                long startSync = System.currentTimeMillis();
                BrowserAgent.ExtractResultTuple<ProductInfo> syncResult = agent.extract(page, options);
                long syncDuration = System.currentTimeMillis() - startSync;

                Thread.sleep(2000);

                logger.info("Testing asynchronous extractAsync...");
                long startAsync = System.currentTimeMillis();
                BrowserAgent.ExtractResultTuple<ProductInfo> asyncResult = agent.extractAsync(options, page);
                long asyncDuration = System.currentTimeMillis() - startAsync;

                assertNotNull("Sync result should not be null", syncResult);
                assertNotNull("Async result should not be null", asyncResult);

                logger.info("✅ Performance comparison completed");
                logger.info("Sync extract duration: {}ms, success: {}",
                           syncDuration, syncResult.isSuccess());
                logger.info("Async extract duration: {}ms, success: {}",
                           asyncDuration, asyncResult.isSuccess());

                page.close();
                browser.close();
            }
        } catch (Exception e) {
            logger.warn("Performance comparison test: {}", e.getMessage());
        }
    }

    @Test
    public void test10_AsyncMethodsWithNullPage() {
        logger.info("Test 10: Testing async methods with null page (should use focused page)");

        assertNotNull("Session must be created", session);

        try {
            session.getBrowser().initialize(new BrowserOption());

            try (Playwright playwright = Playwright.create()) {
                String endpointUrl = session.getBrowser().getEndpointUrl();
                com.microsoft.playwright.Browser browser = playwright.chromium().connectOverCDP(endpointUrl);
                BrowserAgent agent = session.getBrowser().getAgent();

                logger.info("Testing actAsync with null page...");
                ActOptions actOptions = new ActOptions("goto('https://example.com')");
                ActResult actResult = agent.actAsync(actOptions);

                assertNotNull("ActResult should not be null", actResult);
                logger.info("Async act with null page: success={}", actResult.isSuccess());

                Thread.sleep(2000);

                logger.info("Testing extractAsync with null page...");
                ExtractOptions<ProductInfo> extractOptions =
                    new ExtractOptions<>("Extract page title", ProductInfo.class);
                extractOptions.setUseTextExtract(true);

                BrowserAgent.ExtractResultTuple<ProductInfo> extractResult =
                    agent.extractAsync(extractOptions);

                assertNotNull("ExtractResult should not be null", extractResult);
                logger.info("Async extract with null page: success={}", extractResult.isSuccess());

                logger.info("✅ Async methods with null page completed");

                browser.close();
            }
        } catch (Exception e) {
            logger.info("Async methods with null page may fail if no focused page exists: {}",
                       e.getMessage());
        }
    }
}
