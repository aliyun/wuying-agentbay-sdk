// This file is auto-generated, don't edit it. Thanks.
package com.aliyun.wuyingai20250506.models;

import com.aliyun.tea.*;

public class DescribeContextFilesResponse extends TeaModel {
    @NameInMap("headers")
    public java.util.Map<String, String> headers;

    @NameInMap("statusCode")
    public Integer statusCode;

    @NameInMap("body")
    public DescribeContextFilesResponseBody body;

    public static DescribeContextFilesResponse build(java.util.Map<String, ?> map) throws Exception {
        DescribeContextFilesResponse self = new DescribeContextFilesResponse();
        return TeaModel.build(map, self);
    }

    public DescribeContextFilesResponse setHeaders(java.util.Map<String, String> headers) {
        this.headers = headers;
        return this;
    }
    public java.util.Map<String, String> getHeaders() {
        return this.headers;
    }

    public DescribeContextFilesResponse setStatusCode(Integer statusCode) {
        this.statusCode = statusCode;
        return this;
    }
    public Integer getStatusCode() {
        return this.statusCode;
    }

    public DescribeContextFilesResponse setBody(DescribeContextFilesResponseBody body) {
        this.body = body;
        return this;
    }
    public DescribeContextFilesResponseBody getBody() {
        return this.body;
    }

}
