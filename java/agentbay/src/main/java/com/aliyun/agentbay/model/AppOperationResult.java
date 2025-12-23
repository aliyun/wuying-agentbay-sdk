package com.aliyun.agentbay.model;

/**
 * Result of application operations like start/stop.
 */
public class AppOperationResult extends ApiResponse {
    private boolean success;
    private String errorMessage;

    public AppOperationResult() {
        this("", false, "");
    }

    public AppOperationResult(String requestId, boolean success, String errorMessage) {
        super(requestId);
        this.success = success;
        this.errorMessage = errorMessage;
    }

    public boolean isSuccess() {
        return success;
    }

    public void setSuccess(boolean success) {
        this.success = success;
    }

    public String getErrorMessage() {
        return errorMessage;
    }

    public void setErrorMessage(String errorMessage) {
        this.errorMessage = errorMessage;
    }
}

