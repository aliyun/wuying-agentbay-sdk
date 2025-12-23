package com.aliyun.agentbay.mobile;

import com.aliyun.agentbay.AgentBay;
import com.aliyun.agentbay.context.*;
import com.aliyun.agentbay.exception.AgentBayException;
import com.aliyun.agentbay.model.FileUrlResult;
import com.fasterxml.jackson.databind.ObjectMapper;
import okhttp3.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;
import java.util.UUID;

/**
 * Service for managing persistent mobile device info and syncing to mobile devices.
 * Provides methods to upload mobile simulation data and configure simulation settings.
 */
public class MobileSimulate {
    private static final Logger logger = LoggerFactory.getLogger(MobileSimulate.class);
    private static final ObjectMapper objectMapper = new ObjectMapper();
    private static final OkHttpClient httpClient = new OkHttpClient();

    private static final String MOBILE_INFO_DEFAULT_PATH = "/mobile_dev_info";
    private static final String MOBILE_INFO_SUB_PATH = "/mobile_dev_info";
    private static final String MOBILE_INFO_FILE_NAME = "mobile_dev_info.json";

    private final AgentBay agentBay;
    private final ContextService contextService;
    private boolean simulateEnable;
    private MobileSimulateMode simulateMode;
    private String contextId;
    private ContextSync contextSync;
    private String mobileDevInfoPath;
    private boolean useInternalContext;

    public MobileSimulate(AgentBay agentBay) {
        if (agentBay == null) {
            throw new IllegalArgumentException("agentBay is required");
        }
        if (agentBay.getContext() == null) {
            throw new IllegalArgumentException("agentBay.context is required");
        }

        this.agentBay = agentBay;
        this.contextService = agentBay.getContext();
        this.simulateEnable = false;
        this.simulateMode = MobileSimulateMode.PROPERTIES_ONLY;
        this.contextId = null;
        this.contextSync = null;
        this.mobileDevInfoPath = null;
        this.useInternalContext = true;
    }

    /**
     * Set the simulate enable flag.
     *
     * @param enable The simulate feature enable flag
     */
    public void setSimulateEnable(boolean enable) {
        this.simulateEnable = enable;
    }

    /**
     * Get the simulate enable flag.
     *
     * @return The simulate feature enable flag
     */
    public boolean getSimulateEnable() {
        return simulateEnable;
    }

    /**
     * Set the simulate mode.
     *
     * @param mode The simulate mode
     */
    public void setSimulateMode(MobileSimulateMode mode) {
        this.simulateMode = mode;
    }

    /**
     * Get the simulate mode.
     *
     * @return The simulate mode
     */
    public MobileSimulateMode getSimulateMode() {
        return simulateMode;
    }

    /**
     * Set a previously saved simulate context id.
     *
     * @param contextId The context ID of the previously saved mobile simulate context
     */
    public void setSimulateContextId(String contextId) {
        this.contextId = contextId;
        logger.info("Set simulate context id = {}", contextId);
        updateContext(true, contextId, null);
    }

    /**
     * Get the simulate context id.
     *
     * @return The context ID of the mobile simulate context
     */
    public String getSimulateContextId() {
        return contextId;
    }

    /**
     * Get the simulate config.
     *
     * @return The simulate config
     */
    public MobileSimulateConfig getSimulateConfig() {
        String simulatedContextId = useInternalContext ? contextId : null;
        return new MobileSimulateConfig(
            simulateEnable,
            mobileDevInfoPath,
            simulateMode,
            simulatedContextId
        );
    }

    /**
     * Check if the mobile dev info file exists in one context sync.
     *
     * @param contextSync The context sync to check
     * @return True if the mobile dev info file exists, False otherwise
     */
    public boolean hasMobileInfo(ContextSync contextSync) {
        if (contextSync == null) {
            throw new IllegalArgumentException("contextSync is required");
        }
        if (contextSync.getContextId() == null) {
            throw new IllegalArgumentException("contextSync.contextId is required");
        }
        if (contextSync.getPath() == null) {
            throw new IllegalArgumentException("contextSync.path is required");
        }

        String mobileDevInfoPath = contextSync.getPath() + MOBILE_INFO_SUB_PATH;
        logger.debug("hasMobileInfo: context_id = {}, mobile_dev_info_path = {}", 
            contextSync.getContextId(), mobileDevInfoPath);

        try {
            // List files in the context to check if mobile info exists
            ContextFileListResult res = contextService.listFiles(
                contextSync.getContextId(), 
                mobileDevInfoPath, 
                1, 
                50
            );
            
            boolean foundDevInfo = false;
            if (res.isSuccess()) {
                for (FileInfo entry : res.getEntries()) {
                    if (MOBILE_INFO_FILE_NAME.equals(entry.getFileName())) {
                        foundDevInfo = true;
                        break;
                    }
                }
            } else {
                logger.error("Failed to list files: {}", res.getErrorMessage());
                return false;
            }

            if (foundDevInfo) {
                logger.info("Mobile dev info already exists");
                // Update and save context sync if check success
                updateContext(false, contextSync.getContextId(), contextSync);
                return true;
            } else {
                logger.info("Mobile dev info does not exist");
                return false;
            }
        } catch (Exception e) {
            logger.error("Failed to check mobile info existence", e);
            return false;
        }
    }

