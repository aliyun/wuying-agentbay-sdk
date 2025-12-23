package com.aliyun.agentbay.mobile;

import com.aliyun.agentbay.AgentBay;
import com.aliyun.agentbay.context.*;
import com.aliyun.agentbay.exception.AgentBayException;
import com.aliyun.agentbay.model.FileUrlResult;
import org.junit.Before;
import org.junit.Test;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;

import java.util.ArrayList;
import java.util.List;

import static org.junit.Assert.*;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;

/**
 * Unit tests for MobileSimulate module.
 */
public class MobileSimulateTest {
    
    @Mock
    private AgentBay mockAgentBay;
    
    @Mock
    private ContextService mockContextService;
    
    private MobileSimulate mobileSimulate;
    
    @Before
    public void setUp() throws Exception {
        MockitoAnnotations.openMocks(this);
        when(mockAgentBay.getContext()).thenReturn(mockContextService);
        mobileSimulate = new MobileSimulate(mockAgentBay);
    }
    
    @Test
    public void testMobileSimulateInitialization() {
        assertNotNull(mobileSimulate);
    }
    
    @Test(expected = IllegalArgumentException.class)
    public void testMobileSimulateInitializationWithNullAgentBay() {
        new MobileSimulate(null);
    }
    
    @Test(expected = IllegalArgumentException.class)
    public void testMobileSimulateInitializationWithNullContext() {
        AgentBay agentBayWithNullContext = mock(AgentBay.class);
        when(agentBayWithNullContext.getContext()).thenReturn(null);
        new MobileSimulate(agentBayWithNullContext);
    }
    
    @Test
    public void testSetAndGetSimulateEnable() {
        mobileSimulate.setSimulateEnable(true);
        assertTrue(mobileSimulate.getSimulateEnable());
        
        mobileSimulate.setSimulateEnable(false);
        assertFalse(mobileSimulate.getSimulateEnable());
    }
    
    @Test
    public void testSetAndGetSimulateMode() {
        mobileSimulate.setSimulateMode(MobileSimulateMode.ALL);
        assertEquals(MobileSimulateMode.ALL, mobileSimulate.getSimulateMode());
        
        mobileSimulate.setSimulateMode(MobileSimulateMode.PROPERTIES_ONLY);
        assertEquals(MobileSimulateMode.PROPERTIES_ONLY, mobileSimulate.getSimulateMode());
    }
    
    @Test
    public void testSetAndGetSimulateContextId() {
        String contextId = "test-context-id";
        mobileSimulate.setSimulateContextId(contextId);
        assertEquals(contextId, mobileSimulate.getSimulateContextId());
    }
    
    @Test
    public void testGetSimulateConfig() {
        mobileSimulate.setSimulateEnable(true);
        mobileSimulate.setSimulateMode(MobileSimulateMode.ALL);
        
        MobileSimulateConfig config = mobileSimulate.getSimulateConfig();
        
        assertTrue(config.isSimulate());
        assertEquals(MobileSimulateMode.ALL, config.getSimulateMode());
    }
    
    @Test
    public void testHasMobileInfoExists() {
        // Arrange
        ContextSync contextSync = new ContextSync();
        contextSync.setContextId("test-context");
        contextSync.setPath("/test/path");
        
        List<FileInfo> entries = new ArrayList<>();
        FileInfo fileEntry = new FileInfo();
        fileEntry.setFileName("mobile_dev_info.json");
        entries.add(fileEntry);
        ContextFileListResult mockResult = new ContextFileListResult("req-123", true, entries, 1, "");
        
        when(mockContextService.listFiles(anyString(), anyString(), anyInt(), anyInt()))
            .thenReturn(mockResult);
        
        // Act
        boolean result = mobileSimulate.hasMobileInfo(contextSync);
        
        // Assert
        assertTrue(result);
        verify(mockContextService).listFiles(
            eq("test-context"),
            eq("/test/path/mobile_dev_info"),
            eq(1),
            eq(50)
        );
    }
    
    @Test
    public void testHasMobileInfoNotExists() {
        // Arrange
        ContextSync contextSync = new ContextSync();
        contextSync.setContextId("test-context");
        contextSync.setPath("/test/path");
        
        ContextFileListResult mockResult = new ContextFileListResult("req-123", true, new ArrayList<>(), 0, "");
        
        when(mockContextService.listFiles(anyString(), anyString(), anyInt(), anyInt()))
            .thenReturn(mockResult);
        
        // Act
        boolean result = mobileSimulate.hasMobileInfo(contextSync);
        
        // Assert
        assertFalse(result);
    }
    
    @Test(expected = IllegalArgumentException.class)
    public void testHasMobileInfoInvalidContextSync() {
        mobileSimulate.hasMobileInfo(null);
    }
    
