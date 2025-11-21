package com.aliyun.agentbay;

/**
 * Configuration class for AgentBay SDK
 */

public class Config {
    private String regionId;
    private String endpoint;
    private int timeoutMs;

    public Config(String regionId, String endpoint, int timeoutMs) {
        this.regionId = regionId;
        this.endpoint = endpoint;
        this.timeoutMs = timeoutMs;
    }

    public Config() {
        this.regionId = "cn-shanghai";
        this.endpoint = "wuyingai.cn-shanghai.aliyuncs.com";
        this.timeoutMs = 60000; // 60 seconds - matches Python version for browser automation
    }

    public String getRegionId() {
        return regionId;
    }

    public void setRegionId(String regionId) {
        this.regionId = regionId;
    }

    public String getEndpoint() {
        return endpoint;
    }

    public void setEndpoint(String endpoint) {
        this.endpoint = endpoint;
    }

    public int getTimeoutMs() {
        return timeoutMs;
    }

    public void setTimeoutMs(int timeoutMs) {
        this.timeoutMs = timeoutMs;
    }
}