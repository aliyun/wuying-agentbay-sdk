package com.aliyun.agentbay.browser;

import com.aliyun.agentbay.exception.AgentBayException;
import com.aliyun.agentbay.exception.BrowserException;
import com.aliyun.agentbay.model.OperationResult;
import com.aliyun.agentbay.service.BaseService;
import com.aliyun.agentbay.session.Session;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.core.type.TypeReference;
import com.google.gson.Gson;
import com.google.gson.JsonObject;
import com.microsoft.playwright.BrowserContext;
import com.microsoft.playwright.CDPSession;
import com.microsoft.playwright.Page;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.*;

/**
 * BrowserAgent provides AI-powered browser automation capabilities
 * Matches Python BrowserAgent functionality completely
 */
public class BrowserAgent extends BaseService {
    private static final Logger logger = LoggerFactory.getLogger(BrowserAgent.class);
    private static final ObjectMapper objectMapper = new ObjectMapper();

    private final Browser browser;

    public BrowserAgent(Session session, Browser browser) {
        super(session);
        this.browser = browser;
    }

    /**
     * Get page and context index from Playwright Page object
     * Matches Python _get_page_and_context_index method
     */
    private PageContextIndex getPageAndContextIndex(Page page) throws BrowserException {
        if (page == null) {
            return new PageContextIndex(null, 0);
        }

        try {
            BrowserContext context = page.context();
            CDPSession cdpSession = context.newCDPSession(page);
            Object targetInfoResponse = cdpSession.send("Target.getTargetInfo");
            cdpSession.detach();

            String pageIndex;
            if (targetInfoResponse instanceof JsonObject) {
                JsonObject response = (JsonObject) targetInfoResponse;
                JsonObject targetInfo = response.getAsJsonObject("targetInfo");
                pageIndex = targetInfo.get("targetId").getAsString();
            } else if (targetInfoResponse instanceof Map) {
                @SuppressWarnings("unchecked")
                Map<String, Object> response = (Map<String, Object>) targetInfoResponse;
                @SuppressWarnings("unchecked")
                Map<String, Object> targetInfo = (Map<String, Object>) response.get("targetInfo");
                pageIndex = (String) targetInfo.get("targetId");
            } else {
                Gson gson = new Gson();
                String json = gson.toJson(targetInfoResponse);
                JsonObject response = gson.fromJson(json, JsonObject.class);
                JsonObject targetInfo = response.getAsJsonObject("targetInfo");
                pageIndex = targetInfo.get("targetId").getAsString();
            }

            return new PageContextIndex(pageIndex, 0);
        } catch (Exception e) {
            throw new BrowserException("Failed to get page index: " + e.getMessage());
        }
    }

    private static class PageContextIndex {
        final String pageIndex;
        final int contextIndex;

        PageContextIndex(String pageIndex, int contextIndex) {
            this.pageIndex = pageIndex;
            this.contextIndex = contextIndex;
        }
    }

    /**
     * Navigate to a URL - matches Python navigate method
     *
     * @param url The URL to navigate to
     * @return Success message or error message
     * @throws BrowserException if browser is not initialized
     */
    public String navigate(String url) throws BrowserException {
        if (!browser.isInitialized()) {
            throw new BrowserException("Browser must be initialized before calling navigate.");
        }
        try {
            Map<String, Object> args = new HashMap<>();
            args.put("url", url);
            OperationResult response = callMcpToolTimeout("page_use_navigate", args);
            if (response.isSuccess()) {
                return response.getData();
            } else {
                return "Navigation failed: " + response.getErrorMessage();
            }
        } catch (Exception e) {
            throw new BrowserException("Failed to navigate: " + e.getMessage());
        }
    }

    /**
     * Close the remote browser agent session - matches Python close method
     *
     * @return true if successful, false otherwise
     * @throws BrowserException if operation fails
     */
    public boolean close() throws BrowserException {
        try {
            OperationResult response = callMcpToolTimeout("page_use_close_session", new HashMap<>());
            if (response.isSuccess()) {
                logger.info("Session close status: {}", response.getData());
                return true;
            } else {
                logger.warn("Failed to close session: {}", response.getErrorMessage());
                return false;
            }
        } catch (Exception e) {
            throw new BrowserException("Failed to call close: " + e.getMessage());
        }
    }

