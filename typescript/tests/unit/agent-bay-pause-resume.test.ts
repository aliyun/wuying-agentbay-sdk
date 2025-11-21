import { AgentBay, Session } from "../../src";
import * as sinon from "sinon";
import { SessionPauseResult, SessionResumeResult } from "../../src/types/api-response";

// Mock data for tests
const mockSessionData = {
  sessionId: "mock-session-123",
  resourceUrl: "mock-resource-url",
};

describe("AgentBay Pause and Resume", () => {
  let mockClient: any;
  let pauseSessionAsyncStub: sinon.SinonStub;
  let resumeSessionAsyncStub: sinon.SinonStub;
  let getSessionStub: sinon.SinonStub;
  let agentBay: AgentBay;
  let session: Session;

  beforeEach(() => {
    // Create mock client
    mockClient = {
      pauseSessionAsync: sinon.stub(),
      resumeSessionAsync: sinon.stub(),
      getSession: sinon.stub(),
    };

    // Create AgentBay instance with mock client
    agentBay = new AgentBay({ apiKey: "test-api-key" });
    (agentBay as any).client = mockClient;

    // Create mock session
    session = new Session(agentBay, mockSessionData.sessionId);

    // Set up stubs
    pauseSessionAsyncStub = mockClient.pauseSessionAsync;
    resumeSessionAsyncStub = mockClient.resumeSessionAsync;
    getSessionStub = mockClient.getSession;
  });

  afterEach(() => {
    sinon.restore();
  });

  describe("pauseAsync", () => {
    it("should successfully pause a session", async () => {
      // Mock the PauseSessionAsync response
      const mockPauseResponse = {
        body: {
          success: true,
          code: "Success",
          message: "Session pause initiated successfully",
          requestId: "pause-request-id",
          httpStatusCode: 200,
        },
        to_map: () => ({
          body: {
            success: true,
            code: "Success",
            message: "Session pause initiated successfully",
            requestId: "pause-request-id",
            httpStatusCode: 200,
          }
        })
      };

      // Mock get_session to return PAUSED immediately
      const mockGetSessionResponse = {
        body: {
          success: true,
          data: {
            sessionId: mockSessionData.sessionId,
            status: "PAUSED",
          }
        },
        requestId: "get-session-request-id"
      };

      pauseSessionAsyncStub.resolves(mockPauseResponse);
      getSessionStub.resolves(mockGetSessionResponse);

      // Call the method
      const result: SessionPauseResult = await agentBay.pauseAsync(session);

      // Verify the result
      expect(result).toBeDefined();
      expect(result.success).toBe(true);
      expect(result.requestId).toBe("get-session-request-id");
      expect(result.status).toBe("PAUSED");
      expect(result.errorMessage).toBeUndefined();

      // Verify that the API was called with correct parameters
      expect(pauseSessionAsyncStub.calledOnce).toBe(true);
      const calledWith = pauseSessionAsyncStub.getCall(0).args[0];
      expect(calledWith.sessionId).toBe(mockSessionData.sessionId);
    });

    it("should handle pause API error", async () => {
      // Mock the PauseSessionAsync response with error
      const mockPauseResponse = {
        body: {
          success: false,
          code: "InvalidSession",
          message: "Session not found",
          requestId: "test-request-id",
          httpStatusCode: 404,
        },
        to_map: () => ({
          body: {
            success: false,
            code: "InvalidSession",
            message: "Session not found",
            requestId: "test-request-id",
            httpStatusCode: 404,
          }
        })
      };

      pauseSessionAsyncStub.resolves(mockPauseResponse);

      // Call the method
      const result: SessionPauseResult = await agentBay.pauseAsync(session);

      // Verify the result
      expect(result).toBeDefined();
      expect(result.success).toBe(false);
      expect(result.requestId).toBe("test-request-id");
      expect(result.errorMessage).toContain("InvalidSession");
      expect(result.code).toBe("InvalidSession");
      expect(result.message).toBe("Session not found");
      expect(result.httpStatusCode).toBe(404);
    });

    it("should handle network error", async () => {
      // Mock network error
      pauseSessionAsyncStub.rejects(new Error("Network error"));

      // Call the method
      const result: SessionPauseResult = await agentBay.pauseAsync(session);

      // Verify the result
      expect(result).toBeDefined();
      expect(result.success).toBe(false);
      expect(result.errorMessage).toContain("Network error");
    });

    it("should handle timeout scenario", async () => {
      // Mock the PauseSessionAsync response
      const mockPauseResponse = {
        body: {
          success: true,
          code: "Success",
          message: "Session pause initiated successfully",
          requestId: "test-request-id",
          httpStatusCode: 200,
        },
        to_map: () => ({
          body: {
            success: true,
            code: "Success",
            message: "Session pause initiated successfully",
            requestId: "test-request-id",
            httpStatusCode: 200,
          }
        })
      };

      // Mock get_session to always return RUNNING (never PAUSED)
      const mockGetSessionResponse = {
        body: {
          success: true,
          data: {
            sessionId: mockSessionData.sessionId,
            status: "RUNNING",
          }
        }
      };

      pauseSessionAsyncStub.resolves(mockPauseResponse);
      getSessionStub.resolves(mockGetSessionResponse);

      // Call the method with short timeout
      const result: SessionPauseResult = await agentBay.pauseAsync(session, 0.1, 0.05);

      // Verify the result
      expect(result).toBeDefined();
      expect(result.success).toBe(false);
      expect(result.errorMessage).toContain("timed out");
    });

    it("should handle get session failure", async () => {
      // Mock the PauseSessionAsync response
      const mockPauseResponse = {
        body: {
          success: true,
          code: "Success",
          message: "Session pause initiated successfully",
          requestId: "test-request-id",
          httpStatusCode: 200,
        },
        to_map: () => ({
          body: {
            success: true,
            code: "Success",
            message: "Session pause initiated successfully",
            requestId: "test-request-id",
            httpStatusCode: 200,
          }
        })
      };

      // Mock get_session failure
      const mockGetSessionResponse = {
        body: {
          success: false,
          code: "GetSessionError",
          message: "Failed to get session status",
          requestId: "test-request-id",
        }
      };

      pauseSessionAsyncStub.resolves(mockPauseResponse);
      getSessionStub.resolves(mockGetSessionResponse);

      // Call the method
      const result: SessionPauseResult = await agentBay.pauseAsync(session);

      // Verify the result
      expect(result).toBeDefined();
      expect(result.success).toBe(false);
      expect(result.errorMessage).toContain("Failed to get session status");
    });
  });

  describe("resumeAsync", () => {
    it("should successfully resume a session", async () => {
      // Mock the ResumeSessionAsync response
      const mockResumeResponse = {
        body: {
          success: true,
          code: "Success",
          message: "Session resume initiated successfully",
          requestId: "resume-request-id",
          httpStatusCode: 200,
        },
        to_map: () => ({
          body: {
            success: true,
            code: "Success",
            message: "Session resume initiated successfully",
            requestId: "resume-request-id",
            httpStatusCode: 200,
          }
        })
      };

      // Mock get_session to return RUNNING immediately
      const mockGetSessionResponse = {
        body: {
          success: true,
          data: {
            sessionId: mockSessionData.sessionId,
            status: "RUNNING",
          }
        },
        requestId: "get-session-request-id"
      };

      resumeSessionAsyncStub.resolves(mockResumeResponse);
      getSessionStub.resolves(mockGetSessionResponse);

      // Call the method
      const result: SessionResumeResult = await agentBay.resumeAsync(session);

      // Verify the result
      expect(result).toBeDefined();
      expect(result.success).toBe(true);
      expect(result.requestId).toBe("get-session-request-id");
      expect(result.status).toBe("RUNNING");
      expect(result.errorMessage).toBeUndefined();

      // Verify that the API was called with correct parameters
      expect(resumeSessionAsyncStub.calledOnce).toBe(true);
      const calledWith = resumeSessionAsyncStub.getCall(0).args[0];
      expect(calledWith.sessionId).toBe(mockSessionData.sessionId);
    });

    it("should handle resume API error", async () => {
      // Mock the ResumeSessionAsync response with error
      const mockResumeResponse = {
        body: {
          success: false,
          code: "InvalidSession",
          message: "Session not found",
          requestId: "test-request-id",
          httpStatusCode: 404,
        },
        to_map: () => ({
          body: {
            success: false,
            code: "InvalidSession",
            message: "Session not found",
            requestId: "test-request-id",
            httpStatusCode: 404,
          }
        })
      };

      resumeSessionAsyncStub.resolves(mockResumeResponse);

      // Call the method
      const result: SessionResumeResult = await agentBay.resumeAsync(session);

      // Verify the result
      expect(result).toBeDefined();
      expect(result.success).toBe(false);
      expect(result.requestId).toBe("test-request-id");
      expect(result.errorMessage).toContain("InvalidSession");
      expect(result.code).toBe("InvalidSession");
      expect(result.message).toBe("Session not found");
      expect(result.httpStatusCode).toBe(404);
    });

    it("should handle network error", async () => {
      // Mock network error
      resumeSessionAsyncStub.rejects(new Error("Network error"));

      // Call the method
      const result: SessionResumeResult = await agentBay.resumeAsync(session);

      // Verify the result
      expect(result).toBeDefined();
      expect(result.success).toBe(false);
      expect(result.errorMessage).toContain("Network error");
    });

    it("should handle timeout scenario", async () => {
      // Mock the ResumeSessionAsync response
      const mockResumeResponse = {
        body: {
          success: true,
          code: "Success",
          message: "Session resume initiated successfully",
          requestId: "test-request-id",
          httpStatusCode: 200,
        },
        to_map: () => ({
          body: {
            success: true,
            code: "Success",
            message: "Session resume initiated successfully",
            requestId: "test-request-id",
            httpStatusCode: 200,
          }
        })
      };

      // Mock get_session to always return PAUSED (never RUNNING)
      const mockGetSessionResponse = {
        body: {
          success: true,
          data: {
            sessionId: mockSessionData.sessionId,
            status: "PAUSED",
          }
        }
      };

      resumeSessionAsyncStub.resolves(mockResumeResponse);
      getSessionStub.resolves(mockGetSessionResponse);

      // Call the method with short timeout
      const result: SessionResumeResult = await agentBay.resumeAsync(session, 0.1, 0.05);

      // Verify the result
      expect(result).toBeDefined();
      expect(result.success).toBe(false);
      expect(result.errorMessage).toContain("timed out");
    });

    it("should handle get session failure", async () => {
      // Mock the ResumeSessionAsync response
      const mockResumeResponse = {
        body: {
          success: true,
          code: "Success",
          message: "Session resume initiated successfully",
          requestId: "test-request-id",
          httpStatusCode: 200,
        },
        to_map: () => ({
          body: {
            success: true,
            code: "Success",
            message: "Session resume initiated successfully",
            requestId: "test-request-id",
            httpStatusCode: 200,
          }
        })
      };

      // Mock get_session failure
      const mockGetSessionResponse = {
        body: {
          success: false,
          code: "GetSessionError",
          message: "Failed to get session status",
          requestId: "test-request-id",
        }
      };

      resumeSessionAsyncStub.resolves(mockResumeResponse);
      getSessionStub.resolves(mockGetSessionResponse);

      // Call the method
      const result: SessionResumeResult = await agentBay.resumeAsync(session);

      // Verify the result
      expect(result).toBeDefined();
      expect(result.success).toBe(false);
      expect(result.errorMessage).toContain("Failed to get session status");
    });
  });
});