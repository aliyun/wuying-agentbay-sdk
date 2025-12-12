import { AgentBay } from "../../src/agent-bay";
import { CreateSessionParams } from "../../src/session-params";
import { GetAdbLinkRequest } from "../../src/api/models/model";

describe("GetAdbLink Integration Test", () => {
  let agentBay: AgentBay;
  let apiKey : string ;

  beforeAll(() => {
    apiKey = process.env.AGENTBAY_API_KEY as string;
    if (!apiKey) {
      throw new Error("AGENTBAY_API_KEY environment variable not set");
    }
    agentBay = new AgentBay({ apiKey });
  });

  it("should get ADB link with a real mobile session", async () => {
    const params = new CreateSessionParams();
    params.imageId = "mobile_latest";
    const sessionResult = await agentBay.create(params);

    expect(sessionResult).not.toBeNull();
    expect(sessionResult.success).toBe(true);
    expect(sessionResult.session).not.toBeNull();

    const session = sessionResult.session!;

    try {
      const options = JSON.stringify({ adbkey_pub: "test-adb-public-key" });

      const request = new GetAdbLinkRequest({
        authorization: `Bearer ${apiKey}`,
        sessionId: session.sessionId,
        option: options,
      });

      let response;
      try {
        response = await agentBay.client.getAdbLink(request);
      } catch (error: any) {
        if (error.message && error.message.includes("InvalidAction.NotFound")) {
          console.log("Skipping test: GetAdbLink API not yet available in production");
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
      expect(url?.toLowerCase().includes("adb") || url?.includes(":")).toBe(true);
      console.log(`ADB URL: ${url}`);
    } finally {
      await session.delete();
    }
  }, 60000);

  it("should throw error with invalid session ID", async () => {
    const options = JSON.stringify({ adbkey_pub: "test-key" });
    const request = new GetAdbLinkRequest({
      authorization: `Bearer ${apiKey}`,
      sessionId: "invalid-session-id-12345",
      option: options,
    });

    try {
      await agentBay.client.getAdbLink(request);
      fail("Should have thrown an error");
    } catch (error: any) {
      expect(
        error.message.includes("InvalidMcpSession.NotFound") ||
          error.message.includes("InvalidAction.NotFound")
      ).toBe(true);
    }
  }, 30000);
});

