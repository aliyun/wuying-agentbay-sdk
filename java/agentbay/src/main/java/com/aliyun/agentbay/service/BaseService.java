package com.aliyun.agentbay.service;

import com.aliyun.agentbay.exception.AgentBayException;
import com.aliyun.agentbay.model.OperationResult;
import com.aliyun.agentbay.session.Session;
import com.aliyun.agentbay.util.ResponseUtil;
import com.aliyun.wuyingai20250506.models.CallMcpToolResponse;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.util.HashMap;
import java.util.Map;
import java.util.Random;

import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;
import java.util.concurrent.TimeUnit;

/**
 * Base service class that provides common functionality for all service classes.
 * Similar to Python's BaseService, handles MCP tool calls and response parsing.
 */
public class BaseService {
    private static final Logger logger = LoggerFactory.getLogger(BaseService.class);
    private static final ObjectMapper objectMapper = new ObjectMapper();
    private static final OkHttpClient httpClient = new OkHttpClient.Builder()
        .readTimeout(120, TimeUnit.SECONDS)
        .writeTimeout(120, TimeUnit.SECONDS)
        .connectTimeout(30, TimeUnit.SECONDS)
        .build();
    private static final Random random = new Random();

    protected final Session session;

    public BaseService(Session session) {
        this.session = session;
    }

    /**
     * Call an MCP tool and parse the response similar to Python's _call_mcp_tool method.
     * Routes to VPC or API call based on session configuration.
     *
     * @param toolName The name of the tool to call
     * @param args     The arguments to pass to the tool
     * @return OperationResult containing the parsed response
     */
    protected OperationResult callMcpTool(String toolName, Object args) {
        try {
            if (session.isVpcEnabled()) {
                return callMcpToolVpc(toolName, args);
            } else {
                return callMcpToolApi(toolName, args);
            }
        } catch (Exception e) {
            logger.error("Unexpected error calling MCP tool: {}", toolName, e);
            return new OperationResult("", false, "", "Unexpected error: " + e.getMessage());
        }
    }

    /**
     * Call MCP tool via traditional API (non-VPC mode)
     */
    private OperationResult callMcpToolApi(String toolName, Object args) {
        try {
            CallMcpToolResponse response = session.callTool(toolName, args);

            if (response == null) {
                return new OperationResult("", false, "", "No response received");
            }

            String requestId = ResponseUtil.extractRequestId(response);

            if (response.getBody() != null && response.getBody().getData() != null) {
                try {
                    String parsedOutput = parseResponseBody(response.getBody().getData());
                    return new OperationResult(requestId, true, parsedOutput, "");
                } catch (RuntimeException e) {
                    if (e.getMessage() != null && e.getMessage().startsWith("MCP tool execution error:")) {
                        String errorMsg = e.getMessage().substring("MCP tool execution error: ".length());
                        return new OperationResult(requestId, false, "", errorMsg);
                    }
                    throw e;
                }
            } else {
                return new OperationResult(requestId, false, "", "Invalid response body");
            }

        } catch (AgentBayException e) {
            logger.error("Failed to call MCP tool: {}", toolName, e);
            return new OperationResult("", false, "", "Failed to call MCP tool " + toolName + ": " + e.getMessage());
        }
    }

