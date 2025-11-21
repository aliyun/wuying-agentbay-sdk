package com.aliyun.agentbay.context;

import com.aliyun.agentbay.session.Session;
import com.aliyun.agentbay.model.ApiResponse;
import com.aliyun.agentbay.util.ResponseUtil;
import com.aliyun.wuyingai20250506.models.*;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

public class ContextManager {
    private static final Logger logger = LoggerFactory.getLogger(ContextManager.class);
    private static final ObjectMapper objectMapper = new ObjectMapper();

    private final Session session;

    public ContextManager(Session session) {
        this.session = session;
    }

    /**
     * Get context info for the session
     */
    public ContextInfoResult info() {
        return info(null, null, null);
    }

    /**
     * Get context info with optional filters
     *
     * @param contextId Context ID filter (optional)
     * @param path Path filter (optional)
     * @param taskType Task type filter (optional)
     * @return ContextInfoResult containing status data
     */
    public ContextInfoResult info(String contextId, String path, String taskType) {
        try {
            GetContextInfoRequest request = new GetContextInfoRequest();
            request.setAuthorization("Bearer " + session.getApiKey());
            request.setSessionId(session.getSessionId());

            if (contextId != null) {
                request.setContextId(contextId);
            }
            if (path != null) {
                request.setPath(path);
            }
            if (taskType != null) {
                request.setTaskType(taskType);
            }

            logger.debug("GetContextInfo - SessionId={}, ContextId={}, Path={}, TaskType={}",
                        session.getSessionId(), contextId, path, taskType);

            GetContextInfoResponse response = session.getAgentBay().getClient().getContextInfo(request);

            String requestId = ResponseUtil.extractRequestId(response);
            List<ContextStatusData> contextStatusData = new ArrayList<>();

            if (response != null && response.getBody() != null) {
                GetContextInfoResponseBody body = response.getBody();
                if (body.getData() != null) {
                    String contextStatus = body.getData().getContextStatus();
                    if (contextStatus != null && !contextStatus.isEmpty()) {
                        try {
                            // Parse the context status JSON
                            JsonNode statusItems = objectMapper.readTree(contextStatus);
                            for (JsonNode item : statusItems) {
                                if ("data".equals(item.get("type").asText())) {
                                    String dataString = item.get("data").asText();
                                    JsonNode dataItems = objectMapper.readTree(dataString);
                                    for (JsonNode dataItem : dataItems) {
                                        Map<String, Object> itemMap = objectMapper.convertValue(dataItem, Map.class);
                                        contextStatusData.add(ContextStatusData.fromMap(itemMap));
                                    }
                                }
                            }
                        } catch (Exception e) {
                            logger.error("Error parsing context status: {}", e.getMessage());
                        }
                    }
                }
            }

            return new ContextInfoResult(requestId, contextStatusData);

        } catch (Exception e) {
            logger.error("Failed to get context info", e);
            return new ContextInfoResult("", new ArrayList<>());
        }
    }

    /**
     * Sync context data (trigger upload)
     */
    public ContextSyncResult sync() {
        return sync(null, null, null);
    }

    /**
     * Sync context data with optional parameters
     *
     * @param contextId Context ID (optional)
     * @param path Path (optional)
     * @param mode Sync mode (optional)
     * @return ContextSyncResult indicating success/failure
     */
    public ContextSyncResult sync(String contextId, String path, String mode) {
        try {
            SyncContextRequest request = new SyncContextRequest();
            request.setAuthorization("Bearer " + session.getApiKey());
            request.setSessionId(session.getSessionId());

            if (contextId != null) {
                request.setContextId(contextId);
            }
            if (path != null) {
                request.setPath(path);
            }
            if (mode != null) {
                request.setMode(mode);
            }

            logger.debug("SyncContext - SessionId={}, ContextId={}, Path={}, Mode={}",
                        session.getSessionId(), contextId, path, mode);

            SyncContextResponse response = session.getAgentBay().getClient().syncContext(request);

            String requestId = ResponseUtil.extractRequestId(response);
            boolean success = false;

            if (response != null && response.getBody() != null) {
                success = response.getBody().getSuccess() != null ? response.getBody().getSuccess() : false;
            }

            return new ContextSyncResult(requestId, success);

        } catch (Exception e) {
            logger.error("Failed to sync context", e);
            return new ContextSyncResult("", false);
        }
    }

}
