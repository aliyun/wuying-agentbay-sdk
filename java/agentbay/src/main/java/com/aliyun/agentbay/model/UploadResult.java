package com.aliyun.agentbay.model;

public class UploadResult extends ApiResponse {
    private boolean success;
    private String requestIdUploadUrl;
    private String requestIdSync;
    private Integer httpStatus;
    private String etag;
    private long bytesSent;
    private String path;
    private String errorMessage;

    public UploadResult() {
        super();
    }

    public UploadResult(
        String requestId,
        boolean success,
        String requestIdUploadUrl,
        String requestIdSync,
        Integer httpStatus,
        String etag,
        long bytesSent,
        String path,
        String errorMessage
    ) {
        super(requestId);
        this.success = success;
        this.requestIdUploadUrl = requestIdUploadUrl;
        this.requestIdSync = requestIdSync;
        this.httpStatus = httpStatus;
        this.etag = etag;
        this.bytesSent = bytesSent;
        this.path = path;
        this.errorMessage = errorMessage;
    }

    public boolean isSuccess() {
        return success;
    }

    public void setSuccess(boolean success) {
        this.success = success;
    }

    public String getRequestIdUploadUrl() {
        return requestIdUploadUrl;
    }

    public void setRequestIdUploadUrl(String requestIdUploadUrl) {
        this.requestIdUploadUrl = requestIdUploadUrl;
    }

    public String getRequestIdSync() {
        return requestIdSync;
    }

    public void setRequestIdSync(String requestIdSync) {
        this.requestIdSync = requestIdSync;
    }

    public Integer getHttpStatus() {
        return httpStatus;
    }

    public void setHttpStatus(Integer httpStatus) {
        this.httpStatus = httpStatus;
    }

    public String getEtag() {
        return etag;
    }

    public void setEtag(String etag) {
        this.etag = etag;
    }

    public long getBytesSent() {
        return bytesSent;
    }

    public void setBytesSent(long bytesSent) {
        this.bytesSent = bytesSent;
    }

    public String getPath() {
        return path;
    }

    public void setPath(String path) {
        this.path = path;
    }

    public String getErrorMessage() {
        return errorMessage;
    }

    public void setErrorMessage(String errorMessage) {
        this.errorMessage = errorMessage;
    }
}
