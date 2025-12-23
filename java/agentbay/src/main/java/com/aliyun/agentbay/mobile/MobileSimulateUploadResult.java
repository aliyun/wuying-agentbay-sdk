package com.aliyun.agentbay.mobile;

/**
 * Result of mobile simulate upload operations.
 */
public class MobileSimulateUploadResult {
    private boolean success;
    private String mobileSimulateContextId;
    private String errorMessage;

    public MobileSimulateUploadResult() {
        this.success = false;
        this.mobileSimulateContextId = "";
        this.errorMessage = "";
    }

    public MobileSimulateUploadResult(boolean success, String mobileSimulateContextId, String errorMessage) {
        this.success = success;
        this.mobileSimulateContextId = mobileSimulateContextId != null ? mobileSimulateContextId : "";
        this.errorMessage = errorMessage != null ? errorMessage : "";
    }

    public boolean isSuccess() {
        return success;
    }

    public void setSuccess(boolean success) {
        this.success = success;
    }

    public String getMobileSimulateContextId() {
        return mobileSimulateContextId;
    }

    public void setMobileSimulateContextId(String mobileSimulateContextId) {
        this.mobileSimulateContextId = mobileSimulateContextId;
    }

    public String getErrorMessage() {
        return errorMessage;
    }

    public void setErrorMessage(String errorMessage) {
        this.errorMessage = errorMessage;
    }
}
