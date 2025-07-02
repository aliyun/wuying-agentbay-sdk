import { AgentBay, ListSessionParams } from '../../src';
import { log, logError } from '../../src/utils/logger';
import { getTestApiKey } from '../../tests/utils/test-helpers';

/**
 * Label Management Example
 *
 * This example demonstrates how to use the label management features
 * of the Wuying AgentBay SDK.
 */

async function main() {
  try {
    // Get API key from environment variable or use a default value for testing
    const apiKey = getTestApiKey();

    // Initialize the AgentBay client
    const agentBay = new AgentBay({ apiKey });

    // Create a new session with labels
    log('\nCreating a new session with labels...');
    const createResponse1 = await agentBay.create({
      labels: {
        purpose: 'demo',
        feature: 'label-management',
        version: '1.0'
      }
    });
    const session1 = createResponse1.data;
    log(`Session created with ID: ${session1.sessionId}`);
    log(`Create Session 1 RequestId: ${createResponse1.requestId}`);

    // Get labels for the session
    log('\nGetting labels for the session...');
    const labelsResponse = await session1.getLabels();
    log(`Session labels: ${JSON.stringify(labelsResponse.data)}`);
    log(`Get Labels RequestId: ${labelsResponse.requestId}`);

    // Create another session with different labels
    log('\nCreating another session with different labels...');
    const createResponse2 = await agentBay.create({
      labels: {
        purpose: 'demo',
        feature: 'other-feature',
        version: '2.0'
      }
    });
    const session2 = createResponse2.data;
    log(`Session created with ID: ${session2.sessionId}`);
    log(`Create Session 2 RequestId: ${createResponse2.requestId}`);

    // Update labels for the second session
    log('\nUpdating labels for the second session...');
    const setLabelsResponse = await session2.setLabels({
      purpose: 'demo',
      feature: 'label-management',
      version: '2.0',
      status: 'active'
    });
    log(`Set Labels RequestId: ${setLabelsResponse.requestId}`);

    // Get updated labels for the second session
    log('\nGetting updated labels for the second session...');
    const updatedLabelsResponse = await session2.getLabels();
    log(`Updated session labels: ${JSON.stringify(updatedLabelsResponse.data)}`);
    log(`Get Updated Labels RequestId: ${updatedLabelsResponse.requestId}`);

    // List all sessions
    log('\nListing all sessions...');
    const allSessions = agentBay.list();
    log(`Found ${allSessions.length} sessions`);
    for (let i = 0; i < allSessions.length; i++) {
      log(`Session ${i + 1} ID: ${allSessions[i].sessionId}`);
    }

    // List sessions by label using new API
    log('\nListing sessions with purpose=demo and feature=label-management...');
    try {
      const listParams: ListSessionParams = {
        labels: {
          purpose: 'demo',
          feature: 'label-management'
        },
        maxResults: 1
      };

      const filteredSessionsResponse = await agentBay.listByLabels(listParams);
      log(`Found ${filteredSessionsResponse.data.length} matching sessions`);
      log(`Total count: ${filteredSessionsResponse.totalCount}`);
      log(`Max results: ${filteredSessionsResponse.maxResults}`);
      log(`List Sessions By Labels RequestId: ${filteredSessionsResponse.requestId}`);

      for (let i = 0; i < filteredSessionsResponse.data.length; i++) {
        log(`Matching session ${i + 1} ID: ${filteredSessionsResponse.data[i].sessionId}`);
        const sessionLabelsResponse = await filteredSessionsResponse.data[i].getLabels();
        log(`Labels: ${JSON.stringify(sessionLabelsResponse.data)}`);
        log(`Get Session Labels RequestId: ${sessionLabelsResponse.requestId}`);
      }

      // Demonstrate pagination if there's a next token
      if (filteredSessionsResponse.nextToken) {
        log('\nFetching next page...');
        const nextPageParams: ListSessionParams = {
          ...listParams,
          nextToken: filteredSessionsResponse.nextToken
        };
        const nextPageResponse = await agentBay.listByLabels(nextPageParams);
        log(`Next page sessions count: ${nextPageResponse.data.length}`);
        log(`Next page RequestId: ${nextPageResponse.requestId}`);
      }
    } catch (error) {
      log(`Error listing sessions by labels: ${error}`);
    }

    // Delete the sessions
    log('\nDeleting the sessions...');
    try {
      const deleteResponse1 = await agentBay.delete(session1);
      log(`Session ${session1.sessionId} deleted successfully`);
      log(`Delete Session 1 RequestId: ${deleteResponse1.requestId}`);

      const deleteResponse2 = await agentBay.delete(session2);
      log(`Session ${session2.sessionId} deleted successfully`);
      log(`Delete Session 2 RequestId: ${deleteResponse2.requestId}`);
    } catch (error) {
      log(`Error deleting sessions: ${error}`);
    }
  } catch (error) {
    logError(`Error: ${error}`);
    process.exit(1);
  }
}

main();
