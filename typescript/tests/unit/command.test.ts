import { Command } from "../../src/command/command";
import { APIError } from "../../src/exceptions";
import * as sinon from "sinon";

describe("TestCommand", () => {
  let mockCommand: Command;
  let mockSession: any;
  let sandbox: sinon.SinonSandbox;

  beforeEach(() => {
    sandbox = sinon.createSandbox();

    mockSession = {
      getAPIKey: sandbox.stub().returns("dummy_key"),
      getClient: sandbox.stub(),
      getSessionId: sandbox.stub().returns("dummy_session"),
    };

    mockCommand = new Command(mockSession);
  });

  afterEach(() => {
    sandbox.restore();
  });

  describe("test_execute_command_success", () => {
    it("should execute command successfully", async () => {
      const callMcpToolStub = sandbox
        .stub(mockCommand as any, "callMcpTool")
        .resolves({
          data: {},
          textContent: "line1\nline2\n",
          isError: false,
          statusCode: 200,
          requestId: "test-request-id",
        });

      const result = await mockCommand.executeCommand("ls -la");

      // Verify CommandResult structure
      expect(result.success).toBe(true);
      expect(result.requestId).toBe("test-request-id");
      expect(result.output).toBe("line1\nline2\n");
      expect(result.errorMessage).toBeUndefined();

      expect(
        callMcpToolStub.calledOnceWith(
          "shell",
          {
            command: "ls -la",
            timeout_ms: 1000,
          },
          "Failed to execute command"
        )
      ).toBe(true);
    });
  });

  describe("test_execute_command_with_custom_timeout", () => {
    it("should execute command with custom timeout", async () => {
      const callMcpToolStub = sandbox
        .stub(mockCommand as any, "callMcpTool")
        .resolves({
          data: {},
          textContent: "line1\nline2\n",
          isError: false,
          statusCode: 200,
          requestId: "test-request-id",
        });

      const customTimeout = 2000;
      const result = await mockCommand.executeCommand("ls -la", customTimeout);

      // Verify CommandResult structure
      expect(result.success).toBe(true);
      expect(result.requestId).toBe("test-request-id");
      expect(result.output).toBe("line1\nline2\n");
      expect(result.errorMessage).toBeUndefined();

      expect(
        callMcpToolStub.calledOnceWith(
          "shell",
          {
            command: "ls -la",
            timeout_ms: customTimeout,
          },
          "Failed to execute command"
        )
      ).toBe(true);
    });
  });

  describe("test_execute_command_no_content", () => {
    it("should handle no content in response", async () => {
      sandbox.stub(mockCommand as any, "callMcpTool").resolves({
        data: {},
        textContent: "",
        isError: false,
        statusCode: 200,
        requestId: "test-request-id",
      });

      const result = await mockCommand.executeCommand("ls -la");

      // Verify CommandResult structure
      expect(result.success).toBe(true);
      expect(result.requestId).toBe("test-request-id");
      expect(result.output).toBe("");
      expect(result.errorMessage).toBeUndefined();
    });
  });

  describe("test_execute_command_exception", () => {
    it("should handle command execution exception", async () => {
      sandbox
        .stub(mockCommand as any, "callMcpTool")
        .rejects(new Error("mock error"));

      const result = await mockCommand.executeCommand("ls -la");

      // Verify error result structure
      expect(result.success).toBe(false);
      expect(result.requestId).toBe("");
      expect(result.output).toBe("");
      expect(result.errorMessage).toContain("Failed to execute command");
    });
  });

  describe("test_run_code_success_python", () => {
    it("should run Python code successfully", async () => {
      const callMcpToolStub = sandbox
        .stub(mockCommand as any, "callMcpTool")
        .resolves({
          data: {},
          textContent: "Hello, world!\n2\n",
          isError: false,
          statusCode: 200,
          requestId: "test-request-id",
        });

      const code = `
print("Hello, world!")
x = 1 + 1
print(x)
`;
      const result = await mockCommand.runCode(code, "python");

      // Verify CodeExecutionResult structure
      expect(result.success).toBe(true);
      expect(result.requestId).toBe("test-request-id");
      expect(result.result).toBe("Hello, world!\n2\n");
      expect(result.errorMessage).toBeUndefined();

      expect(
        callMcpToolStub.calledOnceWith(
          "run_code",
          {
            code: code,
            language: "python",
            timeout_s: 300,
          },
          "Failed to execute code"
        )
      ).toBe(true);
    });
  });

  describe("test_run_code_success_javascript", () => {
    it("should run JavaScript code successfully", async () => {
      const callMcpToolStub = sandbox
        .stub(mockCommand as any, "callMcpTool")
        .resolves({
          data: {},
          textContent: "Hello, world!\n2\n",
          isError: false,
          statusCode: 200,
          requestId: "test-request-id",
        });

      const code = `
console.log("Hello, world!");
const x = 1 + 1;
console.log(x);
`;
      const customTimeout = 600;
      const result = await mockCommand.runCode(
        code,
        "javascript",
        customTimeout
      );

      // Verify CodeExecutionResult structure
      expect(result.success).toBe(true);
      expect(result.requestId).toBe("test-request-id");
      expect(result.result).toBe("Hello, world!\n2\n");
      expect(result.errorMessage).toBeUndefined();

      expect(
        callMcpToolStub.calledOnceWith(
          "run_code",
          {
            code: code,
            language: "javascript",
            timeout_s: customTimeout,
          },
          "Failed to execute code"
        )
      ).toBe(true);
    });
  });

  describe("test_run_code_invalid_language", () => {
    it("should handle invalid language", async () => {
      const result = await mockCommand.runCode("print('test')", "invalid_language");

      // Verify error result structure
      expect(result.success).toBe(false);
      expect(result.requestId).toBe("");
      expect(result.result).toBe("");
      expect(result.errorMessage).toContain("Unsupported language: invalid_language");
    });
  });

  describe("test_run_code_no_output", () => {
    it("should handle no output in response", async () => {
      sandbox.stub(mockCommand as any, "callMcpTool").resolves({
        data: {},
        textContent: "",
        isError: false,
        statusCode: 200,
        requestId: "test-request-id",
      });

      const result = await mockCommand.runCode("print('test')", "python");

      // Verify CodeExecutionResult structure
      expect(result.success).toBe(true);
      expect(result.requestId).toBe("test-request-id");
      expect(result.result).toBe("");
      expect(result.errorMessage).toBeUndefined();
    });
  });

  describe("test_run_code_exception", () => {
    it("should handle code execution exception", async () => {
      sandbox
        .stub(mockCommand as any, "callMcpTool")
        .rejects(new Error("mock error"));

      const result = await mockCommand.runCode("print('test')", "python");

      // Verify error result structure
      expect(result.success).toBe(false);
      expect(result.requestId).toBe("");
      expect(result.result).toBe("");
      expect(result.errorMessage).toContain("Failed to run code");
    });
  });
});
