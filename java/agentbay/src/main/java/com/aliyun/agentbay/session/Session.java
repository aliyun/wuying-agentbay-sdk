package com.aliyun.agentbay.session;

import com.aliyun.agentbay.AgentBay;
import com.aliyun.agentbay.agent.Agent;
import com.aliyun.agentbay.browser.Browser;
import com.aliyun.agentbay.browser.BrowserOption;
import com.aliyun.agentbay.context.*;
import com.aliyun.agentbay.exception.AgentBayException;
import com.aliyun.agentbay.filesystem.FileSystem;
import com.aliyun.agentbay.model.OperationResult;
import com.aliyun.agentbay.model.SessionInfo;
import com.aliyun.agentbay.model.SessionInfoResult;
import com.aliyun.agentbay.model.SessionParams;
import com.aliyun.agentbay.oss.OSS;
import com.aliyun.agentbay.code.Code;
import com.aliyun.agentbay.command.Command;
import com.aliyun.agentbay.mcp.McpToolsResult;
import com.aliyun.agentbay.util.ResponseUtil;
import com.aliyun.wuyingai20250506.models.*;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.List;
import java.util.Map;

/**
 * Represents a session in the AgentBay cloud environment
 */
public class Session {
    private static final Logger logger = LoggerFactory.getLogger(Session.class);
    private static final ObjectMapper objectMapper = new ObjectMapper();

    private final String sessionId;
    private final AgentBay agentBay;
    private final SessionParams params;
    private Agent agent;
    private FileSystem fileSystem;
    private OSS oss;
    private Code code;
    private Command command;
    private ContextManager contextManager;
    private Browser browser;
    private String fileTransferContextId;
    private boolean isVpc;
    private String httpPort;
    private String token;
    private String vpcLinkUrl;
    private long vpcLinkUrlTimestamp;
    private java.util.List<com.aliyun.agentbay.mcp.McpTool> mcpTools;

    public Session(String sessionId, AgentBay agentBay, SessionParams params) {
        this.sessionId = sessionId;
        this.agentBay = agentBay;
        this.params = params;
        this.agent = new Agent(this);
        this.fileSystem = new FileSystem(this);
        this.oss = new OSS(this);
        this.code = new Code(this);
        this.command = new Command(this);
        this.contextManager = new ContextManager(this);
        this.browser = new Browser(this);
        this.mcpTools = new java.util.ArrayList<>();
    }

    /**
     * Constructor compatible with Python SDK style (AgentBay, sessionId)
     */
    public Session(AgentBay agentBay, String sessionId) {
        this(sessionId, agentBay, new SessionParams());
    }

    /**
     * Get the session ID
     *
     * @return Session ID
     */
    public String getSessionId() {
        return sessionId;
    }

    /**
     * Get the AgentBay client
     *
     * @return AgentBay instance
     */
    public AgentBay getAgentBay() {
        return agentBay;
    }

    /**
     * Get session parameters
     *
     * @return SessionParams
     */
    public SessionParams getParams() {
        return params;
    }

    /**
     * Get the agent for this session
     *
     * @return Agent instance
     */
    public Agent getAgent() {
        return agent;
    }

    /**
     * Get the file system for this session
     *
     * @return FileSystem instance
     */
    public FileSystem getFileSystem() {
        return fileSystem;
    }

    /**
     * Call an MCP tool
     *
     * @param toolName Tool name
     * @param args Tool arguments
     * @return CallMcpToolResponse
     * @throws AgentBayException if the call fails
     */
    public CallMcpToolResponse callTool(String toolName, Object args) throws AgentBayException {
        logger.debug("Calling tool: {} with args: {}", toolName, args);
        return agentBay.getApiClient().callMcpTool(sessionId, toolName, args);
    }

