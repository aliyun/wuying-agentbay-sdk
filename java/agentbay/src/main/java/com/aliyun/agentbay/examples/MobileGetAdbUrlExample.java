package com.aliyun.agentbay.examples;

import com.aliyun.agentbay.AgentBay;
import com.aliyun.agentbay.model.AdbUrlResult;
import com.aliyun.agentbay.model.DeleteResult;
import com.aliyun.agentbay.model.SessionResult;
import com.aliyun.agentbay.session.CreateSessionParams;
import com.aliyun.agentbay.session.Session;

/**
 * Example: Get ADB Connection URL for Mobile Device
 * 
 * This example demonstrates how to use session.mobile.getAdbUrl() to retrieve
 * an ADB connection URL for connecting to a mobile device. This API is only
 * available in mobile environments using the mobile_latest image.
 * 
 * The getAdbUrl method requires an ADB public key for authentication and
 * returns the ADB connection URL that can be used with the `adb connect` command.
 */
public class MobileGetAdbUrlExample {
    
    public static void main(String[] args) {
        try {
            // Get API key from environment variable
            String apiKey = System.getenv("AGENTBAY_API_KEY");
            if (apiKey == null || apiKey.isEmpty()) {
                throw new IllegalStateException("AGENTBAY_API_KEY environment variable is not set");
            }
            
            // Initialize AgentBay client
            AgentBay agentBay = new AgentBay(apiKey);
            
            // Create a mobile session
            // NOTE: This will only work with mobile_latest image
            System.out.println("Creating a mobile session...");
            CreateSessionParams params = new CreateSessionParams();
            params.setImageId("mobile_latest");
            
            SessionResult createResult = agentBay.create(params);
            
            if (!createResult.isSuccess()) {
                System.out.println("Failed to create session: " + createResult.getErrorMessage());
                return;
            }
            
            Session session = createResult.getSession();
            System.out.println("✅ Session created: " + session.getSessionId());
            System.out.println("   Request ID: " + createResult.getRequestId());
            
            try {
                // Example ADB public key
                // In a real scenario, this would come from your ADB setup
                // Replace this with your actual ADB public key
                String adbkeyPub = "QAAAAM0muSn7yQCY...your_adb_public_key...EAAQAA=";
                
                // Get ADB URL for the mobile device
                System.out.println("\nRetrieving ADB connection URL...");
                AdbUrlResult adbResult = session.getMobile().getAdbUrl(adbkeyPub);
                
                if (adbResult.isSuccess()) {
                    System.out.println("✅ ADB URL retrieved successfully");
                    System.out.println("   URL: " + adbResult.getData());
                    System.out.println("   Request ID: " + adbResult.getRequestId());
                    
                    // You can now use this URL to connect via ADB
                    System.out.println("\nYou can use this command to connect:");
                    System.out.println("   " + adbResult.getData());
                } else {
                    System.out.println("❌ Failed to retrieve ADB URL: " + adbResult.getErrorMessage());
                }
                
            } finally {
                // Clean up: delete the session
                System.out.println("\nCleaning up...");
                DeleteResult deleteResult = session.delete();
                if (deleteResult.isSuccess()) {
                    System.out.println("✅ Session deleted successfully");
                    System.out.println("   Request ID: " + deleteResult.getRequestId());
                } else {
                    System.out.println("❌ Failed to delete session: " + deleteResult.getErrorMessage());
                }
            }
            
        } catch (Exception e) {
            System.err.println("Error occurred: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
