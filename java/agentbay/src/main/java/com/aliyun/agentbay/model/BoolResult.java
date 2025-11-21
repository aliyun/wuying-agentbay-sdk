package com.aliyun.agentbay.model;

public class BoolResult extends ApiResponse {
    private boolean success;
    private Boolean data;
    private String errorMessage;

    public BoolResult() {
        this("", false, null, "");
    }

    public BoolResult(String requestId, boolean success, Boolean data, String errorMessage) {
        super(requestId);
        this.success = success;
        this.data = data;
        this.errorMessage = errorMessage;
    }

    public boolean isSuccess() {
        return success;
    }

    public void setSuccess(boolean success) {
        this.success = success;
    }

    public Boolean getData() {
        return data;
    }

    public void setData(Boolean data) {
        this.data = data;
    }

    public String getErrorMessage() {
        return errorMessage;
    }

    public void setErrorMessage(String errorMessage) {
        this.errorMessage = errorMessage;
    }
}