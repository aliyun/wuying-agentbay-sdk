package com.aliyun.agentbay.context;

import com.aliyun.agentbay.model.ApiResponse;
import java.util.ArrayList;
import java.util.List;

public class ContextListResult extends ApiResponse {
    private boolean success;
    private List<Context> contexts;
    private String nextToken;
    private Integer maxResults;
    private Integer totalCount;
    private String errorMessage;

    public ContextListResult() {
        this("", false, new ArrayList<>(), null, null, null, "");
    }

    public ContextListResult(String requestId, boolean success, List<Context> contexts,
                           String nextToken, Integer maxResults, Integer totalCount, String errorMessage) {
        super(requestId);
        this.success = success;
        this.contexts = contexts != null ? contexts : new ArrayList<>();
        this.nextToken = nextToken;
        this.maxResults = maxResults;
        this.totalCount = totalCount;
        this.errorMessage = errorMessage;
    }

    public boolean isSuccess() {
        return success;
    }

    public void setSuccess(boolean success) {
        this.success = success;
    }

    public List<Context> getContexts() {
        return contexts;
    }

    public void setContexts(List<Context> contexts) {
        this.contexts = contexts != null ? contexts : new ArrayList<>();
    }

    public String getNextToken() {
        return nextToken;
    }

    public void setNextToken(String nextToken) {
        this.nextToken = nextToken;
    }

    public Integer getMaxResults() {
        return maxResults;
    }

    public void setMaxResults(Integer maxResults) {
        this.maxResults = maxResults;
    }

    public Integer getTotalCount() {
        return totalCount;
    }

    public void setTotalCount(Integer totalCount) {
        this.totalCount = totalCount;
    }

    public String getErrorMessage() {
        return errorMessage;
    }

    public void setErrorMessage(String errorMessage) {
        this.errorMessage = errorMessage;
    }
}