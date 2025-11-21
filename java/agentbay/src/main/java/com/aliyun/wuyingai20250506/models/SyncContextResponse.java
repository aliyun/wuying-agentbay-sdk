// This file is auto-generated, don't edit it. Thanks.
package com.aliyun.wuyingai20250506.models;

import com.aliyun.tea.*;

public class SyncContextResponse extends TeaModel {
    @NameInMap("headers")
    public java.util.Map<String, String> headers;

    @NameInMap("statusCode")
    public Integer statusCode;

    @NameInMap("body")
    public SyncContextResponseBody body;

    public static SyncContextResponse build(java.util.Map<String, ?> map) throws Exception {
        SyncContextResponse self = new SyncContextResponse();
        return TeaModel.build(map, self);
    }

    public SyncContextResponse setHeaders(java.util.Map<String, String> headers) {
        this.headers = headers;
        return this;
    }
    public java.util.Map<String, String> getHeaders() {
        return this.headers;
    }

    public SyncContextResponse setStatusCode(Integer statusCode) {
        this.statusCode = statusCode;
        return this;
    }
    public Integer getStatusCode() {
        return this.statusCode;
    }

    public SyncContextResponse setBody(SyncContextResponseBody body) {
        this.body = body;
        return this;
    }
    public SyncContextResponseBody getBody() {
        return this.body;
    }

}
