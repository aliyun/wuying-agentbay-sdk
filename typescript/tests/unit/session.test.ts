import * as sinon from "sinon";
import { expect } from "chai";
import { Session } from "../../src/session";
import { AgentBay } from "../../src/agent-bay";
import { Client } from "../../src/api/client";

describe("TestSession", () => {
  let mockAgentBay: sinon.SinonStubbedInstance<AgentBay>;
  let mockClient: sinon.SinonStubbedInstance<Client>;
  let mockSession: Session;

  beforeEach(() => {
    mockClient = sinon.createStubInstance(Client);
    mockAgentBay = sinon.createStubInstance(AgentBay) as unknown as sinon.SinonStubbedInstance<AgentBay>;

    // Set up necessary properties
    mockAgentBay.apiKey = "test_api_key";
    mockAgentBay.getClient.returns(mockClient as unknown as Client);

    // Create a session with the mock agent bay
    mockSession = new Session(mockAgentBay as unknown as AgentBay, "test_session_id");
  });

  afterEach(() => {
    sinon.restore();
  });

  describe("test_get_api_key", () => {
    it("should return correct API key", () => {
      const apiKey = mockSession.getAPIKey();
      expect(apiKey).to.equal("test_api_key");
    });
  });

  describe("test_get_client", () => {
    it("should return correct client", () => {
      const client = mockSession.getClient();
      expect(client).to.equal(mockClient);
    });
  });

  describe("test_get_session_id", () => {
    it("should return correct session ID", () => {
      const sessionId = mockSession.getSessionId();
      expect(sessionId).to.be("test_session_id");
    });
  });

  describe("test_delete_success", () => {
    it("should delete session successfully", async () => {
      const mockResponse = {
        body: {
          requestId: "test-request-id",
          success: true,
        },
        statusCode: 200,
      };

      mockClient.releaseMcpSession.resolves(mockResponse);

      const result = await mockSession.delete();

      // Verify DeleteResult structure
      expect(result.success).to.be(true);
      expect(result.requestId).to.be("test-request-id");
      expect(result.errorMessage).to.be(undefined);

      expect(mockClient.releaseMcpSession.calledOnce).to.be(true);

      const callArgs = mockClient.releaseMcpSession.getCall(0).args[0];
      expect(callArgs.authorization).to.be("Bearer test_api_key");
      expect(callArgs.sessionId).to.be("test_session_id");
    });
  });

  describe("test_delete_without_params", () => {
    it("should delete without syncing contexts when no parameters are provided", async () => {
      // Mock context manager
      mockSession.context = {
        sync: sinon.stub().resolves({ success: true }),
        info: sinon.stub().resolves({ contextStatusData: [] })
      } as any;

      const mockResponse = {
        body: {
          requestId: "test-request-id",
          success: true,
        },
        statusCode: 200,
      };

      mockClient.releaseMcpSession.resolves(mockResponse);

      // Call delete without parameters
      const result = await mockSession.delete();

      // Verify sync was not called
      expect((mockSession.context.sync as sinon.SinonStub).called).to.be(false);
      expect((mockSession.context.info as sinon.SinonStub).called).to.be(false);

      // Verify result
      expect(result.success).to.be(true);
      expect(result.requestId).to.be("test-request-id");
    });
  });

  describe("test_delete_with_syncContext", () => {
    it("should sync contexts when syncContext=true", async () => {
      // Mock context manager
      mockSession.context = {
        sync: sinon.stub().resolves({ success: true, requestId: "sync-request-id" }),
        info: sinon.stub().resolves({
          requestId: "info-request-id",
          contextStatusData: [
            {
              contextId: "ctx1",
              path: "/test/path",
              status: "Success",
              taskType: "upload",
              startTime: 1600000000,
              finishTime: 1600000100,
              errorMessage: ""
            }
          ]
        })
      } as any;

      const mockResponse = {
        body: {
          requestId: "test-request-id",
          success: true,
        },
        statusCode: 200,
      };

      mockClient.releaseMcpSession.resolves(mockResponse);

      // Call delete with syncContext=true
      const result = await mockSession.delete(true);

      // Verify sync was called
      expect((mockSession.context.sync as sinon.SinonStub).calledOnce).to.be(true);
      expect((mockSession.context.info as sinon.SinonStub).calledOnce).to.be(true);

      // Verify result
      expect(result.success).to.be(true);
      expect(result.requestId).to.be("test-request-id");
    });

    it("should only process upload tasks", async () => {
      // Mock context manager with mixed task types
      mockSession.context = {
        sync: sinon.stub().resolves({ success: true }),
        info: sinon.stub().resolves({
          contextStatusData: [
            {
              contextId: "ctx1",
              path: "/test/path",
              status: "Success",
              taskType: "download", // This should be ignored
              startTime: 1600000000,
              finishTime: 1600000100,
              errorMessage: ""
            },
            {
              contextId: "ctx2",
              path: "/test/path2",
              status: "InProgress",
              taskType: "upload", // This should be processed
              startTime: 1600000000,
              finishTime: 0,
              errorMessage: ""
            }
          ]
        })
      } as any;

      const mockResponse = {
        body: {
          requestId: "test-request-id",
          success: true,
        },
        statusCode: 200,
      };

      mockClient.releaseMcpSession.resolves(mockResponse);

      // Set up info to return different values on subsequent calls
      const infoStub = mockSession.context.info as sinon.SinonStub;
      infoStub.onFirstCall().resolves({
        contextStatusData: [
          {
            contextId: "ctx2",
            path: "/test/path2",
            status: "InProgress",
            taskType: "upload",
            startTime: 1600000000,
            finishTime: 0,
            errorMessage: ""
          }
        ]
      });
      infoStub.onSecondCall().resolves({
        contextStatusData: [
          {
            contextId: "ctx2",
            path: "/test/path2",
            status: "Success",
            taskType: "upload",
            startTime: 1600000000,
            finishTime: 1600000100,
            errorMessage: ""
          }
        ]
      });

      // Call delete with syncContext=true
      const result = await mockSession.delete(true);

      // Verify sync was called and info was called multiple times
      expect((mockSession.context.sync as sinon.SinonStub).calledOnce).to.be(true);
      expect(infoStub.callCount).to.be.greaterThan(1);

      // Verify result
      expect(result.success).to.be(true);
    });
  });

  describe("test_delete_failure", () => {
    it("should handle delete failure", async () => {
      mockClient.releaseMcpSession.rejects(new Error("Test error"));

      const result = await mockSession.delete();

      // Verify DeleteResult error structure
      expect(result.success).to.be(false);
      expect(result.requestId).to.be("");
      expect(result.errorMessage).to.contain(
        "Failed to delete session test_session_id"
      );

      expect(mockClient.releaseMcpSession.calledOnce).to.be(true);

      const callArgs = mockClient.releaseMcpSession.getCall(0).args[0];
      expect(callArgs.authorization).to.be("Bearer test_api_key");
      expect(callArgs.sessionId).to.be("test_session_id");
    });
  });

  describe("test_info_success", () => {
    it("should get session info successfully", async () => {
      const mockResponse = {
        body: {
          data: {
            sessionId: "test_session_id",
            resourceUrl: "https://example.com/resource",
            desktopInfo: {
              appId: "test-app-id",
              authCode: "test-auth-code",
              connectionProperties: "test-properties",
              resourceId: "test-resource-id",
              resourceType: "desktop",
              ticket: "test-ticket",
            },
          },
          requestId: "info-request-id",
        },
        statusCode: 200,
      };

      mockClient.getMcpResource.resolves(mockResponse);

      const result = await mockSession.info();

      // Verify OperationResult structure
      expect(result.success).toBe(true);
      expect(result.requestId).toBe("info-request-id");
      expect(result.data).toBeDefined();
      expect(result.errorMessage).toBeUndefined();

      expect(result.data.sessionId).toBe("test_session_id");
      expect(result.data.resourceUrl).toBe("https://example.com/resource");
      expect(result.data.appId).toBe("test-app-id");
      expect(result.data.authCode).toBe("test-auth-code");
      expect(result.data.connectionProperties).toBe("test-properties");
      expect(result.data.resourceId).toBe("test-resource-id");
      expect(result.data.resourceType).toBe("desktop");
      expect(result.data.ticket).toBe("test-ticket");

      expect(mockClient.getMcpResource.calledOnce).toBe(true);

      expect(mockSession.resourceUrl).toBe("https://example.com/resource");

      const callArgs = mockClient.getMcpResource.getCall(0).args[0];
      expect(callArgs.authorization).toBe("Bearer test_api_key");
      expect(callArgs.sessionId).toBe("test_session_id");
    });
  });

  describe("test_info_failure", () => {
    it("should handle info failure", async () => {
      mockClient.getMcpResource.rejects(new Error("Get session info failed"));

      await expect(mockSession.info()).rejects.toThrow(
        "Failed to get session info for session test_session_id: Error: Get session info failed"
      );

      expect(mockClient.getMcpResource.calledOnce).toBe(true);
    });
  });

  describe("test_get_link_success", () => {
    it("should get link successfully", async () => {
      const mockResponse = {
        body: {
          data: { Url: "https://example.com/session-link" },
          requestId: "get-link-request-id",
        },
        statusCode: 200,
      };

      mockClient.getLink.resolves(mockResponse);

      const result = await mockSession.getLink();

      // Verify OperationResult structure
      expect(result.success).toBe(true);
      expect(result.requestId).toBe("get-link-request-id");
      expect(result.data).toBe("https://example.com/session-link");
      expect(result.errorMessage).toBeUndefined();

      expect(mockClient.getLink.calledOnce).toBe(true);

      const callArgs = mockClient.getLink.getCall(0).args[0];
      expect(callArgs.authorization).toBe("Bearer test_api_key");
      expect(callArgs.sessionId).toBe("test_session_id");
      expect(callArgs.protocolType).toBeUndefined();
      expect(callArgs.port).toBeUndefined();
    });

    it("should get link successfully with protocol type and port", async () => {
      const mockResponse = {
        body: {
          data: { Url: "https://example.com/session-link" },
          requestId: "get-link-request-id",
        },
        statusCode: 200,
      };

      mockClient.getLink.resolves(mockResponse);

      const result = await mockSession.getLink("https", 8080);

      // Verify OperationResult structure
      expect(result.success).toBe(true);
      expect(result.requestId).toBe("get-link-request-id");
      expect(result.data).toBe("https://example.com/session-link");
      expect(result.errorMessage).toBeUndefined();

      expect(mockClient.getLink.calledOnce).toBe(true);

      const callArgs = mockClient.getLink.getCall(0).args[0];
      expect(callArgs.authorization).toBe("Bearer test_api_key");
      expect(callArgs.sessionId).toBe("test_session_id");
      expect(callArgs.protocolType).toBe("https");
      expect(callArgs.port).toBe(8080);
    });

    it("should handle string data response", async () => {
      const mockResponse = {
        body: {
          data: { Url: "https://example.com/session-link" },
          requestId: "get-link-request-id",
        },
        statusCode: 200,
      };

      mockClient.getLink.resolves(mockResponse);

      const result = await mockSession.getLink();

      // Verify OperationResult structure
      expect(result.success).toBe(true);
      expect(result.requestId).toBe("get-link-request-id");
      expect(result.data).toBe("https://example.com/session-link");
      expect(result.errorMessage).toBeUndefined();
    });

    it("should handle empty data response", async () => {
      const mockResponse = {
        body: {
          data: {},
          requestId: "get-link-request-id",
        },
        statusCode: 200,
      };

      mockClient.getLink.resolves(mockResponse);

      const result = await mockSession.getLink();

      // Verify OperationResult structure
      expect(result.success).toBe(true);
      expect(result.requestId).toBe("get-link-request-id");
      expect(result.data).toBe("");
      expect(result.errorMessage).toBeUndefined();
    });

    it("should exclude undefined parameters from request", async () => {
      const mockResponse = {
        body: {
          data: { Url: "https://example.com/session-link" },
          requestId: "get-link-request-id",
        },
        statusCode: 200,
      };

      mockClient.getLink.resolves(mockResponse);

      await mockSession.getLink(undefined, undefined);

      const callArgs = mockClient.getLink.getCall(0).args[0];
      expect(callArgs.protocolType).toBeUndefined();
      expect(callArgs.port).toBeUndefined();
    });

    it("should exclude empty string protocol type from request", async () => {
      const mockResponse = {
        body: {
          data: { Url: "https://example.com/session-link" },
          requestId: "get-link-request-id",
        },
        statusCode: 200,
      };

      mockClient.getLink.resolves(mockResponse);

      await mockSession.getLink("", 8080);

      const callArgs = mockClient.getLink.getCall(0).args[0];
      expect(callArgs.protocolType).toBe("");
      expect(callArgs.port).toBe(8080);
    });
  });

  describe("test_get_link_failure", () => {
    it("should handle get link failure", async () => {
      mockClient.getLink.rejects(new Error("Get link failed"));

      await expect(mockSession.getLink()).rejects.toThrow(
        "Failed to get link: Error: Get link failed"
      );

      expect(mockClient.getLink.calledOnce).toBe(true);
    });
  });
});

