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

    // Set up necessary properties using public methods
    mockAgentBay.getAPIKey.returns("test_api_key");
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
      expect(sessionId).to.equal("test_session_id");
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

      mockClient.releaseMcpSession.resolves(mockResponse as any);

      const result = await mockSession.delete();

      // Verify DeleteResult structure
      expect(result.success).to.equal(true);
      expect(result.requestId).to.equal("test-request-id");
      expect(result.errorMessage).to.be.undefined;

      expect(mockClient.releaseMcpSession.calledOnce).to.be.true;

      const callArgs = mockClient.releaseMcpSession.getCall(0).args[0];
      expect(callArgs.authorization).to.equal("Bearer test_api_key");
      expect(callArgs.sessionId).to.equal("test_session_id");
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

      mockClient.releaseMcpSession.resolves(mockResponse as any);

      // Call delete without parameters
      const result = await mockSession.delete();

      // Verify sync was not called
      expect((mockSession.context.sync as sinon.SinonStub).called).to.be.false;
      expect((mockSession.context.info as sinon.SinonStub).called).to.be.false;

      // Verify result
      expect(result.success).to.equal(true);
      expect(result.requestId).to.equal("test-request-id");
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

      mockClient.releaseMcpSession.resolves(mockResponse as any);

      // Call delete with syncContext=true
      const result = await mockSession.delete(true);

      // Verify sync was called
      expect((mockSession.context.sync as sinon.SinonStub).calledOnce).to.be.true;
      expect((mockSession.context.info as sinon.SinonStub).calledOnce).to.be.true;

      // Verify result
      expect(result.success).to.equal(true);
      expect(result.requestId).to.equal("test-request-id");
    });
  });

  describe("test_delete_failure", () => {
    it("should handle delete failure", async () => {
      const mockResponse = {
        body: {
          requestId: "test-request-id",
          success: false,
          errorMessage: "Delete failed",
        },
        statusCode: 400,
      };

      mockClient.releaseMcpSession.resolves(mockResponse as any);

      const result = await mockSession.delete();

      expect(result.success).to.equal(false);
      expect(result.requestId).to.equal("test-request-id");
      expect(result.errorMessage).to.equal("Failed to delete session");

      expect(mockClient.releaseMcpSession.calledOnce).to.be.true;
    });
  });
});