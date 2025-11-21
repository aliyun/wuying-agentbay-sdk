package com.aliyun.agentbay.session;

import com.aliyun.agentbay.model.SessionParams;
import com.aliyun.agentbay.mcp.McpTool;

import java.util.List;

public class SessionState {
    private String sessionId;
    private String fileTransferContextId;
    private boolean isVpc;
    private String httpPort;
    private String token;
    private String vpcLinkUrl;
    private long vpcLinkUrlTimestamp;
    private List<McpTool> mcpTools;

    public SessionState() {
    }

    public String getSessionId() {
        return sessionId;
    }

    public void setSessionId(String sessionId) {
        this.sessionId = sessionId;
    }

    public String getFileTransferContextId() {
        return fileTransferContextId;
    }

    public void setFileTransferContextId(String fileTransferContextId) {
        this.fileTransferContextId = fileTransferContextId;
    }

    public boolean isVpc() {
        return isVpc;
    }

    public void setVpc(boolean vpc) {
        isVpc = vpc;
    }

    public String getHttpPort() {
        return httpPort;
    }

    public void setHttpPort(String httpPort) {
        this.httpPort = httpPort;
    }

    public String getToken() {
        return token;
    }

    public void setToken(String token) {
        this.token = token;
    }

    public String getVpcLinkUrl() {
        return vpcLinkUrl;
    }

    public void setVpcLinkUrl(String vpcLinkUrl) {
        this.vpcLinkUrl = vpcLinkUrl;
    }

    public long getVpcLinkUrlTimestamp() {
        return vpcLinkUrlTimestamp;
    }

    public void setVpcLinkUrlTimestamp(long vpcLinkUrlTimestamp) {
        this.vpcLinkUrlTimestamp = vpcLinkUrlTimestamp;
    }

    public List<McpTool> getMcpTools() {
        return mcpTools;
    }

    public void setMcpTools(List<McpTool> mcpTools) {
        this.mcpTools = mcpTools;
    }
}
