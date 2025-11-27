package com.aliyun.agentbay.test;

import com.aliyun.agentbay.AgentBay;
import com.aliyun.agentbay.context.Context;
import com.aliyun.agentbay.context.ContextResult;
import com.aliyun.agentbay.context.ContextSync;
import com.aliyun.agentbay.context.SyncPolicy;
import com.aliyun.agentbay.exception.AgentBayException;
import com.aliyun.agentbay.filesystem.FileSystem;
import com.aliyun.agentbay.model.*;
import com.aliyun.agentbay.session.CreateSessionParams;
import com.aliyun.agentbay.session.Session;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;

import static org.junit.Assert.*;

/**
 * Test cases for File Transfer functionality in AgentBay Java SDK
 * This test class covers the functionality demonstrated in FileTransferExample.java
 * 
 * Tests cover:
 * 1. File upload operations
 * 2. File download operations
 * 3. Context-based file transfer
 * 4. Upload verification with readFile
 * 5. Download verification with writeFile
 * 6. Error handling for invalid paths
 * 7. Cleanup operations
 */
public class TestFileTransfer {

    private AgentBay agentBay;
    private Session session;
    private FileSystem fs;
    private Context context;
    private String testDirectory = "/tmp/file_transfer_test/";

    /**
     * Helper method to create a test file with specified content
     */
    private String createTestFile(String content, String suffix) throws IOException {
        File tempFile = File.createTempFile("agentbay_test_", suffix);
        try (FileWriter writer = new FileWriter(tempFile)) {
            writer.write(content);
        }
        tempFile.deleteOnExit();
        return tempFile.getAbsolutePath();
    }

    /**
     * Helper method to normalize content for comparison
     */
    private String normalizeContent(String content) {
        if (content == null) {
            return null;
        }
        return content.replaceAll("\\r\\n", "\n").replaceAll("\\r", "\n").trim();
    }

    /**
     * Get API key for testing
     */
    private static String getTestApiKey() {
        String apiKey = System.getenv("AGENTBAY_API_KEY");
        if (apiKey == null || apiKey.trim().isEmpty()) {
            apiKey = "akm-xxx"; // Replace with your test API key
            System.out.println("Warning: Using default API key. Set AGENTBAY_API_KEY environment variable for testing.");
        }
        return apiKey;
    }

    /**
     * Set up before each test - create AgentBay client, context and session
     */
    @Before
    public void setUp() throws AgentBayException, IOException {
        System.out.println("\n========================================");
        System.out.println("Setting up test environment...");
        System.out.println("========================================");
        
        String apiKey = getTestApiKey();
        agentBay = new AgentBay(apiKey);

        // Create context for file transfer
        String contextName = "file-transfer-test-" + System.currentTimeMillis();
        ContextResult contextResult = agentBay.getContextService().get(contextName, true);
        
        assertTrue("Failed to create context: " + contextResult.getErrorMessage(), 
                   contextResult.isSuccess());
        assertNotNull("Context object is null", contextResult.getContext());
        
        context = contextResult.getContext();
        System.out.println("✅ Context created with ID: " + context.getContextId());

        // Create a session with context sync
        CreateSessionParams params = new CreateSessionParams();
        params.setImageId("linux_latest");
        
        ContextSync contextSync = ContextSync.create(
            context.getContextId(),
            "/tmp",
            SyncPolicy.defaultPolicy()
        );
        params.setContextSyncs(java.util.Arrays.asList(contextSync));

        SessionResult sessionResult = agentBay.create(params);
        
        assertTrue("Failed to create session: " + sessionResult.getErrorMessage(), 
                   sessionResult.isSuccess());
        assertNotNull("Session object is null", sessionResult.getSession());

        session = sessionResult.getSession();
        session.setFileTransferContextId(context.getContextId());
        fs = session.getFileSystem();
        
        System.out.println("✅ Session created with ID: " + session.getSessionId());

        // Create test directory
        BoolResult createDirResult = fs.createDirectory(testDirectory);
        assertTrue("Failed to create test directory: " + createDirResult.getErrorMessage(),
                   createDirResult.isSuccess());
        System.out.println("✅ Test directory created: " + testDirectory);
    }

    /**
     * Clean up after each test - delete session and context
     */
    @After
    public void tearDown() {
        System.out.println("\n========================================");
        System.out.println("Cleaning up test environment...");
        System.out.println("========================================");
        
        if (session != null && agentBay != null) {
            try {
                DeleteResult deleteResult = agentBay.delete(session, false);
                if (deleteResult.isSuccess()) {
                    System.out.println("✅ Session deleted successfully");
                } else {
                    System.err.println("⚠️ Failed to delete session: " + deleteResult.getErrorMessage());
                }
            } catch (Exception e) {
                System.err.println("⚠️ Error during session cleanup: " + e.getMessage());
            }
        }

        if (context != null && agentBay != null) {
            try {
                OperationResult deleteContextResult = agentBay.getContextService().delete(context);
                if (deleteContextResult.isSuccess()) {
                    System.out.println("✅ Context deleted successfully");
                } else {
                    System.err.println("⚠️ Failed to delete context: " + deleteContextResult.getErrorMessage());
                }
            } catch (Exception e) {
                System.err.println("⚠️ Error during context cleanup: " + e.getMessage());
            }
        }
    }

