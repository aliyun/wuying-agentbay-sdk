// This file is auto-generated, don't edit it. Thanks.
package com.aliyun.wuyingai20250506.models;

import com.aliyun.tea.*;

public class GetCdpLinkResponse extends TeaModel {
    @NameInMap("headers")
    public java.util.Map<String, String> headers;

    @NameInMap("statusCode")
    public Integer statusCode;

    @NameInMap("body")
    public GetCdpLinkResponseBody body;

    public static GetCdpLinkResponse build(java.util.Map<String, ?> map) throws Exception {
        GetCdpLinkResponse self = new GetCdpLinkResponse();
        return TeaModel.build(map, self);
    }

    public GetCdpLinkResponse setHeaders(java.util.Map<String, String> headers) {
        this.headers = headers;
        return this;
    }
    public java.util.Map<String, String> getHeaders() {
        return this.headers;
    }

    public GetCdpLinkResponse setStatusCode(Integer statusCode) {
        this.statusCode = statusCode;
        return this;
    }
    public Integer getStatusCode() {
        return this.statusCode;
    }

    public GetCdpLinkResponse setBody(GetCdpLinkResponseBody body) {
        this.body = body;
        return this;
    }
    public GetCdpLinkResponseBody getBody() {
        return this.body;
    }

}
