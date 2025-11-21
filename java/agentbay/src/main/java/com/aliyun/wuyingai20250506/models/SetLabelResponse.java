// This file is auto-generated, don't edit it. Thanks.
package com.aliyun.wuyingai20250506.models;

import com.aliyun.tea.*;

public class SetLabelResponse extends TeaModel {
    @NameInMap("headers")
    public java.util.Map<String, String> headers;

    @NameInMap("statusCode")
    public Integer statusCode;

    @NameInMap("body")
    public SetLabelResponseBody body;

    public static SetLabelResponse build(java.util.Map<String, ?> map) throws Exception {
        SetLabelResponse self = new SetLabelResponse();
        return TeaModel.build(map, self);
    }

    public SetLabelResponse setHeaders(java.util.Map<String, String> headers) {
        this.headers = headers;
        return this;
    }
    public java.util.Map<String, String> getHeaders() {
        return this.headers;
    }

    public SetLabelResponse setStatusCode(Integer statusCode) {
        this.statusCode = statusCode;
        return this;
    }
    public Integer getStatusCode() {
        return this.statusCode;
    }

    public SetLabelResponse setBody(SetLabelResponseBody body) {
        this.body = body;
        return this;
    }
    public SetLabelResponseBody getBody() {
        return this.body;
    }

}
