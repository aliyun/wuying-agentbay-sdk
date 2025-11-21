package com.aliyun.agentbay.model;

public class CodeExecutionResult extends ApiResponse {
    private boolean success;
    private String output;
    private String errorMessage;
    private String stdout;
    private String stderr;

    public CodeExecutionResult() {
        this("", false, "", "", "", "");
    }

    public CodeExecutionResult(String requestId, boolean success, String output, String errorMessage, String stdout, String stderr) {
        super(requestId);
        this.success = success;
        this.output = output;
        this.errorMessage = errorMessage;
        this.stdout = stdout;
        this.stderr = stderr;
    }

    public CodeExecutionResult(String requestId, boolean success, String result, String errorMessage) {
        this(requestId, success, result, errorMessage, result, errorMessage);
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

    public String getStdout() {
        return stdout;
    }

    public void setStdout(String stdout) {
        this.stdout = stdout;
    }

    public String getStderr() {
        return stderr;
    }

    public void setStderr(String stderr) {
        this.stderr = stderr;
    }

    public String getResult() {
        return output;
    }
}
