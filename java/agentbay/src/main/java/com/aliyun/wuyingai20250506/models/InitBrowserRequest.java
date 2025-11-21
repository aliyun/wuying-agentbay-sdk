// This file is auto-generated, don't edit it. Thanks.
package com.aliyun.wuyingai20250506.models;

import com.aliyun.tea.*;

public class InitBrowserRequest extends TeaModel {
    @NameInMap("Authorization")
    public String authorization;

    @NameInMap("BrowserOption")
    public String browserOption;

    @NameInMap("PersistentPath")
    public String persistentPath;

    @NameInMap("SessionId")
    public String sessionId;

    public static InitBrowserRequest build(java.util.Map<String, ?> map) throws Exception {
        InitBrowserRequest self = new InitBrowserRequest();
        return TeaModel.build(map, self);
    }

    public InitBrowserRequest setAuthorization(String authorization) {
        this.authorization = authorization;
        return this;
    }
    public String getAuthorization() {
        return this.authorization;
    }

    public InitBrowserRequest setBrowserOption(String browserOption) {
        this.browserOption = browserOption;
        return this;
    }
    public String getBrowserOption() {
        return this.browserOption;
    }

    public InitBrowserRequest setPersistentPath(String persistentPath) {
        this.persistentPath = persistentPath;
        return this;
    }
    public String getPersistentPath() {
        return this.persistentPath;
    }

    public InitBrowserRequest setSessionId(String sessionId) {
        this.sessionId = sessionId;
        return this;
    }
    public String getSessionId() {
        return this.sessionId;
    }

}