    /**
     * List available tools
     *
     * @return List of available tools
     * @throws AgentBayException if the call fails
     */
    public List<Object> listTools() throws AgentBayException {
        logger.debug("Listing tools for session: {}", sessionId);
        ListMcpToolsResponse response = agentBay.getApiClient().listMcpTools(sessionId);

        if (response != null && response.getBody() != null && response.getBody().getData() != null) {
            try {
                String dataJson = response.getBody().getData().toString();
                List<Object> toolsList = objectMapper.readValue(dataJson, List.class);
                return toolsList;
            } catch (Exception e) {
                logger.error("Failed to parse tools data from JSON: {}", e.getMessage(), e);
                throw new AgentBayException("Failed to parse tools data", e);
            }
        }
        return new java.util.ArrayList<>();
    }


    /**
     * Check if the session is active
     *
     * @return true if active, false otherwise
     */
    public boolean isActive() {
        // For now, assume session is active if it exists in our cache
        return agentBay.getSession(sessionId) != null;
    }

    /**
     * Gets information about this session
     *
     * @return SessionInfoResult containing SessionInfo and request ID
     * @throws AgentBayException if the operation fails
     */
    public SessionInfoResult info() throws AgentBayException {
        try {
            GetMcpResourceRequest request = new GetMcpResourceRequest();
            request.setAuthorization("Bearer " + agentBay.getApiKey());
            request.setSessionId(sessionId);

            logger.debug("Getting session info for session: {}", sessionId);

            GetMcpResourceResponse response = agentBay.getApiClient().getClient().getMcpResource(request);

            String requestId = ResponseUtil.extractRequestId(response);

            if (response.getBody() != null && response.getBody().getData() != null) {
                // Extract session info from response data
                GetMcpResourceResponseBody.GetMcpResourceResponseBodyData data = response.getBody().getData();

                SessionInfo sessionInfo = new SessionInfo();

                // Set session ID
                if (data.getSessionId() != null) {
                    sessionInfo.setSessionId(data.getSessionId());
                }

                // Set resource URL
                if (data.getResourceUrl() != null) {
                    sessionInfo.setResourceUrl(data.getResourceUrl());
                }

                // Transfer DesktopInfo fields to SessionInfo
                if (data.getDesktopInfo() != null) {
                    GetMcpResourceResponseBody.GetMcpResourceResponseBodyDataDesktopInfo desktopInfo = data.getDesktopInfo();

                    if (desktopInfo.getAppId() != null) {
                        sessionInfo.setAppId(desktopInfo.getAppId());
                    }
                    if (desktopInfo.getAuthCode() != null) {
                        sessionInfo.setAuthCode(desktopInfo.getAuthCode());
                    }
                    if (desktopInfo.getConnectionProperties() != null) {
                        sessionInfo.setConnectionProperties(desktopInfo.getConnectionProperties());
                    }
                    if (desktopInfo.getResourceId() != null) {
                        sessionInfo.setResourceId(desktopInfo.getResourceId());
                    }
                    if (desktopInfo.getResourceType() != null) {
                        sessionInfo.setResourceType(desktopInfo.getResourceType());
                    }
                    if (desktopInfo.getTicket() != null) {
                        sessionInfo.setTicket(desktopInfo.getTicket());
                    }
                }

                return new SessionInfoResult(requestId, true, sessionInfo, "");
            } else {
                return new SessionInfoResult(requestId, false, null, "No session data found");
            }

        } catch (Exception e) {
            logger.error("Failed to get session info for session {}", sessionId, e);
            throw new AgentBayException("Failed to get session info for session " + sessionId + ": " + e.getMessage(), e);
        }
    }

    /**
     * Get the OSS service for this session
     *
     * @return OSS instance
     */
    public OSS getOss() {
        return oss;
    }

    /**
     * Get the Code service for this session
     *
     * @return Code instance
     */
    public Code getCode() {
        return code;
    }

    /**
     * Get the Command service for this session
     *
     * @return Command instance
     */
    public Command getCommand() {
        return command;
    }

    /**
     * Get the context manager for this session
     *
     * @return ContextManager instance
     */
    public ContextManager getContext() {
        return contextManager;
    }

