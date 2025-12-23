package com.aliyun.agentbay;

import com.aliyun.agentbay.browser.BrowserContext;
import com.aliyun.agentbay.client.ApiClient;
import com.aliyun.agentbay.context.*;
import com.aliyun.agentbay.exception.AgentBayException;
import com.aliyun.agentbay.exception.AuthenticationException;
import com.aliyun.agentbay.mobile.MobileSimulate;
import com.aliyun.agentbay.model.GetSessionData;
import com.aliyun.agentbay.model.GetSessionResult;
import com.aliyun.agentbay.model.SessionParams;
import com.aliyun.agentbay.model.SessionResult;
import com.aliyun.agentbay.session.Session;
import com.aliyun.agentbay.session.CreateSessionParams;
import com.aliyun.agentbay.util.ResponseUtil;
import com.aliyun.agentbay.util.Version;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.aliyun.teaopenapi.models.Config;
import com.aliyun.wuyingai20250506.Client;
import com.aliyun.wuyingai20250506.models.CreateMcpSessionRequest;
import com.aliyun.wuyingai20250506.models.CreateMcpSessionResponse;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.concurrent.ConcurrentHashMap;

/**
 * Main client for interacting with the AgentBay cloud runtime environment
 */
public class AgentBay {
    private static final Logger logger = LoggerFactory.getLogger(AgentBay.class);
    private static final ObjectMapper objectMapper = new ObjectMapper();

    private String apiKey;
    private String regionId;
    private Client client;
    private ApiClient apiClient;
    private ConcurrentHashMap<String, Session> sessions;
    private MobileSimulate mobileSimulate;

    public AgentBay(String apiKey) throws AgentBayException {
        this(apiKey, new com.aliyun.agentbay.Config());
    }

    public AgentBay(String apiKey, com.aliyun.agentbay.Config config) throws AgentBayException {
        if (apiKey == null || apiKey.trim().isEmpty()) {
            apiKey = System.getenv("AGENTBAY_API_KEY");
            if (apiKey == null || apiKey.trim().isEmpty()) {
                throw new AuthenticationException(
                    "API key is required. Provide it as a parameter or set the " +
                    "AGENTBAY_API_KEY environment variable"
                );
            }
        }

        this.apiKey = apiKey;
        this.regionId = config.getRegionId();
        this.sessions = new ConcurrentHashMap<>();

        try {
            // Initialize the OpenAPI client
            Config clientConfig = new Config();
            clientConfig.setEndpoint(config.getEndpoint());
            clientConfig.setAccessKeyId("Bearer");
            clientConfig.setAccessKeySecret(apiKey);
            clientConfig.setReadTimeout(config.getTimeoutMs());
            clientConfig.setConnectTimeout(config.getTimeoutMs());

            this.client = new Client(clientConfig);
            this.apiClient = new ApiClient(this.client, apiKey);
            this.mobileSimulate = new MobileSimulate(this);

            logger.info("AgentBay client initialized successfully");
        } catch (Exception e) {
            logger.error("Failed to initialize AgentBay client", e);
            throw new AgentBayException("Failed to initialize AgentBay client", e);
        }
    }


    /**
     * Get an existing session by ID from local cache only.
     * This method only retrieves sessions from the local cache (sessions created by this AgentBay instance).
     * It does not fetch sessions from the server.
     *
     * @param sessionId The session ID
     * @return Session object if found in cache, null otherwise
     */
    public Session getSession(String sessionId) {
        return sessions.get(sessionId);
    }

