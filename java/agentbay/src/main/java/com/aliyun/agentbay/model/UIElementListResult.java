package com.aliyun.agentbay.model;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

/**
 * Result of UI element listing operations.
 */
public class UIElementListResult extends ApiResponse {
    private boolean success;
    private List<Map<String, Object>> elements;
    private String errorMessage;

    public UIElementListResult() {
        super("");
        this.success = false;
        this.elements = new ArrayList<>();
        this.errorMessage = "";
    }

    public UIElementListResult(String requestId, boolean success, 
                              List<Map<String, Object>> elements, String errorMessage) {
        super(requestId);
        this.success = success;
        this.elements = elements != null ? elements : new ArrayList<>();
        this.errorMessage = errorMessage != null ? errorMessage : "";
    }

    public boolean isSuccess() {
        return success;
    }

    public void setSuccess(boolean success) {
        this.success = success;
    }

    public List<Map<String, Object>> getElements() {
        return elements;
    }

    public void setElements(List<Map<String, Object>> elements) {
        this.elements = elements;
    }

    public String getErrorMessage() {
        return errorMessage;
    }

    public void setErrorMessage(String errorMessage) {
        this.errorMessage = errorMessage;
    }
}
