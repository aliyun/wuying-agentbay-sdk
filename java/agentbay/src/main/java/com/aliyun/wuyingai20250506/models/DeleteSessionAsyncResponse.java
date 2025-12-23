// This file is auto-generated, don't edit it. Thanks.
package com.aliyun.wuyingai20250506.models;

import com.aliyun.tea.*;

public class DeleteSessionAsyncResponse extends TeaModel {
    @NameInMap("headers")
    public java.util.Map<String, String> headers;

    @NameInMap("statusCode")
    public Integer statusCode;

    @NameInMap("body")
    public DeleteSessionAsyncResponseBody body;

    public static DeleteSessionAsyncResponse build(java.util.Map<String, ?> map) throws Exception {
        DeleteSessionAsyncResponse self = new DeleteSessionAsyncResponse();
        return TeaModel.build(map, self);
    }

    public DeleteSessionAsyncResponse setHeaders(java.util.Map<String, String> headers) {
        this.headers = headers;
        return this;
    }
    public java.util.Map<String, String> getHeaders() {
        return this.headers;
    }

    public DeleteSessionAsyncResponse setStatusCode(Integer statusCode) {
        this.statusCode = statusCode;
        return this;
    }
    public Integer getStatusCode() {
        return this.statusCode;
    }

    public DeleteSessionAsyncResponse setBody(DeleteSessionAsyncResponseBody body) {
        this.body = body;
        return this;
    }
    public DeleteSessionAsyncResponseBody getBody() {
        return this.body;
    }

}
