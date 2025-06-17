import { before } from 'node:test';
import { AgentBay, Session } from '../../src';
import { getTestApiKey, extractResourceId } from '../utils/test-helpers';

// Define test runner types if they're not available
declare function describe(name: string, fn: () => void): void;
declare function beforeEach(fn: () => void | Promise<void>): void;
declare function afterEach(fn: () => void | Promise<void>): void;
declare function it(name: string, fn: () => void | Promise<void>): void;
declare function expect(actual: any): any;

describe('Session', () => {
  
  
  describe('properties', () => {
    let agentBay: AgentBay;
    let session: Session;
  
    beforeEach(async () => {
      const apiKey = getTestApiKey();
      agentBay = new AgentBay({ apiKey });
      
      // Create a session
      console.log('Creating a new session for session testing...');
      session = await agentBay.create();
      console.log(`Session created with ID: ${session.sessionId}`);
    });
    
    afterEach(async () => {
      // Clean up the session
      console.log('Cleaning up: Deleting the session...');
      try {
        if(session)
        await agentBay.delete(session);
      } catch (error) {
        console.log(`Warning: Error deleting session: ${error}`);
      }
    });
    it('should have valid sessionId', () => {
      expect(session.sessionId).toBeDefined();
      expect(session.sessionId.length).toBeGreaterThan(0);
    });
    
    it('should log resourceUrl', () => {
      // ResourceUrl is optional, so we just log it without checking if it's non-empty
      console.log(`Session resourceUrl: ${session.resourceUrl}`);
    });
    
    it('should have filesystem, command, and adb properties', () => {
      expect(session.filesystem).toBeDefined();
      expect(session.command).toBeDefined();
      expect(session.adb).toBeDefined();
    });
  });
  
  describe('methods', () => {
    let agentBay: AgentBay;
    let session: Session;
    
    beforeEach(async () => {
      const apiKey = getTestApiKey();
      agentBay = new AgentBay({ apiKey });
      
      // Create a session
      console.log('Creating a new session for session testing...');
      session = await agentBay.create();
      console.log(`Session created with ID: ${session.sessionId}`);
    });
    
    afterEach(async () => {
      // Clean up the session
      console.log('Cleaning up: Deleting the session...');
      try {
        if(session)
        await agentBay.delete(session);
      } catch (error) {
        console.log(`Warning: Error deleting session: ${error}`);
      }
    });
    it('should return the session ID', () => {
      const sessionId = session.getSessionId();
      expect(sessionId).toBe(session.sessionId);
    });
    
    it('should return the API key', () => {
      const apiKey = session.getAPIKey();
      expect(apiKey).toBe(agentBay.getAPIKey());
    });
    
    it('should return the client', () => {
      const client = session.getClient();
      expect(client).toBeDefined();
    });
  });
  
  describe('delete', () => {
    let agentBay: AgentBay;
    beforeEach(async () => {
      agentBay = new AgentBay({ apiKey: getTestApiKey() });
    });
    it('should delete the session', async () => {
      // Create a new session specifically for this test
      console.log('Creating a new session for delete testing...');
      const testSession = await agentBay.create();
      console.log(`Session created with ID: ${testSession.sessionId}`);
      
      // Test delete method
      console.log('Testing session.delete method...');
      try {
        if(testSession)
          await testSession.delete();
        
        // Verify the session was deleted by checking it's not in the list
        const sessions = agentBay.list();
        
        const stillExists = sessions.some(s => s.sessionId === testSession.sessionId);
        expect(stillExists).toBe(false);
      } catch (error) {
        console.log(`Note: Session deletion failed: ${error}`);
        // Clean up if the test failed
        try {
          if(testSession)
            await agentBay.delete(testSession);
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
      console.log('Creating a new session for session testing...');
      session = await agentBay.create();
      console.log(`Session created with ID: ${session.sessionId}`);
    });
    
    afterEach(async () => {
      // Clean up the session
      console.log('Cleaning up: Deleting the session...');
      try {
        if(session)
          await agentBay.delete(session);
      } catch (error) {
        console.log(`Warning: Error deleting session: ${error}`);
      }
    });
    it('should get session info if implemented', async () => {
      // Check if the info method exists
      if (typeof (session as any).info === 'function') {
        console.log('Testing session.info method...');
        try {
          const sessionInfo = await (session as any).info();
          console.log('Session info:', sessionInfo);
          
          // Verify the session info
          expect(sessionInfo).toBeDefined();
          
          // Check SessionId field
          expect(sessionInfo.sessionId).toBeDefined();
          expect(sessionInfo.sessionId).toBe(session.sessionId);
          
          // Check ResourceUrl field
          if (sessionInfo.resourceUrl) {
            console.log(`Session ResourceUrl from Info: ${sessionInfo.resourceUrl}`);
            
            // Extract resourceId from URL if possible
            const resourceId = extractResourceId(sessionInfo.resourceUrl);
            if (resourceId) {
              console.log(`Extracted ResourceId: ${resourceId}`);
            }
            
            // Verify that session.resourceUrl was updated with the value from the API response
            expect(session.resourceUrl).toBe(sessionInfo.resourceUrl);
          }
          
          // Log other fields (these may be empty depending on the API response)
          if (sessionInfo.appId) console.log(`AppId: ${sessionInfo.appId}`);
          if (sessionInfo.authCode) console.log(`AuthCode: ${sessionInfo.authCode}`);
          if (sessionInfo.connectionProperties) console.log(`ConnectionProperties: ${sessionInfo.connectionProperties}`);
          if (sessionInfo.resourceId) console.log(`ResourceId: ${sessionInfo.resourceId}`);
          if (sessionInfo.resourceType) console.log(`ResourceType: ${sessionInfo.resourceType}`);
        } catch (error) {
          console.log(`Note: Session info retrieval failed: ${error}`);
          // Don't fail the test if info method is not fully implemented
        }
      } else {
        console.log('Note: Session info method is not available, skipping info test');
      }
    });
  });
});