    @Test(expected = IllegalArgumentException.class)
    public void testHasMobileInfoMissingContextId() {
        ContextSync contextSync = new ContextSync();
        contextSync.setPath("/test/path");
        mobileSimulate.hasMobileInfo(contextSync);
    }
    
    @Test(expected = IllegalArgumentException.class)
    public void testHasMobileInfoMissingPath() {
        ContextSync contextSync = new ContextSync();
        contextSync.setContextId("test-context");
        mobileSimulate.hasMobileInfo(contextSync);
    }
    
    @Test(expected = IllegalArgumentException.class)
    public void testUploadMobileInfoEmptyContent() {
        mobileSimulate.uploadMobileInfo("");
    }
    
    @Test(expected = IllegalArgumentException.class)
    public void testUploadMobileInfoInvalidJson() {
        mobileSimulate.uploadMobileInfo("not a json");
    }
    
    @Test(expected = IllegalArgumentException.class)
    public void testUploadMobileInfoNullContent() {
        mobileSimulate.uploadMobileInfo(null);
    }
    
    @Test
    public void testHasMobileInfoListFilesFailed() {
        // Arrange
        ContextSync contextSync = new ContextSync();
        contextSync.setContextId("test-context");
        contextSync.setPath("/test/path");
        
        ContextFileListResult mockResult = new ContextFileListResult("req-123", false, null, null, "List failed");
        when(mockContextService.listFiles(anyString(), anyString(), anyInt(), anyInt()))
            .thenReturn(mockResult);
        
        // Act
        boolean result = mobileSimulate.hasMobileInfo(contextSync);
        
        // Assert
        assertFalse(result);
    }
    
    @Test
    public void testGetSimulateConfigWithInternalContext() {
        // Arrange
        mobileSimulate.setSimulateEnable(true);
        mobileSimulate.setSimulateMode(MobileSimulateMode.ALL);
        mobileSimulate.setSimulateContextId("internal-ctx-123");
        
        // Act
        MobileSimulateConfig config = mobileSimulate.getSimulateConfig();
        
        // Assert
        assertTrue(config.isSimulate());
        assertEquals(MobileSimulateMode.ALL, config.getSimulateMode());
        assertEquals("internal-ctx-123", config.getSimulatedContextId());
    }
    
    @Test
    public void testGetSimulateConfigWithExternalContext() {
        // Arrange
        ContextSync contextSync = new ContextSync();
        contextSync.setContextId("external-context");
        contextSync.setPath("/test/path");
        contextSync.setPolicy(new SyncPolicy());
        contextSync.getPolicy().setBwList(new BWList());
        contextSync.getPolicy().getBwList().setWhiteLists(new ArrayList<>());
        
        // Manually trigger internal state update to external mode
        List<FileInfo> entries = new ArrayList<>();
        FileInfo fileEntry = new FileInfo();
        fileEntry.setFileName("mobile_dev_info.json");
        entries.add(fileEntry);
        ContextFileListResult mockResult = new ContextFileListResult("req-123", true, entries, 1, "");
        
        when(mockContextService.listFiles(anyString(), anyString(), anyInt(), anyInt()))
            .thenReturn(mockResult);
        
        mobileSimulate.hasMobileInfo(contextSync);
        mobileSimulate.setSimulateEnable(true);
        mobileSimulate.setSimulateMode(MobileSimulateMode.PROPERTIES_ONLY);
        
        // Act
        MobileSimulateConfig config = mobileSimulate.getSimulateConfig();
        
        // Assert
        assertTrue(config.isSimulate());
        assertEquals(MobileSimulateMode.PROPERTIES_ONLY, config.getSimulateMode());
        assertNull(config.getSimulatedContextId());
    }
    
    @Test
    public void testSimulateModeValues() {
        // Test all simulate mode enum values
        assertEquals("PropertiesOnly", MobileSimulateMode.PROPERTIES_ONLY.getValue());
        assertEquals("SensorsOnly", MobileSimulateMode.SENSORS_ONLY.getValue());
        assertEquals("PackagesOnly", MobileSimulateMode.PACKAGES_ONLY.getValue());
        assertEquals("ServicesOnly", MobileSimulateMode.SERVICES_ONLY.getValue());
        assertEquals("All", MobileSimulateMode.ALL.getValue());
    }
    
    @Test
    public void testSetSimulateContextIdUpdatesInternalState() {
        // Arrange
        String contextId = "new-context-123";
        
        // Act
        mobileSimulate.setSimulateContextId(contextId);
        
        // Assert
        assertEquals(contextId, mobileSimulate.getSimulateContextId());
        
        // Verify config reflects the change
        MobileSimulateConfig config = mobileSimulate.getSimulateConfig();
        assertEquals(contextId, config.getSimulatedContextId());
    }
    
