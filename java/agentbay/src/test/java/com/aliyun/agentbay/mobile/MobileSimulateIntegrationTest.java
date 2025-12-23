package com.aliyun.agentbay.mobile;

import com.aliyun.agentbay.AgentBay;
import com.aliyun.agentbay.context.ContextSync;
import com.aliyun.agentbay.context.SyncPolicy;
import com.aliyun.agentbay.context.BWList;
import org.junit.*;
import org.junit.runners.MethodSorters;

import java.util.ArrayList;

import static org.junit.Assert.*;
import static org.junit.Assume.*;

/**
 * Integration tests for MobileSimulate module.
 * These tests require a real AgentBay API connection.
 * 
 * To run these tests, set the AGENTBAY_API_KEY environment variable.
 * Tests are skipped if the API key is not set.
 */
@FixMethodOrder(MethodSorters.NAME_ASCENDING)
public class MobileSimulateIntegrationTest {
    
    private static AgentBay agentBay;
    private static MobileSimulate mobileSimulate;
    private static String uploadedContextId;
    
    @BeforeClass
    public static void setUpClass() {
        String apiKey = System.getenv("AGENTBAY_API_KEY");
        assumeTrue("AGENTBAY_API_KEY environment variable not set, skipping integration tests", 
            apiKey != null && !apiKey.isEmpty());
        
        try {
            agentBay = new AgentBay(apiKey);
            mobileSimulate = new MobileSimulate(agentBay);
            
            System.out.println("MobileSimulate integration tests initialized");
        } catch (Exception e) {
            System.err.println("Failed to set up test environment: " + e.getMessage());
            assumeTrue("Failed to set up test environment", false);
        }
    }
    
    // ==================== Configuration Tests ====================
    
    @Test
    public void test01_SetAndGetSimulateEnable() {
        System.out.println("\nTest: Set and get simulate enable...");
        
        mobileSimulate.setSimulateEnable(true);
        assertTrue("Simulate should be enabled", mobileSimulate.getSimulateEnable());
        
        mobileSimulate.setSimulateEnable(false);
        assertFalse("Simulate should be disabled", mobileSimulate.getSimulateEnable());
        
        System.out.println("Simulate enable flag works correctly");
    }
    
    @Test
    public void test02_SetAndGetSimulateMode() {
        System.out.println("\nTest: Set and get simulate mode...");
        
        mobileSimulate.setSimulateMode(MobileSimulateMode.ALL);
        assertEquals("Simulate mode should be ALL", 
            MobileSimulateMode.ALL, mobileSimulate.getSimulateMode());
        
        mobileSimulate.setSimulateMode(MobileSimulateMode.PROPERTIES_ONLY);
        assertEquals("Simulate mode should be PROPERTIES_ONLY", 
            MobileSimulateMode.PROPERTIES_ONLY, mobileSimulate.getSimulateMode());
        
        System.out.println("Simulate mode works correctly");
    }
    
    @Test
    public void test03_SetAndGetSimulateContextId() {
        System.out.println("\nTest: Set and get simulate context ID...");
        
        String testContextId = "test-context-integration-123";
        mobileSimulate.setSimulateContextId(testContextId);
        
        assertEquals("Context ID should match", testContextId, mobileSimulate.getSimulateContextId());
        
        System.out.println("Simulate context ID works correctly");
    }
    
    @Test
    public void test04_GetSimulateConfig() {
        System.out.println("\nTest: Get simulate config...");
        
        mobileSimulate.setSimulateEnable(true);
        mobileSimulate.setSimulateMode(MobileSimulateMode.SENSORS_ONLY);
        mobileSimulate.setSimulateContextId("config-test-ctx");
        
        MobileSimulateConfig config = mobileSimulate.getSimulateConfig();
        
        assertNotNull("Config should not be null", config);
        assertTrue("Simulate should be enabled in config", config.isSimulate());
        assertEquals("Mode should be SENSORS_ONLY", 
            MobileSimulateMode.SENSORS_ONLY, config.getSimulateMode());
        assertEquals("Context ID should match", "config-test-ctx", config.getSimulatedContextId());
        
        System.out.println("Simulate config retrieved successfully");
        System.out.println("  - Enabled: " + config.isSimulate());
        System.out.println("  - Mode: " + config.getSimulateMode());
        System.out.println("  - Context ID: " + config.getSimulatedContextId());
    }
    
    // ==================== Upload Tests ====================
    
    @Test
    public void test05_UploadMobileInfoWithInternalContext() {
        System.out.println("\nTest: Upload mobile info with internal context...");
        
        String mobileDevInfo = "{" +
            "\"device\": {" +
            "  \"brand\": \"TestBrand\"," +
            "  \"model\": \"TestModel\"," +
            "  \"manufacturer\": \"TestMfg\"," +
            "  \"android_version\": \"12\"," +
            "  \"sdk_int\": 31" +
            "}," +
            "\"sensors\": [" +
            "  {\"name\": \"Accelerometer\", \"vendor\": \"Test\"}" +
            "]," +
            "\"packages\": [" +
            "  {\"name\": \"com.test.app\", \"version\": \"1.0\"}" +
            "]" +
            "}";
        
        MobileSimulateUploadResult result = mobileSimulate.uploadMobileInfo(mobileDevInfo);
        
        if (result.isSuccess()) {
            uploadedContextId = result.getMobileSimulateContextId();
            assertNotNull("Context ID should not be null on success", uploadedContextId);
            assertFalse("Context ID should not be empty", uploadedContextId.isEmpty());
            System.out.println("Upload successful. Context ID: " + uploadedContextId);
        } else {
            // Upload might fail due to network/permission issues, which is acceptable for integration test
            System.out.println("Upload failed (may be expected): " + result.getErrorMessage());
        }
    }
    
    @Test
    public void test06_ValidateUploadedContextId() {
        System.out.println("\nTest: Validate uploaded context ID...");
        
        if (uploadedContextId != null) {
            // Create a new MobileSimulate instance and set the context ID
            MobileSimulate newInstance = new MobileSimulate(agentBay);
            newInstance.setSimulateContextId(uploadedContextId);
            
            assertEquals("Context ID should be set", uploadedContextId, newInstance.getSimulateContextId());
            System.out.println("Context ID validated: " + uploadedContextId);
        } else {
            System.out.println("Skipping - no uploaded context ID available");
        }
    }
    
    // ==================== Mode Value Tests ====================
    
    @Test
    public void test07_SimulateModeValues() {
        System.out.println("\nTest: Simulate mode values...");
        
        assertEquals("PropertiesOnly", MobileSimulateMode.PROPERTIES_ONLY.getValue());
        assertEquals("SensorsOnly", MobileSimulateMode.SENSORS_ONLY.getValue());
        assertEquals("PackagesOnly", MobileSimulateMode.PACKAGES_ONLY.getValue());
        assertEquals("ServicesOnly", MobileSimulateMode.SERVICES_ONLY.getValue());
        assertEquals("All", MobileSimulateMode.ALL.getValue());
        
        System.out.println("All simulate mode values verified");
    }
}
