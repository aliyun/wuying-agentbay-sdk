package com.aliyun.agentbay.model;

public class FileContentResult extends ApiResponse {
    private boolean success;
    private String content;
    private String errorMessage;

    public FileContentResult() {
        this("", false, "", "");
    }

    public FileContentResult(String requestId, boolean success, String content, String errorMessage) {
        super(requestId);
        this.success = success;
        this.content = content;
        this.errorMessage = errorMessage;
    }

    public boolean isSuccess() {
        return success;
    }

    public void setSuccess(boolean success) {
        this.success = success;
    }

    public String getContent() {
        return content;
    }

    public void setContent(String content) {
        this.content = content;
    }

    public String getErrorMessage() {
        return errorMessage;
    }

    public void setErrorMessage(String errorMessage) {
        this.errorMessage = errorMessage;
    }
}