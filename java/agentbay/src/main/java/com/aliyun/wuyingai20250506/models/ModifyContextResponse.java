// This file is auto-generated, don't edit it. Thanks.
package com.aliyun.wuyingai20250506.models;

import com.aliyun.tea.*;

public class ModifyContextResponse extends TeaModel {
    @NameInMap("headers")
    public java.util.Map<String, String> headers;

    @NameInMap("statusCode")
    public Integer statusCode;

    @NameInMap("body")
    public ModifyContextResponseBody body;

    public static ModifyContextResponse build(java.util.Map<String, ?> map) throws Exception {
        ModifyContextResponse self = new ModifyContextResponse();
        return TeaModel.build(map, self);
    }

    public ModifyContextResponse setHeaders(java.util.Map<String, String> headers) {
        this.headers = headers;
        return this;
    }
    public java.util.Map<String, String> getHeaders() {
        return this.headers;
    }

    public ModifyContextResponse setStatusCode(Integer statusCode) {
        this.statusCode = statusCode;
        return this;
    }
    public Integer getStatusCode() {
        return this.statusCode;
    }

    public ModifyContextResponse setBody(ModifyContextResponseBody body) {
        this.body = body;
        return this;
    }
    public ModifyContextResponseBody getBody() {
        return this.body;
    }

}
