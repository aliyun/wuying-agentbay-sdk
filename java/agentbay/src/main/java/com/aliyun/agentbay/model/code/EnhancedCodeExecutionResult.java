package com.aliyun.agentbay.model.code;

import com.aliyun.agentbay.model.ApiResponse;
import java.util.ArrayList;
import java.util.List;

public class EnhancedCodeExecutionResult extends ApiResponse {
    private boolean success;
    private Integer executionCount;
    private double executionTime;
    private CodeExecutionLogs logs;
    private List<CodeResult> results;
    private CodeExecutionError error;
    private String errorMessage;

    public EnhancedCodeExecutionResult() {
        super();
        this.success = false;
        this.executionTime = 0.0;
        this.logs = new CodeExecutionLogs();
        this.results = new ArrayList<>();
        this.errorMessage = "";
    }

    public EnhancedCodeExecutionResult(String requestId, boolean success, String errorMessage) {
        super(requestId);
        this.success = success;
        this.executionTime = 0.0;
        this.logs = new CodeExecutionLogs();
        this.results = new ArrayList<>();
        this.errorMessage = errorMessage;
    }

    public boolean isSuccess() {
        return success;
    }

    public void setSuccess(boolean success) {
        this.success = success;
    }

    public Integer getExecutionCount() {
        return executionCount;
    }

    public void setExecutionCount(Integer executionCount) {
        this.executionCount = executionCount;
    }

    public double getExecutionTime() {
        return executionTime;
    }

    public void setExecutionTime(double executionTime) {
        this.executionTime = executionTime;
    }

    public CodeExecutionLogs getLogs() {
        return logs;
    }

    public void setLogs(CodeExecutionLogs logs) {
        this.logs = logs;
    }

    public List<CodeResult> getResults() {
        return results;
    }

    public void setResults(List<CodeResult> results) {
        this.results = results;
    }

    public CodeExecutionError getError() {
        return error;
    }

    public void setError(CodeExecutionError error) {
        this.error = error;
    }

    public String getErrorMessage() {
        return errorMessage;
    }

    public void setErrorMessage(String errorMessage) {
        this.errorMessage = errorMessage;
    }

    public String getResult() {
        for (CodeResult res : results) {
            if (res.isMainResult() && res.getText() != null) {
                return res.getText();
            }
        }
        if (!results.isEmpty() && results.get(0).getText() != null) {
            return results.get(0).getText();
        }
        if (logs != null && logs.getStdout() != null && !logs.getStdout().isEmpty()) {
            return String.join("", logs.getStdout());
        }
        return "";
    }
}
