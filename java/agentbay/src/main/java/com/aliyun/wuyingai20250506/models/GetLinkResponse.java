// This file is auto-generated, don't edit it. Thanks.
package com.aliyun.wuyingai20250506.models;

import com.aliyun.tea.*;

public class GetLinkResponse extends TeaModel {
    @NameInMap("headers")
    public java.util.Map<String, String> headers;

    @NameInMap("statusCode")
    public Integer statusCode;

    @NameInMap("body")
    public GetLinkResponseBody body;

    public static GetLinkResponse build(java.util.Map<String, ?> map) throws Exception {
        GetLinkResponse self = new GetLinkResponse();
        return TeaModel.build(map, self);
    }

    public GetLinkResponse setHeaders(java.util.Map<String, String> headers) {
        this.headers = headers;
        return this;
    }
    public java.util.Map<String, String> getHeaders() {
        return this.headers;
    }

    public GetLinkResponse setStatusCode(Integer statusCode) {
        this.statusCode = statusCode;
        return this;
    }
    public Integer getStatusCode() {
        return this.statusCode;
    }

    public GetLinkResponse setBody(GetLinkResponseBody body) {
        this.body = body;
        return this;
    }
    public GetLinkResponseBody getBody() {
        return this.body;
    }

}
