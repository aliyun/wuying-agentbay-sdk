import { AgentBay } from '../../src/agent-bay';
import { Session } from '../../src/session';
import { log } from '../../src/utils/logger';

/**
 * Label Management Example
 *
 * This example demonstrates how to use the label management features
 * of the Wuying AgentBay SDK.
 */

async function main() {
  try {
    // Get API key from environment variable or use a default value for testing
    const apiKey = process.env.AGENTBAY_API_KEY || 'akm-xxx'; // Replace with your actual API key for testing
    if (!process.env.AGENTBAY_API_KEY) {
      log('Warning: Using default API key. Set AGENTBAY_API_KEY environment variable for production use.');
    }

    // Initialize the AgentBay client
    const agentBay = new AgentBay({ apiKey });

    // Create a new session with labels
    log('\nCreating a new session with labels...');
    const session1 = await agentBay.create({
      labels: {
        purpose: 'demo',
        feature: 'label-management',
        version: '1.0'
      }
    });
    log(`Session created with ID: ${session1.sessionId}`);
    
    // Get labels for the session
    log('\nGetting labels for the session...');
    const labels = await session1.getLabels();
    log(`Session labels: ${JSON.stringify(labels)}`);
    
    // Create another session with different labels
    log('\nCreating another session with different labels...');
    const session2 = await agentBay.create({
      labels: {
        purpose: 'demo',
        feature: 'other-feature',
        version: '2.0'
      }
    });
    log(`Session created with ID: ${session2.sessionId}`);
    
    // Update labels for the second session
    log('\nUpdating labels for the second session...');
    await session2.setLabels({
      purpose: 'demo',
      feature: 'label-management',
      version: '2.0',
      status: 'active'
    });
    
    // Get updated labels for the second session
    log('\nGetting updated labels for the second session...');
    const updatedLabels = await session2.getLabels();
    log(`Updated session labels: ${JSON.stringify(updatedLabels)}`);
    
    // List all sessions
    log('\nListing all sessions...');
    const allSessions = agentBay.list();
    log(`Found ${allSessions.length} sessions`);
    for (let i = 0; i < allSessions.length; i++) {
      log(`Session ${i + 1} ID: ${allSessions[i].sessionId}`);
    }
    
    // List sessions by label
    log('\nListing sessions with purpose=demo and feature=label-management...');
    try {
      const filteredSessions = await agentBay.listByLabels({
        purpose: 'demo',
        feature: 'label-management'
      });
      log(`Found ${filteredSessions.length} matching sessions`);
      for (let i = 0; i < filteredSessions.length; i++) {
        log(`Matching session ${i + 1} ID: ${filteredSessions[i].sessionId}`);
        const sessionLabels = await filteredSessions[i].getLabels();
        log(`Labels: ${JSON.stringify(sessionLabels)}`);
      }
    } catch (error) {
      log(`Error listing sessions by labels: ${error}`);
    }
    
    // Delete the sessions
    log('\nDeleting the sessions...');
    try {
      await agentBay.delete(session1);
      log(`Session ${session1.sessionId} deleted successfully`);
      await agentBay.delete(session2);
      log(`Session ${session2.sessionId} deleted successfully`);
    } catch (error) {
      log(`Error deleting sessions: ${error}`);
    }
  } catch (error) {
    log(`Error: ${error}`);
    process.exit(1);
  }
}

main();
