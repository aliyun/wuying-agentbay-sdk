package com.aliyun.agentbay.filesystem;

import com.aliyun.agentbay.AgentBay;
import com.aliyun.agentbay.context.ContextManager;
import com.aliyun.agentbay.context.ContextService;
import com.aliyun.agentbay.context.ContextInfoResult;
import com.aliyun.agentbay.context.ContextSyncResult;
import com.aliyun.agentbay.context.ContextStatusData;
import com.aliyun.agentbay.model.FileUrlResult;
import com.aliyun.agentbay.model.UploadResult;
import com.aliyun.agentbay.model.DownloadResult;
import com.aliyun.agentbay.session.Session;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.*;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.file.Files;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.nio.charset.StandardCharsets;

public class FileTransfer {
    private static final Logger logger = LoggerFactory.getLogger(FileTransfer.class);

    private final AgentBay agentBay;
    private final ContextService contextService;
    private final Session session;
    private final int httpTimeout;
    private final boolean followRedirects;
    private final String contextId;

    private static final Set<String> FINISHED_STATES = new HashSet<>();

    static {
        FINISHED_STATES.add("success");
        FINISHED_STATES.add("successful");
        FINISHED_STATES.add("ok");
        FINISHED_STATES.add("finished");
        FINISHED_STATES.add("done");
        FINISHED_STATES.add("completed");
        FINISHED_STATES.add("complete");
    }

    public FileTransfer(AgentBay agentBay, Session session) {
        this(agentBay, session, 60000, true);
    }

    public FileTransfer(AgentBay agentBay, Session session, int httpTimeout, boolean followRedirects) {
        this.agentBay = agentBay;
        this.contextService = agentBay.getContextService();
        this.session = session;
        this.httpTimeout = httpTimeout;
        this.followRedirects = followRedirects;
        this.contextId = session.getFileTransferContextId();
    }

    public UploadResult upload(
        String localPath,
        String remotePath,
        String contentType,
        boolean wait,
        float waitTimeout,
        float pollInterval
    ) {
        File localFile = new File(localPath);
        if (!localFile.isFile()) {
            return new UploadResult(
                "", false, null, null, null, null, 0, remotePath,
                "Local file not found: " + localPath
            );
        }

        if (contextId == null) {
            return new UploadResult(
                "", false, null, null, null, null, 0, remotePath,
                "No context ID"
            );
        }

        try {
            logger.info("Starting upload: localPath={}, remotePath={}, wait={}, waitTimeout={}",
                localPath, remotePath, wait, waitTimeout);
            logger.info("Getting file upload URL");
            FileUrlResult urlResult = contextService.getFileUploadUrl(contextId, remotePath);
            logger.info("URL result: success={}", urlResult.isSuccess());
            if (!urlResult.isSuccess() || urlResult.getUrl() == null || urlResult.getUrl().isEmpty()) {
                return new UploadResult(
                    "", false, urlResult.getRequestId(), null, null, null, 0, remotePath,
                    "get_file_upload_url failed: " + urlResult.getErrorMessage()
                );
            }

            String uploadUrl = urlResult.getUrl();
            String reqIdUpload = urlResult.getRequestId();

            logger.info("Uploading {} to {}", localPath, uploadUrl);

            PutFileResult putResult = putFileSync(uploadUrl, localPath, contentType);
            logger.info("Upload completed with HTTP {}", putResult.statusCode);

            if (putResult.statusCode < 200 || putResult.statusCode >= 300) {
                return new UploadResult(
                    "", false, reqIdUpload, null, putResult.statusCode, putResult.etag,
                    putResult.bytesSent, remotePath,
                    "Upload failed with HTTP " + putResult.statusCode
                );
            }

            logger.info("Triggering sync to cloud disk");
            String reqIdSync = awaitSync("download", remotePath, contextId);

            logger.info("Sync request ID: {}", reqIdSync);

            if (wait) {
                logger.info("Waiting for task completion: timeout={}, interval={}", waitTimeout, pollInterval);
                WaitResult waitResult = waitForTask(contextId, remotePath, "download", waitTimeout, pollInterval);
                logger.info("Wait result: success={}, error={}", waitResult.success, waitResult.error);
                if (!waitResult.success) {
                    return new UploadResult(
                        "", false, reqIdUpload, reqIdSync, putResult.statusCode, putResult.etag,
                        putResult.bytesSent, remotePath,
                        "Upload sync not finished: " + (waitResult.error != null ? waitResult.error : "timeout or unknown")
                    );
                }
            }

            logger.info("Upload completed successfully: bytesSent={}", putResult.bytesSent);

            return new UploadResult(
                "", true, reqIdUpload, reqIdSync, putResult.statusCode, putResult.etag,
                putResult.bytesSent, remotePath, null
            );

        } catch (Exception e) {
            logger.error("Upload exception", e);
            return new UploadResult(
                "", false, null, null, null, null, 0, remotePath,
                "Upload exception: " + e.getMessage()
            );
        }
    }

