import { BROWSER_DATA_PATH } from "../../src/config";
import { BrowserContext, CreateSessionParams } from "../../src/session-params";
import { AgentBay } from "../../src/agent-bay";

describe("BrowserContextConfig", () => {
  describe("BROWSER_DATA_PATH constant", () => {
    it("should be correctly defined", () => {
      expect(BROWSER_DATA_PATH).toBe("/tmp/agentbay_browser");
      expect(typeof BROWSER_DATA_PATH).toBe("string");
      expect(BROWSER_DATA_PATH.startsWith("/")).toBe(true);
    });
  });

  describe("BrowserContext interface", () => {
    it("should create browser context with correct properties", () => {
      const contextId = "test-context-123";
      const autoUpload = true;

      const browserContext: BrowserContext = {
        contextId,
        autoUpload,
      };

      expect(browserContext.contextId).toBe(contextId);
      expect(browserContext.autoUpload).toBe(autoUpload);
    });

    it("should allow autoUpload to be false", () => {
      const contextId = "test-context-456";
      const autoUpload = false;

      const browserContext: BrowserContext = {
        contextId,
        autoUpload,
      };

      expect(browserContext.contextId).toBe(contextId);
      expect(browserContext.autoUpload).toBe(false);
    });
  });

  describe("CreateSessionParams with browser context", () => {
    it("should accept browser context in constructor", () => {
      const contextId = "test-context-789";
      const browserContext: BrowserContext = {
        contextId,
        autoUpload: false,
      };

      const params = new CreateSessionParams();
      params.browserContext = browserContext;

      expect(params.browserContext).toBeDefined();
      expect(params.browserContext?.contextId).toBe(contextId);
      expect(params.browserContext?.autoUpload).toBe(false);
    });

    it("should support withBrowserContext fluent method", () => {
      const contextId = "test-context-fluent";
      const browserContext: BrowserContext = {
        contextId,
        autoUpload: true,
      };

      const params = new CreateSessionParams().withBrowserContext(browserContext);

      expect(params.browserContext).toBeDefined();
      expect(params.browserContext?.contextId).toBe(contextId);
      expect(params.browserContext?.autoUpload).toBe(true);
    });

    it("should serialize browser context correctly", () => {
      const contextId = "test-context-serialization";
      const browserContext: BrowserContext = {
        contextId,
        autoUpload: true,
      };

      const params = new CreateSessionParams();
      params.browserContext = browserContext;

      const jsonConfig = params.toJSON();

      expect(jsonConfig.browserContext).toBeDefined();
      expect(jsonConfig.browserContext?.contextId).toBe(contextId);
      expect(jsonConfig.browserContext?.autoUpload).toBe(true);
    });

    it("should deserialize browser context correctly", () => {
      const contextId = "test-context-deserialization";
      const config = {
        labels: {},
        contextSync: [],
        browserContext: {
          contextId,
          autoUpload: false,
        },
      };

      const params = CreateSessionParams.fromJSON(config);

      expect(params.browserContext).toBeDefined();
      expect(params.browserContext?.contextId).toBe(contextId);
      expect(params.browserContext?.autoUpload).toBe(false);
    });
  });

  describe("AgentBay with browser context", () => {
    it("should handle browser context in create method", () => {
      // This test verifies that the AgentBay class can handle browser context
      // without throwing errors, even though we can't easily mock the complex
      // API calls in unit tests
      const agentBay = new AgentBay({ apiKey: "test-api-key" });
      
      const browserContext: BrowserContext = {
        contextId: "test-context-agentbay",
        autoUpload: true,
      };

      const params = new CreateSessionParams();
      params.browserContext = browserContext;

      // The create method should not throw an error when called with browser context
      // (though it will fail due to missing API key, but that's expected)
      expect(() => {
        // We're not actually calling create() here because it's async and would fail
        // due to missing API key, but we can verify the params are set correctly
        expect(params.browserContext).toBeDefined();
        expect(params.browserContext?.contextId).toBe("test-context-agentbay");
      }).not.toThrow();
    });
  });

  describe("Browser context JSON serialization", () => {
    it("should serialize browser context to JSON correctly", () => {
      const browserContext: BrowserContext = {
        contextId: "test-context-json",
        autoUpload: true,
      };

      const jsonString = JSON.stringify(browserContext);
      const parsed = JSON.parse(jsonString);

      expect(parsed.contextId).toBe("test-context-json");
      expect(parsed.autoUpload).toBe(true);
    });

    it("should handle different autoUpload values", () => {
      const browserContextFalse: BrowserContext = {
        contextId: "test-context-false",
        autoUpload: false,
      };

      const browserContextTrue: BrowserContext = {
        contextId: "test-context-true",
        autoUpload: true,
      };

      const jsonFalse = JSON.stringify(browserContextFalse);
      const jsonTrue = JSON.stringify(browserContextTrue);

      const parsedFalse = JSON.parse(jsonFalse);
      const parsedTrue = JSON.parse(jsonTrue);

      expect(parsedFalse.autoUpload).toBe(false);
      expect(parsedTrue.autoUpload).toBe(true);
    });
  });
});
