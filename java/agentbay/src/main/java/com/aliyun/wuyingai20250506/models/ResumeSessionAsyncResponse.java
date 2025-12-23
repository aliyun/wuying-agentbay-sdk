// This file is auto-generated, don't edit it. Thanks.
package com.aliyun.wuyingai20250506.models;

import com.aliyun.tea.*;

public class ResumeSessionAsyncResponse extends TeaModel {
    @NameInMap("headers")
    public java.util.Map<String, String> headers;

    @NameInMap("statusCode")
    public Integer statusCode;

    @NameInMap("body")
    public ResumeSessionAsyncResponseBody body;

    public static ResumeSessionAsyncResponse build(java.util.Map<String, ?> map) throws Exception {
        ResumeSessionAsyncResponse self = new ResumeSessionAsyncResponse();
        return TeaModel.build(map, self);
    }

    public ResumeSessionAsyncResponse setHeaders(java.util.Map<String, String> headers) {
        this.headers = headers;
        return this;
    }
    public java.util.Map<String, String> getHeaders() {
        return this.headers;
    }

    public ResumeSessionAsyncResponse setStatusCode(Integer statusCode) {
        this.statusCode = statusCode;
        return this;
    }
    public Integer getStatusCode() {
        return this.statusCode;
    }

    public ResumeSessionAsyncResponse setBody(ResumeSessionAsyncResponseBody body) {
        this.body = body;
        return this;
    }
    public ResumeSessionAsyncResponseBody getBody() {
        return this.body;
    }

}
