// This file is auto-generated, don't edit it. Thanks.
package com.aliyun.wuyingai20250506.models;

import com.aliyun.tea.*;

public class GetContextInfoResponse extends TeaModel {
    @NameInMap("headers")
    public java.util.Map<String, String> headers;

    @NameInMap("statusCode")
    public Integer statusCode;

    @NameInMap("body")
    public GetContextInfoResponseBody body;

    public static GetContextInfoResponse build(java.util.Map<String, ?> map) throws Exception {
        GetContextInfoResponse self = new GetContextInfoResponse();
        return TeaModel.build(map, self);
    }

    public GetContextInfoResponse setHeaders(java.util.Map<String, String> headers) {
        this.headers = headers;
        return this;
    }
    public java.util.Map<String, String> getHeaders() {
        return this.headers;
    }

    public GetContextInfoResponse setStatusCode(Integer statusCode) {
        this.statusCode = statusCode;
        return this;
    }
    public Integer getStatusCode() {
        return this.statusCode;
    }

    public GetContextInfoResponse setBody(GetContextInfoResponseBody body) {
        this.body = body;
        return this;
    }
    public GetContextInfoResponseBody getBody() {
        return this.body;
    }

}