    /**
     * Take a screenshot of the specified page - matches Python screenshot method
     *
     * @param page Playwright Page object (null to use currently focused page)
     * @param fullPage Whether to capture the full scrollable page
     * @param quality Quality of the image (0-100, for JPEG)
     * @param clip Clipping region {x, y, width, height}
     * @param timeout Custom timeout in milliseconds
     * @return Base64 encoded data URL of the screenshot
     * @throws BrowserException if browser is not initialized
     */
    public String screenshot(Page page, boolean fullPage, int quality, Map<String, Double> clip, Integer timeout) throws BrowserException {
        if (!browser.isInitialized()) {
            throw new BrowserException("Browser must be initialized before calling screenshot.");
        }
        try {
            PageContextIndex indices = getPageAndContextIndex(page);
            return executeScreenshot(indices.contextIndex, indices.pageIndex, fullPage, quality, clip, timeout);
        } catch (Exception e) {
            throw new BrowserException("Failed to call screenshot: " + e.getMessage());
        }
    }

    /**
     * Overloaded screenshot method with default parameters
     */
    public String screenshot(Page page) throws BrowserException {
        return screenshot(page, true, 80, null, null);
    }

    /**
     * Execute screenshot with parameters
     */
    private String executeScreenshot(int contextId, String pageId, boolean fullPage, int quality,
                                     Map<String, Double> clip, Integer timeout) {
        logger.debug("Screenshot page_id: {}, context_id: {}", pageId, contextId);
        Map<String, Object> args = new HashMap<>();
        args.put("context_id", contextId);
        if (pageId != null) args.put("page_id", pageId);
        args.put("full_page", fullPage);
        args.put("quality", quality);
        if (clip != null) args.put("clip", clip);
        if (timeout != null) args.put("timeout", timeout);

        OperationResult response = callMcpToolTimeout("page_use_screenshot", args);
        if (response.isSuccess()) {
            return response.getData();
        } else {
            return "Screenshot failed: " + response.getErrorMessage();
        }
    }

    /**
     * Perform an action on the page - matches Python act method
     * Uses synchronous execution
     *
     * @param page Playwright page object
     * @param actionInput Either ActOptions or ObserveResult
     * @return ActResult
     */
    public ActResult act(Page page, Object actionInput) throws BrowserException {
        if (!browser.isInitialized()) {
            throw new BrowserException("Browser is not initialized");
        }

        try {
            PageContextIndex indices = getPageAndContextIndex(page);
            return executeAct(actionInput, indices.contextIndex, indices.pageIndex);
        } catch (Exception e) {
            throw new BrowserException("Failed to act: " + e.getMessage());
        }
    }

    /**
     * Perform an action on the page asynchronously - matches Python act_async method
     * Uses asynchronous execution with task polling for long-running operations
     *
     * @param actionInput Either ActOptions or ObserveResult describing the action
     * @param page Playwright page object (null to use currently focused page)
     * @return ActResult containing success status and execution details
     * @throws BrowserException if browser is not initialized or action fails
     *
     * Example:
     * <pre>
     * ActOptions options = new ActOptions("click('#submit-button')");
     * ActResult result = agent.actAsync(options, page);
     * if (result.isSuccess()) {
     *     System.out.println("Action completed: " + result.getMessage());
     * }
     * </pre>
     */
    public ActResult actAsync(Object actionInput, Page page) throws BrowserException {
        if (!browser.isInitialized()) {
            throw new BrowserException("Browser is not initialized");
        }

        try {
            PageContextIndex indices = getPageAndContextIndex(page);
            return executeActAsync(actionInput, indices.contextIndex, indices.pageIndex);
        } catch (Exception e) {
            throw new BrowserException("Failed to act async: " + e.getMessage());
        }
    }

