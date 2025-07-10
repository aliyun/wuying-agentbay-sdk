import { AgentBay, Context } from '../src';
import { log, logError } from '../src/utils/logger';
import { getTestApiKey } from '../tests/utils/test-helpers';

/**
 * Context Management Example
 *
 * This example demonstrates how to use the Context API in TypeScript,
 * corresponding to the Go context_management example.
 */
async function main() {
  try {
    // Initialize the AgentBay client
    // You can provide the API key as a parameter or set the AGENTBAY_API_KEY environment variable
    const apiKey = getTestApiKey();

    const agentBay = new AgentBay({ apiKey });

    // Example 1: List all contexts
    log('\nExample 1: Listing all contexts...');
    const listResponse = await agentBay.context.list();
    log(`Found ${listResponse.contexts.length} contexts (RequestID: ${listResponse.requestId}):`);
    for (const context of listResponse.contexts) {
      log(`- ${context.name} (${context.id}): state=${context.state}, os=${context.osType}`);
    }

    // Example 2: Get a context (create if it doesn't exist)
    log('\nExample 2: Getting a context (creating if it doesn\'t exist)...');
    const contextName = 'my-test-context';
    const getResponse = await agentBay.context.get(contextName, true);

    if (!getResponse.success || !getResponse.context) {
      log('Context not found and could not be created');
      return;
    }

    const context = getResponse.context;
    log(`Got context: ${context.name} (${context.id}) with RequestID: ${getResponse.requestId}`);

    //Example 3: Create a session with the context
    log('\nExample 3: Creating a session with the context...');
    const createResponse = await agentBay.create({
      contextId: context.id,
      labels: {
        username: 'alice',
        project: 'my-project',
      },
    });

    if (!createResponse.success || !createResponse.session) {
      log('Failed to create session with context');
      return;
    }

    const session = createResponse.session;
    log(`Session created with ID: ${session.sessionId} (RequestID: ${createResponse.requestId})`);

    // Example 4: Update the context
    log('\nExample 4: Updating the context...');
    context.name = 'renamed-test-context';
    const updateResponse = await agentBay.context.update(context);

    if (!updateResponse.success) {
      log('Context update was not successful');
    } else {
      log(`Context updated successfully to: ${context.name} (RequestID: ${updateResponse.requestId})`);
    }

    // Clean up
    log('\nCleaning up...');

    // Delete the session
    const deleteSessionResponse = await agentBay.delete(session);
    if (deleteSessionResponse.success) {
      log(`Session deleted successfully (RequestID: ${deleteSessionResponse.requestId})`);
    } else {
      log(`Error deleting session: ${deleteSessionResponse.errorMessage}`);
    }

    // Delete the context
    log('Deleting the context...');
    const deleteContextResponse = await agentBay.context.delete(context);
    if (deleteContextResponse.success) {
      log(`Context deleted successfully (RequestID: ${deleteContextResponse.requestId})`);
    } else {
      log(`Error deleting context: ${deleteContextResponse.errorMessage}`);
    }
  } catch (error) {
    logError('Error:', error);
  }
}

// Run the example
main().catch(logError);