    /**
     * Get the browser service for this session
     *
     * @return Browser instance
     */
    public Browser getBrowser() {
        return browser;
    }

    /**
     * Get the file transfer context ID for this session
     *
     * @return File transfer context ID
     */
    public String getFileTransferContextId() {
        return fileTransferContextId;
    }

    /**
     * Set the file transfer context ID for this session
     *
     * @param fileTransferContextId File transfer context ID
     */
    public void setFileTransferContextId(String fileTransferContextId) {
        this.fileTransferContextId = fileTransferContextId;
    }

    /**
     * Initialize browser instance with the given options
     * This calls the AgentBay cloud service to create a browser instance
     */
    public OperationResult initializeBrowser(BrowserOption option) throws AgentBayException {
        try {
            InitBrowserRequest request = new InitBrowserRequest();
            request.setAuthorization("Bearer " + getApiKey());
            request.setSessionId(sessionId);
            request.setPersistentPath("/tmp/browser_data");  // Default path
            try {
                com.fasterxml.jackson.databind.ObjectMapper objectMapper = new com.fasterxml.jackson.databind.ObjectMapper();
                request.setBrowserOption(objectMapper.writeValueAsString(option.toMap()));
            } catch (Exception e) {
                throw new AgentBayException("Failed to serialize browser option: " + e.getMessage());
            }

            InitBrowserResponse response = agentBay.getClient().initBrowser(request);

            if (response == null || response.getBody() == null) {
                return new OperationResult("", false, "", "Invalid response from init browser API");
            }

            InitBrowserResponseBody.InitBrowserResponseBodyData data = response.getBody().getData();
            if (data != null && data.getPort() != null) {
                logger.info("Browser initialized successfully with port: {}", data.getPort());
                return new OperationResult(
                    ResponseUtil.extractRequestId(response),
                    true,
                    "Browser initialized",
                    ""
                );
            } else {
                return new OperationResult("", false, "", "Failed to get browser port from response");
            }
        } catch (Exception e) {
            logger.error("Failed to initialize browser", e);
            return new OperationResult("", false, "", "Failed to initialize browser: " + e.getMessage());
        }
    }

    /**
     * Get the API key for this session
     *
     * @return API key
     */
    public String getApiKey() {
        return agentBay.getApiKey();
    }

    /**
     * List MCP tools for this session
     *
     * @return McpToolsResult
     */
    public McpToolsResult listMcpTools() {
        try {
            List<Object> toolsData = listTools();
            McpToolsResult result = new McpToolsResult();
            result.setSuccess(true);

            java.util.List<com.aliyun.agentbay.mcp.McpTool> tools = new java.util.ArrayList<>();
            if (toolsData != null) {
                for (Object toolData : toolsData) {
                    try {
                        if (toolData instanceof Map) {
                            @SuppressWarnings("unchecked")
                            Map<String, Object> toolMap = (Map<String, Object>) toolData;

                            com.aliyun.agentbay.mcp.McpTool tool = new com.aliyun.agentbay.mcp.McpTool();
                            tool.setName((String) toolMap.get("name"));
                            tool.setDescription((String) toolMap.get("description"));
                            @SuppressWarnings("unchecked")
                            Map<String, Object> inputSchema = (Map<String, Object>) toolMap.get("inputSchema");
                            tool.setInputSchema(inputSchema);
                            tool.setServer((String) toolMap.get("server"));
                            tool.setTool((String) toolMap.get("tool"));
                            tools.add(tool);
                        } else if (toolData instanceof String) {
                            @SuppressWarnings("unchecked")
                            Map<String, Object> toolMap = objectMapper.readValue((String) toolData, Map.class);

                            com.aliyun.agentbay.mcp.McpTool tool = new com.aliyun.agentbay.mcp.McpTool();
                            tool.setName((String) toolMap.get("name"));
                            tool.setDescription((String) toolMap.get("description"));
                            @SuppressWarnings("unchecked")
                            Map<String, Object> inputSchema = (Map<String, Object>) toolMap.get("inputSchema");
                            tool.setInputSchema(inputSchema);
                            tool.setServer((String) toolMap.get("server"));
                            tool.setTool((String) toolMap.get("tool"));
                            tools.add(tool);
                        }
                    } catch (Exception e) {
                        logger.warn("Failed to parse tool data: {}", toolData, e);
                    }
                }
            }

            this.mcpTools = tools;

            result.setTools(tools);
            return result;
        } catch (AgentBayException e) {
            McpToolsResult result = new McpToolsResult();
            result.setSuccess(false);
            result.setErrorMessage(e.getMessage());
            return result;
        }
    }

