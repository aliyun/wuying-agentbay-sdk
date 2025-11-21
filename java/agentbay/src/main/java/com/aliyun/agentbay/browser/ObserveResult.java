package com.aliyun.agentbay.browser;

import java.util.Map;

/**
 * Result of browser observe operations - matches Python ObserveResult
 */
public class ObserveResult {
    private String selector;
    private String description;
    private String method;
    private Map<String, Object> arguments;

    public ObserveResult(String selector, String description, String method, Map<String, Object> arguments) {
        this.selector = selector;
        this.description = description;
        this.method = method;
        this.arguments = arguments;
    }

    // Getters and setters
    public String getSelector() { return selector; }
    public void setSelector(String selector) { this.selector = selector; }

    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }

    public String getMethod() { return method; }
    public void setMethod(String method) { this.method = method; }

    public Map<String, Object> getArguments() { return arguments; }
    public void setArguments(Map<String, Object> arguments) { this.arguments = arguments; }

    @Override
    public String toString() {
        return String.format("ObserveResult{selector='%s', description='%s', method='%s', arguments=%s}",
                           selector, description, method, arguments);
    }
}