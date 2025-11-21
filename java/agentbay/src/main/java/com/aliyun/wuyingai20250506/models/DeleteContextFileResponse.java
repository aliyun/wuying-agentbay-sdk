// This file is auto-generated, don't edit it. Thanks.
package com.aliyun.wuyingai20250506.models;

import com.aliyun.tea.*;

public class DeleteContextFileResponse extends TeaModel {
    @NameInMap("headers")
    public java.util.Map<String, String> headers;

    @NameInMap("statusCode")
    public Integer statusCode;

    @NameInMap("body")
    public DeleteContextFileResponseBody body;

    public static DeleteContextFileResponse build(java.util.Map<String, ?> map) throws Exception {
        DeleteContextFileResponse self = new DeleteContextFileResponse();
        return TeaModel.build(map, self);
    }

    public DeleteContextFileResponse setHeaders(java.util.Map<String, String> headers) {
        this.headers = headers;
        return this;
    }
    public java.util.Map<String, String> getHeaders() {
        return this.headers;
    }

    public DeleteContextFileResponse setStatusCode(Integer statusCode) {
        this.statusCode = statusCode;
        return this;
    }
    public Integer getStatusCode() {
        return this.statusCode;
    }

    public DeleteContextFileResponse setBody(DeleteContextFileResponseBody body) {
        this.body = body;
        return this;
    }
    public DeleteContextFileResponseBody getBody() {
        return this.body;
    }

}
