package com.aliyun.agentbay.model;

/**
 * Result of ADB URL retrieval operations.
 */
public class AdbUrlResult extends ApiResponse {
    private boolean success;
    private String data;
    private String errorMessage;

    public AdbUrlResult() {
        super("");
        this.success = false;
        this.data = null;
        this.errorMessage = "";
    }

    public AdbUrlResult(String requestId, boolean success, String data, String errorMessage) {
        super(requestId);
        this.success = success;
        this.data = data;
        this.errorMessage = errorMessage != null ? errorMessage : "";
    }

    public boolean isSuccess() {
        return success;
    }

    public void setSuccess(boolean success) {
        this.success = success;
    }

    public String getData() {
        return data;
    }

    public void setData(String data) {
        this.data = data;
    }

    public String getErrorMessage() {
        return errorMessage;
    }

    public void setErrorMessage(String errorMessage) {
        this.errorMessage = errorMessage;
    }
}
