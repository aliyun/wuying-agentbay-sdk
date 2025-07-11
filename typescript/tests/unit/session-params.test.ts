import { AgentBay, Session } from "../../src";
import { APIError } from "../../src/exceptions";
import * as sinon from "sinon";

describe("Session Parameters", () => {
  let mockAgentBay: any;
  let mockSession: Session;
  let mockClient: any;
  let sandbox: sinon.SinonSandbox;

  beforeEach(() => {
    sandbox = sinon.createSandbox();

    mockClient = {
      createMcpSession: sandbox.stub(),
      releaseMcpSession: sandbox.stub(),
    };

    mockAgentBay = {
      getAPIKey: sandbox.stub().returns("test-api-key"),
      getClient: sandbox.stub().returns(mockClient),
      removeSession: sandbox.stub(),
      create: sandbox.stub(),
    };

    mockSession = new Session(mockAgentBay, "test-session-id");
  });

  afterEach(() => {
    sandbox.restore();
  });

  describe("create method options", () => {
    it("should accept empty options", async () => {
      // Mock create response with SessionResult structure
      const mockCreateResponse = {
        requestId: "create-request-id",
        success: true,
        session: mockSession,
      };
      mockAgentBay.create.resolves(mockCreateResponse);

      const createResponse = await mockAgentBay.create();

      // Verify SessionResult structure
      expect(createResponse.success).toBe(true);
      expect(createResponse.requestId).toBe("create-request-id");
      expect(typeof createResponse.requestId).toBe("string");
      expect(createResponse.session).toBe(mockSession);
      expect(createResponse.errorMessage).toBeUndefined();
    });

    it("should accept contextId option", async () => {
      const contextId = "test-context-id";

      // Mock create response with contextId and SessionResult structure
      const mockCreateResponse = {
        requestId: "create-with-context-request-id",
        success: true,
        session: mockSession,
      };
      mockAgentBay.create.resolves(mockCreateResponse);

      const createResponse = await mockAgentBay.create({ contextId });

      // Verify SessionResult structure
      expect(createResponse.success).toBe(true);
      expect(createResponse.requestId).toBe("create-with-context-request-id");
      expect(createResponse.session).toBe(mockSession);
      expect(createResponse.errorMessage).toBeUndefined();
      expect(mockAgentBay.create.calledOnceWith({ contextId })).toBe(true);
    });

    it("should accept labels option", async () => {
      const labels = { username: "alice", project: "my-project" };

      // Mock create response with labels and SessionResult structure
      const mockCreateResponse = {
        requestId: "create-with-labels-request-id",
        success: true,
        session: mockSession,
      };
      mockAgentBay.create.resolves(mockCreateResponse);

      const createResponse = await mockAgentBay.create({ labels });

      // Verify SessionResult structure
      expect(createResponse.success).toBe(true);
      expect(createResponse.requestId).toBe("create-with-labels-request-id");
      expect(createResponse.session).toBe(mockSession);
      expect(createResponse.errorMessage).toBeUndefined();
      expect(mockAgentBay.create.calledOnceWith({ labels })).toBe(true);
    });

    it("should accept imageId option", async () => {
      const imageId = "test-image-id";

      // Mock create response with imageId and SessionResult structure
      const mockCreateResponse = {
        requestId: "create-with-image-request-id",
        success: true,
        session: mockSession,
      };
      mockAgentBay.create.resolves(mockCreateResponse);

      const createResponse = await mockAgentBay.create({ imageId });

      // Verify SessionResult structure
      expect(createResponse.success).toBe(true);
      expect(createResponse.requestId).toBe("create-with-image-request-id");
      expect(createResponse.session).toBe(mockSession);
      expect(createResponse.errorMessage).toBeUndefined();
      expect(mockAgentBay.create.calledOnceWith({ imageId })).toBe(true);
    });

    it("should accept both contextId and labels options", async () => {
      const contextId = "test-context-id";
      const labels = { username: "alice", project: "my-project" };

      // Mock create response with both options and SessionResult structure
      const mockCreateResponse = {
        requestId: "create-with-both-request-id",
        success: true,
        session: mockSession,
      };
      mockAgentBay.create.resolves(mockCreateResponse);

      const createResponse = await mockAgentBay.create({ contextId, labels });

      // Verify SessionResult structure
      expect(createResponse.success).toBe(true);
      expect(createResponse.requestId).toBe("create-with-both-request-id");
      expect(createResponse.session).toBe(mockSession);
      expect(createResponse.errorMessage).toBeUndefined();
      expect(mockAgentBay.create.calledOnceWith({ contextId, labels })).toBe(
        true
      );
    });

    it("should accept all options together", async () => {
      const contextId = "test-context-id";
      const labels = { username: "alice", project: "my-project" };
      const imageId = "test-image-id";

      // Mock create response with all options and SessionResult structure
      const mockCreateResponse = {
        requestId: "create-with-all-request-id",
        success: true,
        session: mockSession,
      };
      mockAgentBay.create.resolves(mockCreateResponse);

      const createResponse = await mockAgentBay.create({
        contextId,
        labels,
        imageId,
      });

      // Verify SessionResult structure
      expect(createResponse.success).toBe(true);
      expect(createResponse.requestId).toBe("create-with-all-request-id");
      expect(createResponse.session).toBe(mockSession);
      expect(createResponse.errorMessage).toBeUndefined();
      expect(
        mockAgentBay.create.calledOnceWith({ contextId, labels, imageId })
      ).toBe(true);
    });
  });

  describe("session creation with options", () => {
    it("should create a session with the specified options", async () => {
      const options = {
        contextId: "test-context-id",
        labels: { username: "alice" },
        imageId: "test-image-id",
      };

      // Mock create response with options and SessionResult structure
      const mockCreateResponse = {
        requestId: "create-with-options-request-id",
        success: true,
        session: mockSession,
      };
      mockAgentBay.create.resolves(mockCreateResponse);

      const createResponse = await mockAgentBay.create(options);

      // Verify SessionResult structure
      expect(createResponse.success).toBe(true);
      expect(createResponse.requestId).toBe("create-with-options-request-id");
      expect(createResponse.session).toBe(mockSession);
      expect(createResponse.errorMessage).toBeUndefined();
      expect(mockAgentBay.create.calledOnceWith(options)).toBe(true);
    });

    it("should handle create session failure", async () => {
      const options = {
        contextId: "test-context-id",
        labels: { username: "alice" },
      };

      // Mock create response with failure and SessionResult structure
      const mockCreateResponse = {
        requestId: "create-failure-request-id",
        success: false,
        errorMessage: "Failed to create session: API Error",
      };
      mockAgentBay.create.resolves(mockCreateResponse);

      const createResponse = await mockAgentBay.create(options);

      // Verify SessionResult error structure
      expect(createResponse.success).toBe(false);
      expect(createResponse.requestId).toBe("create-failure-request-id");
      expect(createResponse.session).toBeUndefined();
      expect(createResponse.errorMessage).toContain("Failed to create session");
    });
  });
});
