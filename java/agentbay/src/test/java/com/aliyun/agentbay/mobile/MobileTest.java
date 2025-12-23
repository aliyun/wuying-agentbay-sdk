package com.aliyun.agentbay.mobile;

import com.aliyun.agentbay.AgentBay;
import com.aliyun.agentbay.client.ApiClient;
import com.aliyun.agentbay.model.*;
import com.aliyun.agentbay.session.Session;
import com.aliyun.wuyingai20250506.models.*;
import org.junit.Before;
import org.junit.Test;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;

import java.util.*;

import static org.junit.Assert.*;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;

/**
 * Unit tests for Mobile module.
 * Following TDD principles - tests first, then implementation.
 */
public class MobileTest {
    
    @Mock
    private Session mockSession;
    
    @Mock
    private AgentBay mockAgentBay;
    
    @Mock
    private ApiClient mockApiClient;
    
    private Mobile mobile;
    
    @Before
    public void setUp() throws Exception {
        MockitoAnnotations.openMocks(this);
        mobile = new Mobile(mockSession);
        // Mock VPC disabled by default (use API mode)
        when(mockSession.isVpcEnabled()).thenReturn(false);
    }
    
    /**
     * Helper method to create a mock CallMcpToolResponse with the given data.
     * The structure matches what BaseService.parseResponseBody() expects:
     * response.body.data = Map with "content" (List of Maps with "text") and "isError" fields
     */
    private CallMcpToolResponse createMockResponse(boolean success, String data, String requestId) {
        CallMcpToolResponse response = mock(CallMcpToolResponse.class);
        CallMcpToolResponseBody body = mock(CallMcpToolResponseBody.class);
        
        // Setup mock chain
        when(response.getBody()).thenReturn(body);
        when(body.getRequestId()).thenReturn(requestId);
        
        // Setup content structure - this is what parseResponseBody expects
        Map<String, Object> contentItem = new HashMap<>();
        contentItem.put("text", data);
        
        Map<String, Object> dataMap = new HashMap<>();
        dataMap.put("content", java.util.Arrays.asList(contentItem));
        dataMap.put("isError", !success);
        
        // body.getData() returns this Map as Object
        when(body.getData()).thenReturn(dataMap);
        
        return response;
    }
    
    @Test
    public void testMobileInitialization() {
        assertNotNull(mobile);
    }
    
    // ==================== Touch Operations Tests ====================
    
    @Test
    public void testTapSuccess() throws Exception {
        // Arrange
        CallMcpToolResponse mockResponse = createMockResponse(true, "true", "test-123");
        when(mockSession.callTool(anyString(), any())).thenReturn(mockResponse);
        
        // Act
        BoolResult result = mobile.tap(100, 200);
        
        // Assert
        assertTrue(result.isSuccess());
        assertTrue(result.getData());
        verify(mockSession).callTool(eq("tap"), any());
    }
    
    @Test
    public void testSwipeSuccess() throws Exception {
        // Arrange
        CallMcpToolResponse mockResponse = createMockResponse(true, "true", "test-123");
        when(mockSession.callTool(anyString(), any())).thenReturn(mockResponse);
        
        // Act
        BoolResult result = mobile.swipe(100, 100, 200, 200, 300);
        
        // Assert
        assertTrue(result.isSuccess());
        assertTrue(result.getData());
        verify(mockSession).callTool(eq("swipe"), any());
    }
    
    @Test
    public void testInputTextSuccess() throws Exception {
        // Arrange
        CallMcpToolResponse mockResponse = createMockResponse(true, "true", "test-123");
        when(mockSession.callTool(anyString(), any())).thenReturn(mockResponse);
        
        // Act
        BoolResult result = mobile.inputText("Hello Mobile");
        
        // Assert
        assertTrue(result.isSuccess());
        assertTrue(result.getData());
        verify(mockSession).callTool(eq("input_text"), any());
    }
    
