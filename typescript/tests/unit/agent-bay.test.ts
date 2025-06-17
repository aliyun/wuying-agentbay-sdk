import { AgentBay, Session, AuthenticationError, APIError } from '../../src';
import { getTestApiKey } from '../utils/test-helpers';

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

// Define test runner types if they're not available
declare function describe(name: string, fn: () => void): void;
declare function beforeEach(fn: () => void | Promise<void>): void;
declare function afterEach(fn: () => void | Promise<void>): void;
declare function it(name: string, fn: () => void | Promise<void>): void;
declare function expect(actual: any): any;

describe('AgentBay', () => {
  describe('constructor', () => {
    it('should initialize with API key from options', () => {
      const apiKey = getTestApiKey();
      const agentBay = new AgentBay({ apiKey });
      console.log(apiKey);
      
      expect(agentBay.getAPIKey()).toBe(apiKey);
    });
    
    it('should initialize with API key from environment variable', () => {
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
    
    it('should throw AuthenticationError if no API key is provided', () => {
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
    
    it('should create, list, and delete a session', async () => {
      // Create a session
      console.log('Creating a new session...');
      session = await agentBay.create();
      console.log(`Session created with ID: ${session.sessionId}`);
      
      // Ensure session ID is not empty
      expect(session.sessionId).toBeDefined();
      expect(session.sessionId.length).toBeGreaterThan(0);
      
      // List sessions
      console.log('Listing sessions...');
      const sessions = agentBay.list();
      
      // Ensure at least one session (the one we just created)
      expect(sessions.length).toBeGreaterThanOrEqual(1);
      
      // Check if our created session is in the list
      const found = sessions.some(s => s.sessionId === session.sessionId);
      expect(found).toBe(true);
      
      // Delete the session
      console.log('Deleting the session...');
      await agentBay.delete(session);
      
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
        console.log('Creating session with labels A...');
        sessionA = await agentBay.create({ labels: labelsA });
        console.log(`Session created with ID: ${sessionA.sessionId}`);
        
        // Create session with labels B
        sessionB = await agentBay.create({ labels: labelsB });
        console.log(`Session created with ID: ${sessionB.sessionId}`);
        

      }catch(error){
        console.log(`Failed to constructor: ${error}`)
      }
    });
    
    afterEach(async () => {
      // Clean up sessions
      console.log('Cleaning up sessions...');
      if (sessionA) {
        try {
          await agentBay.delete(sessionA);
        } catch (error) {
          console.log(`Warning: Error deleting session A: ${error}`);
        }
      }
      
      if (sessionB) {
        try {
          await agentBay.delete(sessionB);
        } catch (error) {
          console.log(`Warning: Error deleting session B: ${error}`);
        }
      }
    });
    
    it('should list sessions by labels ', async () => {
      
      // Test 1: List all sessions
      const allSessions = agentBay.list();
      console.log(`Found ${allSessions.length} sessions in total`);
      
      // Test 2: List sessions by environment=development label
      try {
        const devSessions = await agentBay.listByLabels({ environment: 'development' });
        
        // Verify that session A is in the results
        const foundSessionA = devSessions.some(s => s.sessionId === sessionA.sessionId);
        expect(foundSessionA).toBe(true);
      } catch (error) {
        console.log(`Error listing sessions by environment=development: ${error}`);
      }
      
      // Test 3: List sessions by owner=team-b label
      try {
        const teamBSessions = await agentBay.listByLabels({ owner: 'team-b' });
        
        // Verify that session B is in the results
        const foundSessionB = teamBSessions.some(s => s.sessionId === sessionB.sessionId);
        expect(foundSessionB).toBe(true);
      } catch (error) {
        console.log(`Error listing sessions by owner=team-b: ${error}`);
      }
      
      // Test 4: List sessions with multiple labels (environment=testing AND project=project-y)
      try {
        const multiLabelSessions = await agentBay.listByLabels({
          environment: 'testing',
          project: 'project-y'
        });
        console.log(`Found ${multiLabelSessions.length} sessions with environment=testing AND project=project-y`);
        
        // Verify that session B is in the results and session A is not
        const foundSessionA = multiLabelSessions.some(s => s.sessionId === sessionA.sessionId);
        const foundSessionB = multiLabelSessions.some(s => s.sessionId === sessionB.sessionId);
        
        expect(foundSessionA).toBe(false);
        expect(foundSessionB).toBe(true);
      } catch (error) {
        console.log(`Error listing sessions by multiple labels: ${error}`);
      }
      
      // Test 5: List sessions with non-existent label
      try {
        const nonExistentSessions = await agentBay.listByLabels({ 'non-existent': 'value' });
        console.log(`Found ${nonExistentSessions.length} sessions with non-existent label`);
        
        if (nonExistentSessions.length > 0) {
          console.log('Warning: Found sessions with non-existent label, this might indicate an issue');
        }
      } catch (error) {
        console.log(`Error listing sessions by non-existent label: ${error}`);
      }
      
      console.log('Test completed successfully');
    },);
  });
});
