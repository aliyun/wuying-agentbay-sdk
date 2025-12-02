package com.aliyun.agentbay.examples;

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

import java.util.List;

/**
 * Example demonstrating the use of async browser agent methods (actAsync and extractAsync)
 *
 * This example shows how to use the asynchronous variants of browser automation methods
 * which use page_use_act_async and page_use_extract_async for long-running tasks.
 *
 * Prerequisites:
 * - AGENTBAY_API_KEY environment variable must be set
 * - Internet connection for accessing web pages
 *
 * Usage:
 * mvn clean compile exec:java -Dexec.mainClass="examples.BrowserAgentAsyncExample"
 */
public class BrowserAgentAsyncExample {

    /**
     * Data model for extracting game state from 2048 game
     */
    public static class GameState {
        @JsonProperty("score")
        private Integer score;

        @JsonProperty("highestTile")
        private Integer highestTile;

        @JsonProperty("grid")
        private List<List<Integer>> grid;

        public Integer getScore() { return score; }
        public void setScore(Integer score) { this.score = score; }

        public Integer getHighestTile() { return highestTile; }
        public void setHighestTile(Integer highestTile) { this.highestTile = highestTile; }

        public List<List<Integer>> getGrid() { return grid; }
        public void setGrid(List<List<Integer>> grid) { this.grid = grid; }
    }

