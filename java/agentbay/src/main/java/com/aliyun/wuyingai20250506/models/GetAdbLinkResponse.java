// This file is auto-generated, don't edit it. Thanks.
package com.aliyun.wuyingai20250506.models;

import com.aliyun.tea.*;

public class GetAdbLinkResponse extends TeaModel {
    @NameInMap("headers")
    public java.util.Map<String, String> headers;

    @NameInMap("statusCode")
    public Integer statusCode;

    @NameInMap("body")
    public GetAdbLinkResponseBody body;

    public static GetAdbLinkResponse build(java.util.Map<String, ?> map) throws Exception {
        GetAdbLinkResponse self = new GetAdbLinkResponse();
        return TeaModel.build(map, self);
    }

    public GetAdbLinkResponse setHeaders(java.util.Map<String, String> headers) {
        this.headers = headers;
        return this;
    }
    public java.util.Map<String, String> getHeaders() {
        return this.headers;
    }

    public GetAdbLinkResponse setStatusCode(Integer statusCode) {
        this.statusCode = statusCode;
        return this;
    }
    public Integer getStatusCode() {
        return this.statusCode;
    }

    public GetAdbLinkResponse setBody(GetAdbLinkResponseBody body) {
        this.body = body;
        return this;
    }
    public GetAdbLinkResponseBody getBody() {
        return this.body;
    }

}
