package com.aliyun.agentbay.session;

import java.util.List;
import java.util.Map;
import com.aliyun.agentbay.context.ContextSync;

public class CreateSessionParams {
    private String appId;
    private String browserType;
    private boolean autoUpload;
    private String imageId;
    private Map<String, String> labels;
    private Map<String, String> metadata;
    private List<ContextSync> contextSyncs;
    private Boolean isVpc;

    public CreateSessionParams() {
    }

    public CreateSessionParams(String appId) {
        this.appId = appId;
        this.browserType = "chrome";
        this.autoUpload = true;
    }

    public String getAppId() {
        return appId;
    }

    public void setAppId(String appId) {
        this.appId = appId;
    }

    public String getBrowserType() {
        return browserType;
    }

    public void setBrowserType(String browserType) {
        this.browserType = browserType;
    }

    public boolean isAutoUpload() {
        return autoUpload;
    }

    public void setAutoUpload(boolean autoUpload) {
        this.autoUpload = autoUpload;
    }

    public Map<String, String> getMetadata() {
        return metadata;
    }

    public void setMetadata(Map<String, String> metadata) {
        this.metadata = metadata;
    }

    public String getImageId() {
        return imageId;
    }

    public void setImageId(String imageId) {
        this.imageId = imageId;
    }

    public Map<String, String> getLabels() {
        return labels;
    }

    public void setLabels(Map<String, String> labels) {
        this.labels = labels;
    }

    public List<ContextSync> getContextSyncs() {
        return contextSyncs;
    }

    public void setContextSyncs(List<ContextSync> contextSyncs) {
        this.contextSyncs = contextSyncs;
    }

    public Boolean getIsVpc() {
        return isVpc;
    }

    public void setIsVpc(Boolean isVpc) {
        this.isVpc = isVpc;
    }
}