    /**
     * Get session information by session ID from remote server.
     * This method retrieves detailed session metadata from the API without creating a Session object.
     *
     * @param sessionId The ID of the session to retrieve
     * @return GetSessionResult containing session information
     */
    public GetSessionResult getSessionInfo(String sessionId) {
        try {
            logger.debug("Getting session information for session: {}", sessionId);

            com.aliyun.wuyingai20250506.models.GetSessionRequest request = 
                new com.aliyun.wuyingai20250506.models.GetSessionRequest();
            request.setAuthorization("Bearer " + apiKey);
            request.setSessionId(sessionId);

            com.aliyun.wuyingai20250506.models.GetSessionResponse response = client.getSession(request);

            String requestId = ResponseUtil.extractRequestId(response);

            if (response == null || response.getBody() == null) {
                return new GetSessionResult(
                    requestId,
                    false,
                    null,
                    "Invalid response from GetSession API"
                );
            }

            com.aliyun.wuyingai20250506.models.GetSessionResponseBody body = response.getBody();
            Boolean success = body.getSuccess();
            String code = body.getCode();
            String message = body.getMessage();

            // Check for API-level errors
            if (success == null || !success) {
                String errorMsg = message != null ? message : "Unknown error";
                if (code != null) {
                    errorMsg = "[" + code + "] " + errorMsg;
                }
                return new GetSessionResult(
                    requestId,
                    false,
                    null,
                    errorMsg
                );
            }

            // Extract session data
            GetSessionData data = null;
            if (body.getData() != null) {
                com.aliyun.wuyingai20250506.models.GetSessionResponseBody.GetSessionResponseBodyData responseData = 
                    body.getData();
                data = new GetSessionData(
                    responseData.getSessionId(),
                    responseData.getAppInstanceId(),
                    responseData.getResourceId(),
                    responseData.getResourceUrl(),
                    responseData.getVpcResource() != null ? responseData.getVpcResource() : false,
                    responseData.getNetworkInterfaceIp(),
                    responseData.getHttpPort(),
                    responseData.getToken(),
                    body.getCode() != null ? body.getCode() : ""
                );
            }

            return new GetSessionResult(
                requestId,
                true,
                data,
                ""
            );

        } catch (com.aliyun.tea.TeaException e) {
            String errorStr = e.getMessage();
            String requestId = "";
            if (e.getData() != null && e.getData().get("RequestId") != null) {
                requestId = e.getData().get("RequestId").toString();
            }

            // Check if this is an expected business error (e.g., session not found)
            if (errorStr != null && (errorStr.contains("InvalidMcpSession.NotFound") || 
                                     errorStr.contains("NotFound"))) {
                logger.info("Session not found: {}", sessionId);
                return new GetSessionResult(
                    requestId,
                    false,
                    null,
                    "Session " + sessionId + " not found"
                );
            } else {
                logger.error("Error calling GetSession API for session: {}", sessionId, e);
                return new GetSessionResult(
                    requestId,
                    false,
                    null,
                    "Failed to get session " + sessionId + ": " + errorStr
                );
            }
        } catch (Exception e) {
            logger.error("Unexpected error calling GetSession API for session: {}", sessionId, e);
            return new GetSessionResult(
                "",
                false,
                null,
                "Failed to get session " + sessionId + ": " + e.getMessage()
            );
        }
    }

    /**
     * Get a session by its ID from remote server.
     * This method calls the GetSession API to retrieve session information and creates a Session object.
     * Unlike getSession(), this method fetches from the remote server, enabling session recovery scenarios.
     *
     * @param sessionId The ID of the session to retrieve. Must be a non-empty string.
     * @return SessionResult containing the Session instance, request ID, and success status.
     * @throws AgentBayException if the API request fails
     */
    public SessionResult get(String sessionId) throws AgentBayException {
        // Validate input
        if (sessionId == null || sessionId.trim().isEmpty()) {
            SessionResult result = new SessionResult();
            result.setSuccess(false);
            result.setErrorMessage("session_id is required");
            result.setRequestId("");
            return result;
        }

        // Call GetSession API
        GetSessionResult getResult = getSessionInfo(sessionId);

        // Check if the API call was successful
        if (!getResult.isSuccess()) {
            String errorMsg = getResult.getErrorMessage() != null ? getResult.getErrorMessage() : "Unknown error";
            SessionResult result = new SessionResult();
            result.setSuccess(false);
            result.setErrorMessage("Failed to get session " + sessionId + ": " + errorMsg);
            result.setRequestId(getResult.getRequestId());
            return result;
        }

        // Create the Session object
        Session session = new Session(sessionId, this, new SessionParams());

        // Set ResourceUrl from GetSession response
        if (getResult.getData() != null) {
            GetSessionData data = getResult.getData();
            session.setResourceUrl(data.getResourceUrl());
            
            // TODO: VPC functionality temporarily disabled
            /*
            if (data.isVpcResource()) {
                session.setHttpPort(data.getHttpPort());
                session.setToken(data.getToken());
                session.setNetworkInterfaceIp(data.getNetworkInterfaceIp());
            }
            */
        }

        // Create a default context for file transfer operations for the recovered session
        try {
            String contextName = "file-transfer-context-" + System.currentTimeMillis() / 1000;
            com.aliyun.agentbay.context.ContextResult contextResult = 
                getContextService().get(contextName, true);
            if (contextResult.isSuccess() && contextResult.getContext() != null) {
                session.setFileTransferContextId(contextResult.getContext().getContextId());
                logger.info("Created file transfer context for recovered session: {}", 
                           contextResult.getContext().getContextId());
            } else {
                logger.warn("Failed to create file transfer context for recovered session: {}", 
                           contextResult.getErrorMessage() != null ? contextResult.getErrorMessage() : "Unknown error");
            }
        } catch (Exception e) {
            logger.warn("Failed to create file transfer context for recovered session: {}", e.getMessage());
        }

        SessionResult result = new SessionResult();
        result.setRequestId(getResult.getRequestId());
        result.setSuccess(true);
        result.setSession(session);
        return result;
    }

