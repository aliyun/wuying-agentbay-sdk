package com.aliyun.agentbay.context;

public class ContextListParams {
    private Integer maxResults;
    private String nextToken;

    public ContextListParams() {
    }

    public ContextListParams(Integer maxResults, String nextToken) {
        this.maxResults = maxResults;
        this.nextToken = nextToken;
    }

    public Integer getMaxResults() {
        return maxResults;
    }

    public void setMaxResults(Integer maxResults) {
        this.maxResults = maxResults;
    }

    public String getNextToken() {
        return nextToken;
    }

    public void setNextToken(String nextToken) {
        this.nextToken = nextToken;
    }
}