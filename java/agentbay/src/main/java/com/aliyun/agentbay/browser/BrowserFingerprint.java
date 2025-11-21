package com.aliyun.agentbay.browser;

import java.util.*;

/**
 * Browser fingerprint configuration.
 */
public class BrowserFingerprint {
    private List<String> devices;
    private List<String> operatingSystems;
    private List<String> locales;

    public BrowserFingerprint() {
    }

    public BrowserFingerprint(List<String> devices, List<String> operatingSystems, List<String> locales) {
        this.devices = devices;
        this.operatingSystems = operatingSystems;
        this.locales = locales;
        validate();
    }

    private void validate() {
        if (devices != null) {
            for (String device : devices) {
                if (!"desktop".equals(device) && !"mobile".equals(device)) {
                    throw new IllegalArgumentException("device must be desktop or mobile");
                }
            }
        }

        if (operatingSystems != null) {
            Set<String> validOS = new HashSet<>();
            validOS.add("windows");
            validOS.add("macos");
            validOS.add("linux");
            validOS.add("android");
            validOS.add("ios");
            for (String os : operatingSystems) {
                if (!validOS.contains(os)) {
                    throw new IllegalArgumentException("operating_system must be windows, macos, linux, android or ios");
                }
            }
        }
    }

    public Map<String, Object> toMap() {
        Map<String, Object> map = new HashMap<>();
        if (devices != null) map.put("devices", devices);
        if (operatingSystems != null) map.put("operatingSystems", operatingSystems);
        if (locales != null) map.put("locales", locales);
        return map;
    }

    @SuppressWarnings("unchecked")
    public static BrowserFingerprint fromMap(Map<String, Object> map) {
        if (map == null) {
            return new BrowserFingerprint();
        }

        return new BrowserFingerprint(
            (List<String>) map.get("devices"),
            (List<String>) map.get("operatingSystems"),
            (List<String>) map.get("locales")
        );
    }

    // Getters and setters
    public List<String> getDevices() { return devices; }
    public void setDevices(List<String> devices) { this.devices = devices; }

    public List<String> getOperatingSystems() { return operatingSystems; }
    public void setOperatingSystems(List<String> operatingSystems) { this.operatingSystems = operatingSystems; }

    public List<String> getLocales() { return locales; }
    public void setLocales(List<String> locales) { this.locales = locales; }
}