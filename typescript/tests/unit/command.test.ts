import * as sinon from "sinon";
import { expect } from "chai";
import { Command } from "../../src/command/command";
import { APIError } from "../../src/exceptions";

describe("Command", () => {
  let mockSession: any;
  let command: Command;
  let callMcpToolStub: sinon.SinonStub;

  beforeEach(() => {
    // Create a mock session
    mockSession = {
      getAPIKey: sinon.stub().returns("test-api-key"),
      getSessionId: sinon.stub().returns("test-session-id"),
      getClient: sinon.stub().returns({}),
    };

    command = new Command(mockSession);
    
    // Stub the private callMcpTool method
    callMcpToolStub = sinon.stub(command as any, "callMcpTool");
  });

  afterEach(() => {
    sinon.restore();
  });

  describe("executeCommand", () => {
    it("should execute command successfully", async () => {
      // Setup mock response
      const mockResult = {
        textContent: "Hello, world!",
        requestId: "test-request-id",
      };
      callMcpToolStub.resolves(mockResult);

      // Execute the test
      const result = await command.executeCommand("echo 'Hello, world!'");

      // Verify results
      expect(result.success).to.be.true;
      expect(result.requestId).to.equal("test-request-id");
      expect(result.output).to.equal("Hello, world!");
      expect(result.errorMessage).to.be.undefined;

      // Verify method was called correctly
      expect(callMcpToolStub.calledOnceWith(
        "shell",
        {
          command: "echo 'Hello, world!'",
          timeout_ms: 1000,
        },
        "Failed to execute command"
      )).to.be.true;
    });

    it("should execute command with custom timeout", async () => {
      // Setup mock response
      const mockResult = {
        textContent: "Command output",
        requestId: "test-request-id",
      };
      callMcpToolStub.resolves(mockResult);

      const customTimeout = 5000;
      
      // Execute the test
      const result = await command.executeCommand("ls", customTimeout);

      // Verify results
      expect(result.success).to.be.true;
      expect(result.requestId).to.equal("test-request-id");
      expect(result.output).to.equal("Command output");

      // Verify method was called with custom timeout
      expect(callMcpToolStub.calledOnceWith(
        "shell",
        {
          command: "ls",
          timeout_ms: customTimeout,
        },
        "Failed to execute command"
      )).to.be.true;
    });

    it("should handle command execution failure", async () => {
      // Setup mock error
      callMcpToolStub.rejects(new APIError("Command execution failed"));

      // Execute the test
      const result = await command.executeCommand("invalid-command");

      // Verify error handling
      expect(result.success).to.be.false;
      expect(result.output).to.equal("");
      expect(result.errorMessage).to.equal("Failed to execute command: APIError: Command execution failed");
    });

    it("should handle empty command", async () => {
      // Setup mock response
      const mockResult = {
        textContent: "",
        requestId: "test-request-id",
      };
      callMcpToolStub.resolves(mockResult);

      // Execute the test
      const result = await command.executeCommand("");

      // Verify results
      expect(result.success).to.be.true;
      expect(result.output).to.equal("");
      expect(result.requestId).to.equal("test-request-id");
    });
  });
});
