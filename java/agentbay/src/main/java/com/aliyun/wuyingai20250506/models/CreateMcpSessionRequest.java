// This file is auto-generated, don't edit it. Thanks.
package com.aliyun.wuyingai20250506.models;

import com.aliyun.tea.*;

public class CreateMcpSessionRequest extends TeaModel {
    @NameInMap("Authorization")
    public String authorization;

    @NameInMap("ContextId")
    public String contextId;

    @NameInMap("DirectLink")
    public Boolean directLink;

    /**
     * <strong>if can be null:</strong>
     * <p>true</p>
     */
    @NameInMap("EnableRecord")
    public Boolean enableRecord;

    @NameInMap("ExternalUserId")
    public String externalUserId;

    @NameInMap("ImageId")
    public String imageId;

    @NameInMap("Labels")
    public String labels;

    @NameInMap("LoginRegionId")
    public String loginRegionId;

    @NameInMap("McpPolicyId")
    public String mcpPolicyId;

    @NameInMap("NetworkId")
    public String networkId;

    @NameInMap("PersistenceDataList")
    public java.util.List<CreateMcpSessionRequestPersistenceDataList> persistenceDataList;

    @NameInMap("SdkStats")
    public String sdkStats;

    @NameInMap("SessionId")
    public String sessionId;

    @NameInMap("VpcResource")
    public Boolean vpcResource;

    public static CreateMcpSessionRequest build(java.util.Map<String, ?> map) throws Exception {
        CreateMcpSessionRequest self = new CreateMcpSessionRequest();
        return TeaModel.build(map, self);
    }

    public CreateMcpSessionRequest setAuthorization(String authorization) {
        this.authorization = authorization;
        return this;
    }
    public String getAuthorization() {
        return this.authorization;
    }

    public CreateMcpSessionRequest setContextId(String contextId) {
        this.contextId = contextId;
        return this;
    }
    public String getContextId() {
        return this.contextId;
    }

    public CreateMcpSessionRequest setDirectLink(Boolean directLink) {
        this.directLink = directLink;
        return this;
    }
    public Boolean getDirectLink() {
        return this.directLink;
    }

    public CreateMcpSessionRequest setEnableRecord(Boolean enableRecord) {
        this.enableRecord = enableRecord;
        return this;
    }
    public Boolean getEnableRecord() {
        return this.enableRecord;
    }

    public CreateMcpSessionRequest setExternalUserId(String externalUserId) {
        this.externalUserId = externalUserId;
        return this;
    }
    public String getExternalUserId() {
        return this.externalUserId;
    }

    public CreateMcpSessionRequest setImageId(String imageId) {
        this.imageId = imageId;
        return this;
    }
    public String getImageId() {
        return this.imageId;
    }

    public CreateMcpSessionRequest setLabels(String labels) {
        this.labels = labels;
        return this;
    }
    public String getLabels() {
        return this.labels;
    }

    public CreateMcpSessionRequest setLoginRegionId(String loginRegionId) {
        this.loginRegionId = loginRegionId;
        return this;
    }
    public String getLoginRegionId() {
        return this.loginRegionId;
    }

    public CreateMcpSessionRequest setMcpPolicyId(String mcpPolicyId) {
        this.mcpPolicyId = mcpPolicyId;
        return this;
    }
    public String getMcpPolicyId() {
        return this.mcpPolicyId;
    }

    public CreateMcpSessionRequest setNetworkId(String networkId) {
        this.networkId = networkId;
        return this;
    }
    public String getNetworkId() {
        return this.networkId;
    }

    public CreateMcpSessionRequest setPersistenceDataList(java.util.List<CreateMcpSessionRequestPersistenceDataList> persistenceDataList) {
        this.persistenceDataList = persistenceDataList;
        return this;
    }
    public java.util.List<CreateMcpSessionRequestPersistenceDataList> getPersistenceDataList() {
        return this.persistenceDataList;
    }

    public CreateMcpSessionRequest setSdkStats(String sdkStats) {
        this.sdkStats = sdkStats;
        return this;
    }
    public String getSdkStats() {
        return this.sdkStats;
    }

    public CreateMcpSessionRequest setSessionId(String sessionId) {
        this.sessionId = sessionId;
        return this;
    }
    public String getSessionId() {
        return this.sessionId;
    }

    public CreateMcpSessionRequest setVpcResource(Boolean vpcResource) {
        this.vpcResource = vpcResource;
        return this;
    }
    public Boolean getVpcResource() {
        return this.vpcResource;
    }

    public static class CreateMcpSessionRequestPersistenceDataList extends TeaModel {
        @NameInMap("ContextId")
        public String contextId;

        @NameInMap("Path")
        public String path;

        @NameInMap("Policy")
        public String policy;

        public static CreateMcpSessionRequestPersistenceDataList build(java.util.Map<String, ?> map) throws Exception {
            CreateMcpSessionRequestPersistenceDataList self = new CreateMcpSessionRequestPersistenceDataList();
            return TeaModel.build(map, self);
        }

        public CreateMcpSessionRequestPersistenceDataList setContextId(String contextId) {
            this.contextId = contextId;
            return this;
        }
        public String getContextId() {
            return this.contextId;
        }

        public CreateMcpSessionRequestPersistenceDataList setPath(String path) {
            this.path = path;
            return this;
        }
        public String getPath() {
            return this.path;
        }

        public CreateMcpSessionRequestPersistenceDataList setPolicy(String policy) {
            this.policy = policy;
            return this;
        }
        public String getPolicy() {
            return this.policy;
        }

    }

}
