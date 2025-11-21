package com.aliyun.agentbay.model;

public class DownloadResult extends ApiResponse {
    private boolean success;
    private String requestIdDownloadUrl;
    private String requestIdSync;
    private Integer httpStatus;
    private long bytesReceived;
    private String path;
    private String localPath;
    private byte[] content;
    private String errorMessage;

    public DownloadResult() {
        super();
    }

    public DownloadResult(
        String requestId,
        boolean success,
        String requestIdDownloadUrl,
        String requestIdSync,
        Integer httpStatus,
        long bytesReceived,
        String path,
        String localPath,
        byte[] content,
        String errorMessage
    ) {
        super(requestId);
        this.success = success;
        this.requestIdDownloadUrl = requestIdDownloadUrl;
        this.requestIdSync = requestIdSync;
        this.httpStatus = httpStatus;
        this.bytesReceived = bytesReceived;
        this.path = path;
        this.localPath = localPath;
        this.content = content;
        this.errorMessage = errorMessage;
    }

    public boolean isSuccess() {
        return success;
    }

    public void setSuccess(boolean success) {
        this.success = success;
    }

    public String getRequestIdDownloadUrl() {
        return requestIdDownloadUrl;
    }

    public void setRequestIdDownloadUrl(String requestIdDownloadUrl) {
        this.requestIdDownloadUrl = requestIdDownloadUrl;
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

    public long getBytesReceived() {
        return bytesReceived;
    }

    public void setBytesReceived(long bytesReceived) {
        this.bytesReceived = bytesReceived;
    }

    public String getPath() {
        return path;
    }

    public void setPath(String path) {
        this.path = path;
    }

    public String getLocalPath() {
        return localPath;
    }

    public void setLocalPath(String localPath) {
        this.localPath = localPath;
    }

    public byte[] getContent() {
        return content;
    }

    public void setContent(byte[] content) {
        this.content = content;
    }

    public String getErrorMessage() {
        return errorMessage;
    }

    public void setErrorMessage(String errorMessage) {
        this.errorMessage = errorMessage;
    }
}
