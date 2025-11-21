package com.aliyun.agentbay.context;

import java.util.HashMap;
import java.util.Map;

/**
 * Defines the upload policy for context synchronization
 */
public class UploadPolicy {
    private boolean autoUpload = true;
    private UploadStrategy uploadStrategy = UploadStrategy.UPLOAD_BEFORE_RESOURCE_RELEASE;
    private UploadMode uploadMode = UploadMode.FILE;
    private Integer period = 30;

    public UploadPolicy() {
    }

    public UploadPolicy(boolean autoUpload, UploadStrategy uploadStrategy, Integer period) {
        this.autoUpload = autoUpload;
        this.uploadStrategy = uploadStrategy;
        this.period = period;
        this.uploadMode = UploadMode.FILE;
    }

    public UploadPolicy(boolean autoUpload, UploadStrategy uploadStrategy, UploadMode uploadMode, Integer period) {
        this.autoUpload = autoUpload;
        this.uploadStrategy = uploadStrategy;
        this.uploadMode = uploadMode;
        this.period = period;
    }

    public static UploadPolicy defaultPolicy() {
        return new UploadPolicy();
    }

    public boolean isAutoUpload() {
        return autoUpload;
    }

    public void setAutoUpload(boolean autoUpload) {
        this.autoUpload = autoUpload;
    }

    public UploadStrategy getUploadStrategy() {
        return uploadStrategy;
    }

    public void setUploadStrategy(UploadStrategy uploadStrategy) {
        this.uploadStrategy = uploadStrategy;
    }

    public Integer getPeriod() {
        return period;
    }

    public void setPeriod(Integer period) {
        this.period = period;
    }

    public UploadMode getUploadMode() {
        return uploadMode;
    }

    public void setUploadMode(UploadMode uploadMode) {
        this.uploadMode = uploadMode;
    }

    public Map<String, Object> toMap() {
        Map<String, Object> map = new HashMap<>();
        map.put("autoUpload", autoUpload);
        map.put("uploadStrategy", uploadStrategy != null ? uploadStrategy.getValue() : null);
        map.put("uploadMode", uploadMode != null ? uploadMode.getValue() : null);
        map.put("period", period);
        return map;
    }
}