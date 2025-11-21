package com.aliyun.agentbay.util;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Utility class for handling API responses
 */
public class ResponseUtil {
    private static final Logger logger = LoggerFactory.getLogger(ResponseUtil.class);
    private static final ObjectMapper objectMapper = new ObjectMapper();

    /**
     * Extracts RequestID from API response.
     * This is a helper function used to extract RequestID in all API methods.
     *
     * @param response The response object from the API call
     * @return The request ID extracted from the response, or an empty string if not found
     */
    public static String extractRequestId(Object response) {
        if (response == null) {
            return "";
        }

        try {
            // Check if the response has a toMap method (most SDK responses have this)
            if (response.getClass().getMethod("toMap") != null) {
                Object responseMap = response.getClass().getMethod("toMap").invoke(response);

                if (responseMap instanceof java.util.Map) {
                    @SuppressWarnings("unchecked")
                    java.util.Map<String, Object> map = (java.util.Map<String, Object>) responseMap;

                    // Extract RequestId from the body field
                    Object body = map.get("body");
                    if (body instanceof java.util.Map) {
                        @SuppressWarnings("unchecked")
                        java.util.Map<String, Object> bodyMap = (java.util.Map<String, Object>) body;
                        Object requestId = bodyMap.get("RequestId");
                        if (requestId instanceof String) {
                            return (String) requestId;
                        }
                    }
                }
            }
        } catch (Exception e) {
            logger.debug("Failed to extract request ID from response: {}", e.getMessage());
        }

        return "";
    }
}