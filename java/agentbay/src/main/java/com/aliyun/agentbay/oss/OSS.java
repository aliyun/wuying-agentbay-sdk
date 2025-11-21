package com.aliyun.agentbay.oss;

import com.aliyun.agentbay.exception.OSSException;
import com.aliyun.agentbay.model.DeleteResult;
import com.aliyun.agentbay.model.OperationResult;
import com.aliyun.agentbay.service.BaseService;
import com.aliyun.agentbay.session.Session;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.HashMap;
import java.util.Map;

/**
 * Handles Object Storage Service operations in the AgentBay cloud environment.
 * Similar to Python's Oss class.
 */
public class OSS extends BaseService {
    private static final Logger logger = LoggerFactory.getLogger(OSS.class);

    public OSS(Session session) {
        super(session);
    }

    /**
     * Create an OSS client with the provided credentials.
     * Similar to Python's env_init method.
     *
     * @param accessKeyId The Access Key ID for OSS authentication
     * @param accessKeySecret The Access Key Secret for OSS authentication
     * @param securityToken Optional security token for temporary credentials
     * @param endpoint The OSS service endpoint
     * @param region The OSS region
     * @return OSSClientResult containing client configuration and error message if any
     */
    public OSSClientResult envInit(String accessKeyId, String accessKeySecret, String securityToken, String endpoint, String region) {
        try {
            Map<String, Object> args = new HashMap<>();
            args.put("access_key_id", accessKeyId);
            args.put("access_key_secret", accessKeySecret);
            args.put("security_token", securityToken);

            if (endpoint != null) {
                args.put("endpoint", endpoint);
            }
            if (region != null) {
                args.put("region", region);
            }

            OperationResult result = callMcpTool("oss_env_init", args);
            logger.debug("oss_env_init response: {}", result);

            if (result.isSuccess()) {
                return new OSSClientResult(result.getRequestId(), true, result.getData(), "");
            } else {
                return new OSSClientResult(result.getRequestId(), false, null,
                    result.getErrorMessage() != null ? result.getErrorMessage() : "Failed to initialize OSS environment");
            }

        } catch (Exception e) {
            logger.error("Failed to initialize OSS environment", e);
            return new OSSClientResult("", false, null, "Failed to initialize OSS environment: " + e.getMessage());
        }
    }

    /**
     * Upload a local file or directory to OSS.
     * Similar to Python's upload method.
     *
     * @param bucket OSS bucket name
     * @param object Object key in OSS
     * @param path Local file or directory path to upload
     * @return OSSUploadResult containing upload result and error message if any
     */
    public OSSUploadResult upload(String bucket, String object, String path) {
        try {
            // Validate required parameters
            if (bucket == null || bucket.trim().isEmpty()) {
                return new OSSUploadResult("", false, "", "Bucket name is required");
            }
            if (object == null || object.trim().isEmpty()) {
                return new OSSUploadResult("", false, "", "Object key is required");
            }
            if (path == null || path.trim().isEmpty()) {
                return new OSSUploadResult("", false, "", "File path is required");
            }

            Map<String, Object> args = new HashMap<>();
            args.put("bucket", bucket);
            args.put("object", object);
            args.put("path", path);

            OperationResult result = callMcpTool("oss_upload", args);
            logger.debug("oss_upload response: {}", result);

            if (result.isSuccess()) {
                return new OSSUploadResult(result.getRequestId(), true, result.getData(), "");
            } else {
                return new OSSUploadResult(result.getRequestId(), false, "",
                    result.getErrorMessage() != null ? result.getErrorMessage() : "Failed to upload to OSS");
            }

        } catch (Exception e) {
            logger.error("Failed to upload to OSS", e);
            return new OSSUploadResult("", false, "", "Failed to upload to OSS: " + e.getMessage());
        }
    }

    /**
     * Upload a local file or directory to a URL anonymously.
     * Similar to Python's upload_anonymous method.
     *
     * @param url The HTTP/HTTPS URL to upload the file to
     * @param path Local file or directory path to upload
     * @return OSSUploadResult containing upload result and error message if any
     */
    public OSSUploadResult uploadAnonymous(String url, String path) {
        try {
            // Validate required parameters
            if (url == null || url.trim().isEmpty()) {
                return new OSSUploadResult("", false, "", "Upload URL is required");
            }
            if (path == null || path.trim().isEmpty()) {
                return new OSSUploadResult("", false, "", "File path is required");
            }

            Map<String, Object> args = new HashMap<>();
            args.put("url", url);
            args.put("path", path);

            OperationResult result = callMcpTool("oss_upload_annon", args);
            logger.debug("oss_upload_annon response: {}", result);

            if (result.isSuccess()) {
                return new OSSUploadResult(result.getRequestId(), true, result.getData(), "");
            } else {
                return new OSSUploadResult(result.getRequestId(), false, "",
                    result.getErrorMessage() != null ? result.getErrorMessage() : "Failed to upload anonymously");
            }

        } catch (Exception e) {
            logger.error("Failed to upload anonymously", e);
            return new OSSUploadResult("", false, "", "Failed to upload anonymously: " + e.getMessage());
        }
    }

