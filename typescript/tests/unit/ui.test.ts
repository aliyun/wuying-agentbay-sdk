import { UI, KeyCode } from "../../src/ui/ui";
import * as sinon from "sinon";

describe("TestUIApi", () => {
  let mockUI: UI;
  let mockSession: any;
  let sandbox: sinon.SinonSandbox;

  beforeEach(() => {
    sandbox = sinon.createSandbox();
    mockSession = {
      getAPIKey: sandbox.stub().returns("test-api-key"),
      getSessionId: sandbox.stub().returns("test-session-id"),
      getClient: sandbox.stub().returns({
        callMcpTool: sandbox.stub(),
      }),
    };
    mockUI = new UI(mockSession);
  });

  afterEach(() => {
    sandbox.restore();
  });
  describe("test_get_clickable_ui_elements_success", () => {
    it("should get clickable UI elements successfully", async () => {
      const mockElements = [
        {
          bounds: "48,90,1032,630",
          className: "LinearLayout",
          text: "digital_widget",
          type: "clickable",
          resourceId: "com.android.deskclock:id/digital_widget",
          index: 11,
          isParent: false,
        },
      ];

      const mockResponse = {
        body: {
          data: {
            isError: false,
            content: [
              {
                text: JSON.stringify(mockElements),
              },
            ],
          },
          requestId: "test-request-id",
        },
        statusCode: 200,
      };

      mockSession.getClient().callMcpTool.resolves(mockResponse);

      const result = await mockUI.getClickableUIElements();

      // Verify UIElementListResult structure
      expect(result.success).toBe(true);
      expect(result.requestId).toBe("test-request-id");
      expect(result.elements).toHaveLength(1);
      expect(result.errorMessage).toBeUndefined();

      expect(result.elements[0].bounds).toBe("48,90,1032,630");
      expect(result.elements[0].className).toBe("LinearLayout");
      expect(result.elements[0].text).toBe("digital_widget");
      expect(result.elements[0].type).toBe("clickable");
      expect(result.elements[0].resourceId).toBe(
        "com.android.deskclock:id/digital_widget"
      );
    });
  });

  describe("test_get_clickable_ui_elements_failure", () => {
    it("should handle get clickable UI elements failure", async () => {
      const mockResponse = {
        body: {
          data: {
            isError: true,
            content: [
              {
                text: "Failed to get clickable UI elements",
              },
            ],
          },
        },
        statusCode: 500,
      };

      mockSession.getClient().callMcpTool.resolves(mockResponse);

      const result = await mockUI.getClickableUIElements();

      // Verify error result structure
      expect(result.success).toBe(false);
      expect(result.requestId).toBe("");
      expect(result.elements).toEqual([]);
      expect(result.errorMessage).toContain(
        "Failed to get clickable UI elements"
      );
    });
  });

  describe("test_send_key_success", () => {
    it("should send key successfully", async () => {
      const mockResponse = {
        body: {
          data: {
            isError: false,
            content: [
              {
                text: "true",
              },
            ],
          },
          requestId: "send-key-request-id",
        },
        statusCode: 200,
      };

      mockSession.getClient().callMcpTool.resolves(mockResponse);

      const result = await mockUI.sendKey(KeyCode.HOME);

      // Verify BoolResult structure
      expect(result.success).toBe(true);
      expect(result.requestId).toBe("send-key-request-id");
      expect(result.data).toBe(true);
      expect(result.errorMessage).toBeUndefined();
    });
  });

  describe("test_send_key_failure", () => {
    it("should handle send key failure", async () => {
      const mockResponse = {
        body: {
          data: {
            isError: true,
            content: [
              {
                text: "Failed to send key",
              },
            ],
          },
        },
        statusCode: 500,
      };

      mockSession.getClient().callMcpTool.resolves(mockResponse);

      const result = await mockUI.sendKey(KeyCode.HOME);

      // Verify error result structure
      expect(result.success).toBe(false);
      expect(result.requestId).toBe("");
      expect(result.errorMessage).toContain("Failed to send key");
    });
  });

  describe("test_swipe_success", () => {
    it("should perform swipe successfully", async () => {
      const mockResponse = {
        body: {
          data: {
            isError: false,
            content: [
              {
                text: "Swipe completed",
              },
            ],
          },
          requestId: "swipe-request-id",
        },
        statusCode: 200,
      };

      mockSession.getClient().callMcpTool.resolves(mockResponse);

      const result = await mockUI.swipe(100, 200, 300, 400, 500);

      // Verify BoolResult structure
      expect(result.success).toBe(true);
      expect(result.requestId).toBe("swipe-request-id");
      expect(result.data).toBe(true);
      expect(result.errorMessage).toBeUndefined();
    });
  });

  describe("test_swipe_failure", () => {
    it("should handle swipe failure", async () => {
      const mockResponse = {
        body: {
          data: {
            isError: true,
            content: [
              {
                text: "Failed to perform swipe",
              },
            ],
          },
        },
        statusCode: 500,
      };

      mockSession.getClient().callMcpTool.resolves(mockResponse);

      const result = await mockUI.swipe(100, 200, 300, 400, 500);

      // Verify error result structure
      expect(result.success).toBe(false);
      expect(result.requestId).toBe("");
      expect(result.errorMessage).toContain("Failed to perform swipe");
    });
  });

  describe("test_click_success", () => {
    it("should perform click successfully", async () => {
      const mockResponse = {
        body: {
          data: {
            isError: false,
            content: [
              {
                text: "Click completed",
              },
            ],
          },
          requestId: "click-request-id",
        },
        statusCode: 200,
      };

      mockSession.getClient().callMcpTool.resolves(mockResponse);

      const result = await mockUI.click(150, 250, "left");

      // Verify BoolResult structure
      expect(result.success).toBe(true);
      expect(result.requestId).toBe("click-request-id");
      expect(result.data).toBe(true);
      expect(result.errorMessage).toBeUndefined();
    });
  });

  describe("test_click_failure", () => {
    it("should handle click failure", async () => {
      const mockResponse = {
        body: {
          data: {
            isError: true,
            content: [
              {
                text: "Failed to perform click",
              },
            ],
          },
        },
        statusCode: 500,
      };

      mockSession.getClient().callMcpTool.resolves(mockResponse);

      const result = await mockUI.click(150, 250, "left");

      // Verify error result structure
      expect(result.success).toBe(false);
      expect(result.requestId).toBe("");
      expect(result.errorMessage).toContain("Failed to perform click");
    });
  });

  describe("test_input_text_success", () => {
    it("should input text successfully", async () => {
      const mockResponse = {
        body: {
          data: {
            isError: false,
            content: [
              {
                text: "Text input completed",
              },
            ],
          },
          requestId: "input-text-request-id",
        },
        statusCode: 200,
      };

      mockSession.getClient().callMcpTool.resolves(mockResponse);

      const result = await mockUI.inputText("Hello, world!");

      // Verify BoolResult structure
      expect(result.success).toBe(true);
      expect(result.requestId).toBe("input-text-request-id");
      expect(result.data).toBe(true);
      expect(result.errorMessage).toBeUndefined();
    });
  });

  describe("test_input_text_failure", () => {
    it("should handle input text failure", async () => {
      const mockResponse = {
        body: {
          data: {
            isError: true,
            content: [
              {
                text: "Failed to input text",
              },
            ],
          },
        },
        statusCode: 500,
      };

      mockSession.getClient().callMcpTool.resolves(mockResponse);

      const result = await mockUI.inputText("Hello, world!");

      // Verify error result structure
      expect(result.success).toBe(false);
      expect(result.requestId).toBe("");
      expect(result.errorMessage).toContain("Failed to input text");
    });
  });

  describe("test_get_all_ui_elements_success", () => {
    it("should get all UI elements successfully", async () => {
      const mockElements = [
        {
          bounds: "48,90,1032,630",
          className: "LinearLayout",
          text: "Sample Text",
          type: "UIElement",
          resourceId: "com.example:id/sample",
          index: 0,
          isParent: true,
          children: [
            {
              bounds: "50,100,200,300",
              className: "TextView",
              text: "Child Text",
              type: "UIElement",
              resourceId: "com.example:id/child",
              index: 1,
              isParent: false,
              children: [],
            },
          ],
        },
      ];

      const mockResponse = {
        body: {
          data: {
            isError: false,
            content: [
              {
                text: JSON.stringify(mockElements),
              },
            ],
          },
          requestId: "get-all-elements-request-id",
        },
        statusCode: 200,
      };

      mockSession.getClient().callMcpTool.resolves(mockResponse);

      const result = await mockUI.getAllUIElements();

      // Verify UIElementListResult structure
      expect(result.success).toBe(true);
      expect(result.requestId).toBe("get-all-elements-request-id");
      expect(result.elements).toHaveLength(1);
      expect(result.errorMessage).toBeUndefined();

      expect(result.elements[0].bounds).toBe("48,90,1032,630");
      expect(result.elements[0].className).toBe("LinearLayout");
      expect(result.elements[0].text).toBe("Sample Text");
      expect(result.elements[0].type).toBe("UIElement");
      expect(result.elements[0].resourceId).toBe("com.example:id/sample");
      expect(result.elements[0].children).toHaveLength(1);
      expect(result.elements[0].children![0].text).toBe("Child Text");
    });
  });

  describe("test_get_all_ui_elements_failure", () => {
    it("should handle get all UI elements failure", async () => {
      const mockResponse = {
        body: {
          data: {
            isError: true,
            content: [
              {
                text: "Failed to get all UI elements",
              },
            ],
          },
        },
        statusCode: 500,
      };

      mockSession.getClient().callMcpTool.resolves(mockResponse);

      const result = await mockUI.getAllUIElements();

      // Verify error result structure
      expect(result.success).toBe(false);
      expect(result.requestId).toBe("");
      expect(result.elements).toEqual([]);
      expect(result.errorMessage).toContain("Failed to get all UI elements");
    });
  });

  describe("test_screenshot_success", () => {
    it("should take screenshot successfully", async () => {
      const OSS_URL = "https://oss-url/screenshot.png";
      const mockResponse = {
        body: {
          data: {
            isError: false,
            content: [
              {
                text: OSS_URL,
              },
            ],
          },
          requestId: "screenshot-request-id",
        },
        statusCode: 200,
      };

      mockSession.getClient().callMcpTool.resolves(mockResponse);

      const result = await mockUI.screenshot();

      // Verify OperationResult structure
      expect(result.success).toBe(true);
      expect(result.requestId).toBe("screenshot-request-id");
      expect(result.data).toBe(OSS_URL);
      expect(result.errorMessage).toBeUndefined();
    });
  });

  describe("test_screenshot_failure", () => {
    it("should handle screenshot failure", async () => {
      const mockResponse = {
        body: {
          data: {
            isError: true,
            content: [
              {
                text: "Error in response: Failed to take screenshot",
              },
            ],
          },
        },
        statusCode: 500,
      };

      mockSession.getClient().callMcpTool.resolves(mockResponse);

      const result = await mockUI.screenshot();

      // Verify error result structure
      expect(result.success).toBe(false);
      expect(result.requestId).toBe("");
      expect(result.errorMessage).toContain("Failed to take screenshot");
    });
  });

  describe("test_screenshot_exception_handling", () => {
    it("should handle screenshot exception", async () => {
      mockSession.getClient().callMcpTool.rejects(new Error("Network error"));

      const result = await mockUI.screenshot();

      // Verify error result structure
      expect(result.success).toBe(false);
      expect(result.requestId).toBe("");
      expect(result.errorMessage).toContain("Failed to take screenshot");
    });
  });
});