    @Test
    public void testSendKeySuccess() throws Exception {
        // Arrange
        CallMcpToolResponse mockResponse = createMockResponse(true, "true", "test-123");
        when(mockSession.callTool(anyString(), any())).thenReturn(mockResponse);
        
        // Act
        BoolResult result = mobile.sendKey(KeyCode.BACK);
        
        // Assert
        assertTrue(result.isSuccess());
        assertTrue(result.getData());
        verify(mockSession).callTool(eq("send_key"), any());
    }
    
    // ==================== UI Element Operations Tests ====================
    
    @Test
    public void testGetClickableUiElementsSuccess() throws Exception {
        // Arrange
        String jsonData = "[{\"id\":\"button1\",\"text\":\"Click me\"}]";
        CallMcpToolResponse mockResponse = createMockResponse(true, jsonData, "test-123");
        when(mockSession.callTool(anyString(), any())).thenReturn(mockResponse);
        
        // Act
        UIElementListResult result = mobile.getClickableUiElements();
        
        // Assert
        assertTrue(result.isSuccess());
        assertFalse(result.getElements().isEmpty());
        verify(mockSession).callTool(eq("get_clickable_ui_elements"), any());
    }
    
    @Test
    public void testGetAllUiElementsSuccess() throws Exception {
        // Arrange
        String jsonData = "[{\"bounds\":\"[0,0][100,100]\",\"className\":\"Button\",\"text\":\"OK\"}]";
        CallMcpToolResponse mockResponse = createMockResponse(true, jsonData, "test-123");
        when(mockSession.callTool(anyString(), any())).thenReturn(mockResponse);
        
        // Act
        UIElementListResult result = mobile.getAllUiElements();
        
        // Assert
        assertTrue(result.isSuccess());
        assertFalse(result.getElements().isEmpty());
        verify(mockSession).callTool(eq("get_all_ui_elements"), any());
    }
    
    // ==================== Application Management Tests ====================
    
    @Test
    public void testGetInstalledAppsSuccess() throws Exception {
        // Arrange
        String jsonData = "[{\"name\":\"Settings\",\"start_cmd\":\"com.android.settings\"}]";
        CallMcpToolResponse mockResponse = createMockResponse(true, jsonData, "test-123");
        when(mockSession.callTool(anyString(), any())).thenReturn(mockResponse);
        
        // Act
        InstalledAppListResult result = mobile.getInstalledApps(true, false, true);
        
        // Assert
        assertTrue(result.isSuccess());
        assertFalse(result.getData().isEmpty());
        verify(mockSession).callTool(eq("get_installed_apps"), any());
    }
    
    @Test
    public void testStartAppSuccess() throws Exception {
        // Arrange
        String jsonData = "[{\"pname\":\"settings\",\"pid\":12345,\"cmdline\":\"com.android.settings\"}]";
        CallMcpToolResponse mockResponse = createMockResponse(true, jsonData, "test-123");
        when(mockSession.callTool(anyString(), any())).thenReturn(mockResponse);
        
        // Act
        ProcessListResult result = mobile.startApp("com.android.settings");
        
        // Assert
        assertTrue(result.isSuccess());
        assertFalse(result.getData().isEmpty());
        verify(mockSession).callTool(eq("start_app"), any());
    }
    
    @Test
    public void testStopAppByCmdSuccess() throws Exception {
        // Arrange
        CallMcpToolResponse mockResponse = createMockResponse(true, "true", "test-123");
        when(mockSession.callTool(anyString(), any())).thenReturn(mockResponse);
        
        // Act
        AppOperationResult result = mobile.stopAppByCmd("com.android.settings");
        
        // Assert
        assertTrue(result.isSuccess());
        verify(mockSession).callTool(eq("stop_app_by_cmd"), any());
    }
    
    // ==================== Screenshot Tests ====================
    
