// This file is auto-generated, don't edit it. Thanks.
package com.aliyun.wuyingai20250506.models;

import com.aliyun.tea.*;

public class CreateMcpSessionResponse extends TeaModel {
    @NameInMap("headers")
    public java.util.Map<String, String> headers;

    @NameInMap("statusCode")
    public Integer statusCode;

    @NameInMap("body")
    public CreateMcpSessionResponseBody body;

    public static CreateMcpSessionResponse build(java.util.Map<String, ?> map) throws Exception {
        CreateMcpSessionResponse self = new CreateMcpSessionResponse();
        return TeaModel.build(map, self);
    }

    public CreateMcpSessionResponse setHeaders(java.util.Map<String, String> headers) {
        this.headers = headers;
        return this;
    }
    public java.util.Map<String, String> getHeaders() {
        return this.headers;
    }

    public CreateMcpSessionResponse setStatusCode(Integer statusCode) {
        this.statusCode = statusCode;
        return this;
    }
    public Integer getStatusCode() {
        return this.statusCode;
    }

    public CreateMcpSessionResponse setBody(CreateMcpSessionResponseBody body) {
        this.body = body;
        return this;
    }
    public CreateMcpSessionResponseBody getBody() {
        return this.body;
    }

}
