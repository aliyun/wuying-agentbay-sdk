package com.aliyun.agentbay.model.code;

import java.util.ArrayList;
import java.util.List;

public class CodeExecutionLogs {
    private List<String> stdout;
    private List<String> stderr;

    public CodeExecutionLogs() {
        this.stdout = new ArrayList<>();
        this.stderr = new ArrayList<>();
    }

    public CodeExecutionLogs(List<String> stdout, List<String> stderr) {
        this.stdout = stdout != null ? stdout : new ArrayList<>();
        this.stderr = stderr != null ? stderr : new ArrayList<>();
    }

    public List<String> getStdout() {
        return stdout;
    }

    public void setStdout(List<String> stdout) {
        this.stdout = stdout;
    }

    public List<String> getStderr() {
        return stderr;
    }

    public void setStderr(List<String> stderr) {
        this.stderr = stderr;
    }
}