    @Test
    public void testScreenshotSuccess() throws Exception {
        // Arrange
        CallMcpToolResponse mockResponse = createMockResponse(true, "/path/to/screenshot.png", "test-123");
        when(mockSession.callTool(anyString(), any())).thenReturn(mockResponse);
        
        // Act
        OperationResult result = mobile.screenshot();
        
        // Assert
        assertTrue(result.isSuccess());
        assertNotNull(result.getData());
        verify(mockSession).callTool(eq("system_screenshot"), any());
    }
    
    // ==================== ADB URL Tests ====================
    
    @Test
    public void testGetAdbUrlSuccess() throws Exception {
        // Arrange
        GetAdbLinkResponse mockResponse = new GetAdbLinkResponse();
        GetAdbLinkResponseBody mockBody = new GetAdbLinkResponseBody();
        mockBody.setSuccess(true);
        mockBody.setRequestId("adb-request-123");
        
        GetAdbLinkResponseBody.GetAdbLinkResponseBodyData mockData = 
            new GetAdbLinkResponseBody.GetAdbLinkResponseBodyData();
        mockData.setUrl("adb connect 47.99.76.99:54848");
        mockBody.setData(mockData);
        
        mockResponse.setBody(mockBody);
        
        when(mockSession.getAgentBay()).thenReturn(mockAgentBay);
        when(mockAgentBay.getApiClient()).thenReturn(mockApiClient);
        when(mockApiClient.getAdbLink(anyString(), anyString())).thenReturn(mockResponse);
        when(mockSession.getSessionId()).thenReturn("session-123");
        
        // Act
        String adbkeyPub = "test_adb_key...";
        AdbUrlResult result = mobile.getAdbUrl(adbkeyPub);
        
        // Assert
        assertTrue(result.isSuccess());
        assertEquals("adb-request-123", result.getRequestId());
        assertEquals("adb connect 47.99.76.99:54848", result.getData());
        verify(mockApiClient).getAdbLink(eq("session-123"), eq(adbkeyPub));
    }
    
    @Test
    public void testGetAdbUrlFailure() throws Exception {
        // Arrange
        GetAdbLinkResponse mockResponse = new GetAdbLinkResponse();
        GetAdbLinkResponseBody mockBody = new GetAdbLinkResponseBody();
        mockBody.setSuccess(false);
        mockBody.setRequestId("adb-request-error");
        mockBody.setMessage("ImageTypeNotMatched: Expected: MobileUse, Actual: BrowserUse");
        
        mockResponse.setBody(mockBody);
        
        when(mockSession.getAgentBay()).thenReturn(mockAgentBay);
        when(mockAgentBay.getApiClient()).thenReturn(mockApiClient);
        when(mockApiClient.getAdbLink(anyString(), anyString())).thenReturn(mockResponse);
        when(mockSession.getSessionId()).thenReturn("session-123");
        
        // Act
        String adbkeyPub = "test_adb_key...";
        AdbUrlResult result = mobile.getAdbUrl(adbkeyPub);
        
        // Assert
        assertFalse(result.isSuccess());
        assertTrue(result.getErrorMessage().contains("ImageTypeNotMatched") || 
                   result.getErrorMessage().contains("Expected: MobileUse"));
    }
    
    // ==================== Mobile Configuration Tests ====================
    
    @Test
    public void testConfigureWithMobileExtraConfig() {
        // Arrange
        MobileExtraConfig config = new MobileExtraConfig();
        config.setLockResolution(true);
        config.setHideNavigationBar(true);
        
        // Mock command
        com.aliyun.agentbay.command.Command mockCommand = mock(com.aliyun.agentbay.command.Command.class);
        CommandResult mockCmdResult = new CommandResult("", true, "", "", 0);
        when(mockCommand.executeCommand(anyString(), anyInt())).thenReturn(mockCmdResult);
        when(mockSession.getCommand()).thenReturn(mockCommand);
        
        // Act
        mobile.configure(config);
        
        // Assert
        verify(mockCommand, atLeastOnce()).executeCommand(anyString(), anyInt());
    }
    
