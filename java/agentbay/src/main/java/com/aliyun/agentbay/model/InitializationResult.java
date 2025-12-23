package com.aliyun.agentbay.model;

public class InitializationResult extends ApiResponse {
    private boolean success;
    private String errorMessage;

    public InitializationResult() {
        super();
        this.success = false;
        this.errorMessage = "";
    }

    public InitializationResult(String requestId, boolean success, String errorMessage) {
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
