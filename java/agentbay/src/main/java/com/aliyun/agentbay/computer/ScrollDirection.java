package com.aliyun.agentbay.computer;

/**
 * Scroll direction for scroll operations.
 */
public enum ScrollDirection {
    UP("up"),
    DOWN("down"),
    LEFT("left"),
    RIGHT("right");

    private final String value;

    ScrollDirection(String value) {
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

