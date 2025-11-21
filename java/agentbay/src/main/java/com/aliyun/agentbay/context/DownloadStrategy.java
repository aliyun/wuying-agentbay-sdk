package com.aliyun.agentbay.context;

/**
 * Download strategy for context synchronization
 */
public enum DownloadStrategy {
    DOWNLOAD_ASYNC("DownloadAsync");

    private final String value;

    DownloadStrategy(String value) {
        this.value = value;
    }

    public String getValue() {
        return value;
    }
}