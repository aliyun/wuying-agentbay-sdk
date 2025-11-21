package com.aliyun.agentbay.browser;

import java.util.*;

/**
 * Browser initialization options.
 */
public class BrowserOption {
    private boolean useStealth;
    private String userAgent;
    private BrowserViewport viewport;
    private BrowserScreen screen;
    private BrowserFingerprint fingerprint;
    private boolean solveCaptchas;
    private List<BrowserProxy> proxies;
    private String extensionPath;

    public BrowserOption() {
        this.useStealth = false;
        this.solveCaptchas = false;
        this.extensionPath = "/tmp/extensions/";
    }

    public BrowserOption(boolean useStealth, String userAgent, BrowserViewport viewport,
                         BrowserScreen screen, BrowserFingerprint fingerprint, boolean solveCaptchas,
                         List<BrowserProxy> proxies, String extensionPath) {
        this.useStealth = useStealth;
        this.userAgent = userAgent;
        this.viewport = viewport;
        this.screen = screen;
        this.fingerprint = fingerprint;
        this.solveCaptchas = solveCaptchas;
        this.proxies = proxies;
        this.extensionPath = extensionPath;
        validate();
    }

    private void validate() {
        if (proxies != null) {
            if (proxies.size() > 1) {
                throw new IllegalArgumentException("proxies list length must be limited to 1");
            }
        }

        if (extensionPath != null && extensionPath.trim().isEmpty()) {
            throw new IllegalArgumentException("extension_path cannot be empty");
        }
    }

    public Map<String, Object> toMap() {
        Map<String, Object> map = new HashMap<>();

        // Check environment variable for behavior simulate
        String behaviorSimulate = System.getenv("AGENTBAY_BROWSER_BEHAVIOR_SIMULATE");
        if (behaviorSimulate != null) {
            map.put("behaviorSimulate", !"0".equals(behaviorSimulate));
        }

        map.put("useStealth", useStealth);
        if (userAgent != null) map.put("userAgent", userAgent);
        if (viewport != null) map.put("viewport", viewport.toMap());
        if (screen != null) map.put("screen", screen.toMap());
        if (fingerprint != null) map.put("fingerprint", fingerprint.toMap());
        map.put("solveCaptchas", solveCaptchas);
        if (proxies != null) {
            List<Map<String, Object>> proxyMaps = new ArrayList<>();
            for (BrowserProxy proxy : proxies) {
                proxyMaps.add(proxy.toMap());
            }
            map.put("proxies", proxyMaps);
        }
        if (extensionPath != null) map.put("extensionPath", extensionPath);

        return map;
    }

    @SuppressWarnings("unchecked")
    public static BrowserOption fromMap(Map<String, Object> map) {
        if (map == null) {
            return new BrowserOption();
        }

        BrowserOption option = new BrowserOption();
        option.useStealth = Boolean.TRUE.equals(map.get("useStealth"));
        option.userAgent = (String) map.get("userAgent");

        if (map.get("viewport") instanceof Map) {
            option.viewport = BrowserViewport.fromMap((Map<String, Object>) map.get("viewport"));
        }

        if (map.get("screen") instanceof Map) {
            option.screen = BrowserScreen.fromMap((Map<String, Object>) map.get("screen"));
        }

        if (map.get("fingerprint") instanceof Map) {
            option.fingerprint = BrowserFingerprint.fromMap((Map<String, Object>) map.get("fingerprint"));
        }

        option.solveCaptchas = Boolean.TRUE.equals(map.get("solveCaptchas"));

        if (map.get("proxies") instanceof List) {
            List<Map<String, Object>> proxyList = (List<Map<String, Object>>) map.get("proxies");
            if (proxyList.size() > 1) {
                throw new IllegalArgumentException("proxies list length must be limited to 1");
            }
            option.proxies = new ArrayList<>();
            for (Map<String, Object> proxyData : proxyList) {
                option.proxies.add(BrowserProxy.fromMap(proxyData));
            }
        }

        option.extensionPath = (String) map.get("extensionPath");

        return option;
    }

    // Getters and setters
    public boolean isUseStealth() { return useStealth; }
    public void setUseStealth(boolean useStealth) { this.useStealth = useStealth; }

    public String getUserAgent() { return userAgent; }
    public void setUserAgent(String userAgent) { this.userAgent = userAgent; }

    public BrowserViewport getViewport() { return viewport; }
    public void setViewport(BrowserViewport viewport) { this.viewport = viewport; }

    public BrowserScreen getScreen() { return screen; }
    public void setScreen(BrowserScreen screen) { this.screen = screen; }

    public BrowserFingerprint getFingerprint() { return fingerprint; }
    public void setFingerprint(BrowserFingerprint fingerprint) { this.fingerprint = fingerprint; }

    public boolean isSolveCaptchas() { return solveCaptchas; }
    public void setSolveCaptchas(boolean solveCaptchas) { this.solveCaptchas = solveCaptchas; }

    public List<BrowserProxy> getProxies() { return proxies; }
    public void setProxies(List<BrowserProxy> proxies) { this.proxies = proxies; }

    public String getExtensionPath() { return extensionPath; }
    public void setExtensionPath(String extensionPath) { this.extensionPath = extensionPath; }
}