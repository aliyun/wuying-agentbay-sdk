import { AgentBay, Session } from "../../src";
import { getTestApiKey, randomString } from "../utils/test-helpers";

describe("fileSystem.deleteFile", () => {
  let agentBay: AgentBay;
  let session: Session;

  beforeEach(async () => {
    const apiKey = getTestApiKey();
    agentBay = new AgentBay({ apiKey });

    const createResponse = await agentBay.create({ imageId: "linux_latest" });
    if (!createResponse.success || !createResponse.session) {
      throw new Error(
        `Failed to create session: ${createResponse.errorMessage || "Unknown error"}`
      );
    }
    session = createResponse.session;
  });

  afterEach(async () => {
    try {
      if (session) {
        await agentBay.delete(session);
      }
    } catch {
      // ignore cleanup errors
    }
  });

  it("should delete a file", async () => {
    const dir = "/tmp";
    const path = `${dir}/agentbay-delete-file-${randomString()}.txt`;

    const writeRes = await session.fileSystem.writeFile(path, "hello", "overwrite");
    expect(writeRes.success).toBe(true);

    const delRes = await session.fileSystem.deleteFile(path);
    expect(delRes.success).toBe(true);

    const infoRes = await session.fileSystem.getFileInfo(path);
    expect(infoRes.success).toBe(false);
    expect(infoRes.errorMessage).toBeDefined();
  });
});