    /**
     * Call MCP tool via VPC direct connection
     */
    private OperationResult callMcpToolVpc(String toolName, Object args) {
        try {
            //logger.debug("Calling VPC tool: {} with args: {}", toolName, args);

            String server = findServerForTool(toolName);
            if (server == null || server.isEmpty()) {
                return new OperationResult("", false, "", "Server not found for tool: " + toolName);
            }

            String requestId = String.format("vpc-%d-%09d",
                System.currentTimeMillis(), random.nextInt(1000000000));

            String vpcLinkUrl = session.getVpcLinkUrl();
            if (vpcLinkUrl == null || vpcLinkUrl.isEmpty()) {
                return new OperationResult("", false, "",
                    "VPC link URL not available. Ensure session VPC configuration is complete.");
            }

            String url = vpcLinkUrl + "/callTool";

            Map<String, Object> bodyParams = new HashMap<>();
            bodyParams.put("args", args);
            bodyParams.put("server", server);
            bodyParams.put("requestId", requestId);
            bodyParams.put("tool", toolName);
            bodyParams.put("token", session.getToken() != null ? session.getToken() : "");
            String bodyJson = objectMapper.writeValueAsString(bodyParams);

            String curlCommand = String.format("curl -X POST \"%s/callTool\" -H \"Content-Type: application/json\" -d '%s' -w \"\\n总耗时: %%{time_total}s\\n\"",
                vpcLinkUrl,
                bodyJson
            );
            //logger.info("VPC tool call curl command: \n {}", curlCommand);

            RequestBody requestBody = RequestBody.create(bodyJson, MediaType.parse("application/json"));
            Request request = new Request.Builder()
                .url(url)
                .header("Content-Type", "application/json")
                .post(requestBody)
                .build();

            try (Response response = httpClient.newCall(request).execute()) {
                if (!response.isSuccessful()) {
                    return new OperationResult(requestId, false, "",
                        "HTTP request failed with code: " + response.code());
                }

                String responseBody = response.body().string();
                Map<String, Object> outerData = objectMapper.readValue(responseBody, Map.class);

                Object dataField = outerData.get("data");
                if (dataField == null) {
                    return new OperationResult(requestId, false, "",
                        "No data field in VPC response");
                }

                Map<String, Object> parsedData;
                if (dataField instanceof String) {
                    parsedData = objectMapper.readValue((String) dataField, Map.class);
                } else if (dataField instanceof Map) {
                    parsedData = (Map<String, Object>) dataField;
                } else {
                    return new OperationResult(requestId, false, "",
                        "Invalid data field type in VPC response");
                }

                Object resultField = parsedData.get("result");
                if (resultField == null || !(resultField instanceof Map)) {
                    return new OperationResult(requestId, false, "",
                        "No result field in VPC response data");
                }

                Map<String, Object> resultData = (Map<String, Object>) resultField;
                Boolean isError = (Boolean) resultData.get("isError");
                Object contentObj = resultData.get("content");

                String textContent = "";
                if (contentObj instanceof java.util.List) {
                    java.util.List<?> content = (java.util.List<?>) contentObj;
                    if (!content.isEmpty() && content.get(0) instanceof Map) {
                        Map<?, ?> firstContent = (Map<?, ?>) content.get(0);
                        Object text = firstContent.get("text");
                        if (text != null) {
                            textContent = text.toString();
                        }
                    }
                }

                if (isError != null && isError) {
                    logger.error("VPC tool returned error: {}", textContent);
                    return new OperationResult(requestId, false, "", textContent);
                }

                logger.debug("VPC tool call successful: {}", textContent.substring(0, Math.min(200, textContent.length())));
                return new OperationResult(requestId, true, textContent, "");
            }

        } catch (IOException e) {
            logger.error("HTTP request failed for VPC tool call: {}", toolName, e);
            return new OperationResult("", false, "", "HTTP request failed: " + e.getMessage());
        } catch (Exception e) {
            logger.error("Failed to call VPC tool: {}", toolName, e);
            return new OperationResult("", false, "", "Unexpected error: " + e.getMessage());
        }
    }

    /**
     * Find server for a given tool name
     */
    private String findServerForTool(String toolName) {
        return session.findServerForTool(toolName);
    }

    /**
     * Parse MCP tool response body, similar to Python's _parse_response_body method.
     * Extracts text content from body.Data.content[0].text structure.
     *
     * @param responseData The response data to parse
     * @return Parsed text content
     */
    private String parseResponseBody(Object responseData) {
        try {
            if (responseData instanceof Map) {
                @SuppressWarnings("unchecked")
                Map<String, Object> dataMap = (Map<String, Object>) responseData;

                // Check for error first (similar to Python implementation)
                Boolean isError = (Boolean) dataMap.get("isError");
                if (isError != null && isError) {
                    // Handle error case - extract error message from content
                    Object contentObj = dataMap.get("content");
                    if (contentObj instanceof java.util.List) {
                        @SuppressWarnings("unchecked")
                        java.util.List<Object> content = (java.util.List<Object>) contentObj;
                        if (!content.isEmpty() && content.get(0) instanceof Map) {
                            @SuppressWarnings("unchecked")
                            Map<String, Object> contentItem = (Map<String, Object>) content.get(0);
                            Object text = contentItem.get("text");
                            if (text != null) {
                                throw new RuntimeException("MCP tool execution error: " + text.toString());
                            }
                        }
                    }
                    throw new RuntimeException("MCP tool execution failed with unknown error");
                }

                // Extract content[0].text like Python implementation
                Object contentObj = dataMap.get("content");
                if (contentObj instanceof java.util.List) {
                    @SuppressWarnings("unchecked")
                    java.util.List<Object> content = (java.util.List<Object>) contentObj;
                    if (!content.isEmpty() && content.get(0) instanceof Map) {
                        @SuppressWarnings("unchecked")
                        Map<String, Object> contentItem = (Map<String, Object>) content.get(0);
                        Object text = contentItem.get("text");
                        if (text != null) {
                            return text.toString();
                        }
                    }
                }
            }

            // Fallback to toString if parsing fails
            logger.warn("Failed to parse MCP response structure, using fallback");
            return responseData.toString();

        } catch (RuntimeException e) {
            // Re-throw RuntimeExceptions (like MCP tool execution errors) to be handled upstream
            throw e;
        } catch (Exception e) {
            logger.error("Error parsing MCP response", e);
            return "Error parsing MCP response: " + e.getMessage();
        }
    }
}