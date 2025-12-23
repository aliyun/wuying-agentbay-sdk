package com.aliyun.agentbay.model.code;

public class CodeExecutionError {
    private String name;
    private String value;
    private String traceback;

    public CodeExecutionError() {
    }

    public CodeExecutionError(String name, String value, String traceback) {
        this.name = name;
        this.value = value;
        this.traceback = traceback;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getValue() {
        return value;
    }

    public void setValue(String value) {
        this.value = value;
    }

    public String getTraceback() {
        return traceback;
    }

    public void setTraceback(String traceback) {
        this.traceback = traceback;
    }
}
