package com.aliyun.agentbay.model;

public class FileUrlResult extends ApiResponse {
    private boolean success;
    private String url;
    private Long expireTime;
    private String errorMessage;

    public FileUrlResult() {
        super();
    }

    public FileUrlResult(
        String requestId,
        boolean success,
        String url,
        Long expireTime,
        String errorMessage
    ) {
        super(requestId);
        this.success = success;
        this.url = url;
        this.expireTime = expireTime;
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

    public Long getExpireTime() {
        return expireTime;
    }

    public void setExpireTime(Long expireTime) {
        this.expireTime = expireTime;
    }

    public String getErrorMessage() {
        return errorMessage;
    }

    public void setErrorMessage(String errorMessage) {
        this.errorMessage = errorMessage;
    }
}
