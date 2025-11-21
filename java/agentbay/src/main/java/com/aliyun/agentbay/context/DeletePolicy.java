package com.aliyun.agentbay.context;

import java.util.HashMap;
import java.util.Map;

/**
 * Defines the delete policy for context synchronization
 */
public class DeletePolicy {
    private boolean syncLocalFile = true;

    public DeletePolicy() {
    }

    public DeletePolicy(boolean syncLocalFile) {
        this.syncLocalFile = syncLocalFile;
    }

    public static DeletePolicy defaultPolicy() {
        return new DeletePolicy();
    }

    public boolean isSyncLocalFile() {
        return syncLocalFile;
    }

    public void setSyncLocalFile(boolean syncLocalFile) {
        this.syncLocalFile = syncLocalFile;
    }

    public Map<String, Object> toMap() {
        Map<String, Object> map = new HashMap<>();
        map.put("syncLocalFile", syncLocalFile);
        return map;
    }
}