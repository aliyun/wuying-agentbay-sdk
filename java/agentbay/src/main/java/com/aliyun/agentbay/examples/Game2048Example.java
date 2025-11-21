package com.aliyun.agentbay.examples;

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
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.*;

/**
 * Example: 2048 Game (Extract)
 * Extract board state
 * Use minimax algorithm to decide next move and execute in loop
 * Focus: Extract combined with strategy; keyboard actions
 */
public class Game2048Example {
    private static final Logger logger = LoggerFactory.getLogger(Game2048Example.class);

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

    public static void main(String[] args) {
        String apiKey = System.getenv("AGENTBAY_API_KEY");
        if (apiKey == null || apiKey.trim().isEmpty()) {
            System.err.println("Error: AGENTBAY_API_KEY environment variable not set");
            return;
        }

        try {
            System.out.println("Initializing AgentBay client...");
            AgentBay agentBay = new AgentBay(apiKey);

            System.out.println("Creating a new session...");
            CreateSessionParams params = new CreateSessionParams();
            params.setImageId("browser_latest");

            SessionResult sessionResult = agentBay.create(params);

            if (sessionResult.isSuccess()) {
                Session session = sessionResult.getSession();

                SessionInfoResult result = session.info();
                if (result.isSuccess()) {
                    String desktopUrl = result.getSessionInfo().getResourceUrl();
                    System.out.println("Session URL: " + desktopUrl);
                }

                System.out.println("Session created with ID: " + session.getSessionId());

                if (session.getBrowser().initialize(new BrowserOption())) {
                    System.out.println("Browser initialized successfully");
                    String endpointUrl = session.getBrowser().getEndpointUrl();
                    System.out.println("endpoint_url = " + endpointUrl);

                    try (Playwright playwright = Playwright.create()) {
                        com.microsoft.playwright.Browser browser = playwright.chromium().connectOverCDP(endpointUrl);
                        BrowserContext context = browser.contexts().get(0);
                        Page page = context.newPage();
                        BrowserAgent agent = session.getBrowser().getAgent();

                        System.out.println("🌐 Navigating to 2048...");
                        page.navigate("https://ovolve.github.io/2048-AI/",
                            new Page.NavigateOptions()
                                .setWaitUntil(com.microsoft.playwright.options.WaitUntilState.DOMCONTENTLOADED)
                                .setTimeout(180000));
                        System.out.println("🌐 Navigated to 2048 done");
                        page.waitForSelector(".grid-container", new Page.WaitForSelectorOptions().setTimeout(10000));

                        MiniMax helper = new MiniMax();
                        Deque<MoveHistoryEntry> moveHistory = new ArrayDeque<>(3);
                        String lastGridState = null;
                        Map<Integer, String> movesMap = new HashMap<>();
                        movesMap.put(0, "left");
                        movesMap.put(1, "up");
                        movesMap.put(2, "right");
                        movesMap.put(3, "down");
                        List<String> allPossibleMoves = Arrays.asList("left", "up", "right", "down");

                        while (true) {
                            System.out.println("🔄 Game loop iteration...");
                            Thread.sleep(300);

                            System.out.println("📊 Extracting game state...");
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

                            ExtractOptions<GameState> extractOptions = new ExtractOptions<>(instruction, GameState.class);
                            extractOptions.setUseTextExtract(false);

                            BrowserAgent.ExtractResultTuple<GameState> extractResult = agent.extract(page, extractOptions);

                            if (extractResult.isSuccess() && extractResult.getData() != null) {
                                GameState gameState = extractResult.getData();
                                List<List<Integer>> transposedGrid = transposeGrid(gameState.getGrid());
                                System.out.println("transposed grid: " + transposedGrid);
                                System.out.println("🤔 Analyzing board for next move...");

                                String currentGridFlat = gridToString(transposedGrid);

                                if (lastGridState != null && currentGridFlat.equals(lastGridState)) {
                                    System.out.println("Grid has not changed from the last iteration. This might indicate a stuck state.");
                                }
                                lastGridState = currentGridFlat;

                                helper.grid = flattenGrid(transposedGrid);
                                helper.startSearch();

                                String bestMoveStr = movesMap.getOrDefault(helper.bestOperation, "no_move");
                                String selectedMove = bestMoveStr;
                                System.out.println(String.format("Calculated mini max move: %s (explored %d nodes, max_depth=%d).",
                                    bestMoveStr, helper.node, helper.maxDepth));

                                String currentGridTuple = gridToString(gameState.getGrid());

                                if (moveHistory.size() == 3) {
                                    moveHistory.removeFirst();
                                }
                                moveHistory.addLast(new MoveHistoryEntry(currentGridTuple, bestMoveStr));

                                if (moveHistory.size() == 3) {
                                    boolean isCycling = true;
                                    MoveHistoryEntry first = moveHistory.getFirst();
                                    for (MoveHistoryEntry entry : moveHistory) {
                                        if (!entry.equals(first)) {
                                            isCycling = false;
                                            break;
                                        }
                                    }

                                    if (isCycling && !bestMoveStr.equals("no_move")) {
                                        System.out.println(String.format("Detected a continuous cycle! The pattern %s repeated 3 times.", first));
                                        System.out.println("Breaking out of cycle with alternative moves!");
                                        moveHistory.clear();

                                        List<String> availableMoves = new ArrayList<>();
                                        for (String m : allPossibleMoves) {
                                            if (!m.equals(bestMoveStr) && !m.equals("no_move")) {
                                                availableMoves.add(m);
                                            }
                                        }
                                        if (!availableMoves.isEmpty()) {
                                            selectedMove = availableMoves.get(new Random().nextInt(availableMoves.size()));
                                        }
                                    }
                                }

                                Map<String, String> moveKeyMap = new HashMap<>();
                                moveKeyMap.put("up", "ArrowUp");
                                moveKeyMap.put("down", "ArrowDown");
                                moveKeyMap.put("left", "ArrowLeft");
                                moveKeyMap.put("right", "ArrowRight");
                                moveKeyMap.put("no_move", "Escape");

                                String moveKey = moveKeyMap.get(selectedMove);
                                page.keyboard().press(moveKey);
                            } else {
                                System.out.println("❌ Failed to extract game state, retry observing");
                            }
                        }

                    } catch (Exception error) {
                        System.err.println("❌ Error in game loop: " + error.getMessage());
                        logger.error("Error in game loop", error);
                    }
                } else {
                    System.err.println("Failed to initialize browser");
                }

            } else {
                System.err.println("Failed to create session: " + sessionResult.getErrorMessage());
            }

        } catch (AgentBayException e) {
            logger.error("AgentBay error occurred", e);
            System.err.println("AgentBay error: " + e.getMessage());
        } catch (Exception e) {
            logger.error("Unexpected error occurred", e);
            System.err.println("Unexpected error: " + e.getMessage());
        }
    }

