// This file is auto-generated, don't edit it. Thanks.
package com.aliyun.wuyingai20250506.models;

import com.aliyun.tea.*;

public class CallMcpToolRequest extends TeaModel {
    @NameInMap("Args")
    public String args;

    @NameInMap("Authorization")
    public String authorization;

    @NameInMap("AutoGenSession")
    public Boolean autoGenSession;

    @NameInMap("ExternalUserId")
    public String externalUserId;

    @NameInMap("ImageId")
    public String imageId;

    @NameInMap("Name")
    public String name;

    @NameInMap("Server")
    public String server;

    @NameInMap("SessionId")
    public String sessionId;

    @NameInMap("Tool")
    public String tool;

    public static CallMcpToolRequest build(java.util.Map<String, ?> map) throws Exception {
        CallMcpToolRequest self = new CallMcpToolRequest();
        return TeaModel.build(map, self);
    }

    public CallMcpToolRequest setArgs(String args) {
        this.args = args;
        return this;
    }
    public String getArgs() {
        return this.args;
    }

    public CallMcpToolRequest setAuthorization(String authorization) {
        this.authorization = authorization;
        return this;
    }
    public String getAuthorization() {
        return this.authorization;
    }

    public CallMcpToolRequest setAutoGenSession(Boolean autoGenSession) {
        this.autoGenSession = autoGenSession;
        return this;
    }
    public Boolean getAutoGenSession() {
        return this.autoGenSession;
    }

    public CallMcpToolRequest setExternalUserId(String externalUserId) {
        this.externalUserId = externalUserId;
        return this;
    }
    public String getExternalUserId() {
        return this.externalUserId;
    }

    public CallMcpToolRequest setImageId(String imageId) {
        this.imageId = imageId;
        return this;
    }
    public String getImageId() {
        return this.imageId;
    }

    public CallMcpToolRequest setName(String name) {
        this.name = name;
        return this;
    }
    public String getName() {
        return this.name;
    }

    public CallMcpToolRequest setServer(String server) {
        this.server = server;
        return this;
    }
    public String getServer() {
        return this.server;
    }

    public CallMcpToolRequest setSessionId(String sessionId) {
        this.sessionId = sessionId;
        return this;
    }
    public String getSessionId() {
        return this.sessionId;
    }

    public CallMcpToolRequest setTool(String tool) {
        this.tool = tool;
        return this;
    }
    public String getTool() {
        return this.tool;
    }

}
