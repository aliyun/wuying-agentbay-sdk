// This file is auto-generated, don't edit it. Thanks.
package com.aliyun.wuyingai20250506.models;

import com.aliyun.tea.*;

public class GetContextFileDownloadUrlResponseBody extends TeaModel {
    @NameInMap("Code")
    public String code;

    @NameInMap("Data")
    public GetContextFileDownloadUrlResponseBodyData data;

    @NameInMap("HttpStatusCode")
    public Integer httpStatusCode;

    @NameInMap("Message")
    public String message;

    @NameInMap("RequestId")
    public String requestId;

    @NameInMap("Success")
    public Boolean success;

    public static GetContextFileDownloadUrlResponseBody build(java.util.Map<String, ?> map) throws Exception {
        GetContextFileDownloadUrlResponseBody self = new GetContextFileDownloadUrlResponseBody();
        return TeaModel.build(map, self);
    }

    public GetContextFileDownloadUrlResponseBody setCode(String code) {
        this.code = code;
        return this;
    }
    public String getCode() {
        return this.code;
    }

    public GetContextFileDownloadUrlResponseBody setData(GetContextFileDownloadUrlResponseBodyData data) {
        this.data = data;
        return this;
    }
    public GetContextFileDownloadUrlResponseBodyData getData() {
        return this.data;
    }

    public GetContextFileDownloadUrlResponseBody setHttpStatusCode(Integer httpStatusCode) {
        this.httpStatusCode = httpStatusCode;
        return this;
    }
    public Integer getHttpStatusCode() {
        return this.httpStatusCode;
    }

    public GetContextFileDownloadUrlResponseBody setMessage(String message) {
        this.message = message;
        return this;
    }
    public String getMessage() {
        return this.message;
    }

    public GetContextFileDownloadUrlResponseBody setRequestId(String requestId) {
        this.requestId = requestId;
        return this;
    }
    public String getRequestId() {
        return this.requestId;
    }

    public GetContextFileDownloadUrlResponseBody setSuccess(Boolean success) {
        this.success = success;
        return this;
    }
    public Boolean getSuccess() {
        return this.success;
    }

    public static class GetContextFileDownloadUrlResponseBodyData extends TeaModel {
        @NameInMap("ExpireTime")
        public Long expireTime;

        @NameInMap("Url")
        public String url;

        public static GetContextFileDownloadUrlResponseBodyData build(java.util.Map<String, ?> map) throws Exception {
            GetContextFileDownloadUrlResponseBodyData self = new GetContextFileDownloadUrlResponseBodyData();
            return TeaModel.build(map, self);
        }

        public GetContextFileDownloadUrlResponseBodyData setExpireTime(Long expireTime) {
            this.expireTime = expireTime;
            return this;
        }
        public Long getExpireTime() {
            return this.expireTime;
        }

        public GetContextFileDownloadUrlResponseBodyData setUrl(String url) {
            this.url = url;
            return this;
        }
        public String getUrl() {
            return this.url;
        }

    }

}