    public static void main(String[] args) {
        System.out.println("=== BrowserAgent Async Methods Example ===\n");

        // Get API key from environment variable
        String apiKey = System.getenv("AGENTBAY_API_KEY");
        if (apiKey == null || apiKey.isEmpty()) {
            System.err.println("Error: AGENTBAY_API_KEY environment variable is not set");
            System.exit(1);
        }

        Session session = null;

        try {
            // 1. Initialize AgentBay client
            System.out.println("1. Initializing AgentBay client...");
            AgentBay agentBay = new AgentBay(apiKey);

            // 2. Create a browser session
            System.out.println("2. Creating browser session...");
            CreateSessionParams params = new CreateSessionParams();
            params.setImageId("browser_latest");
            SessionResult sessionResult = agentBay.create(params);

            if (!sessionResult.isSuccess()) {
                System.err.println("Failed to create session: " + sessionResult.getErrorMessage());
                System.exit(1);
            }

            session = sessionResult.getSession();
            System.out.println("   Session created with ID: " + session.getSessionId());

            // 3. Initialize browser
            System.out.println("3. Initializing browser...");
            BrowserOption browserOption = new BrowserOption();
            boolean browserInitialized = session.getBrowser().initialize(browserOption);

            if (!browserInitialized) {
                System.err.println("Failed to initialize browser");
                System.exit(1);
            }
            System.out.println("   Browser initialized successfully");

            // 4. Connect to browser using Playwright
            System.out.println("4. Connecting to browser via Playwright...");
            String endpointUrl = session.getBrowser().getEndpointUrl();
            System.out.println("   Endpoint URL: " + endpointUrl);

            try (Playwright playwright = Playwright.create()) {
                Browser browser = playwright.chromium().connectOverCDP(endpointUrl);
                com.microsoft.playwright.BrowserContext context = browser.contexts().get(0);
                Page page = context.newPage();
                BrowserAgent agent = session.getBrowser().getAgent();

                // 5. Example 1: Using actAsync for navigation
                System.out.println("\n5. Example 1: Using actAsync for navigation");
                System.out.println("   Navigating to 2048 game using actAsync...");

                ActOptions navOptions = new ActOptions("goto('https://ovolve.github.io/2048-AI/')");
                navOptions.setTimeoutMS(60000);

                ActResult navResult = agent.actAsync(navOptions, page);
                System.out.println("   Navigation result: " +
                    (navResult.isSuccess() ? "Success" : "Failed"));
                System.out.println("   Message: " + navResult.getMessage());

                Thread.sleep(2000);

                // Wait for game to load
                page.waitForSelector(".grid-container",
                    new Page.WaitForSelectorOptions().setTimeout(10000));
                Thread.sleep(1000);

                // 6. Example 2: Using extractAsync for data extraction
                System.out.println("\n6. Example 2: Using extractAsync for data extraction");
                System.out.println("   Extracting game state using extractAsync...");

                String instruction = "Extract the current game state:\n" +
                    "1. Score from the score counter\n" +
                    "2. All tile values and their positions in the 4x4 grid. " +
                    "Each tile's position is in the tile-position-x-y class where x is column (1-4) and y is row (1-4). " +
                    "Empty spaces should be 0. For example, if only tiles at column 1, row 4 (value 2) and " +
                    "column 4, row 1 (value 2) exist, the grid should be: [[0,0,0,2],[0,0,0,0],[0,0,0,0],[2,0,0,0]]\n" +
                    "3. Highest tile value present";

                ExtractOptions<GameState> extractOptions =
                    new ExtractOptions<>(instruction, GameState.class);
                extractOptions.setUseTextExtract(false);
                extractOptions.setUseVision(true);

                BrowserAgent.ExtractResultTuple<GameState> extractResult =
                    agent.extractAsync(extractOptions, page);

                if (extractResult.isSuccess()) {
                    GameState gameState = extractResult.getData();
                    System.out.println("   Extraction successful!");
                    System.out.println("   Score: " + gameState.getScore());
                    System.out.println("   Highest Tile: " + gameState.getHighestTile());
                    System.out.println("   Grid:");

                    if (gameState.getGrid() != null) {
                        for (int i = 0; i < gameState.getGrid().size(); i++) {
                            System.out.println("     Row " + (i+1) + ": " +
                                gameState.getGrid().get(i));
                        }
                    }
                } else {
                    System.out.println("   Extraction failed");
                }

                // 7. Example 3: Using actAsync for game interaction
                System.out.println("\n7. Example 3: Using actAsync for game interaction");
                System.out.println("   Making moves using keyboard...");

                // Make a few moves
                String[] moves = {"ArrowLeft", "ArrowUp", "ArrowRight", "ArrowDown"};
                for (String move : moves) {
                    ActOptions moveOptions = new ActOptions(
                        "keyboard.press('" + move + "')");
                    ActResult moveResult = agent.actAsync(moveOptions, page);

                    System.out.println("   Move " + move + ": " +
                        (moveResult.isSuccess() ? "Success" : "Failed"));
                    Thread.sleep(500);
                }

                // 8. Example 4: Extract updated game state
                System.out.println("\n8. Example 4: Extract updated game state");
                System.out.println("   Extracting game state after moves...");

                Thread.sleep(1000);

                BrowserAgent.ExtractResultTuple<GameState> finalResult =
                    agent.extractAsync(extractOptions, page);

                if (finalResult.isSuccess()) {
                    GameState finalState = finalResult.getData();
                    System.out.println("   Final extraction successful!");
                    System.out.println("   Final Score: " + finalState.getScore());
                    System.out.println("   Final Highest Tile: " + finalState.getHighestTile());
                    System.out.println("   Score increased: " +
                        (finalState.getScore() > extractResult.getData().getScore()));
                }

                // 9. Comparison: Sync vs Async methods
                System.out.println("\n9. Comparison: Testing sync vs async performance");

                // Test sync method
                System.out.println("   Testing synchronous extract...");
                long syncStart = System.currentTimeMillis();
                BrowserAgent.ExtractResultTuple<GameState> syncResult =
                    agent.extract(page, extractOptions);
                long syncDuration = System.currentTimeMillis() - syncStart;
                System.out.println("   Sync extract completed in: " + syncDuration + "ms");

                Thread.sleep(2000);

                // Test async method
                System.out.println("   Testing asynchronous extractAsync...");
                long asyncStart = System.currentTimeMillis();
                BrowserAgent.ExtractResultTuple<GameState> asyncResult =
                    agent.extractAsync(extractOptions, page);
                long asyncDuration = System.currentTimeMillis() - asyncStart;
                System.out.println("   Async extract completed in: " + asyncDuration + "ms");

                System.out.println("\n   Note: Both sync and async methods use task polling.");
                System.out.println("   The async variant (page_use_extract_async) is designed");
                System.out.println("   for long-running complex extraction tasks.");

                // Clean up
                page.close();
                browser.close();

                System.out.println("\n=== Example completed successfully ===");
            }

        } catch (AgentBayException e) {
            System.err.println("AgentBay error: " + e.getMessage());
            e.printStackTrace();
        } catch (Exception e) {
            System.err.println("Unexpected error: " + e.getMessage());
            e.printStackTrace();
        } finally {
            // Session cleanup is handled automatically by SDK
            if (session != null) {
                System.out.println("\nSession " + session.getSessionId() + " will be cleaned up automatically");
            }
        }
    }
}
