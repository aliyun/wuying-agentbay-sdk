package com.aliyun.agentbay.context;

import com.aliyun.agentbay.model.ApiResponse;

public class ContextSyncResult extends ApiResponse {
    private boolean success = false;
    private String errorMessage = "";

    public ContextSyncResult() {
        this("", false);
    }

    public ContextSyncResult(String requestId, boolean success) {
        this(requestId, success, "");
    }

    public ContextSyncResult(String requestId, boolean success, String errorMessage) {
        super(requestId);
        this.success = success;
        this.errorMessage = errorMessage != null ? errorMessage : "";
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
        this.errorMessage = errorMessage != null ? errorMessage : "";
    }
}