package com.aliyun.agentbay.examples;

import com.aliyun.agentbay.AgentBay;
import com.aliyun.agentbay.context.Context;
import com.aliyun.agentbay.context.ContextResult;
import com.aliyun.agentbay.exception.AgentBayException;
import com.aliyun.agentbay.filesystem.ProgressCallback;
import com.aliyun.agentbay.model.*;
import com.aliyun.agentbay.session.CreateSessionParams;
import com.aliyun.agentbay.session.Session;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.concurrent.atomic.AtomicInteger;

public class FileTransferExample {

    private static String createTestFile(String content, String suffix) throws IOException {
        File tempFile = File.createTempFile("agentbay_test_", suffix);
        try (FileWriter writer = new FileWriter(tempFile)) {
            writer.write(content);
        }
        tempFile.deleteOnExit();
        return tempFile.getAbsolutePath();
    }

    public static boolean fileTransferExample() throws AgentBayException {
        String apiKey = System.getenv("AGENTBAY_API_KEY");
        if (apiKey == null || apiKey.trim().isEmpty()) {
            System.out.println("❌ Please set the AGENTBAY_API_KEY environment variable");
            return false;
        }

        System.out.println("🚀 File Transfer Example");
        System.out.println("==================================================");

        AgentBay agentbay = new AgentBay(apiKey);
        System.out.println("✅ AgentBay client initialized");

        CreateSessionParams sessionParams = new CreateSessionParams();
        sessionParams.setImageId("linux_latest");

        SessionResult sessionResult = agentbay.create(sessionParams);
        if (!sessionResult.isSuccess() || sessionResult.getSession() == null) {
            String errorMsg = sessionResult.getErrorMessage() != null ? sessionResult.getErrorMessage() : "Unknown error";
            System.out.println("❌ Failed to create session: " + errorMsg);
            return false;
        }

        Session session = sessionResult.getSession();
        System.out.println("✅ Session created: " + session.getSessionId());

        String localFilePath = null;
        String downloadFilePath = null;

        try {
            StringBuilder contentBuilder = new StringBuilder();
            for (int i = 0; i < 10; i++) {
                contentBuilder.append("Hello, AgentBay! This is a test file for file transfer operations.\n");
            }
            String testContent = contentBuilder.toString();
            localFilePath = createTestFile(testContent, ".txt");
            System.out.println("✅ Created test file: " + localFilePath);

            String fileTransferContextPath = "/home/wuying";
            String remotePath =  fileTransferContextPath + "/upload_test.txt";
            System.out.println("\n📤 Uploading file to " + remotePath + "...");

            UploadResult uploadResult = session.getFileSystem().uploadFile(
                localFilePath,
                remotePath,
                null,
                true,
                60.0f,
                1.5f,
                null
            );

            if (uploadResult.isSuccess()) {
                System.out.println("✅ Upload successful!");
                System.out.println("   - Bytes sent: " + uploadResult.getBytesSent());
                System.out.println("   - HTTP status: " + uploadResult.getHttpStatus());
                System.out.println("   - Request ID: " + uploadResult.getRequestIdUploadUrl());
            } else {
                String error = uploadResult.getErrorMessage() != null ? uploadResult.getErrorMessage() : "Unknown error";
                System.out.println("❌ Upload failed: " + error);
                return false;
            }

            DirectoryListResult listResult = session.getFileSystem().listDirectory(fileTransferContextPath);
            if (listResult.isSuccess()) {
                boolean fileFound = false;
                for (java.util.Map<String, Object> entry : listResult.getEntries()) {
                    if ("upload_test.txt".equals(entry.get("name"))) {
                        fileFound = true;
                        break;
                    }
                }
                if (fileFound) {
                    System.out.println("✅ File verified in remote directory");
                } else {
                    System.out.println("⚠️  File not found in remote directory");
                }
            } else {
                String errorMsg = listResult.getErrorMessage() != null ? listResult.getErrorMessage() : "Unknown error";
                System.out.println("⚠️  Could not list remote directory: " + errorMsg);
            }

            downloadFilePath = localFilePath + ".downloaded";

            System.out.println("\n📥 Downloading file from " + remotePath + "...");
            DownloadResult downloadResult = session.getFileSystem().downloadFile(
                remotePath,
                downloadFilePath,
                true,
                true,
                60.0f,
                1.5f,
                null
            );

            if (downloadResult.isSuccess()) {
                System.out.println("✅ Download successful!");
                System.out.println("   - Bytes received: " + downloadResult.getBytesReceived());
                System.out.println("   - HTTP status: " + downloadResult.getHttpStatus());
                System.out.println("   - Saved to: " + downloadResult.getLocalPath());

                String downloadedContent = new String(Files.readAllBytes(Paths.get(downloadFilePath)));

                if (downloadedContent.equals(testContent)) {
                    System.out.println("✅ Content verification successful!");
                } else {
                    System.out.println("❌ Content mismatch!");
                    return false;
                }
            } else {
                String error = downloadResult.getErrorMessage() != null ? downloadResult.getErrorMessage() : "Unknown error";
                System.out.println("❌ Download failed: " + error);
                return false;
            }

            System.out.println("\n🎉 File transfer example completed successfully!");
            return true;

        } catch (Exception e) {
            System.out.println("❌ Error during file transfer example: " + e.getMessage());
            e.printStackTrace();
            return false;
        } finally {
            if (localFilePath != null && new File(localFilePath).exists()) {
                new File(localFilePath).delete();
                System.out.println("🧹 Cleaned up local file: " + localFilePath);
            }
            if (downloadFilePath != null && new File(downloadFilePath).exists()) {
                new File(downloadFilePath).delete();
                System.out.println("🧹 Cleaned up local file: " + downloadFilePath);
            }

            System.out.println("\n🧹 Cleaning up...");
            try {
                DeleteResult deleteResult = agentbay.delete(session, false);
                if (deleteResult.isSuccess()) {
                    System.out.println("✅ Session cleaned up successfully");
                } else {
                    System.out.println("⚠️  Session cleanup warning: " + deleteResult.getErrorMessage());
                }
            } catch (Exception e) {
                System.out.println("⚠️  Error deleting session: " + e.getMessage());
            }

            try {
                System.out.println("✅ Context deleted");
            } catch (Exception e) {
                System.out.println("⚠️  Error deleting context: " + e.getMessage());
            }
        }
    }

