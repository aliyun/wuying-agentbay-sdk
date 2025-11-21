package com.aliyun.agentbay.examples;

import com.aliyun.agentbay.AgentBay;
import com.aliyun.agentbay.exception.AgentBayException;
import com.aliyun.agentbay.filesystem.FileSystem;
import com.aliyun.agentbay.model.*;
import com.aliyun.agentbay.session.CreateSessionParams;
import com.aliyun.agentbay.session.Session;
import com.aliyun.agentbay.context.ContextSync;
import com.aliyun.agentbay.context.SyncPolicy;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;

public class FileTransferExample {

    private static String createTestFile(String content, String suffix) throws IOException {
        File tempFile = File.createTempFile("agentbay_test_", suffix);
        try (FileWriter writer = new FileWriter(tempFile)) {
            writer.write(content);
        }
        return tempFile.getAbsolutePath();
    }

    public static boolean fileTransferExample() {
        String apiKey = System.getenv("AGENTBAY_API_KEY");
        if (apiKey == null || apiKey.trim().isEmpty()) {
            System.err.println("❌ Please set the AGENTBAY_API_KEY environment variable");
            return false;
        }

        System.out.println("🚀 File Transfer Example");
        System.out.println("==================================================");

        AgentBay agentBay = null;
        Session session = null;
        String localFilePath = null;
        String downloadFilePath = null;
        com.aliyun.agentbay.context.Context context = null;

        try {
            agentBay = new AgentBay(apiKey);
            System.out.println("✅ AgentBay client initialized");

            String contextName = "file-transfer-example-" + System.currentTimeMillis();
            com.aliyun.agentbay.context.ContextResult contextResult = agentBay.getContextService().get(contextName, true);
            if (!contextResult.isSuccess() || contextResult.getContext() == null) {
                System.err.println("❌ Failed to create context: " + contextResult.getErrorMessage());
                return false;
            }

            context = contextResult.getContext();
            System.out.println("✅ Context created: " + context.getContextId());

            CreateSessionParams sessionParams = new CreateSessionParams();
            sessionParams.setImageId("linux_latest");

            ContextSync contextSync = ContextSync.create(
                context.getContextId(),
                "/tmp",
                SyncPolicy.defaultPolicy()
            );
            sessionParams.setContextSyncs(java.util.Arrays.asList(contextSync));

            SessionResult sessionResult = agentBay.create(sessionParams);
            session = sessionResult.getSession();

            session.setFileTransferContextId(context.getContextId());
            System.out.println("✅ Session created: " + session.getSessionId());

            StringBuilder testContentBuilder = new StringBuilder();
            for (int i = 0; i < 10; i++) {
                testContentBuilder.append("Hello, AgentBay! This is a test file for file transfer operations.\n");
            }
            String testContent = testContentBuilder.toString();
            localFilePath = createTestFile(testContent, ".txt");
            System.out.println("✅ Created test file: " + localFilePath);

            FileSystem fs = session.getFileSystem();

            // ===== TEST 1: Upload local file and verify with readFile =====
            System.out.println("\n===== TEST 1: Upload File =====");

            System.out.println("Creating test directory...");
            BoolResult createDirResult = fs.createDirectory("/tmp/file_transfer_test/");
            if (!createDirResult.isSuccess()) {
                System.err.println("❌ Failed to create directory: " + createDirResult.getErrorMessage());
                return false;
            }
            System.out.println("✅ Test directory created");

            String uploadRemotePath = "/tmp/file_transfer_test/upload_test.txt";
            System.out.println("\n📤 Uploading local file to " + uploadRemotePath + "...");

            UploadResult uploadResult = fs.uploadFile(localFilePath, uploadRemotePath);

            if (uploadResult.isSuccess()) {
                System.out.println("✅ Upload successful!");
                System.out.println("   - Bytes sent: " + uploadResult.getBytesSent());
                System.out.println("   - HTTP status: " + uploadResult.getHttpStatus());
                System.out.println("   - Request ID: " + uploadResult.getRequestIdUploadUrl());
            } else {
                System.err.println("❌ Upload failed: " + uploadResult.getErrorMessage());
                return false;
            }

            // Verify uploaded file with readFile
            System.out.println("\nVerifying uploaded file with readFile...");
            FileContentResult readResult = fs.readFile(uploadRemotePath);
            if (readResult.isSuccess()) {
                String remoteContent = readResult.getContent();
                if (remoteContent.equals(testContent)) {
                    System.out.println("✅ Upload verification successful! Content matches.");
                    System.out.println("   - Remote file size: " + remoteContent.length() + " bytes");
                } else {
                    System.err.println("❌ Upload verification failed! Content mismatch.");
                    System.err.println("   - Expected size: " + testContent.length());
                    System.err.println("   - Actual size: " + remoteContent.length());
                    return false;
                }
            } else {
                System.err.println("❌ Failed to read uploaded file: " + readResult.getErrorMessage());
                return false;
            }

            // ===== TEST 2: Write remote file and download to verify =====
            System.out.println("\n===== TEST 2: Download File =====");

            String downloadTestContent = "This is a test file created remotely for download verification.\n" +
                                        "It contains multiple lines of text.\n" +
                                        "Line 3\n" +
                                        "Line 4\n" +
                                        "End of file.\n";

            String downloadRemotePath = "/tmp/file_transfer_test/download_test.txt";
            System.out.println("\n📝 Creating remote file with writeFile: " + downloadRemotePath);

            BoolResult writeResult = fs.writeFile(downloadRemotePath, downloadTestContent);
            if (!writeResult.isSuccess()) {
                System.err.println("❌ Failed to write remote file: " + writeResult.getErrorMessage());
                return false;
            }
            System.out.println("✅ Remote file created successfully");
            System.out.println("   - File size: " + downloadTestContent.length() + " bytes");

            downloadFilePath = localFilePath + ".downloaded";
            System.out.println("\n📥 Downloading remote file to " + downloadFilePath + "...");

            DownloadResult downloadResult = fs.downloadFile(downloadRemotePath, downloadFilePath);

            if (downloadResult.isSuccess()) {
                System.out.println("✅ Download successful!");
                System.out.println("   - Bytes received: " + downloadResult.getBytesReceived());
                System.out.println("   - HTTP status: " + downloadResult.getHttpStatus());
                System.out.println("   - Saved to: " + downloadResult.getLocalPath());

                // Verify downloaded content
                String downloadedContent = new String(Files.readAllBytes(Paths.get(downloadFilePath)));

                if (downloadedContent.equals(downloadTestContent)) {
                    System.out.println("✅ Download verification successful! Content matches.");
                } else {
                    System.err.println("❌ Download verification failed! Content mismatch.");
                    System.err.println("   - Expected size: " + downloadTestContent.length());
                    System.err.println("   - Actual size: " + downloadedContent.length());
                    return false;
                }
            } else {
                System.err.println("❌ Download failed: " + downloadResult.getErrorMessage());
                return false;
            }

            System.out.println("\n🎉 File transfer example completed successfully!");
            return true;

        } catch (Exception e) {
            System.err.println("❌ Error during file transfer example: " + e.getMessage());
            e.printStackTrace();
            return false;
        } finally {
            if (localFilePath != null) {
                File localFile = new File(localFilePath);
                if (localFile.exists()) {
                    localFile.delete();
                    System.out.println("🧹 Cleaned up local file: " + localFilePath);
                }
            }

            if (downloadFilePath != null) {
                File downloadFile = new File(downloadFilePath);
                if (downloadFile.exists()) {
                    downloadFile.delete();
                    System.out.println("🧹 Cleaned up local file: " + downloadFilePath);
                }
            }

            System.out.println("\n🧹 Cleaning up...");
            if (session != null && agentBay != null) {
                try {
                    DeleteResult deleteResult = session.delete();
                    if (deleteResult.isSuccess()) {
                        System.out.println("✅ Session cleaned up successfully");
                    } else {
                        System.out.println("⚠️  Session cleanup warning: " + deleteResult.getErrorMessage());
                    }
                } catch (Exception e) {
                    System.out.println("⚠️  Error deleting session: " + e.getMessage());
                }
            }

            if (context != null && agentBay != null) {
                try {
                    com.aliyun.agentbay.model.OperationResult deleteContextResult =
                        agentBay.getContextService().delete(context);
                    if (deleteContextResult.isSuccess()) {
                        System.out.println("✅ Context deleted");
                    } else {
                        System.out.println("⚠️  Context deletion warning: " + deleteContextResult.getErrorMessage());
                    }
                } catch (Exception e) {
                    System.out.println("⚠️  Error deleting context: " + e.getMessage());
                }
            }
        }
    }

    public static void main(String[] args) {
        System.out.println("AgentBay File Transfer Examples");
        System.out.println("==================================================");

        if (System.getenv("AGENTBAY_API_KEY") == null || System.getenv("AGENTBAY_API_KEY").trim().isEmpty()) {
            System.err.println("❌ Please set AGENTBAY_API_KEY environment variable");
            return;
        }

        boolean success = fileTransferExample();

        System.out.println("\n==================================================");
        if (success) {
            System.out.println("🎉 All examples completed successfully!");
        } else {
            System.out.println("⚠️  Some examples encountered issues");
        }
    }
}
