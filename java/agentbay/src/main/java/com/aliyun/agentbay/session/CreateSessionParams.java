package com.aliyun.agentbay.session;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import com.aliyun.agentbay.browser.BrowserContext;
import com.aliyun.agentbay.context.ContextSync;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class CreateSessionParams {
    private static final Logger logger = LoggerFactory.getLogger(CreateSessionParams.class);
    
    private String appId;
    private String browserType;
    private boolean autoUpload;
    private String imageId;
    private Map<String, String> labels;
    private Map<String, String> metadata;
    private List<ContextSync> contextSyncs;
    private BrowserContext browserContext;
    private String framework;

    public CreateSessionParams() {
        this.contextSyncs = new ArrayList<>();
    }

    public CreateSessionParams(String appId) {
        this.appId = appId;
        this.browserType = "chrome";
        this.autoUpload = true;
        this.contextSyncs = new ArrayList<>();
    }
    
    /**
     * Set the browser context and automatically merge extension and fingerprint context syncs.
     * 
     * @param browserContext Browser context configuration
     */
    public void setBrowserContext(BrowserContext browserContext) {
        this.browserContext = browserContext;
        
        if (browserContext != null) {
            // Initialize contextSyncs if null
            if (this.contextSyncs == null) {
                this.contextSyncs = new ArrayList<>();
            }
            
            // Add extension context syncs from browser_context if available
            List<ContextSync> extensionSyncs = browserContext.getExtensionContextSyncs();
            if (extensionSyncs != null && !extensionSyncs.isEmpty()) {
                this.contextSyncs.addAll(extensionSyncs);
                logger.info("Added {} extension context sync(s) from BrowserContext", 
                          extensionSyncs.size());
            }
            
            // Add fingerprint context sync from browser_context if available
            ContextSync fingerprintSync = browserContext.getFingerprintContextSync();
            if (fingerprintSync != null) {
                this.contextSyncs.add(fingerprintSync);
                logger.info("Added fingerprint context sync from BrowserContext");
            }
        }
    }

    public String getAppId() {
        return appId;
    }

    public void setAppId(String appId) {
        this.appId = appId;
    }

    public String getBrowserType() {
        return browserType;
    }

    public void setBrowserType(String browserType) {
        this.browserType = browserType;
    }

    public boolean isAutoUpload() {
        return autoUpload;
    }

    public void setAutoUpload(boolean autoUpload) {
        this.autoUpload = autoUpload;
    }

    public Map<String, String> getMetadata() {
        return metadata;
    }

    public void setMetadata(Map<String, String> metadata) {
        this.metadata = metadata;
    }

    public String getImageId() {
        return imageId;
    }

    public void setImageId(String imageId) {
        this.imageId = imageId;
    }

    public Map<String, String> getLabels() {
        return labels;
    }

    public void setLabels(Map<String, String> labels) {
        this.labels = labels;
    }

    public List<ContextSync> getContextSyncs() {
        return contextSyncs;
    }

    public void setContextSyncs(List<ContextSync> contextSyncs) {
        this.contextSyncs = contextSyncs;
    }
    
    public BrowserContext getBrowserContext() {
        return browserContext;
    }
    
    /**
     * Get the framework name (e.g., "spring-ai", "langchain4j").
     * This is used for SDK statistics tracking.
     * 
     * @return framework name, or null if not set
     */
    public String getFramework() {
        return framework;
    }
    
    /**
     * Set the framework name (e.g., "spring-ai", "langchain4j").
     * This is used for SDK statistics tracking.
     * 
     * @param framework framework name
     */
    public void setFramework(String framework) {
        this.framework = framework;
    }

}