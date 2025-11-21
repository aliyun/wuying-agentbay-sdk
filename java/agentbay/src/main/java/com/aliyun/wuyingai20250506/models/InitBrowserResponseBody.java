// This file is auto-generated, don't edit it. Thanks.
package com.aliyun.wuyingai20250506.models;

import com.aliyun.tea.*;

public class InitBrowserResponseBody extends TeaModel {
    @NameInMap("Code")
    public String code;

    @NameInMap("Data")
    public InitBrowserResponseBodyData data;

    @NameInMap("HttpStatusCode")
    public Integer httpStatusCode;

    @NameInMap("Message")
    public String message;

    @NameInMap("RequestId")
    public String requestId;

    @NameInMap("Success")
    public Boolean success;

    public static InitBrowserResponseBody build(java.util.Map<String, ?> map) throws Exception {
        InitBrowserResponseBody self = new InitBrowserResponseBody();
        return TeaModel.build(map, self);
    }

    public InitBrowserResponseBody setCode(String code) {
        this.code = code;
        return this;
    }
    public String getCode() {
        return this.code;
    }

    public InitBrowserResponseBody setData(InitBrowserResponseBodyData data) {
        this.data = data;
        return this;
    }
    public InitBrowserResponseBodyData getData() {
        return this.data;
    }

    public InitBrowserResponseBody setHttpStatusCode(Integer httpStatusCode) {
        this.httpStatusCode = httpStatusCode;
        return this;
    }
    public Integer getHttpStatusCode() {
        return this.httpStatusCode;
    }

    public InitBrowserResponseBody setMessage(String message) {
        this.message = message;
        return this;
    }
    public String getMessage() {
        return this.message;
    }

    public InitBrowserResponseBody setRequestId(String requestId) {
        this.requestId = requestId;
        return this;
    }
    public String getRequestId() {
        return this.requestId;
    }

    public InitBrowserResponseBody setSuccess(Boolean success) {
        this.success = success;
        return this;
    }
    public Boolean getSuccess() {
        return this.success;
    }

    public static class InitBrowserResponseBodyData extends TeaModel {
        @NameInMap("Port")
        public Integer port;

        public static InitBrowserResponseBodyData build(java.util.Map<String, ?> map) throws Exception {
            InitBrowserResponseBodyData self = new InitBrowserResponseBodyData();
            return TeaModel.build(map, self);
        }

        public InitBrowserResponseBodyData setPort(Integer port) {
            this.port = port;
            return this;
        }
        public Integer getPort() {
            return this.port;
        }

    }

}
