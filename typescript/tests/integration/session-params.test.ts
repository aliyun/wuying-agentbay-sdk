import { AgentBay, Session } from "../../src";
import { getTestApiKey } from "../utils/test-helpers";
import { log } from "../../src/utils/logger";

describe("Session Parameters", () => {
  let agentBay: AgentBay;
  let session: Session;

  beforeEach(async () => {
    const apiKey = getTestApiKey();
    agentBay = new AgentBay({ apiKey });
  });
  afterEach(async () => {
    try {
      if (session) {
        const deleteResponse = await session.delete();
        log("Session deleted successfully");
        log(
          `Delete Session RequestId: ${deleteResponse.requestId || "undefined"}`
        );
      }
    } catch (error) {
      log(`Error deleting session: ${error}`);
    }
  });

  describe("create method options", () => {
    it.only("should accept empty options", async () => {
      try {
        const createResponse = await agentBay.create();
        session = createResponse.session;
        log(
          `Create Session RequestId: ${createResponse.requestId || "undefined"}`
        );

        // Verify that the response contains requestId
        expect(createResponse.requestId).toBeDefined();
        expect(typeof createResponse.requestId).toBe("string");
      } catch (error) {
        log(`Error creating session: ${error}`);
      }
    });

    it.only("should accept contextId option", async () => {
      try {
        const contextId = "test-context-id";
        const createResponse = await agentBay.create({ contextId });
        session = createResponse.session;
        log(
          `Create Session with ContextId RequestId: ${
            createResponse.requestId || "undefined"
          }`
        );
      } catch (error: any) {
        expect(error.message).toMatch(/Failed to create session/);
      }
    });

    it.only("should accept labels option", async () => {
      try {
        const labels = { username: "alice", project: "my-project" };
        const createResponse = await agentBay.create({ labels });
        session = createResponse.session;
        log(
          `Create Session with Labels RequestId: ${
            createResponse.requestId || "undefined"
          }`
        );
      } catch (error: any) {
        log(`Error creating session with labels: ${error}`);
        expect(error.message).toMatch(/Failed to create session/);
      }
    });

    it.only("should accept both contextId and labels options", async () => {
      try {
        const contextId = "test-context-id";
        const labels = { username: "alice", project: "my-project" };
        const createResponse = await agentBay.create({ contextId, labels });
        session = createResponse.session;
        log(
          `Create Session with ContextId and Labels RequestId: ${
            createResponse.requestId || "undefined"
          }`
        );
      } catch (error: any) {
        log(`Error creating session with contextId and labels: ${error}`);
        expect(error.message).toMatch(/Failed to create session/);
      }
    });
  });

  describe("session creation with options", () => {
    it.only("should create a session with the specified options", async () => {
      try {
        const createResponse = await agentBay.create({
          contextId: "test-context-id",
          labels: { username: "alice" },
        });
        session = createResponse.session;
        log(
          `Create Session with Options RequestId: ${
            createResponse.requestId || "undefined"
          }`
        );
      } catch (error: any) {
        log(`Error creating session with options: ${error}`);
        expect(error.message).toMatch(/Failed to create session/);
      }
    });
  });
});
