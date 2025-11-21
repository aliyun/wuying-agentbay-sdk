// This file is auto-generated, don't edit it. Thanks.
package com.aliyun.wuyingai20250506.models;

import com.aliyun.tea.*;

public class DescribeNetworkResponse extends TeaModel {
    @NameInMap("headers")
    public java.util.Map<String, String> headers;

    @NameInMap("statusCode")
    public Integer statusCode;

    @NameInMap("body")
    public DescribeNetworkResponseBody body;

    public static DescribeNetworkResponse build(java.util.Map<String, ?> map) throws Exception {
        DescribeNetworkResponse self = new DescribeNetworkResponse();
        return TeaModel.build(map, self);
    }

    public DescribeNetworkResponse setHeaders(java.util.Map<String, String> headers) {
        this.headers = headers;
        return this;
    }
    public java.util.Map<String, String> getHeaders() {
        return this.headers;
    }

    public DescribeNetworkResponse setStatusCode(Integer statusCode) {
        this.statusCode = statusCode;
        return this;
    }
    public Integer getStatusCode() {
        return this.statusCode;
    }

    public DescribeNetworkResponse setBody(DescribeNetworkResponseBody body) {
        this.body = body;
        return this;
    }
    public DescribeNetworkResponseBody getBody() {
        return this.body;
    }

}