    /**
     * Set image ID for this session (placeholder method)
     */
    public void setImageId(String imageId) {
        // TODO: Implement set image ID
    }

    /**
     * Check if VPC mode is enabled for this session
     *
     * @return true if VPC is enabled, false otherwise
     */
    public boolean isVpcEnabled() {
        return isVpc;
    }

    /**
     * Set VPC mode for this session
     *
     * @param isVpc true to enable VPC mode, false otherwise
     */
    public void setIsVpc(boolean isVpc) {
        this.isVpc = isVpc;
    }

    /**
     * Get the HTTP port for VPC mode
     *
     * @return HTTP port
     */
    public String getHttpPort() {
        return httpPort;
    }

    /**
     * Set the HTTP port for VPC mode
     *
     * @param httpPort HTTP port
     */
    public void setHttpPort(String httpPort) {
        this.httpPort = httpPort;
    }

    /**
     * Get the token for VPC mode
     *
     * @return Token
     */
    public String getToken() {
        return token;
    }

    /**
     * Set the token for VPC mode
     *
     * @param token Token
     */
    public void setToken(String token) {
        this.token = token;
    }

    /**
     * Get MCP tools list for this session
     *
     * @return List of MCP tools
     */
    public java.util.List<com.aliyun.agentbay.mcp.McpTool> getMcpTools() {
        return mcpTools;
    }

    /**
     * Set MCP tools list for this session
     *
     * @param mcpTools List of MCP tools
     */
    public void setMcpTools(java.util.List<com.aliyun.agentbay.mcp.McpTool> mcpTools) {
        this.mcpTools = mcpTools;
    }

    /**
     * Find the server that provides a given tool
     *
     * @param toolName Tool name
     * @return Server name, or empty string if not found
     */
    public String findServerForTool(String toolName) {
        if (mcpTools == null) {
            return "";
        }
        for (com.aliyun.agentbay.mcp.McpTool tool : mcpTools) {
            if (tool.getName() != null && tool.getName().equals(toolName)) {
                return tool.getServer() != null ? tool.getServer() : "";
            }
        }
        return "";
    }

    /**
     * Get the cached VPC link URL for VPC sessions.
     * Automatically refreshes if older than 9 minutes.
     *
     * @return Cached VPC link URL or null if not available
     */
    public String getVpcLinkUrl() {
        if (vpcLinkUrl != null) {
            long currentTime = System.currentTimeMillis();
            long elapsedMinutes = (currentTime - vpcLinkUrlTimestamp) / (60 * 1000);

            if (elapsedMinutes >= 1) {
                logger.info("VPC link URL expired ({} minutes old), refreshing...", elapsedMinutes);
                updateVpcLinkUrl();
            }
        }
        return vpcLinkUrl;
    }

    /**
     * Update the cached VPC link URL based on current networkInterfaceIp and httpPort
     */
    public void updateVpcLinkUrl() {
        if (isVpc && httpPort != null) {
            try {
                Integer port = Integer.parseInt(httpPort);
                OperationResult linkResult = getLink("https", port);
                if (linkResult.isSuccess() && linkResult.getData() != null) {
                    this.vpcLinkUrl = linkResult.getData();
                    this.vpcLinkUrlTimestamp = System.currentTimeMillis();
                    logger.info("VPC link URL cached: {}", vpcLinkUrl);
                }
            } catch (Exception e) {
                logger.warn("Failed to update VPC link URL: {}", e.getMessage());
            }
        }
    }

