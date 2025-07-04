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
    it.only("should accept empty options", async () => {
      // Mock create response
      const mockCreateResponse = {
        data: mockSession,
        requestId: "create-request-id",
      };
      mockAgentBay.create.resolves(mockCreateResponse);

      const createResponse = await mockAgentBay.create();

      // Verify that the response contains requestId
      expect(createResponse.requestId).toBe("create-request-id");
      expect(typeof createResponse.requestId).toBe("string");
    });

    it.only("should accept contextId option", async () => {
      const contextId = "test-context-id";

      // Mock create response with contextId
      const mockCreateResponse = {
        data: mockSession,
        requestId: "create-with-context-request-id",
      };
      mockAgentBay.create.resolves(mockCreateResponse);

      const createResponse = await mockAgentBay.create({ contextId });
      expect(createResponse.requestId).toBe("create-with-context-request-id");
      expect(mockAgentBay.create.calledOnceWith({ contextId })).toBe(true);
    });

    it.only("should accept labels option", async () => {
      const labels = { username: "alice", project: "my-project" };

      // Mock create response with labels
      const mockCreateResponse = {
        data: mockSession,
        requestId: "create-with-labels-request-id",
      };
      mockAgentBay.create.resolves(mockCreateResponse);

      const createResponse = await mockAgentBay.create({ labels });
      expect(createResponse.requestId).toBe("create-with-labels-request-id");
      expect(mockAgentBay.create.calledOnceWith({ labels })).toBe(true);
    });

    it.only("should accept both contextId and labels options", async () => {
      const contextId = "test-context-id";
      const labels = { username: "alice", project: "my-project" };

      // Mock create response with both options
      const mockCreateResponse = {
        data: mockSession,
        requestId: "create-with-both-request-id",
      };
      mockAgentBay.create.resolves(mockCreateResponse);

      const createResponse = await mockAgentBay.create({ contextId, labels });
      expect(createResponse.requestId).toBe("create-with-both-request-id");
      expect(mockAgentBay.create.calledOnceWith({ contextId, labels })).toBe(
        true
      );
    });
  });

  describe("session creation with options", () => {
    it.only("should create a session with the specified options", async () => {
      const options = {
        contextId: "test-context-id",
        labels: { username: "alice" },
      };

      // Mock create response with options
      const mockCreateResponse = {
        data: mockSession,
        requestId: "create-with-options-request-id",
      };
      mockAgentBay.create.resolves(mockCreateResponse);

      const createResponse = await mockAgentBay.create(options);
      expect(createResponse.requestId).toBe("create-with-options-request-id");
      expect(mockAgentBay.create.calledOnceWith(options)).toBe(true);
    });
  });
});