    // ==================== Error Handling Tests ====================
    
    @Test
    public void testTapFailure() throws Exception {
        // Arrange
        CallMcpToolResponse mockResponse = createMockResponse(false, null, "test-123");
        CallMcpToolResponseBody body = mockResponse.getBody();
        when(body.getMessage()).thenReturn("MCP tool failed");
        when(mockSession.callTool(anyString(), any())).thenReturn(mockResponse);
        
        // Act
        BoolResult result = mobile.tap(100, 200);
        
        // Assert
        assertFalse(result.isSuccess());
        assertTrue(result.getErrorMessage().contains("MCP tool failed") || 
                   result.getErrorMessage().contains("failed"));
    }
    
    @Test
    public void testTapException() throws Exception {
        // Arrange
        when(mockSession.callTool(anyString(), any())).thenThrow(new RuntimeException("Network error"));
        
        // Act
        BoolResult result = mobile.tap(100, 200);
        
        // Assert
        assertFalse(result.isSuccess());
        assertTrue(result.getErrorMessage().contains("Failed to tap") || 
                   result.getErrorMessage().contains("Network error"));
    }
    
    @Test
    public void testSwipeFailure() throws Exception {
        // Arrange
        CallMcpToolResponse mockResponse = createMockResponse(false, null, "test-123");
        CallMcpToolResponseBody body = mockResponse.getBody();
        when(body.getMessage()).thenReturn("Swipe failed");
        when(mockSession.callTool(anyString(), any())).thenReturn(mockResponse);
        
        // Act
        BoolResult result = mobile.swipe(100, 100, 200, 200);
        
        // Assert
        assertFalse(result.isSuccess());
        assertTrue(result.getErrorMessage().contains("Swipe failed") || 
                   result.getErrorMessage().contains("failed"));
    }
    
    @Test
    public void testInputTextFailure() throws Exception {
        // Arrange
        CallMcpToolResponse mockResponse = createMockResponse(false, null, "test-123");
        CallMcpToolResponseBody body = mockResponse.getBody();
        when(body.getMessage()).thenReturn("Input failed");
        when(mockSession.callTool(anyString(), any())).thenReturn(mockResponse);
        
        // Act
        BoolResult result = mobile.inputText("test");
        
        // Assert
        assertFalse(result.isSuccess());
    }
    
    @Test
    public void testSendKeyFailure() throws Exception {
        // Arrange
        CallMcpToolResponse mockResponse = createMockResponse(false, null, "test-123");
        CallMcpToolResponseBody body = mockResponse.getBody();
        when(body.getMessage()).thenReturn("Key send failed");
        when(mockSession.callTool(anyString(), any())).thenReturn(mockResponse);
        
        // Act
        BoolResult result = mobile.sendKey(KeyCode.HOME);
        
        // Assert
        assertFalse(result.isSuccess());
    }
    
    @Test
    public void testGetClickableUiElementsFailure() throws Exception {
        // Arrange
        CallMcpToolResponse mockResponse = createMockResponse(false, null, "test-123");
        CallMcpToolResponseBody body = mockResponse.getBody();
        when(body.getMessage()).thenReturn("Get UI elements failed");
        when(mockSession.callTool(anyString(), any())).thenReturn(mockResponse);
        
        // Act
        UIElementListResult result = mobile.getClickableUiElements();
        
        // Assert
        assertFalse(result.isSuccess());
    }
    
    @Test
    public void testGetClickableUiElementsException() throws Exception {
        // Arrange
        when(mockSession.callTool(anyString(), any())).thenThrow(new RuntimeException("Network error"));
        
        // Act
        UIElementListResult result = mobile.getClickableUiElements();
        
        // Assert
        assertFalse(result.isSuccess());
        assertTrue(result.getErrorMessage().contains("Failed to get clickable UI elements") || 
                   result.getErrorMessage().contains("Network error"));
    }
    
