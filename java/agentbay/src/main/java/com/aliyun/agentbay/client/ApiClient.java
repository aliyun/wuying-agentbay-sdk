package com.aliyun.agentbay.client;

import com.aliyun.agentbay.exception.AgentBayException;
import com.aliyun.agentbay.exception.ApiException;
import com.aliyun.wuyingai20250506.Client;
import com.aliyun.wuyingai20250506.models.*;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * API client wrapper for WuyingAI client
 */
public class ApiClient {
    private static final Logger logger = LoggerFactory.getLogger(ApiClient.class);
    private static final ObjectMapper objectMapper = new ObjectMapper();

    private final Client client;
    private final String apiKey;

    public ApiClient(Client client, String apiKey) {
        this.client = client;
        this.apiKey = apiKey;
    }

    /**
     * Call an MCP tool
     *
     * @param sessionId The session ID
     * @param toolName The tool name
     * @param args The tool arguments
     * @return CallMcpToolResponse
     * @throws AgentBayException if the call fails
     */
    public CallMcpToolResponse callMcpTool(String sessionId, String toolName, Object args) throws AgentBayException {
        try {
            CallMcpToolRequest request = new CallMcpToolRequest();
            request.authorization = "Bearer " + apiKey;
            request.sessionId = sessionId;

            // Use 'name' field like Python version, with plain tool name
            request.name = toolName;

            // Properly serialize arguments to JSON
            String argsJson;
            if (args == null) {
                argsJson = "{}";
            } else {
                try {
                    argsJson = objectMapper.writeValueAsString(args);
                } catch (Exception e) {
                    logger.warn("Failed to serialize args to JSON, using toString: " + e.getMessage());
                    argsJson = args.toString();
                }
            }
            request.args = argsJson;

            logger.debug("Calling MCP tool: {} for session: {} with args: {}", toolName, sessionId, argsJson);

            CallMcpToolResponse response = client.callMcpTool(request);

            logger.debug("MCP tool called successfully: {} for session: {}", toolName, sessionId);
            return response;
        } catch (Exception e) {
            logger.error("Failed to call MCP tool: {} for session: {}", toolName, sessionId, e);
            throw new ApiException(String.format(
                    "Failed to call MCP tool '%s' for session '%s': %s",
                    toolName,
                    sessionId,
                    e.getMessage()
            ), e);
        }
    }

    /**
     * List available MCP tools
     *
     * @param sessionId The session ID
     * @return ListMcpToolsResponse
     * @throws AgentBayException if the call fails
     */
    public ListMcpToolsResponse listMcpTools(String sessionId) throws AgentBayException {
        try {
            ListMcpToolsRequest request = new ListMcpToolsRequest();
            request.authorization = "Bearer " + apiKey;
            // sessionId is not available in this API request

            ListMcpToolsResponse response = client.listMcpTools(request);

            logger.debug("Listed MCP tools for session: {}", sessionId);
            return response;
        } catch (Exception e) {
            logger.error("Failed to list MCP tools for session: {}", sessionId, e);
            throw new ApiException("Failed to list MCP tools", e);
        }
    }


    /**
     * Get ADB connection link for mobile sessions
     *
     * @param sessionId The session ID
     * @param adbkeyPub The ADB public key
     * @return GetAdbLinkResponse
     * @throws AgentBayException if the call fails
     */
    public GetAdbLinkResponse getAdbLink(String sessionId, String adbkeyPub) throws AgentBayException {
        try {
            GetAdbLinkRequest request = new GetAdbLinkRequest();
            request.setAuthorization("Bearer " + apiKey);
            request.setSessionId(sessionId);
            
            // Build options JSON with adbkey_pub
            String optionsJson = String.format("{\"adbkey_pub\":\"%s\"}", adbkeyPub);
            request.setOption(optionsJson);

            logger.debug("Getting ADB link for session: {} with adbkey_pub", sessionId);

            GetAdbLinkResponse response = client.getAdbLink(request);

            logger.debug("ADB link retrieved successfully for session: {}", sessionId);
            return response;
        } catch (Exception e) {
            logger.error("Failed to get ADB link for session: {}", sessionId, e);
            throw new ApiException(String.format(
                    "Failed to get ADB link for session '%s': %s",
                    sessionId,
                    e.getMessage()
            ), e);
        }
    }

    /**
     * Simple session deletion - stub implementation
     *
     * @param sessionId The session ID
     * @throws AgentBayException if the call fails
     */
    public void deleteSession(String sessionId) throws AgentBayException {
        logger.info("Session deletion requested: {}", sessionId);
        // In a real implementation, this would call the appropriate API
        // For now, we just log the deletion request
    }

    /**
     * Get the underlying client
     *
     * @return Client instance
     */
    public Client getClient() {
        return client;
    }
}