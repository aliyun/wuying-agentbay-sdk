package com.aliyun.agentbay.model;

public class DeleteResult extends ApiResponse {
    private boolean success;
    private String errorMessage;

    public DeleteResult() {
        this("", false, "");
    }

    public DeleteResult(String requestId, boolean success, String errorMessage) {
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