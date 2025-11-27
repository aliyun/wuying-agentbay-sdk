package com.aliyun.agentbay.test;

import com.aliyun.agentbay.AgentBay;
import com.aliyun.agentbay.filesystem.FileSystem;
import com.aliyun.agentbay.model.DeleteResult;
import com.aliyun.agentbay.model.FileContentResult;
import com.aliyun.agentbay.model.SessionResult;
import com.aliyun.agentbay.oss.OSS;
import com.aliyun.agentbay.oss.OSSClientResult;
import com.aliyun.agentbay.oss.OSSDownloadResult;
import com.aliyun.agentbay.oss.OSSUploadResult;
import com.aliyun.agentbay.session.CreateSessionParams;
import com.aliyun.agentbay.session.Session;
import org.junit.*;
import org.junit.runners.MethodSorters;

import static org.junit.Assert.*;
import static org.junit.Assume.assumeTrue;

/**
 * Test class for OSS Management functionality
 * 
 * This test class validates:
 * 1. OSS environment initialization
 * 2. File upload to OSS
 * 3. File download from OSS
 * 4. Anonymous upload operations
 * 5. Error handling for invalid credentials
 */
@FixMethodOrder(MethodSorters.NAME_ASCENDING)
public class TestOSSManagement {
    
    private static AgentBay agentBay;
    private static Session session;
    private static OSS oss;
    private static FileSystem fs;
    
    // Test configuration
    private static final String TEST_FILE_PATH = "/tmp/test_oss_upload.txt";
    private static final String TEST_CONTENT = "This is a test file for OSS upload validation.";
    private static final String TEST_OBJECT_KEY = "test-object.txt";
    private static final String TEST_DOWNLOAD_PATH = "/tmp/test_oss_download.txt";
    
    // OSS credentials from environment
    private static String ossAccessKeyId;
    private static String ossAccessKeySecret;
    private static String ossSecurityToken;
    private static String ossEndpoint;
    private static String ossRegion;
    private static String ossBucket;
    private static String ossUploadUrl;
    
    @BeforeClass
    public static void setUp() throws Exception {
        System.out.println("\n=== Setting up OSS Management Tests ===");
        
        // Get API Key
        String apiKey = System.getenv("AGENTBAY_API_KEY");
        assertNotNull("AGENTBAY_API_KEY environment variable must be set", apiKey);
        assertFalse("AGENTBAY_API_KEY cannot be empty", apiKey.isEmpty());
        
        // Get OSS credentials from environment
        ossAccessKeyId = System.getenv("OSS_ACCESS_KEY_ID");
        ossAccessKeySecret = System.getenv("OSS_ACCESS_KEY_SECRET");
        ossSecurityToken = System.getenv("OSS_SECURITY_TOKEN");
        ossEndpoint = System.getenv("OSS_ENDPOINT");
        ossRegion = System.getenv("OSS_REGION");
        ossBucket = System.getenv("OSS_TEST_BUCKET");
        ossUploadUrl = System.getenv("OSS_TEST_UPLOAD_URL");
        
        System.out.println("OSS_ACCESS_KEY_ID: " + (ossAccessKeyId != null ? "Set" : "Not set"));
        System.out.println("OSS_ACCESS_KEY_SECRET: " + (ossAccessKeySecret != null ? "Set" : "Not set"));
        System.out.println("OSS_SECURITY_TOKEN: " + (ossSecurityToken != null ? "Set" : "Not set"));
        System.out.println("OSS_ENDPOINT: " + ossEndpoint);
        System.out.println("OSS_REGION: " + ossRegion);
        System.out.println("OSS_TEST_BUCKET: " + ossBucket);
        
        // Initialize AgentBay
        agentBay = new AgentBay(apiKey);
        
        // Create session
        System.out.println("\nCreating a new session...");
        CreateSessionParams params = new CreateSessionParams();
        params.setImageId("code_latest");
        
        SessionResult sessionResult = agentBay.create(params);
        assertTrue("Session creation should succeed", sessionResult.isSuccess());
        assertNotNull("Session should not be null", sessionResult.getSession());
        
        session = sessionResult.getSession();
        oss = session.getOss();
        fs = session.getFileSystem();
        
        System.out.println("Session created with ID: " + session.getSessionId());
        System.out.println("\n=== Setup Complete ===\n");
    }
    