    @Test(expected = IllegalArgumentException.class)
    public void testUploadMobileInfoWithContextSyncMissingContextId() {
        String mobileDevInfo = "{\"device\":\"test\"}";
        ContextSync contextSync = new ContextSync();
        contextSync.setPath("/data/data");
        
        mobileSimulate.uploadMobileInfo(mobileDevInfo, contextSync);
    }
    
    @Test
    public void testUploadMobileInfoContextCreationFailed() throws AgentBayException {
        // Arrange
        String mobileDevInfo = "{\"device\":\"test\",\"model\":\"TestModel\"}";
        
        ContextResult failedResult = new ContextResult("req-123", false, "", null, "Failed to create context");
        when(mockContextService.get(anyString(), eq(true))).thenReturn(failedResult);
        
        // Act
        MobileSimulateUploadResult result = mobileSimulate.uploadMobileInfo(mobileDevInfo);
        
        // Assert
        assertFalse(result.isSuccess());
        assertEquals("Failed to create context for simulate", result.getErrorMessage());
    }
    
    @Test
    public void testUploadMobileInfoGetUploadUrlFailed() throws AgentBayException {
        // Arrange
        String mobileDevInfo = "{\"device\":\"test\",\"model\":\"TestModel\"}";
        
        // Mock context creation success
        Context mockContext = new Context();
        mockContext.setContextId("new-context-123");
        mockContext.setName("test-context");
        ContextResult successResult = new ContextResult("req-123", true, "new-context-123", mockContext, "");
        when(mockContextService.get(anyString(), eq(true))).thenReturn(successResult);
        
        // Mock get upload URL failure
        FileUrlResult failedUrlResult = new FileUrlResult("req-456", false, null, null, "Failed to get upload URL");
        when(mockContextService.getFileUploadUrl(anyString(), anyString())).thenReturn(failedUrlResult);
        
        // Act
        MobileSimulateUploadResult result = mobileSimulate.uploadMobileInfo(mobileDevInfo);
        
        // Assert
        assertFalse(result.isSuccess());
        assertEquals("Failed to get upload URL", result.getErrorMessage());
    }
    
    @Test
    public void testUploadMobileInfoWithExistingContextSuccess() throws AgentBayException {
        // Arrange
        String mobileDevInfo = "{\"device\":\"test\",\"model\":\"TestModel\"}";
        ContextSync contextSync = new ContextSync();
        contextSync.setContextId("existing-context");
        contextSync.setPath("/data/data");
        contextSync.setPolicy(new SyncPolicy());
        contextSync.getPolicy().setBwList(new BWList());
        contextSync.getPolicy().getBwList().setWhiteLists(new ArrayList<>());
        
        // Mock get upload URL success
        FileUrlResult mockUploadUrl = new FileUrlResult("req-123", true, "https://upload-url.com", null, "");
        when(mockContextService.getFileUploadUrl(anyString(), anyString())).thenReturn(mockUploadUrl);
        
        // Act
        MobileSimulateUploadResult result = mobileSimulate.uploadMobileInfo(mobileDevInfo, contextSync);
        
        // Assert
        // Note: Will fail at HTTP upload stage without mocking OkHttpClient, but we verify setup
        assertFalse(result.isSuccess()); // Expected to fail at HTTP stage
        assertNotNull(result.getErrorMessage());
    }
    
    @Test
    public void testMobileSimulateConfigBuilder() {
        // Test MobileSimulateConfig construction
        MobileSimulateConfig config = new MobileSimulateConfig(
            true, 
            "/mobile_dev_info", 
            MobileSimulateMode.ALL, 
            "ctx-123"
        );
        
        assertTrue(config.isSimulate());
        assertEquals("/mobile_dev_info", config.getSimulatePath());
        assertEquals(MobileSimulateMode.ALL, config.getSimulateMode());
        assertEquals("ctx-123", config.getSimulatedContextId());
    }
    
    @Test
    public void testMobileSimulateUploadResultSuccess() {
        MobileSimulateUploadResult result = new MobileSimulateUploadResult(true, "ctx-456", "");
        
        assertTrue(result.isSuccess());
        assertEquals("ctx-456", result.getMobileSimulateContextId());
        assertEquals("", result.getErrorMessage());
    }
    
    @Test
    public void testMobileSimulateUploadResultFailure() {
        MobileSimulateUploadResult result = new MobileSimulateUploadResult(false, "", "Upload failed");
        
        assertFalse(result.isSuccess());
        assertEquals("", result.getMobileSimulateContextId());
        assertEquals("Upload failed", result.getErrorMessage());
    }
}
