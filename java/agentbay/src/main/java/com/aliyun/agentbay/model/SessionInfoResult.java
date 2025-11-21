package com.aliyun.agentbay.model;

/**
 * Result class for session info operations.
 * Contains SessionInfo data and operation metadata.
 */
public class SessionInfoResult {
    private String requestId;
    private boolean success;
    private SessionInfo sessionInfo;
    private String errorMessage;

    public SessionInfoResult() {
    }

    public SessionInfoResult(String requestId, boolean success, SessionInfo sessionInfo, String errorMessage) {
        this.requestId = requestId;
        this.success = success;
        this.sessionInfo = sessionInfo;
        this.errorMessage = errorMessage;
    }

    public String getRequestId() {
        return requestId;
    }

    public void setRequestId(String requestId) {
        this.requestId = requestId;
    }

    public boolean isSuccess() {
        return success;
    }

    public void setSuccess(boolean success) {
        this.success = success;
    }

    public SessionInfo getSessionInfo() {
        return sessionInfo;
    }

    public void setSessionInfo(SessionInfo sessionInfo) {
        this.sessionInfo = sessionInfo;
    }

    public String getErrorMessage() {
        return errorMessage;
    }

    public void setErrorMessage(String errorMessage) {
        this.errorMessage = errorMessage;
    }

    @Override
    public String toString() {
        return "SessionInfoResult{" +
                "requestId='" + requestId + '\'' +
                ", success=" + success +
                ", sessionInfo=" + sessionInfo +
                ", errorMessage='" + errorMessage + '\'' +
                '}';
    }
}