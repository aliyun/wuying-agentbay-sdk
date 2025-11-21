package com.aliyun.agentbay;

import com.aliyun.agentbay.client.ApiClient;
import com.aliyun.agentbay.context.ContextSync;
import com.aliyun.agentbay.exception.AgentBayException;
import com.aliyun.agentbay.exception.AuthenticationException;
import com.aliyun.agentbay.model.SessionParams;
import com.aliyun.agentbay.model.SessionResult;
import com.aliyun.agentbay.session.Session;
import com.aliyun.agentbay.session.CreateSessionParams;
import com.aliyun.agentbay.util.ResponseUtil;
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

            logger.info("AgentBay client initialized successfully");
        } catch (Exception e) {
            logger.error("Failed to initialize AgentBay client", e);
            throw new AgentBayException("Failed to initialize AgentBay client", e);
        }
    }


    /**
     * Get an existing session by ID
     *
     * @param sessionId The session ID
     * @return Session object if found, null otherwise
     */
    public Session getSession(String sessionId) {
        return sessions.get(sessionId);
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
            session.setIsVpc(params.getIsVpc() != null ? params.getIsVpc() : false);
            if (response.getBody().getData() != null) {
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
            }

            sessions.put(result.getSessionId(), session);
            result.setSession(session);

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