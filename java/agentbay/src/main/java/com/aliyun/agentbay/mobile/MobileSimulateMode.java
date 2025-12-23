package com.aliyun.agentbay.mobile;

/**
 * Mobile simulation modes.
 */
public enum MobileSimulateMode {
    PROPERTIES_ONLY("PropertiesOnly"),
    SENSORS_ONLY("SensorsOnly"),
    PACKAGES_ONLY("PackagesOnly"),
    SERVICES_ONLY("ServicesOnly"),
    ALL("All");

    private final String value;

    MobileSimulateMode(String value) {
        this.value = value;
    }

    public String getValue() {
        return value;
    }

    public static MobileSimulateMode fromValue(String value) {
        for (MobileSimulateMode mode : MobileSimulateMode.values()) {
            if (mode.value.equals(value)) {
                return mode;
            }
        }
        throw new IllegalArgumentException("Unknown MobileSimulateMode: " + value);
    }
}
