package com.aliyun.agentbay.browser;

import java.util.HashMap;
import java.util.Map;

/**
 * Browser proxy configuration.
 */
public class BrowserProxy {
    private String type;
    private String server;
    private String username;
    private String password;
    private String strategy;
    private int pollsize;

    public BrowserProxy(String type) {
        this.type = type;
        this.pollsize = 10; // default
        validateType();
    }

    public BrowserProxy(String type, String server, String username, String password) {
        this.type = type;
        this.server = server;
        this.username = username;
        this.password = password;
        this.pollsize = 10; // default
        validateType();
        validateCustomProxy();
    }

    public BrowserProxy(String type, String strategy, int pollsize) {
        this.type = type;
        this.strategy = strategy;
        this.pollsize = pollsize;
        validateType();
        validateWuyingProxy();
    }

    private void validateType() {
        if (!"custom".equals(type) && !"wuying".equals(type)) {
            throw new IllegalArgumentException("proxy_type must be custom or wuying");
        }
    }

    private void validateCustomProxy() {
        if ("custom".equals(type) && (server == null || server.trim().isEmpty())) {
            throw new IllegalArgumentException("server is required for custom proxy type");
        }
    }

    private void validateWuyingProxy() {
        if ("wuying".equals(type)) {
            if (strategy == null || strategy.trim().isEmpty()) {
                throw new IllegalArgumentException("strategy is required for wuying proxy type");
            }
            if (!"restricted".equals(strategy) && !"polling".equals(strategy)) {
                throw new IllegalArgumentException("strategy must be restricted or polling for wuying proxy type");
            }
            if ("polling".equals(strategy) && pollsize <= 0) {
                throw new IllegalArgumentException("pollsize must be greater than 0 for polling strategy");
            }
        }
    }

    public Map<String, Object> toMap() {
        Map<String, Object> map = new HashMap<>();
        map.put("type", type);

        if ("custom".equals(type)) {
            if (server != null) map.put("server", server);
            if (username != null) map.put("username", username);
            if (password != null) map.put("password", password);
        } else if ("wuying".equals(type)) {
            if (strategy != null) map.put("strategy", strategy);
            if ("polling".equals(strategy)) {
                map.put("pollsize", pollsize);
            }
        }

        return map;
    }

    public static BrowserProxy fromMap(Map<String, Object> map) {
        if (map == null || map.isEmpty()) {
            return null;
        }

        String type = (String) map.get("type");
        if (type == null) {
            throw new IllegalArgumentException("type is required in proxy configuration");
        }

        if ("custom".equals(type)) {
            return new BrowserProxy(
                type,
                (String) map.get("server"),
                (String) map.get("username"),
                (String) map.get("password")
            );
        } else if ("wuying".equals(type)) {
            return new BrowserProxy(
                type,
                (String) map.get("strategy"),
                (Integer) map.getOrDefault("pollsize", 10)
            );
        } else {
            throw new IllegalArgumentException("Unsupported proxy type: " + type);
        }
    }

    // Getters and setters
    public String getType() { return type; }
    public void setType(String type) { this.type = type; }

    public String getServer() { return server; }
    public void setServer(String server) { this.server = server; }

    public String getUsername() { return username; }
    public void setUsername(String username) { this.username = username; }

    public String getPassword() { return password; }
    public void setPassword(String password) { this.password = password; }

    public String getStrategy() { return strategy; }
    public void setStrategy(String strategy) { this.strategy = strategy; }

    public int getPollsize() { return pollsize; }
    public void setPollsize(int pollsize) { this.pollsize = pollsize; }
}