describe("TestAgentBayDelete", () => {
  let mockAgentBay: AgentBay;
  let mockSession: Session;

  beforeEach(() => {
    mockSession = sinon.createStubInstance(Session) as unknown as Session;
    mockSession.sessionId = "test_session_id";

    mockAgentBay = new AgentBay({ apiKey: "test_api_key" });
    mockAgentBay.sessions = new Map();
    mockAgentBay.sessions.set("test_session_id", mockSession);
  });

  afterEach(() => {
    sinon.restore();
  });

  it("should pass no parameters to session.delete when called without parameters", async () => {
    // Set up mock response from session.delete
    const deleteResult = {
      requestId: "test-request-id",
      success: true
    };
    (mockSession.delete as sinon.SinonStub).resolves(deleteResult);

    // Call delete without parameters
    const result = await mockAgentBay.delete(mockSession);

    // Verify session.delete was called without parameters
    expect((mockSession.delete as sinon.SinonStub).calledOnce).to.be(true);
    expect((mockSession.delete as sinon.SinonStub).firstCall.args.length).to.be(0);
    expect(result).to.equal(deleteResult);
  });

  it("should pass syncContext parameter to session.delete", async () => {
    // Set up mock response from session.delete
    const deleteResult = {
      requestId: "test-request-id",
      success: true
    };
    (mockSession.delete as sinon.SinonStub).resolves(deleteResult);

    // Call delete with syncContext=true
    const result = await mockAgentBay.delete(mockSession, true);

    // Verify session.delete was called with syncContext=true
    expect((mockSession.delete as sinon.SinonStub).calledOnce).to.be(true);
    expect((mockSession.delete as sinon.SinonStub).calledWith(true)).to.be(true);
    expect(result).to.equal(deleteResult);
  });
});
