import { Oss } from "../../src/oss/oss";
import { APIError } from "../../src/exceptions";
import * as sinon from "sinon";

describe("TestOss", () => {
  let mockOss: Oss;
  let mockSession: any;
  let sandbox: sinon.SinonSandbox;

  beforeEach(() => {
    sandbox = sinon.createSandbox();

    mockSession = {
      getAPIKey: sandbox.stub().returns("dummy_key"),
      getClient: sandbox.stub(),
      getSessionId: sandbox.stub().returns("dummy_session"),
    };

    mockOss = new Oss(mockSession);
  });

  afterEach(() => {
    sandbox.restore();
  });

  describe("test_env_init_success", () => {
    it("should initialize OSS environment successfully", async () => {
      const callMcpToolStub = sandbox
        .stub(mockOss as any, "callMcpTool")
        .resolves({
          data: {},
          textContent: '{"endpoint": "test_endpoint", "region": "test_region"}',
          isError: false,
          statusCode: 200,
          requestId: "test-request-id",
        });

      const result = await mockOss.envInit(
        "key_id",
        "key_secret",
        "security_token",
        "test_endpoint"
      );

      // Verify OSSClientResult structure
      expect(result.success).toBe(true);
      expect(result.requestId).toBe("test-request-id");
      expect(result.clientConfig).toBeDefined();
      expect(result.clientConfig.endpoint).toBe("test_endpoint");
      expect(result.clientConfig.region).toBe("test_region");
      expect(result.errorMessage).toBeUndefined();

      expect(callMcpToolStub.calledOnce).toBe(true);
    });
  });

  describe("test_env_init_failure", () => {
    it("should handle env init failure", async () => {
      sandbox
        .stub(mockOss as any, "callMcpTool")
        .rejects(new Error("Failed to create OSS client"));

      const result = await mockOss.envInit(
        "key_id",
        "key_secret",
        "security_token"
      );

      // Verify error result structure
      expect(result.success).toBe(false);
      expect(result.requestId).toBe("");
      expect(result.clientConfig).toEqual({});
      expect(result.errorMessage).toContain(
        "Failed to initialize OSS environment"
      );
    });
  });

  describe("test_upload_success", () => {
    it("should upload file successfully", async () => {
      const callMcpToolStub = sandbox
        .stub(mockOss as any, "callMcpTool")
        .resolves({
          data: {},
          textContent: "Upload success",
          isError: false,
          statusCode: 200,
          requestId: "test-request-id",
        });

      const result = await mockOss.upload(
        "test_bucket",
        "test_object",
        "test_path"
      );

      // Verify OSSUploadResult structure
      expect(result.success).toBe(true);
      expect(result.requestId).toBe("test-request-id");
      expect(result.content).toBe("Upload success");
      expect(result.errorMessage).toBeUndefined();

      expect(callMcpToolStub.calledOnce).toBe(true);
    });
  });

  describe("test_upload_failure", () => {
    it("should handle upload failure", async () => {
      sandbox
        .stub(mockOss as any, "callMcpTool")
        .rejects(
          new Error(
            "Upload failed: The OSS Access Key Id you provided does not exist in our records."
          )
        );

      const result = await mockOss.upload(
        "test_bucket",
        "test_object",
        "test_path"
      );

      // Verify error result structure
      expect(result.success).toBe(false);
      expect(result.requestId).toBe("");
      expect(result.content).toBe("");
      expect(result.errorMessage).toContain("Failed to upload to OSS");
    });
  });

  describe("test_upload_anonymous_success", () => {
    it("should upload anonymously successfully", async () => {
      const callMcpToolStub = sandbox
        .stub(mockOss as any, "callMcpTool")
        .resolves({
          data: {},
          textContent: "upload_anon_success",
          isError: false,
          statusCode: 200,
          requestId: "test-request-id",
        });

      const result = await mockOss.uploadAnonymous("test_url", "test_path");

      // Verify OSSUploadResult structure
      expect(result.success).toBe(true);
      expect(result.requestId).toBe("test-request-id");
      expect(result.content).toBe("upload_anon_success");
      expect(result.errorMessage).toBeUndefined();

      expect(callMcpToolStub.calledOnce).toBe(true);
    });
  });

  describe("test_upload_anonymous_failure", () => {
    it("should handle upload anonymous failure", async () => {
      sandbox
        .stub(mockOss as any, "callMcpTool")
        .rejects(new Error("Failed to upload anonymously"));

      const result = await mockOss.uploadAnonymous("test_url", "test_path");

      // Verify error result structure
      expect(result.success).toBe(false);
      expect(result.requestId).toBe("");
      expect(result.content).toBe("");
      expect(result.errorMessage).toContain("Failed to upload anonymously");
    });
  });

  describe("test_download_success", () => {
    it("should download file successfully", async () => {
      const callMcpToolStub = sandbox
        .stub(mockOss as any, "callMcpTool")
        .resolves({
          data: {},
          textContent: "download_success",
          isError: false,
          statusCode: 200,
          requestId: "test-request-id",
        });

      const result = await mockOss.download(
        "test_bucket",
        "test_object",
        "test_path"
      );

      // Verify OSSDownloadResult structure
      expect(result.success).toBe(true);
      expect(result.requestId).toBe("test-request-id");
      expect(result.content).toBe("download_success");
      expect(result.errorMessage).toBeUndefined();

      expect(callMcpToolStub.calledOnce).toBe(true);
    });
  });

  describe("test_download_failure", () => {
    it("should handle download failure", async () => {
      sandbox
        .stub(mockOss as any, "callMcpTool")
        .rejects(new Error("Failed to download from OSS"));

      const result = await mockOss.download(
        "test_bucket",
        "test_object",
        "test_path"
      );

      // Verify error result structure
      expect(result.success).toBe(false);
      expect(result.requestId).toBe("");
      expect(result.content).toBe("");
      expect(result.errorMessage).toContain("Failed to download from OSS");
    });
  });

  describe("test_download_anonymous_success", () => {
    it("should download anonymously successfully", async () => {
      const callMcpToolStub = sandbox
        .stub(mockOss as any, "callMcpTool")
        .resolves({
          data: {},
          textContent: "download_anon_success",
          isError: false,
          statusCode: 200,
          requestId: "test-request-id",
        });

      const result = await mockOss.downloadAnonymous("test_url", "test_path");

      // Verify OSSDownloadResult structure
      expect(result.success).toBe(true);
      expect(result.requestId).toBe("test-request-id");
      expect(result.content).toBe("download_anon_success");
      expect(result.errorMessage).toBeUndefined();

      expect(callMcpToolStub.calledOnce).toBe(true);
    });
  });

  describe("test_download_anonymous_failure", () => {
    it("should handle download anonymous failure", async () => {
      sandbox
        .stub(mockOss as any, "callMcpTool")
        .rejects(new Error("Failed to download anonymously"));

      const result = await mockOss.downloadAnonymous("test_url", "test_path");

      // Verify error result structure
      expect(result.success).toBe(false);
      expect(result.requestId).toBe("");
      expect(result.content).toBe("");
      expect(result.errorMessage).toContain("Failed to download anonymously");
    });
  });

  describe("test_call_mcp_tool_success", () => {
    it("should call MCP tool successfully", async () => {
      // Mock the response from call_mcp_tool
      const mockResponse = {
        body: {
          data: {
            content: [{ text: "success", type: "text" }],
            isError: false,
          },
          requestId: "test-request-id",
        },
        statusCode: 200,
      };

      mockSession.getClient.returns({
        callMcpTool: sandbox.stub().resolves(mockResponse),
      });

      // Call the private method directly for testing
      const result = await (mockOss as any).callMcpTool(
        "test_tool",
        { arg1: "value1" },
        "Failed to call test_tool"
      );

      expect(result.textContent).toBe("success");
      expect(result.requestId).toBe("test-request-id");
      expect(mockSession.getClient().callMcpTool.calledOnce).toBe(true);

      // Verify the call arguments
      const callArgs = mockSession.getClient().callMcpTool.getCall(0).args[0];
      expect(callArgs.name).toBe("test_tool");
      expect(JSON.parse(callArgs.args)).toEqual({ arg1: "value1" });
    });
  });

  describe("test_call_mcp_tool_failure", () => {
    it("should handle MCP tool failure", async () => {
      // Mock the response from call_mcp_tool
      const mockResponse = {
        body: {
          data: {
            content: [{ text: "Test error message", type: "text" }],
            isError: true,
          },
        },
        statusCode: 200,
        headers: {
          "x-acs-request-id": "test-request-id",
        },
      };

      mockSession.getClient.returns({
        callMcpTool: sandbox.stub().resolves(mockResponse),
      });

      // Call the private method and expect error
      await expect(
        (mockOss as any).callMcpTool(
          "test_tool",
          { arg1: "value1" },
          "Failed to call test_tool"
        )
      ).rejects.toThrow("Test error message");
    });
  });

  describe("test_call_mcp_tool_invalid_response", () => {
    it("should handle invalid response format", async () => {
      // Mock the response from call_mcp_tool with invalid format
      const mockResponse = {
        body: {}, // Empty response
        statusCode: 200,
        headers: {
          "x-acs-request-id": "test-request-id",
        },
      };

      mockSession.getClient.returns({
        callMcpTool: sandbox.stub().resolves(mockResponse),
      });

      // Call the private method and expect error
      await expect(
        (mockOss as any).callMcpTool(
          "test_tool",
          { arg1: "value1" },
          "Failed to call test_tool"
        )
      ).rejects.toThrow("Invalid response data format");
    });
  });

  describe("test_call_mcp_tool_api_error", () => {
    it("should handle API error", async () => {
      // Mock the API call to raise an exception
      mockSession.getClient.returns({
        callMcpTool: sandbox.stub().rejects(new Error("API error")),
      });

      // Call the private method and expect error
      await expect(
        (mockOss as any).callMcpTool(
          "test_tool",
          { arg1: "value1" },
          "Failed to call test_tool"
        )
      ).rejects.toThrow("Failed to call MCP tool test_tool: Error: API error");
    });
  });
});
