package com.aliyun.agentbay.context;

/**
 * Lifecycle options for recycle policy
 */
public enum Lifecycle {
    LIFECYCLE_1DAY("Lifecycle_1Day"),
    LIFECYCLE_3DAYS("Lifecycle_3Days"),
    LIFECYCLE_5DAYS("Lifecycle_5Days"),
    LIFECYCLE_10DAYS("Lifecycle_10Days"),
    LIFECYCLE_15DAYS("Lifecycle_15Days"),
    LIFECYCLE_30DAYS("Lifecycle_30Days"),
    LIFECYCLE_90DAYS("Lifecycle_90Days"),
    LIFECYCLE_180DAYS("Lifecycle_180Days"),
    LIFECYCLE_360DAYS("Lifecycle_360Days"),
    LIFECYCLE_FOREVER("Lifecycle_Forever");

    private final String value;

    Lifecycle(String value) {
        this.value = value;
    }

    public String getValue() {
        return value;
    }

    @Override
    public String toString() {
        return value;
    }
}

