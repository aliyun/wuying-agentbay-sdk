import { AgentBay } from "../../src/agent-bay";
import { CreateSessionParams } from "../../src/session-params";
import { GetCdpLinkRequest } from "../../src/api/models/model";

describe("GetCdpLink Integration Test", () => {
  let agentBay: AgentBay;

  beforeAll(() => {
    const apiKey = process.env.AGENTBAY_API_KEY;
    if (!apiKey) {
      throw new Error("AGENTBAY_API_KEY environment variable not set");
    }
    agentBay = new AgentBay({ apiKey });
  });

  it("should get CDP link with a real browser session", async () => {
    const params = new CreateSessionParams();
    params.imageId = "linux_latest";
    const sessionResult = await agentBay.create(params);

    expect(sessionResult).not.toBeNull();
    expect(sessionResult.success).toBe(true);
    expect(sessionResult.session).not.toBeNull();

    const session = sessionResult.session!;

    try {
      const request = new GetCdpLinkRequest({
        authorization: `Bearer ${agentBay.apiKey}`,
        sessionId: session.sessionId,
      });

      let response;
      try {
        response = await agentBay.client.getCdpLink(request);
      } catch (error: any) {
        if (error.message && error.message.includes("InvalidAction.NotFound")) {
          console.log("Skipping test: GetCdpLink API not yet available in production");
          return;
        }
        throw error;
      }

      expect(response).not.toBeNull();
      expect(response.body).not.toBeNull();
      expect(response.body?.success).toBe(true);
      expect(response.body?.data).not.toBeNull();
      expect(response.body?.data?.url).not.toBeNull();

      const url = response.body?.data?.url;
      expect(url?.startsWith("ws://") || url?.startsWith("wss://")).toBe(true);
      console.log(`CDP URL: ${url}`);
    } finally {
      await session.delete();
    }
  }, 60000);

  it("should throw error with invalid session ID", async () => {
    const request = new GetCdpLinkRequest({
      authorization: `Bearer ${agentBay.apiKey}`,
      sessionId: "invalid-session-id-12345",
    });

    try {
      await agentBay.client.getCdpLink(request);
      fail("Should have thrown an error");
    } catch (error: any) {
      expect(
        error.message.includes("InvalidMcpSession.NotFound") ||
          error.message.includes("InvalidAction.NotFound")
      ).toBe(true);
    }
  }, 30000);
});

