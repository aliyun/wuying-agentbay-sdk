package com.aliyun.agentbay.context;

/**
 * Defines the context synchronization configuration
 */
public class ContextSync {
    private String contextId;
    private String path;
    private SyncPolicy policy;

    public ContextSync() {
    }

    public ContextSync(String contextId, String path, SyncPolicy policy) {
        this.contextId = contextId;
        this.path = path;
        this.policy = policy;
    }

    public static ContextSync create(String contextId, String path, SyncPolicy policy) {
        return new ContextSync(contextId, path, policy);
    }

    public ContextSync withPolicy(SyncPolicy policy) {
        this.policy = policy;
        return this;
    }

    public String getContextId() {
        return contextId;
    }

    public void setContextId(String contextId) {
        this.contextId = contextId;
    }

    public String getPath() {
        return path;
    }

    public void setPath(String path) {
        this.path = path;
    }

    public SyncPolicy getPolicy() {
        return policy;
    }

    public void setPolicy(SyncPolicy policy) {
        this.policy = policy;
    }
}