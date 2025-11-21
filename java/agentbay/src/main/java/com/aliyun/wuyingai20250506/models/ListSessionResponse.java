// This file is auto-generated, don't edit it. Thanks.
package com.aliyun.wuyingai20250506.models;

import com.aliyun.tea.*;

public class ListSessionResponse extends TeaModel {
    @NameInMap("headers")
    public java.util.Map<String, String> headers;

    @NameInMap("statusCode")
    public Integer statusCode;

    @NameInMap("body")
    public ListSessionResponseBody body;

    public static ListSessionResponse build(java.util.Map<String, ?> map) throws Exception {
        ListSessionResponse self = new ListSessionResponse();
        return TeaModel.build(map, self);
    }

    public ListSessionResponse setHeaders(java.util.Map<String, String> headers) {
        this.headers = headers;
        return this;
    }
    public java.util.Map<String, String> getHeaders() {
        return this.headers;
    }

    public ListSessionResponse setStatusCode(Integer statusCode) {
        this.statusCode = statusCode;
        return this;
    }
    public Integer getStatusCode() {
        return this.statusCode;
    }

    public ListSessionResponse setBody(ListSessionResponseBody body) {
        this.body = body;
        return this;
    }
    public ListSessionResponseBody getBody() {
        return this.body;
    }

}
