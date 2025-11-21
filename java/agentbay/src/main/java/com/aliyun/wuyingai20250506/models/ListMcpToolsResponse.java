// This file is auto-generated, don't edit it. Thanks.
package com.aliyun.wuyingai20250506.models;

import com.aliyun.tea.*;

public class ListMcpToolsResponse extends TeaModel {
    @NameInMap("headers")
    public java.util.Map<String, String> headers;

    @NameInMap("statusCode")
    public Integer statusCode;

    @NameInMap("body")
    public ListMcpToolsResponseBody body;

    public static ListMcpToolsResponse build(java.util.Map<String, ?> map) throws Exception {
        ListMcpToolsResponse self = new ListMcpToolsResponse();
        return TeaModel.build(map, self);
    }

    public ListMcpToolsResponse setHeaders(java.util.Map<String, String> headers) {
        this.headers = headers;
        return this;
    }
    public java.util.Map<String, String> getHeaders() {
        return this.headers;
    }

    public ListMcpToolsResponse setStatusCode(Integer statusCode) {
        this.statusCode = statusCode;
        return this;
    }
    public Integer getStatusCode() {
        return this.statusCode;
    }

    public ListMcpToolsResponse setBody(ListMcpToolsResponseBody body) {
        this.body = body;
        return this;
    }
    public ListMcpToolsResponseBody getBody() {
        return this.body;
    }

}
