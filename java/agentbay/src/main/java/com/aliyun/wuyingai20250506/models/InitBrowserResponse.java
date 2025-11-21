// This file is auto-generated, don't edit it. Thanks.
package com.aliyun.wuyingai20250506.models;

import com.aliyun.tea.*;

public class InitBrowserResponse extends TeaModel {
    @NameInMap("headers")
    public java.util.Map<String, String> headers;

    @NameInMap("statusCode")
    public Integer statusCode;

    @NameInMap("body")
    public InitBrowserResponseBody body;

    public static InitBrowserResponse build(java.util.Map<String, ?> map) throws Exception {
        InitBrowserResponse self = new InitBrowserResponse();
        return TeaModel.build(map, self);
    }

    public InitBrowserResponse setHeaders(java.util.Map<String, String> headers) {
        this.headers = headers;
        return this;
    }
    public java.util.Map<String, String> getHeaders() {
        return this.headers;
    }

    public InitBrowserResponse setStatusCode(Integer statusCode) {
        this.statusCode = statusCode;
        return this;
    }
    public Integer getStatusCode() {
        return this.statusCode;
    }

    public InitBrowserResponse setBody(InitBrowserResponseBody body) {
        this.body = body;
        return this;
    }
    public InitBrowserResponseBody getBody() {
        return this.body;
    }

}
