import { AgentBay, Context } from '../src';
import { log, logError } from '../src/utils/logger';
import { getTestApiKey } from '../tests/utils/test-helpers';

/**
 * Example demonstrating how to use the Context API in TypeScript.
 */
async function main() {
  try {
    // Initialize the AgentBay client
    // You can provide the API key as a parameter or set the AGENTBAY_API_KEY environment variable
    const apiKey = getTestApiKey();// Replace with your actual API key

    const agentBay = new AgentBay({apiKey});

    // Example 1: List all contexts
    log('\nExample 1: Listing all contexts...');
    const listResponse = await agentBay.context.list();
    log(`Found ${listResponse.data.length} contexts:`);
    log(`List Contexts RequestId: ${listResponse.requestId}`);
    for (const context of listResponse.data) {
      log(`- ${context.name} (${context.id}): state=${context.state}, os=${context.osType}`);
    }

    // Example 2: Get a context (create if it doesn't exist)
    log('\nExample 2: Getting a context (creating if it doesn\'t exist)...');
    const contextName = 'my-test-context';
    const getResponse = await agentBay.context.get(contextName, true);
    log(`Get Context RequestId: ${getResponse.requestId}`);
    const context = getResponse.data;
    if (context) {
      log(`Got context: ${context.name} (${context.id})`);
    } else {
      log('Context not found and could not be created');
      return;
    }

    // Example 3: Create a session with the context
    log('\nExample 3: Creating a session with the context...');
    const createResponse = await agentBay.create({
      contextId: context.id,
      labels: {
        username: 'alice',
        project: 'my-project',
      },
    });
    const session = createResponse.data;
    log(`Session created with ID: ${session.sessionId}`);
    log(`Create Session RequestId: ${createResponse.requestId}`);

    // Example 4: Update the context
    log('\nExample 4: Updating the context...');
    context.name = 'renamed-test-context';
    const updateResponse = await agentBay.context.update(context);
    log(`Context updated: ${updateResponse.data.name} (${updateResponse.data.id})`);
    log(`Update Context RequestId: ${updateResponse.requestId}`);

    // Clean up
    log('\nCleaning up...');

    // Delete the session
    const deleteSessionResponse = await agentBay.delete(session);
    log('Session deleted successfully');
    log(`Delete Session RequestId: ${deleteSessionResponse.requestId}`);

    // Delete the context
    log('Deleting the context...');
    const deleteContextResponse = await agentBay.context.delete(context);
    log('Context deleted successfully');
    log(`Delete Context RequestId: ${deleteContextResponse.requestId}`);
  } catch (error) {
    logError('Error:', error);
  }
}

// Run the example
main().catch(logError);