    /**
     * Perform an action on the page asynchronously without explicit Playwright Page
     * This overload allows using the agent independently of Playwright
     * Uses the default context (index 0) and currently focused page
     *
     * @param actionInput Either ActOptions or ObserveResult describing the action
     * @return ActResult containing success status and execution details
     * @throws BrowserException if browser is not initialized or action fails
     *
     * Example:
     * <pre>
     * ActOptions options = new ActOptions("click('#submit-button')");
     * ActResult result = agent.actAsync(options);
     * if (result.isSuccess()) {
     *     System.out.println("Action completed: " + result.getMessage());
     * }
     * </pre>
     */
    public ActResult actAsync(Object actionInput) throws BrowserException {
        return actAsync(actionInput, null);
    }

    /**
     * Execute act with task polling mechanism - matches Python _execute_act
     * Uses synchronous page_use_act tool
     */
    private ActResult executeAct(Object actionInput, int contextId, String pageId) throws BrowserException {
        return executeActInternal(actionInput, contextId, pageId, false);
    }

    /**
     * Execute act with async task mechanism - matches Python _execute_act_async
     * Uses asynchronous page_use_act_async tool for long-running tasks
     *
     * @param actionInput Either ActOptions or ObserveResult
     * @param contextId Browser context ID
     * @param pageId Page ID
     * @return ActResult containing success status and execution details
     * @throws BrowserException if the action fails
     */
    private ActResult executeActAsync(Object actionInput, int contextId, String pageId) throws BrowserException {
        return executeActInternal(actionInput, contextId, pageId, true);
    }

    /**
     * Internal method to execute act with either sync or async tool
     */
    private ActResult executeActInternal(Object actionInput, int contextId, String pageId, boolean useAsync) throws BrowserException {
        logger.debug("Acting page_id: {}, context_id: {}, async: {}", pageId, contextId, useAsync);
        Map<String, Object> args = new HashMap<>();
        args.put("context_id", contextId);
        if (pageId != null) args.put("page_id", pageId);

        String taskName = "act";
        if (actionInput instanceof ActOptions) {
            ActOptions options = (ActOptions) actionInput;
            args.put("action", options.getAction());
            if (options.getVariables() != null) args.put("variables", options.getVariables());
            if (options.getTimeoutMS() != null) args.put("timeout_ms", options.getTimeoutMS());
            if (options.getIframes() != null) args.put("iframes", options.getIframes());
            if (options.getDomSettleTimeoutMs() != null) args.put("dom_settle_timeout_ms", options.getDomSettleTimeoutMs());
            if (options.getUseVision() != null) args.put("use_vision", options.getUseVision());
            taskName = options.getAction();
        } else if (actionInput instanceof ObserveResult) {
            ObserveResult result = (ObserveResult) actionInput;
            try {
                Map<String, Object> actionDict = new HashMap<>();
                actionDict.put("method", result.getMethod());
                actionDict.put("arguments", result.getArguments());
                args.put("action", objectMapper.writeValueAsString(actionDict));
                taskName = result.getMethod();
            } catch (Exception e) {
                throw new BrowserException("Failed to serialize action: " + e.getMessage());
            }
        }

        // Remove null values
        args.values().removeIf(java.util.Objects::isNull);
        logger.info("{}", taskName);

        String toolName = useAsync ? "page_use_act_async" : "page_use_act";
        OperationResult response = callMcpToolTimeout(toolName, args);
        if (!response.isSuccess()) {
            throw new BrowserException("Failed to start act task: " + response.getErrorMessage());
        }

        // Parse task_id from response
        try {
            Map<String, Object> responseData = parseJsonResponse(response.getData());
            String taskId = (String) responseData.get("task_id");

            if (taskId == null) {
                // Task completed immediately
                if (responseData.containsKey("steps") || responseData.containsKey("is_done")) {
                    Object steps = responseData.get("steps");
                    boolean success = Boolean.TRUE.equals(responseData.get("success"));
                    String taskStatus = steps instanceof String ? (String) steps : objectMapper.writeValueAsString(steps);
                    logger.info("Task {} completed immediately. Success: {}", taskName, success);
                    return new ActResult(success, taskStatus, taskName);
                }
                throw new BrowserException("No task_id in response: " + responseData);
            }

            // Task polling loop
            int maxRetries = 30;
            while (maxRetries > 0) {
                Thread.sleep(5000); // 5 seconds

                Map<String, Object> params = new HashMap<>();
                params.put("task_id", taskId);
                OperationResult result = callMcpToolTimeout("page_use_get_act_result", params);

                if (result.isSuccess() && result.getData() != null) {
                    Map<String, Object> data = parseJsonResponse(result.getData());
                    logger.debug("Act result data type: {}, data: {}", data.getClass(), data);

                    if (!(data instanceof Map)) {
                        logger.warn("Received non-map data for act result, skipping this iteration");
                        maxRetries--;
                        continue;
                    }

                    Object steps = data.get("steps");
                    boolean isDone = Boolean.TRUE.equals(data.get("is_done"));
                    boolean success = Boolean.TRUE.equals(data.get("success"));
                    String noActionMsg = "No actions have been executed.";

                    if (isDone) {
                        String taskStatus;
                        if (steps != null) {
                            taskStatus = steps instanceof String ? (String) steps : objectMapper.writeValueAsString(steps);
                        } else {
                            taskStatus = noActionMsg;
                        }
                        logger.info("Task {}:{} is done. Success: {}. {}", taskId, taskName, success, taskStatus);
                        return new ActResult(success, taskStatus, taskName);
                    }

                    String taskStatus = steps != null ? "steps done. Details: " + steps : noActionMsg;
                    logger.info("Task {}:{} in progress. {}", taskId, taskName, taskStatus);
                }
                maxRetries--;
            }
            throw new BrowserException("Task " + taskId + ":" + taskName + " Act timed out");
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            throw new BrowserException("Act task interrupted: " + e.getMessage());
        } catch (Exception e) {
            throw new BrowserException("Failed to parse act response: " + e.getMessage());
        }
    }

