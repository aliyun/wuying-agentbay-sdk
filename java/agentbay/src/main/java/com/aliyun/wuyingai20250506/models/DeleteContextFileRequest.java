// This file is auto-generated, don't edit it. Thanks.
package com.aliyun.wuyingai20250506.models;

import com.aliyun.tea.*;

public class DeleteContextFileRequest extends TeaModel {
    @NameInMap("Authorization")
    public String authorization;

    @NameInMap("ContextId")
    public String contextId;

    @NameInMap("FilePath")
    public String filePath;

    public static DeleteContextFileRequest build(java.util.Map<String, ?> map) throws Exception {
        DeleteContextFileRequest self = new DeleteContextFileRequest();
        return TeaModel.build(map, self);
    }

    public DeleteContextFileRequest setAuthorization(String authorization) {
        this.authorization = authorization;
        return this;
    }
    public String getAuthorization() {
        return this.authorization;
    }

    public DeleteContextFileRequest setContextId(String contextId) {
        this.contextId = contextId;
        return this;
    }
    public String getContextId() {
        return this.contextId;
    }

    public DeleteContextFileRequest setFilePath(String filePath) {
        this.filePath = filePath;
        return this;
    }
    public String getFilePath() {
        return this.filePath;
    }

}
