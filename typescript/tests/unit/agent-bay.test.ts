import {
  AgentBay,
  Session,
  AuthenticationError,
  APIError,
  ListSessionParams,
} from "../../src";
import { log } from "../../src/utils/logger";
import * as sinon from "sinon";

// Define Node.js process if it's not available
declare namespace NodeJS {
  interface ProcessEnv {
    [key: string]: string | undefined;
  }
}

declare var process: {
  env: {
    [key: string]: string | undefined;
  };
};

// Mock data for tests
const mockSessionData = {
  sessionId: "mock-session-123",
  resourceUrl: "mock-resource-url",
};

const mockSessionAData = {
  sessionId: "mock-session-a-456",
  resourceUrl: "mock-resource-url-a",
};

const mockSessionBData = {
  sessionId: "mock-session-b-789",
  resourceUrl: "mock-resource-url-b",
};

// Mock config data
const mockConfigData = {
  endpoint: "mock-endpoint",
  timeout_ms: 30000,
};

describe("AgentBay", () => {
  let mockClient: any;
  let createMcpSessionStub: sinon.SinonStub;
  let listSessionStub: sinon.SinonStub;
  let releaseMcpSessionStub: sinon.SinonStub;
  let clientConstructorStub: sinon.SinonStub;
  let contextServiceConstructorStub: sinon.SinonStub;

  beforeEach(() => {
    // Create mock client
    mockClient = {
      createMcpSession: sinon.stub(),
      listSession: sinon.stub(),
      releaseMcpSession: sinon.stub(),
    };

    // Get references to stubs for easier access
    createMcpSessionStub = mockClient.createMcpSession;
    listSessionStub = mockClient.listSession;
    releaseMcpSessionStub = mockClient.releaseMcpSession;

    // Set environment variables for config instead of stubbing loadConfig
    process.env.AGENTBAY_ENDPOINT = mockConfigData.endpoint;
    process.env.AGENTBAY_TIMEOUT_MS = String(mockConfigData.timeout_ms);

    // Mock Client constructor
    clientConstructorStub = sinon.stub().returns(mockClient);
    sinon
      .stub(require("../../src/api/client"), "Client")
      .callsFake(clientConstructorStub);

    // Mock ContextService constructor
    const mockContextService = {
      get: sinon.stub().resolves({ 
        success: false, 
        errorMessage: 'Context not found' 
      })
    };
    contextServiceConstructorStub = sinon.stub().returns(mockContextService);
    sinon
      .stub(require("../../src/context"), "ContextService")
      .callsFake(contextServiceConstructorStub);

    // Mock AgentBay's getClient method to return our mock client
    sinon.stub(AgentBay.prototype, "getClient").returns(mockClient);

    // getAPIKey is now private, no need to mock it

    log("Mock client setup complete");
  });

  afterEach(() => {
    sinon.restore();
  });

  describe("constructor", () => {
    it("should initialize with API key from options", () => {
      const apiKey = "test-api-key";
      const agentBay = new AgentBay({ apiKey });
      log(apiKey);

      expect(agentBay.getAPIKey()).toBe(apiKey);

      // loadConfig is now internal, no need to verify

      // Verify that Client was constructed with correct config
      expect(clientConstructorStub.calledOnce).toBe(true);
      const clientConfig = clientConstructorStub.getCall(0).args[0];
      expect(clientConfig.regionId).toBe("");
      expect(clientConfig.endpoint).toBe(mockConfigData.endpoint);
      expect(clientConfig.readTimeout).toBe(mockConfigData.timeout_ms);
      expect(clientConfig.connectTimeout).toBe(mockConfigData.timeout_ms);

      // Verify that ContextService was constructed
      expect(contextServiceConstructorStub.calledOnce).toBe(true);
    });

    it("should initialize with API key from environment variable", () => {
      const originalEnv = process.env.AGENTBAY_API_KEY;
      process.env.AGENTBAY_API_KEY = "env_api_key";

      try {
        const agentBay = new AgentBay();
        expect(agentBay.getAPIKey()).toBe("env_api_key");

        // Verify dependencies were called
        expect(clientConstructorStub.called).toBe(true);
        expect(contextServiceConstructorStub.called).toBe(true);
      } finally {
        // Restore original environment
        if (originalEnv) {
          process.env.AGENTBAY_API_KEY = originalEnv;
        } else {
          delete process.env.AGENTBAY_API_KEY;
        }
      }
    });

    it("should throw AuthenticationError if no API key is provided", () => {
      const originalEnv = process.env.AGENTBAY_API_KEY;
      delete process.env.AGENTBAY_API_KEY;

      // Mock the dotenv.config function to prevent loading .env file
      const dotenvConfigStub = sinon.stub(require("dotenv"), "config");
      
      // Also mock fs.existsSync to prevent loading .env file
      const fsExistsSyncStub = sinon.stub(require("fs"), "existsSync").returns(false);

      try {
        expect(() => new AgentBay()).toThrow(AuthenticationError);
      } finally {
        // Restore original environment
        if (originalEnv) {
          process.env.AGENTBAY_API_KEY = originalEnv;
        }
        // Restore stubs
        dotenvConfigStub.restore();
        fsExistsSyncStub.restore();
      }
    });
  });

  describe("create, list, and delete", () => {
    let agentBay: AgentBay;
    let session: Session;

    beforeEach(() => {
      const apiKey = "test-api-key";
      agentBay = new AgentBay({ apiKey });
    });

    it("should create, list, and delete a session with requestId", async () => {
      // Setup mock response for create session
      const createMockResponse = {
        statusCode: 200,
        body: {
          data: mockSessionData,
          requestId: "mock-request-id-create",
        },
      };

      // Setup mock response for delete session
      const deleteMockResponse = {
        statusCode: 200,
        body: {
          requestId: "mock-request-id-delete",
        },
      };

      createMcpSessionStub.resolves(createMockResponse);
      releaseMcpSessionStub.resolves(deleteMockResponse);

      // Verify mock setup before test
      log("Verifying mock setup...");
      expect(createMcpSessionStub).toBeDefined();
      expect(releaseMcpSessionStub).toBeDefined();
      expect(typeof createMcpSessionStub.resolves).toBe("function");

      // Create a session
      log("Creating a new session...");
      const createResponse = await agentBay.create();
      session = createResponse.session!; // Use session field instead of data
      log(`Session created with ID: ${session?.sessionId || 'undefined'}`);
      log(
        `Create Session RequestId: ${createResponse.requestId || "undefined"}`
      );

      // Verify that the mock was called
      expect(createMcpSessionStub.called).toBe(true);
      log(`createMcpSessionStub called: ${createMcpSessionStub.called}`);
      log(`createMcpSessionStub callCount: ${createMcpSessionStub.callCount}`);

      // Verify that the response contains requestId and success
      expect(createResponse.requestId).toBeDefined();
      expect(typeof createResponse.requestId).toBe("string");
      expect(createResponse.requestId).toBe("mock-request-id-create");
      expect(createResponse.success).toBe(true);
      expect(createResponse.session).toBeDefined();

      // Ensure session ID matches mock data
      expect(session.sessionId).toBe(mockSessionData.sessionId);

      // Client is now private, cannot verify directly
      // The session should work correctly if properly initialized


      // Delete the session
      log("Deleting the session...");
      const deleteResponse = await agentBay.delete(session);
      log(
        `Delete Session RequestId: ${deleteResponse.requestId || "undefined"}`
      );

      // Verify that the delete mock was called
      expect(releaseMcpSessionStub.called).toBe(true);
      log(`releaseMcpSessionStub called: ${releaseMcpSessionStub.called}`);
      log(
        `releaseMcpSessionStub callCount: ${releaseMcpSessionStub.callCount}`
      );

      // Verify that the delete response contains requestId and success
      expect(deleteResponse.requestId).toBeDefined();
      expect(typeof deleteResponse.requestId).toBe("string");
      expect(deleteResponse.requestId).toBe("mock-request-id-delete");
      expect(deleteResponse.success).toBe(true);

      // Session deletion completed

      // Verify API calls were made with correct parameters
      expect(createMcpSessionStub.calledOnce).toBe(true);
      expect(releaseMcpSessionStub.calledOnce).toBe(true);

      const createCallArgs = createMcpSessionStub.getCall(0).args[0];
      expect(createCallArgs.authorization).toBe("Bearer test-api-key");

      const deleteCallArgs = releaseMcpSessionStub.getCall(0).args[0];
      expect(deleteCallArgs.sessionId).toBe(mockSessionData.sessionId);
      expect(deleteCallArgs.authorization).toBe("Bearer test-api-key");

      log("All mock verifications passed successfully");
    });
  });

  describe("list", () => {
    let agentBay: AgentBay;

    beforeEach(() => {
      const apiKey = "test-api-key";
      agentBay = new AgentBay({ apiKey });
    });

    it("should list all sessions without labels", async () => {
      const mockResponse = {
        statusCode: 200,
        body: {
          success: true,
          data: [mockSessionAData, mockSessionBData, mockSessionData],
          maxResults: 10,
          totalCount: 3,
          requestId: "mock-request-id-list-all",
        },
      };

      listSessionStub.resolves(mockResponse);

      const result = await agentBay.list();

      expect(result.success).toBe(true);
      expect(result.requestId).toBe("mock-request-id-list-all");
      expect(result.sessionIds.length).toBe(3);
      expect(result.totalCount).toBe(3);
    });

    it("should list sessions with specific labels", async () => {
      const mockResponse = {
        statusCode: 200,
        body: {
          success: true,
          data: [mockSessionAData],
          maxResults: 10,
          totalCount: 1,
          requestId: "mock-request-id-list-labeled",
        },
      };

      listSessionStub.resolves(mockResponse);

      const result = await agentBay.list({ env: "prod" });

      expect(result.success).toBe(true);
      expect(result.requestId).toBe("mock-request-id-list-labeled");
      expect(result.sessionIds.length).toBe(1);
      expect(listSessionStub.calledOnce).toBe(true);
      const callArgs = listSessionStub.getCall(0).args[0];
      expect(JSON.parse(callArgs.labels)).toEqual({ env: "prod" });
    });

    it("should list sessions with pagination", async () => {
      // First page response
      const mockResponsePage1 = {
        statusCode: 200,
        body: {
          success: true,
          data: [mockSessionAData, mockSessionBData],
          maxResults: 2,
          totalCount: 4,
          nextToken: "token-page2",
          requestId: "mock-request-id-page1",
        },
      };

      // Second page response
      const mockResponsePage2 = {
        statusCode: 200,
        body: {
          success: true,
          data: [mockSessionData],
          maxResults: 2,
          totalCount: 4,
          nextToken: "",
          requestId: "mock-request-id-page2",
        },
      };

      listSessionStub.onFirstCall().resolves(mockResponsePage1);
      listSessionStub.onSecondCall().resolves(mockResponsePage2);

      // Request page 2
      const result = await agentBay.list({ env: "prod" }, 2, 2);

      expect(result.success).toBe(true);
      expect(result.requestId).toBe("mock-request-id-page2");
      expect(result.sessionIds.length).toBe(1);
      expect(result.sessionIds[0]).toBe(mockSessionData.sessionId);
      expect(listSessionStub.calledTwice).toBe(true);
    });

    it("should use default limit of 10 when not specified", async () => {
      const mockResponse = {
        statusCode: 200,
        body: {
          success: true,
          data: [mockSessionAData],
          maxResults: 10,
          totalCount: 1,
          requestId: "mock-request-id",
        },
      };

      listSessionStub.resolves(mockResponse);

      await agentBay.list();

      const callArgs = listSessionStub.getCall(0).args[0];
      expect(callArgs.maxResults).toBe(10);
    });
  });

  describe("policyId passthrough", () => {
    it("should pass policyId to CreateMcpSession request body", async () => {
      const apiKey = "test-api-key";
      const agentBay = new AgentBay({ apiKey });

      const createMockResponse = {
        statusCode: 200,
        body: {
          data: mockSessionData,
          requestId: "mock-request-id-create",
        },
      };
      createMcpSessionStub.resolves(createMockResponse);

      const policyId = "policy-xyz";
      await agentBay.create({ policyId });

      expect(createMcpSessionStub.calledOnce).toBe(true);
      const createCallArgs = createMcpSessionStub.getCall(0).args[0];
      expect(createCallArgs.mcpPolicyId).toBe(policyId);
    });
  });
});