    /**
     * Parse JSON response - helper method for parsing API responses
     */
    @SuppressWarnings("unchecked")
    private Map<String, Object> parseJsonResponse(String data) throws Exception {
        if (data == null || data.isEmpty()) {
            return new HashMap<>();
        }
        return objectMapper.readValue(data, new TypeReference<Map<String, Object>>(){});
    }

    /**
     * Observe elements on the page - matches Python observe method
     *
     * @param page Playwright page object
     * @param options ObserveOptions
     * @return Tuple of success and list of ObserveResult
     */
    public ObserveResultTuple observe(Page page, ObserveOptions options) throws BrowserException {
        if (!browser.isInitialized()) {
            throw new BrowserException("Browser is not initialized");
        }

        try {
            PageContextIndex indices = getPageAndContextIndex(page);
            Map<String, Object> args = new HashMap<>();
            // Use Python-compatible parameter names
            args.put("page_id", indices.pageIndex);
            args.put("context_id", indices.contextIndex);
            args.putAll(options.toMap());

            OperationResult result = callMcpTool("page_use_observe", args);
            return parseObserveResult(result);
        } catch (Exception e) {
            logger.error("Failed to observe elements", e);
            return new ObserveResultTuple(false, new ArrayList<>());
        }
    }

    private ObserveResultTuple parseObserveResult(OperationResult result) {
        if (!result.isSuccess()) {
            return new ObserveResultTuple(false, new ArrayList<>());
        }

        try {
            List<Map<String, Object>> observeResults = objectMapper.readValue(
                result.getData(),
                new TypeReference<List<Map<String, Object>>>(){}
            );

            List<ObserveResult> results = new ArrayList<>();
            if (observeResults != null) {
                for (Map<String, Object> item : observeResults) {
                    String selector = (String) item.get("selector");
                    String description = (String) item.get("description");
                    String method = (String) item.get("method");
                    String argumentsStr = (String) item.get("arguments");

                    Map<String, Object> arguments;
                    try {
                        arguments = objectMapper.readValue(argumentsStr, new TypeReference<Map<String, Object>>(){});
                    } catch (Exception e) {
                        logger.warn("Could not parse arguments as JSON: {}", argumentsStr);
                        arguments = new HashMap<>();
                    }

                    results.add(new ObserveResult(selector, description, method, arguments));
                }
            }

            return new ObserveResultTuple(true, results);
        } catch (Exception e) {
            logger.warn("Failed to parse observe result", e);
            return new ObserveResultTuple(false, new ArrayList<>());
        }
    }

