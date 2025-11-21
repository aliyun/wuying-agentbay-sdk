// This file is auto-generated, don't edit it. Thanks.
package com.aliyun.wuyingai20250506.models;

import com.aliyun.tea.*;

public class DescribeNetworkResponseBody extends TeaModel {
    @NameInMap("Code")
    public String code;

    @NameInMap("Data")
    public DescribeNetworkResponseBodyData data;

    @NameInMap("HttpStatusCode")
    public Integer httpStatusCode;

    @NameInMap("Message")
    public String message;

    @NameInMap("RequestId")
    public String requestId;

    @NameInMap("Success")
    public Boolean success;

    public static DescribeNetworkResponseBody build(java.util.Map<String, ?> map) throws Exception {
        DescribeNetworkResponseBody self = new DescribeNetworkResponseBody();
        return TeaModel.build(map, self);
    }

    public DescribeNetworkResponseBody setCode(String code) {
        this.code = code;
        return this;
    }
    public String getCode() {
        return this.code;
    }

    public DescribeNetworkResponseBody setData(DescribeNetworkResponseBodyData data) {
        this.data = data;
        return this;
    }
    public DescribeNetworkResponseBodyData getData() {
        return this.data;
    }

    public DescribeNetworkResponseBody setHttpStatusCode(Integer httpStatusCode) {
        this.httpStatusCode = httpStatusCode;
        return this;
    }
    public Integer getHttpStatusCode() {
        return this.httpStatusCode;
    }

    public DescribeNetworkResponseBody setMessage(String message) {
        this.message = message;
        return this;
    }
    public String getMessage() {
        return this.message;
    }

    public DescribeNetworkResponseBody setRequestId(String requestId) {
        this.requestId = requestId;
        return this;
    }
    public String getRequestId() {
        return this.requestId;
    }

    public DescribeNetworkResponseBody setSuccess(Boolean success) {
        this.success = success;
        return this;
    }
    public Boolean getSuccess() {
        return this.success;
    }

    public static class DescribeNetworkResponseBodyData extends TeaModel {
        @NameInMap("Online")
        public Boolean online;

        public static DescribeNetworkResponseBodyData build(java.util.Map<String, ?> map) throws Exception {
            DescribeNetworkResponseBodyData self = new DescribeNetworkResponseBodyData();
            return TeaModel.build(map, self);
        }

        public DescribeNetworkResponseBodyData setOnline(Boolean online) {
            this.online = online;
            return this;
        }
        public Boolean getOnline() {
            return this.online;
        }

    }

}
