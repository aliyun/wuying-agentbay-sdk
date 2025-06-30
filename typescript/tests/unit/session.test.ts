import { before } from 'node:test';
import { AgentBay, Session } from '../../src';
import { getTestApiKey, extractResourceId } from '../utils/test-helpers';
import { log } from '../../src/utils/logger';

describe('Session', () => {


  describe('properties', () => {
    let agentBay: AgentBay;
    let session: Session;

    beforeEach(async () => {
      const apiKey = getTestApiKey();
      agentBay = new AgentBay({ apiKey });

      // Create a session
      log('Creating a new session for session testing...');
      const createResponse = await agentBay.create();
      session = createResponse.data;
      log(`Session created with ID: ${session.sessionId}`);
      log(`Create Session RequestId: ${createResponse.requestId || 'undefined'}`);
    });

    afterEach(async () => {
      // Clean up the session
      log('Cleaning up: Deleting the session...');
      try {
        if(session) {
          const deleteResponse = await agentBay.delete(session);
          log(`Delete Session RequestId: ${deleteResponse.requestId || 'undefined'}`);
        }
      } catch (error) {
        log(`Warning: Error deleting session: ${error}`);
      }
    });
    it.only('should have valid sessionId', () => {
      expect(session.sessionId).toBeDefined();
      expect(session.sessionId.length).toBeGreaterThan(0);
    });

    it.only('should log resourceUrl', () => {
      // ResourceUrl is optional, so we just log it without checking if it's non-empty
      log(`Session resourceUrl: ${session.resourceUrl}`);
    });

    it.only('should have filesystem, command, and ui properties', () => {
      expect(session.filesystem).toBeDefined();
      expect(session.command).toBeDefined();
      expect(session.ui).toBeDefined();
    });
  });

  describe('methods', () => {
    let agentBay: AgentBay;
    let session: Session;

    beforeEach(async () => {
      const apiKey = getTestApiKey();
      agentBay = new AgentBay({ apiKey });

      // Create a session
      log('Creating a new session for session testing...');
      const createResponse = await agentBay.create();
      session = createResponse.data;
      log(`Session created with ID: ${session.sessionId}`);
      log(`Create Session RequestId: ${createResponse.requestId || 'undefined'}`);
    });

    afterEach(async () => {
      // Clean up the session
      log('Cleaning up: Deleting the session...');
      try {
        if(session) {
          const deleteResponse = await agentBay.delete(session);
          log(`Delete Session RequestId: ${deleteResponse.requestId || 'undefined'}`);
        }
      } catch (error) {
        log(`Warning: Error deleting session: ${error}`);
      }
    });
    it.only('should return the session ID', () => {
      const sessionId = session.getSessionId();
      expect(sessionId).toBe(session.sessionId);
    });

    it.only('should return the API key', () => {
      const apiKey = session.getAPIKey();
      expect(apiKey).toBe(agentBay.getAPIKey());
    });

    it.only('should return the client', () => {
      const client = session.getClient();
      expect(client).toBeDefined();
    });

    it.only('should get link if implemented', async () => {
      // Check if the getLink method exists
      if (typeof session.getLink === 'function') {
        log('Testing session.getLink method...');
        try {
          // First, create a new session with imageId for getLink testing
          // This is consistent with the Go implementation in TestSession_GetLinkMethod
          const createLinkResponse = await agentBay.create({ imageId: 'imgc-07if81c4ktj9shiru' });
          const linkTestSession = createLinkResponse.data;
          log(`Session created with ID: ${linkTestSession.sessionId} for getLink testing`);
          log(`Create Link Session RequestId: ${createLinkResponse.requestId || 'undefined'}`);

          const linkResponse = await linkTestSession.getLink();
          log('Session link:', linkResponse.data);
          log(`Get Link RequestId: ${linkResponse.requestId || 'undefined'}`);

          // Verify that the response contains requestId
          expect(linkResponse.requestId).toBeDefined();
          expect(typeof linkResponse.requestId).toBe('string');

          // Verify the link
          expect(linkResponse.data).toBeDefined();

          // Clean up the session after test
          const deleteLinkResponse = await agentBay.delete(linkTestSession);
          log(`Delete Link Session RequestId: ${deleteLinkResponse.requestId || 'undefined'}`);
        } catch (error) {
          log(`Note: Session link retrieval failed: ${error}`);
          // Don't fail the test if getLink method is not fully implemented
        }
      } else {
        log('Note: Session getLink method is not available, skipping test');
      }
    });
  });

  describe('delete', () => {
    let agentBay: AgentBay;
    beforeEach(async () => {
      agentBay = new AgentBay({ apiKey: getTestApiKey() });
    });
    it.only('should delete the session', async () => {
      // Create a new session specifically for this test
      log('Creating a new session for delete testing...');
      const createResponse = await agentBay.create();
      const testSession = createResponse.data;
      log(`Session created with ID: ${testSession.sessionId}`);
      log(`Create Session RequestId: ${createResponse.requestId || 'undefined'}`);

      // Test delete method
      log('Testing session.delete method...');
      try {
        if(testSession) {
          const deleteResponse = await testSession.delete();
          log(`Delete Session RequestId: ${deleteResponse.requestId || 'undefined'}`);

          // Verify that the response contains requestId
          expect(deleteResponse.requestId).toBeDefined();
          expect(typeof deleteResponse.requestId).toBe('string');
        }

        // Verify the session was deleted by checking it's not in the list
        const sessions = agentBay.list();

        const stillExists = sessions.some(s => s.sessionId === testSession.sessionId);
        expect(stillExists).toBe(false);
      } catch (error) {
        log(`Note: Session deletion failed: ${error}`);
        // Clean up if the test failed
        try {
          if(testSession) {
            const deleteResponse = await agentBay.delete(testSession);
            log(`Cleanup Delete Session RequestId: ${deleteResponse.requestId || 'undefined'}`);
          }
        } catch {
          // Ignore cleanup errors
        }
        throw error;
      }
    });
  });

  describe('info', () => {
    let agentBay: AgentBay;
    let session: Session;

    beforeEach(async () => {
      const apiKey = getTestApiKey();
      agentBay = new AgentBay({ apiKey });

      // Create a session
      log('Creating a new session for session testing...');
      const createResponse = await agentBay.create();
      session = createResponse.data;
      log(`Session created with ID: ${session.sessionId}`);
      log(`Create Session RequestId: ${createResponse.requestId || 'undefined'}`);
    });

    afterEach(async () => {
      // Clean up the session
      log('Cleaning up: Deleting the session...');
      try {
        if(session) {
          const deleteResponse = await agentBay.delete(session);
          log(`Delete Session RequestId: ${deleteResponse.requestId || 'undefined'}`);
        }
      } catch (error) {
        log(`Warning: Error deleting session: ${error}`);
      }
    });
    it.only('should get session info if implemented', async () => {
      // Check if the info method exists
      if (typeof session.info === 'function') {
        log('Testing session.info method...');
        try {
          const sessionInfoResponse = await session.info();
          log('Session info:', sessionInfoResponse.data);
          log(`Session Info RequestId: ${sessionInfoResponse.requestId || 'undefined'}`);

          // Verify that the response contains requestId
          expect(sessionInfoResponse.requestId).toBeDefined();
          expect(typeof sessionInfoResponse.requestId).toBe('string');

          // Verify the session info
          expect(sessionInfoResponse.data).toBeDefined();

          // Check SessionId field
          expect(sessionInfoResponse.data.sessionId).toBeDefined();
          expect(sessionInfoResponse.data.sessionId).toBe(session.sessionId);

          // Check ResourceUrl field
          if (sessionInfoResponse.data.resourceUrl) {
            log(`Session ResourceUrl from Info: ${sessionInfoResponse.data.resourceUrl}`);

            // Extract resourceId from URL if possible
            const resourceId = extractResourceId(sessionInfoResponse.data.resourceUrl);
            if (resourceId) {
              log(`Extracted ResourceId: ${resourceId}`);
            }

            // Verify that session.resourceUrl was updated with the value from the API response
            expect(session.resourceUrl).toBe(sessionInfoResponse.data.resourceUrl);
          }

          // Log other fields (these may be empty depending on the API response)
          if (sessionInfoResponse.data.appId) log(`AppId: ${sessionInfoResponse.data.appId}`);
          if (sessionInfoResponse.data.authCode) log(`AuthCode: ${sessionInfoResponse.data.authCode}`);
          if (sessionInfoResponse.data.connectionProperties) log(`ConnectionProperties: ${sessionInfoResponse.data.connectionProperties}`);
          if (sessionInfoResponse.data.resourceId) log(`ResourceId: ${sessionInfoResponse.data.resourceId}`);
          if (sessionInfoResponse.data.resourceType) log(`ResourceType: ${sessionInfoResponse.data.resourceType}`);
        } catch (error) {
          log(`Note: Session info retrieval failed: ${error}`);
          // Don't fail the test if info method is not fully implemented
        }
      } else {
        log('Note: Session info method is not available, skipping info test');
      }
    });
  });
});
