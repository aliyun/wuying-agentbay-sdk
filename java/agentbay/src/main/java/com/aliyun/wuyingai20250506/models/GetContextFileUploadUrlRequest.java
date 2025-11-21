// This file is auto-generated, don't edit it. Thanks.
package com.aliyun.wuyingai20250506.models;

import com.aliyun.tea.*;

public class GetContextFileUploadUrlRequest extends TeaModel {
    @NameInMap("Authorization")
    public String authorization;

    @NameInMap("ContextId")
    public String contextId;

    @NameInMap("FilePath")
    public String filePath;

    public static GetContextFileUploadUrlRequest build(java.util.Map<String, ?> map) throws Exception {
        GetContextFileUploadUrlRequest self = new GetContextFileUploadUrlRequest();
        return TeaModel.build(map, self);
    }

    public GetContextFileUploadUrlRequest setAuthorization(String authorization) {
        this.authorization = authorization;
        return this;
    }
    public String getAuthorization() {
        return this.authorization;
    }

    public GetContextFileUploadUrlRequest setContextId(String contextId) {
        this.contextId = contextId;
        return this;
    }
    public String getContextId() {
        return this.contextId;
    }

    public GetContextFileUploadUrlRequest setFilePath(String filePath) {
        this.filePath = filePath;
        return this;
    }
    public String getFilePath() {
        return this.filePath;
    }

}
