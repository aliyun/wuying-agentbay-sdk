import { AgentBay, ListSessionParams } from '../../src';
import { log, logError } from '../../src/utils/logger';
import { getTestApiKey } from '../../tests/utils/test-helpers';

async function main() {
  // Get API key from environment variable or use default value for testing
  const apiKey = getTestApiKey();

  // Initialize the AgentBay client
  const agentBay = new AgentBay({ apiKey });

  // Example 1: Create a session with custom labels
  log('\nExample 1: Creating a session with custom labels...');

  // Create parameters with labels
  const params = {
    labels: {
      username: 'alice',
      project: 'my-project'
    }
  };

  const createResponse = await agentBay.create(params);
  const session = createResponse.session;
  log(`\nSession created with ID: ${session.sessionId} and labels: username=alice, project=my-project`);
  log(`Create Session RequestId: ${createResponse.requestId}`);

  // Example 2: List sessions by labels using new API
  log('\nExample 2: Listing sessions by labels...');

  // Query sessions with the "project" label set to "my-project" using new ListSessionParams format
  try {
    const listParams: ListSessionParams = {
      labels: { project: 'my-project' },
      maxResults: 5
    };

    const listResponse = await agentBay.listByLabels(listParams);

    log(`\nFound ${listResponse.data.length} sessions with project=my-project:`);
    log(`Total count: ${listResponse.totalCount}`);
    log(`Max results: ${listResponse.maxResults}`);
    log(`List Sessions RequestId: ${listResponse.requestId}`);
    listResponse.data.forEach((s, i) => {
      log(`  ${i + 1}. Session ID: ${s.sessionId}`);
    });

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
    log(`\nError listing sessions by labels: ${error}`);
  }

  // Clean up
  log('\nCleaning up sessions...');

  try {
    const deleteResponse = await agentBay.delete(session);
    log('Session deleted successfully');
    log(`Delete Session RequestId: ${deleteResponse.requestId}`);
  } catch (error) {
    log(`Error deleting session: ${error}`);
  }
}

main().catch(error => {
  logError('Error in main execution:', error);
  process.exit(1);
});
