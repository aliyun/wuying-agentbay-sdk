package com.aliyun.agentbay.context;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

/**
 * Defines the synchronization policy
 */
public class SyncPolicy {
    private UploadPolicy uploadPolicy;
    private DownloadPolicy downloadPolicy;
    private DeletePolicy deletePolicy;
    private ExtractPolicy extractPolicy;
    private RecyclePolicy recyclePolicy;
    private BWList bwList;

    public SyncPolicy() {
        // Set default values if not provided
        initializeDefaults();
    }

    public SyncPolicy(UploadPolicy uploadPolicy, DownloadPolicy downloadPolicy,
                     DeletePolicy deletePolicy, ExtractPolicy extractPolicy, BWList bwList) {
        this.uploadPolicy = uploadPolicy;
        this.downloadPolicy = downloadPolicy;
        this.deletePolicy = deletePolicy;
        this.extractPolicy = extractPolicy;
        this.recyclePolicy = null; // Will be initialized in initializeDefaults
        this.bwList = bwList;

        // Initialize defaults for null values
        initializeDefaults();
    }

    public SyncPolicy(UploadPolicy uploadPolicy, DownloadPolicy downloadPolicy,
                     DeletePolicy deletePolicy, ExtractPolicy extractPolicy, 
                     RecyclePolicy recyclePolicy, BWList bwList) {
        this.uploadPolicy = uploadPolicy;
        this.downloadPolicy = downloadPolicy;
        this.deletePolicy = deletePolicy;
        this.extractPolicy = extractPolicy;
        this.recyclePolicy = recyclePolicy;
        this.bwList = bwList;

        // Initialize defaults for null values
        initializeDefaults();
    }

    private void initializeDefaults() {
        if (this.uploadPolicy == null) {
            this.uploadPolicy = UploadPolicy.defaultPolicy();
        }
        if (this.downloadPolicy == null) {
            this.downloadPolicy = DownloadPolicy.defaultPolicy();
        }
        if (this.deletePolicy == null) {
            this.deletePolicy = DeletePolicy.defaultPolicy();
        }
        if (this.extractPolicy == null) {
            this.extractPolicy = ExtractPolicy.defaultPolicy();
        }
        if (this.recyclePolicy == null) {
            this.recyclePolicy = RecyclePolicy.defaultPolicy();
        }
        if (this.bwList == null) {
            WhiteList whiteList = new WhiteList("", new ArrayList<>());
            this.bwList = new BWList(java.util.Arrays.asList(whiteList));
        }
    }

    public static SyncPolicy defaultPolicy() {
        return new SyncPolicy(
                UploadPolicy.defaultPolicy(),
                DownloadPolicy.defaultPolicy(),
                DeletePolicy.defaultPolicy(),
                ExtractPolicy.defaultPolicy(),
                RecyclePolicy.defaultPolicy(),
                new BWList(java.util.Arrays.asList(new WhiteList("", new ArrayList<>())))
        );
    }

    public UploadPolicy getUploadPolicy() {
        return uploadPolicy;
    }

    public void setUploadPolicy(UploadPolicy uploadPolicy) {
        this.uploadPolicy = uploadPolicy;
    }

    public DownloadPolicy getDownloadPolicy() {
        return downloadPolicy;
    }

    public void setDownloadPolicy(DownloadPolicy downloadPolicy) {
        this.downloadPolicy = downloadPolicy;
    }

    public DeletePolicy getDeletePolicy() {
        return deletePolicy;
    }

    public void setDeletePolicy(DeletePolicy deletePolicy) {
        this.deletePolicy = deletePolicy;
    }

    public ExtractPolicy getExtractPolicy() {
        return extractPolicy;
    }

    public void setExtractPolicy(ExtractPolicy extractPolicy) {
        this.extractPolicy = extractPolicy;
    }

    public RecyclePolicy getRecyclePolicy() {
        return recyclePolicy;
    }

    public void setRecyclePolicy(RecyclePolicy recyclePolicy) {
        this.recyclePolicy = recyclePolicy;
    }

    public BWList getBwList() {
        return bwList;
    }

    public void setBwList(BWList bwList) {
        this.bwList = bwList;
    }

    public Map<String, Object> toMap() {
        Map<String, Object> result = new HashMap<>();
        if (uploadPolicy != null) {
            result.put("uploadPolicy", uploadPolicy.toMap());
        }
        if (downloadPolicy != null) {
            result.put("downloadPolicy", downloadPolicy.toMap());
        }
        if (deletePolicy != null) {
            result.put("deletePolicy", deletePolicy.toMap());
        }
        if (extractPolicy != null) {
            result.put("extractPolicy", extractPolicy.toMap());
        }
        if (recyclePolicy != null) {
            result.put("recyclePolicy", recyclePolicy.toMap());
        }
        if (bwList != null) {
            result.put("bwList", bwList.toMap());
        }
        return result;
    }
}