package com.aliyun.agentbay.model;

import java.util.Map;

public class FileInfoResult extends ApiResponse {
    private boolean success;
    private String info;
    private Map<String, Object> fileInfo;
    private String errorMessage;

    public FileInfoResult() {
        this("", false, "", "");
    }

    public FileInfoResult(String requestId, boolean success, String info, String errorMessage) {
        super(requestId);
        this.success = success;
        this.info = info;
        this.errorMessage = errorMessage;
    }

    public boolean isSuccess() {
        return success;
    }

    public void setSuccess(boolean success) {
        this.success = success;
    }

    public String getInfo() {
        return info;
    }

    public Map<String, Object> getFileInfo() {
        return fileInfo;
    }

    public void setFileInfo(Map<String, Object> fileInfo) {
        this.fileInfo = fileInfo;
    }

    public void setInfo(String info) {
        this.info = info;
    }

    public String getErrorMessage() {
        return errorMessage;
    }

    public void setErrorMessage(String errorMessage) {
        this.errorMessage = errorMessage;
    }
}
