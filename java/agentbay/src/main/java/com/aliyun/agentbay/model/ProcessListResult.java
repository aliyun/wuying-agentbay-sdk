package com.aliyun.agentbay.model;

import java.util.ArrayList;
import java.util.List;

/**
 * Result of operations returning a list of Processes.
 */
public class ProcessListResult extends ApiResponse {
    private boolean success;
    private List<Process> data;
    private String errorMessage;

    public ProcessListResult() {
        this("", false, new ArrayList<>(), "");
    }

    public ProcessListResult(String requestId, boolean success, List<Process> data, String errorMessage) {
        super(requestId);
        this.success = success;
        this.data = data != null ? data : new ArrayList<>();
        this.errorMessage = errorMessage;
    }

    public boolean isSuccess() {
        return success;
    }

    public void setSuccess(boolean success) {
        this.success = success;
    }

    public List<Process> getData() {
        return data;
    }

    public void setData(List<Process> data) {
        this.data = data != null ? data : new ArrayList<>();
    }

    public String getErrorMessage() {
        return errorMessage;
    }

    public void setErrorMessage(String errorMessage) {
        this.errorMessage = errorMessage;
    }
}

