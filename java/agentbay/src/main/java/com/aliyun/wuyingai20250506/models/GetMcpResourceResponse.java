// This file is auto-generated, don't edit it. Thanks.
package com.aliyun.wuyingai20250506.models;

import com.aliyun.tea.*;

public class GetMcpResourceResponse extends TeaModel {
    @NameInMap("headers")
    public java.util.Map<String, String> headers;

    @NameInMap("statusCode")
    public Integer statusCode;

    @NameInMap("body")
    public GetMcpResourceResponseBody body;

    public static GetMcpResourceResponse build(java.util.Map<String, ?> map) throws Exception {
        GetMcpResourceResponse self = new GetMcpResourceResponse();
        return TeaModel.build(map, self);
    }

    public GetMcpResourceResponse setHeaders(java.util.Map<String, String> headers) {
        this.headers = headers;
        return this;
    }
    public java.util.Map<String, String> getHeaders() {
        return this.headers;
    }

    public GetMcpResourceResponse setStatusCode(Integer statusCode) {
        this.statusCode = statusCode;
        return this;
    }
    public Integer getStatusCode() {
        return this.statusCode;
    }

    public GetMcpResourceResponse setBody(GetMcpResourceResponseBody body) {
        this.body = body;
        return this;
    }
    public GetMcpResourceResponseBody getBody() {
        return this.body;
    }

}
