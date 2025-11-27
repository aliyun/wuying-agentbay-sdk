package com.aliyun.agentbay.browser;

import java.util.ArrayList;
import java.util.List;

/**
 * Configuration options for browser extension integration.
 * 
 * This class encapsulates the necessary parameters for setting up
 * browser extension synchronization and context management.
 */
public class ExtensionOption {
    private String contextId;
    private List<String> extensionIds;

    /**
     * Initialize ExtensionOption with context and extension configuration.
     * 
     * @param contextId ID of the extension context for browser extensions.
     *                  This should match the context where extensions are stored.
     * @param extensionIds List of extension IDs to be loaded in the browser session.
     *                     Each ID should correspond to a valid extension in the context.
     * @throws IllegalArgumentException if contextId is empty or extensionIds is empty.
     */
    public ExtensionOption(String contextId, List<String> extensionIds) {
        if (contextId == null || contextId.trim().isEmpty()) {
            throw new IllegalArgumentException("contextId cannot be empty");
        }
        
        if (extensionIds == null || extensionIds.isEmpty()) {
            throw new IllegalArgumentException("extensionIds cannot be empty");
        }
        
        this.contextId = contextId;
        this.extensionIds = new ArrayList<>(extensionIds);
    }

    /**
     * Get the context ID
     * 
     * @return the context ID for browser extensions
     */
    public String getContextId() {
        return contextId;
    }

    /**
     * Get the list of extension IDs
     * 
     * @return list of extension IDs to be loaded
     */
    public List<String> getExtensionIds() {
        return new ArrayList<>(extensionIds);
    }

    /**
     * Validate the extension option configuration.
     * 
     * @return true if configuration is valid, false otherwise
     */
    public boolean validate() {
        try {
            // Check context_id
            if (contextId == null || contextId.trim().isEmpty()) {
                return false;
            }
            
            // Check extension_ids
            if (extensionIds == null || extensionIds.isEmpty()) {
                return false;
            }
            
            // Check that all extension IDs are non-empty strings
            for (String extId : extensionIds) {
                if (extId == null || extId.trim().isEmpty()) {
                    return false;
                }
            }
            
            return true;
        } catch (Exception e) {
            return false;
        }
    }

    @Override
    public String toString() {
        return String.format("Extension Config: %d extension(s) in context '%s'", 
                           extensionIds.size(), contextId);
    }
}

