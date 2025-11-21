package com.aliyun.agentbay.oss;

import com.aliyun.agentbay.model.DeleteResult;
import com.aliyun.agentbay.exception.OSSException;

public class OssClient {

    public void uploadFile(String localPath, String remotePath) throws OSSException {
        // TODO: Implement file upload to OSS
        throw new OSSException("Not implemented");
    }

    public void downloadFile(String remotePath, String localPath) throws OSSException {
        // TODO: Implement file download from OSS
        throw new OSSException("Not implemented");
    }

    public DeleteResult deleteFile(String remotePath) throws OSSException {
        // TODO: Implement file deletion from OSS
        DeleteResult result = new DeleteResult();
        result.setSuccess(false);
        result.setErrorMessage("Not implemented");
        return result;
    }
}