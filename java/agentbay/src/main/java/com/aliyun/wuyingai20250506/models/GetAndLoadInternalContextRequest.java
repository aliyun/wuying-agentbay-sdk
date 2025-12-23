// This file is auto-generated, don't edit it. Thanks.
package com.aliyun.wuyingai20250506.models;

import com.aliyun.tea.*;

public class GetAndLoadInternalContextRequest extends TeaModel {
    @NameInMap("Authorization")
    public String authorization;

    @NameInMap("ContextTypes")
    public java.util.List<String> contextTypes;

    @NameInMap("SessionId")
    public String sessionId;

    public static GetAndLoadInternalContextRequest build(java.util.Map<String, ?> map) throws Exception {
        GetAndLoadInternalContextRequest self = new GetAndLoadInternalContextRequest();
        return TeaModel.build(map, self);
    }

    public GetAndLoadInternalContextRequest setAuthorization(String authorization) {
        this.authorization = authorization;
        return this;
    }
    public String getAuthorization() {
        return this.authorization;
    }

    public GetAndLoadInternalContextRequest setContextTypes(java.util.List<String> contextTypes) {
        this.contextTypes = contextTypes;
        return this;
    }
    public java.util.List<String> getContextTypes() {
        return this.contextTypes;
    }

    public GetAndLoadInternalContextRequest setSessionId(String sessionId) {
        this.sessionId = sessionId;
        return this;
    }
    public String getSessionId() {
        return this.sessionId;
    }

}
