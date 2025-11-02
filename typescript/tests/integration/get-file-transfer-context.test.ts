import { AgentBay, Session } from "../../src";
import { getTestApiKey } from "../utils/test-helpers";
import { log } from "../../src/utils/logger";

/**
 * Integration tests for the get method file transfer context fix.
 *
 * This test suite verifies that the get() method properly creates a file transfer
 * context when recovering a session, allowing file operations to work correctly.
 */
describe("Get Method File Transfer Context", () => {
  let agentBay: AgentBay;
  let testSession: Session;

  beforeEach(async () => {
    const apiKey = getTestApiKey();
    agentBay = new AgentBay({ apiKey });

    // Create a test session
    log("Creating test session...");
    const createResult = await agentBay.create({ imageId: "code_latest" });

    expect(createResult.success).toBe(true);
    expect(createResult.session).toBeDefined();

    testSession = createResult.session!;
    log(`Test session created with ID: ${testSession.sessionId}`);
  });

  afterEach(async () => {
    // Cleanup: delete the session after test
    if (testSession) {
      try {
        log(`Cleaning up session: ${testSession.sessionId}`);
        await agentBay.delete(testSession);
      } catch (error) {
        log(`Warning: Failed to cleanup session ${testSession.sessionId}: ${error}`);
      }
    }
  });

  it("should create file transfer context when using get method", async () => {
    /**
     * Test that get method creates file transfer context automatically.
     *
     * This test verifies the fix for the bug where recovered sessions
     * couldn't perform file operations due to missing file transfer context.
     */
    log("Testing get method creates file transfer context...");

    // Get the session_id from the test session
    const sessionId = testSession.sessionId;

    // Use get method to recover the session
    const getResult = await agentBay.get(sessionId);

    // Verify get was successful
    expect(getResult.success).toBe(true);
    expect(getResult.session).toBeDefined();
    expect(getResult.session!.sessionId).toBe(sessionId);

    // Verify that the recovered session has a file transfer context ID
    const recoveredSession = getResult.session!;
    expect(recoveredSession.fileTransferContextId).toBeDefined();
    expect(recoveredSession.fileTransferContextId).not.toBeNull();
    expect(recoveredSession.fileTransferContextId).not.toBe("");

    log(`File transfer context ID: ${recoveredSession.fileTransferContextId}`);
  });

  it("should perform file operations on recovered session", async () => {
    /**
     * Test that recovered session can perform actual file operations.
     *
     * This is an end-to-end test that verifies the recovered session
     * can actually upload and download files.
     */
    log("Testing recovered session can perform file operations...");

    // Get the session_id from the test session
    const sessionId = testSession.sessionId;

    // Wait a bit for session to be fully ready
    await new Promise(resolve => setTimeout(resolve, 5000));

    // Use get method to recover the session
    const getResult = await agentBay.get(sessionId);
    expect(getResult.success).toBe(true);

    const recoveredSession = getResult.session!;

    // Create a test file to upload
    const testContent = `Test content at ${Date.now()}`;
    const testFilename = `test_file_${Date.now()}.txt`;
    const testPath = `/tmp/${testFilename}`;

    // Try to write the file using file_system operations
    // This should work if file transfer context is properly set up
    log(`Writing file: ${testPath}`);
    const writeResult = await recoveredSession.fileSystem.writeFile(
      testPath,
      testContent
    );

    // Verify the write was successful
    expect(writeResult.success).toBe(true);

    // Read back the file to verify
    log(`Reading file: ${testPath}`);
    const readResult = await recoveredSession.fileSystem.readFile(testPath);

    expect(readResult.success).toBe(true);
    expect(readResult.content).toBe(testContent);

    log("File operations completed successfully");
  });

  it("should allow both original and recovered sessions to work", async () => {
    /**
     * Test that both original session and recovered session can perform file operations.
     *
     * This test verifies that:
     * 1. Original session created with create() works
     * 2. Recovered session obtained with get() works
     * 3. Both can perform file operations independently
     */
    log("Testing both original and recovered sessions...");

    const sessionId = testSession.sessionId;

    // Wait a bit for session to be fully ready
    await new Promise(resolve => setTimeout(resolve, 5000));

    // Test 1: Original session can write files
    const testContent1 = `Original session test at ${Date.now()}`;
    const testFilename1 = `original_test_${Date.now()}.txt`;
    const testPath1 = `/tmp/${testFilename1}`;

    log(`Original session writing file: ${testPath1}`);
    const writeResult1 = await testSession.fileSystem.writeFile(
      testPath1,
      testContent1
    );
    expect(writeResult1.success).toBe(true);

    // Test 2: Recover the session
    log("Recovering session...");
    const getResult = await agentBay.get(sessionId);
    expect(getResult.success).toBe(true);
    const recoveredSession = getResult.session!;

    // Test 3: Recovered session can write files
    const testContent2 = `Recovered session test at ${Date.now()}`;
    const testFilename2 = `recovered_test_${Date.now()}.txt`;
    const testPath2 = `/tmp/${testFilename2}`;

    log(`Recovered session writing file: ${testPath2}`);
    const writeResult2 = await recoveredSession.fileSystem.writeFile(
      testPath2,
      testContent2
    );
    expect(writeResult2.success).toBe(true);

    // Test 4: Verify both files exist and have correct content
    log("Verifying both files...");
    const readResult1 = await recoveredSession.fileSystem.readFile(testPath1);
    expect(readResult1.success).toBe(true);
    expect(readResult1.content).toBe(testContent1);

    const readResult2 = await recoveredSession.fileSystem.readFile(testPath2);
    expect(readResult2.success).toBe(true);
    expect(readResult2.content).toBe(testContent2);

    log("Both sessions work correctly");
  });
});
