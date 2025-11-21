// This file is auto-generated, don't edit it. Thanks.
package com.aliyun.wuyingai20250506.models;

import com.aliyun.tea.*;

public class GetContextFileUploadUrlResponseBody extends TeaModel {
    @NameInMap("Code")
    public String code;

    @NameInMap("Data")
    public GetContextFileUploadUrlResponseBodyData data;

    @NameInMap("HttpStatusCode")
    public Integer httpStatusCode;

    @NameInMap("Message")
    public String message;

    @NameInMap("RequestId")
    public String requestId;

    @NameInMap("Success")
    public Boolean success;

    public static GetContextFileUploadUrlResponseBody build(java.util.Map<String, ?> map) throws Exception {
        GetContextFileUploadUrlResponseBody self = new GetContextFileUploadUrlResponseBody();
        return TeaModel.build(map, self);
    }

    public GetContextFileUploadUrlResponseBody setCode(String code) {
        this.code = code;
        return this;
    }
    public String getCode() {
        return this.code;
    }

    public GetContextFileUploadUrlResponseBody setData(GetContextFileUploadUrlResponseBodyData data) {
        this.data = data;
        return this;
    }
    public GetContextFileUploadUrlResponseBodyData getData() {
        return this.data;
    }

    public GetContextFileUploadUrlResponseBody setHttpStatusCode(Integer httpStatusCode) {
        this.httpStatusCode = httpStatusCode;
        return this;
    }
    public Integer getHttpStatusCode() {
        return this.httpStatusCode;
    }

    public GetContextFileUploadUrlResponseBody setMessage(String message) {
        this.message = message;
        return this;
    }
    public String getMessage() {
        return this.message;
    }

    public GetContextFileUploadUrlResponseBody setRequestId(String requestId) {
        this.requestId = requestId;
        return this;
    }
    public String getRequestId() {
        return this.requestId;
    }

    public GetContextFileUploadUrlResponseBody setSuccess(Boolean success) {
        this.success = success;
        return this;
    }
    public Boolean getSuccess() {
        return this.success;
    }

    public static class GetContextFileUploadUrlResponseBodyData extends TeaModel {
        @NameInMap("ExpireTime")
        public Long expireTime;

        @NameInMap("Url")
        public String url;

        public static GetContextFileUploadUrlResponseBodyData build(java.util.Map<String, ?> map) throws Exception {
            GetContextFileUploadUrlResponseBodyData self = new GetContextFileUploadUrlResponseBodyData();
            return TeaModel.build(map, self);
        }

        public GetContextFileUploadUrlResponseBodyData setExpireTime(Long expireTime) {
            this.expireTime = expireTime;
            return this;
        }
        public Long getExpireTime() {
            return this.expireTime;
        }

        public GetContextFileUploadUrlResponseBodyData setUrl(String url) {
            this.url = url;
            return this;
        }
        public String getUrl() {
            return this.url;
        }

    }

}
