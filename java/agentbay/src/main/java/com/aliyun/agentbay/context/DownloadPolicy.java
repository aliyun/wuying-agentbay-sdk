package com.aliyun.agentbay.context;

import java.util.HashMap;
import java.util.Map;

/**
 * Defines the download policy for context synchronization
 */
public class DownloadPolicy {
    private boolean autoDownload = true;
    private DownloadStrategy downloadStrategy = DownloadStrategy.DOWNLOAD_ASYNC;

    public DownloadPolicy() {
    }

    public DownloadPolicy(boolean autoDownload, DownloadStrategy downloadStrategy) {
        this.autoDownload = autoDownload;
        this.downloadStrategy = downloadStrategy;
    }

    public static DownloadPolicy defaultPolicy() {
        return new DownloadPolicy();
    }

    public boolean isAutoDownload() {
        return autoDownload;
    }

    public void setAutoDownload(boolean autoDownload) {
        this.autoDownload = autoDownload;
    }

    public DownloadStrategy getDownloadStrategy() {
        return downloadStrategy;
    }

    public void setDownloadStrategy(DownloadStrategy downloadStrategy) {
        this.downloadStrategy = downloadStrategy;
    }

    public Map<String, Object> toMap() {
        Map<String, Object> map = new HashMap<>();
        map.put("autoDownload", autoDownload);
        map.put("downloadStrategy", downloadStrategy != null ? downloadStrategy.getValue() : null);
        return map;
    }
}