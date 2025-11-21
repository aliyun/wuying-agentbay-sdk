// This file is auto-generated, don't edit it. Thanks.
package com.aliyun.wuyingai20250506.models;

import com.aliyun.tea.*;

public class CallMcpToolResponse extends TeaModel {
    @NameInMap("headers")
    public java.util.Map<String, String> headers;

    @NameInMap("statusCode")
    public Integer statusCode;

    @NameInMap("body")
    public CallMcpToolResponseBody body;

    public static CallMcpToolResponse build(java.util.Map<String, ?> map) throws Exception {
        CallMcpToolResponse self = new CallMcpToolResponse();
        return TeaModel.build(map, self);
    }

    public CallMcpToolResponse setHeaders(java.util.Map<String, String> headers) {
        this.headers = headers;
        return this;
    }
    public java.util.Map<String, String> getHeaders() {
        return this.headers;
    }

    public CallMcpToolResponse setStatusCode(Integer statusCode) {
        this.statusCode = statusCode;
        return this;
    }
    public Integer getStatusCode() {
        return this.statusCode;
    }

    public CallMcpToolResponse setBody(CallMcpToolResponseBody body) {
        this.body = body;
        return this;
    }
    public CallMcpToolResponseBody getBody() {
        return this.body;
    }

}
