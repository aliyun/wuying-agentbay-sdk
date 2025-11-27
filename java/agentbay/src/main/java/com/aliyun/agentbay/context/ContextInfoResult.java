package com.aliyun.agentbay.context;

import com.aliyun.agentbay.model.ApiResponse;

import java.util.ArrayList;
import java.util.List;

public class ContextInfoResult extends ApiResponse {
    private boolean success = true;
    private List<ContextStatusData> contextStatusData = new ArrayList<>();
    private String errorMessage = "";

    public ContextInfoResult() {
        this("", new ArrayList<>());
    }

    public ContextInfoResult(String requestId, List<ContextStatusData> contextStatusData) {
        this(requestId, true, contextStatusData, "");
    }

    public ContextInfoResult(String requestId, boolean success, List<ContextStatusData> contextStatusData, String errorMessage) {
        super(requestId);
        this.success = success;
        this.contextStatusData = contextStatusData != null ? contextStatusData : new ArrayList<>();
        this.errorMessage = errorMessage != null ? errorMessage : "";
    }

    public boolean isSuccess() {
        return success;
    }

    public void setSuccess(boolean success) {
        this.success = success;
    }

    public List<ContextStatusData> getContextStatusData() {
        return contextStatusData;
    }

    public void setContextStatusData(List<ContextStatusData> contextStatusData) {
        this.contextStatusData = contextStatusData != null ? contextStatusData : new ArrayList<>();
    }

    public String getErrorMessage() {
        return errorMessage;
    }

    public void setErrorMessage(String errorMessage) {
        this.errorMessage = errorMessage != null ? errorMessage : "";
    }
}