    /**
     * Download an object from OSS to a local file or directory.
     * Similar to Python's download method.
     *
     * @param bucket OSS bucket name
     * @param object Object key in OSS
     * @param path Local file or directory path to download to
     * @return OSSDownloadResult containing download status and error message if any
     */
    public OSSDownloadResult download(String bucket, String object, String path) {
        try {
            // Validate required parameters
            if (bucket == null || bucket.trim().isEmpty()) {
                return new OSSDownloadResult("", false, "", "Bucket name is required");
            }
            if (object == null || object.trim().isEmpty()) {
                return new OSSDownloadResult("", false, "", "Object key is required");
            }
            if (path == null || path.trim().isEmpty()) {
                return new OSSDownloadResult("", false, "", "File path is required");
            }

            Map<String, Object> args = new HashMap<>();
            args.put("bucket", bucket);
            args.put("object", object);
            args.put("path", path);

            OperationResult result = callMcpTool("oss_download", args);
            logger.debug("oss_download response: {}", result);

            if (result.isSuccess()) {
                return new OSSDownloadResult(result.getRequestId(), true, result.getData(), "");
            } else {
                return new OSSDownloadResult(result.getRequestId(), false, "",
                    result.getErrorMessage() != null ? result.getErrorMessage() : "Failed to download from OSS");
            }

        } catch (Exception e) {
            logger.error("Failed to download from OSS", e);
            return new OSSDownloadResult("", false, "", "Failed to download from OSS: " + e.getMessage());
        }
    }

    /**
     * Download a file from a URL anonymously to a local file path.
     * Similar to Python's download_anonymous method.
     *
     * @param url The HTTP/HTTPS URL to download the file from
     * @param path Local file or directory path to download to
     * @return OSSDownloadResult containing download status and error message if any
     */
    public OSSDownloadResult downloadAnonymous(String url, String path) {
        try {
            // Validate required parameters
            if (url == null || url.trim().isEmpty()) {
                return new OSSDownloadResult("", false, "", "Download URL is required");
            }
            if (path == null || path.trim().isEmpty()) {
                return new OSSDownloadResult("", false, "", "File path is required");
            }

            Map<String, Object> args = new HashMap<>();
            args.put("url", url);
            args.put("path", path);

            OperationResult result = callMcpTool("oss_download_annon", args);
            logger.debug("oss_download_annon response: {}", result);

            if (result.isSuccess()) {
                return new OSSDownloadResult(result.getRequestId(), true, result.getData(), "");
            } else {
                return new OSSDownloadResult(result.getRequestId(), false, "",
                    result.getErrorMessage() != null ? result.getErrorMessage() : "Failed to download anonymously");
            }

        } catch (Exception e) {
            logger.error("Failed to download anonymously", e);
            return new OSSDownloadResult("", false, "", "Failed to download anonymously: " + e.getMessage());
        }
    }

    // Legacy method aliases for backwards compatibility

    /**
     * @deprecated Use {@link #upload(String, String, String)} instead
     */
    @Deprecated
    public OSSUploadResult uploadFile(String localPath, String remotePath) throws OSSException {
        OSSUploadResult result = new OSSUploadResult();
        result.setSuccess(false);
        result.setErrorMessage("Please use upload(bucket, object, path) method instead");
        return result;
    }

    /**
     * @deprecated Use {@link #download(String, String, String)} instead
     */
    @Deprecated
    public OSSDownloadResult downloadFile(String remotePath, String localPath) throws OSSException {
        OSSDownloadResult result = new OSSDownloadResult();
        result.setSuccess(false);
        result.setErrorMessage("Please use download(bucket, object, path) method instead");
        return result;
    }

    /**
     * @deprecated Use appropriate OSS delete operations through MCP tools
     */
    @Deprecated
    public DeleteResult deleteFile(String remotePath) throws OSSException {
        DeleteResult result = new DeleteResult();
        result.setSuccess(false);
        result.setErrorMessage("Delete operations not implemented");
        return result;
    }

    /**
     * @deprecated This method is not implemented
     */
    @Deprecated
    public OSSClientResult getClient() {
        OSSClientResult result = new OSSClientResult();
        result.setSuccess(false);
        result.setErrorMessage("Not implemented - use envInit instead");
        return result;
    }

    /**
     * @deprecated Use {@link #upload(String, String, String)} instead
     */
    @Deprecated
    public OSSUploadResult uploadLegacy(String localPath, String remotePath, String bucketName) throws OSSException {
        return upload(bucketName, remotePath, localPath);
    }

    /**
     * @deprecated Use {@link #uploadAnonymous(String, String)} instead
     */
    @Deprecated
    public OSSUploadResult uploadAnonymousLegacy(String localPath, String remotePath) throws OSSException {
        return uploadAnonymous(remotePath, localPath);
    }

    /**
     * @deprecated Use {@link #download(String, String, String)} instead
     */
    @Deprecated
    public OSSDownloadResult downloadLegacy(String remotePath, String localPath, String bucketName) throws OSSException {
        return download(bucketName, remotePath, localPath);
    }

    /**
     * @deprecated Delete operations not supported
     */
    @Deprecated
    public void deleteFileVoid(String remotePath) throws OSSException {
        throw new OSSException("Delete operations not supported");
    }
}
