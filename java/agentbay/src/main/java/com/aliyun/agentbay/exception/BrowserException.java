package com.aliyun.agentbay.exception;

/**
 * Exception thrown when browser operations fail
 */
public class BrowserException extends Exception {

    public BrowserException(String message) {
        super(message);
    }

    public BrowserException(String message, Throwable cause) {
        super(message, cause);
    }

    public BrowserException(Throwable cause) {
        super(cause);
    }
}