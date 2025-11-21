// This file is auto-generated, don't edit it. Thanks.
package com.aliyun.wuyingai20250506.models;

import com.aliyun.tea.*;

public class CreateNetworkResponse extends TeaModel {
    @NameInMap("headers")
    public java.util.Map<String, String> headers;

    @NameInMap("statusCode")
    public Integer statusCode;

    @NameInMap("body")
    public CreateNetworkResponseBody body;

    public static CreateNetworkResponse build(java.util.Map<String, ?> map) throws Exception {
        CreateNetworkResponse self = new CreateNetworkResponse();
        return TeaModel.build(map, self);
    }

    public CreateNetworkResponse setHeaders(java.util.Map<String, String> headers) {
        this.headers = headers;
        return this;
    }
    public java.util.Map<String, String> getHeaders() {
        return this.headers;
    }

    public CreateNetworkResponse setStatusCode(Integer statusCode) {
        this.statusCode = statusCode;
        return this;
    }
    public Integer getStatusCode() {
        return this.statusCode;
    }

    public CreateNetworkResponse setBody(CreateNetworkResponseBody body) {
        this.body = body;
        return this;
    }
    public CreateNetworkResponseBody getBody() {
        return this.body;
    }

}