    @AfterClass
    public static void tearDown() throws Exception {
        System.out.println("\n=== Cleaning up OSS Management Tests ===");
        
        if (session != null) {
            try {
                System.out.println("Deleting the session...");
                DeleteResult deleteResult = session.delete();
                System.out.println("Session deleted successfully. Request ID: " + deleteResult.getRequestId());
            } catch (Exception e) {
                System.err.println("Error deleting session: " + e.getMessage());
            }
        }
        
        System.out.println("=== Cleanup Complete ===\n");
    }
    
    @Test
    public void test01_OSSEnvInit() throws Exception {
        System.out.println("\n--- Test 1: OSS Environment Initialization ---");
        
        // Skip if credentials are not provided
        if (ossAccessKeyId == null || ossAccessKeySecret == null || ossSecurityToken == null) {
            System.out.println("Skipping test: OSS credentials not provided");
            assumeTrue("OSS credentials not provided", false);
            return;
        }
        
        OSSClientResult clientResult = oss.envInit(
            ossAccessKeyId,
            ossAccessKeySecret,
            ossSecurityToken,
            ossEndpoint,
            ossRegion
        );
        
        assertNotNull("Client result should not be null", clientResult);
        assertNotNull("Request ID should not be null", clientResult.getRequestId());
        assertTrue("env_init should succeed: " + clientResult.getErrorMessage(), clientResult.isSuccess());
        assertNotNull("Client config should not be null", clientResult.getClientConfig());
        
        System.out.println("✓ env_init successful");
        System.out.println("  Request ID: " + clientResult.getRequestId());
        System.out.println("  Client config: " + clientResult.getClientConfig());
    }
    
    @Test
    public void test02_OSSUpload() throws Exception {
        System.out.println("\n--- Test 2: File Upload to OSS ---");
        
        // Skip if credentials or bucket are not provided
        if (ossAccessKeyId == null || ossAccessKeySecret == null || 
            ossSecurityToken == null || ossBucket == null) {
            System.out.println("Skipping test: OSS credentials or bucket not provided");
            assumeTrue("OSS credentials or bucket not provided", false);
            return;
        }
        
        // Initialize OSS environment first
        OSSClientResult clientResult = oss.envInit(
            ossAccessKeyId,
            ossAccessKeySecret,
            ossSecurityToken,
            ossEndpoint,
            ossRegion
        );
        assertTrue("env_init should succeed before upload", clientResult.isSuccess());
        
        // Create a test file
        System.out.println("Creating test file: " + TEST_FILE_PATH);
        fs.writeFile(TEST_FILE_PATH, TEST_CONTENT, "overwrite");
        
        // Upload file
        System.out.println("Uploading file to OSS bucket: " + ossBucket);
        OSSUploadResult uploadResult = oss.upload(ossBucket, TEST_OBJECT_KEY, TEST_FILE_PATH);
        
        assertNotNull("Upload result should not be null", uploadResult);
        assertNotNull("Request ID should not be null", uploadResult.getRequestId());
        assertTrue("Upload should succeed: " + uploadResult.getErrorMessage(), uploadResult.isSuccess());
        assertNotNull("Upload content should not be null", uploadResult.getContent());
        
        System.out.println("✓ Upload successful");
        System.out.println("  Request ID: " + uploadResult.getRequestId());
        System.out.println("  Content: " + uploadResult.getContent());
    }
    
