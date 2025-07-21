import { AgentBay, ListSessionParams } from 'wuying-agentbay-sdk';
async function main() {
  try {
    // Use the test API key function from test-helpers
    const apiKey = process.env.AGENTBAY_API_KEY || 'akm-xxx'; // Replace with your actual API key
  if (!process.env.AGENTBAY_API_KEY) {
    console.log('Warning: Using placeholder API key. Set AGENTBAY_API_KEY environment variable for production use.');
  }

    // Initialize the AgentBay client
    const agentBay = new AgentBay({ apiKey });

    // Create a new session with labels
    console.log('Creating a new session with labels...');
    const createResponse = await agentBay.create({imageId:'browser_latest'});
    const session = createResponse.session;
    console.log(`Session created with ID: ${session.sessionId}`);
    console.log(`Create Session RequestId: ${createResponse.requestId}`);

    // Execute a command
    console.log('\nExecuting a command...');
    const commandResponse = await session.command.executeCommand('ls -la');
    console.log('Command result:', commandResponse.output);
    console.log(`Execute Command RequestId: ${commandResponse.requestId}`);

    // Read a file
    console.log('\nReading a file...');
    const fileResponse = await session.fileSystem.readFile('/etc/hosts');
    console.log(`File content: ${fileResponse.content}`);
    console.log(`Read File RequestId: ${fileResponse.requestId}`);

    // Get the session link
    console.log('\nGetting session link...');
    try {
      const linkResponse = await session.getLink();
      console.log(`Session link: ${linkResponse.data}`);
      console.log(`Get Link RequestId: ${linkResponse.requestId}`);
    } catch (error) {
      console.log(`Note: Failed to get session link: ${error}`);
    }

    // Use the UI module to take a screenshot
    console.log('\nTaking a screenshot...');
    try {
      const screenshotResponse = await session.ui.screenshot();
      console.log(`Screenshot data length: ${screenshotResponse.data.length} characters`);
      console.log(`Screenshot RequestId: ${screenshotResponse.requestId}`);
    } catch (error) {
      console.log(`Note: Failed to take screenshot: ${error}`);
    }

    // List all sessions by labels using new API
    console.log('\nListing sessions by labels...');
    try {
      const listParams: ListSessionParams = {
        labels: { test: 'basic-usage' },
        maxResults: 5
      };
      const listResponse = await agentBay.listByLabels(listParams);
      console.log(`Available sessions count: ${listResponse.data.length}`);
      console.log(`Total count: ${listResponse.totalCount}`);
      console.log(`Max results: ${listResponse.maxResults}`);
      console.log('Session IDs:', listResponse.data.map(s => s.sessionId));
      console.log(`List Sessions RequestId: ${listResponse.requestId}`);

      // Demonstrate pagination if there's a next token
      if (listResponse.nextToken) {
        console.log('\nFetching next page...');
        const nextPageParams: ListSessionParams = {
          ...listParams,
          nextToken: listResponse.nextToken
        };
        const nextPageResponse = await agentBay.listByLabels(nextPageParams);
        console.log(`Next page sessions count: ${nextPageResponse.data.length}`);
        console.log(`Next page RequestId: ${nextPageResponse.requestId}`);
      }
    } catch (error) {
      console.log(`Note: Failed to list sessions by labels: ${error}`);
    }

    // Delete the session
    console.log('\nDeleting the session...');
    const deleteResponse = await agentBay.delete(session);
    console.log('Session deleted successfully');
    console.log(`Delete Session RequestId: ${deleteResponse.requestId}`);

  } catch (error) {
    console.log('Error:', error);
    // In a Node.js environment, you would use process.exit(1) here
    throw error;
  }
}

main();
