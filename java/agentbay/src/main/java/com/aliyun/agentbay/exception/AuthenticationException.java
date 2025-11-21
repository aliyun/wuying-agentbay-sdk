package com.aliyun.agentbay.exception;

/**
 * Authentication exception for AgentBay SDK
 */
public class AuthenticationException extends AgentBayException {

    public AuthenticationException(String message) {
        super("AUTHENTICATION_ERROR", message);
    }

    public AuthenticationException(String message, Throwable cause) {
        super("AUTHENTICATION_ERROR", message, cause);
    }
}