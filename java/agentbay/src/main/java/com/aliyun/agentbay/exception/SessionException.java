package com.aliyun.agentbay.exception;

public class SessionException extends AgentBayException {
    public SessionException(String message) {
        super(message);
    }

    public SessionException(String message, Throwable cause) {
        super(message, cause);
    }
}
