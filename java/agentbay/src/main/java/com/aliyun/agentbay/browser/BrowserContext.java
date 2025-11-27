package com.aliyun.agentbay.browser;

import com.aliyun.agentbay.Config;
import com.aliyun.agentbay.context.*;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/**
 * Browser context configuration for session.
 * 
 * This class provides browser context configuration for cloud sessions, supports browser fingerprint
 * context persistence, supports automatic extension synchronization when ExtensionOption is provided.
 * 
 * Key Features:
 * - Browser context binding for sessions
 * - Automatic browser data upload on session end
 * - Optional browser fingerprint integration with automatic context sync generation
 * - Optional extension integration with automatic context sync generation
 * - Clean API with ExtensionOption encapsulation
 * 
 * Usage Examples:
 * <pre>{@code
 * // With extensions using ExtensionOption
 * ExtensionOption extOption = new ExtensionOption(
 *     "my_extensions",
 *     Arrays.asList("ext1", "ext2")
 * );
 * 
 * BrowserContext browserContext = new BrowserContext(
 *     "browser_session",
 *     true,
 *     extOption,
 *     null
 * );
 * 
 * // Without extensions (minimal configuration)
 * BrowserContext browserContext = new BrowserContext(
 *     "browser_session",
 *     true
 * );
 * }</pre>
 */
public class BrowserContext {
    private String contextId;
    private boolean autoUpload;
    private ExtensionOption extensionOption;
    private BrowserFingerprintContext fingerprintContext;
    
    private String extensionContextId;
    private List<String> extensionIds;
    private List<ContextSync> extensionContextSyncs;
    
    private String fingerprintContextId;
    private ContextSync fingerprintContextSync;

    /**
     * Initialize BrowserContext with optional extension and fingerprint support.
     * 
     * @param contextId ID of the browser context to bind to the session.
     *                  This identifies the browser instance for the session.
     * @param autoUpload Whether to automatically upload browser data when the session ends.
     * @param extensionOption Extension configuration object containing context_id and extension_ids.
     *                       This encapsulates all extension-related configuration. Can be null.
     * @param fingerprintContext Browser fingerprint context configuration object containing 
     *                          fingerprint_context_id. Can be null.
     */
    public BrowserContext(String contextId, boolean autoUpload, 
                         ExtensionOption extensionOption,
                         BrowserFingerprintContext fingerprintContext) {
        this.contextId = contextId;
        this.autoUpload = autoUpload;
        this.extensionOption = extensionOption;
        this.fingerprintContext = fingerprintContext;
        
        // Handle extension configuration from ExtensionOption
        if (extensionOption != null) {
            // Extract extension information from ExtensionOption
            this.extensionContextId = extensionOption.getContextId();
            this.extensionIds = extensionOption.getExtensionIds();
            // Auto-generate extension context syncs
            this.extensionContextSyncs = createExtensionContextSyncs();
        } else {
            // No extension configuration provided
            this.extensionContextId = null;
            this.extensionIds = new ArrayList<>();
            this.extensionContextSyncs = null;
        }
        
        // Handle browser fingerprint configuration from BrowserFingerprintContext
        if (fingerprintContext != null) {
            this.fingerprintContextId = fingerprintContext.getFingerprintContextId();
            // Auto-generate fingerprint context sync
            this.fingerprintContextSync = createFingerprintContextSync();
        } else {
            this.fingerprintContextId = null;
            this.fingerprintContextSync = null;
        }
    }

    /**
     * Initialize BrowserContext with minimal configuration (no extensions, no fingerprint).
     * 
     * @param contextId ID of the browser context to bind to the session
     * @param autoUpload Whether to automatically upload browser data when session ends
     */
    public BrowserContext(String contextId, boolean autoUpload) {
        this(contextId, autoUpload, null, null);
    }

    /**
     * Initialize BrowserContext with default autoUpload=true.
     * 
     * @param contextId ID of the browser context to bind to the session
     */
    public BrowserContext(String contextId) {
        this(contextId, true, null, null);
    }

