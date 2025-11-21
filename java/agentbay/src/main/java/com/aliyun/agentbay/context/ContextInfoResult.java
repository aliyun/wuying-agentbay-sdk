package com.aliyun.agentbay.context;

import com.aliyun.agentbay.model.ApiResponse;

import java.util.ArrayList;
import java.util.List;

public class ContextInfoResult extends ApiResponse {
    private List<ContextStatusData> contextStatusData = new ArrayList<>();

    public ContextInfoResult() {
        this("", new ArrayList<>());
    }

    public ContextInfoResult(String requestId, List<ContextStatusData> contextStatusData) {
        super(requestId);
        this.contextStatusData = contextStatusData != null ? contextStatusData : new ArrayList<>();
    }

    public List<ContextStatusData> getContextStatusData() {
        return contextStatusData;
    }

    public void setContextStatusData(List<ContextStatusData> contextStatusData) {
        this.contextStatusData = contextStatusData != null ? contextStatusData : new ArrayList<>();
    }
}