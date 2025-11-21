package com.aliyun.agentbay.oss;

import com.aliyun.agentbay.model.ApiResponse;

public class OSSUploadResult extends ApiResponse {
    private boolean success;
    private String url;
    private String errorMessage;

    public OSSUploadResult() {
        this("", false, "", "");
    }

    public OSSUploadResult(String requestId, boolean success, String url, String errorMessage) {
        super(requestId);
        this.success = success;
        this.url = url;
        this.errorMessage = errorMessage;
    }

    public boolean isSuccess() {
        return success;
    }

    public void setSuccess(boolean success) {
        this.success = success;
    }

    public String getUrl() {
        return url;
    }

    public void setUrl(String url) {
        this.url = url;
    }

    public String getErrorMessage() {
        return errorMessage;
    }

    public void setErrorMessage(String errorMessage) {
        this.errorMessage = errorMessage;
    }

    public String getContent() {
        return url;
    }
}
