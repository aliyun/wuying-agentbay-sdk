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
     * Perform an action on the page - matches Python act method
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
            Map<String, Object> args = new HashMap<>();
            // Use Python-compatible parameter names
            args.put("page_id", indices.pageIndex);
            args.put("context_id", indices.contextIndex);

            if (actionInput instanceof ActOptions) {
                ActOptions options = (ActOptions) actionInput;
                args.put("action", options.getAction());
                if (options.getTimeoutMS() != null) {
                    args.put("timeout_ms", options.getTimeoutMS());
                }
                if (options.getIframes() != null) {
                    args.put("iframes", options.getIframes());
                }
                if (options.getDomSettleTimeoutMs() != null) {
                    args.put("dom_settle_timeout_ms", options.getDomSettleTimeoutMs());
                }
                if (options.getVariables() != null) {
                    args.put("variables", options.getVariables());
                }
                if (options.getUseVision() != null) {
                    args.put("use_vision", options.getUseVision());
                }
            } else if (actionInput instanceof ObserveResult) {
                ObserveResult result = (ObserveResult) actionInput;
                // Format action like Python version
                Map<String, Object> actionDict = new HashMap<>();
                actionDict.put("method", result.getMethod());
                actionDict.put("arguments", result.getArguments());
                args.put("action", objectMapper.writeValueAsString(actionDict));
            } else {
                throw new BrowserException("Invalid action input type");
            }

            OperationResult result = callMcpTool("page_use_act", args);
            return parseActResult(result);
        } catch (Exception e) {
            logger.error("Failed to perform action", e);
            return new ActResult(false, "Failed to perform action: " + e.getMessage(), "unknown");
        }
    }

    private String formatArguments(Map<String, Object> arguments) {
        if (arguments == null || arguments.isEmpty()) {
            return "";
        }

        List<String> parts = new ArrayList<>();
        for (Map.Entry<String, Object> entry : arguments.entrySet()) {
            if (entry.getValue() instanceof String) {
                parts.add("'" + entry.getValue() + "'");
            } else {
                parts.add(entry.getValue().toString());
            }
        }
        return String.join(", ", parts);
    }

    private ActResult parseActResult(OperationResult result) {
        if (!result.isSuccess()) {
            return new ActResult(false, result.getErrorMessage(), "");
        }

        try {
            // Parse response data like Python version
            Map<String, Object> data;
            String dataStr = result.getData();
            if (dataStr != null && !dataStr.isEmpty()) {
                data = objectMapper.readValue(dataStr, new TypeReference<Map<String, Object>>(){});
            } else {
                data = new HashMap<>();
            }

            // Extract fields with same logic as Python
            boolean success = Boolean.TRUE.equals(data.get("success"));
            String message = (String) data.getOrDefault("message", "");
            String action = (String) data.getOrDefault("action", "");

            return new ActResult(success, message, action);
        } catch (Exception e) {
            logger.warn("Failed to parse act result, returning basic result", e);
            return new ActResult(false, result.getErrorMessage(), "");
        }
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
            Map<String, Object> args = new HashMap<>();
            // Use Python-compatible parameter names
            args.put("page_id", indices.pageIndex);
            args.put("context_id", indices.contextIndex);
            args.putAll(options.toMap());

            OperationResult result = callMcpTool("page_use_extract", args);
            return parseExtractResult(result, options.getSchema());
        } catch (Exception e) {
            logger.error("Failed to extract data", e);
            return new ExtractResultTuple<>(false, null);
        }
    }

    private <T> ExtractResultTuple<T> parseExtractResult(OperationResult result, Class<T> schema) {
        if (!result.isSuccess()) {
            return new ExtractResultTuple<>(false, null);
        }

        try {
            String dataStr = result.getData();
            if (dataStr != null && schema != null) {
                T extractedObject = objectMapper.readValue(dataStr, schema);
                logger.info("Extract result: {}", dataStr);
                return new ExtractResultTuple<>(true, extractedObject);
            }

            return new ExtractResultTuple<>(true, null);
        } catch (Exception e) {
            logger.warn("Failed to parse extract result", e);
            return new ExtractResultTuple<>(false, null);
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