import { AgentBay } from '../../src/agent-bay';
import { Session } from '../../src/session';
import { log, logError } from '../../src/utils/logger';
import { getTestApiKey } from '../../tests/utils/test-helpers';

// This example demonstrates how to create, list, and delete sessions
// using the Wuying AgentBay SDK.

async function main() {
  try {
    // Get API key from environment variable or use a default value for testing
    const apiKey = getTestApiKey();

    // Initialize the AgentBay client
    const agentBay = new AgentBay({ apiKey });

    // Create a new session with default parameters
    log('\nCreating a new session...');
    const createResponse = await agentBay.create();
    const session = createResponse.session;
    log(`\nSession created with ID: ${session.sessionId}`);
    log(`Create Session RequestId: ${createResponse.requestId}`);

    // List all sessions - Note: This method is not available in TypeScript version
    log('\nNote: Simple list() method is not available in TypeScript version');

    // Create multiple sessions to demonstrate listing
    log('\nCreating additional sessions...');
    const additionalSessions: Session[] = [];
    for (let i = 0; i < 2; i++) {
      try {
        const additionalCreateResponse = await agentBay.create();
        const additionalSession = additionalCreateResponse.session;
        log(`Additional session created with ID: ${additionalSession.sessionId}`);
        log(`Additional Create Session RequestId: ${additionalCreateResponse.requestId}`);

        // Store the session for later cleanup
        additionalSessions.push(additionalSession);
      } catch (error) {
        log(`\nError creating additional session: ${error}`);
        continue;
      }
    }

    // Clean up all sessions
    log('\nCleaning up sessions...');
    // First delete the initial session
    try {
      const deleteResponse = await agentBay.delete(session);
      log(`Session ${session.sessionId} deleted successfully`);
      log(`Delete Session RequestId: ${deleteResponse.requestId}`);
    } catch (error) {
      log(`Error deleting session ${session.sessionId}: ${error}`);
    }

    // Then delete the additional sessions
    for (const s of additionalSessions) {
      try {
        const deleteResponse = await agentBay.delete(s);
        log(`Session ${s.sessionId} deleted successfully`);
        log(`Delete Session RequestId: ${deleteResponse.requestId}`);
      } catch (error) {
        log(`Error deleting session ${s.sessionId}: ${error}`);
      }
    }

    log('\nSession creation example completed successfully');
  } catch (error) {
    logError(`Error initializing AgentBay client: ${error}`);
    process.exit(1);
  }
}

main();
