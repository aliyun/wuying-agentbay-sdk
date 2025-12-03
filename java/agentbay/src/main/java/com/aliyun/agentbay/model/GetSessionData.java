package com.aliyun.agentbay.model;

/**
 * Data returned by GetSession API
 */
public class GetSessionData {
    private String sessionId;
    private String appInstanceId;
    private String resourceId;
    private String resourceUrl;
    private boolean vpcResource;
    private String networkInterfaceIp;
    private String httpPort;
    private String token;
    private String status;
    private String code;

    public GetSessionData() {
    }

    public GetSessionData(String sessionId, String appInstanceId, String resourceId, 
                         String resourceUrl, boolean vpcResource, String networkInterfaceIp,
                         String httpPort, String token, String code) {
        this.sessionId = sessionId;
        this.appInstanceId = appInstanceId;
        this.resourceId = resourceId;
        this.resourceUrl = resourceUrl;
        this.vpcResource = vpcResource;
        this.networkInterfaceIp = networkInterfaceIp;
        this.httpPort = httpPort;
        this.token = token;
        this.code = code;
    }

    public String getSessionId() {
        return sessionId;
    }

    public void setSessionId(String sessionId) {
        this.sessionId = sessionId;
    }

    public String getAppInstanceId() {
        return appInstanceId;
    }

    public void setAppInstanceId(String appInstanceId) {
        this.appInstanceId = appInstanceId;
    }

    public String getResourceId() {
        return resourceId;
    }

    public void setResourceId(String resourceId) {
        this.resourceId = resourceId;
    }

    public String getResourceUrl() {
        return resourceUrl;
    }

    public void setResourceUrl(String resourceUrl) {
        this.resourceUrl = resourceUrl;
    }

    public boolean isVpcResource() {
        return vpcResource;
    }

    public void setVpcResource(boolean vpcResource) {
        this.vpcResource = vpcResource;
    }

    public String getNetworkInterfaceIp() {
        return networkInterfaceIp;
    }

    public void setNetworkInterfaceIp(String networkInterfaceIp) {
        this.networkInterfaceIp = networkInterfaceIp;
    }

    public String getHttpPort() {
        return httpPort;
    }

    public void setHttpPort(String httpPort) {
        this.httpPort = httpPort;
    }

    public String getToken() {
        return token;
    }

    public void setToken(String token) {
        this.token = token;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public String getCode() {
        return code;
    }

    public void setCode(String code) {
        this.code = code;
    }
}

