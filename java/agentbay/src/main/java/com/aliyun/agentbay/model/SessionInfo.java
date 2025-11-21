package com.aliyun.agentbay.model;

/**
 * SessionInfo contains information about a session.
 * This mirrors the Python SDK's SessionInfo class.
 */
public class SessionInfo {
    private String sessionId = "";
    private String resourceUrl = "";
    private String appId = "";
    private String authCode = "";
    private String connectionProperties = "";
    private String resourceId = "";
    private String resourceType = "";
    private String ticket = "";

    public SessionInfo() {
    }

    public SessionInfo(String sessionId, String resourceUrl, String appId, String authCode,
                      String connectionProperties, String resourceId, String resourceType, String ticket) {
        this.sessionId = sessionId;
        this.resourceUrl = resourceUrl;
        this.appId = appId;
        this.authCode = authCode;
        this.connectionProperties = connectionProperties;
        this.resourceId = resourceId;
        this.resourceType = resourceType;
        this.ticket = ticket;
    }

    public String getSessionId() {
        return sessionId;
    }

    public void setSessionId(String sessionId) {
        this.sessionId = sessionId;
    }

    public String getResourceUrl() {
        return resourceUrl;
    }

    public void setResourceUrl(String resourceUrl) {
        this.resourceUrl = resourceUrl;
    }

    public String getAppId() {
        return appId;
    }

    public void setAppId(String appId) {
        this.appId = appId;
    }

    public String getAuthCode() {
        return authCode;
    }

    public void setAuthCode(String authCode) {
        this.authCode = authCode;
    }

    public String getConnectionProperties() {
        return connectionProperties;
    }

    public void setConnectionProperties(String connectionProperties) {
        this.connectionProperties = connectionProperties;
    }

    public String getResourceId() {
        return resourceId;
    }

    public void setResourceId(String resourceId) {
        this.resourceId = resourceId;
    }

    public String getResourceType() {
        return resourceType;
    }

    public void setResourceType(String resourceType) {
        this.resourceType = resourceType;
    }

    public String getTicket() {
        return ticket;
    }

    public void setTicket(String ticket) {
        this.ticket = ticket;
    }

    @Override
    public String toString() {
        return "SessionInfo{" +
                "sessionId='" + sessionId + '\'' +
                ", resourceUrl='" + resourceUrl + '\'' +
                ", appId='" + appId + '\'' +
                ", authCode='" + authCode + '\'' +
                ", connectionProperties='" + connectionProperties + '\'' +
                ", resourceId='" + resourceId + '\'' +
                ", resourceType='" + resourceType + '\'' +
                ", ticket='" + ticket + '\'' +
                '}';
    }
}