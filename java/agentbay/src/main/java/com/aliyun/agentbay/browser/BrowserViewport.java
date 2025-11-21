package com.aliyun.agentbay.browser;

import java.util.HashMap;
import java.util.Map;

/**
 * Browser viewport configuration.
 */
public class BrowserViewport {
    private int width;
    private int height;

    public BrowserViewport() {
        this.width = 1920;
        this.height = 1080;
    }

    public BrowserViewport(int width, int height) {
        this.width = width;
        this.height = height;
    }

    public Map<String, Object> toMap() {
        Map<String, Object> map = new HashMap<>();
        map.put("width", width);
        map.put("height", height);
        return map;
    }

    public static BrowserViewport fromMap(Map<String, Object> map) {
        if (map == null) {
            return new BrowserViewport();
        }

        Integer width = (Integer) map.get("width");
        Integer height = (Integer) map.get("height");

        return new BrowserViewport(
            width != null ? width : 1920,
            height != null ? height : 1080
        );
    }

    // Getters and setters
    public int getWidth() { return width; }
    public void setWidth(int width) { this.width = width; }

    public int getHeight() { return height; }
    public void setHeight(int height) { this.height = height; }
}