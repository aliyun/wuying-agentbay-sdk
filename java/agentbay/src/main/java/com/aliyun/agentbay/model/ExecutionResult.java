package com.aliyun.agentbay.model;

public class ExecutionResult extends ApiResponse {
    private boolean success;
    private String errorMessage;
    private String taskId;
    private String taskStatus;
    private String taskResult;

    public ExecutionResult() {
        super();
        this.success = false;
        this.errorMessage = "";
        this.taskId = "";
        this.taskStatus = "";
        this.taskResult = "";
    }

    public ExecutionResult(String requestId, boolean success, String errorMessage) {
        super(requestId);
        this.success = success;
        this.errorMessage = errorMessage;
        this.taskId = "";
        this.taskStatus = "";
        this.taskResult = "";
    }

    public ExecutionResult(String requestId, boolean success, String errorMessage,
                          String taskId, String taskStatus) {
        super(requestId);
        this.success = success;
        this.errorMessage = errorMessage;
        this.taskId = taskId;
        this.taskStatus = taskStatus;
        this.taskResult = "";
    }

    public ExecutionResult(String requestId, boolean success, String errorMessage,
                          String taskId, String taskStatus, String taskResult) {
        super(requestId);
        this.success = success;
        this.errorMessage = errorMessage;
        this.taskId = taskId;
        this.taskStatus = taskStatus;
        this.taskResult = taskResult;
    }

    public boolean isSuccess() {
        return success;
    }

    public void setSuccess(boolean success) {
        this.success = success;
    }

    public String getErrorMessage() {
        return errorMessage;
    }

    public void setErrorMessage(String errorMessage) {
        this.errorMessage = errorMessage;
    }

    public String getTaskId() {
        return taskId;
    }

    public void setTaskId(String taskId) {
        this.taskId = taskId;
    }

    public String getTaskStatus() {
        return taskStatus;
    }

    public void setTaskStatus(String taskStatus) {
        this.taskStatus = taskStatus;
    }

    public String getTaskResult() {
        return taskResult;
    }

    public void setTaskResult(String taskResult) {
        this.taskResult = taskResult;
    }
}