    /**
     * Create ContextSync configurations for browser extensions.
     * 
     * This method is called only when extension_option is provided and contains
     * valid extension configuration (context_id and extension_ids).
     * 
     * @return List of context sync configurations for extensions.
     *         Returns empty list if extension configuration is invalid.
     */
    private List<ContextSync> createExtensionContextSyncs() {
        if (extensionIds == null || extensionIds.isEmpty() || 
            extensionContextId == null || extensionContextId.trim().isEmpty()) {
            return Collections.emptyList();
        }

        // Create whitelist for each extension ID
        List<WhiteList> whiteLists = new ArrayList<>();
        for (String extId : extensionIds) {
            whiteLists.add(new WhiteList(extId, new ArrayList<>()));
        }

        // Create sync policy for extensions
        SyncPolicy syncPolicy = new SyncPolicy(
            new UploadPolicy(false, UploadStrategy.UPLOAD_BEFORE_RESOURCE_RELEASE, 30),
            DownloadPolicy.defaultPolicy(),
            new DeletePolicy(false),
            new ExtractPolicy(true, true, false),
            RecyclePolicy.defaultPolicy(),
            new BWList(whiteLists)
        );

        // Create context sync for extensions
        ContextSync extensionSync = new ContextSync(
            extensionContextId,
            "/tmp/extensions/",
            syncPolicy
        );

        List<ContextSync> syncs = new ArrayList<>();
        syncs.add(extensionSync);
        return syncs;
    }

    /**
     * Create ContextSync configuration for browser fingerprint.
     * 
     * This method is called only when fingerprint_context is provided and contains
     * valid fingerprint configuration (fingerprint_context_id).
     * 
     * @return Context sync configuration for fingerprint.
     *         Returns null if fingerprint configuration is invalid.
     */
    private ContextSync createFingerprintContextSync() {
        if (fingerprintContextId == null || fingerprintContextId.trim().isEmpty()) {
            return null;
        }

        // Create whitelist for fingerprint context
        List<WhiteList> whiteLists = new ArrayList<>();

        // Create sync policy for fingerprint
        SyncPolicy syncPolicy = new SyncPolicy(
            new UploadPolicy(false, UploadStrategy.UPLOAD_BEFORE_RESOURCE_RELEASE, 30),
            DownloadPolicy.defaultPolicy(),
            DeletePolicy.defaultPolicy(),
            new ExtractPolicy(true, true, false),
            RecyclePolicy.defaultPolicy(),
            new BWList(whiteLists)
        );

        // Create context sync for fingerprint
        return new ContextSync(
            fingerprintContextId,
            Config.BROWSER_FINGERPRINT_PERSIST_PATH,
            syncPolicy
        );
    }

    /**
     * Get context syncs for extensions.
     * 
     * @return Context sync configurations for extensions.
     *         Returns empty list if no extensions configured.
     */
    public List<ContextSync> getExtensionContextSyncs() {
        return extensionContextSyncs != null ? 
               new ArrayList<>(extensionContextSyncs) : 
               Collections.emptyList();
    }

    /**
     * Get context sync for fingerprint.
     * 
     * @return Context sync configuration for fingerprint.
     *         Returns null if fingerprint configuration is invalid.
     */
    public ContextSync getFingerprintContextSync() {
        return fingerprintContextSync;
    }

    // Getters
    public String getContextId() {
        return contextId;
    }

    public boolean isAutoUpload() {
        return autoUpload;
    }

    public ExtensionOption getExtensionOption() {
        return extensionOption;
    }

    public BrowserFingerprintContext getFingerprintContext() {
        return fingerprintContext;
    }

    public String getExtensionContextId() {
        return extensionContextId;
    }

    public List<String> getExtensionIds() {
        return extensionIds != null ? new ArrayList<>(extensionIds) : new ArrayList<>();
    }

    public String getFingerprintContextId() {
        return fingerprintContextId;
    }

    @Override
    public String toString() {
        return String.format("BrowserContext(contextId='%s', autoUpload=%s, extensions=%d, hasFingerprint=%s)",
                           contextId, autoUpload, 
                           extensionIds != null ? extensionIds.size() : 0,
                           fingerprintContextId != null);
    }
}

