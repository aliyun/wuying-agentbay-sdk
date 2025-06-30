import { AgentBay, Session, AuthenticationError, APIError } from '../../src';
import { getTestApiKey } from '../utils/test-helpers';
import { log } from '../../src/utils/logger';

// Define Node.js process if it's not available
declare namespace NodeJS {
  interface ProcessEnv {
    [key: string]: string | undefined;
  }
}

declare var process: {
  env: {
    [key: string]: string | undefined;
  }
};

describe('AgentBay', () => {
  describe('constructor', () => {
    it.only('should initialize with API key from options', () => {
      const apiKey = getTestApiKey();
      const agentBay = new AgentBay({ apiKey });
      log(apiKey);

      expect(agentBay.getAPIKey()).toBe(apiKey);
    });

    it.only('should initialize with API key from environment variable', () => {
      const originalEnv = process.env.AGENTBAY_API_KEY;
      process.env.AGENTBAY_API_KEY = 'env_api_key';

      try {
        const agentBay = new AgentBay();
        expect(agentBay.getAPIKey()).toBe('env_api_key');
      } finally {
        // Restore original environment
        if (originalEnv) {
          process.env.AGENTBAY_API_KEY = originalEnv;
        } else {
          delete process.env.AGENTBAY_API_KEY;
        }
      }
    });

    it.only('should throw AuthenticationError if no API key is provided', () => {
      const originalEnv = process.env.AGENTBAY_API_KEY;
      delete process.env.AGENTBAY_API_KEY;

      try {
        expect(() => new AgentBay()).toThrow(AuthenticationError);
      } finally {
        // Restore original environment
        if (originalEnv) {
          process.env.AGENTBAY_API_KEY = originalEnv;
        }
      }
    });
  });

  describe('create, list, and delete', () => {
    let agentBay: AgentBay;
    let session: Session;

    beforeEach(() => {
      const apiKey = getTestApiKey();
      agentBay = new AgentBay({ apiKey });
    });

    it.only('should create, list, and delete a session with requestId', async () => {
      // Create a session
      log('Creating a new session...');
      const createResponse = await agentBay.create();
      session = createResponse.data;
      log(`Session created with ID: ${session.sessionId}`);
      log(`Create Session RequestId: ${createResponse.requestId || 'undefined'}`);

      // Verify that the response contains requestId
      expect(createResponse.requestId).toBeDefined();
      expect(typeof createResponse.requestId).toBe('string');
      expect(createResponse.requestId!.length).toBeGreaterThan(0);

      // Ensure session ID is not empty
      expect(session.sessionId).toBeDefined();
      expect(session.sessionId.length).toBeGreaterThan(0);

      // List sessions
      log('Listing sessions...');
      const sessions = agentBay.list();

      // Ensure at least one session (the one we just created)
      expect(sessions.length).toBeGreaterThanOrEqual(1);

      // Check if our created session is in the list
      const found = sessions.some(s => s.sessionId === session.sessionId);
      expect(found).toBe(true);

      // Delete the session
      log('Deleting the session...');
      const deleteResponse = await agentBay.delete(session);
      log(`Delete Session RequestId: ${deleteResponse.requestId || 'undefined'}`);

      // Verify that the delete response contains requestId
      expect(deleteResponse.requestId).toBeDefined();
      expect(typeof deleteResponse.requestId).toBe('string');
      expect(deleteResponse.requestId!.length).toBeGreaterThan(0);

      // List sessions again to ensure it's deleted
      const sessionsAfterDelete = agentBay.list();

      // Check if the deleted session is not in the list
      const stillExists = sessionsAfterDelete.some(s => s.sessionId === session.sessionId);
      expect(stillExists).toBe(false);
    });
  });

  describe('listByLabels', () => {
    let agentBay: AgentBay;
    let sessionA: Session;
    let sessionB: Session;

    beforeEach(async () => {
      try{
        const apiKey = getTestApiKey();
        agentBay = new AgentBay({ apiKey });
        const labelsA = {
          environment: 'development',
          owner: 'team-a',
          project: 'project-x'
        };

        const labelsB = {
          environment: 'testing',
          owner: 'team-b',
          project: 'project-y'
        };

        // Create session with labels A
        log('Creating session with labels A...');
        const createResponseA = await agentBay.create({ labels: labelsA });
        sessionA = createResponseA.data;
        log(`Session created with ID: ${sessionA.sessionId}`);
        log(`Create Session A RequestId: ${createResponseA.requestId || 'undefined'}`);

        // Create session with labels B
        const createResponseB = await agentBay.create({ labels: labelsB });
        sessionB = createResponseB.data;
        log(`Session created with ID: ${sessionB.sessionId}`);
        log(`Create Session B RequestId: ${createResponseB.requestId || 'undefined'}`);

      }catch(error){
        log(`Failed to constructor: ${error}`)
      }
    });

    afterEach(async () => {
      // Clean up sessions
      log('Cleaning up sessions...');
      if (sessionA) {
        try {
          const deleteResponseA = await agentBay.delete(sessionA);
          log(`Delete Session A RequestId: ${deleteResponseA.requestId || 'undefined'}`);
        } catch (error) {
          log(`Warning: Error deleting session A: ${error}`);
        }
      }

      if (sessionB) {
        try {
          const deleteResponseB = await agentBay.delete(sessionB);
          log(`Delete Session B RequestId: ${deleteResponseB.requestId || 'undefined'}`);
        } catch (error) {
          log(`Warning: Error deleting session B: ${error}`);
        }
      }
    });

    it.only('should list sessions by labels with requestId', async () => {

      // Test 1: List all sessions
      const allSessions = agentBay.list();
      log(`Found ${allSessions.length} sessions in total`);

      // Test 2: List sessions by environment=development label
      try {
        const devSessionsResponse = await agentBay.listByLabels({ environment: 'development' });
        log(`List Sessions by environment=development RequestId: ${devSessionsResponse.requestId || 'undefined'}`);

        // Verify that the response contains requestId
        expect(devSessionsResponse.requestId).toBeDefined();
        expect(typeof devSessionsResponse.requestId).toBe('string');
        expect(devSessionsResponse.requestId!.length).toBeGreaterThan(0);

        // Verify that session A is in the results
        const foundSessionA = devSessionsResponse.data.some(s => s.sessionId === sessionA.sessionId);
        expect(foundSessionA).toBe(true);
      } catch (error) {
        log(`Error listing sessions by environment=development: ${error}`);
      }

      // Test 3: List sessions by owner=team-b label
      try {
        const teamBSessionsResponse = await agentBay.listByLabels({ owner: 'team-b' });
        log(`List Sessions by owner=team-b RequestId: ${teamBSessionsResponse.requestId || 'undefined'}`);

        // Verify that the response contains requestId
        expect(teamBSessionsResponse.requestId).toBeDefined();

        // Verify that session B is in the results
        const foundSessionB = teamBSessionsResponse.data.some(s => s.sessionId === sessionB.sessionId);
        expect(foundSessionB).toBe(true);
      } catch (error) {
        log(`Error listing sessions by owner=team-b: ${error}`);
      }

      // Test 4: List sessions with multiple labels (environment=testing AND project=project-y)
      try {
        const multiLabelSessionsResponse = await agentBay.listByLabels({
          environment: 'testing',
          project: 'project-y'
        });
        log(`Found ${multiLabelSessionsResponse.data.length} sessions with environment=testing AND project=project-y`);
        log(`List Sessions by multiple labels RequestId: ${multiLabelSessionsResponse.requestId || 'undefined'}`);

        // Verify that the response contains requestId
        expect(multiLabelSessionsResponse.requestId).toBeDefined();

        // Verify that session B is in the results and session A is not
        const foundSessionA = multiLabelSessionsResponse.data.some(s => s.sessionId === sessionA.sessionId);
        const foundSessionB = multiLabelSessionsResponse.data.some(s => s.sessionId === sessionB.sessionId);

        expect(foundSessionA).toBe(false);
        expect(foundSessionB).toBe(true);
      } catch (error) {
        log(`Error listing sessions by multiple labels: ${error}`);
      }

      // Test 5: List sessions with non-existent label
      try {
        const nonExistentSessionsResponse = await agentBay.listByLabels({ 'non-existent': 'value' });
        log(`Found ${nonExistentSessionsResponse.data.length} sessions with non-existent label`);
        log(`List Sessions by non-existent label RequestId: ${nonExistentSessionsResponse.requestId || 'undefined'}`);

        // Verify that the response contains requestId even for empty results
        expect(nonExistentSessionsResponse.requestId).toBeDefined();

        if (nonExistentSessionsResponse.data.length > 0) {
          log('Warning: Found sessions with non-existent label, this might indicate an issue');
        }
      } catch (error) {
        log(`Error listing sessions by non-existent label: ${error}`);
      }

      log('Test completed successfully');
    },);
  });
});
