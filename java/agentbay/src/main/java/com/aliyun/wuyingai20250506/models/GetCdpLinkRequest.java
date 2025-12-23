// This file is auto-generated, don't edit it. Thanks.
package com.aliyun.wuyingai20250506.models;

import com.aliyun.tea.*;

public class GetCdpLinkRequest extends TeaModel {
    @NameInMap("Authorization")
    public String authorization;

    @NameInMap("SessionId")
    public String sessionId;

    public static GetCdpLinkRequest build(java.util.Map<String, ?> map) throws Exception {
        GetCdpLinkRequest self = new GetCdpLinkRequest();
        return TeaModel.build(map, self);
    }

    public GetCdpLinkRequest setAuthorization(String authorization) {
        this.authorization = authorization;
        return this;
    }
    public String getAuthorization() {
        return this.authorization;
    }

    public GetCdpLinkRequest setSessionId(String sessionId) {
        this.sessionId = sessionId;
        return this;
    }
    public String getSessionId() {
        return this.sessionId;
    }

}
