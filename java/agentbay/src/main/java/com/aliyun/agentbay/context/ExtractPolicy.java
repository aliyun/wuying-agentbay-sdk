package com.aliyun.agentbay.context;

import java.util.HashMap;
import java.util.Map;

/**
 * Defines the extract policy for context synchronization
 */
public class ExtractPolicy {
    private boolean extract = true;
    private boolean deleteSrcFile = true;
    private boolean extractCurrentFolder = false;

    public ExtractPolicy() {
    }

    public ExtractPolicy(boolean extract, boolean deleteSrcFile, boolean extractCurrentFolder) {
        this.extract = extract;
        this.deleteSrcFile = deleteSrcFile;
        this.extractCurrentFolder = extractCurrentFolder;
    }

    public static ExtractPolicy defaultPolicy() {
        return new ExtractPolicy();
    }

    public boolean isExtract() {
        return extract;
    }

    public void setExtract(boolean extract) {
        this.extract = extract;
    }

    public boolean isDeleteSrcFile() {
        return deleteSrcFile;
    }

    public void setDeleteSrcFile(boolean deleteSrcFile) {
        this.deleteSrcFile = deleteSrcFile;
    }

    public boolean isExtractCurrentFolder() {
        return extractCurrentFolder;
    }

    public void setExtractCurrentFolder(boolean extractCurrentFolder) {
        this.extractCurrentFolder = extractCurrentFolder;
    }

    public Map<String, Object> toMap() {
        Map<String, Object> map = new HashMap<>();
        map.put("extract", extract);
        map.put("deleteSrcFile", deleteSrcFile);
        map.put("extractToCurrentFolder", extractCurrentFolder);
        return map;
    }
}
