package com.aliyun.agentbay.browser;

import com.aliyun.agentbay.exception.AgentBayException;
import com.aliyun.agentbay.exception.BrowserException;
import com.aliyun.agentbay.model.OperationResult;
import com.aliyun.agentbay.service.BaseService;
import com.aliyun.agentbay.session.Session;
import com.aliyun.agentbay.util.ResponseUtil;
import com.aliyun.wuyingai20250506.models.InitBrowserRequest;
import com.aliyun.wuyingai20250506.models.InitBrowserResponse;
import com.aliyun.wuyingai20250506.models.InitBrowserResponseBody;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.HashMap;
import java.util.Map;

/**
 * Browser provides browser-related operations for the session.
 */
public class Browser extends BaseService {
    private static final Logger logger = LoggerFactory.getLogger(Browser.class);
    private static final ObjectMapper objectMapper = new ObjectMapper();
    private static final String BROWSER_DATA_PATH = "/tmp/browser_data";

    private String endpointUrl;
    private boolean initialized;
    private BrowserOption option;
    private BrowserAgent agent;
    private Integer endpointRouterPort;

    public Browser(Session session) {
        super(session);
        this.initialized = false;
        this.agent = new BrowserAgent(session, this);
    }

    /**
     * Initialize the browser instance with the given options.
     *
     * @param option Browser initialization options
     * @return true if successful, false otherwise
     */
    public boolean initialize(BrowserOption option) {
        if (isInitialized()) {
            return true;
        }

        try {
            InitBrowserRequest request = new InitBrowserRequest();
            request.setAuthorization("Bearer " + session.getApiKey());
            request.setSessionId(session.getSessionId());
            request.setPersistentPath(BROWSER_DATA_PATH);

            // Convert BrowserOption to JSON string
            String browserOptionJson = objectMapper.writeValueAsString(option.toMap());
            request.setBrowserOption(browserOptionJson);

            InitBrowserResponse response = session.getAgentBay().getClient().initBrowser(request);

            logger.debug("Response from init_browser: {}", response);
            String requestId = ResponseUtil.extractRequestId(response);

            if (response != null && response.getBody() != null && response.getBody().getData() != null) {
                // Extract port from response using the correct data type
                InitBrowserResponseBody.InitBrowserResponseBodyData data = response.getBody().getData();
                logger.debug("Data object: {}", data);

                Integer port = data.getPort();
                logger.debug("Port from response: {}", port);

                if (port != null) {
                    this.endpointRouterPort = port;
                    this.initialized = true;
                    this.option = option;
                    logger.info("Browser instance successfully initialized with port: {}", endpointRouterPort);
                    return true;
                } else {
                    logger.warn("Port is null in response data");
                }
            }

            logger.error("Failed to initialize browser: No port in response");
            return false;

        } catch (Exception e) {
            logger.error("Failed to initialize browser instance", e);
            this.initialized = false;
            this.endpointUrl = null;
            this.option = null;
            return false;
        }
    }

    /**
     * Stop the browser instance (internal use only).
     */
    public void stopBrowser() throws BrowserException {
        if (!isInitialized()) {
            throw new BrowserException("Browser is not initialized. Cannot stop browser.");
        }

        try {
            OperationResult result = callMcpTool("stopChrome", new HashMap<>());
            if (!result.isSuccess()) {
                logger.warn("Failed to stop browser: {}", result.getErrorMessage());
            }
        } catch (Exception e) {
            logger.error("Error stopping browser", e);
            throw new BrowserException("Failed to stop browser: " + e.getMessage());
        }
    }

    /**
     * Get the endpoint URL for browser connection.
     *
     * @return Browser endpoint URL
     * @throws BrowserException if browser is not initialized
     */
    public String getEndpointUrl() throws BrowserException {
        if (!isInitialized()) {
            throw new BrowserException("Browser is not initialized. Cannot access endpoint URL.");
        }

        try {
            // Get CDP URL from session
            OperationResult linkResult = getLinkFromSession();
            if (linkResult.isSuccess()) {
                this.endpointUrl = linkResult.getData();
            } else {
                throw new BrowserException("Failed to get link from session: " + linkResult.getErrorMessage());
            }

            return this.endpointUrl;

        } catch (Exception e) {
            throw new BrowserException("Failed to get endpoint URL from session: " + e.getMessage());
        }
    }

    /**
     * Get link from session.
     */
    private OperationResult getLinkFromSession() {
        try {
            return session.getLink();
        } catch (Exception e) {
            logger.error("Failed to get link from session", e);
            return new OperationResult("", false, "", "Failed to get link from session: " + e.getMessage());
        }
    }

    /**
     * Get the current BrowserOption used to initialize the browser.
     *
     * @return BrowserOption or null if not set
     */
    public BrowserOption getOption() {
        return option;
    }

    /**
     * Check if the browser is initialized.
     *
     * @return true if initialized, false otherwise
     */
    public boolean isInitialized() {
        return initialized;
    }

    /**
     * Get the browser agent for advanced browser operations.
     *
     * @return BrowserAgent instance
     */
    public BrowserAgent getAgent() {
        return agent;
    }

    /**
     * Get the endpoint router port.
     *
     * @return Port number or null if not set
     */
    public Integer getEndpointRouterPort() {
        return endpointRouterPort;
    }
}