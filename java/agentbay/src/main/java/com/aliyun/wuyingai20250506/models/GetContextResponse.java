// This file is auto-generated, don't edit it. Thanks.
package com.aliyun.wuyingai20250506.models;

import com.aliyun.tea.*;

public class GetContextResponse extends TeaModel {
    @NameInMap("headers")
    public java.util.Map<String, String> headers;

    @NameInMap("statusCode")
    public Integer statusCode;

    @NameInMap("body")
    public GetContextResponseBody body;

    public static GetContextResponse build(java.util.Map<String, ?> map) throws Exception {
        GetContextResponse self = new GetContextResponse();
        return TeaModel.build(map, self);
    }

    public GetContextResponse setHeaders(java.util.Map<String, String> headers) {
        this.headers = headers;
        return this;
    }
    public java.util.Map<String, String> getHeaders() {
        return this.headers;
    }

    public GetContextResponse setStatusCode(Integer statusCode) {
        this.statusCode = statusCode;
        return this;
    }
    public Integer getStatusCode() {
        return this.statusCode;
    }

    public GetContextResponse setBody(GetContextResponseBody body) {
        this.body = body;
        return this;
    }
    public GetContextResponseBody getBody() {
        return this.body;
    }

}
