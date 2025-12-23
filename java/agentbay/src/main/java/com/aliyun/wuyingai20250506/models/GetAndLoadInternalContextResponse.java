// This file is auto-generated, don't edit it. Thanks.
package com.aliyun.wuyingai20250506.models;

import com.aliyun.tea.*;

public class GetAndLoadInternalContextResponse extends TeaModel {
    @NameInMap("headers")
    public java.util.Map<String, String> headers;

    @NameInMap("statusCode")
    public Integer statusCode;

    @NameInMap("body")
    public GetAndLoadInternalContextResponseBody body;

    public static GetAndLoadInternalContextResponse build(java.util.Map<String, ?> map) throws Exception {
        GetAndLoadInternalContextResponse self = new GetAndLoadInternalContextResponse();
        return TeaModel.build(map, self);
    }

    public GetAndLoadInternalContextResponse setHeaders(java.util.Map<String, String> headers) {
        this.headers = headers;
        return this;
    }
    public java.util.Map<String, String> getHeaders() {
        return this.headers;
    }

    public GetAndLoadInternalContextResponse setStatusCode(Integer statusCode) {
        this.statusCode = statusCode;
        return this;
    }
    public Integer getStatusCode() {
        return this.statusCode;
    }

    public GetAndLoadInternalContextResponse setBody(GetAndLoadInternalContextResponseBody body) {
        this.body = body;
        return this;
    }
    public GetAndLoadInternalContextResponseBody getBody() {
        return this.body;
    }

}
