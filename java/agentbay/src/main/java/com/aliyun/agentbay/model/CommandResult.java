package com.aliyun.agentbay.model;

public class CommandResult extends ApiResponse {
    private boolean success;
    private String output;
    private String errorMessage;
    private int exitCode;

    public CommandResult() {
        this("", false, "", "", 0);
    }

    public CommandResult(String requestId, boolean success, String output, String errorMessage, int exitCode) {
        super(requestId);
        this.success = success;
        this.output = output;
        this.errorMessage = errorMessage;
        this.exitCode = exitCode;
    }

    public boolean isSuccess() {
        return success;
    }

    public void setSuccess(boolean success) {
        this.success = success;
    }

    public String getOutput() {
        return output;
    }

    public void setOutput(String output) {
        this.output = output;
    }

    public String getErrorMessage() {
        return errorMessage;
    }

    public void setErrorMessage(String errorMessage) {
        this.errorMessage = errorMessage;
    }

    public int getExitCode() {
        return exitCode;
    }

    public void setExitCode(int exitCode) {
        this.exitCode = exitCode;
    }
}