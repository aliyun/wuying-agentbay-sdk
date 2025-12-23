package com.aliyun.agentbay.model;

import java.util.ArrayList;
import java.util.List;

/**
 * Result of operations returning a list of InstalledApps.
 */
public class InstalledAppListResult extends ApiResponse {
    private boolean success;
    private List<InstalledApp> data;
    private String errorMessage;

    public InstalledAppListResult() {
        this("", false, new ArrayList<>(), "");
    }

    public InstalledAppListResult(String requestId, boolean success, List<InstalledApp> data, String errorMessage) {
        super(requestId);
        this.success = success;
        this.data = data != null ? data : new ArrayList<>();
        this.errorMessage = errorMessage;
    }

    public boolean isSuccess() {
        return success;
    }

    public void setSuccess(boolean success) {
        this.success = success;
    }

    public List<InstalledApp> getData() {
        return data;
    }

    public void setData(List<InstalledApp> data) {
        this.data = data != null ? data : new ArrayList<>();
    }

    public String getErrorMessage() {
        return errorMessage;
    }

    public void setErrorMessage(String errorMessage) {
        this.errorMessage = errorMessage;
    }
}

