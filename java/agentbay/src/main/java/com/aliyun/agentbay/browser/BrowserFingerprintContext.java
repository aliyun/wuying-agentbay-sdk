package com.aliyun.agentbay.browser;

/**
 * Browser fingerprint context configuration.
 * 
 * This class represents the configuration for browser fingerprint management,
 * allowing sessions to use consistent fingerprint data for anti-detection purposes.
 */
public class BrowserFingerprintContext {
    private String fingerprintContextId;

    /**
     * Initialize BrowserFingerprintContext with context id.
     * 
     * @param fingerprintContextId ID of the fingerprint context for browser fingerprint.
     * @throws IllegalArgumentException if fingerprintContextId is empty.
     */
    public BrowserFingerprintContext(String fingerprintContextId) {
        if (fingerprintContextId == null || fingerprintContextId.trim().isEmpty()) {
            throw new IllegalArgumentException("fingerprintContextId cannot be empty");
        }
        
        this.fingerprintContextId = fingerprintContextId;
    }

    /**
     * Get the fingerprint context ID
     * 
     * @return the fingerprint context ID
     */
    public String getFingerprintContextId() {
        return fingerprintContextId;
    }

    @Override
    public String toString() {
        return String.format("BrowserFingerprintContext(fingerprintContextId='%s')", 
                           fingerprintContextId);
    }
}

