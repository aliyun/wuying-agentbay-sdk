// This file is auto-generated, don't edit it. Thanks.
package com.aliyun.wuyingai20250506.models;

import com.aliyun.tea.*;

public class DeleteContextRequest extends TeaModel {
    @NameInMap("Authorization")
    public String authorization;

    @NameInMap("Id")
    public String id;

    public static DeleteContextRequest build(java.util.Map<String, ?> map) throws Exception {
        DeleteContextRequest self = new DeleteContextRequest();
        return TeaModel.build(map, self);
    }

    public DeleteContextRequest setAuthorization(String authorization) {
        this.authorization = authorization;
        return this;
    }
    public String getAuthorization() {
        return this.authorization;
    }

    public DeleteContextRequest setId(String id) {
        this.id = id;
        return this;
    }
    public String getId() {
        return this.id;
    }

}
