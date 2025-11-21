// This file is auto-generated, don't edit it. Thanks.
package com.aliyun.wuyingai20250506.models;

import com.aliyun.tea.*;

public class DeleteContextResponse extends TeaModel {
    @NameInMap("headers")
    public java.util.Map<String, String> headers;

    @NameInMap("statusCode")
    public Integer statusCode;

    @NameInMap("body")
    public DeleteContextResponseBody body;

    public static DeleteContextResponse build(java.util.Map<String, ?> map) throws Exception {
        DeleteContextResponse self = new DeleteContextResponse();
        return TeaModel.build(map, self);
    }

    public DeleteContextResponse setHeaders(java.util.Map<String, String> headers) {
        this.headers = headers;
        return this;
    }
    public java.util.Map<String, String> getHeaders() {
        return this.headers;
    }

    public DeleteContextResponse setStatusCode(Integer statusCode) {
        this.statusCode = statusCode;
        return this;
    }
    public Integer getStatusCode() {
        return this.statusCode;
    }

    public DeleteContextResponse setBody(DeleteContextResponseBody body) {
        this.body = body;
        return this;
    }
    public DeleteContextResponseBody getBody() {
        return this.body;
    }

}
