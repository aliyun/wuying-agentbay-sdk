// This file is auto-generated, don't edit it. Thanks.
package com.aliyun.wuyingai20250506.models;

import com.aliyun.tea.*;

public class ReleaseMcpSessionResponse extends TeaModel {
    @NameInMap("headers")
    public java.util.Map<String, String> headers;

    @NameInMap("statusCode")
    public Integer statusCode;

    @NameInMap("body")
    public ReleaseMcpSessionResponseBody body;

    public static ReleaseMcpSessionResponse build(java.util.Map<String, ?> map) throws Exception {
        ReleaseMcpSessionResponse self = new ReleaseMcpSessionResponse();
        return TeaModel.build(map, self);
    }

    public ReleaseMcpSessionResponse setHeaders(java.util.Map<String, String> headers) {
        this.headers = headers;
        return this;
    }
    public java.util.Map<String, String> getHeaders() {
        return this.headers;
    }

    public ReleaseMcpSessionResponse setStatusCode(Integer statusCode) {
        this.statusCode = statusCode;
        return this;
    }
    public Integer getStatusCode() {
        return this.statusCode;
    }

    public ReleaseMcpSessionResponse setBody(ReleaseMcpSessionResponseBody body) {
        this.body = body;
        return this;
    }
    public ReleaseMcpSessionResponseBody getBody() {
        return this.body;
    }

}