    /**
     * Remove a session from the cache
     *
     * @param sessionId The session ID to remove
     */
    public void removeSession(String sessionId) {
        sessions.remove(sessionId);
        logger.info("Session removed from cache: {}", sessionId);
    }

    /**
     * Get the API client
     *
     * @return ApiClient instance
     */
    public ApiClient getApiClient() {
        return apiClient;
    }

    /**
     * Get the underlying OpenAPI client
     *
     * @return Client instance
     */
    public Client getClient() {
        return client;
    }

    /**
     * Get the API key
     *
     * @return The API key
     */
    public String getApiKey() {
        return apiKey;
    }

    /**
     * Get the region ID
     *
     * @return The region ID
     */
    public String getRegionId() {
        return regionId;
    }

    /**
     * Create a new session with CreateSessionParams
     *
     * @param params Parameters for creating the session
     * @return SessionResult containing the created session information
     * @throws AgentBayException if the session creation fails
     */
    public SessionResult create(CreateSessionParams params) throws AgentBayException {
        try {
            if (params == null) {
                params = new CreateSessionParams();
            }

            logger.info("Creating new session with params");

            CreateMcpSessionRequest request = new CreateMcpSessionRequest();
            request.authorization = "Bearer " + apiKey;

            // Handle context syncs
            if (params.getContextSyncs() != null && !params.getContextSyncs().isEmpty()) {
                List<CreateMcpSessionRequest.CreateMcpSessionRequestPersistenceDataList> persistenceDataList =
                    new ArrayList<>();

                for (ContextSync cs : params.getContextSyncs()) {
                    String policyJson = null;
                    if (cs.getPolicy() != null) {
                        try {
                            // Convert policy to Map first, then to JSON
                            Map<String, Object> policyMap = cs.getPolicy().toMap();
                            policyJson = objectMapper.writeValueAsString(policyMap);
                        } catch (Exception e) {
                            logger.warn("Failed to serialize policy to JSON: {}", e.getMessage());
                        }
                    }

                    CreateMcpSessionRequest.CreateMcpSessionRequestPersistenceDataList persistenceData =
                        new CreateMcpSessionRequest.CreateMcpSessionRequestPersistenceDataList();
                    persistenceData.setContextId(cs.getContextId());
                    persistenceData.setPath(cs.getPath());
                    persistenceData.setPolicy(policyJson);

                    persistenceDataList.add(persistenceData);
                }

                request.setPersistenceDataList(persistenceDataList);
                logger.debug("Added {} context sync configurations", persistenceDataList.size());
            }

            // Add BrowserContext as a ContextSync if provided
            if (params.getBrowserContext() != null) {
                BrowserContext browserContext = params.getBrowserContext();
                
                // Create a new SyncPolicy with default values for browser context
                UploadPolicy uploadPolicy = new UploadPolicy(
                    browserContext.isAutoUpload(),
                    UploadStrategy.UPLOAD_BEFORE_RESOURCE_RELEASE,
                    30
                );
                
                // Create BWList with white lists for browser data paths
                List<WhiteList> whiteLists = new ArrayList<>();
                whiteLists.add(new WhiteList("/Local State", new ArrayList<>()));
                whiteLists.add(new WhiteList("/Default/Cookies", new ArrayList<>()));
                whiteLists.add(new WhiteList("/Default/Cookies-journal", new ArrayList<>()));
                BWList bwList = new BWList(whiteLists);
                
                SyncPolicy syncPolicy = new SyncPolicy(
                    uploadPolicy,
                    DownloadPolicy.defaultPolicy(),
                    DeletePolicy.defaultPolicy(),
                    ExtractPolicy.defaultPolicy(),
                    RecyclePolicy.defaultPolicy(),
                    bwList
                );
                
                // Serialize the sync_policy to JSON
                String policyJson = null;
                try {
                    Map<String, Object> policyMap = syncPolicy.toMap();
                    policyJson = objectMapper.writeValueAsString(policyMap);
                } catch (Exception e) {
                    logger.warn("Failed to serialize browser context policy to JSON: {}", e.getMessage());
                }
                
                // Create browser context sync item
                CreateMcpSessionRequest.CreateMcpSessionRequestPersistenceDataList browserContextSync =
                    new CreateMcpSessionRequest.CreateMcpSessionRequestPersistenceDataList();
                browserContextSync.setContextId(browserContext.getContextId());
                browserContextSync.setPath(com.aliyun.agentbay.Config.BROWSER_DATA_PATH);
                browserContextSync.setPolicy(policyJson);
                
                // Add to persistence data list or create new one if not exists
                if (request.getPersistenceDataList() == null) {
                    request.setPersistenceDataList(new ArrayList<>());
                }
                request.getPersistenceDataList().add(browserContextSync);
                
                logger.info("Added browser context to persistence_data_list. Total items: {}", 
                          request.getPersistenceDataList().size());
                for (int i = 0; i < request.getPersistenceDataList().size(); i++) {
                    CreateMcpSessionRequest.CreateMcpSessionRequestPersistenceDataList item = 
                        request.getPersistenceDataList().get(i);
                    logger.info("persistence_data_list[{}]: context_id={}, path={}, policy_length={}", 
                              i, item.getContextId(), item.getPath(), 
                              item.getPolicy() != null ? item.getPolicy().length() : 0);
                    logger.debug("persistence_data_list[{}] policy content: {}", i, item.getPolicy());
                }
            }

            // Set image ID if provided
            if (params.getImageId() != null) {
                request.setImageId(params.getImageId());
            }
            // Set labels if provided
            if (params.getLabels() != null && !params.getLabels().isEmpty()) {
                try {
                    String labelsJson = objectMapper.writeValueAsString(params.getLabels());
                    request.setLabels(labelsJson);
                    logger.debug("Added labels: {}", labelsJson);
                } catch (Exception e) {
                    logger.warn("Failed to serialize labels to JSON: {}", e.getMessage());
                }
            }

            // Add SDK stats for tracking
            String framework = params.getFramework() != null ? params.getFramework() : "";
            String sdkStatsJson = String.format(
                "{\"source\":\"sdk\",\"sdk_language\":\"%s\",\"sdk_version\":\"%s\",\"is_release\":%s,\"framework\":\"%s\"}",
                Version.getSdkLanguage(),
                Version.getVersionString(),
                Version.isRelease(),
                framework
            );
            request.setSdkStats(sdkStatsJson);
            logger.debug("Added SDK stats: {}", sdkStatsJson);

            CreateMcpSessionResponse response = client.createMcpSession(request);

            if (response == null || response.getBody() == null) {
                String requestId = response != null ? ResponseUtil.extractRequestId(response) : "";
                SessionResult result = new SessionResult();
                result.setSuccess(false);
                result.setErrorMessage("Invalid response from create session API");
                result.setRequestId(requestId);
                return result;
            }

            SessionResult result = new SessionResult();

            // Extract session ID from response data
            String sessionId = null;
            if (response.getBody().getData() != null) {
                // The getData() returns the session data object, we need to extract SessionId
                try {
                    sessionId = response.getBody().getData().getSessionId();
                } catch (Exception e) {
                    logger.warn("Failed to extract session ID directly, trying alternative approach", e);
                    sessionId = response.getBody().getData().toString();
                }
            }

            if (sessionId == null || sessionId.isEmpty()) {
                String requestId = ResponseUtil.extractRequestId(response);
                result.setSuccess(false);
                result.setErrorMessage("SessionId not found in response");
                result.setRequestId(requestId);
                return result;
            }

            result.setSessionId(sessionId);
            result.setStatus("created");
            result.setRequestId(ResponseUtil.extractRequestId(response));
            result.setBrowserType(params.getBrowserType());
            result.setSuccess(true);

            // Create and cache the session
            SessionParams sessionParams = new SessionParams();
            sessionParams.setBrowserType(params.getBrowserType());
            Session session = new Session(result.getSessionId(), this, sessionParams);

            // Set VPC-related fields if this is a VPC session
            /*if (response.getBody().getData() != null) {
                boolean vpcResource = (response.getBody().getData().getHttpPort() != null && !response.getBody().getData().getHttpPort().isEmpty());
                if (vpcResource) {
                    session.setHttpPort(response.getBody().getData().getHttpPort());
                    session.updateVpcLinkUrl();
                    session.setToken(response.getBody().getData().getToken());
                    logger.info("session created with http Port: {}", session.getHttpPort());
                    try {
                        session.listMcpTools();
                        logger.info("Successfully fetched MCP tools for VPC session");
                    } catch (Exception e) {
                        logger.warn("Failed to fetch MCP tools for VPC session: {}", e.getMessage());
                    }
                }
            }*/

            sessions.put(result.getSessionId(), session);
            result.setSession(session);

            // If we have persistence data, wait for context synchronization
            boolean needsContextSync = (params.getContextSyncs() != null && !params.getContextSyncs().isEmpty()) ||
                                      (params.getBrowserContext() != null);
            if (needsContextSync) {
                waitForContextSynchronization(session);
            }

            logger.info("Session created successfully: {}", result.getSessionId());
            return result;
        } catch (Exception e) {
            logger.error("Failed to create session", e);
            SessionResult result = new SessionResult();
            result.setSuccess(false);
            result.setErrorMessage(e.getMessage());
            // Try to extract requestId if exception has it (for ClientException cases)
            if (e instanceof com.aliyun.tea.TeaException) {
                com.aliyun.tea.TeaException teaException = (com.aliyun.tea.TeaException) e;
                if (teaException.getData() != null && teaException.getData().get("RequestId") != null) {
                    result.setRequestId(teaException.getData().get("RequestId").toString());
                }
            }
            return result;
        }
    }

