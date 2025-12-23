// This file is auto-generated, don't edit it. Thanks.
package com.aliyun.wuyingai20250506.models;

import com.aliyun.tea.*;

public class CreateMcpSessionShrinkRequest extends TeaModel {
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
    public String persistenceDataListShrink;

    @NameInMap("SdkStats")
    public String sdkStats;

    @NameInMap("SessionId")
    public String sessionId;

    @NameInMap("VpcResource")
    public Boolean vpcResource;

    public static CreateMcpSessionShrinkRequest build(java.util.Map<String, ?> map) throws Exception {
        CreateMcpSessionShrinkRequest self = new CreateMcpSessionShrinkRequest();
        return TeaModel.build(map, self);
    }

    public CreateMcpSessionShrinkRequest setAuthorization(String authorization) {
        this.authorization = authorization;
        return this;
    }
    public String getAuthorization() {
        return this.authorization;
    }

    public CreateMcpSessionShrinkRequest setContextId(String contextId) {
        this.contextId = contextId;
        return this;
    }
    public String getContextId() {
        return this.contextId;
    }

    public CreateMcpSessionShrinkRequest setDirectLink(Boolean directLink) {
        this.directLink = directLink;
        return this;
    }
    public Boolean getDirectLink() {
        return this.directLink;
    }

    public CreateMcpSessionShrinkRequest setEnableRecord(Boolean enableRecord) {
        this.enableRecord = enableRecord;
        return this;
    }
    public Boolean getEnableRecord() {
        return this.enableRecord;
    }

    public CreateMcpSessionShrinkRequest setExternalUserId(String externalUserId) {
        this.externalUserId = externalUserId;
        return this;
    }
    public String getExternalUserId() {
        return this.externalUserId;
    }

    public CreateMcpSessionShrinkRequest setImageId(String imageId) {
        this.imageId = imageId;
        return this;
    }
    public String getImageId() {
        return this.imageId;
    }

    public CreateMcpSessionShrinkRequest setLabels(String labels) {
        this.labels = labels;
        return this;
    }
    public String getLabels() {
        return this.labels;
    }

    public CreateMcpSessionShrinkRequest setLoginRegionId(String loginRegionId) {
        this.loginRegionId = loginRegionId;
        return this;
    }
    public String getLoginRegionId() {
        return this.loginRegionId;
    }

    public CreateMcpSessionShrinkRequest setMcpPolicyId(String mcpPolicyId) {
        this.mcpPolicyId = mcpPolicyId;
        return this;
    }
    public String getMcpPolicyId() {
        return this.mcpPolicyId;
    }

    public CreateMcpSessionShrinkRequest setNetworkId(String networkId) {
        this.networkId = networkId;
        return this;
    }
    public String getNetworkId() {
        return this.networkId;
    }

    public CreateMcpSessionShrinkRequest setPersistenceDataListShrink(String persistenceDataListShrink) {
        this.persistenceDataListShrink = persistenceDataListShrink;
        return this;
    }
    public String getPersistenceDataListShrink() {
        return this.persistenceDataListShrink;
    }

    public CreateMcpSessionShrinkRequest setSdkStats(String sdkStats) {
        this.sdkStats = sdkStats;
        return this;
    }
    public String getSdkStats() {
        return this.sdkStats;
    }

    public CreateMcpSessionShrinkRequest setSessionId(String sessionId) {
        this.sessionId = sessionId;
        return this;
    }
    public String getSessionId() {
        return this.sessionId;
    }

    public CreateMcpSessionShrinkRequest setVpcResource(Boolean vpcResource) {
        this.vpcResource = vpcResource;
        return this;
    }
    public Boolean getVpcResource() {
        return this.vpcResource;
    }

}
