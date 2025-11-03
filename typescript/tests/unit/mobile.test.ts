/**
 * Unit tests for Mobile module.
 * Following TDD principles - tests first, then implementation.
 */

import { Mobile } from '../../src/mobile/mobile';

// Mock Session interface
interface MockSession {
  callMcpTool: jest.Mock;
  getAPIKey: () => string;
  sessionId: string;
}

describe('Mobile', () => {
  let mockSession: MockSession;
  let mobile: Mobile;

  beforeEach(() => {
    mockSession = {
      callMcpTool: jest.fn(),
      getAPIKey: () => 'test-api-key',
      sessionId: 'test-session-id'
    };
    mobile = new Mobile(mockSession as any);
  });

  describe('Touch Operations', () => {
    test('tap should call MCP tool with correct parameters', async () => {
      // Arrange
      const mockResult = {
        success: true,
        requestId: 'test-123',
        errorMessage: ''
      };
      mockSession.callMcpTool.mockResolvedValue(mockResult);

      // Act
      const result = await mobile.tap(100, 200);

      // Assert
      expect(mockSession.callMcpTool).toHaveBeenCalledWith('tap', {
        x: 100,
        y: 200
      });
      expect(result.success).toBe(true);
      expect(result.requestId).toBe('test-123');
    });

    test('swipe should call MCP tool with correct parameters', async () => {
      // Arrange
      const mockResult = {
        success: true,
        requestId: 'test-123'
      };
      mockSession.callMcpTool.mockResolvedValue(mockResult);

      // Act
      const result = await mobile.swipe(100, 100, 200, 200, 500);

      // Assert
      expect(mockSession.callMcpTool).toHaveBeenCalledWith('swipe', {
        start_x: 100,
        start_y: 100,
        end_x: 200,
        end_y: 200,
        duration_ms: 500
      });
      expect(result.success).toBe(true);
    });

    test('swipe should use default duration when not provided', async () => {
      // Arrange
      const mockResult = {
        success: true,
        requestId: 'test-123'
      };
      mockSession.callMcpTool.mockResolvedValue(mockResult);

      // Act
      const result = await mobile.swipe(100, 100, 200, 200);

      // Assert
      expect(mockSession.callMcpTool).toHaveBeenCalledWith('swipe', {
        start_x: 100,
        start_y: 100,
        end_x: 200,
        end_y: 200,
        duration_ms: 300
      });
    });
  });

  describe('Input Operations', () => {
    test('inputText should call MCP tool with correct parameters', async () => {
      // Arrange
      const mockResult = {
        success: true,
        requestId: 'test-123'
      };
      mockSession.callMcpTool.mockResolvedValue(mockResult);

      // Act
      const result = await mobile.inputText('Hello Mobile');

      // Assert
      expect(mockSession.callMcpTool).toHaveBeenCalledWith('input_text', {
        text: 'Hello Mobile'
      });
      expect(result.success).toBe(true);
    });

    test('sendKey should call MCP tool with correct parameters', async () => {
      // Arrange
      const mockResult = {
        success: true,
        requestId: 'test-123'
      };
      mockSession.callMcpTool.mockResolvedValue(mockResult);

      // Act
      const result = await mobile.sendKey(4); // BACK key

      // Assert
      expect(mockSession.callMcpTool).toHaveBeenCalledWith('send_key', {
        key: 4
      });
      expect(result.success).toBe(true);
    });
  });

  describe('UI Element Operations', () => {
    test('getClickableUIElements should call MCP tool and return elements', async () => {
      // Arrange
      const mockResult = {
        success: true,
        requestId: 'test-123',
        data: JSON.stringify([
          {
            text: 'Button 1',
            className: 'android.widget.Button',
            bounds: { left: 0, top: 0, right: 100, bottom: 50 }
          }
        ])
      };
      mockSession.callMcpTool.mockResolvedValue(mockResult);

      // Act
      const result = await mobile.getClickableUIElements(5000);

      // Assert
      expect(mockSession.callMcpTool).toHaveBeenCalledWith('get_clickable_ui_elements', {
        timeout_ms: 5000
      });
      expect(result.elements).toHaveLength(1);
      expect(result.elements[0].text).toBe('Button 1');
    });

    test('getAllUIElements should call MCP tool and return all elements', async () => {
      // Arrange
      const mockResult = {
        success: true,
        requestId: 'test-123',
        data: JSON.stringify([
          {
            text: 'Text View',
            className: 'android.widget.TextView',
            bounds: { left: 0, top: 0, right: 200, bottom: 30 }
          }
        ])
      };
      mockSession.callMcpTool.mockResolvedValue(mockResult);

      // Act
      const result = await mobile.getAllUIElements(3000);

      // Assert
      expect(mockSession.callMcpTool).toHaveBeenCalledWith('get_all_ui_elements', {
        timeout_ms: 3000
      });
      expect(result.elements).toHaveLength(1);
      expect(result.elements[0].className).toBe('android.widget.TextView');
    });
  });

  describe('App Management Operations', () => {
    test('getInstalledApps should call MCP tool and return apps', async () => {
      // Arrange
      const mockResult = {
        success: true,
        requestId: 'test-123',
        data: JSON.stringify([
          {
            name: 'Calculator',
            startCmd: 'com.android.calculator2',
            workDirectory: ''
          }
        ])
      };
      mockSession.callMcpTool.mockResolvedValue(mockResult);

      // Act
      const result = await mobile.getInstalledApps(false, true, true);

      // Assert
      expect(mockSession.callMcpTool).toHaveBeenCalledWith('get_installed_apps', {
        start_menu: false,
        desktop: true,
        ignore_system_apps: true
      });
      expect(result.apps).toHaveLength(1);
      expect(result.apps[0].name).toBe('Calculator');
    });

    test('startApp should call MCP tool with correct parameters', async () => {
      // Arrange
      const mockResult = {
        success: true,
        requestId: 'test-123',
        data: JSON.stringify([
          {
            pid: 1234,
            pname: 'com.android.calculator2'
          }
        ])
      };
      mockSession.callMcpTool.mockResolvedValue(mockResult);

      // Act
      const result = await mobile.startApp('com.android.calculator2', '', '');

      // Assert
      expect(mockSession.callMcpTool).toHaveBeenCalledWith('start_app', {
        start_cmd: 'com.android.calculator2',
        work_directory: '',
        activity: ''
      });
      expect(result.processes).toHaveLength(1);
      expect(result.processes[0].pid).toBe(1234);
    });

    test('stopAppByCmd should call MCP tool with correct parameters', async () => {
      // Arrange
      const mockResult = {
        success: true,
        requestId: 'test-123'
      };
      mockSession.callMcpTool.mockResolvedValue(mockResult);

      // Act
      const result = await mobile.stopAppByCmd('am force-stop com.android.calculator2');

      // Assert
      expect(mockSession.callMcpTool).toHaveBeenCalledWith('stop_app_by_cmd', {
        stop_cmd: 'am force-stop com.android.calculator2'
      });
      expect(result.success).toBe(true);
    });
  });

  describe('Screen Operations', () => {
    test('screenshot should call MCP tool and return URL', async () => {
      // Arrange
      const mockResult = {
        success: true,
        requestId: 'test-123',
        data: 'https://example.com/mobile-screenshot.png'
      };
      mockSession.callMcpTool.mockResolvedValue(mockResult);

      // Act
      const result = await mobile.screenshot();

      // Assert
      expect(mockSession.callMcpTool).toHaveBeenCalledWith('system_screenshot', {});
      expect(result.data).toBe('https://example.com/mobile-screenshot.png');
    });
  });

  describe('Error Handling', () => {
    test('should handle MCP tool errors gracefully', async () => {
      // Arrange
      const mockError = new Error('MCP tool failed');
      mockSession.callMcpTool.mockRejectedValue(mockError);

      // Act
      const result = await mobile.tap(100, 200);

      // Assert
      expect(result.success).toBe(false);
      expect(result.errorMessage).toContain('MCP tool failed');
    });

    test('should handle invalid JSON response for UI elements', async () => {
      // Arrange
      const mockResult = {
        success: true,
        requestId: 'test-123',
        data: 'invalid json'
      };
      mockSession.callMcpTool.mockResolvedValue(mockResult);

      // Act
      const result = await mobile.getClickableUIElements(5000);

      // Assert
      expect(result.success).toBe(false);
      expect(result.errorMessage).toContain('Failed to parse');
    });
  });

  describe('ADB Connection', () => {
    test.skip('getAdbUrl should fail on non-mobile environment', async () => {
      // Note: This test is skipped because getAdbUrl no longer validates image ID
      // on the client side. It directly calls the getLink API which handles
      // environment validation server-side.
      //
      // Full getAdbUrl functionality is covered by integration tests.
    });

    test('getAdbUrl should succeed on mobile environment', async () => {
      // Arrange
      const expectedUrl = 'adb connect xx.xx.xx.xx:xxxxx';
      const mockSessionWithImage = {
        ...mockSession,
        imageId: 'mobile_latest',
        getLink: jest.fn().mockResolvedValue({
          success: true,
          requestId: 'test-adb-123',
          data: expectedUrl,
          errorMessage: ''
        })
      };
      const mobileWithImage = new Mobile(mockSessionWithImage as any);
      const adbkeyPub = 'QAAAAM0muSn7yQCY...test_key...EAAQAA=';

      // Act
      const result = await mobileWithImage.getAdbUrl(adbkeyPub);

      // Assert
      const callArgs = mockSessionWithImage.getLink.mock.calls[0];
      expect(callArgs[0]).toBe('adb');
      expect(callArgs[1]).toBeUndefined();
      expect(callArgs[2]).toContain('adbkey_pub');
      expect(result.success).toBe(true);
      expect(result.data).toBe(expectedUrl);
      expect(result.url).toBe(expectedUrl);
      expect(result.requestId).toBe('test-adb-123');
    });

    test('getAdbUrl should handle getLink errors', async () => {
      // Arrange
      const mockSessionWithImage = {
        ...mockSession,
        imageId: 'mobile_latest',
        getLink: jest.fn().mockRejectedValue(new Error('Network error'))
      };
      const mobileWithImage = new Mobile(mockSessionWithImage as any);
      const adbkeyPub = 'test_key_456';

      // Act
      const result = await mobileWithImage.getAdbUrl(adbkeyPub);

      // Assert
      expect(result.success).toBe(false);
      expect(result.errorMessage).toContain('Failed to get ADB URL');
      expect(result.errorMessage).toContain('Network error');
    });
  });
}); 