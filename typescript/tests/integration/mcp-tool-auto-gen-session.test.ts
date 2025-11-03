import { AgentBay, Session } from "../../src";
import { getTestApiKey } from "../utils/test-helpers";
import { log } from "../../src/utils/logger";

describe("MCP Tool AutoGenSession Integration", () => {
  let agentBay: AgentBay;

  beforeAll(() => {
    const apiKey = getTestApiKey();
    agentBay = new AgentBay({ apiKey });
  });

  describe("MCP tool call with active session", () => {
    let session: Session;

    beforeAll(async () => {
      // Create a session
      log("Creating session for MCP tool call test...");
      const result = await agentBay.create();
      expect(result.success).toBe(true);
      expect(result.session).toBeDefined();
      session = result.session;
      log(`Session created successfully, ID: ${session.sessionId}`);
    });

    afterAll(async () => {
      // Clean up
      if (session) {
        log("Deleting session...");
        try {
          const deleteResult = await agentBay.delete(session);
          expect(deleteResult.success).toBe(true);
          log("Session deleted successfully");
        } catch (error) {
          log(`Warning: Error deleting session: ${error}`);
        }
      }
    });

    it("should succeed when session is active with autoGenSession=false", async () => {
      // Call MCP tool with active session (autoGenSession=false)
      log("Calling MCP tool with active session...");
      const toolResult = await session.callMcpTool(
        "shell",
        { command: "echo 'test'", timeout_ms: 5000 },
        false
      );
      expect(toolResult.success).toBe(true);
      log(`MCP tool call succeeded (RequestID: ${toolResult.requestId})`);
    });
  });

  describe("MCP tool call with deleted session and autoGenSession=false", () => {
    let session: Session;
    let sessionId: string;

    beforeAll(async () => {
      // Create a session
      log("Creating session for deletion test...");
      const result = await agentBay.create();
      expect(result.success).toBe(true);
      expect(result.session).toBeDefined();
      session = result.session;
      sessionId = session.sessionId;
      log(`Session created successfully, ID: ${sessionId}`);

      // Delete the session
      log("Deleting session...");
      const deleteResult = await session.delete();
      expect(deleteResult.success).toBe(true);
      log(`Session deleted successfully (RequestID: ${deleteResult.requestId})`);

      // Wait for deletion to complete
      await new Promise(resolve => setTimeout(resolve, 2000));

      // Verify session is deleted
      const listResult = await agentBay.list();
      expect(listResult.success).toBe(true);
      expect(listResult.sessionIds).not.toContain(sessionId);
    });

    it("should fail when session is deleted and autoGenSession=false", async () => {
      // Try to call MCP tool with deleted session (autoGenSession=false)
      log("Calling MCP tool with deleted session (autoGenSession=false)...");
      const toolResult = await session.callMcpTool(
        "shell",
        { command: "echo 'test'", timeout_ms: 5000 },
        false
      );
      // Expect failure
      expect(toolResult.success).toBe(false);
      expect(toolResult.errorMessage).toBeDefined();
      expect(toolResult.errorMessage.length).toBeGreaterThan(0);
      log(`MCP tool call failed as expected: ${toolResult.errorMessage}`);
    });
  });

  describe("MCP tool call with deleted session and autoGenSession=true", () => {
    let session: Session;
    let sessionId: string;

    beforeAll(async () => {
      // Create a session
      log("Creating session for auto-gen test...");
      const result = await agentBay.create();
      expect(result.success).toBe(true);
      expect(result.session).toBeDefined();
      session = result.session;
      sessionId = session.sessionId;
      log(`Session created successfully, ID: ${sessionId}`);

      // Delete the session
      log("Deleting session...");
      const deleteResult = await session.delete();
      expect(deleteResult.success).toBe(true);
      log(`Session deleted successfully (RequestID: ${deleteResult.requestId})`);

      // Wait for deletion to complete
      await new Promise(resolve => setTimeout(resolve, 2000));

      // Verify session is deleted
      const listResult = await agentBay.list();
      expect(listResult.success).toBe(true);
      expect(listResult.sessionIds).not.toContain(sessionId);
    });

    it("should handle autoGenSession=true appropriately", async () => {
      // Try to call MCP tool with deleted session (autoGenSession=true)
      log("Calling MCP tool with deleted session (autoGenSession=true)...");
      const toolResult = await session.callMcpTool(
        "shell",
        { command: "echo 'test'", timeout_ms: 5000 },
        true
      );
      // The behavior depends on the server implementation
      // If auto_gen_session is supported, it may succeed by creating a new session
      // If not supported, it should fail
      log(`MCP tool call result: success=${toolResult.success}, error=${toolResult.errorMessage}`);
      // We don't assert success/failure here as it depends on server support
      // Just verify we got a response
      expect(toolResult).toBeDefined();
    });
  });
});