    public DownloadResult download(
        String remotePath,
        String localPath,
        boolean overwrite,
        boolean wait,
        float waitTimeout,
        float pollInterval
    ) {
        if (contextId == null) {
            return new DownloadResult(
                "", false, null, null, null, 0, remotePath, localPath, null,
                "No context ID"
            );
        }

        try {
            logger.info("Starting download: remotePath={}, localPath={}, wait={}, waitTimeout={}",
                remotePath, localPath, wait, waitTimeout);
            logger.info("Triggering sync from cloud disk to OSS");
            String reqIdSync = awaitSync("upload", remotePath, contextId);
            logger.info("Sync completed: reqIdSync={}", reqIdSync);

            if (wait) {
                logger.info("Waiting for task completion: timeout={}, interval={}", waitTimeout, pollInterval);
                WaitResult waitResult = waitForTask(contextId, remotePath, "upload", waitTimeout, pollInterval);
                logger.info("Wait result: success={}, error={}", waitResult.success, waitResult.error);
                if (!waitResult.success) {
                    return new DownloadResult(
                        "", false, null, reqIdSync, null, 0, remotePath, localPath, null,
                        "Download sync not finished: " + (waitResult.error != null ? waitResult.error : "timeout or unknown")
                    );
                }
            }

            logger.info("Getting file download URL");
            FileUrlResult urlResult = contextService.getFileDownloadUrl(contextId, remotePath);
            logger.info("URL result: success={}, url={}", urlResult.isSuccess(),
                urlResult.getUrl() != null ? urlResult.getUrl().substring(0, Math.min(50, urlResult.getUrl().length())) + "..." : "null");
            if (!urlResult.isSuccess() || urlResult.getUrl() == null || urlResult.getUrl().isEmpty()) {
                return new DownloadResult(
                    "", false, urlResult.getRequestId(), reqIdSync, null, 0, remotePath, localPath, null,
                    "get_file_download_url failed: " + urlResult.getErrorMessage()
                );
            }

            String downloadUrl = urlResult.getUrl();
            String reqIdDownload = urlResult.getRequestId();

            logger.info("Starting HTTP download");
            GetFileResult getResult = getFileSync(downloadUrl, localPath);
            logger.info("HTTP result: statusCode={}, bytesReceived={}", getResult.statusCode, getResult.bytesReceived);

            if (getResult.statusCode != 200) {
                return new DownloadResult(
                    "", false, reqIdDownload, reqIdSync, getResult.statusCode,
                    getResult.bytesReceived, remotePath, localPath, null,
                    "Download failed with HTTP " + getResult.statusCode
                );
            }

            long actualFileSize = getResult.bytesReceived;
            if (localPath != null && !localPath.isEmpty()) {
                File downloadedFile = new File(localPath);
                actualFileSize = downloadedFile.exists() ? downloadedFile.length() : getResult.bytesReceived;
            }
            logger.info("Download completed successfully: actualFileSize={}", actualFileSize);

            return new DownloadResult(
                "", true, reqIdDownload, reqIdSync, 200,
                actualFileSize, remotePath, localPath, getResult.content, null
            );

        } catch (Exception e) {
            logger.error("Download exception", e);
            return new DownloadResult(
                "", false, null, null, null, 0, remotePath, localPath, null,
                "Download exception: " + e.getMessage()
            );
        }
    }

    private String awaitSync(String mode, String remotePath, String contextId) {
        logger.info("session.context.sync(mode={}, path={}, context_id={})", mode, remotePath, contextId);
        ContextSyncResult result = session.getContext().sync(contextId, remotePath, mode);
        logger.info("   Result: {}", result.isSuccess());
        return result.getRequestId();
    }

