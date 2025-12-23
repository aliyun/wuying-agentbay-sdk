// This file is auto-generated, don't edit it. Thanks.
package com.aliyun.wuyingai20250506.models;

import com.aliyun.tea.*;

public class PauseSessionAsyncResponse extends TeaModel {
    @NameInMap("headers")
    public java.util.Map<String, String> headers;

    @NameInMap("statusCode")
    public Integer statusCode;

    @NameInMap("body")
    public PauseSessionAsyncResponseBody body;

    public static PauseSessionAsyncResponse build(java.util.Map<String, ?> map) throws Exception {
        PauseSessionAsyncResponse self = new PauseSessionAsyncResponse();
        return TeaModel.build(map, self);
    }

    public PauseSessionAsyncResponse setHeaders(java.util.Map<String, String> headers) {
        this.headers = headers;
        return this;
    }
    public java.util.Map<String, String> getHeaders() {
        return this.headers;
    }

    public PauseSessionAsyncResponse setStatusCode(Integer statusCode) {
        this.statusCode = statusCode;
        return this;
    }
    public Integer getStatusCode() {
        return this.statusCode;
    }

    public PauseSessionAsyncResponse setBody(PauseSessionAsyncResponseBody body) {
        this.body = body;
        return this;
    }
    public PauseSessionAsyncResponseBody getBody() {
        return this.body;
    }

}
