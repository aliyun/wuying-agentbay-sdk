package com.aliyun.agentbay.context;

import java.util.Map;

public class ContextStatusData {
    private String contextId = "";
    private String path = "";
    private String errorMessage = "";
    private String status = "";
    private long startTime = 0;
    private long finishTime = 0;
    private String taskType = "";

    public ContextStatusData() {
    }

    public ContextStatusData(String contextId, String path, String errorMessage, String status,
                           long startTime, long finishTime, String taskType) {
        this.contextId = contextId;
        this.path = path;
        this.errorMessage = errorMessage;
        this.status = status;
        this.startTime = startTime;
        this.finishTime = finishTime;
        this.taskType = taskType;
    }

    public static ContextStatusData fromMap(Map<String, Object> data) {
        return new ContextStatusData(
                (String) data.getOrDefault("contextId", ""),
                (String) data.getOrDefault("path", ""),
                (String) data.getOrDefault("errorMessage", ""),
                (String) data.getOrDefault("status", ""),
                ((Number) data.getOrDefault("startTime", 0)).longValue(),
                ((Number) data.getOrDefault("finishTime", 0)).longValue(),
                (String) data.getOrDefault("taskType", "")
        );
    }

    public String getContextId() {
        return contextId;
    }

    public void setContextId(String contextId) {
        this.contextId = contextId;
    }

    public String getPath() {
        return path;
    }

    public void setPath(String path) {
        this.path = path;
    }

    public String getErrorMessage() {
        return errorMessage;
    }

    public void setErrorMessage(String errorMessage) {
        this.errorMessage = errorMessage;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public long getStartTime() {
        return startTime;
    }

    public void setStartTime(long startTime) {
        this.startTime = startTime;
    }

    public long getFinishTime() {
        return finishTime;
    }

    public void setFinishTime(long finishTime) {
        this.finishTime = finishTime;
    }

    public String getTaskType() {
        return taskType;
    }

    public void setTaskType(String taskType) {
        this.taskType = taskType;
    }
}