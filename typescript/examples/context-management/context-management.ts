import { AgentBay } from '../../src/agent-bay';
import { log, logError } from '../../src/utils/logger';
import { getTestApiKey } from '../../tests/utils/test-helpers';

async function main() {
  try {
    // Initialize the AgentBay client
    // You can provide the API key as a parameter or set the AGENTBAY_API_KEY environment variable
    const apiKey = getTestApiKey();

    const agentBay = new AgentBay({ apiKey });

    // Example 1: List all contexts
    log('\nExample 1: Listing all contexts...');
    try {
      const contextsResponse = await agentBay.context.list();
      log(`Found ${contextsResponse.data.length} contexts:`);
      log(`List Contexts RequestId: ${contextsResponse.requestId}`);
      for (const context of contextsResponse.data) {
        log(`- ${context.name} (${context.id}): state=${context.state}, os=${context.osType}`);
      }
    } catch (error) {
      log(`Error listing contexts: ${error}`);
    }

    // Example 2: Get a context (create if it doesn't exist)
    log('\nExample 2: Getting a context (creating if it doesn\'t exist)...');
    const contextName = 'my-test-context';
    let context;
    try {
      const contextResponse = await agentBay.context.get(contextName, true);
      log(`Get Context RequestId: ${contextResponse.requestId}`);
      if (contextResponse.data) {
        context = contextResponse.data;
        log(`Got context: ${context.name} (${context.id})`);
      } else {
        log('Context not found and could not be created');
        return;
      }
    } catch (error) {
      log(`Error getting context: ${error}`);
      return;
    }

    // Example 3: Create a session with the context
    log('\nExample 3: Creating a session with the context...');
    try {
      const createResponse = await agentBay.create({
        contextId: context.id,
        labels: {
          username: 'alice',
          project: 'my-project'
        }
      });
      const session = createResponse.data;
      log(`Session created with ID: ${session.sessionId}`);
      log(`Create Session RequestId: ${createResponse.requestId}`);

      // Example 4: Update the context
      log('\nExample 4: Updating the context...');
      context.name = 'renamed-test-context';
      try {
        const updateResponse = await agentBay.context.update(context);
        log(`Context updated successfully to: ${updateResponse.data.name}`);
        log(`Update Context RequestId: ${updateResponse.requestId}`);
      } catch (error) {
        log(`Error updating context: ${error}`);
      }

      // Clean up
      log('\nCleaning up...');

      // Delete the session
      try {
        const deleteSessionResponse = await agentBay.delete(session);
        log('Session deleted successfully');
        log(`Delete Session RequestId: ${deleteSessionResponse.requestId}`);
      } catch (error) {
        log(`Error deleting session: ${error}`);
      }

      // Delete the context
      log('Deleting the context...');
      try {
        const deleteContextResponse = await agentBay.context.delete(context);
        log('Context deleted successfully');
        log(`Delete Context RequestId: ${deleteContextResponse.requestId}`);
      } catch (error) {
        log(`Error deleting context: ${error}`);
      }
    } catch (error) {
      log(`Error creating session: ${error}`);
    }
  } catch (error) {
    logError(`Error initializing AgentBay: ${error}`);
  }
}

main();
