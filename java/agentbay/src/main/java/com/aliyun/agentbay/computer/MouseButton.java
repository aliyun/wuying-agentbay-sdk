package com.aliyun.agentbay.computer;

/**
 * Mouse button types for click and drag operations.
 */
public enum MouseButton {
    LEFT("left"),
    RIGHT("right"),
    MIDDLE("middle"),
    DOUBLE_LEFT("double_left");

    private final String value;

    MouseButton(String value) {
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

