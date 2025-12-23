package com.aliyun.agentbay.model;

import java.util.ArrayList;
import java.util.List;

/**
 * Result of window listing operations.
 */
public class WindowListResult extends ApiResponse {
    private boolean success;
    private List<Window> windows;
    private String errorMessage;

    public WindowListResult() {
        this("", false, new ArrayList<>(), "");
    }

    public WindowListResult(String requestId, boolean success, List<Window> windows, String errorMessage) {
        super(requestId);
        this.success = success;
        this.windows = windows != null ? windows : new ArrayList<>();
        this.errorMessage = errorMessage;
    }

    public boolean isSuccess() {
        return success;
    }

    public void setSuccess(boolean success) {
        this.success = success;
    }

    public List<Window> getWindows() {
        return windows;
    }

    public void setWindows(List<Window> windows) {
        this.windows = windows != null ? windows : new ArrayList<>();
    }

    public String getErrorMessage() {
        return errorMessage;
    }

    public void setErrorMessage(String errorMessage) {
        this.errorMessage = errorMessage;
    }
}

