import { AgentBay, Context } from '../src';

/**
 * Example demonstrating how to use the Context API in TypeScript.
 */
async function main() {
  try {
    // Initialize the AgentBay client
    // You can provide the API key as a parameter or set the AGENTBAY_API_KEY environment variable
    const agentBay = new AgentBay({
      apiKey: process.env.AGENTBAY_API_KEY || 'your_api_key_here', // Replace with your actual API key
    });

    // Example 1: List all contexts
    console.log('\nExample 1: Listing all contexts...');
    const contexts = await agentBay.context.list();
    console.log(`Found ${contexts.length} contexts:`);
    for (const context of contexts) {
      console.log(`- ${context.name} (${context.id}): state=${context.state}, os=${context.osType}`);
    }

    // Example 2: Get a context (create if it doesn't exist)
    console.log('\nExample 2: Getting a context (creating if it doesn\'t exist)...');
    const contextName = 'my-test-context';
    const context = await agentBay.context.get(contextName, true);
    if (context) {
      console.log(`Got context: ${context.name} (${context.id})`);
    } else {
      console.log('Context not found and could not be created');
      return;
    }

    // Example 3: Create a session with the context
    console.log('\nExample 3: Creating a session with the context...');
    const session = await agentBay.create({
      contextId: context.id,
      labels: {
        username: 'alice',
        project: 'my-project',
      },
    });
    console.log(`Session created with ID: ${session.sessionId}`);

    // Example 4: Update the context
    console.log('\nExample 4: Updating the context...');
    context.name = 'renamed-test-context';
    const updatedContext = await agentBay.context.update(context);
    console.log(`Context updated: ${updatedContext.name} (${updatedContext.id})`);

    // Clean up
    console.log('\nCleaning up...');

    // Delete the session
    await agentBay.delete(session);
    console.log('Session deleted successfully');

    // Delete the context
    console.log('Deleting the context...');
    await agentBay.context.delete(context);
    console.log('Context deleted successfully');
  } catch (error) {
    console.error('Error:', error);
  }
}

// Run the example
main().catch(console.error);
