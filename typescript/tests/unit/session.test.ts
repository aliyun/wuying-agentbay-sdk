import { Session } from "../../src/session";
import { APIError } from "../../src/exceptions";
import * as sinon from "sinon";

describe("TestSession", () => {
  let mockSession: Session;
  let mockAgentBay: any;
  let mockClient: any;
  let sandbox: sinon.SinonSandbox;

  beforeEach(() => {
    sandbox = sinon.createSandbox();

    mockClient = {
      releaseMcpSession: sandbox.stub(),
      setLabel: sandbox.stub(),
      getLabel: sandbox.stub(),
      getMcpResource: sandbox.stub(),
      getLink: sandbox.stub(),
    };

    mockAgentBay = {
      getAPIKey: sandbox.stub().returns("test_api_key"),
      getClient: sandbox.stub().returns(mockClient),
      removeSession: sandbox.stub(),
    };

    mockSession = new Session(mockAgentBay, "test_session_id");
  });

  afterEach(() => {
    sandbox.restore();
  });

  describe("test_initialization", () => {
    it("should initialize session with correct properties", () => {
      expect(mockSession.sessionId).toBe("test_session_id");
      expect(mockSession.getAPIKey()).toBe("test_api_key");
      expect(mockSession.filesystem).toBeDefined();
      expect(mockSession.command).toBeDefined();
      expect(mockSession.oss).toBeDefined();
      expect(mockSession.Application).toBeDefined();
      expect(mockSession.window).toBeDefined();
      expect(mockSession.ui).toBeDefined();
    });
  });

  describe("test_get_api_key", () => {
    it("should return correct API key", () => {
      const apiKey = mockSession.getAPIKey();
      expect(apiKey).toBe("test_api_key");
      expect(mockAgentBay.getAPIKey.calledOnce).toBe(true);
    });
  });

  describe("test_get_client", () => {
    it("should return correct client", () => {
      const client = mockSession.getClient();
      expect(client).toBe(mockClient);
    });
  });

  describe("test_get_session_id", () => {
    it("should return correct session ID", () => {
      const sessionId = mockSession.getSessionId();
      expect(sessionId).toBe("test_session_id");
    });
  });

  describe("test_delete_success", () => {
    it("should delete session successfully", async () => {
      const mockResponse = {
        body: {
          requestId: "test-request-id",
        },
        statusCode: 200,
      };

      mockClient.releaseMcpSession.resolves(mockResponse);

      const result = await mockSession.delete();

      expect(result.requestId).toBe("test-request-id");
      expect(mockClient.releaseMcpSession.calledOnce).toBe(true);
      expect(mockAgentBay.removeSession.calledOnceWith("test_session_id")).toBe(
        true
      );

      const callArgs = mockClient.releaseMcpSession.getCall(0).args[0];
      expect(callArgs.authorization).toBe("Bearer test_api_key");
      expect(callArgs.sessionId).toBe("test_session_id");
    });
  });

  describe("test_delete_failure", () => {
    it("should handle delete failure", async () => {
      mockClient.releaseMcpSession.rejects(new Error("Test error"));

      await expect(mockSession.delete()).rejects.toThrow(
        "Failed to delete session: Error: Test error"
      );

      expect(mockClient.releaseMcpSession.calledOnce).toBe(true);

      const callArgs = mockClient.releaseMcpSession.getCall(0).args[0];
      expect(callArgs.authorization).toBe("Bearer test_api_key");
      expect(callArgs.sessionId).toBe("test_session_id");
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
            },
          },
          requestId: "info-request-id",
        },
        statusCode: 200,
      };

      mockClient.getMcpResource.resolves(mockResponse);

      const result = await mockSession.info();

      expect(result.data.sessionId).toBe("test_session_id");
      expect(result.data.resourceUrl).toBe("https://example.com/resource");
      expect(result.data.appId).toBe("test-app-id");
      expect(result.data.authCode).toBe("test-auth-code");
      expect(result.data.connectionProperties).toBe("test-properties");
      expect(result.data.resourceId).toBe("test-resource-id");
      expect(result.data.resourceType).toBe("desktop");
      expect(result.requestId).toBe("info-request-id");
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
          data: "https://example.com/session-link",
          requestId: "get-link-request-id",
        },
        statusCode: 200,
      };

      mockClient.getLink.resolves(mockResponse);

      const result = await mockSession.getLink();

      expect(result.data).toBe("https://example.com/session-link");
      expect(result.requestId).toBe("get-link-request-id");
      expect(mockClient.getLink.calledOnce).toBe(true);

      const callArgs = mockClient.getLink.getCall(0).args[0];
      expect(callArgs.authorization).toBe("Bearer test_api_key");
      expect(callArgs.sessionId).toBe("test_session_id");
    });
  });

  describe("test_get_link_failure", () => {
    it("should handle get link failure", async () => {
      mockClient.getLink.rejects(new Error("Get link failed"));

      await expect(mockSession.getLink()).rejects.toThrow(
        "Failed to get link for session test_session_id: Error: Get link failed"
      );

      expect(mockClient.getLink.calledOnce).toBe(true);
    });
  });
});