    public static class ObserveResultTuple {
        private final boolean success;
        private final List<ObserveResult> results;

        public ObserveResultTuple(boolean success, List<ObserveResult> results) {
            this.success = success;
            this.results = results;
        }

        public boolean isSuccess() { return success; }
        public List<ObserveResult> getResults() { return results; }
    }

    /**
     * Extract structured data from the page - matches Python extract method
     * Uses synchronous execution
     *
     * @param page Playwright page object
     * @param options ExtractOptions
     * @return Tuple of success and extracted data
     */
    public <T> ExtractResultTuple<T> extract(Page page, ExtractOptions<T> options) throws BrowserException {
        if (!browser.isInitialized()) {
            throw new BrowserException("Browser is not initialized");
        }

        try {
            PageContextIndex indices = getPageAndContextIndex(page);
            return executeExtract(options, indices.contextIndex, indices.pageIndex);
        } catch (Exception e) {
            throw new BrowserException("Failed to extract: " + e.getMessage());
        }
    }

    /**
     * Extract structured data from the page asynchronously - matches Python extract_async method
     * Uses asynchronous execution with task polling for complex extraction operations
     *
     * @param options ExtractOptions containing instruction, schema, and extraction parameters
     * @param page Playwright page object (null to use currently focused page)
     * @param <T> The type of data to extract (must match the schema class)
     * @return ExtractResultTuple containing success status and extracted data of type T
     * @throws BrowserException if browser is not initialized or extraction fails
     *
     * Example:
     * <pre>
     * class ProductInfo {
     *     public String name;
     *     public double price;
     * }
     *
     * ExtractOptions&lt;ProductInfo&gt; options = new ExtractOptions&lt;&gt;(
     *     "Extract product name and price",
     *     ProductInfo.class
     * );
     *
     * ExtractResultTuple&lt;ProductInfo&gt; result = agent.extractAsync(options, page);
     * if (result.isSuccess()) {
     *     ProductInfo product = result.getData();
     *     System.out.println("Product: " + product.name + ", Price: $" + product.price);
     * }
     * </pre>
     */
    public <T> ExtractResultTuple<T> extractAsync(ExtractOptions<T> options, Page page) throws BrowserException {
        if (!browser.isInitialized()) {
            throw new BrowserException("Browser is not initialized");
        }

        try {
            PageContextIndex indices = getPageAndContextIndex(page);
            return executeExtractAsync(options, indices.contextIndex, indices.pageIndex);
        } catch (Exception e) {
            throw new BrowserException("Failed to extract async: " + e.getMessage());
        }
    }

    /**
     * Extract structured data from the page asynchronously without explicit Playwright Page
     * This overload allows using the agent independently of Playwright
     * Uses the default context (index 0) and currently focused page
     *
     * @param options ExtractOptions containing instruction, schema, and extraction parameters
     * @param <T> The type of data to extract (must match the schema class)
     * @return ExtractResultTuple containing success status and extracted data of type T
     * @throws BrowserException if browser is not initialized or extraction fails
     *
     * Example:
     * <pre>
     * class ProductInfo {
     *     public String name;
     *     public double price;
     * }
     *
     * ExtractOptions&lt;ProductInfo&gt; options = new ExtractOptions&lt;&gt;(
     *     "Extract product name and price",
     *     ProductInfo.class
     * );
     *
     * ExtractResultTuple&lt;ProductInfo&gt; result = agent.extractAsync(options);
     * if (result.isSuccess()) {
     *     ProductInfo product = result.getData();
     *     System.out.println("Product: " + product.name);
     * }
     * </pre>
     */
    public <T> ExtractResultTuple<T> extractAsync(ExtractOptions<T> options) throws BrowserException {
        return extractAsync(options, null);
    }

    /**
     * Execute extract with task polling mechanism - matches Python _execute_extract
     * Uses synchronous page_use_extract tool
     */
    private <T> ExtractResultTuple<T> executeExtract(ExtractOptions<T> options, int contextId, String pageId) throws BrowserException {
        return executeExtractInternal(options, contextId, pageId, false);
    }

