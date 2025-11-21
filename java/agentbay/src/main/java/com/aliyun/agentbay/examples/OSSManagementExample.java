package com.aliyun.agentbay.examples;

import com.aliyun.agentbay.AgentBay;
import com.aliyun.agentbay.exception.AgentBayException;
import com.aliyun.agentbay.exception.OSSException;
import com.aliyun.agentbay.filesystem.FileSystem;
import com.aliyun.agentbay.model.DeleteResult;
import com.aliyun.agentbay.model.SessionResult;
import com.aliyun.agentbay.oss.OSS;
import com.aliyun.agentbay.oss.OSSClientResult;
import com.aliyun.agentbay.oss.OSSDownloadResult;
import com.aliyun.agentbay.oss.OSSUploadResult;
import com.aliyun.agentbay.session.CreateSessionParams;
import com.aliyun.agentbay.session.Session;

/**
 * OSS Management Example - Java equivalent of Python OSS management
 * 
 * This example demonstrates how to:
 * 1. Initialize OSS environment with credentials
 * 2. Upload files to OSS
 * 3. Download files from OSS
 * 4. Anonymous upload and download operations
 */
public class OSSManagementExample {
    
    /**
     * Helper function to get OSS credentials from environment variables or use defaults
     */
    private static OSSCredentials getOSSCredentials() {
        return new OSSCredentials(
            System.getenv("OSS_ACCESS_KEY_ID"),
            System.getenv("OSS_ACCESS_KEY_SECRET"),
            System.getenv("OSS_SECURITY_TOKEN"),
            System.getenv("OSS_ENDPOINT"),
            System.getenv("OSS_REGION")
        );
    }
    
    /**
     * Helper class to hold OSS credentials
     */
    private static class OSSCredentials {
        public final String accessKeyId;
        public final String accessKeySecret;
        public final String securityToken;
        public final String endpoint;
        public final String region;
        
        public OSSCredentials(String accessKeyId, String accessKeySecret, String securityToken,
                             String endpoint, String region) {
            this.accessKeyId = accessKeyId;
            this.accessKeySecret = accessKeySecret;
            this.securityToken = securityToken;
            this.endpoint = endpoint;
            this.region = region;
        }
    }
    
    public static void main(String[] args) {
        // Get API Key
        String apiKey = System.getenv("AGENTBAY_API_KEY");
        if (apiKey == null || apiKey.isEmpty()) {
            apiKey = "";  // Replace with your actual API key if needed
        }
        
        Session session = null;
        
        try {
            AgentBay agentBay = new AgentBay(apiKey);
            
            // Create session
            System.out.println("\nCreating a new session...");
            CreateSessionParams params = new CreateSessionParams();
            params.setImageId("code_latest");
            
            SessionResult sessionResult = agentBay.create(params);
            if (!sessionResult.isSuccess() || sessionResult.getSession() == null) {
                System.out.println("Failed to create session");
                return;
            }
            
            session = sessionResult.getSession();
            System.out.println("Session created with ID: " + session.getSessionId());
            
            OSS oss = session.getOss();
            
            // env_init
            System.out.println("\nTesting env_init...");
            OSSCredentials credentials = getOSSCredentials();
            OSSClientResult clientResult = oss.envInit(
                credentials.accessKeyId,
                credentials.accessKeySecret,
                credentials.securityToken,
                credentials.endpoint,
                credentials.region
            );
            
            System.out.println("env_init result: " + clientResult);
            System.out.println("Request ID: " + clientResult.getRequestId());
            System.out.println("Success: " + clientResult.isSuccess());
            if (clientResult.isSuccess()) {
                System.out.println("Client config: " + clientResult.getClientConfig());
            } else {
                System.out.println("Error: " + clientResult.getErrorMessage());
            }
            
            // Create a test file to upload
            String testContent = "This is a test file for OSS upload.";
            String testFilePath = "/tmp/test_oss_upload.txt";
            FileSystem fs = session.getFileSystem();
            fs.writeFile(testFilePath, testContent, "overwrite");
            
            // upload
            System.out.println("\nTesting upload...");
            String bucket = System.getenv("OSS_TEST_BUCKET");
            OSSUploadResult uploadResult = oss.upload(bucket, "test-object.txt", testFilePath);
            System.out.println("Upload result: " + uploadResult);
            System.out.println("Request ID: " + uploadResult.getRequestId());
            System.out.println("Success: " + uploadResult.isSuccess());
            if (uploadResult.isSuccess()) {
                System.out.println("Content: " + uploadResult.getContent());
            } else {
                System.out.println("Error: " + uploadResult.getErrorMessage());
            }
            
            // upload_anonymous
            System.out.println("\nTesting upload_anonymous...");
            String uploadUrl = System.getenv("OSS_TEST_UPLOAD_URL");
            OSSUploadResult uploadAnonResult = oss.uploadAnonymous(uploadUrl, testFilePath);
            System.out.println("Upload anonymous result: " + uploadAnonResult);
            System.out.println("Request ID: " + uploadAnonResult.getRequestId());
            System.out.println("Success: " + uploadAnonResult.isSuccess());
            if (uploadAnonResult.isSuccess()) {
                System.out.println("Content: " + uploadAnonResult.getContent());
            } else {
                System.out.println("Error: " + uploadAnonResult.getErrorMessage());
            }
            
            // download test
            System.out.println("\nTesting download...");
            OSSDownloadResult downloadResult = oss.download(
                bucket,
                "test-object.txt",
                "/tmp/test_oss_download.txt"
            );
            System.out.println("Download result: " + downloadResult);
            System.out.println("Request ID: " + downloadResult.getRequestId());
            System.out.println("Success: " + downloadResult.isSuccess());
            if (downloadResult.isSuccess()) {
                System.out.println("Content: " + downloadResult.getContent());
            } else {
                System.out.println("Error: " + downloadResult.getErrorMessage());
            }
            
        } catch (OSSException e) {
            System.err.println("Failed to test OSS integration: " + e.getMessage());
        } catch (AgentBayException e) {
            System.err.println("AgentBay error: " + e.getMessage());
        } catch (Exception e) {
            System.err.println("Unexpected error: " + e.getMessage());
        } finally {
            // Delete the session
            if (session != null) {
                try {
                    System.out.println("\nDeleting the session...");
                    DeleteResult deleteResult = session.delete();
                    System.out.println("Session deleted successfully. Request ID: " + deleteResult.getRequestId());
                } catch (Exception deleteError) {
                    System.err.println("Error deleting session: " + deleteError.getMessage());
                }
            }
        }
    }
}