    @Test
    public void test03_OSSDownload() throws Exception {
        System.out.println("\n--- Test 3: File Download from OSS ---");
        
        // Skip if credentials or bucket are not provided
        if (ossAccessKeyId == null || ossAccessKeySecret == null || 
            ossSecurityToken == null || ossBucket == null) {
            System.out.println("Skipping test: OSS credentials or bucket not provided");
            assumeTrue("OSS credentials or bucket not provided", false);
            return;
        }
        
        // Initialize OSS environment first
        OSSClientResult clientResult = oss.envInit(
            ossAccessKeyId,
            ossAccessKeySecret,
            ossSecurityToken,
            ossEndpoint,
            ossRegion
        );
        assertTrue("env_init should succeed before download", clientResult.isSuccess());
        
        // Create and upload a test file first
        fs.writeFile(TEST_FILE_PATH, TEST_CONTENT, "overwrite");
        OSSUploadResult uploadResult = oss.upload(ossBucket, TEST_OBJECT_KEY, TEST_FILE_PATH);
        assertTrue("Upload should succeed before download test", uploadResult.isSuccess());
        
        // Download file
        System.out.println("Downloading file from OSS bucket: " + ossBucket);
        OSSDownloadResult downloadResult = oss.download(
            ossBucket,
            TEST_OBJECT_KEY,
            TEST_DOWNLOAD_PATH
        );
        
        assertNotNull("Download result should not be null", downloadResult);
        assertNotNull("Request ID should not be null", downloadResult.getRequestId());
        assertTrue("Download should succeed: " + downloadResult.getErrorMessage(), downloadResult.isSuccess());
        assertNotNull("Download content should not be null", downloadResult.getContent());
        
        // Verify downloaded file content
        FileContentResult fileContentResult = fs.readFile(TEST_DOWNLOAD_PATH);
        String downloadedContent = fileContentResult.getContent();
        assertEquals("Downloaded content should match original", TEST_CONTENT, downloadedContent);
        
        System.out.println("✓ Download successful");
        System.out.println("  Request ID: " + downloadResult.getRequestId());
        System.out.println("  Content: " + downloadResult.getContent());
        System.out.println("  Downloaded content matches original: " + downloadedContent.equals(TEST_CONTENT));
    }
    
    @Test
    public void test04_OSSUploadAnonymous() throws Exception {
        System.out.println("\n--- Test 4: Anonymous File Upload ---");
        
        // Skip if upload URL is not provided
        if (ossUploadUrl == null || ossUploadUrl.isEmpty()) {
            System.out.println("Skipping test: OSS_TEST_UPLOAD_URL not provided");
            assumeTrue("OSS_TEST_UPLOAD_URL not provided", false);
            return;
        }
        
        // Create a test file
        System.out.println("Creating test file: " + TEST_FILE_PATH);
        fs.writeFile(TEST_FILE_PATH, TEST_CONTENT, "overwrite");
        
        // Upload file anonymously
        System.out.println("Uploading file anonymously to URL: " + ossUploadUrl);
        OSSUploadResult uploadAnonResult = oss.uploadAnonymous(ossUploadUrl, TEST_FILE_PATH);
        
        assertNotNull("Upload anonymous result should not be null", uploadAnonResult);
        assertNotNull("Request ID should not be null", uploadAnonResult.getRequestId());
        assertTrue("Anonymous upload should succeed: " + uploadAnonResult.getErrorMessage(), uploadAnonResult.isSuccess());
        assertNotNull("Upload content should not be null", uploadAnonResult.getContent());
        
        System.out.println("✓ Anonymous upload successful");
        System.out.println("  Request ID: " + uploadAnonResult.getRequestId());
        System.out.println("  Content: " + uploadAnonResult.getContent());
    }
    
    @Test
    public void test05_OSSEnvInitWithInvalidCredentials() throws Exception {
        System.out.println("\n--- Test 5: OSS env_init with Invalid Credentials ---");
        
        // Test with invalid credentials
        OSSClientResult clientResult = oss.envInit(
            "invalid_access_key_id",
            "invalid_access_key_secret",
            "invalid_security_token",
            ossEndpoint,
            ossRegion
        );
        
        assertNotNull("Client result should not be null", clientResult);
        assertNotNull("Request ID should not be null", clientResult.getRequestId());
        
        // The result might succeed or fail depending on validation timing
        // If it fails, error message should be present
        if (!clientResult.isSuccess()) {
            assertNotNull("Error message should not be null when failed", clientResult.getErrorMessage());
            System.out.println("✓ Invalid credentials handled correctly");
            System.out.println("  Error message: " + clientResult.getErrorMessage());
        } else {
            System.out.println("⚠ env_init succeeded with invalid credentials (validation may occur later)");
        }
    }
    
