// This file is auto-generated, don't edit it. Thanks.
package com.aliyun.wuyingai20250506.models;

import com.aliyun.tea.*;

public class GetContextFileDownloadUrlRequest extends TeaModel {
    @NameInMap("Authorization")
    public String authorization;

    @NameInMap("ContextId")
    public String contextId;

    @NameInMap("FilePath")
    public String filePath;

    public static GetContextFileDownloadUrlRequest build(java.util.Map<String, ?> map) throws Exception {
        GetContextFileDownloadUrlRequest self = new GetContextFileDownloadUrlRequest();
        return TeaModel.build(map, self);
    }

    public GetContextFileDownloadUrlRequest setAuthorization(String authorization) {
        this.authorization = authorization;
        return this;
    }
    public String getAuthorization() {
        return this.authorization;
    }

    public GetContextFileDownloadUrlRequest setContextId(String contextId) {
        this.contextId = contextId;
        return this;
    }
    public String getContextId() {
        return this.contextId;
    }

    public GetContextFileDownloadUrlRequest setFilePath(String filePath) {
        this.filePath = filePath;
        return this;
    }
    public String getFilePath() {
        return this.filePath;
    }

}