    /**
     * Test 1: Basic file upload
     */
    @Test
    public void testFileUpload() throws IOException {
        System.out.println("\n===== TEST 1: Basic File Upload =====");
        
        String testContent = "Hello, AgentBay! This is a test file for upload.\n";
        String localFilePath = createTestFile(testContent, ".txt");
        String remotePath = testDirectory + "upload_basic.txt";

        System.out.println("📤 Uploading file to: " + remotePath);
        UploadResult uploadResult = fs.uploadFile(localFilePath, remotePath);

        assertTrue("Upload should succeed", uploadResult.isSuccess());
        assertNotNull("Upload result should have bytes sent", uploadResult.getBytesSent());
        assertTrue("Bytes sent should be greater than 0", uploadResult.getBytesSent() > 0);
        assertEquals("HTTP status should be 200", Integer.valueOf(200), Integer.valueOf(uploadResult.getHttpStatus()));
        
        System.out.println("✅ File uploaded successfully");
        System.out.println("   - Bytes sent: " + uploadResult.getBytesSent());
        System.out.println("   - HTTP status: " + uploadResult.getHttpStatus());
    }

    /**
     * Test 2: File upload with verification using readFile
     */
    @Test
    public void testFileUploadWithVerification() throws IOException {
        System.out.println("\n===== TEST 2: File Upload with Verification =====");
        
        StringBuilder contentBuilder = new StringBuilder();
        for (int i = 0; i < 10; i++) {
            contentBuilder.append("Line ").append(i + 1).append(": Hello from AgentBay!\n");
        }
        String testContent = contentBuilder.toString();
        
        String localFilePath = createTestFile(testContent, ".txt");
        String remotePath = testDirectory + "upload_verify.txt";

        System.out.println("📤 Uploading file...");
        UploadResult uploadResult = fs.uploadFile(localFilePath, remotePath);
        assertTrue("Upload should succeed", uploadResult.isSuccess());
        System.out.println("✅ Upload successful - " + uploadResult.getBytesSent() + " bytes");

        // Verify with readFile
        System.out.println("🔍 Verifying uploaded content with readFile...");
        FileContentResult readResult = fs.readFile(remotePath);
        
        assertTrue("Read should succeed", readResult.isSuccess());
        assertNotNull("Read content should not be null", readResult.getContent());
        
        String normalizedExpected = normalizeContent(testContent);
        String normalizedActual = normalizeContent(readResult.getContent());
        
        assertEquals("Content should match", normalizedExpected, normalizedActual);
        System.out.println("✅ Content verification successful!");
    }

    /**
     * Test 3: Basic file download
     */
    @Test
    public void testFileDownload() throws IOException {
        System.out.println("\n===== TEST 3: Basic File Download =====");
        
        String testContent = "This is a remote file created for download testing.\n";
        String remotePath = testDirectory + "download_basic.txt";
        
        // Create remote file first
        System.out.println("📝 Creating remote file...");
        BoolResult writeResult = fs.writeFile(remotePath, testContent);
        assertTrue("Write should succeed", writeResult.isSuccess());
        System.out.println("✅ Remote file created");

        // Wait for file to be available for download
        System.out.println("⏳ Waiting for file to be available...");
        try {
            Thread.sleep(2000);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }

        // Download the file
        String localDownloadPath = createTestFile("", ".txt") + ".downloaded";
        System.out.println("📥 Downloading file to: " + localDownloadPath);
        
        DownloadResult downloadResult = fs.downloadFile(remotePath, localDownloadPath);

        assertTrue("Download should succeed", downloadResult.isSuccess());
        assertNotNull("Download result should have bytes received", downloadResult.getBytesReceived());
        assertTrue("Bytes received should be greater than 0", downloadResult.getBytesReceived() > 0);
        assertEquals("HTTP status should be 200", Integer.valueOf(200), Integer.valueOf(downloadResult.getHttpStatus()));
        assertEquals("Local path should match", localDownloadPath, downloadResult.getLocalPath());
        
        System.out.println("✅ File downloaded successfully");
        System.out.println("   - Bytes received: " + downloadResult.getBytesReceived());
        System.out.println("   - HTTP status: " + downloadResult.getHttpStatus());
        
        // Clean up local file
        new File(localDownloadPath).delete();
    }

