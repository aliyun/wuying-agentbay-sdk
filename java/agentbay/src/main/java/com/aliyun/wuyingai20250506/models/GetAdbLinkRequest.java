// This file is auto-generated, don't edit it. Thanks.
package com.aliyun.wuyingai20250506.models;

import com.aliyun.tea.*;

public class GetAdbLinkRequest extends TeaModel {
    @NameInMap("Authorization")
    public String authorization;

    @NameInMap("Option")
    public String option;

    @NameInMap("SessionId")
    public String sessionId;

    public static GetAdbLinkRequest build(java.util.Map<String, ?> map) throws Exception {
        GetAdbLinkRequest self = new GetAdbLinkRequest();
        return TeaModel.build(map, self);
    }

    public GetAdbLinkRequest setAuthorization(String authorization) {
        this.authorization = authorization;
        return this;
    }
    public String getAuthorization() {
        return this.authorization;
    }

    public GetAdbLinkRequest setOption(String option) {
        this.option = option;
        return this;
    }
    public String getOption() {
        return this.option;
    }

    public GetAdbLinkRequest setSessionId(String sessionId) {
        this.sessionId = sessionId;
        return this;
    }
    public String getSessionId() {
        return this.sessionId;
    }

}
