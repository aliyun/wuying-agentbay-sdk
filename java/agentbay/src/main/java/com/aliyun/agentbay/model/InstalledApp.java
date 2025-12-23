package com.aliyun.agentbay.model;

import com.fasterxml.jackson.annotation.JsonProperty;

/**
 * Represents an installed application.
 */
public class InstalledApp {
    private String name;
    private String startCmd;
    private String stopCmd;
    private String workDirectory;

    public InstalledApp() {
        this("", "", null, null);
    }

    public InstalledApp(String name, String startCmd, String stopCmd, String workDirectory) {
        this.name = name;
        this.startCmd = startCmd;
        this.stopCmd = stopCmd;
        this.workDirectory = workDirectory;
    }

    @JsonProperty("name")
    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    @JsonProperty("start_cmd")
    public String getStartCmd() {
        return startCmd;
    }

    public void setStartCmd(String startCmd) {
        this.startCmd = startCmd;
    }

    @JsonProperty("stop_cmd")
    public String getStopCmd() {
        return stopCmd;
    }

    public void setStopCmd(String stopCmd) {
        this.stopCmd = stopCmd;
    }

    @JsonProperty("work_directory")
    public String getWorkDirectory() {
        return workDirectory;
    }

    public void setWorkDirectory(String workDirectory) {
        this.workDirectory = workDirectory;
    }
}

