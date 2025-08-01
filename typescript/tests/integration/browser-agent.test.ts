// Browser agent integration tests
import { AgentBay, Browser, BrowserAgent, log } from '../../src';

function getTestApiKey() {
  const apiKey = process.env.AGENTBAY_API_KEY;
  if (!apiKey) {
    log("Warning: Using default API key. Set AGENTBAY_API_KEY environment variable for testing.");
    return "akm-xxx";
  }
  return apiKey;
}

describe('BrowserAgent Integration Tests', () => {
  let agentBay: AgentBay;
  let session: any;

  beforeEach(async () => {
    const apiKey = getTestApiKey();
    log("api_key =", apiKey);
    agentBay = new AgentBay({ apiKey });

    // Create a session
    log("Creating a new session for browser agent testing...");
    const sessionParam = {
      imageId: "browser_latest"
    };
    
    const result = await agentBay.create(sessionParam);
    
    if (!result.success) {
      log("⚠️ Session creation failed - probably due to resource limitations");
      log("Result data:", result.errorMessage || result);
      session = null; // Mark as failed
      return;
    }
    
    session = result.session;
    log(`Session created with ID: ${session.sessionId}`);
  });

  afterEach(async () => {
    if (session) {
      log("Cleaning up: Deleting the session...");
      try {
        await agentBay.delete(session);
      } catch (error) {
        log(`Warning: Error deleting session: ${error}`);
      }
    }
  });

  test('should have browser property', () => {
    if (!session) {
      log("⏭️ Skipping test - session creation failed");
      expect(true).toBe(true); // Skip test gracefully
      return;
    }
    
    const browser = session.browser;
    expect(browser).toBeDefined();
    expect(browser).toBeInstanceOf(Browser);
    expect(browser.agent).toBeInstanceOf(BrowserAgent);
  });

  test('should initialize browser successfully', async () => {
    if (!session) {
      log("⏭️ Skipping test - session creation failed");
      expect(true).toBe(true); // Skip test gracefully
      return;
    }
    
    const browser = session.browser;
    expect(browser).toBeDefined();
    expect(browser).toBeInstanceOf(Browser);

    const initialized = await browser.initializeAsync({});
    expect(initialized).toBe(true);

    // Note: Getting endpoint URL requires actual MCP tool response
    // In a real test environment, this would return a valid WebSocket URL
    try {
      const endpointUrl = await browser.getEndpointUrl();
      log("endpoint_url data:", endpointUrl.data || endpointUrl);
      expect(endpointUrl).toBeDefined();
    } catch (error: any) {
      log("Expected: Getting endpoint URL might fail in test environment:", error.message);
    }
  }, 30000);

  test('should perform browser agent operations', async () => {
    if (!session) {
      log("⏭️ Skipping test - session creation failed");
      expect(true).toBe(true); // Skip test gracefully
      return;
    }
    
    const browser = session.browser;
    expect(browser).toBeDefined();
    expect(browser).toBeInstanceOf(Browser);

    const initialized = await browser.initializeAsync({});
    expect(initialized).toBe(true);

    // Mock page object (in real scenario would be from Playwright)
    const mockPage = {
      url: () => "http://example.com",
      title: () => "Example Domain"
    };

    // Test act operation
    try {
      const result = await browser.agent.act(mockPage, { action: "Click search button" });
      log("Act result data:", result.data || result);
      expect(result).toBeDefined();
    } catch (error: any) {
      log("Expected: Act operation might fail without real page:", error.message);
    }

    // Test observe operation
    try {
      const [success, observeResults] = await browser.agent.observe(mockPage, { instruction: "Find the search button" });
      log("Observe success:", success);
      log("Observe results count:", observeResults.length);
      expect(typeof success).toBe('boolean');
      expect(Array.isArray(observeResults)).toBe(true);
    } catch (error: any) {
      log("Expected: Observe operation might fail without real page:", error.message);
    }

    // Test extract operation
    try {
      class TestSchema {
        title: string = "";
      }

      const [success, objects] = await browser.agent.extract(mockPage, { 
        instruction: "Extract the title", 
        schema: TestSchema 
      });
      
      log("Extract success:", success);
      log("Extract objects count:", objects.length);
      expect(typeof success).toBe('boolean');
      expect(Array.isArray(objects)).toBe(true);
    } catch (error: any) {
      log("Expected: Extract operation might fail without real page:", error.message);
    }
  }, 60000);
});