    /**
     * Demonstrates byte array upload and download (Java SDK extension feature)
     * This feature allows working with file data in memory without writing to disk
     */
    public static boolean byteArrayTransferExample() throws AgentBayException {
        String apiKey = System.getenv("AGENTBAY_API_KEY");
        if (apiKey == null || apiKey.trim().isEmpty()) {
            System.out.println("❌ Please set the AGENTBAY_API_KEY environment variable");
            return false;
        }

        System.out.println("\n🚀 Byte Array Transfer Example (Java SDK Extension)");
        System.out.println("==================================================");

        AgentBay agentbay = new AgentBay(apiKey);
        System.out.println("✅ AgentBay client initialized");

        CreateSessionParams sessionParams = new CreateSessionParams();
        sessionParams.setImageId("linux_latest");

        SessionResult sessionResult = agentbay.create(sessionParams);
        if (!sessionResult.isSuccess() || sessionResult.getSession() == null) {
            String errorMsg = sessionResult.getErrorMessage() != null ? sessionResult.getErrorMessage() : "Unknown error";
            System.out.println("❌ Failed to create session: " + errorMsg);
            return false;
        }

        Session session = sessionResult.getSession();
        System.out.println("✅ Session created: " + session.getSessionId());

        try {
            // Example 1: Upload byte array
            System.out.println("\n📤 Example 1: Uploading byte array to remote file...");
            String testContent = "Hello from byte array! 你好世界 🌍\n" +
                    "This content is uploaded directly from memory.\n" +
                    "No local file was created for this upload.\n";
            byte[] contentBytes = testContent.getBytes("UTF-8");
            System.out.println("   Content size: " + contentBytes.length + " bytes");

            String fileTransferContextPath = "/home/wuying";
            String remotePath = fileTransferContextPath + "/byte_array_test.txt";

            UploadResult uploadResult = session.getFileSystem().uploadFileBytes(contentBytes, remotePath);

            if (uploadResult.isSuccess()) {
                System.out.println("✅ Byte array uploaded successfully!");
                System.out.println("   - Bytes sent: " + uploadResult.getBytesSent());
                System.out.println("   - HTTP status: " + uploadResult.getHttpStatus());
            } else {
                String error = uploadResult.getErrorMessage() != null ? uploadResult.getErrorMessage() : "Unknown error";
                System.out.println("❌ Upload failed: " + error);
                return false;
            }

            // Wait for sync
            Thread.sleep(2000);

            // Example 2: Download to byte array
            System.out.println("\n📥 Example 2: Downloading file to byte array...");
            DownloadResult downloadResult = session.getFileSystem().downloadFileBytes(remotePath);

            if (downloadResult.isSuccess()) {
                System.out.println("✅ File downloaded to byte array successfully!");
                System.out.println("   - Bytes received: " + downloadResult.getBytesReceived());
                System.out.println("   - Content length: " + downloadResult.getContent().length);

                // Verify content
                String downloadedContent = new String(downloadResult.getContent(), "UTF-8");
                if (downloadedContent.trim().equals(testContent.trim())) {
                    System.out.println("✅ Content verification passed!");
                } else {
                    System.out.println("⚠️  Content mismatch detected");
                }

                System.out.println("\n📄 Downloaded content preview:");
                String[] lines = downloadedContent.split("\n");
                for (int i = 0; i < Math.min(3, lines.length); i++) {
                    System.out.println("   " + lines[i]);
                }
            } else {
                String error = downloadResult.getErrorMessage() != null ? downloadResult.getErrorMessage() : "Unknown error";
                System.out.println("❌ Download failed: " + error);
                return false;
            }

            // Example 3: Round-trip with larger data
            System.out.println("\n🔄 Example 3: Round-trip test with larger data...");
            StringBuilder largeContent = new StringBuilder();
            for (int i = 0; i < 100; i++) {
                largeContent.append("Line ").append(i + 1).append(": Test data ").append(i * 123).append("\n");
            }
            byte[] largeBytes = largeContent.toString().getBytes("UTF-8");
            System.out.println("   Original size: " + largeBytes.length + " bytes");

            String largeRemotePath = fileTransferContextPath + "/large_byte_array.txt";
            UploadResult largeUpload = session.getFileSystem().uploadFileBytes(largeBytes, largeRemotePath);

            if (!largeUpload.isSuccess()) {
                System.out.println("❌ Large upload failed");
                return false;
            }
            System.out.println("✅ Large file uploaded: " + largeUpload.getBytesSent() + " bytes");

            Thread.sleep(2000);

            DownloadResult largeDownload = session.getFileSystem().downloadFileBytes(largeRemotePath);
            if (!largeDownload.isSuccess()) {
                System.out.println("❌ Large download failed");
                return false;
            }
            System.out.println("✅ Large file downloaded: " + largeDownload.getBytesReceived() + " bytes");

            // Byte-by-byte comparison
            byte[] downloadedBytes = largeDownload.getContent();
            if (largeBytes.length == downloadedBytes.length) {
                boolean match = true;
                for (int i = 0; i < largeBytes.length; i++) {
                    if (largeBytes[i] != downloadedBytes[i]) {
                        match = false;
                        break;
                    }
                }
                if (match) {
                    System.out.println("✅ Byte-by-byte verification passed!");
                } else {
                    System.out.println("⚠️  Byte content mismatch");
                }
            } else {
                System.out.println("⚠️  Size mismatch: " + largeBytes.length + " vs " + downloadedBytes.length);
            }

            return true;

        } catch (Exception e) {
            System.out.println("❌ Error: " + e.getMessage());
            e.printStackTrace();
            return false;
        } finally {
            try {
                DeleteResult deleteResult = agentbay.delete(session, false);
                if (deleteResult.isSuccess()) {
                    System.out.println("\n✅ Session deleted");
                } else {
                    System.out.println("\n⚠️  Error deleting session: " + deleteResult.getErrorMessage());
                }
            } catch (Exception e) {
                System.out.println("\n⚠️  Error deleting session: " + e.getMessage());
            }
        }
    }

    public static void main(String[] args) throws AgentBayException {
        System.out.println("AgentBay File Transfer Examples");
        System.out.println("==================================================");

        if (System.getenv("AGENTBAY_API_KEY") == null || System.getenv("AGENTBAY_API_KEY").trim().isEmpty()) {
            System.out.println("❌ Please set AGENTBAY_API_KEY environment variable");
            return;
        }

        // Run standard file transfer example
        boolean success1 = fileTransferExample();

        // Run byte array transfer example (Java SDK extension)
        boolean success2 = byteArrayTransferExample();

        System.out.println("\n==================================================");
        if (success1 && success2) {
            System.out.println("🎉 All examples completed successfully!");
        } else {
            System.out.println("⚠️  Some examples encountered issues");
        }
    }
}