    private static class MoveHistoryEntry {
        String gridState;
        String move;

        MoveHistoryEntry(String gridState, String move) {
            this.gridState = gridState;
            this.move = move;
        }

        @Override
        public boolean equals(Object o) {
            if (this == o) return true;
            if (o == null || getClass() != o.getClass()) return false;
            MoveHistoryEntry that = (MoveHistoryEntry) o;
            return Objects.equals(gridState, that.gridState) && Objects.equals(move, that.move);
        }

        @Override
        public int hashCode() {
            return Objects.hash(gridState, move);
        }

        @Override
        public String toString() {
            return "(" + gridState + ", " + move + ")";
        }
    }

    private static List<List<Integer>> transposeGrid(List<List<Integer>> grid) {
        if (grid == null || grid.isEmpty()) {
            return new ArrayList<>();
        }

        int rows = grid.size();
        int cols = grid.get(0).size();
        List<List<Integer>> transposed = new ArrayList<>();

        for (int j = 0; j < cols; j++) {
            List<Integer> newRow = new ArrayList<>();
            for (int i = 0; i < rows; i++) {
                newRow.add(grid.get(i).get(j));
            }
            transposed.add(newRow);
        }

        return transposed;
    }

    private static List<Integer> flattenGrid(List<List<Integer>> grid) {
        List<Integer> flat = new ArrayList<>();
        for (List<Integer> row : grid) {
            flat.addAll(row);
        }
        return flat;
    }

    private static String gridToString(List<List<Integer>> grid) {
        StringBuilder sb = new StringBuilder();
        for (List<Integer> row : grid) {
            for (Integer val : row) {
                sb.append(val).append(",");
            }
        }
        return sb.toString();
    }

    private static class MiniMax {
        int bestOperation = -1;
        List<Integer> grid = new ArrayList<>(Collections.nCopies(16, 0));
        int node = 0;
        int maxDepth = 3;

