package com.aliyun.agentbay.oss;

import com.aliyun.agentbay.model.ApiResponse;

public class OSSDownloadResult extends ApiResponse {
    private boolean success;
    private String localPath;
    private String errorMessage;

    public OSSDownloadResult() {
        this("", false, "", "");
    }

    public OSSDownloadResult(String requestId, boolean success, String localPath, String errorMessage) {
        super(requestId);
        this.success = success;
        this.localPath = localPath;
        this.errorMessage = errorMessage;
    }

    public boolean isSuccess() {
        return success;
    }

    public void setSuccess(boolean success) {
        this.success = success;
    }

    public String getLocalPath() {
        return localPath;
    }

    public void setLocalPath(String localPath) {
        this.localPath = localPath;
    }

    public String getErrorMessage() {
        return errorMessage;
    }

    public void setErrorMessage(String errorMessage) {
        this.errorMessage = errorMessage;
    }

    public String getContent() {
        return localPath;
    }
}
