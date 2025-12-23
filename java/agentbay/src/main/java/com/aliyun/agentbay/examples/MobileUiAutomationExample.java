package com.aliyun.agentbay.examples;

import com.aliyun.agentbay.AgentBay;
import com.aliyun.agentbay.model.CommandResult;
import com.aliyun.agentbay.model.SessionResult;
import com.aliyun.agentbay.session.CreateSessionParams;
import com.aliyun.agentbay.session.Session;

/**
 * Mobile UI Automation Example
 * 
 * This example demonstrates:
 * 1. UI element interaction
 * 2. Screen gestures
 * 3. UI testing automation
 */
public class MobileUiAutomationExample {
    
    public static void main(String[] args) {
        System.out.println("=== Mobile UI Automation Example ===\n");
        
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
            
            // Get screen size
            System.out.println("\n1. Getting screen size...");
            CommandResult result = session.getCommand().execute("wm size");
            System.out.println("Screen size: " + result.getOutput());
            
            // Get screen density
            System.out.println("\n2. Getting screen density...");
            result = session.getCommand().execute("wm density");
            System.out.println("Screen density: " + result.getOutput());
            
            // Simulate tap (demonstration)
            System.out.println("\n3. Simulating screen tap...");
            System.out.println("Note: Actual tap would use: session.getMobile().tap(x, y)");
            result = session.getCommand().execute("input tap 500 500");
            System.out.println("Tap simulated at (500, 500)");
            
            // Simulate swipe (demonstration)
            System.out.println("\n4. Simulating swipe gesture...");
            System.out.println("Note: Actual swipe would use: session.getMobile().swipe(x1, y1, x2, y2)");
            result = session.getCommand().execute("input swipe 500 1000 500 500 300");
            System.out.println("Swipe simulated (upward)");
            
            // Get current activity
            System.out.println("\n5. Getting current activity...");
            result = session.getCommand().execute("dumpsys window | grep mCurrentFocus");
            System.out.println("Current activity:\n" + result.getOutput());
            
            // Take screenshot (demonstration)
            System.out.println("\n6. Taking screenshot...");
            result = session.getCommand().execute("screencap -p /sdcard/screenshot.png");
            System.out.println("Screenshot saved to /sdcard/screenshot.png");
            
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
