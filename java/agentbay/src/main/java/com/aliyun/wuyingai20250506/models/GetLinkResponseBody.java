// This file is auto-generated, don't edit it. Thanks.
package com.aliyun.wuyingai20250506.models;

import com.aliyun.tea.*;

public class GetLinkResponseBody extends TeaModel {
    @NameInMap("Code")
    public String code;

    @NameInMap("Data")
    public GetLinkResponseBodyData data;

    @NameInMap("HttpStatusCode")
    public Integer httpStatusCode;

    @NameInMap("Message")
    public String message;

    @NameInMap("RequestId")
    public String requestId;

    @NameInMap("Success")
    public Boolean success;

    public static GetLinkResponseBody build(java.util.Map<String, ?> map) throws Exception {
        GetLinkResponseBody self = new GetLinkResponseBody();
        return TeaModel.build(map, self);
    }

    public GetLinkResponseBody setCode(String code) {
        this.code = code;
        return this;
    }
    public String getCode() {
        return this.code;
    }

    public GetLinkResponseBody setData(GetLinkResponseBodyData data) {
        this.data = data;
        return this;
    }
    public GetLinkResponseBodyData getData() {
        return this.data;
    }

    public GetLinkResponseBody setHttpStatusCode(Integer httpStatusCode) {
        this.httpStatusCode = httpStatusCode;
        return this;
    }
    public Integer getHttpStatusCode() {
        return this.httpStatusCode;
    }

    public GetLinkResponseBody setMessage(String message) {
        this.message = message;
        return this;
    }
    public String getMessage() {
        return this.message;
    }

    public GetLinkResponseBody setRequestId(String requestId) {
        this.requestId = requestId;
        return this;
    }
    public String getRequestId() {
        return this.requestId;
    }

    public GetLinkResponseBody setSuccess(Boolean success) {
        this.success = success;
        return this;
    }
    public Boolean getSuccess() {
        return this.success;
    }

    public static class GetLinkResponseBodyData extends TeaModel {
        @NameInMap("Url")
        public String url;

        public static GetLinkResponseBodyData build(java.util.Map<String, ?> map) throws Exception {
            GetLinkResponseBodyData self = new GetLinkResponseBodyData();
            return TeaModel.build(map, self);
        }

        public GetLinkResponseBodyData setUrl(String url) {
            this.url = url;
            return this;
        }
        public String getUrl() {
            return this.url;
        }

    }

}
