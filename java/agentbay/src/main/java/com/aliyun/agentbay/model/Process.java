package com.aliyun.agentbay.model;

import com.fasterxml.jackson.annotation.JsonProperty;

/**
 * Represents a running process.
 */
public class Process {
    private String pname;
    private int pid;
    private String cmdline;

    public Process() {
        this("", 0, null);
    }

    public Process(String pname, int pid, String cmdline) {
        this.pname = pname;
        this.pid = pid;
        this.cmdline = cmdline;
    }

    @JsonProperty("pname")
    public String getPname() {
        return pname;
    }

    public void setPname(String pname) {
        this.pname = pname;
    }

    @JsonProperty("pid")
    public int getPid() {
        return pid;
    }

    public void setPid(int pid) {
        this.pid = pid;
    }

    @JsonProperty("cmdline")
    public String getCmdline() {
        return cmdline;
    }

    public void setCmdline(String cmdline) {
        this.cmdline = cmdline;
    }
}

