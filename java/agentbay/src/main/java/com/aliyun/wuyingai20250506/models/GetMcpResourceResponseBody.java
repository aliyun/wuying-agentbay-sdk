// This file is auto-generated, don't edit it. Thanks.
package com.aliyun.wuyingai20250506.models;

import com.aliyun.tea.*;

public class GetMcpResourceResponseBody extends TeaModel {
    @NameInMap("Code")
    public String code;

    @NameInMap("Data")
    public GetMcpResourceResponseBodyData data;

    @NameInMap("HttpStatusCode")
    public Integer httpStatusCode;

    @NameInMap("Message")
    public String message;

    @NameInMap("RequestId")
    public String requestId;

    @NameInMap("Success")
    public Boolean success;

    public static GetMcpResourceResponseBody build(java.util.Map<String, ?> map) throws Exception {
        GetMcpResourceResponseBody self = new GetMcpResourceResponseBody();
        return TeaModel.build(map, self);
    }

    public GetMcpResourceResponseBody setCode(String code) {
        this.code = code;
        return this;
    }
    public String getCode() {
        return this.code;
    }

    public GetMcpResourceResponseBody setData(GetMcpResourceResponseBodyData data) {
        this.data = data;
        return this;
    }
    public GetMcpResourceResponseBodyData getData() {
        return this.data;
    }

    public GetMcpResourceResponseBody setHttpStatusCode(Integer httpStatusCode) {
        this.httpStatusCode = httpStatusCode;
        return this;
    }
    public Integer getHttpStatusCode() {
        return this.httpStatusCode;
    }

    public GetMcpResourceResponseBody setMessage(String message) {
        this.message = message;
        return this;
    }
    public String getMessage() {
        return this.message;
    }

    public GetMcpResourceResponseBody setRequestId(String requestId) {
        this.requestId = requestId;
        return this;
    }
    public String getRequestId() {
        return this.requestId;
    }

    public GetMcpResourceResponseBody setSuccess(Boolean success) {
        this.success = success;
        return this;
    }
    public Boolean getSuccess() {
        return this.success;
    }

    public static class GetMcpResourceResponseBodyDataDesktopInfo extends TeaModel {
        @NameInMap("AppId")
        public String appId;

        @NameInMap("AuthCode")
        public String authCode;

        @NameInMap("ConnectionProperties")
        public String connectionProperties;

        @NameInMap("ResourceId")
        public String resourceId;

        @NameInMap("ResourceType")
        public String resourceType;

        @NameInMap("Ticket")
        public String ticket;

        public static GetMcpResourceResponseBodyDataDesktopInfo build(java.util.Map<String, ?> map) throws Exception {
            GetMcpResourceResponseBodyDataDesktopInfo self = new GetMcpResourceResponseBodyDataDesktopInfo();
            return TeaModel.build(map, self);
        }

        public GetMcpResourceResponseBodyDataDesktopInfo setAppId(String appId) {
            this.appId = appId;
            return this;
        }
        public String getAppId() {
            return this.appId;
        }

        public GetMcpResourceResponseBodyDataDesktopInfo setAuthCode(String authCode) {
            this.authCode = authCode;
            return this;
        }
        public String getAuthCode() {
            return this.authCode;
        }

        public GetMcpResourceResponseBodyDataDesktopInfo setConnectionProperties(String connectionProperties) {
            this.connectionProperties = connectionProperties;
            return this;
        }
        public String getConnectionProperties() {
            return this.connectionProperties;
        }

        public GetMcpResourceResponseBodyDataDesktopInfo setResourceId(String resourceId) {
            this.resourceId = resourceId;
            return this;
        }
        public String getResourceId() {
            return this.resourceId;
        }

        public GetMcpResourceResponseBodyDataDesktopInfo setResourceType(String resourceType) {
            this.resourceType = resourceType;
            return this;
        }
        public String getResourceType() {
            return this.resourceType;
        }

        public GetMcpResourceResponseBodyDataDesktopInfo setTicket(String ticket) {
            this.ticket = ticket;
            return this;
        }
        public String getTicket() {
            return this.ticket;
        }

    }

    public static class GetMcpResourceResponseBodyData extends TeaModel {
        @NameInMap("DesktopInfo")
        public GetMcpResourceResponseBodyDataDesktopInfo desktopInfo;

        @NameInMap("ResourceUrl")
        public String resourceUrl;

        @NameInMap("SessionId")
        public String sessionId;

        public static GetMcpResourceResponseBodyData build(java.util.Map<String, ?> map) throws Exception {
            GetMcpResourceResponseBodyData self = new GetMcpResourceResponseBodyData();
            return TeaModel.build(map, self);
        }

        public GetMcpResourceResponseBodyData setDesktopInfo(GetMcpResourceResponseBodyDataDesktopInfo desktopInfo) {
            this.desktopInfo = desktopInfo;
            return this;
        }
        public GetMcpResourceResponseBodyDataDesktopInfo getDesktopInfo() {
            return this.desktopInfo;
        }

        public GetMcpResourceResponseBodyData setResourceUrl(String resourceUrl) {
            this.resourceUrl = resourceUrl;
            return this;
        }
        public String getResourceUrl() {
            return this.resourceUrl;
        }

        public GetMcpResourceResponseBodyData setSessionId(String sessionId) {
            this.sessionId = sessionId;
            return this;
        }
        public String getSessionId() {
            return this.sessionId;
        }

    }

}