    @Test
    public void testGetAllUiElementsWithChildren() throws Exception {
        // Arrange
        String jsonData = "[{\"bounds\":\"[0,0][100,100]\",\"className\":\"Layout\",\"text\":\"\",\"type\":\"view\",\"resourceId\":\"layout1\",\"index\":0,\"isParent\":true,\"children\":[{\"bounds\":\"[10,10][90,90]\",\"className\":\"Button\",\"text\":\"OK\",\"type\":\"button\",\"resourceId\":\"btn1\",\"index\":0,\"isParent\":false}]}]";
        CallMcpToolResponse mockResponse = createMockResponse(true, jsonData, "test-123");
        when(mockSession.callTool(anyString(), any())).thenReturn(mockResponse);
        
        // Act
        UIElementListResult result = mobile.getAllUiElements(5000);
        
        // Assert
        assertTrue(result.isSuccess());
        assertFalse(result.getElements().isEmpty());
        Map<String, Object> firstElement = result.getElements().get(0);
        assertNotNull(firstElement.get("children"));
    }
    
    @Test
    public void testGetAllUiElementsEmptyData() throws Exception {
        // Arrange
        CallMcpToolResponse mockResponse = createMockResponse(true, "", "test-123");
        when(mockSession.callTool(anyString(), any())).thenReturn(mockResponse);
        
        // Act
        UIElementListResult result = mobile.getAllUiElements();
        
        // Assert
        assertTrue(result.isSuccess());
        assertTrue(result.getElements().isEmpty());
    }
    
    @Test
    public void testScreenshotFailure() throws Exception {
        // Arrange
        CallMcpToolResponse mockResponse = createMockResponse(false, null, "test-123");
        CallMcpToolResponseBody body = mockResponse.getBody();
        when(body.getMessage()).thenReturn("Screenshot failed");
        when(mockSession.callTool(anyString(), any())).thenReturn(mockResponse);
        
        // Act
        OperationResult result = mobile.screenshot();
        
        // Assert
        assertFalse(result.isSuccess());
    }
    
    @Test
    public void testStartAppWithActivity() throws Exception {
        // Arrange
        String jsonData = "[{\"pname\":\"settings\",\"pid\":12345,\"cmdline\":\"com.android.settings/.MainActivity\"}]";
        CallMcpToolResponse mockResponse = createMockResponse(true, jsonData, "test-123");
        when(mockSession.callTool(anyString(), any())).thenReturn(mockResponse);
        
        // Act
        ProcessListResult result = mobile.startApp("com.android.settings", "", ".MainActivity");
        
        // Assert
        assertTrue(result.isSuccess());
        verify(mockSession).callTool(eq("start_app"), any());
    }
    
    @Test
    public void testStartAppWithWorkDirectory() throws Exception {
        // Arrange
        String jsonData = "[{\"pname\":\"app\",\"pid\":12345,\"cmdline\":\"test\"}]";
        CallMcpToolResponse mockResponse = createMockResponse(true, jsonData, "test-123");
        when(mockSession.callTool(anyString(), any())).thenReturn(mockResponse);
        
        // Act
        ProcessListResult result = mobile.startApp("test", "/data/local/tmp");
        
        // Assert
        assertTrue(result.isSuccess());
    }
    
    @Test
    public void testGetInstalledAppsDefaultParams() throws Exception {
        // Arrange
        String jsonData = "[{\"name\":\"App1\",\"start_cmd\":\"com.app1\"}]";
        CallMcpToolResponse mockResponse = createMockResponse(true, jsonData, "test-123");
        when(mockSession.callTool(anyString(), any())).thenReturn(mockResponse);
        
        // Act
        InstalledAppListResult result = mobile.getInstalledApps();
        
        // Assert
        assertTrue(result.isSuccess());
    }
    
