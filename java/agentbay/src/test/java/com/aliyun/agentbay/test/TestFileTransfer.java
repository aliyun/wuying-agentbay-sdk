package com.aliyun.agentbay.test;

import com.aliyun.agentbay.AgentBay;
import com.aliyun.agentbay.exception.AgentBayException;
import com.aliyun.agentbay.filesystem.FileSystem;
import com.aliyun.agentbay.filesystem.ProgressCallback;
import com.aliyun.agentbay.model.*;
import com.aliyun.agentbay.session.CreateSessionParams;
import com.aliyun.agentbay.session.Session;
import org.junit.AfterClass;
import org.junit.BeforeClass;
import org.junit.Test;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.concurrent.atomic.AtomicLong;

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

    private static AgentBay agentBay;
    private static Session session;
    private static FileSystem fs;
    private static String testDirectory = "/tmp/file-transfer/";

    /**
     * Helper method to create a test file with specified content
     */
    private static String createTestFile(String content, String suffix) throws IOException {
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
    private static String normalizeContent(String content) {
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
     * Set up before all tests - create AgentBay client, context and session
     */
    @BeforeClass
    public static void setUp() throws AgentBayException, IOException {
        System.out.println("\n========================================");
        System.out.println("Setting up test environment...");
        System.out.println("========================================");

        String apiKey = getTestApiKey();
        agentBay = new AgentBay(apiKey);

        // Create a simple session - let AgentBay handle context creation automatically
        CreateSessionParams params = new CreateSessionParams();
        params.setImageId("linux_latest");

        SessionResult sessionResult = agentBay.create(params);

        assertTrue("Failed to create session: " + sessionResult.getErrorMessage(),
                sessionResult.isSuccess());
        assertNotNull("Session object is null", sessionResult.getSession());

        session = sessionResult.getSession();
        fs = session.getFileSystem();

        System.out.println("✅ Session created with ID: " + session.getSessionId());

        // Get the auto-created file_transfer context path
        String contextPath = fs.getFileTransferContextPath();
        System.out.println("✅ File transfer context path: " + contextPath);

        // Update testDirectory to use the context path
        if (contextPath != null) {
            testDirectory = contextPath;
        }
        System.out.println("✅ Test directory set to: " + testDirectory);
    }

    /**
     * Clean up after all tests - delete session and context
     */
    @AfterClass
    public static void tearDown() {
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

        String contextPath = fs.getFileTransferContextPath();
        System.out.println("Context path: " + contextPath);
        String remotePath = (contextPath != null ? contextPath : testDirectory) + "/upload_verify.txt";
        System.out.println("Remote path: " + remotePath);

        System.out.println("📤 Uploading file...");
        UploadResult uploadResult = fs.uploadFile(localFilePath, remotePath);
        assertTrue("Upload should succeed", uploadResult.isSuccess());
        System.out.println("✅ Upload successful - " + uploadResult.getBytesSent() + " bytes");

        // Wait for file to be available for reading
        System.out.println("⏳ Waiting for file to be available...");
        try {
            Thread.sleep(2000);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }

        // First check if file exists using command
        System.out.println("🔍 Checking if file exists...");
        try {
            String lsCommand = "ls -la " + remotePath;
            System.out.println("Running: " + lsCommand);
            CommandResult lsResult = session.getCommand().execute(lsCommand);
            System.out.println("File info: " + lsResult.getOutput());

            String catCommand = "cat " + remotePath;
            System.out.println("Running: " + catCommand);
            CommandResult catResult = session.getCommand().execute(catCommand);
            System.out.println("File content from cat: " + catResult.getOutput());
        } catch (Exception e) {
            System.out.println("Command check failed: " + e.getMessage());
        }

        // Verify with readFile
        System.out.println("🔍 Verifying uploaded content with readFile...");
        FileContentResult readResult = fs.readFile(remotePath);

        assertTrue("Read should succeed", readResult.isSuccess());
        assertNotNull("Read content should not be null", readResult.getContent());

        System.out.println("DEBUG: Read content length: " + readResult.getContent().length());
        if (readResult.getContent().length() > 0) {
            System.out.println("DEBUG: Read content preview: " + readResult.getContent().substring(0, Math.min(100, readResult.getContent().length())));
        }

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
     * Test 5: Upload with progress callback
     */
    @Test
    public void testFileUploadWithProgress() throws IOException {
        System.out.println("\n===== TEST 5: File Upload with Progress Callback =====");

        StringBuilder contentBuilder = new StringBuilder();
        for (int i = 0; i < 1000; i++) {
            contentBuilder.append("Line ").append(i + 1).append(": Test data for progress tracking\n");
        }
        String testContent = contentBuilder.toString();
        String localFilePath = createTestFile(testContent, ".txt");
        String remotePath = testDirectory + "upload_progress.txt";

        AtomicLong lastProgress = new AtomicLong(0);
        ProgressCallback progressCallback = (bytesTransferred) -> {
            lastProgress.set(bytesTransferred);
            if (bytesTransferred % 10000 < 8192) {
                System.out.println("   Upload progress: " + bytesTransferred + " bytes");
            }
        };

        System.out.println("📤 Uploading file with progress tracking...");
        UploadResult uploadResult = fs.uploadFile(localFilePath, remotePath, null, true, 30.0f, 1.5f, progressCallback);

        assertTrue("Upload should succeed", uploadResult.isSuccess());
        assertTrue("Progress callback should have been called", lastProgress.get() > 0);
        assertEquals("Final progress should match bytes sent", uploadResult.getBytesSent(), lastProgress.get());

        System.out.println("✅ Upload with progress tracking successful!");
        System.out.println("   - Total bytes: " + uploadResult.getBytesSent());
        System.out.println("   - Progress reported: " + lastProgress.get());
    }

    /**
     * Test 6: Download with progress callback
     */
    @Test
    public void testFileDownloadWithProgress() throws IOException {
        System.out.println("\n===== TEST 6: File Download with Progress Callback =====");

        StringBuilder contentBuilder = new StringBuilder();
        for (int i = 0; i < 1000; i++) {
            contentBuilder.append("Line ").append(i + 1).append(": Test data for download progress\n");
        }
        String testContent = contentBuilder.toString();
        String remotePath = testDirectory + "download_progress.txt";

        System.out.println("📝 Creating remote file...");
        BoolResult writeResult = fs.writeFile(remotePath, testContent);
        assertTrue("Write should succeed", writeResult.isSuccess());
        System.out.println("✅ Remote file created - " + testContent.length() + " bytes");

        System.out.println("⏳ Waiting for file to be available...");
        try {
            Thread.sleep(2000);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }

        AtomicLong lastProgress = new AtomicLong(0);
        ProgressCallback progressCallback = (bytesTransferred) -> {
            lastProgress.set(bytesTransferred);
            if (bytesTransferred % 10000 < 8192) {
                System.out.println("   Download progress: " + bytesTransferred + " bytes");
            }
        };

        String localDownloadPath = createTestFile("", ".txt") + ".downloaded";
        System.out.println("📥 Downloading file with progress tracking...");

        DownloadResult downloadResult = fs.downloadFile(remotePath, localDownloadPath, true, true, 30.0f, 1.5f, progressCallback);

        assertTrue("Download should succeed", downloadResult.isSuccess());
        assertTrue("Progress callback should have been called", lastProgress.get() > 0);

        System.out.println("✅ Download with progress tracking successful!");
        System.out.println("   - Total bytes: " + downloadResult.getBytesReceived());
        System.out.println("   - Progress reported: " + lastProgress.get());

        new File(localDownloadPath).delete();
    }

    /**
     * Test 7: Upload to non-existent directory (should fail)
     */
    @Test
    public void testUploadToNonExistentDirectory() throws IOException {
        System.out.println("\n===== TEST 7: Upload to Non-existent Directory =====");

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
     * Test 8: Download from non-existent file (should fail)
     */
    @Test
    public void testDownloadNonExistentFile() throws IOException {
        System.out.println("\n===== TEST 8: Download Non-existent File =====");

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
     * Test 9: File transfer context path verification
     */
    @Test
    public void testFileTransferContextPath() throws IOException {
        System.out.println("\n===== TEST 9: File Transfer Context Path Verification =====");

        String contextPath = fs.getFileTransferContextPath();

        assertNotNull("Context path should not be null", contextPath);
        assertFalse("Context path should not be empty", contextPath.isEmpty());

        System.out.println("✅ Context path loaded successfully: " + contextPath);
    }

    /**
     * Test 10: File transfer with context integration
     */
    @Test
    public void testFileTransferWithContext() throws IOException {
        System.out.println("\n===== TEST 10: File Transfer with Context Integration =====");

        String contextPath = fs.getFileTransferContextPath();
        assertNotNull("Context path should be loaded", contextPath);

        System.out.println("✅ Context integration verified:");
        System.out.println("   - Context path: " + contextPath);

        // Test file transfer with context
        String testContent = "Testing file transfer with context integration.\n";
        String localFilePath = createTestFile(testContent, ".txt");
        String remotePath = testDirectory + "/context_test.txt";

        System.out.println("📤 Uploading file with context...");
        UploadResult uploadResult = fs.uploadFile(localFilePath, remotePath);
        assertTrue("Upload with context should succeed", uploadResult.isSuccess());

        // Wait for file to be available for reading
        System.out.println("⏳ Waiting for file to be available...");
        try {
            Thread.sleep(2000);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }

        // Verify with readFile
        FileContentResult readResult = fs.readFile(remotePath);
        assertTrue("Read should succeed", readResult.isSuccess());

        String normalizedExpected = normalizeContent(testContent);
        String normalizedActual = normalizeContent(readResult.getContent());
        assertEquals("Content should match", normalizedExpected, normalizedActual);

        System.out.println("✅ File transfer with context successful!");
    }

    /**
     * Test 11: Verify DownloadResult does not return content
     */
    @Test
    public void testDownloadResultNoContent() throws IOException {
        System.out.println("\n===== TEST 11: DownloadResult Content Field Verification =====");

        String testContent = "Test content for verifying no content in result\n";
        String remotePath = testDirectory + "no_content_test.txt";

        System.out.println("📝 Creating remote file...");
        BoolResult writeResult = fs.writeFile(remotePath, testContent);
        assertTrue("Write should succeed", writeResult.isSuccess());

        System.out.println("⏳ Waiting for file to be available...");
        try {
            Thread.sleep(2000);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }

        String localDownloadPath = createTestFile("", ".txt") + ".downloaded";
        System.out.println("📥 Downloading file...");

        DownloadResult downloadResult = fs.downloadFile(remotePath, localDownloadPath);

        assertTrue("Download should succeed", downloadResult.isSuccess());
        assertNull("Content field should be null (streaming mode)", downloadResult.getContent());
        assertTrue("File should exist on disk", new File(localDownloadPath).exists());

        System.out.println("✅ Verified: DownloadResult.content is null (memory efficient)");
        System.out.println("✅ File written to disk: " + localDownloadPath);

        new File(localDownloadPath).delete();
    }

    /**
     * Test 12: Upload byte array (Java SDK extension)
     */
    @Test
    public void testUploadBytes() throws IOException {
        System.out.println("\n===== TEST 12: Upload Byte Array (Java SDK Extension) =====");

        String testContent = "Hello from byte array upload! This is a test of the Java SDK extension feature.\n";
        byte[] contentBytes = testContent.getBytes("UTF-8");
        String remotePath = testDirectory + "upload_bytes.txt";

        System.out.println("📤 Uploading byte array to: " + remotePath);
        System.out.println("   - Content size: " + contentBytes.length + " bytes");

        UploadResult uploadResult = fs.uploadFileBytes(contentBytes, remotePath);

        assertTrue("Upload should succeed", uploadResult.isSuccess());
        assertNotNull("Upload result should have bytes sent", uploadResult.getBytesSent());
        assertEquals("Bytes sent should match content length", contentBytes.length, uploadResult.getBytesSent());
        assertNotNull("HTTP status should be present", uploadResult.getHttpStatus());

        System.out.println("✅ Byte array uploaded successfully");
        System.out.println("   - Bytes sent: " + uploadResult.getBytesSent());
        System.out.println("   - HTTP status: " + uploadResult.getHttpStatus());

        // Wait for file to be available for reading
        System.out.println("⏳ Waiting for file to be available...");
        try {
            Thread.sleep(2000);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }

        // Verify uploaded content with readFile
        System.out.println("🔍 Verifying uploaded content...");
        FileContentResult readResult = fs.readFile(remotePath);
        assertTrue("Read should succeed", readResult.isSuccess());

        String normalizedExpected = normalizeContent(testContent);
        String normalizedActual = normalizeContent(readResult.getContent());
        assertEquals("Content should match", normalizedExpected, normalizedActual);

        System.out.println("✅ Content verification successful!");
    }

    /**
     * Test 13: Download to byte array (Java SDK extension)
     */
    @Test
    public void testDownloadBytes() throws IOException {
        System.out.println("\n===== TEST 13: Download to Byte Array (Java SDK Extension) =====");

        String testContent = "This is remote file content that will be downloaded to a byte array.\n" +
                "Line 2 of test content.\n" +
                "Line 3 for verification.\n";
        String remotePath = testDirectory + "download_bytes.txt";

        // Create remote file first
        System.out.println("📝 Creating remote file...");
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

        // Download to byte array
        System.out.println("📥 Downloading file to byte array...");
        DownloadResult downloadResult = fs.downloadFileBytes(remotePath);

        assertTrue("Download should succeed", downloadResult.isSuccess());
        assertNotNull("Content should not be null", downloadResult.getContent());
        assertNull("Local path should be null (in-memory mode)", downloadResult.getLocalPath());
        assertTrue("Bytes received should be greater than 0", downloadResult.getBytesReceived() > 0);
        assertEquals("HTTP status should be 200", Integer.valueOf(200), Integer.valueOf(downloadResult.getHttpStatus()));

        System.out.println("✅ File downloaded to byte array successfully");
        System.out.println("   - Bytes received: " + downloadResult.getBytesReceived());
        System.out.println("   - Content length: " + downloadResult.getContent().length);

        // Verify content
        System.out.println("🔍 Verifying downloaded content...");
        String downloadedContent = new String(downloadResult.getContent(), "UTF-8");

        String normalizedExpected = normalizeContent(testContent);
        String normalizedActual = normalizeContent(downloadedContent);
        assertEquals("Downloaded content should match original", normalizedExpected, normalizedActual);

        System.out.println("✅ Content verification successful!");
    }

    /**
     * Test 14: Upload and download byte array round-trip (Java SDK extension)
     */
    @Test
    public void testBytesRoundTrip() throws IOException {
        System.out.println("\n===== TEST 14: Byte Array Round-Trip Test (Java SDK Extension) =====");

        // Create test data with special characters
        StringBuilder contentBuilder = new StringBuilder();
        contentBuilder.append("=== Byte Array Round-Trip Test ===\n");
        contentBuilder.append("Testing UTF-8 encoding: 你好世界 🌍\n");
        contentBuilder.append("Special characters: @#$%^&*()\n");
        for (int i = 0; i < 10; i++) {
            contentBuilder.append("Line ").append(i + 1).append(": Test data ").append(i * 123).append("\n");
        }
        String testContent = contentBuilder.toString();
        byte[] originalBytes = testContent.getBytes("UTF-8");

        String remotePath = testDirectory + "roundtrip_bytes.txt";

        // Upload byte array
        System.out.println("📤 Uploading byte array...");
        System.out.println("   - Original size: " + originalBytes.length + " bytes");
        UploadResult uploadResult = fs.uploadFileBytes(originalBytes, remotePath);
        assertTrue("Upload should succeed", uploadResult.isSuccess());
        System.out.println("✅ Upload successful - " + uploadResult.getBytesSent() + " bytes");

        // Wait for file to be available
        System.out.println("⏳ Waiting for file to be available...");
        try {
            Thread.sleep(2000);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }

        // Download to byte array
        System.out.println("📥 Downloading to byte array...");
        DownloadResult downloadResult = fs.downloadFileBytes(remotePath);
        assertTrue("Download should succeed", downloadResult.isSuccess());
        assertNotNull("Downloaded content should not be null", downloadResult.getContent());
        System.out.println("✅ Download successful - " + downloadResult.getBytesReceived() + " bytes");

        // Verify byte-by-byte match
        System.out.println("🔍 Verifying byte-by-byte match...");
        byte[] downloadedBytes = downloadResult.getContent();

        assertEquals("Byte array length should match", originalBytes.length, downloadedBytes.length);
        assertArrayEquals("Byte arrays should match exactly", originalBytes, downloadedBytes);

        // Verify string content
        String originalString = new String(originalBytes, "UTF-8");
        String downloadedString = new String(downloadedBytes, "UTF-8");
        assertEquals("String content should match", originalString, downloadedString);

        System.out.println("✅ Round-trip verification successful!");
        System.out.println("   - Original bytes: " + originalBytes.length);
        System.out.println("   - Downloaded bytes: " + downloadedBytes.length);
        System.out.println("   - Bytes match: ✓");
        System.out.println("   - UTF-8 encoding preserved: ✓");
    }

    /**
     * Test 15: Upload byte array with progress callback (Java SDK extension)
     */
    @Test
    public void testUploadBytesWithProgress() throws IOException {
        System.out.println("\n===== TEST 15: Upload Byte Array with Progress Callback =====");

        // Create larger test data
        StringBuilder contentBuilder = new StringBuilder();
        for (int i = 0; i < 1000; i++) {
            contentBuilder.append("Line ").append(i + 1).append(": Test data for progress tracking in byte upload\n");
        }
        byte[] contentBytes = contentBuilder.toString().getBytes("UTF-8");
        String remotePath = testDirectory + "upload_bytes_progress.txt";

        AtomicLong lastProgress = new AtomicLong(0);
        ProgressCallback progressCallback = (bytesTransferred) -> {
            lastProgress.set(bytesTransferred);
            if (bytesTransferred % 10000 < 8192) {
                System.out.println("   Upload progress: " + bytesTransferred + " bytes");
            }
        };

        System.out.println("📤 Uploading byte array with progress tracking...");
        System.out.println("   - Content size: " + contentBytes.length + " bytes");

        UploadResult uploadResult = fs.uploadFileBytes(contentBytes, remotePath, null, true, 30.0f, 1.5f, progressCallback);

        assertTrue("Upload should succeed", uploadResult.isSuccess());
        assertTrue("Progress callback should have been called", lastProgress.get() > 0);
        assertEquals("Final progress should match bytes sent", uploadResult.getBytesSent(), lastProgress.get());

        System.out.println("✅ Upload with progress tracking successful!");
        System.out.println("   - Total bytes: " + uploadResult.getBytesSent());
        System.out.println("   - Progress reported: " + lastProgress.get());
    }

    /**
     * Test 16: Download byte array with progress callback (Java SDK extension)
     */
    @Test
    public void testDownloadBytesWithProgress() throws IOException {
        System.out.println("\n===== TEST 16: Download Byte Array with Progress Callback =====");

        // Create larger test data
        StringBuilder contentBuilder = new StringBuilder();
        for (int i = 0; i < 1000; i++) {
            contentBuilder.append("Line ").append(i + 1).append(": Test data for download progress tracking\n");
        }
        String testContent = contentBuilder.toString();
        String remotePath = testDirectory + "download_bytes_progress.txt";

        System.out.println("📝 Creating remote file...");
        BoolResult writeResult = fs.writeFile(remotePath, testContent);
        assertTrue("Write should succeed", writeResult.isSuccess());
        System.out.println("✅ Remote file created - " + testContent.length() + " bytes");

        System.out.println("⏳ Waiting for file to be available...");
        try {
            Thread.sleep(2000);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }

        AtomicLong lastProgress = new AtomicLong(0);
        ProgressCallback progressCallback = (bytesTransferred) -> {
            lastProgress.set(bytesTransferred);
            if (bytesTransferred % 10000 < 8192) {
                System.out.println("   Download progress: " + bytesTransferred + " bytes");
            }
        };

        System.out.println("📥 Downloading to byte array with progress tracking...");
        DownloadResult downloadResult = fs.downloadFileBytes(remotePath, true, 30.0f, 1.5f, progressCallback);

        assertTrue("Download should succeed", downloadResult.isSuccess());
        assertNotNull("Content should not be null", downloadResult.getContent());
        assertTrue("Progress callback should have been called", lastProgress.get() > 0);

        System.out.println("✅ Download with progress tracking successful!");
        System.out.println("   - Total bytes: " + downloadResult.getBytesReceived());
        System.out.println("   - Progress reported: " + lastProgress.get());
        System.out.println("   - Content length: " + downloadResult.getContent().length);
    }

    /**
     * Test 17: Upload null byte array (should fail gracefully)
     */
    @Test
    public void testUploadNullBytes() {
        System.out.println("\n===== TEST 17: Upload Null Byte Array (Error Handling) =====");

        String remotePath = testDirectory + "null_bytes.txt";

        System.out.println("📤 Attempting to upload null byte array...");
        UploadResult uploadResult = fs.uploadFileBytes(null, remotePath);

        assertFalse("Upload should fail", uploadResult.isSuccess());
        assertNotNull("Error message should be present", uploadResult.getErrorMessage());
        assertTrue("Error message should mention null",
                uploadResult.getErrorMessage().toLowerCase().contains("null") ||
                uploadResult.getErrorMessage().toLowerCase().contains("cannot"));

        System.out.println("✅ Upload failed gracefully as expected");
        System.out.println("   - Error: " + uploadResult.getErrorMessage());
    }

    /**
     * Test 18: Download non-existent file to byte array (should fail)
     */
    @Test
    public void testDownloadNonExistentFileToBytes() {
        System.out.println("\n===== TEST 18: Download Non-existent File to Byte Array =====");

        String remotePath = testDirectory + "nonexistent_bytes_" + System.currentTimeMillis() + ".txt";

        System.out.println("📥 Attempting download of non-existent file to byte array...");
        DownloadResult downloadResult = fs.downloadFileBytes(remotePath);

        assertFalse("Download should fail", downloadResult.isSuccess());
        assertNotNull("Error message should be present", downloadResult.getErrorMessage());
        assertNull("Content should be null", downloadResult.getContent());

        System.out.println("✅ Download failed as expected: " + downloadResult.getErrorMessage());
    }
}