    /**
     * Wait for context synchronization to complete
     *
     * @param session The session to wait for context synchronization
     */
    private void waitForContextSynchronization(Session session) {
        logger.info("Waiting for context synchronization to complete");

        // Wait for context synchronization to complete
        int maxRetries = 150; // Maximum number of retries
        int retryInterval = 2000; // 2 seconds in milliseconds

        for (int retry = 0; retry < maxRetries; retry++) {
            try {
                // Get context status data
                com.aliyun.agentbay.context.ContextInfoResult infoResult = session.getContext().info();

                // Check if all context items have status "Success" or "Failed"
                boolean allCompleted = true;
                boolean hasFailure = false;

                for (com.aliyun.agentbay.context.ContextStatusData item : infoResult.getContextStatusData()) {
                    logger.info("Context {} status: {}, path: {}",
                               item.getContextId(), item.getStatus(), item.getPath());

                    if (!"Success".equals(item.getStatus()) && !"Failed".equals(item.getStatus())) {
                        allCompleted = false;
                        break;
                    }

                    if ("Failed".equals(item.getStatus())) {
                        hasFailure = true;
                        logger.error("Context synchronization failed for {}: {}",
                                   item.getContextId(), item.getErrorMessage());
                    }
                }

                if (allCompleted || infoResult.getContextStatusData().isEmpty()) {
                    if (hasFailure) {
                        logger.warn("Context synchronization completed with failures");
                    } else {
                        logger.info("Context synchronization completed successfully");
                    }
                    break;
                }

                logger.debug("Waiting for context synchronization, attempt {}/{}", retry + 1, maxRetries);
                Thread.sleep(retryInterval);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                logger.warn("Context synchronization wait interrupted");
                break;
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

    /**
     * Get context service for this AgentBay instance
     *
     * @return ContextService instance
     */
    public com.aliyun.agentbay.context.ContextService getContextService() {
        return new com.aliyun.agentbay.context.ContextService(this);
    }

    /**
     * Get context service for this AgentBay instance (alias for getContextService)
     *
     * @return ContextService instance
     */
    public com.aliyun.agentbay.context.ContextService getContext() {
        return getContextService();
    }

    /**
     * Get mobile simulate service for this AgentBay instance
     *
     * @return MobileSimulate instance
     */
    public MobileSimulate getMobileSimulate() {
        return mobileSimulate;
    }

    /**
     * Delete a session
     *
     * @param session The session to delete
     * @param syncContext Whether to sync context before deletion
     * @return DeleteResult
     */
    public com.aliyun.agentbay.model.DeleteResult delete(Session session, boolean syncContext) {
        if (session == null) {
            return new com.aliyun.agentbay.model.DeleteResult("", false, "Session is null");
        }

        com.aliyun.agentbay.model.DeleteResult result = session.delete(syncContext);

        // Remove from sessions map
        sessions.remove(session.getSessionId());

        return result;
    }

}