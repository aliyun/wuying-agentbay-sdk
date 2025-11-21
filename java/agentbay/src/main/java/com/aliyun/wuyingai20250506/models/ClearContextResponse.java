// This file is auto-generated, don't edit it. Thanks.
package com.aliyun.wuyingai20250506.models;

import com.aliyun.tea.*;

public class ClearContextResponse extends TeaModel {
    @NameInMap("headers")
    public java.util.Map<String, String> headers;

    @NameInMap("statusCode")
    public Integer statusCode;

    @NameInMap("body")
    public ClearContextResponseBody body;

    public static ClearContextResponse build(java.util.Map<String, ?> map) throws Exception {
        ClearContextResponse self = new ClearContextResponse();
        return TeaModel.build(map, self);
    }

    public ClearContextResponse setHeaders(java.util.Map<String, String> headers) {
        this.headers = headers;
        return this;
    }
    public java.util.Map<String, String> getHeaders() {
        return this.headers;
    }

    public ClearContextResponse setStatusCode(Integer statusCode) {
        this.statusCode = statusCode;
        return this;
    }
    public Integer getStatusCode() {
        return this.statusCode;
    }

    public ClearContextResponse setBody(ClearContextResponseBody body) {
        this.body = body;
        return this;
    }
    public ClearContextResponseBody getBody() {
        return this.body;
    }

}
