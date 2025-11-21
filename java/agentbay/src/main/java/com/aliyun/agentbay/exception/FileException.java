package com.aliyun.agentbay.exception;

public class FileException extends AgentBayException {
    public FileException(String message) {
        super(message);
    }

    public FileException(String message, Throwable cause) {
        super(message, cause);
    }
}