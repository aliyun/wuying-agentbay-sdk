package com.aliyun.agentbay.exception;

/**
 * API exception for AgentBay SDK
 */
public class ApiException extends AgentBayException {

    public ApiException(String message) {
        super("API_ERROR", message);
    }

    public ApiException(String message, Throwable cause) {
        super("API_ERROR", message, cause);
    }

    public ApiException(String code, String message) {
        super(code, message);
    }

    public ApiException(String code, String message, Throwable cause) {
        super(code, message, cause);
    }
}