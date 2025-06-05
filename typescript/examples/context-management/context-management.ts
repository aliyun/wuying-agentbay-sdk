import { AgentBay } from '../../src/agent-bay';

async function main() {
  try {
    // Initialize the AgentBay client
    // You can provide the API key as a parameter or set the AGENTBAY_API_KEY environment variable
    const apiKey = process.env.AGENTBAY_API_KEY || 'akm-xxx'; // Replace with your actual API key
    if (!process.env.AGENTBAY_API_KEY) {
      console.log('Warning: Using default API key. Set AGENTBAY_API_KEY environment variable for production use.');
    }

    const agentBay = new AgentBay({ apiKey });

    // Example 1: List all contexts
    console.log('\nExample 1: Listing all contexts...');
    try {
      const contexts = await agentBay.context.list();
      console.log(`Found ${contexts.length} contexts:`);
      for (const context of contexts) {
        console.log(`- ${context.name} (${context.id}): state=${context.state}, os=${context.osType}`);
      }
    } catch (error) {
      console.log(`Error listing contexts: ${error}`);
    }

    // Example 2: Get a context (create if it doesn't exist)
    console.log('\nExample 2: Getting a context (creating if it doesn\'t exist)...');
    const contextName = 'my-test-context';
    let context;
    try {
      context = await agentBay.context.get(contextName, true);
      if (context) {
        console.log(`Got context: ${context.name} (${context.id})`);
      } else {
        console.log('Context not found and could not be created');
        return;
      }
    } catch (error) {
      console.log(`Error getting context: ${error}`);
      return;
    }

    // Example 3: Create a session with the context
    console.log('\nExample 3: Creating a session with the context...');
    try {
      const session = await agentBay.create({
        contextId: context.id,
        labels: {
          username: 'alice',
          project: 'my-project'
        }
      });
      console.log(`Session created with ID: ${session.sessionId}`);

      // Example 4: Update the context
      console.log('\nExample 4: Updating the context...');
      context.name = 'renamed-test-context';
      try {
        const success = await agentBay.context.update(context);
        if (!success) {
          console.log('Context update was not successful');
        } else {
          console.log(`Context updated successfully to: ${context.name}`);
        }
      } catch (error) {
        console.log(`Error updating context: ${error}`);
      }

      // Clean up
      console.log('\nCleaning up...');

      // Delete the session
      try {
        await agentBay.delete(session.sessionId);
        console.log('Session deleted successfully');
      } catch (error) {
        console.log(`Error deleting session: ${error}`);
      }

      // Delete the context
      console.log('Deleting the context...');
      try {
        await agentBay.context.delete(context);
        console.log('Context deleted successfully');
      } catch (error) {
        console.log(`Error deleting context: ${error}`);
      }
    } catch (error) {
      console.log(`Error creating session: ${error}`);
    }
  } catch (error) {
    console.log(`Error initializing AgentBay: ${error}`);
  }
}

main();