    private WaitResult waitForTask(
        String contextId,
        String remotePath,
        String taskType,
        float timeout,
        float interval
    ) {
        long deadline = System.currentTimeMillis() + (long) (timeout * 1000);
        String lastErr = null;

        while (System.currentTimeMillis() < deadline) {
            try {
                ContextInfoResult res = session.getContext().info(contextId, remotePath, taskType);
                List<ContextStatusData> statusList = res.getContextStatusData();

                for (ContextStatusData item : statusList) {
                    String cid = item.getContextId();
                    String path = item.getPath();
                    String ttype = item.getTaskType();
                    String status = item.getStatus();
                    String err = item.getErrorMessage();

                    if (contextId.equals(cid) && remotePath.equals(path) &&
                        (taskType == null || taskType.equals(ttype))) {
                        if (err != null && !err.isEmpty()) {
                            return new WaitResult(false, "Task error: " + err);
                        }
                        if (status != null && FINISHED_STATES.contains(status.toLowerCase())) {
                            return new WaitResult(true, null);
                        }
                    }
                }

                lastErr = "task not finished";
            } catch (Exception e) {
                lastErr = "info error: " + e.getMessage();
            }

            try {
                Thread.sleep((long) (interval * 1000));
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                return new WaitResult(false, "Interrupted");
            }
        }

        return new WaitResult(false, lastErr != null ? lastErr : "timeout");
    }

    private PutFileResult putFileSync(String url, String filePath, String contentType) throws IOException {
        File file = new File(filePath);
        long fileSize = file.length();

        HttpURLConnection conn = (HttpURLConnection) new URL(url).openConnection();
        conn.setRequestMethod("PUT");
        conn.setDoOutput(true);
        conn.setConnectTimeout(httpTimeout);
        conn.setReadTimeout(httpTimeout);
        conn.setInstanceFollowRedirects(followRedirects);

        if (contentType != null && !contentType.isEmpty()) {
            conn.setRequestProperty("Content-Type", contentType);
        }

        try (FileInputStream fis = new FileInputStream(file);
             OutputStream os = conn.getOutputStream()) {
            byte[] buffer = new byte[8192];
            int bytesRead;
            while ((bytesRead = fis.read(buffer)) != -1) {
                os.write(buffer, 0, bytesRead);
            }
        }

        int statusCode = conn.getResponseCode();
        String etag = conn.getHeaderField("ETag");

        conn.disconnect();
        return new PutFileResult(statusCode, etag, fileSize);
    }

    private GetFileResult getFileSync(String url, String destPath) throws IOException {
        HttpURLConnection conn = (HttpURLConnection) new URL(url).openConnection();
        conn.setRequestMethod("GET");
        conn.setConnectTimeout(httpTimeout);
        conn.setReadTimeout(httpTimeout);
        conn.setInstanceFollowRedirects(followRedirects);

        int statusCode = conn.getResponseCode();
        long bytesReceived = 0;
        byte[] content = null;

        if (statusCode == 200) {
            try (InputStream is = conn.getInputStream()) {
                ByteArrayOutputStream baos = new ByteArrayOutputStream();
                byte[] buffer = new byte[8192];
                int bytesRead;
                while ((bytesRead = is.read(buffer)) != -1) {
                    baos.write(buffer, 0, bytesRead);
                    bytesReceived += bytesRead;
                }
                content = baos.toByteArray();

                if (destPath != null && !destPath.isEmpty()) {
                    File destFile = new File(destPath);
                    File parentDir = destFile.getParentFile();
                    if (parentDir != null && !parentDir.exists()) {
                        parentDir.mkdirs();
                    }
                    try (FileOutputStream fos = new FileOutputStream(destPath)) {
                        fos.write(content);
                    }
                }
            }
        }

        conn.disconnect();
        return new GetFileResult(statusCode, bytesReceived, content);
    }

    private static class PutFileResult {
        int statusCode;
        String etag;
        long bytesSent;

        PutFileResult(int statusCode, String etag, long bytesSent) {
            this.statusCode = statusCode;
            this.etag = etag;
            this.bytesSent = bytesSent;
        }
    }

    private static class GetFileResult {
        int statusCode;
        long bytesReceived;
        byte[] content;

        GetFileResult(int statusCode, long bytesReceived, byte[] content) {
            this.statusCode = statusCode;
            this.bytesReceived = bytesReceived;
            this.content = content;
        }
    }

    private static class WaitResult {
        boolean success;
        String error;

        WaitResult(boolean success, String error) {
            this.success = success;
            this.error = error;
        }
    }
}