    /**
     * Execute extract with async task mechanism - matches Python _execute_extract_async
     * Uses asynchronous page_use_extract_async tool for complex extraction tasks
     *
     * @param options ExtractOptions containing instruction and schema
     * @param contextId Browser context ID
     * @param pageId Page ID
     * @return ExtractResultTuple containing success status and extracted data
     * @throws BrowserException if extraction fails
     */
    private <T> ExtractResultTuple<T> executeExtractAsync(ExtractOptions<T> options, int contextId, String pageId) throws BrowserException {
        return executeExtractInternal(options, contextId, pageId, true);
    }

    /**
     * Internal method to execute extract with either sync or async tool
     */
    private <T> ExtractResultTuple<T> executeExtractInternal(ExtractOptions<T> options, int contextId, String pageId, boolean useAsync) throws BrowserException {
        Map<String, Object> args = new HashMap<>();
        args.put("context_id", contextId);
        if (pageId != null) args.put("page_id", pageId);
        args.putAll(options.toMap());

        // Remove null values
        args.values().removeIf(java.util.Objects::isNull);

        String toolName = useAsync ? "page_use_extract_async" : "page_use_extract";
        OperationResult response = callMcpToolTimeout(toolName, args);
        if (!response.isSuccess()) {
            throw new BrowserException("Failed to start extraction task");
        }

        // Parse task_id from response
        try {
            Map<String, Object> responseData = parseJsonResponse(response.getData());
            String taskId = (String) responseData.get("task_id");

            if (taskId == null) {
                // Extraction completed immediately
                try {
                    logger.info("Extract completed immediately, validating response");
                    T extractedObject = objectMapper.convertValue(responseData, options.getSchema());
                    return new ExtractResultTuple<>(true, extractedObject);
                } catch (Exception e) {
                    throw new BrowserException("No task_id and failed to validate response as result: " + e.getMessage() + ", data: " + responseData);
                }
            }

            // Task polling loop
            int maxRetries = 20;
            while (maxRetries > 0) {
                Thread.sleep(8000); // 8 seconds

                Map<String, Object> extractParams = new HashMap<>();
                extractParams.put("task_id", taskId);
                OperationResult result = callMcpToolTimeout("page_use_get_extract_result", extractParams);

                if (result.isSuccess() && result.getData() != null) {
                    Map<String, Object> extractResult = parseJsonResponse(result.getData());
                    T extractedObject = objectMapper.convertValue(extractResult, options.getSchema());
                    return new ExtractResultTuple<>(true, extractedObject);
                }
                maxRetries--;
                logger.debug("Task {}: No extract result yet (attempt {}/20)", taskId, 20 - maxRetries);
            }
            throw new BrowserException("Task " + taskId + ": Extract timed out");
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            throw new BrowserException("Extract task interrupted: " + e.getMessage());
        } catch (Exception e) {
            throw new BrowserException("Failed to parse extract response: " + e.getMessage());
        }
    }

    public static class ExtractResultTuple<T> {
        private final boolean success;
        private final T data;

        public ExtractResultTuple(boolean success, T data) {
            this.success = success;
            this.data = data;
        }

        public boolean isSuccess() { return success; }
        public T getData() { return data; }
    }

    /**
     * Call MCP tool with timeout - matches Python _call_mcp_tool_timeout method
     */
    private OperationResult callMcpToolTimeout(String name, Map<String, Object> args) {
        return callMcpTool(name, args);
    }

    // Convenience methods for common operations (matching existing functionality)

    /**
     * Navigate to a URL using act method
     */
    public ActResult navigateTo(Page page, String url) throws BrowserException {
        return act(page, new ActOptions("goto('" + url + "')"));
    }

    /**
     * Click on an element using act method
     */
    public ActResult click(Page page, String selector) throws BrowserException {
        return act(page, new ActOptions("click('" + selector + "')"));
    }

    /**
     * Type text into an input field using act method
     */
    public ActResult type(Page page, String selector, String text) throws BrowserException {
        return act(page, new ActOptions("fill('" + selector + "', '" + text + "')"));
    }

    /**
     * Take a screenshot using act method
     */
    public ActResult takeScreenshot(Page page) throws BrowserException {
        return act(page, new ActOptions("screenshot()"));
    }
}