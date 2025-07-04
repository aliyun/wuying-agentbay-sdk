import { Context, ContextService } from "../../src/context";
import { APIError } from "../../src/exceptions";
import * as sinon from "sinon";

describe("TestContext", () => {
  describe("test_context_initialization", () => {
    it("should initialize Context with the correct attributes", () => {
      const context = new Context(
        "test-id",
        "test-context",
        "available",
        "2025-05-29T12:00:00Z",
        "2025-05-29T12:30:00Z",
        "linux"
      );

      expect(context.id).toBe("test-id");
      expect(context.name).toBe("test-context");
      expect(context.state).toBe("available");
      expect(context.createdAt).toBe("2025-05-29T12:00:00Z");
      expect(context.lastUsedAt).toBe("2025-05-29T12:30:00Z");
      expect(context.osType).toBe("linux");
    });
  });
});

describe("TestContextService", () => {
  let mockContextService: ContextService;
  let mockAgentBay: any;
  let mockClient: any;
  let sandbox: sinon.SinonSandbox;

  beforeEach(() => {
    sandbox = sinon.createSandbox();

    mockClient = {
      listContexts: sandbox.stub(),
      getContext: sandbox.stub(),
      modifyContext: sandbox.stub(),
      deleteContext: sandbox.stub(),
    };

    mockAgentBay = {
      getAPIKey: sandbox.stub().returns("test-api-key"),
      getClient: sandbox.stub().returns(mockClient),
    };

    mockContextService = new ContextService(mockAgentBay);
  });

  afterEach(() => {
    sandbox.restore();
  });

  describe("test_list_contexts", () => {
    it("should list contexts", async () => {
      // Mock the response from the API
      const mockResponse = {
        body: {
          data: [
            {
              id: "context-1",
              name: "context-1-name",
              state: "available",
              createTime: "2025-05-29T12:00:00Z",
              lastUsedTime: "2025-05-29T12:30:00Z",
              osType: "linux",
            },
            {
              id: "context-2",
              name: "context-2-name",
              state: "in-use",
              createTime: "2025-05-29T13:00:00Z",
              lastUsedTime: "2025-05-29T13:30:00Z",
              osType: "windows",
            },
          ],
          requestId: "test-list-request-id",
        },
        statusCode: 200,
      };

      mockClient.listContexts.resolves(mockResponse);

      // Call the method
      const result = await mockContextService.list();

      // Verify the results
      expect(result.data).toHaveLength(2);
      expect(result.data[0].id).toBe("context-1");
      expect(result.data[0].name).toBe("context-1-name");
      expect(result.data[0].state).toBe("available");
      expect(result.data[1].id).toBe("context-2");
      expect(result.data[1].name).toBe("context-2-name");
      expect(result.data[1].state).toBe("in-use");
      expect(result.requestId).toBe("test-list-request-id");

      expect(mockClient.listContexts.calledOnce).toBe(true);
    });
  });

  describe("test_get_context", () => {
    it("should get a context", async () => {
      // Mock the get context response
      const mockGetResponse = {
        body: {
          data: { id: "context-1" },
          requestId: "test-get-request-id",
        },
        statusCode: 200,
      };
      mockClient.getContext.resolves(mockGetResponse);

      // Mock the list response to get full context details
      const mockListResponse = {
        body: {
          data: [
            {
              id: "context-1",
              name: "test-context",
              state: "available",
              createTime: "2025-05-29T12:00:00Z",
              lastUsedTime: "2025-05-29T12:30:00Z",
              osType: "linux",
            },
          ],
          requestId: "test-list-request-id",
        },
        statusCode: 200,
      };
      mockClient.listContexts.resolves(mockListResponse);

      // Call the method
      const result = await mockContextService.get("test-context");

      // Verify the results
      expect(result.data).not.toBeNull();
      expect(result.data!.id).toBe("context-1");
      expect(result.data!.name).toBe("test-context");
      expect(result.data!.state).toBe("available");
      expect(result.requestId).toBe("test-get-request-id");

      expect(mockClient.getContext.calledOnce).toBe(true);
      expect(mockClient.listContexts.calledOnce).toBe(true);
    });
  });

  describe("test_create_context", () => {
    it("should create a context", async () => {
      // Mock the get context response (create via get with allowCreate=true)
      const mockGetResponse = {
        body: {
          data: { id: "new-context-id" },
          requestId: "test-create-request-id",
        },
        statusCode: 200,
      };
      mockClient.getContext.resolves(mockGetResponse);

      // Mock the list response to get full context details
      const mockListResponse = {
        body: {
          data: [
            {
              id: "new-context-id",
              name: "new-context",
              state: "available",
              createTime: "2025-05-29T12:00:00Z",
              lastUsedTime: "2025-05-29T12:30:00Z",
              osType: null,
            },
          ],
          requestId: "test-list-request-id",
        },
        statusCode: 200,
      };
      mockClient.listContexts.resolves(mockListResponse);

      // Call the method
      const result = await mockContextService.create("new-context");

      // Verify the results
      expect(result.data.id).toBe("new-context-id");
      expect(result.data.name).toBe("new-context");
      expect(result.data.state).toBe("available");
      expect(result.requestId).toBe("test-create-request-id");

      expect(mockClient.getContext.calledOnce).toBe(true);
      expect(mockClient.listContexts.calledOnce).toBe(true);
    });
  });

  describe("test_update_context", () => {
    it("should update a context", async () => {
      // Create a context to update
      const context = new Context(
        "context-to-update",
        "updated-name",
        "available"
      );

      // Mock the API response
      const mockResponse = {
        body: {
          code: "ok",
          httpStatusCode: 200,
          success: true,
          requestId: "test-update-request-id",
        },
        statusCode: 200,
      };
      mockClient.modifyContext.resolves(mockResponse);

      // Call the method
      const result = await mockContextService.update(context);

      // Verify the API was called correctly
      expect(mockClient.modifyContext.calledOnce).toBe(true);

      // Verify the results - should return the updated context
      expect(result.data).toBe(context);
      expect(result.data.name).toBe("updated-name");
      expect(result.requestId).toBe("test-update-request-id");
    });
  });

  describe("test_delete_context", () => {
    it("should delete a context", async () => {
      // Create a context to delete
      const context = new Context(
        "context-to-delete",
        "context-name",
        "available"
      );

      // Mock the API response with requestId in body
      const mockResponse = {
        body: {
          code: "ok",
          httpStatusCode: 200,
          success: true,
          requestId: "test-delete-request-id",
        },
        statusCode: 200,
      };
      mockClient.deleteContext.resolves(mockResponse);

      // Call the method
      const result = await mockContextService.delete(context);

      // Verify the API was called correctly
      expect(mockClient.deleteContext.calledOnce).toBe(true);

      // Verify the result has requestId
      expect(result.requestId).toBe("test-delete-request-id");
    });
  });
});