    @Test
    public void testConfigureWithNullConfig() {
        // Act - should not throw exception
        mobile.configure(null);
        
        // Assert - no exception thrown means success
    }
    
    @Test
    public void testConfigureWithAppWhitelist() {
        // Arrange
        MobileExtraConfig config = new MobileExtraConfig();
        AppManagerRule appRule = new AppManagerRule();
        appRule.setRuleType("White");
        appRule.setAppPackageNameList(Arrays.asList("com.app1", "com.app2"));
        config.setAppManagerRule(appRule);
        
        com.aliyun.agentbay.command.Command mockCommand = mock(com.aliyun.agentbay.command.Command.class);
        CommandResult mockCmdResult = new CommandResult("", true, "", "", 0);
        when(mockCommand.executeCommand(anyString(), anyInt())).thenReturn(mockCmdResult);
        when(mockSession.getCommand()).thenReturn(mockCommand);
        
        // Act
        mobile.configure(config);
        
        // Assert
        verify(mockCommand, atLeastOnce()).executeCommand(anyString(), anyInt());
    }
    
    @Test
    public void testConfigureWithAppBlacklist() {
        // Arrange
        MobileExtraConfig config = new MobileExtraConfig();
        AppManagerRule appRule = new AppManagerRule();
        appRule.setRuleType("Black");
        appRule.setAppPackageNameList(Arrays.asList("com.blocked1", "com.blocked2"));
        config.setAppManagerRule(appRule);
        
        com.aliyun.agentbay.command.Command mockCommand = mock(com.aliyun.agentbay.command.Command.class);
        CommandResult mockCmdResult = new CommandResult("", true, "", "", 0);
        when(mockCommand.executeCommand(anyString(), anyInt())).thenReturn(mockCmdResult);
        when(mockSession.getCommand()).thenReturn(mockCommand);
        
        // Act
        mobile.configure(config);
        
        // Assert
        verify(mockCommand, atLeastOnce()).executeCommand(anyString(), anyInt());
    }
    
    @Test
    public void testConfigureWithUninstallBlacklist() {
        // Arrange
        MobileExtraConfig config = new MobileExtraConfig();
        config.setUninstallBlacklist(Arrays.asList("com.protected1", "com.protected2"));
        
        com.aliyun.agentbay.command.Command mockCommand = mock(com.aliyun.agentbay.command.Command.class);
        CommandResult mockCmdResult = new CommandResult("", true, "", "", 0);
        when(mockCommand.executeCommand(anyString(), anyInt())).thenReturn(mockCmdResult);
        when(mockSession.getCommand()).thenReturn(mockCommand);
        
        // Act
        mobile.configure(config);
        
        // Assert
        verify(mockCommand, atLeastOnce()).executeCommand(anyString(), anyInt());
    }
    
    @Test
    public void testSetAppWhitelistEmpty() {
        // Act - should not throw, just log warning
        mobile.setAppWhitelist(new ArrayList<>());
        
        // No exception means success
    }
    
    @Test
    public void testSetAppBlacklistEmpty() {
        // Act - should not throw, just log warning
        mobile.setAppBlacklist(new ArrayList<>());
        
        // No exception means success
    }
    
    @Test
    public void testSetUninstallBlacklistEmpty() {
        // Act - should not throw, just log warning
        mobile.setUninstallBlacklist(new ArrayList<>());
        
        // No exception means success
    }
    
    @Test
    public void testKeyCodeValues() {
        // Assert key code constants
        assertEquals(3, KeyCode.HOME);
        assertEquals(4, KeyCode.BACK);
        assertEquals(24, KeyCode.VOLUME_UP);
        assertEquals(25, KeyCode.VOLUME_DOWN);
        assertEquals(26, KeyCode.POWER);
        assertEquals(82, KeyCode.MENU);
    }
}
