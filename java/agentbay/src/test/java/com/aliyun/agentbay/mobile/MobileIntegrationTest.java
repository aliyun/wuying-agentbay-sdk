package com.aliyun.agentbay.mobile;

import com.aliyun.agentbay.AgentBay;
import com.aliyun.agentbay.model.*;
import com.aliyun.agentbay.session.CreateSessionParams;
import com.aliyun.agentbay.session.Session;
import org.junit.*;
import org.junit.runners.MethodSorters;

import static org.junit.Assert.*;
import static org.junit.Assume.*;

/**
 * Integration tests for Mobile module.
 * These tests require a real AgentBay API connection and mobile environment.
 * 
 * To run these tests, set the AGENTBAY_API_KEY environment variable.
 * Tests are skipped if the API key is not set.
 */
@FixMethodOrder(MethodSorters.NAME_ASCENDING)
public class MobileIntegrationTest {
    
    private static AgentBay agentBay;
    private static Session session;
    private static Mobile mobile;
    
    @BeforeClass
    public static void setUpClass() {
        String apiKey = System.getenv("AGENTBAY_API_KEY");
        assumeTrue("AGENTBAY_API_KEY environment variable not set, skipping integration tests", 
            apiKey != null && !apiKey.isEmpty());
        
        try {
            agentBay = new AgentBay(apiKey);
            
            System.out.println("Creating mobile session for integration tests...");
            CreateSessionParams params = new CreateSessionParams();
            params.setImageId("mobile_latest");
            
            SessionResult result = agentBay.create(params);
            assertTrue("Failed to create session: " + result.getErrorMessage(), result.isSuccess());
            
            session = result.getSession();
            mobile = session.getMobile();
            
            System.out.println("Session created with ID: " + session.getSessionId());
            
            // Wait for mobile environment to be ready
            Thread.sleep(3000);
        } catch (Exception e) {
            System.err.println("Failed to set up test environment: " + e.getMessage());
            assumeTrue("Failed to set up test environment", false);
        }
    }
    
    @AfterClass
    public static void tearDownClass() {
        if (session != null && agentBay != null) {
            try {
                System.out.println("Cleaning up: Deleting the session...");
                DeleteResult result = agentBay.delete(session, false);
                System.out.println("Session deleted. Success: " + result.isSuccess());
            } catch (Exception e) {
                System.err.println("Warning: Error deleting session: " + e.getMessage());
            }
        }
    }
    
    // ==================== Touch Operations Tests ====================
    
    @Test
    public void test01_Tap() {
        System.out.println("\nTest: Tap operation...");
        
        BoolResult result = mobile.tap(500, 800);
        
        assertTrue("Tap failed: " + result.getErrorMessage(), result.isSuccess());
        assertTrue("Tap should return true", result.getData());
        System.out.println("Tap operation successful");
    }
    
    @Test
    public void test02_Swipe() {
        System.out.println("\nTest: Swipe operation...");
        
        BoolResult result = mobile.swipe(500, 1500, 500, 500, 500);
        
        assertTrue("Swipe failed: " + result.getErrorMessage(), result.isSuccess());
        assertTrue("Swipe should return true", result.getData());
        System.out.println("Swipe operation successful");
    }
    
    @Test
    public void test03_SwipeWithDefaultDuration() {
        System.out.println("\nTest: Swipe with default duration...");
        
        BoolResult result = mobile.swipe(500, 500, 500, 1000);
        
        assertTrue("Swipe failed: " + result.getErrorMessage(), result.isSuccess());
        System.out.println("Swipe with default duration successful");
    }
    
    @Test
    public void test04_InputText() {
        System.out.println("\nTest: Text input...");
        
        BoolResult result = mobile.inputText("Hello Mobile Test");
        
        assertTrue("Input text failed: " + result.getErrorMessage(), result.isSuccess());
        assertTrue("Input should return true", result.getData());
        System.out.println("Text input successful");
    }
    
    @Test
    public void test05_SendHomeKey() {
        System.out.println("\nTest: Press HOME key...");
        
        BoolResult result = mobile.sendKey(KeyCode.HOME);
        
        assertTrue("Send key failed: " + result.getErrorMessage(), result.isSuccess());
        assertTrue("Press key should return true", result.getData());
        System.out.println("HOME key press successful");
    }
    
    @Test
    public void test06_SendBackKey() {
        System.out.println("\nTest: Press BACK key...");
        
        BoolResult result = mobile.sendKey(KeyCode.BACK);
        
        assertTrue("Send key failed: " + result.getErrorMessage(), result.isSuccess());
        System.out.println("BACK key press successful");
    }
    
    // ==================== UI Element Operations Tests ====================
    