    /**
     * Get a link associated with the current session
     *
     * @param protocolType The protocol type to use for the link (optional)
     * @param port The port to use for the link (optional)
     * @return OperationResult containing the link URL
     * @throws AgentBayException if the request fails
     */
    public OperationResult getLink(String protocolType, Integer port) throws AgentBayException {
        try {
            GetLinkRequest request = new GetLinkRequest();
            request.setAuthorization("Bearer " + getApiKey());
            request.setSessionId(sessionId);
            if (protocolType != null) {
                request.setProtocolType(protocolType);
            }
            if (port != null) {
                request.setPort(port);
            }

            GetLinkResponse response = agentBay.getClient().getLink(request);
            String requestId = ResponseUtil.extractRequestId(response);

            if (response != null && response.getBody() != null && response.getBody().getData() != null) {
                String url = response.getBody().getData().getUrl();
                return new OperationResult(requestId, true, url, "");
            } else {
                return new OperationResult(requestId, false, "", "No URL in response");
            }
        } catch (Exception e) {
            logger.error("Failed to get link for session {}: {}", sessionId, e.getMessage());
            throw new AgentBayException("Failed to get link: " + e.getMessage(), e);
        }
    }

    /**
     * Get a link associated with the current session with default parameters
     *
     * @return OperationResult containing the link URL
     * @throws AgentBayException if the request fails
     */
    public OperationResult getLink() throws AgentBayException {
        return getLink(null, null);
    }

    /**
     * Dump session state to a JSON string for persistence
     *
     * @return JSON string containing session state
     * @throws AgentBayException if serialization fails
     */
    public String dumpState() throws AgentBayException {
        try {
            SessionState state = new SessionState();
            state.setSessionId(this.sessionId);
            state.setFileTransferContextId(this.fileTransferContextId);
            state.setVpc(this.isVpc);
            state.setHttpPort(this.httpPort);
            state.setToken(this.token);
            state.setVpcLinkUrl(this.vpcLinkUrl);
            state.setVpcLinkUrlTimestamp(this.vpcLinkUrlTimestamp);
            state.setMcpTools(this.mcpTools);

            return objectMapper.writeValueAsString(state);
        } catch (Exception e) {
            logger.error("Failed to dump session state", e);
            throw new AgentBayException("Failed to dump session state: " + e.getMessage(), e);
        }
    }

    /**
     * Restore session from a JSON state string
     *
     * @param agentBay AgentBay client instance
     * @param stateJson JSON string containing session state
     * @return Restored Session object
     * @throws AgentBayException if deserialization or restoration fails
     */
    public static Session restoreState(AgentBay agentBay, String stateJson) throws AgentBayException {
        try {
            SessionState state = objectMapper.readValue(stateJson, SessionState.class);

            Session session = new Session(state.getSessionId(), agentBay, new SessionParams());

            session.setFileTransferContextId(state.getFileTransferContextId());
            session.setIsVpc(state.isVpc());
            session.setHttpPort(state.getHttpPort());
            session.setToken(state.getToken());
            session.setMcpTools(state.getMcpTools());
            session.vpcLinkUrl = state.getVpcLinkUrl();
            session.vpcLinkUrlTimestamp = state.getVpcLinkUrlTimestamp();

            logger.info("Session state restored successfully: {}", state.getSessionId());
            return session;
        } catch (Exception e) {
            logger.error("Failed to restore session state", e);
            throw new AgentBayException("Failed to restore session state: " + e.getMessage(), e);
        }
    }

    /**
     * Delete this session
     *
     * @return DeleteResult
     */
    public com.aliyun.agentbay.model.DeleteResult delete() {
        return delete(false);
    }

