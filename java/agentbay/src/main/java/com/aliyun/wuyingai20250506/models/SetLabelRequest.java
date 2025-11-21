// This file is auto-generated, don't edit it. Thanks.
package com.aliyun.wuyingai20250506.models;

import com.aliyun.tea.*;

public class SetLabelRequest extends TeaModel {
    @NameInMap("Authorization")
    public String authorization;

    @NameInMap("Labels")
    public String labels;

    @NameInMap("SessionId")
    public String sessionId;

    public static SetLabelRequest build(java.util.Map<String, ?> map) throws Exception {
        SetLabelRequest self = new SetLabelRequest();
        return TeaModel.build(map, self);
    }

    public SetLabelRequest setAuthorization(String authorization) {
        this.authorization = authorization;
        return this;
    }
    public String getAuthorization() {
        return this.authorization;
    }

    public SetLabelRequest setLabels(String labels) {
        this.labels = labels;
        return this;
    }
    public String getLabels() {
        return this.labels;
    }

    public SetLabelRequest setSessionId(String sessionId) {
        this.sessionId = sessionId;
        return this;
    }
    public String getSessionId() {
        return this.sessionId;
    }

}
