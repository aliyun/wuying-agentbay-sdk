// This file is auto-generated, don't edit it. Thanks.
package com.aliyun.wuyingai20250506.models;

import com.aliyun.tea.*;

public class GetLabelResponse extends TeaModel {
    @NameInMap("headers")
    public java.util.Map<String, String> headers;

    @NameInMap("statusCode")
    public Integer statusCode;

    @NameInMap("body")
    public GetLabelResponseBody body;

    public static GetLabelResponse build(java.util.Map<String, ?> map) throws Exception {
        GetLabelResponse self = new GetLabelResponse();
        return TeaModel.build(map, self);
    }

    public GetLabelResponse setHeaders(java.util.Map<String, String> headers) {
        this.headers = headers;
        return this;
    }
    public java.util.Map<String, String> getHeaders() {
        return this.headers;
    }

    public GetLabelResponse setStatusCode(Integer statusCode) {
        this.statusCode = statusCode;
        return this;
    }
    public Integer getStatusCode() {
        return this.statusCode;
    }

    public GetLabelResponse setBody(GetLabelResponseBody body) {
        this.body = body;
        return this;
    }
    public GetLabelResponseBody getBody() {
        return this.body;
    }

}
