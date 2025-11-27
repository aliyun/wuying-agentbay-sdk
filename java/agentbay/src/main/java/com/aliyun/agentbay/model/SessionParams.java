package com.aliyun.agentbay.model;

/**
 * Session parameters for creating sessions
 */
public class SessionParams {
    private String name;
    private String browserType;
    private boolean headless;
    private String userAgent;
    private String windowSize;
    private boolean enableCookie;
    private String timeZone;
    private String language;

    public SessionParams() {
        this.browserType = "chrome";
        this.headless = false;
        this.enableCookie = true;
        this.timeZone = "Asia/Shanghai";
        this.language = "zh-CN";
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getBrowserType() {
        return browserType;
    }

    public void setBrowserType(String browserType) {
        this.browserType = browserType;
    }

    public boolean isHeadless() {
        return headless;
    }

    public void setHeadless(boolean headless) {
        this.headless = headless;
    }

    public String getUserAgent() {
        return userAgent;
    }

    public void setUserAgent(String userAgent) {
        this.userAgent = userAgent;
    }

    public String getWindowSize() {
        return windowSize;
    }

    public void setWindowSize(String windowSize) {
        this.windowSize = windowSize;
    }

    public boolean isEnableCookie() {
        return enableCookie;
    }

    public void setEnableCookie(boolean enableCookie) {
        this.enableCookie = enableCookie;
    }

    public String getTimeZone() {
        return timeZone;
    }

    public void setTimeZone(String timeZone) {
        this.timeZone = timeZone;
    }

    public String getLanguage() {
        return language;
    }

    public void setLanguage(String language) {
        this.language = language;
    }
}