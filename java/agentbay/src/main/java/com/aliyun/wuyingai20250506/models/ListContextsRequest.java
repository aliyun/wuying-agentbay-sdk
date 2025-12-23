// This file is auto-generated, don't edit it. Thanks.
package com.aliyun.wuyingai20250506.models;

import com.aliyun.tea.*;

public class ListContextsRequest extends TeaModel {
    @NameInMap("Authorization")
    public String authorization;

    @NameInMap("ContextType")
    public String contextType;

    @NameInMap("MaxResults")
    public Integer maxResults;

    @NameInMap("NextToken")
    public String nextToken;

    @NameInMap("SessionId")
    public String sessionId;

    public static ListContextsRequest build(java.util.Map<String, ?> map) throws Exception {
        ListContextsRequest self = new ListContextsRequest();
        return TeaModel.build(map, self);
    }

    public ListContextsRequest setAuthorization(String authorization) {
        this.authorization = authorization;
        return this;
    }
    public String getAuthorization() {
        return this.authorization;
    }

    public ListContextsRequest setContextType(String contextType) {
        this.contextType = contextType;
        return this;
    }
    public String getContextType() {
        return this.contextType;
    }

    public ListContextsRequest setMaxResults(Integer maxResults) {
        this.maxResults = maxResults;
        return this;
    }
    public Integer getMaxResults() {
        return this.maxResults;
    }

    public ListContextsRequest setNextToken(String nextToken) {
        this.nextToken = nextToken;
        return this;
    }
    public String getNextToken() {
        return this.nextToken;
    }

    public ListContextsRequest setSessionId(String sessionId) {
        this.sessionId = sessionId;
        return this;
    }
    public String getSessionId() {
        return this.sessionId;
    }

}
