// This file is auto-generated, don't edit it. Thanks.
package com.aliyun.wuyingai20250506.models;

import com.aliyun.tea.*;

public class GetContextFileUploadUrlResponse extends TeaModel {
    @NameInMap("headers")
    public java.util.Map<String, String> headers;

    @NameInMap("statusCode")
    public Integer statusCode;

    @NameInMap("body")
    public GetContextFileUploadUrlResponseBody body;

    public static GetContextFileUploadUrlResponse build(java.util.Map<String, ?> map) throws Exception {
        GetContextFileUploadUrlResponse self = new GetContextFileUploadUrlResponse();
        return TeaModel.build(map, self);
    }

    public GetContextFileUploadUrlResponse setHeaders(java.util.Map<String, String> headers) {
        this.headers = headers;
        return this;
    }
    public java.util.Map<String, String> getHeaders() {
        return this.headers;
    }

    public GetContextFileUploadUrlResponse setStatusCode(Integer statusCode) {
        this.statusCode = statusCode;
        return this;
    }
    public Integer getStatusCode() {
        return this.statusCode;
    }

    public GetContextFileUploadUrlResponse setBody(GetContextFileUploadUrlResponseBody body) {
        this.body = body;
        return this;
    }
    public GetContextFileUploadUrlResponseBody getBody() {
        return this.body;
    }

}
