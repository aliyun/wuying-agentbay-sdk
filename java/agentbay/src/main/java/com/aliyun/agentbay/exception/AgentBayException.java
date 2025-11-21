package com.aliyun.agentbay.exception;

/**
 * Base exception class for AgentBay SDK
 */
public class AgentBayException extends Exception {
    private String code;
    private String requestId;

    public AgentBayException(String message) {
        super(message);
    }

    public AgentBayException(String message, Throwable cause) {
        super(message, cause);
    }

    public AgentBayException(String code, String message) {
        super(message);
        this.code = code;
    }

    public AgentBayException(String code, String message, Throwable cause) {
        super(message, cause);
        this.code = code;
    }

    public String getCode() {
        return code;
    }

    public void setCode(String code) {
        this.code = code;
    }

    public String getRequestId() {
        return requestId;
    }

    public void setRequestId(String requestId) {
        this.requestId = requestId;
    }
}