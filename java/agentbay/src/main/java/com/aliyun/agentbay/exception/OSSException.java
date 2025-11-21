package com.aliyun.agentbay.exception;

public class OSSException extends AgentBayException {
    public OSSException(String message) {
        super(message);
    }

    public OSSException(String message, Throwable cause) {
        super(message, cause);
    }
}