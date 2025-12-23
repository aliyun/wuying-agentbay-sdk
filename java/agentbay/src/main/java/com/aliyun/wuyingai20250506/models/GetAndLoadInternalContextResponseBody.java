// This file is auto-generated, don't edit it. Thanks.
package com.aliyun.wuyingai20250506.models;

import com.aliyun.tea.*;

public class GetAndLoadInternalContextResponseBody extends TeaModel {
    @NameInMap("Code")
    public String code;

    @NameInMap("Data")
    public java.util.List<GetAndLoadInternalContextResponseBodyData> data;

    @NameInMap("HttpStatusCode")
    public Integer httpStatusCode;

    @NameInMap("Message")
    public String message;

    @NameInMap("RequestId")
    public String requestId;

    @NameInMap("Success")
    public Boolean success;

    public static GetAndLoadInternalContextResponseBody build(java.util.Map<String, ?> map) throws Exception {
        GetAndLoadInternalContextResponseBody self = new GetAndLoadInternalContextResponseBody();
        return TeaModel.build(map, self);
    }

    public GetAndLoadInternalContextResponseBody setCode(String code) {
        this.code = code;
        return this;
    }
    public String getCode() {
        return this.code;
    }

    public GetAndLoadInternalContextResponseBody setData(java.util.List<GetAndLoadInternalContextResponseBodyData> data) {
        this.data = data;
        return this;
    }
    public java.util.List<GetAndLoadInternalContextResponseBodyData> getData() {
        return this.data;
    }

    public GetAndLoadInternalContextResponseBody setHttpStatusCode(Integer httpStatusCode) {
        this.httpStatusCode = httpStatusCode;
        return this;
    }
    public Integer getHttpStatusCode() {
        return this.httpStatusCode;
    }

    public GetAndLoadInternalContextResponseBody setMessage(String message) {
        this.message = message;
        return this;
    }
    public String getMessage() {
        return this.message;
    }

    public GetAndLoadInternalContextResponseBody setRequestId(String requestId) {
        this.requestId = requestId;
        return this;
    }
    public String getRequestId() {
        return this.requestId;
    }

    public GetAndLoadInternalContextResponseBody setSuccess(Boolean success) {
        this.success = success;
        return this;
    }
    public Boolean getSuccess() {
        return this.success;
    }

    public static class GetAndLoadInternalContextResponseBodyData extends TeaModel {
        @NameInMap("ContextId")
        public String contextId;

        @NameInMap("ContextPath")
        public String contextPath;

        @NameInMap("ContextType")
        public String contextType;

        public static GetAndLoadInternalContextResponseBodyData build(java.util.Map<String, ?> map) throws Exception {
            GetAndLoadInternalContextResponseBodyData self = new GetAndLoadInternalContextResponseBodyData();
            return TeaModel.build(map, self);
        }

        public GetAndLoadInternalContextResponseBodyData setContextId(String contextId) {
            this.contextId = contextId;
            return this;
        }
        public String getContextId() {
            return this.contextId;
        }

        public GetAndLoadInternalContextResponseBodyData setContextPath(String contextPath) {
            this.contextPath = contextPath;
            return this;
        }
        public String getContextPath() {
            return this.contextPath;
        }

        public GetAndLoadInternalContextResponseBodyData setContextType(String contextType) {
            this.contextType = contextType;
            return this;
        }
        public String getContextType() {
            return this.contextType;
        }

    }

}
