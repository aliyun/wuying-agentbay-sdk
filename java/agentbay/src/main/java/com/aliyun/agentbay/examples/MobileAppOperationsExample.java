package com.aliyun.agentbay.examples;

import com.aliyun.agentbay.AgentBay;
import com.aliyun.agentbay.model.CommandResult;
import com.aliyun.agentbay.model.SessionResult;
import com.aliyun.agentbay.session.CreateSessionParams;
import com.aliyun.agentbay.session.Session;

/**
 * Mobile App Operations Example
 * 
 * This example demonstrates:
 * 1. Launching mobile apps
 * 2. App interaction
 * 3. App state management
 */
public class MobileAppOperationsExample {
    
    public static void main(String[] args) {
        System.out.println("=== Mobile App Operations Example ===\n");
        
        Session session = null;
        
        try {
            // Initialize AgentBay client
            AgentBay client = new AgentBay(System.getenv("AGENTBAY_API_KEY"));
            
            // Create a mobile session
            System.out.println("Creating mobile session...");
            CreateSessionParams params = new CreateSessionParams();
            params.setImageId("mobile_latest");
            
            SessionResult sessionResult = client.create(params);
            session = sessionResult.getSession();
            System.out.println("Session created: " + session.getSessionId());
            
            // Get ADB connection info
            System.out.println("\n1. Getting ADB connection info...");
            System.out.println("ADB connection available through mobile module");
            System.out.println("Note: Use session.getMobile().getAdbUrl(adbkey_pub) to get connection URL");
            
            // List installed packages
            System.out.println("\n2. Listing installed packages...");
            CommandResult result = session.getCommand().execute("pm list packages | head -10");
            System.out.println("Installed packages (first 10):\n" + result.getOutput());
            
            // Get device info
            System.out.println("\n3. Getting device information...");
            result = session.getCommand().execute("getprop ro.product.model");
            System.out.println("Device model: " + result.getOutput());
            
            result = session.getCommand().execute("getprop ro.build.version.release");
            System.out.println("Android version: " + result.getOutput());
            
            // Check screen status
            System.out.println("\n4. Checking screen status...");
            result = session.getCommand().execute("dumpsys power | grep 'Display Power'");
            System.out.println("Screen status:\n" + result.getOutput());
            
            System.out.println("\n=== Example completed successfully ===");
            
        } catch (Exception e) {
            System.err.println("\nError occurred: " + e.getMessage());
            e.printStackTrace();
        } finally {
            if (session != null) {
                try {
                    System.out.println("\nCleaning up session...");
                    session.delete();
                    System.out.println("Session closed");
                } catch (Exception e) {
                    System.err.println("Error closing session: " + e.getMessage());
                }
            }
        }
    }
}
