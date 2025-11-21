// This file is auto-generated, don't edit it. Thanks.
package com.aliyun.wuyingai20250506.models;

import com.aliyun.tea.*;

public class CreateNetworkResponseBody extends TeaModel {
    @NameInMap("Code")
    public String code;

    @NameInMap("Data")
    public CreateNetworkResponseBodyData data;

    @NameInMap("HttpStatusCode")
    public Integer httpStatusCode;

    @NameInMap("Message")
    public String message;

    @NameInMap("RequestId")
    public String requestId;

    @NameInMap("Success")
    public Boolean success;

    public static CreateNetworkResponseBody build(java.util.Map<String, ?> map) throws Exception {
        CreateNetworkResponseBody self = new CreateNetworkResponseBody();
        return TeaModel.build(map, self);
    }

    public CreateNetworkResponseBody setCode(String code) {
        this.code = code;
        return this;
    }
    public String getCode() {
        return this.code;
    }

    public CreateNetworkResponseBody setData(CreateNetworkResponseBodyData data) {
        this.data = data;
        return this;
    }
    public CreateNetworkResponseBodyData getData() {
        return this.data;
    }

    public CreateNetworkResponseBody setHttpStatusCode(Integer httpStatusCode) {
        this.httpStatusCode = httpStatusCode;
        return this;
    }
    public Integer getHttpStatusCode() {
        return this.httpStatusCode;
    }

    public CreateNetworkResponseBody setMessage(String message) {
        this.message = message;
        return this;
    }
    public String getMessage() {
        return this.message;
    }

    public CreateNetworkResponseBody setRequestId(String requestId) {
        this.requestId = requestId;
        return this;
    }
    public String getRequestId() {
        return this.requestId;
    }

    public CreateNetworkResponseBody setSuccess(Boolean success) {
        this.success = success;
        return this;
    }
    public Boolean getSuccess() {
        return this.success;
    }

    public static class CreateNetworkResponseBodyData extends TeaModel {
        @NameInMap("NetworkId")
        public String networkId;

        @NameInMap("NetworkToken")
        public String networkToken;

        public static CreateNetworkResponseBodyData build(java.util.Map<String, ?> map) throws Exception {
            CreateNetworkResponseBodyData self = new CreateNetworkResponseBodyData();
            return TeaModel.build(map, self);
        }

        public CreateNetworkResponseBodyData setNetworkId(String networkId) {
            this.networkId = networkId;
            return this;
        }
        public String getNetworkId() {
            return this.networkId;
        }

        public CreateNetworkResponseBodyData setNetworkToken(String networkToken) {
            this.networkToken = networkToken;
            return this;
        }
        public String getNetworkToken() {
            return this.networkToken;
        }

    }

}
