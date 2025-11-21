package com.aliyun.agentbay.browser;

/**
 * Configuration specifically for browser operations with extended timeouts
 */
public class BrowserConfig extends com.aliyun.agentbay.Config {

    public BrowserConfig() {
        super();
        // Browser operations often need more time for AI processing
        // Set to match Python version timeout configuration
        setTimeoutMs(90000); // 90 seconds for complex browser tasks
    }

    public BrowserConfig(String regionId, String endpoint) {
        super(regionId, endpoint, 90000); // Default to 90 seconds for browser operations
    }

    public BrowserConfig(String regionId, String endpoint, int timeoutMs) {
        super(regionId, endpoint, timeoutMs);
    }

    /**
     * Get timeout specifically optimized for browser automation tasks
     * @return timeout in milliseconds
     */
    public int getBrowserTimeoutMs() {
        return Math.max(getTimeoutMs(), 60000); // Minimum 60 seconds for browser operations
    }

    /**
     * Get timeout for complex AI browser tasks (search, extraction, etc.)
     * @return extended timeout in milliseconds
     */
    public int getExtendedTimeoutMs() {
        return Math.max(getTimeoutMs(), 120000); // Minimum 120 seconds for complex tasks
    }
}