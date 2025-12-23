package com.aliyun.agentbay.filesystem;

@FunctionalInterface
public interface ProgressCallback {
    void onProgress(long bytesTransferred);
}
