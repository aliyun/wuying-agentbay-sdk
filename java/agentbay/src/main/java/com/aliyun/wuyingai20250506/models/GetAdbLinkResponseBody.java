// This file is auto-generated, don't edit it. Thanks.
package com.aliyun.wuyingai20250506.models;

import com.aliyun.tea.*;

public class GetAdbLinkResponseBody extends TeaModel {
    @NameInMap("Code")
    public String code;

    @NameInMap("Data")
    public GetAdbLinkResponseBodyData data;

    @NameInMap("HttpStatusCode")
    public Integer httpStatusCode;

    @NameInMap("Message")
    public String message;

    @NameInMap("RequestId")
    public String requestId;

    @NameInMap("Success")
    public Boolean success;

    public static GetAdbLinkResponseBody build(java.util.Map<String, ?> map) throws Exception {
        GetAdbLinkResponseBody self = new GetAdbLinkResponseBody();
        return TeaModel.build(map, self);
    }

    public GetAdbLinkResponseBody setCode(String code) {
        this.code = code;
        return this;
    }
    public String getCode() {
        return this.code;
    }

    public GetAdbLinkResponseBody setData(GetAdbLinkResponseBodyData data) {
        this.data = data;
        return this;
    }
    public GetAdbLinkResponseBodyData getData() {
        return this.data;
    }

    public GetAdbLinkResponseBody setHttpStatusCode(Integer httpStatusCode) {
        this.httpStatusCode = httpStatusCode;
        return this;
    }
    public Integer getHttpStatusCode() {
        return this.httpStatusCode;
    }

    public GetAdbLinkResponseBody setMessage(String message) {
        this.message = message;
        return this;
    }
    public String getMessage() {
        return this.message;
    }

    public GetAdbLinkResponseBody setRequestId(String requestId) {
        this.requestId = requestId;
        return this;
    }
    public String getRequestId() {
        return this.requestId;
    }

    public GetAdbLinkResponseBody setSuccess(Boolean success) {
        this.success = success;
        return this;
    }
    public Boolean getSuccess() {
        return this.success;
    }

    public static class GetAdbLinkResponseBodyData extends TeaModel {
        @NameInMap("Url")
        public String url;

        public static GetAdbLinkResponseBodyData build(java.util.Map<String, ?> map) throws Exception {
            GetAdbLinkResponseBodyData self = new GetAdbLinkResponseBodyData();
            return TeaModel.build(map, self);
        }

        public GetAdbLinkResponseBodyData setUrl(String url) {
            this.url = url;
            return this;
        }
        public String getUrl() {
            return this.url;
        }

    }

}
