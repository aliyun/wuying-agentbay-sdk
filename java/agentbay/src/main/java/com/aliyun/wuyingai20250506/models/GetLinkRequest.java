// This file is auto-generated, don't edit it. Thanks.
package com.aliyun.wuyingai20250506.models;

import com.aliyun.tea.*;

public class GetLinkRequest extends TeaModel {
    @NameInMap("Authorization")
    public String authorization;

    @NameInMap("Option")
    public String option;

    @NameInMap("Port")
    public Integer port;

    @NameInMap("ProtocolType")
    public String protocolType;

    @NameInMap("SessionId")
    public String sessionId;

    public static GetLinkRequest build(java.util.Map<String, ?> map) throws Exception {
        GetLinkRequest self = new GetLinkRequest();
        return TeaModel.build(map, self);
    }

    public GetLinkRequest setAuthorization(String authorization) {
        this.authorization = authorization;
        return this;
    }
    public String getAuthorization() {
        return this.authorization;
    }

    public GetLinkRequest setOption(String option) {
        this.option = option;
        return this;
    }
    public String getOption() {
        return this.option;
    }

    public GetLinkRequest setPort(Integer port) {
        this.port = port;
        return this;
    }
    public Integer getPort() {
        return this.port;
    }

    public GetLinkRequest setProtocolType(String protocolType) {
        this.protocolType = protocolType;
        return this;
    }
    public String getProtocolType() {
        return this.protocolType;
    }

    public GetLinkRequest setSessionId(String sessionId) {
        this.sessionId = sessionId;
        return this;
    }
    public String getSessionId() {
        return this.sessionId;
    }

}
