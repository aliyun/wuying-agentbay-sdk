package com.aliyun.agentbay.context;

import com.aliyun.agentbay.model.ApiResponse;

public class ContextResult extends ApiResponse {
    private boolean success;
    private String contextId;
    private Context context;
    private String errorMessage;

    public ContextResult() {
        this("", false, "", null, "");
    }

    public ContextResult(String requestId, boolean success, String contextId, Context context, String errorMessage) {
        super(requestId);
        this.success = success;
        this.contextId = contextId;
        this.context = context;
        this.errorMessage = errorMessage;
    }

    public boolean isSuccess() {
        return success;
    }

    public void setSuccess(boolean success) {
        this.success = success;
    }

    public String getContextId() {
        return contextId;
    }

    public void setContextId(String contextId) {
        this.contextId = contextId;
    }

    public Context getContext() {
        return context;
    }

    public void setContext(Context context) {
        this.context = context;
    }

    public String getErrorMessage() {
        return errorMessage;
    }

    public void setErrorMessage(String errorMessage) {
        this.errorMessage = errorMessage;
    }
}