    /**
     * Delete this session with optional sync context
     *
     * @param syncContext Whether to sync context before deletion
     * @return DeleteResult
     */
    public com.aliyun.agentbay.model.DeleteResult delete(boolean syncContext) {
        try {
            // If sync_context is True, trigger file uploads first
            if (syncContext) {
                logger.info("Context synchronization before session deletion");

                // Trigger file upload
                try {
                    ContextSyncResult syncResult = contextManager.sync();
                    if (!syncResult.isSuccess()) {
                        logger.warn("Context sync operation returned failure status");
                    }
                } catch (Exception e) {
                    logger.warn("Failed to trigger context sync: {}", e.getMessage());
                    // Continue with deletion even if sync fails
                }

                // Wait for uploads to complete
                int maxRetries = 150; // Maximum number of retries
                int retryInterval = 2000; // 2 seconds in milliseconds

                for (int retry = 0; retry < maxRetries; retry++) {
                    try {
                        // Get context status data
                        ContextInfoResult infoResult = contextManager.info();

                        // Check if all upload context items have status "Success" or "Failed"
                        boolean allCompleted = true;
                        boolean hasFailure = false;
                        boolean hasUploads = false;

                        for (ContextStatusData item : infoResult.getContextStatusData()) {
                            // We only care about upload tasks
                            if (!"upload".equals(item.getTaskType())) {
                                continue;
                            }

                            hasUploads = true;
                            logger.info("Upload context {} status: {}, path: {}",
                                       item.getContextId(), item.getStatus(), item.getPath());

                            if (!"Success".equals(item.getStatus()) && !"Failed".equals(item.getStatus())) {
                                allCompleted = false;
                                break;
                            }

                            if ("Failed".equals(item.getStatus())) {
                                hasFailure = true;
                                logger.error("Upload failed for context {}: {}",
                                           item.getContextId(), item.getErrorMessage());
                            }
                        }

                        if (allCompleted || !hasUploads) {
                            if (hasFailure) {
                                logger.warn("Context upload completed with failures");
                            } else if (hasUploads) {
                                logger.info("Context upload completed successfully");
                            } else {
                                logger.info("No upload tasks found");
                            }
                            break;
                        }

                        logger.info("Waiting for context upload to complete, attempt {}/{}", retry + 1, maxRetries);
                        Thread.sleep(retryInterval);
                    } catch (Exception e) {
                        logger.error("Error checking context status on attempt {}: {}", retry + 1, e.getMessage());
                        try {
                            Thread.sleep(retryInterval);
                        } catch (InterruptedException ie) {
                            Thread.currentThread().interrupt();
                            break;
                        }
                    }
                }
            }

            // Proceed with session deletion
            ReleaseMcpSessionRequest request = new ReleaseMcpSessionRequest();
            request.setAuthorization("Bearer " + getApiKey());
            request.setSessionId(sessionId);

            ReleaseMcpSessionResponse response = agentBay.getClient().releaseMcpSession(request);

            String requestId = ResponseUtil.extractRequestId(response);

            // Check if the response is successful
            boolean success = true;
            if (response != null && response.getBody() != null) {
                success = response.getBody().getSuccess() != null ? response.getBody().getSuccess() : true;
            }

            if (!success) {
                return new com.aliyun.agentbay.model.DeleteResult(
                    requestId, false, "Failed to delete session");
            }

            logger.info("Session deleted successfully: {}", sessionId);
            return new com.aliyun.agentbay.model.DeleteResult(requestId, true, "");

        } catch (Exception e) {
            logger.error("Failed to delete session {}: {}", sessionId, e.getMessage());
            return new com.aliyun.agentbay.model.DeleteResult(
                "", false, "Failed to delete session " + sessionId + ": " + e.getMessage());
        }
    }

    @Override
    public String toString() {
        return "Session{" +
                "sessionId='" + sessionId + '\'' +
                ", params=" + params +
                '}';
    }
}