    @Test
    public void test06_UploadWithoutEnvInit() throws Exception {
        System.out.println("\n--- Test 6: Upload without env_init ---");
        
        // Skip if bucket is not provided
        if (ossBucket == null) {
            System.out.println("Skipping test: OSS_TEST_BUCKET not provided");
            assumeTrue("OSS_TEST_BUCKET not provided", false);
            return;
        }
        
        // Create a new session to ensure no env_init has been called
        CreateSessionParams params = new CreateSessionParams();
        params.setImageId("code_latest");
        SessionResult sessionResult = agentBay.create(params);
        Session newSession = sessionResult.getSession();
        OSS newOss = newSession.getOss();
        FileSystem newFs = newSession.getFileSystem();
        
        try {
            // Create a test file
            newFs.writeFile(TEST_FILE_PATH, TEST_CONTENT, "overwrite");
            
            // Try to upload without calling env_init first
            System.out.println("Attempting upload without env_init...");
            OSSUploadResult uploadResult = newOss.upload(ossBucket, TEST_OBJECT_KEY, TEST_FILE_PATH);
            
            assertNotNull("Upload result should not be null", uploadResult);
            assertFalse("Upload should fail without env_init", uploadResult.isSuccess());
            assertNotNull("Error message should be present", uploadResult.getErrorMessage());
            
            System.out.println("✓ Upload correctly failed without env_init");
            System.out.println("  Error message: " + uploadResult.getErrorMessage());
        } finally {
            // Clean up new session
            newSession.delete();
        }
    }
    
    @Test
    public void test07_UploadWithNonExistentFile() throws Exception {
        System.out.println("\n--- Test 7: Upload with Non-existent File ---");
        
        // Skip if credentials or bucket are not provided
        if (ossAccessKeyId == null || ossAccessKeySecret == null || 
            ossSecurityToken == null || ossBucket == null) {
            System.out.println("Skipping test: OSS credentials or bucket not provided");
            assumeTrue("OSS credentials or bucket not provided", false);
            return;
        }
        
        // Initialize OSS environment
        oss.envInit(ossAccessKeyId, ossAccessKeySecret, ossSecurityToken, ossEndpoint, ossRegion);
        
        // Try to upload non-existent file
        String nonExistentFile = "/tmp/non_existent_file_12345.txt";
        System.out.println("Attempting to upload non-existent file: " + nonExistentFile);
        
        OSSUploadResult uploadResult = oss.upload(ossBucket, TEST_OBJECT_KEY, nonExistentFile);
        
        assertNotNull("Upload result should not be null", uploadResult);
        assertFalse("Upload should fail with non-existent file", uploadResult.isSuccess());
        assertNotNull("Error message should be present", uploadResult.getErrorMessage());
        
        System.out.println("✓ Upload correctly failed with non-existent file");
        System.out.println("  Error message: " + uploadResult.getErrorMessage());
    }
    
    @Test
    public void test08_DownloadWithNonExistentObject() throws Exception {
        System.out.println("\n--- Test 8: Download with Non-existent Object ---");
        
        // Skip if credentials or bucket are not provided
        if (ossAccessKeyId == null || ossAccessKeySecret == null || 
            ossSecurityToken == null || ossBucket == null) {
            System.out.println("Skipping test: OSS credentials or bucket not provided");
            assumeTrue("OSS credentials or bucket not provided", false);
            return;
        }
        
        // Initialize OSS environment
        oss.envInit(ossAccessKeyId, ossAccessKeySecret, ossSecurityToken, ossEndpoint, ossRegion);
        
        // Try to download non-existent object
        String nonExistentObject = "non_existent_object_12345.txt";
        System.out.println("Attempting to download non-existent object: " + nonExistentObject);
        
        OSSDownloadResult downloadResult = oss.download(
            ossBucket,
            nonExistentObject,
            TEST_DOWNLOAD_PATH
        );
        
        assertNotNull("Download result should not be null", downloadResult);
        assertFalse("Download should fail with non-existent object", downloadResult.isSuccess());
        assertNotNull("Error message should be present", downloadResult.getErrorMessage());
        
        System.out.println("✓ Download correctly failed with non-existent object");
        System.out.println("  Error message: " + downloadResult.getErrorMessage());
    }
}


