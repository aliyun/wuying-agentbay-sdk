// This file is auto-generated, don't edit it. Thanks.
package com.aliyun.wuyingai20250506.models;

import com.aliyun.tea.*;

public class ModifyContextRequest extends TeaModel {
    @NameInMap("Authorization")
    public String authorization;

    @NameInMap("Id")
    public String id;

    @NameInMap("Name")
    public String name;

    public static ModifyContextRequest build(java.util.Map<String, ?> map) throws Exception {
        ModifyContextRequest self = new ModifyContextRequest();
        return TeaModel.build(map, self);
    }

    public ModifyContextRequest setAuthorization(String authorization) {
        this.authorization = authorization;
        return this;
    }
    public String getAuthorization() {
        return this.authorization;
    }

    public ModifyContextRequest setId(String id) {
        this.id = id;
        return this;
    }
    public String getId() {
        return this.id;
    }

    public ModifyContextRequest setName(String name) {
        this.name = name;
        return this;
    }
    public String getName() {
        return this.name;
    }

}
