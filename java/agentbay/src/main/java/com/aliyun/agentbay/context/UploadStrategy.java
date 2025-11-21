package com.aliyun.agentbay.context;

/**
 * Upload strategy for context synchronization
 */
public enum UploadStrategy {
    UPLOAD_BEFORE_RESOURCE_RELEASE("UploadBeforeResourceRelease");

    private final String value;

    UploadStrategy(String value) {
        this.value = value;
    }

    public String getValue() {
        return value;
    }
}