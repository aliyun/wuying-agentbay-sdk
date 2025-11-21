// This file is auto-generated, don't edit it. Thanks.
package com.aliyun.wuyingai20250506.models;

import com.aliyun.tea.*;

public class GetContextFileDownloadUrlResponse extends TeaModel {
    @NameInMap("headers")
    public java.util.Map<String, String> headers;

    @NameInMap("statusCode")
    public Integer statusCode;

    @NameInMap("body")
    public GetContextFileDownloadUrlResponseBody body;

    public static GetContextFileDownloadUrlResponse build(java.util.Map<String, ?> map) throws Exception {
        GetContextFileDownloadUrlResponse self = new GetContextFileDownloadUrlResponse();
        return TeaModel.build(map, self);
    }

    public GetContextFileDownloadUrlResponse setHeaders(java.util.Map<String, String> headers) {
        this.headers = headers;
        return this;
    }
    public java.util.Map<String, String> getHeaders() {
        return this.headers;
    }

    public GetContextFileDownloadUrlResponse setStatusCode(Integer statusCode) {
        this.statusCode = statusCode;
        return this;
    }
    public Integer getStatusCode() {
        return this.statusCode;
    }

    public GetContextFileDownloadUrlResponse setBody(GetContextFileDownloadUrlResponseBody body) {
        this.body = body;
        return this;
    }
    public GetContextFileDownloadUrlResponseBody getBody() {
        return this.body;
    }

}
