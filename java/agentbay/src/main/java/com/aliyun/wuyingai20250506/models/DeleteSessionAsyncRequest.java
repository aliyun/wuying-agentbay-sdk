// This file is auto-generated, don't edit it. Thanks.
package com.aliyun.wuyingai20250506.models;

import com.aliyun.tea.*;

public class DeleteSessionAsyncRequest extends TeaModel {
    @NameInMap("Authorization")
    public String authorization;

    @NameInMap("SessionId")
    public String sessionId;

    public static DeleteSessionAsyncRequest build(java.util.Map<String, ?> map) throws Exception {
        DeleteSessionAsyncRequest self = new DeleteSessionAsyncRequest();
        return TeaModel.build(map, self);
    }

    public DeleteSessionAsyncRequest setAuthorization(String authorization) {
        this.authorization = authorization;
        return this;
    }
    public String getAuthorization() {
        return this.authorization;
    }

    public DeleteSessionAsyncRequest setSessionId(String sessionId) {
        this.sessionId = sessionId;
        return this;
    }
    public String getSessionId() {
        return this.sessionId;
    }

}