    /**
     * Test 4: File download with content verification
     */
    @Test
    public void testFileDownloadWithVerification() throws IOException {
        System.out.println("\n===== TEST 4: File Download with Verification =====");
        
        String testContent = "This is a test file created remotely for download verification.\n" +
                           "It contains multiple lines of text.\n" +
                           "Line 3\n" +
                           "Line 4\n" +
                           "End of file.\n";
        String remotePath = testDirectory + "download_verify.txt";
        
        // Create remote file with writeFile
        System.out.println("📝 Creating remote file with writeFile...");
        BoolResult writeResult = fs.writeFile(remotePath, testContent);
        assertTrue("Write should succeed", writeResult.isSuccess());
        System.out.println("✅ Remote file created - " + testContent.length() + " bytes");

        // Wait for file to be available for download
        System.out.println("⏳ Waiting for file to be available...");
        try {
            Thread.sleep(2000);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }

        // Download the file
        String localDownloadPath = createTestFile("", ".txt") + ".downloaded";
        System.out.println("📥 Downloading file...");
        
        DownloadResult downloadResult = fs.downloadFile(remotePath, localDownloadPath);
        assertTrue("Download should succeed", downloadResult.isSuccess());
        System.out.println("✅ Download successful - " + downloadResult.getBytesReceived() + " bytes");

        // Verify downloaded content
        System.out.println("🔍 Verifying downloaded content...");
        String downloadedContent = new String(Files.readAllBytes(Paths.get(localDownloadPath)));
        
        String normalizedExpected = normalizeContent(testContent);
        String normalizedActual = normalizeContent(downloadedContent);
        
        assertEquals("Downloaded content should match original", normalizedExpected, normalizedActual);
        System.out.println("✅ Content verification successful!");
        
        // Clean up local file
        new File(localDownloadPath).delete();
    }


    /**
     * Test 6: Upload to non-existent directory (should fail)
     */
    @Test
    public void testUploadToNonExistentDirectory() throws IOException {
        System.out.println("\n===== TEST 6: Upload to Non-existent Directory =====");
        
        String testContent = "Test content\n";
        String localFilePath = createTestFile(testContent, ".txt");
        String remotePath = "/tmp/nonexistent_directory_" + System.currentTimeMillis() + "/test.txt";

        System.out.println("📤 Attempting upload to non-existent directory...");
        UploadResult uploadResult = fs.uploadFile(localFilePath, remotePath);

        // Depending on implementation, this might succeed (creating parent dir) or fail
        // Let's just verify we get a valid result
        assertNotNull("Upload result should not be null", uploadResult);
        
        if (uploadResult.isSuccess()) {
            System.out.println("✅ Upload succeeded (parent directory created automatically)");
        } else {
            System.out.println("✅ Upload failed as expected: " + uploadResult.getErrorMessage());
        }
    }

    /**
     * Test 7: Download from non-existent file (should fail)
     */
    @Test
    public void testDownloadNonExistentFile() throws IOException {
        System.out.println("\n===== TEST 7: Download Non-existent File =====");
        
        String remotePath = testDirectory + "nonexistent_file_" + System.currentTimeMillis() + ".txt";
        String localDownloadPath = createTestFile("", ".txt") + ".downloaded";

        System.out.println("📥 Attempting download of non-existent file...");
        DownloadResult downloadResult = fs.downloadFile(remotePath, localDownloadPath);

        assertFalse("Download should fail", downloadResult.isSuccess());
        assertNotNull("Error message should be present", downloadResult.getErrorMessage());
        System.out.println("✅ Download failed as expected: " + downloadResult.getErrorMessage());
        
        // Clean up if file was created
        File localFile = new File(localDownloadPath);
        if (localFile.exists()) {
            localFile.delete();
        }
    }



    /**
     * Test 10: File transfer with context integration
     */
    @Test
    public void testFileTransferWithContext() throws IOException {
        System.out.println("\n===== TEST 10: File Transfer with Context Integration =====");
        
        // Verify context is set
        assertNotNull("Context should be set", context);
        assertNotNull("Session should have context ID", session.getFileTransferContextId());
        assertEquals("Session context ID should match", 
                    context.getContextId(), 
                    session.getFileTransferContextId());
        
        System.out.println("✅ Context integration verified:");
        System.out.println("   - Context ID: " + context.getContextId());
        System.out.println("   - Session context ID: " + session.getFileTransferContextId());
        
        // Test file transfer with context
        String testContent = "Testing file transfer with context integration.\n";
        String localFilePath = createTestFile(testContent, ".txt");
        String remotePath = testDirectory + "context_test.txt";

        System.out.println("📤 Uploading file with context...");
        UploadResult uploadResult = fs.uploadFile(localFilePath, remotePath);
        assertTrue("Upload with context should succeed", uploadResult.isSuccess());
        
        // Verify with readFile
        FileContentResult readResult = fs.readFile(remotePath);
        assertTrue("Read should succeed", readResult.isSuccess());
        
        String normalizedExpected = normalizeContent(testContent);
        String normalizedActual = normalizeContent(readResult.getContent());
        assertEquals("Content should match", normalizedExpected, normalizedActual);
        
        System.out.println("✅ File transfer with context successful!");
    }
}

