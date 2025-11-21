// This file is auto-generated, don't edit it. Thanks.
package com.aliyun.wuyingai20250506.models;

import com.aliyun.tea.*;

public class ClearContextRequest extends TeaModel {
    @NameInMap("Authorization")
    public String authorization;

    @NameInMap("Id")
    public String id;

    public static ClearContextRequest build(java.util.Map<String, ?> map) throws Exception {
        ClearContextRequest self = new ClearContextRequest();
        return TeaModel.build(map, self);
    }

    public ClearContextRequest setAuthorization(String authorization) {
        this.authorization = authorization;
        return this;
    }
    public String getAuthorization() {
        return this.authorization;
    }

    public ClearContextRequest setId(String id) {
        this.id = id;
        return this;
    }
    public String getId() {
        return this.id;
    }

}
