package com.aliyun.agentbay.browser;

/**
 * Result of browser act operations - matches Python ActResult
 */
public class ActResult {
    private boolean success;
    private String message;
    private String action;

    public ActResult(boolean success, String message, String action) {
        this.success = success;
        this.message = message;
        this.action = action;
    }

    // Getters and setters
    public boolean isSuccess() { return success; }
    public void setSuccess(boolean success) { this.success = success; }

    public String getMessage() { return message; }
    public void setMessage(String message) { this.message = message; }

    public String getAction() { return action; }
    public void setAction(String action) { this.action = action; }

    @Override
    public String toString() {
        return String.format("ActResult{success=%s, message='%s', action='%s'}", success, message, action);
    }
}