        private List<Integer> moveRowLeftSingle(List<Integer> rowIn) {
            List<Integer> compactedRow = new ArrayList<>();
            for (int val : rowIn) {
                if (val != 0) {
                    compactedRow.add(val);
                }
            }

            List<Integer> processedRow = new ArrayList<>();
            int idxCompacted = 0;
            while (idxCompacted < compactedRow.size()) {
                int currentVal = compactedRow.get(idxCompacted);
                if (idxCompacted + 1 < compactedRow.size() && currentVal == compactedRow.get(idxCompacted + 1)) {
                    processedRow.add(currentVal * 2);
                    idxCompacted += 2;
                } else {
                    processedRow.add(currentVal);
                    idxCompacted += 1;
                }
            }

            while (processedRow.size() < 4) {
                processedRow.add(0);
            }

            return processedRow;
        }

        private List<Integer> moveLeft(List<Integer> sIn) {
            List<Integer> newGrid1d = new ArrayList<>(Collections.nCopies(16, 0));
            for (int rowIdx = 0; rowIdx < 4; rowIdx++) {
                int startIdx = rowIdx * 4;
                List<Integer> rowSlice = new ArrayList<>(sIn.subList(startIdx, startIdx + 4));
                List<Integer> movedRow = moveRowLeftSingle(rowSlice);
                for (int i = 0; i < 4; i++) {
                    newGrid1d.set(startIdx + i, movedRow.get(i));
                }
            }
            return newGrid1d;
        }

        private List<Integer> rotate(List<Integer> s) {
            List<Integer> rotated = new ArrayList<>(Collections.nCopies(16, 0));
            int[] indices = {12, 8, 4, 0, 13, 9, 5, 1, 14, 10, 6, 2, 15, 11, 7, 3};
            for (int i = 0; i < 16; i++) {
                rotated.set(i, s.get(indices[i]));
            }
            return rotated;
        }

        private double estimate(List<Integer> s) {
            int diff = 0;
            int totalSum = 0;
            for (int i = 0; i < 16; i++) {
                totalSum += s.get(i);
                if (i % 4 != 3) {
                    diff += Math.abs(s.get(i) - s.get(i + 1));
                }
                if (i < 12) {
                    diff += Math.abs(s.get(i) - s.get(i + 4));
                }
            }
            return (totalSum * 4.0 - diff) * 2.0;
        }

        private double search(List<Integer> sIn, int depth) {
            node++;
            if (node >= 10000 || depth >= maxDepth) {
                return estimate(sIn);
            }

            double bestScore = Double.NEGATIVE_INFINITY;
            List<Integer> sCurrentDirection = new ArrayList<>(sIn);

            for (int i = 0; i < 4; i++) {
                List<Integer> movedGrid = moveLeft(sCurrentDirection);
                boolean gridChanged = false;
                for (int j = 0; j < 16; j++) {
                    if (!movedGrid.get(j).equals(sCurrentDirection.get(j))) {
                        gridChanged = true;
                        break;
                    }
                }

                if (gridChanged) {
                    double tempExpectedValue = 0.0;
                    List<Integer> emptySlotsIndices = new ArrayList<>();
                    for (int idx = 0; idx < movedGrid.size(); idx++) {
                        if (movedGrid.get(idx) == 0) {
                            emptySlotsIndices.add(idx);
                        }
                    }

                    if (!emptySlotsIndices.isEmpty()) {
                        for (int slotIdx : emptySlotsIndices) {
                            movedGrid.set(slotIdx, 2);
                            tempExpectedValue += search(movedGrid, depth + 1) * 0.9;

                            movedGrid.set(slotIdx, 4);
                            tempExpectedValue += search(movedGrid, depth + 1) * 0.1;

                            movedGrid.set(slotIdx, 0);
                        }
                        tempExpectedValue /= emptySlotsIndices.size();
                    } else {
                        tempExpectedValue = -1e20;
                    }

                    double currentMoveTotalValue = tempExpectedValue;

                    if (currentMoveTotalValue > bestScore) {
                        bestScore = currentMoveTotalValue;
                        if (depth == 0) {
                            bestOperation = i;
                        }
                    }
                } else {
                    if (depth == 0) {
                        double currentMoveTotalValue = -1e20;
                        if (currentMoveTotalValue > bestScore) {
                            bestScore = currentMoveTotalValue;
                            bestOperation = i;
                        }
                    }
                }

                if (i != 3) {
                    sCurrentDirection = rotate(sCurrentDirection);
                }
            }

            return bestScore != Double.NEGATIVE_INFINITY ? bestScore : -1e20;
        }

        void startSearch() {
            node = 0;
            maxDepth = 3;

            while (true) {
                node = 0;
                search(grid, 0);
                if (node >= 10000 || maxDepth >= 8) {
                    break;
                }
                maxDepth++;
            }
        }
    }
}
