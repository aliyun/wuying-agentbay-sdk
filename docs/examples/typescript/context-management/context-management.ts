import { AgentBay } from 'wuying-agentbay-sdk';

/**
 * Context Management Example
 *
 * This example demonstrates how to use the Context API in TypeScript.
 */
async function main() {
  try {
    // Initialize the AgentBay client
    // You can provide the API key as a parameter or set the AGENTBAY_API_KEY environment variable
    const apiKey = process.env.AGENTBAY_API_KEY || 'akm-xxx'; // Replace with your actual API key
    if (!process.env.AGENTBAY_API_KEY) {
      console.log('Warning: Using placeholder API key. Set AGENTBAY_API_KEY environment variable for production use.');
    }

    const agentBay = new AgentBay({ apiKey });

    // Example 1: List all contexts
    console.log('\nExample 1: Listing all contexts...');
    try {
      const listResult = await agentBay.context.list();
      console.log(`Found ${listResult.contexts.length} contexts (RequestID: ${listResult.requestId}):`);
      for (const ctx of listResult.contexts) {
        console.log(`- ${ctx.name} (${ctx.id}): state=${ctx.state}, os=${ctx.osType}`);
      }
    } catch (error) {
      console.log(`Error listing contexts: ${error}`);
    }

    // Example 2: Get a context (create if it doesn't exist)
    console.log('\nExample 2: Getting a context (creating if it doesn\'t exist)...');
    const contextName = 'my-test-context';
    const getResult = await agentBay.context.get(contextName, true);
    if (!getResult.contextId || getResult.contextId === '') {
      console.log('Context not found and could not be created');
      return;
    }

    console.log(`Got context: ${getResult.context.name} (${getResult.contextId}) with RequestID: ${getResult.requestId}`);

    // Use the Context object directly
    const context = getResult.context;

    // Example 3: Create a session with the context
    console.log('\nExample 3: Creating a session with the context...');
    const sessionResult = await agentBay.create({
      contextId: context.id,
      labels: {
        username: 'alice',
        project: 'my-project'
      }
    });

    if (!sessionResult.session) {
      console.log('Error creating session');
      return;
    }

    console.log(`Session created with ID: ${sessionResult.session.sessionId} (RequestID: ${sessionResult.requestId})`);
    const session = sessionResult.session;

    // Example 4: Update the context
    console.log('\nExample 4: Updating the context...');
    context.name = 'renamed-test-context';
    try {
      const updateResult = await agentBay.context.update(context);
      if (!updateResult.success) {
        console.log('Context update was not successful');
      } else {
        console.log(`Context updated successfully to: ${context.name} (RequestID: ${updateResult.requestId})`);
      }
    } catch (error) {
      console.log(`Error updating context: ${error}`);
    }

    // Clean up
    console.log('\nCleaning up...');

    // Delete the session
    try {
      const deleteSessionResult = await agentBay.delete(session);
      console.log(`Session deleted successfully (RequestID: ${deleteSessionResult.requestId})`);
    } catch (error) {
      console.log(`Error deleting session: ${error}`);
    }

    // Delete the context
    console.log('Deleting the context...');
    try {
      const deleteContextResult = await agentBay.context.delete(context);
      console.log(`Context deleted successfully (RequestID: ${deleteContextResult.requestId})`);
    } catch (error) {
      console.log(`Error deleting context: ${error}`);
    }
  } catch (error) {
    console.error(`Error initializing AgentBay: ${error}`);
  }
}

// Execute the main function
main().catch(error => {
  console.error('Error in main execution:', error);
  process.exit(1);
}); 