package com.aliyun.agentbay.model;

import java.util.Map;

public class MultipleFileContentResult extends ApiResponse {
    private boolean success;
    private Map<String, String> files;
    private String errorMessage;

    public MultipleFileContentResult() {
        this("", false, null, "");
    }

    public MultipleFileContentResult(String requestId, boolean success, Map<String, String> files, String errorMessage) {
        super(requestId);
        this.success = success;
        this.files = files;
        this.errorMessage = errorMessage;
    }

    public boolean isSuccess() {
        return success;
    }

    public void setSuccess(boolean success) {
        this.success = success;
    }

    public Map<String, String> getFiles() {
        return files;
    }

    public Map<String, String> getContent() {
        return files;
    }

    public void setFiles(Map<String, String> files) {
        this.files = files;
    }

    public String getErrorMessage() {
        return errorMessage;
    }

    public void setErrorMessage(String errorMessage) {
        this.errorMessage = errorMessage;
    }
}