package com.aliyun.agentbay.model;

/**
 * Result of window info operations.
 */
public class WindowInfoResult extends ApiResponse {
    private boolean success;
    private Window window;
    private String errorMessage;

    public WindowInfoResult() {
        this("", false, null, "");
    }

    public WindowInfoResult(String requestId, boolean success, Window window, String errorMessage) {
        super(requestId);
        this.success = success;
        this.window = window;
        this.errorMessage = errorMessage;
    }

    public boolean isSuccess() {
        return success;
    }

    public void setSuccess(boolean success) {
        this.success = success;
    }

    public Window getWindow() {
        return window;
    }

    public void setWindow(Window window) {
        this.window = window;
    }

    public String getErrorMessage() {
        return errorMessage;
    }

    public void setErrorMessage(String errorMessage) {
        this.errorMessage = errorMessage;
    }
}

