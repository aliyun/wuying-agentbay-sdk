import { AgentBay, ListSessionParams } from '../src';
import { log, logError } from '../src/utils/logger';
import { getTestApiKey } from '../tests/utils/test-helpers';
async function main() {
  try {
    // Use the test API key function from test-helpers
    const apiKey = getTestApiKey();
    log('Using test API key for demonstration purposes.');

    // Initialize the AgentBay client
    const agentBay = new AgentBay({ apiKey });

    // Create a new session with labels
    log('Creating a new session with labels...');
    const createResponse = await agentBay.create({imageId:'linux_latest'});
    const session = createResponse.data;
    log(`Session created with ID: ${session.sessionId}`);
    log(`Create Session RequestId: ${createResponse.requestId}`);

    // Execute a command
    log('\nExecuting a command...');
    const commandResponse = await session.command.executeCommand('ls -la');
    log('Command result:', commandResponse.data);
    log(`Execute Command RequestId: ${commandResponse.requestId}`);

    // Read a file
    log('\nReading a file...');
    const fileResponse = await session.filesystem.readFile('/etc/hosts');
    log(`File content: ${fileResponse.data}`);
    log(`Read File RequestId: ${fileResponse.requestId}`);

    // Get the session link
    log('\nGetting session link...');
    try {
      const linkResponse = await session.getLink();
      log(`Session link: ${linkResponse.data}`);
      log(`Get Link RequestId: ${linkResponse.requestId}`);
    } catch (error) {
      log(`Note: Failed to get session link: ${error}`);
    }

    // Use the UI module to take a screenshot
    log('\nTaking a screenshot...');
    try {
      const screenshotResponse = await session.ui.screenshot();
      log(`Screenshot data length: ${screenshotResponse.data.length} characters`);
      log(`Screenshot RequestId: ${screenshotResponse.requestId}`);
    } catch (error) {
      log(`Note: Failed to take screenshot: ${error}`);
    }

    // List all sessions by labels using new API
    log('\nListing sessions by labels...');
    try {
      const listParams: ListSessionParams = {
        labels: { test: 'basic-usage' },
        maxResults: 5
      };
      const listResponse = await agentBay.listByLabels(listParams);
      log(`Available sessions count: ${listResponse.data.length}`);
      log(`Total count: ${listResponse.totalCount}`);
      log(`Max results: ${listResponse.maxResults}`);
      log('Session IDs:', listResponse.data.map(s => s.sessionId));
      log(`List Sessions RequestId: ${listResponse.requestId}`);

      // Demonstrate pagination if there's a next token
      if (listResponse.nextToken) {
        log('\nFetching next page...');
        const nextPageParams: ListSessionParams = {
          ...listParams,
          nextToken: listResponse.nextToken
        };
        const nextPageResponse = await agentBay.listByLabels(nextPageParams);
        log(`Next page sessions count: ${nextPageResponse.data.length}`);
        log(`Next page RequestId: ${nextPageResponse.requestId}`);
      }
    } catch (error) {
      log(`Note: Failed to list sessions by labels: ${error}`);
    }

    // Delete the session
    log('\nDeleting the session...');
    const deleteResponse = await agentBay.delete(session);
    log('Session deleted successfully');
    log(`Delete Session RequestId: ${deleteResponse.requestId}`);

  } catch (error) {
    logError('Error:', error);
    // In a Node.js environment, you would use process.exit(1) here
    throw error;
  }
}

main();