    /**
     * Upload the mobile simulate dev info.
     *
     * @param mobileDevInfoContent The mobile simulate dev info content to upload (JSON string)
     * @param contextSync Optional context sync. If not provided, a new context will be created
     * @return MobileSimulateUploadResult containing the result of the upload operation
     */
    public MobileSimulateUploadResult uploadMobileInfo(String mobileDevInfoContent, ContextSync contextSync) {
        // Validate parameters
        if (mobileDevInfoContent == null || mobileDevInfoContent.isEmpty()) {
            throw new IllegalArgumentException("mobileDevInfoContent is required");
        }

        // Validate JSON
        try {
            objectMapper.readTree(mobileDevInfoContent);
        } catch (Exception e) {
            throw new IllegalArgumentException("mobileDevInfoContent is not a valid JSON string", e);
        }

        // Create context sync for simulate if not provided
        if (contextSync == null) {
            Context createdContext = createContextForSimulate();
            if (createdContext == null) {
                logger.error("Failed to create context for simulate");
                return new MobileSimulateUploadResult(false, "", "Failed to create context for simulate");
            }
            updateContext(true, createdContext.getId(), null);
        } else {
            if (contextSync.getContextId() == null) {
                throw new IllegalArgumentException("contextSync.contextId is required");
            }
            updateContext(false, contextSync.getContextId(), contextSync);
        }

        // Get upload URL
        String uploadPath = mobileDevInfoPath + "/" + MOBILE_INFO_FILE_NAME;
        FileUrlResult uploadUrlResult;
        try {
            uploadUrlResult = contextService.getFileUploadUrl(contextId, uploadPath);
        } catch (AgentBayException e) {
            logger.error("Failed to get file upload URL: {}", e.getMessage());
            return new MobileSimulateUploadResult(false, "", e.getMessage());
        }
        
        if (!uploadUrlResult.isSuccess()) {
            logger.error("Failed to get file upload URL: {}", uploadUrlResult.getErrorMessage());
            return new MobileSimulateUploadResult(false, "", uploadUrlResult.getErrorMessage());
        }

        logger.debug("upload_url = {}", uploadUrlResult.getUrl());

        // Upload file using HTTP PUT
        try {
            RequestBody body = RequestBody.create(
                mobileDevInfoContent, 
                MediaType.parse("application/json")
            );
            
            Request request = new Request.Builder()
                .url(uploadUrlResult.getUrl())
                .put(body)
                .build();

            try (Response response = httpClient.newCall(request).execute()) {
                if (!response.isSuccessful()) {
                    String errorMsg = "HTTP upload failed with code: " + response.code();
                    logger.error(errorMsg);
                    return new MobileSimulateUploadResult(false, "", errorMsg);
                }
            }
        } catch (IOException e) {
            logger.error("An error occurred while uploading the file", e);
            return new MobileSimulateUploadResult(false, "", e.getMessage());
        }

        logger.info("Mobile dev info uploaded successfully");
        return new MobileSimulateUploadResult(true, contextId, "");
    }

    /**
     * Upload mobile info without context sync (creates internal context).
     *
     * @param mobileDevInfoContent The mobile dev info JSON content
     * @return MobileSimulateUploadResult
     */
    public MobileSimulateUploadResult uploadMobileInfo(String mobileDevInfoContent) {
        return uploadMobileInfo(mobileDevInfoContent, null);
    }

    /**
     * Update internal context state.
     */
    private void updateContext(boolean isInternal, String contextId, ContextSync contextSync) {
        if (!isInternal) {
            if (contextSync == null) {
                throw new IllegalArgumentException("contextSync is required");
            }
            // Add mobile info path to context sync whitelist if needed
            if (contextSync.getPolicy() != null && 
                contextSync.getPolicy().getBwList() != null && 
                contextSync.getPolicy().getBwList().getWhiteLists() != null) {
                
                java.util.List<WhiteList> whiteLists = contextSync.getPolicy().getBwList().getWhiteLists();
                boolean found = false;
                for (WhiteList whiteList : whiteLists) {
                    if (MOBILE_INFO_SUB_PATH.equals(whiteList.getPath())) {
                        found = true;
                        break;
                    }
                }
                
                if (!found) {
                    WhiteList mobileInfoWhiteList = new WhiteList();
                    mobileInfoWhiteList.setPath(MOBILE_INFO_SUB_PATH);
                    mobileInfoWhiteList.setExcludePaths(new java.util.ArrayList<String>());
                    whiteLists.add(mobileInfoWhiteList);
                    logger.info("Added mobile_dev_info_path to context_sync.policy.bw_list.white_lists: {}", 
                        MOBILE_INFO_SUB_PATH);
                }
            }
        }

        this.useInternalContext = isInternal;
        this.contextId = contextId;
        this.contextSync = contextSync;
        
        if (isInternal) {
            this.mobileDevInfoPath = MOBILE_INFO_DEFAULT_PATH;
        } else {
            this.mobileDevInfoPath = contextSync.getPath() + MOBILE_INFO_SUB_PATH;
        }
        
        logger.info("Updated context, is_internal = {}, context_id = {}, mobile_dev_info_path = {}", 
            isInternal, this.contextId, this.mobileDevInfoPath);
    }

    /**
     * Create a new context for mobile simulation.
     */
    private Context createContextForSimulate() {
        String contextName = String.format("mobile_sim_%s_%d", 
            UUID.randomUUID().toString().replace("-", ""), 
            System.currentTimeMillis());
        
        try {
            ContextResult contextResult = contextService.get(contextName, true);
            if (!contextResult.isSuccess() || contextResult.getContext() == null) {
                logger.error("Failed to create mobile simulate context: {}", contextResult.getErrorMessage());
                return null;
            }

            Context context = contextResult.getContext();
            logger.info("Created mobile simulate context, context_id = {}, context_name = {}", 
                context.getId(), context.getName());
            return context;
        } catch (AgentBayException e) {
            logger.error("Failed to create mobile simulate context: {}", e.getMessage());
            return null;
        }
    }
}
