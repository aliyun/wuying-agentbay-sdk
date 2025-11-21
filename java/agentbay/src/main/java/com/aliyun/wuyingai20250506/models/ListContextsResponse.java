// This file is auto-generated, don't edit it. Thanks.
package com.aliyun.wuyingai20250506.models;

import com.aliyun.tea.*;

public class ListContextsResponse extends TeaModel {
    @NameInMap("headers")
    public java.util.Map<String, String> headers;

    @NameInMap("statusCode")
    public Integer statusCode;

    @NameInMap("body")
    public ListContextsResponseBody body;

    public static ListContextsResponse build(java.util.Map<String, ?> map) throws Exception {
        ListContextsResponse self = new ListContextsResponse();
        return TeaModel.build(map, self);
    }

    public ListContextsResponse setHeaders(java.util.Map<String, String> headers) {
        this.headers = headers;
        return this;
    }
    public java.util.Map<String, String> getHeaders() {
        return this.headers;
    }

    public ListContextsResponse setStatusCode(Integer statusCode) {
        this.statusCode = statusCode;
        return this;
    }
    public Integer getStatusCode() {
        return this.statusCode;
    }

    public ListContextsResponse setBody(ListContextsResponseBody body) {
        this.body = body;
        return this;
    }
    public ListContextsResponseBody getBody() {
        return this.body;
    }

}
