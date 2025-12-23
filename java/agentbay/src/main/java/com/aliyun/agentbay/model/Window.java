package com.aliyun.agentbay.model;

import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.ArrayList;
import java.util.List;

/**
 * Represents a window in the system.
 */
public class Window {
    private int windowId;
    private String title;
    private Integer absoluteUpperLeftX;
    private Integer absoluteUpperLeftY;
    private Integer width;
    private Integer height;
    private Integer pid;
    private String pname;
    private List<Window> childWindows;

    public Window() {
        this.childWindows = new ArrayList<>();
    }

    public Window(int windowId, String title) {
        this();
        this.windowId = windowId;
        this.title = title;
    }

    @JsonProperty("window_id")
    public int getWindowId() {
        return windowId;
    }

    public void setWindowId(int windowId) {
        this.windowId = windowId;
    }

    @JsonProperty("title")
    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    @JsonProperty("absolute_upper_left_x")
    public Integer getAbsoluteUpperLeftX() {
        return absoluteUpperLeftX;
    }

    public void setAbsoluteUpperLeftX(Integer absoluteUpperLeftX) {
        this.absoluteUpperLeftX = absoluteUpperLeftX;
    }

    @JsonProperty("absolute_upper_left_y")
    public Integer getAbsoluteUpperLeftY() {
        return absoluteUpperLeftY;
    }

    public void setAbsoluteUpperLeftY(Integer absoluteUpperLeftY) {
        this.absoluteUpperLeftY = absoluteUpperLeftY;
    }

    @JsonProperty("width")
    public Integer getWidth() {
        return width;
    }

    public void setWidth(Integer width) {
        this.width = width;
    }

    @JsonProperty("height")
    public Integer getHeight() {
        return height;
    }

    public void setHeight(Integer height) {
        this.height = height;
    }

    @JsonProperty("pid")
    public Integer getPid() {
        return pid;
    }

    public void setPid(Integer pid) {
        this.pid = pid;
    }

    @JsonProperty("pname")
    public String getPname() {
        return pname;
    }

    public void setPname(String pname) {
        this.pname = pname;
    }

    @JsonProperty("child_windows")
    public List<Window> getChildWindows() {
        return childWindows;
    }

    public void setChildWindows(List<Window> childWindows) {
        this.childWindows = childWindows != null ? childWindows : new ArrayList<>();
    }
}

