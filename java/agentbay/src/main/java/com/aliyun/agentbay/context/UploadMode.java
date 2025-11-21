package com.aliyun.agentbay.context;

public enum UploadMode {
    FILE("File"),
    ARCHIVE("Archive");

    private final String value;

    UploadMode(String value) {
        this.value = value;
    }

    public String getValue() {
        return value;
    }

    public static UploadMode fromValue(String value) {
        for (UploadMode mode : UploadMode.values()) {
            if (mode.value.equals(value)) {
                return mode;
            }
        }
        throw new IllegalArgumentException("Unknown UploadMode value: " + value);
    }
}
