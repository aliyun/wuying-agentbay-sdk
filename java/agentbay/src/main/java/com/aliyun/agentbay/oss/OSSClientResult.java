package com.aliyun.agentbay.oss;

import com.aliyun.agentbay.model.ApiResponse;

public class OSSClientResult extends ApiResponse {
    private boolean success;
    private Object client;
    private String errorMessage;

    public OSSClientResult() {
        this("", false, null, "");
    }

    public OSSClientResult(String requestId, boolean success, Object client, String errorMessage) {
        super(requestId);
        this.success = success;
        this.client = client;
        this.errorMessage = errorMessage;
    }

    public boolean isSuccess() {
        return success;
    }

    public void setSuccess(boolean success) {
        this.success = success;
    }

    public Object getClient() {
        return client;
    }

    public Object getClientConfig() {
        return client;
    }

    public void setClient(Object client) {
        this.client = client;
    }

    public String getErrorMessage() {
        return errorMessage;
    }

    public void setErrorMessage(String errorMessage) {
        this.errorMessage = errorMessage;
    }
}
