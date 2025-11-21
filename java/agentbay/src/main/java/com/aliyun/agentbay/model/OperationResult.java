package com.aliyun.agentbay.model;

/**
 * Operation result class similar to Python's OperationResult.
 * Contains success status, data, and error message for MCP tool operations.
 */
public class OperationResult {
    private String requestId;
    private boolean success;
    private String data;
    private String errorMessage;

    public OperationResult() {
    }

    public OperationResult(String requestId, boolean success, String data, String errorMessage) {
        this.requestId = requestId;
        this.success = success;
        this.data = data;
        this.errorMessage = errorMessage;
    }

    public String getRequestId() {
        return requestId;
    }

    public void setRequestId(String requestId) {
        this.requestId = requestId;
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

    @Override
    public String toString() {
        return "OperationResult{" +
                "requestId='" + requestId + '\'' +
                ", success=" + success +
                ", data='" + data + '\'' +
                ", errorMessage='" + errorMessage + '\'' +
                '}';
    }
}