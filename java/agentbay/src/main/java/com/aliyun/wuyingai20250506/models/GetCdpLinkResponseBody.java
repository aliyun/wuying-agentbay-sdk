// This file is auto-generated, don't edit it. Thanks.
package com.aliyun.wuyingai20250506.models;

import com.aliyun.tea.*;

public class GetCdpLinkResponseBody extends TeaModel {
    @NameInMap("Code")
    public String code;

    @NameInMap("Data")
    public GetCdpLinkResponseBodyData data;

    @NameInMap("HttpStatusCode")
    public Integer httpStatusCode;

    @NameInMap("Message")
    public String message;

    @NameInMap("RequestId")
    public String requestId;

    @NameInMap("Success")
    public Boolean success;

    public static GetCdpLinkResponseBody build(java.util.Map<String, ?> map) throws Exception {
        GetCdpLinkResponseBody self = new GetCdpLinkResponseBody();
        return TeaModel.build(map, self);
    }

    public GetCdpLinkResponseBody setCode(String code) {
        this.code = code;
        return this;
    }
    public String getCode() {
        return this.code;
    }

    public GetCdpLinkResponseBody setData(GetCdpLinkResponseBodyData data) {
        this.data = data;
        return this;
    }
    public GetCdpLinkResponseBodyData getData() {
        return this.data;
    }

    public GetCdpLinkResponseBody setHttpStatusCode(Integer httpStatusCode) {
        this.httpStatusCode = httpStatusCode;
        return this;
    }
    public Integer getHttpStatusCode() {
        return this.httpStatusCode;
    }

    public GetCdpLinkResponseBody setMessage(String message) {
        this.message = message;
        return this;
    }
    public String getMessage() {
        return this.message;
    }

    public GetCdpLinkResponseBody setRequestId(String requestId) {
        this.requestId = requestId;
        return this;
    }
    public String getRequestId() {
        return this.requestId;
    }

    public GetCdpLinkResponseBody setSuccess(Boolean success) {
        this.success = success;
        return this;
    }
    public Boolean getSuccess() {
        return this.success;
    }

    public static class GetCdpLinkResponseBodyData extends TeaModel {
        @NameInMap("Url")
        public String url;

        public static GetCdpLinkResponseBodyData build(java.util.Map<String, ?> map) throws Exception {
            GetCdpLinkResponseBodyData self = new GetCdpLinkResponseBodyData();
            return TeaModel.build(map, self);
        }

        public GetCdpLinkResponseBodyData setUrl(String url) {
            this.url = url;
            return this;
        }
        public String getUrl() {
            return this.url;
        }

    }

}
