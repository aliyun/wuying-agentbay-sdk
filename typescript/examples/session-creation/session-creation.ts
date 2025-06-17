import { AgentBay } from '../../src/agent-bay';
import { Session } from '../../src/session';

// This example demonstrates how to create, list, and delete sessions
// using the Wuying AgentBay SDK.

async function main() {
  try {
    // Get API key from environment variable or use a default value for testing
    const apiKey = process.env.AGENTBAY_API_KEY || 'akm-xxx'; // Replace with your actual API key for testing
    if (!process.env.AGENTBAY_API_KEY) {
      console.log('Warning: Using default API key. Set AGENTBAY_API_KEY environment variable for production use.');
    }

    // Initialize the AgentBay client
    const agentBay = new AgentBay({ apiKey });

    // Create a new session with default parameters
    console.log('\nCreating a new session...');
    const session = await agentBay.create();
    console.log(`\nSession created with ID: ${session.sessionId}`);

    // List all sessions
    console.log('\nListing all sessions...');
    const sessions = agentBay.list();

    // Extract session_id list and join as string
    const sessionIds = sessions.map(s => s.sessionId);
    const sessionIdsStr = sessionIds.join(', ');
    console.log(`\nAvailable sessions: ${sessionIdsStr}`);

    // Create multiple sessions to demonstrate listing
    console.log('\nCreating additional sessions...');
    const additionalSessions: Session[] = [];
    for (let i = 0; i < 2; i++) {
      try {
        const additionalSession = await agentBay.create();
        console.log(`Additional session created with ID: ${additionalSession.sessionId}`);

        // Store the session for later cleanup
        additionalSessions.push(additionalSession);
      } catch (error) {
        console.log(`\nError creating additional session: ${error}`);
        continue;
      }
    }

    // List sessions again to show the new sessions
    console.log('\nListing all sessions after creating additional ones...');
    try {
      const updatedSessions = agentBay.list();
      const updatedSessionIds = updatedSessions.map(s => s.sessionId);
      const updatedSessionIdsStr = updatedSessionIds.join(', ');
      console.log(`\nUpdated list of sessions: ${updatedSessionIdsStr}`);
    } catch (error) {
      console.log(`\nError listing sessions: ${error}`);
    }

    // Clean up all sessions
    console.log('\nCleaning up sessions...');
    // First delete the initial session
    try {
      await agentBay.delete(session);
      console.log(`Session ${session.sessionId} deleted successfully`);
    } catch (error) {
      console.log(`Error deleting session ${session.sessionId}: ${error}`);
    }

    // Then delete the additional sessions
    for (const s of additionalSessions) {
      try {
        await agentBay.delete(s);
        console.log(`Session ${s.sessionId} deleted successfully`);
      } catch (error) {
        console.log(`Error deleting session ${s.sessionId}: ${error}`);
      }
    }

    // List sessions one more time to confirm deletion
    console.log('\nListing sessions after cleanup...');
    try {
      const finalSessions = agentBay.list();
      if (finalSessions.length === 0) {
        console.log('All sessions have been deleted successfully.');
      } else {
        const finalSessionIds = finalSessions.map(s => s.sessionId);
        const finalSessionIdsStr = finalSessionIds.join(', ');
        console.log(`\nRemaining sessions: ${finalSessionIdsStr}`);
      }
    } catch (error) {
      console.log(`\nError listing sessions: ${error}`);
    }
  } catch (error) {
    console.log(`Error initializing AgentBay client: ${error}`);
    process.exit(1);
  }
}

main();
