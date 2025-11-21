package com.aliyun.agentbay.context;

import com.aliyun.agentbay.model.ApiResponse;

public class ContextSyncResult extends ApiResponse {
    private boolean success = false;

    public ContextSyncResult() {
        this("", false);
    }

    public ContextSyncResult(String requestId, boolean success) {
        super(requestId);
        this.success = success;
    }

    public boolean isSuccess() {
        return success;
    }

    public void setSuccess(boolean success) {
        this.success = success;
    }
}