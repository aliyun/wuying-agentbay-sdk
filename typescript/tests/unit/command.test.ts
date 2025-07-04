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

      expect(result.data).toBe("line1\nline2\n");
      expect(result.requestId).toBe("test-request-id");

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

      expect(result.data).toBe("line1\nline2\n");
      expect(result.requestId).toBe("test-request-id");

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

      expect(result.data).toBe("");
      expect(result.requestId).toBe("test-request-id");
    });
  });

  describe("test_execute_command_exception", () => {
    it("should handle command execution exception", async () => {
      sandbox
        .stub(mockCommand as any, "callMcpTool")
        .rejects(new Error("mock error"));

      await expect(mockCommand.executeCommand("ls -la")).rejects.toThrow(
        "mock error"
      );
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

      expect(result.data).toBe("Hello, world!\n2\n");
      expect(result.requestId).toBe("test-request-id");

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

      expect(result.data).toBe("Hello, world!\n2\n");
      expect(result.requestId).toBe("test-request-id");

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
      await expect(
        mockCommand.runCode("print('test')", "invalid_language")
      ).rejects.toThrow("Unsupported language");
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

      expect(result.data).toBe("");
      expect(result.requestId).toBe("test-request-id");
    });
  });

  describe("test_run_code_exception", () => {
    it("should handle code execution exception", async () => {
      sandbox
        .stub(mockCommand as any, "callMcpTool")
        .rejects(new Error("mock error"));

      await expect(
        mockCommand.runCode("print('test')", "python")
      ).rejects.toThrow("mock error");
    });
  });
});
