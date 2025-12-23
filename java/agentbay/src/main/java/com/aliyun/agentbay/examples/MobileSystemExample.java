package com.aliyun.agentbay.examples;

import com.aliyun.agentbay.AgentBay;
import com.aliyun.agentbay.model.*;
import com.aliyun.agentbay.model.Process;
import com.aliyun.agentbay.session.CreateSessionParams;
import com.aliyun.agentbay.session.Session;
import com.aliyun.agentbay.mobile.KeyCode;

import java.util.List;
import java.util.Map;

/**
 * Mobile System Example
 * 
 * This comprehensive example demonstrates the full range of mobile use capabilities:
 * 1. Getting installed applications
 * 2. Starting and stopping applications
 * 3. Getting UI elements (clickable and all)
 * 4. Sending key events
 * 5. Input text
 * 6. Screen gestures (swipe, tap)
 * 7. Taking screenshots
 * 8. Advanced app management
 */
public class MobileSystemExample {
    
    public static void main(String[] args) {
        System.out.println("=== Mobile System Example ===\n");
        
        // Get API key from environment variable
        String apiKey = System.getenv("AGENTBAY_API_KEY");
        if (apiKey == null || apiKey.isEmpty()) {
            apiKey = "akm-xxx"; // Replace with your actual API key
        }
        
        Session session = null;
        
        try {
            // Initialize AgentBay client
            AgentBay agentBay = new AgentBay(apiKey);
            
            // Create a mobile session
            System.out.println("Creating a new mobile session...");
            CreateSessionParams params = new CreateSessionParams();
            params.setImageId("mobile_latest");
            
            SessionResult sessionResult = agentBay.create(params);
            session = sessionResult.getSession();
            System.out.println("Session created with ID: " + session.getSessionId());
            System.out.println("Request ID: " + sessionResult.getRequestId());
            
            // 1. Get installed applications
            System.out.println("\n1. Getting installed applications...");
            InstalledAppListResult appsResult = session.getMobile().getInstalledApps(
                true,   // startMenu
                false,  // desktop
                true    // ignoreSystemApps
            );
            
            if (appsResult.isSuccess()) {
                System.out.println("Installed Applications:");
                List<InstalledApp> apps = appsResult.getData();
                if (apps != null) {
                    for (InstalledApp app : apps) {
                        System.out.println("  - " + app.getName());
                        System.out.println("    Start: " + app.getStartCmd());
                        if (app.getWorkDirectory() != null && !app.getWorkDirectory().isEmpty()) {
                            System.out.println("    Work Dir: " + app.getWorkDirectory());
                        }
                    }
                }
                System.out.println("Request ID: " + appsResult.getRequestId());
            } else {
                System.out.println("Error getting applications: " + appsResult.getErrorMessage());
            }
            
            // 2. Start an application
            System.out.println("\n2. Starting an application...");
            // Note: Using system Settings app which is always available
            // Replace with an actual installed app package name for real scenarios
            ProcessListResult startResult = session.getMobile().startApp(
                "monkey -p com.android.settings -c android.intent.category.LAUNCHER 1"
            );
            System.out.println("Started Application successfully: " + startResult.isSuccess());
            if (!startResult.isSuccess()) {
                System.out.println("Error: " + startResult.getErrorMessage());
                System.out.println("Tip: Check installed apps in step 1 and use a valid package name");
            }
            System.out.println("Request ID: " + startResult.getRequestId());
            
            // 3. Stop an application
            System.out.println("\n3. Stopping an application...");
            // Note: Stop the Settings app we just started
            AppOperationResult stopResult = session.getMobile().stopAppByCmd(
                "am force-stop com.android.settings"
            );
            System.out.println("Application stopped: " + stopResult.isSuccess());
            if (!stopResult.isSuccess()) {
                System.out.println("Error: " + stopResult.getErrorMessage());
            }
            System.out.println("Request ID: " + stopResult.getRequestId());
            
            // 4. Get clickable UI elements
            System.out.println("\n4. Getting clickable UI elements...");
            UIElementListResult elementsResult = session.getMobile().getClickableUiElements();
            if (elementsResult.isSuccess()) {
                System.out.println("Clickable UI Elements count: " + elementsResult.getElements().size());
                System.out.println("Request ID: " + elementsResult.getRequestId());
            } else {
                System.out.println("Error getting clickable elements: " + elementsResult.getErrorMessage());
            }
            
            // 5. Get all UI elements
            System.out.println("\n5. Getting all UI elements...");
            UIElementListResult allElementsResult = session.getMobile().getAllUiElements(3000);
            if (allElementsResult.isSuccess()) {
                System.out.println("\nUI Element Tree:");
                List<Map<String, Object>> elements = allElementsResult.getElements();
                // Print a preview of the elements (truncate if too long)
                if (elements != null && !elements.isEmpty()) {
                    System.out.println("Total UI elements: " + elements.size());
                    // Print first few elements as sample
                    int count = Math.min(3, elements.size());
                    for (int i = 0; i < count; i++) {
                        Map<String, Object> elem = elements.get(i);
                        System.out.println("  Element " + (i + 1) + ": " + 
                            elem.getOrDefault("className", "N/A") + 
                            " (text: " + elem.getOrDefault("text", "") + ")");
                    }
                    if (elements.size() > 3) {
                        System.out.println("  ... and " + (elements.size() - 3) + " more elements");
                    }
                }
                System.out.println("Request ID: " + allElementsResult.getRequestId());
            } else {
                System.out.println("Error getting all UI elements: " + allElementsResult.getErrorMessage());
            }
            
            // 6. Send key event
            System.out.println("\n6. Sending key event...");
            BoolResult keyResult = session.getMobile().sendKey(KeyCode.HOME);
            System.out.println("Key event sent successfully: " + keyResult.isSuccess());
            System.out.println("Request ID: " + keyResult.getRequestId());
            
            // 7. Input text
            System.out.println("\n7. Input text...");
            BoolResult inputResult = session.getMobile().inputText("Hello, AgentBay!");
            System.out.println("Text input successfully: " + inputResult.isSuccess());
            System.out.println("Request ID: " + inputResult.getRequestId());
            
            // 8. Swipe screen
            System.out.println("\n8. Swiping screen...");
            BoolResult swipeResult = session.getMobile().swipe(
                100,  // startX
                800,  // startY
                900,  // endX
                200,  // endY
                500   // durationMs
            );
            System.out.println("Screen swiped successfully: " + swipeResult.isSuccess());
            System.out.println("Request ID: " + swipeResult.getRequestId());
            
            // 9. Tap event (mobile touch)
            System.out.println("\n9. Tapping screen...");
            BoolResult tapResult = session.getMobile().tap(
                500,  // x
                800   // y
            );
            System.out.println("Screen tapped successfully: " + tapResult.isSuccess());
            System.out.println("Request ID: " + tapResult.getRequestId());
            
            // 10. Screenshot
            System.out.println("\n10. Taking screenshot...");
            OperationResult screenshotResult = session.getMobile().screenshot();
            System.out.println("Screenshot taken successfully: " + screenshotResult.isSuccess());
            if (screenshotResult.isSuccess() && screenshotResult.getData() != null) {
                System.out.println("Screenshot data length: " + screenshotResult.getData().length() + " chars");
            }
            System.out.println("Request ID: " + screenshotResult.getRequestId());
            
            // 11. Start application with specific activity
            System.out.println("\n11. Starting application with specific activity...");
            // Note: Using Calculator app with specific activity as example
            // Replace with actual app package and activity for real scenarios
            String appPackage = "com.android.calculator2";
            String appActivity = "com.android.calculator2.Calculator";
            String startCmd = String.format("monkey -p %s -c android.intent.category.LAUNCHER 1", appPackage);
            
            ProcessListResult startWithActivityResult = session.getMobile().startApp(startCmd, null, appActivity);
            System.out.println("Start app with activity success: " + startWithActivityResult.isSuccess());
            if (startWithActivityResult.isSuccess() && startWithActivityResult.getData() != null) {
                System.out.println("Started processes:");
                for (Process process : startWithActivityResult.getData()) {
                    System.out.println("  - " + process.getPname() + " (PID: " + process.getPid() + ")");
                }
            } else if (!startWithActivityResult.isSuccess()) {
                System.out.println("Error: " + startWithActivityResult.getErrorMessage());
                System.out.println("Note: This example uses Calculator app, which may not be available on all devices");
            }
            System.out.println("Request ID: " + startWithActivityResult.getRequestId());
            
            System.out.println("\n=== Example completed successfully ===");
            
        } catch (Exception e) {
            System.err.println("\nFailed to test mobile system API: " + e.getMessage());
            e.printStackTrace();
        } finally {
            if (session != null) {
                try {
                    System.out.println("\nDeleting session...");
                    DeleteResult deleteResult = session.delete();
                    System.out.println("Session deleted successfully: " + deleteResult.isSuccess());
                    System.out.println("Request ID: " + deleteResult.getRequestId());
                } catch (Exception e) {
                    System.err.println("Error deleting session: " + e.getMessage());
                }
            }
        }
    }
}
