package com.aliyun.agentbay.context;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Defines the white list configuration
 */
public class WhiteList {
    private String path = "";
    private List<String> excludePaths = new ArrayList<>();

    public WhiteList() {
    }

    public WhiteList(String path, List<String> excludePaths) {
        this.path = path;
        this.excludePaths = excludePaths != null ? excludePaths : new ArrayList<>();
    }

    public String getPath() {
        return path;
    }

    public void setPath(String path) {
        this.path = path;
    }

    public List<String> getExcludePaths() {
        return excludePaths;
    }

    public void setExcludePaths(List<String> excludePaths) {
        this.excludePaths = excludePaths != null ? excludePaths : new ArrayList<>();
    }

    public Map<String, Object> toMap() {
        Map<String, Object> map = new HashMap<>();
        map.put("path", path);
        map.put("excludePaths", excludePaths);
        return map;
    }
}