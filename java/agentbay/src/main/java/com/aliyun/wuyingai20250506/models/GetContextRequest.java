// This file is auto-generated, don't edit it. Thanks.
package com.aliyun.wuyingai20250506.models;

import com.aliyun.tea.*;

public class GetContextRequest extends TeaModel {
    @NameInMap("AllowCreate")
    public Boolean allowCreate;

    @NameInMap("Authorization")
    public String authorization;

    @NameInMap("ContextId")
    public String contextId;

    @NameInMap("LoginRegionId")
    public String loginRegionId;

    @NameInMap("Name")
    public String name;

    public static GetContextRequest build(java.util.Map<String, ?> map) throws Exception {
        GetContextRequest self = new GetContextRequest();
        return TeaModel.build(map, self);
    }

    public GetContextRequest setAllowCreate(Boolean allowCreate) {
        this.allowCreate = allowCreate;
        return this;
    }
    public Boolean getAllowCreate() {
        return this.allowCreate;
    }

    public GetContextRequest setAuthorization(String authorization) {
        this.authorization = authorization;
        return this;
    }
    public String getAuthorization() {
        return this.authorization;
    }

    public GetContextRequest setContextId(String contextId) {
        this.contextId = contextId;
        return this;
    }
    public String getContextId() {
        return this.contextId;
    }

    public GetContextRequest setLoginRegionId(String loginRegionId) {
        this.loginRegionId = loginRegionId;
        return this;
    }
    public String getLoginRegionId() {
        return this.loginRegionId;
    }

    public GetContextRequest setName(String name) {
        this.name = name;
        return this;
    }
    public String getName() {
        return this.name;
    }

}
