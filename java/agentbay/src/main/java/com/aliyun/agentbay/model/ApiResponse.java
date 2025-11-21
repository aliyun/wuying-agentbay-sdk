package com.aliyun.agentbay.model;

public class ApiResponse {
    private String requestId;

    public ApiResponse() {
        this("");
    }

    public ApiResponse(String requestId) {
        this.requestId = requestId;
    }

    public String getRequestId() {
        return requestId;
    }

    public void setRequestId(String requestId) {
        this.requestId = requestId;
    }
}