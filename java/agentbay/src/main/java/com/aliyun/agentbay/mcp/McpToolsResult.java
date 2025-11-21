package com.aliyun.agentbay.mcp;

import com.aliyun.agentbay.model.ApiResponse;
import java.util.List;

public class McpToolsResult extends ApiResponse {
    private boolean success;
    private List<McpTool> tools;
    private String errorMessage;

    public McpToolsResult() {
        this("", false, null, "");
    }

    public McpToolsResult(String requestId, boolean success, List<McpTool> tools, String errorMessage) {
        super(requestId);
        this.success = success;
        this.tools = tools;
        this.errorMessage = errorMessage;
    }

    public boolean isSuccess() {
        return success;
    }

    public void setSuccess(boolean success) {
        this.success = success;
    }

    public List<McpTool> getTools() {
        return tools;
    }

    public void setTools(List<McpTool> tools) {
        this.tools = tools;
    }

    public String getErrorMessage() {
        return errorMessage;
    }

    public void setErrorMessage(String errorMessage) {
        this.errorMessage = errorMessage;
    }
}
