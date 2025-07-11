import { AgentBay, Session } from "../../src";
import { Window, WindowManager } from "../../src/window/window";
import { log } from "../../src/utils/logger";
import * as sinon from "sinon";

// Helper function to check if window has valid properties
function isValidWindow(window: Window): boolean {
  return (
    typeof window === "object" &&
    window !== null &&
    typeof window.window_id === "number" &&
    typeof window.title === "string"
  );
}

// Mock data for tests
const mockWindows: Window[] = [
  {
    window_id: 1,
    title: "Test Window 1",
    absolute_upper_left_x: 100,
    absolute_upper_left_y: 100,
    width: 800,
    height: 600,
    pid: 1234,
    pname: "test_app",
  },
  {
    window_id: 2,
    title: "Test Window 2",
    absolute_upper_left_x: 200,
    absolute_upper_left_y: 200,
    width: 1024,
    height: 768,
    pid: 5678,
    pname: "another_app",
  },
];

const mockActiveWindow: Window = mockWindows[0];

describe("WindowManager", () => {
  let windowManager: WindowManager;
  let mockSession: any;
  let mockClient: any;
  let callMcpToolStub: sinon.SinonStub;

  beforeEach(() => {
    // Create mock client
    mockClient = {
      callMcpTool: sinon.stub(),
    };

    // Create mock session
    mockSession = {
      getAPIKey: sinon.stub().returns("mock-api-key"),
      getClient: sinon.stub().returns(mockClient),
      getSessionId: sinon.stub().returns("mock-session-id"),
    };

    // Get reference to the callMcpTool stub for easier access
    callMcpToolStub = mockClient.callMcpTool;

    // Create WindowManager with mock session
    windowManager = new WindowManager(mockSession);

    log("WindowManager created with mock session");
  });

  afterEach(() => {
    sinon.restore();
  });

  describe("listRootWindows()", () => {
    it("should return a list of root windows with requestId", async () => {
      log("Testing listRootWindows...");

      // Setup mock response
      const mockResponse = {
        statusCode: 200,
        body: {
          data: {
            isError: false,
            content: [{ text: JSON.stringify(mockWindows) }],
          },
          requestId: "mock-request-id-list",
        },
      };

      callMcpToolStub.resolves(mockResponse);

      // Call the method
      const windowsResponse = await windowManager.listRootWindows();
      log(`Retrieved ${windowsResponse.windows.length} root windows`);
      log(
        `List Root Windows RequestId: ${
          windowsResponse.requestId || "undefined"
        }`
      );

      // Verify WindowListResult structure
      expect(windowsResponse.success).toBe(true);
      expect(windowsResponse.requestId).toBeDefined();
      expect(typeof windowsResponse.requestId).toBe("string");
      expect(windowsResponse.requestId).toBe("mock-request-id-list");
      expect(windowsResponse.errorMessage).toBeUndefined();

      // Verify windows array
      expect(windowsResponse.windows).toBeDefined();
      expect(Array.isArray(windowsResponse.windows)).toBe(true);
      expect(windowsResponse.windows.length).toBe(2);

      // Verify the results
      windowsResponse.windows.forEach((window) => {
        expect(isValidWindow(window)).toBe(true);
      });

      // Verify the API was called with correct parameters
      expect(callMcpToolStub.calledOnce).toBe(true);
      const callArgs = callMcpToolStub.getCall(0).args[0];
      expect(callArgs.name).toBe("list_root_windows");
      expect(callArgs.sessionId).toBe("mock-session-id");
      expect(callArgs.authorization).toBe("Bearer mock-api-key");
    });

    it("should handle list root windows failure", async () => {
      const mockResponse = {
        statusCode: 500,
        body: {
          data: {
            isError: true,
            content: [{ text: "Failed to list root windows" }],
          },
        },
      };

      callMcpToolStub.resolves(mockResponse);

      const result = await windowManager.listRootWindows();

      // Verify error result structure
      expect(result.success).toBe(false);
      expect(result.requestId).toBe("");
      expect(result.windows).toEqual([]);
      expect(result.errorMessage).toContain("Failed to list root windows");
    });
  });

  describe("getActiveWindow()", () => {
    it("should return the active window with requestId", async () => {
      log("Testing getActiveWindow...");

      // Setup mock response
      const mockResponse = {
        statusCode: 200,
        body: {
          data: {
            isError: false,
            content: [{ text: JSON.stringify(mockActiveWindow) }],
          },
          requestId: "mock-request-id-active",
        },
      };

      callMcpToolStub.resolves(mockResponse);

      const windowResponse = await windowManager.getActiveWindow();
      log(
        `Get Active Window RequestId: ${
          windowResponse.requestId || "undefined"
        }`
      );

      // Verify WindowInfoResult structure
      expect(windowResponse.success).toBe(true);
      expect(windowResponse.requestId).toBeDefined();
      expect(typeof windowResponse.requestId).toBe("string");
      expect(windowResponse.requestId).toBe("mock-request-id-active");
      expect(windowResponse.errorMessage).toBeUndefined();

      if (windowResponse.window) {
        log(
          `Active window: ${windowResponse.window.title} (ID: ${windowResponse.window.window_id})`
        );

        // Verify the results
        expect(isValidWindow(windowResponse.window)).toBe(true);
        expect(windowResponse.window.window_id).toBe(
          mockActiveWindow.window_id
        );
        expect(windowResponse.window.title).toBe(mockActiveWindow.title);
      }

      // Verify the API was called with correct parameters
      expect(callMcpToolStub.calledOnce).toBe(true);
      const callArgs = callMcpToolStub.getCall(0).args[0];
      expect(callArgs.name).toBe("get_active_window");
    });

    it("should handle get active window failure", async () => {
      const mockResponse = {
        statusCode: 500,
        body: {
          data: {
            isError: true,
            content: [{ text: "Failed to get active window" }],
          },
        },
      };

      callMcpToolStub.resolves(mockResponse);

      const result = await windowManager.getActiveWindow();

      // Verify error result structure
      expect(result.success).toBe(false);
      expect(result.requestId).toBe("");
      expect(result.window).toBeUndefined();
      expect(result.errorMessage).toContain("Failed to get active window");
    });
  });

  describe("activateWindow()", () => {
    it("should activate a window with requestId", async () => {
      log("Testing activateWindow...");

      const windowId = mockWindows[0].window_id;
      log(`Activating window with ID: ${windowId}`);

      // Setup mock response
      const mockResponse = {
        statusCode: 200,
        body: {
          data: {
            isError: false,
            content: [],
          },
          requestId: "mock-request-id-activate",
        },
      };

      callMcpToolStub.resolves(mockResponse);

      // Call the method
      const activateResponse = await windowManager.activateWindow(windowId);
      log("Window activated successfully");
      log(
        `Activate Window RequestId: ${
          activateResponse.requestId || "undefined"
        }`
      );

      // Verify BoolResult structure
      expect(activateResponse.success).toBe(true);
      expect(activateResponse.requestId).toBeDefined();
      expect(typeof activateResponse.requestId).toBe("string");
      expect(activateResponse.requestId).toBe("mock-request-id-activate");
      expect(activateResponse.data).toBe(true);
      expect(activateResponse.errorMessage).toBeUndefined();

      // Verify the API was called with correct parameters
      expect(callMcpToolStub.calledOnce).toBe(true);
      const callArgs = callMcpToolStub.getCall(0).args[0];
      expect(callArgs.name).toBe("activate_window");
      expect(JSON.parse(callArgs.args)).toEqual({ window_id: windowId });
    });

    it("should handle activate window failure", async () => {
      const mockResponse = {
        statusCode: 500,
        body: {
          data: {
            isError: true,
            content: [{ text: "Failed to activate window" }],
          },
        },
      };

      callMcpToolStub.resolves(mockResponse);

      const result = await windowManager.activateWindow(1);

      // Verify error result structure
      expect(result.success).toBe(false);
      expect(result.requestId).toBe("");
      expect(result.errorMessage).toContain("Failed to activate window");
    });
  });

  describe("maximizeWindow()", () => {
    it("should maximize a window with requestId", async () => {
      log("Testing maximizeWindow...");

      const windowId = mockWindows[0].window_id;
      log(`Maximizing window with ID: ${windowId}`);

      // Setup mock response
      const mockResponse = {
        statusCode: 200,
        body: {
          data: {
            isError: false,
            content: [],
          },
          requestId: "mock-request-id-maximize",
        },
      };

      callMcpToolStub.resolves(mockResponse);

      // Call the method
      const maximizeResponse = await windowManager.maximizeWindow(windowId);
      log("Window maximized successfully");
      log(
        `Maximize Window RequestId: ${
          maximizeResponse.requestId || "undefined"
        }`
      );

      // Verify BoolResult structure
      expect(maximizeResponse.success).toBe(true);
      expect(maximizeResponse.requestId).toBeDefined();
      expect(typeof maximizeResponse.requestId).toBe("string");
      expect(maximizeResponse.requestId).toBe("mock-request-id-maximize");
      expect(maximizeResponse.data).toBe(true);
      expect(maximizeResponse.errorMessage).toBeUndefined();

      // Verify the API was called with correct parameters
      expect(callMcpToolStub.calledOnce).toBe(true);
      const callArgs = callMcpToolStub.getCall(0).args[0];
      expect(callArgs.name).toBe("maximize_window");
      expect(JSON.parse(callArgs.args)).toEqual({ window_id: windowId });
    });
  });

  describe("minimizeWindow()", () => {
    it("should minimize a window with requestId", async () => {
      log("Testing minimizeWindow...");

      const windowId = mockWindows[0].window_id;
      log(`Minimizing window with ID: ${windowId}`);

      // Setup mock response
      const mockResponse = {
        statusCode: 200,
        body: {
          data: {
            isError: false,
            content: [],
          },
          requestId: "mock-request-id-minimize",
        },
      };

      callMcpToolStub.resolves(mockResponse);

      // Call the method
      const minimizeResponse = await windowManager.minimizeWindow(windowId);
      log("Window minimized successfully");
      log(
        `Minimize Window RequestId: ${
          minimizeResponse.requestId || "undefined"
        }`
      );

      // Verify BoolResult structure
      expect(minimizeResponse.success).toBe(true);
      expect(minimizeResponse.requestId).toBeDefined();
      expect(typeof minimizeResponse.requestId).toBe("string");
      expect(minimizeResponse.requestId).toBe("mock-request-id-minimize");
      expect(minimizeResponse.data).toBe(true);
      expect(minimizeResponse.errorMessage).toBeUndefined();

      // Verify the API was called with correct parameters
      expect(callMcpToolStub.calledOnce).toBe(true);
      const callArgs = callMcpToolStub.getCall(0).args[0];
      expect(callArgs.name).toBe("minimize_window");
      expect(JSON.parse(callArgs.args)).toEqual({ window_id: windowId });
    });
  });

  describe("restoreWindow()", () => {
    it("should restore a window with requestId", async () => {
      log("Testing restoreWindow...");

      const windowId = mockWindows[0].window_id;
      log(`Restoring window with ID: ${windowId}`);

      // Setup mock response
      const mockResponse = {
        statusCode: 200,
        body: {
          data: {
            isError: false,
            content: [],
          },
          requestId: "mock-request-id-restore",
        },
      };

      callMcpToolStub.resolves(mockResponse);

      // Call the method
      const restoreResponse = await windowManager.restoreWindow(windowId);
      log("Window restored successfully");
      log(
        `Restore Window RequestId: ${restoreResponse.requestId || "undefined"}`
      );

      // Verify BoolResult structure
      expect(restoreResponse.success).toBe(true);
      expect(restoreResponse.requestId).toBeDefined();
      expect(typeof restoreResponse.requestId).toBe("string");
      expect(restoreResponse.requestId).toBe("mock-request-id-restore");
      expect(restoreResponse.data).toBe(true);
      expect(restoreResponse.errorMessage).toBeUndefined();

      // Verify the API was called with correct parameters
      expect(callMcpToolStub.calledOnce).toBe(true);
      const callArgs = callMcpToolStub.getCall(0).args[0];
      expect(callArgs.name).toBe("restore_window");
      expect(JSON.parse(callArgs.args)).toEqual({ window_id: windowId });
    });
  });

  describe("resizeWindow()", () => {
    it("should resize a window with requestId", async () => {
      log("Testing resizeWindow...");

      const windowId = mockWindows[0].window_id;
      const width = 800;
      const height = 600;
      log(`Resizing window with ID: ${windowId} to ${width}x${height}`);

      // Setup mock response
      const mockResponse = {
        statusCode: 200,
        body: {
          data: {
            isError: false,
            content: [],
          },
          requestId: "mock-request-id-resize",
        },
      };

      callMcpToolStub.resolves(mockResponse);

      // Call the method
      const resizeResponse = await windowManager.resizeWindow(
        windowId,
        width,
        height
      );
      log(`Window resized successfully to ${width}x${height}`);
      log(
        `Resize Window RequestId: ${resizeResponse.requestId || "undefined"}`
      );

      // Verify BoolResult structure
      expect(resizeResponse.success).toBe(true);
      expect(resizeResponse.requestId).toBeDefined();
      expect(typeof resizeResponse.requestId).toBe("string");
      expect(resizeResponse.requestId).toBe("mock-request-id-resize");
      expect(resizeResponse.data).toBe(true);
      expect(resizeResponse.errorMessage).toBeUndefined();

      // Verify the API was called with correct parameters
      expect(callMcpToolStub.calledOnce).toBe(true);
      const callArgs = callMcpToolStub.getCall(0).args[0];
      expect(callArgs.name).toBe("resize_window");
      expect(JSON.parse(callArgs.args)).toEqual({
        window_id: windowId,
        width: width,
        height: height,
      });
    });
  });

  describe("focusMode()", () => {
    it("should enable focus mode with requestId", async () => {
      log("Testing focusMode enable...");

      // Setup mock response
      const mockResponse = {
        statusCode: 200,
        body: {
          data: {
            isError: false,
            content: [],
          },
          requestId: "mock-request-id-focus-enable",
        },
      };

      callMcpToolStub.resolves(mockResponse);

      // Call the method
      const focusEnableResponse = await windowManager.focusMode(true);
      log("Focus mode enabled successfully");
      log(
        `Focus Mode Enable RequestId: ${
          focusEnableResponse.requestId || "undefined"
        }`
      );

      // Verify that the response contains requestId
      expect(focusEnableResponse.success).toBe(true);
      expect(focusEnableResponse.requestId).toBeDefined();
      expect(typeof focusEnableResponse.requestId).toBe("string");
      expect(focusEnableResponse.requestId).toBe(
        "mock-request-id-focus-enable"
      );
      expect(focusEnableResponse.data).toBe(true);
      expect(focusEnableResponse.errorMessage).toBeUndefined();

      // Verify the API was called with correct parameters
      expect(callMcpToolStub.calledOnce).toBe(true);
      const callArgs = callMcpToolStub.getCall(0).args[0];
      expect(callArgs.name).toBe("focus_mode");
      expect(JSON.parse(callArgs.args)).toEqual({ on: true });
    });

    it("should disable focus mode with requestId", async () => {
      log("Testing focusMode disable...");

      // Setup mock response
      const mockResponse = {
        statusCode: 200,
        body: {
          data: {
            isError: false,
            content: [],
          },
          requestId: "mock-request-id-focus-disable",
        },
      };

      callMcpToolStub.resolves(mockResponse);

      // Call the method
      const focusDisableResponse = await windowManager.focusMode(false);
      log("Focus mode disabled successfully");
      log(
        `Focus Mode Disable RequestId: ${
          focusDisableResponse.requestId || "undefined"
        }`
      );

      // Verify that the response contains requestId
      expect(focusDisableResponse.success).toBe(true);
      expect(focusDisableResponse.requestId).toBeDefined();
      expect(typeof focusDisableResponse.requestId).toBe("string");
      expect(focusDisableResponse.requestId).toBe(
        "mock-request-id-focus-disable"
      );
      expect(focusDisableResponse.data).toBe(true);
      expect(focusDisableResponse.errorMessage).toBeUndefined();

      // Verify the API was called with correct parameters
      expect(callMcpToolStub.calledOnce).toBe(true);
      const callArgs = callMcpToolStub.getCall(0).args[0];
      expect(callArgs.name).toBe("focus_mode");
      expect(JSON.parse(callArgs.args)).toEqual({ on: false });
    });
  });
});
