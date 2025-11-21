// This file is auto-generated, don't edit it. Thanks.
package com.aliyun.wuyingai20250506.models;

import com.aliyun.tea.*;

public class GetContextInfoResponseBody extends TeaModel {
    @NameInMap("Code")
    public String code;

    @NameInMap("Data")
    public GetContextInfoResponseBodyData data;

    @NameInMap("HttpStatusCode")
    public Integer httpStatusCode;

    @NameInMap("Message")
    public String message;

    @NameInMap("RequestId")
    public String requestId;

    @NameInMap("Success")
    public Boolean success;

    public static GetContextInfoResponseBody build(java.util.Map<String, ?> map) throws Exception {
        GetContextInfoResponseBody self = new GetContextInfoResponseBody();
        return TeaModel.build(map, self);
    }

    public GetContextInfoResponseBody setCode(String code) {
        this.code = code;
        return this;
    }
    public String getCode() {
        return this.code;
    }

    public GetContextInfoResponseBody setData(GetContextInfoResponseBodyData data) {
        this.data = data;
        return this;
    }
    public GetContextInfoResponseBodyData getData() {
        return this.data;
    }

    public GetContextInfoResponseBody setHttpStatusCode(Integer httpStatusCode) {
        this.httpStatusCode = httpStatusCode;
        return this;
    }
    public Integer getHttpStatusCode() {
        return this.httpStatusCode;
    }

    public GetContextInfoResponseBody setMessage(String message) {
        this.message = message;
        return this;
    }
    public String getMessage() {
        return this.message;
    }

    public GetContextInfoResponseBody setRequestId(String requestId) {
        this.requestId = requestId;
        return this;
    }
    public String getRequestId() {
        return this.requestId;
    }

    public GetContextInfoResponseBody setSuccess(Boolean success) {
        this.success = success;
        return this;
    }
    public Boolean getSuccess() {
        return this.success;
    }

    public static class GetContextInfoResponseBodyData extends TeaModel {
        @NameInMap("ContextStatus")
        public String contextStatus;

        public static GetContextInfoResponseBodyData build(java.util.Map<String, ?> map) throws Exception {
            GetContextInfoResponseBodyData self = new GetContextInfoResponseBodyData();
            return TeaModel.build(map, self);
        }

        public GetContextInfoResponseBodyData setContextStatus(String contextStatus) {
            this.contextStatus = contextStatus;
            return this;
        }
        public String getContextStatus() {
            return this.contextStatus;
        }

    }

}
