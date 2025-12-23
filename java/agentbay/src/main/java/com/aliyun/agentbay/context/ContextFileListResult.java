package com.aliyun.agentbay.context;

import com.aliyun.agentbay.model.ApiResponse;

import java.util.ArrayList;
import java.util.List;

/**
 * Result of file listing operation.
 */
public class ContextFileListResult extends ApiResponse {
    private boolean success;
    private List<FileInfo> entries;
    private Integer count;
    private String errorMessage;

    public ContextFileListResult() {
        super();
        this.entries = new ArrayList<>();
    }

    public ContextFileListResult(String requestId, boolean success, List<FileInfo> entries, Integer count, String errorMessage) {
        super(requestId);
        this.success = success;
        this.entries = entries != null ? entries : new ArrayList<>();
        this.count = count;
        this.errorMessage = errorMessage;
    }

    public boolean isSuccess() {
        return success;
    }

    public void setSuccess(boolean success) {
        this.success = success;
    }

    public List<FileInfo> getEntries() {
        return entries;
    }

    public void setEntries(List<FileInfo> entries) {
        this.entries = entries != null ? entries : new ArrayList<>();
    }

    public Integer getCount() {
        return count;
    }

    public void setCount(Integer count) {
        this.count = count;
    }

    public String getErrorMessage() {
        return errorMessage;
    }

    public void setErrorMessage(String errorMessage) {
        this.errorMessage = errorMessage;
    }
}