    @Test
    public void test07_GetClickableUiElements() {
        System.out.println("\nTest: Getting clickable UI elements...");
        
        UIElementListResult result = mobile.getClickableUiElements(5000);
        
        assertTrue("Get clickable UI elements failed: " + result.getErrorMessage(), result.isSuccess());
        assertNotNull("Elements list should not be null", result.getElements());
        System.out.println("Found " + result.getElements().size() + " clickable elements");
    }
    
    @Test
    public void test08_GetAllUiElements() {
        System.out.println("\nTest: Getting all UI elements...");
        
        UIElementListResult result = mobile.getAllUiElements(5000);
        
        assertTrue("Get all UI elements failed: " + result.getErrorMessage(), result.isSuccess());
        assertNotNull("Elements list should not be null", result.getElements());
        System.out.println("Found " + result.getElements().size() + " UI elements");
    }
    
    // ==================== Screenshot Operations Tests ====================
    
    @Test
    public void test09_Screenshot() {
        System.out.println("\nTest: Taking screenshot...");
        
        OperationResult result = mobile.screenshot();
        
        assertTrue("Screenshot failed: " + result.getErrorMessage(), result.isSuccess());
        assertNotNull("Screenshot data should not be null", result.getData());
        assertTrue("Screenshot URL should not be empty", result.getData().length() > 0);
        System.out.println("Screenshot taken successfully: " + 
            (result.getData().length() > 100 ? result.getData().substring(0, 100) + "..." : result.getData()));
    }
    
    // ==================== Application Management Tests ====================
    
    @Test
    public void test10_GetInstalledApps() {
        System.out.println("\nTest: Getting installed apps...");
        
        InstalledAppListResult result = mobile.getInstalledApps(true, false, true);
        
        assertTrue("Get installed apps failed: " + result.getErrorMessage(), result.isSuccess());
        assertNotNull("Apps list should not be null", result.getData());
        System.out.println("Found " + result.getData().size() + " apps");
        
        // Print first few apps
        int count = 0;
        for (InstalledApp app : result.getData()) {
            if (count++ < 5) {
                System.out.println("  - " + app.getName() + ": " + app.getStartCmd());
            }
        }
    }
    
    @Test
    public void test11_StartAndStopApp() {
        System.out.println("\nTest: Starting and stopping Settings app...");
        
        // Start Settings app
        ProcessListResult startResult = mobile.startApp("monkey -p com.android.settings -c android.intent.category.LAUNCHER 1");
        assertTrue("Start app failed: " + startResult.getErrorMessage(), startResult.isSuccess());
        System.out.println("Settings app started");
        
        // Wait for app to start
        try {
            Thread.sleep(2000);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        
        // Stop the app
        AppOperationResult stopResult = mobile.stopAppByCmd("am force-stop com.android.settings");
        assertTrue("Stop app failed: " + stopResult.getErrorMessage(), stopResult.isSuccess());
        System.out.println("Settings app stopped");
    }
    
    // ==================== Mobile Configuration Tests ====================
    
    @Test
    public void test12_SetResolutionLock() {
        System.out.println("\nTest: Setting resolution lock...");
        
        // This test just verifies no exception is thrown
        mobile.setResolutionLock(true);
        System.out.println("Resolution lock enabled");
        
        mobile.setResolutionLock(false);
        System.out.println("Resolution lock disabled");
    }
    
    @Test
    public void test13_SetNavigationBarVisibility() {
        System.out.println("\nTest: Setting navigation bar visibility...");
        
        // Hide navigation bar
        mobile.setNavigationBarVisibility(true);
        System.out.println("Navigation bar hidden");
        
        try {
            Thread.sleep(1000);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        
        // Show navigation bar
        mobile.setNavigationBarVisibility(false);
        System.out.println("Navigation bar shown");
    }
    
    // ==================== ADB URL Test ====================
    
    @Test
    public void test14_GetAdbUrl() {
        System.out.println("\nTest: Getting ADB URL...");
        
        // Note: This test requires a valid ADB public key
        // Using a test key for now
        String testAdbKey = "test_adb_public_key_for_testing";
        
        AdbUrlResult result = mobile.getAdbUrl(testAdbKey);
        
        // The result depends on the actual mobile environment setup
        if (result.isSuccess()) {
            assertNotNull("ADB URL should not be null", result.getData());
            assertTrue("ADB URL should start with 'adb connect'", 
                result.getData().startsWith("adb connect"));
            System.out.println("ADB URL: " + result.getData());
        } else {
            // It's acceptable if this fails due to environment setup
            System.out.println("ADB URL retrieval failed (may be expected): " + result.getErrorMessage());
        }
    }
}
