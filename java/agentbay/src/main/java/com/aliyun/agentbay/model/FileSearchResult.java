package com.aliyun.agentbay.model;

import java.util.List;

public class FileSearchResult extends ApiResponse {
    private boolean success;
    private List<String> files;
    private String errorMessage;

    public FileSearchResult() {
        this("", false, null, "");
    }

    public FileSearchResult(String requestId, boolean success, List<String> files, String errorMessage) {
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

    public List<String> getFiles() {
        return files;
    }

    public List<String> getMatches() {
        return files;
    }

    public void setFiles(List<String> files) {
        this.files = files;
    }

    public String getErrorMessage() {
        return errorMessage;
    }

    public void setErrorMessage(String errorMessage) {
        this.errorMessage = errorMessage;
    }
}