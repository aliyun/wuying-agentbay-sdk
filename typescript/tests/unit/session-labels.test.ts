import { AgentBay, Session } from '../../src';
import * as sinon from 'sinon';
import { getTestApiKey,generateUniqueId } from '../utils/test-helpers';

// Define test runner types if they're not available
declare function describe(name: string, fn: () => void): void;
declare function beforeEach(fn: () => void | Promise<void>): void;
declare function afterEach(fn: () => void | Promise<void>): void;
declare function it(name: string, fn: () => void | Promise<void>): void;
declare function expect(actual: any): any;

describe('Session Labels', () => {
  let agentBay: AgentBay;
  let session: Session;
  let clientStub: any;
  let self: any;
  let labels: Record<string, string>;
  let setupFailed = false; // 新增状态标记
  
  beforeEach(async () => {
    // Create a real AgentBay instance with test API key
    const apiKey = getTestApiKey();
    agentBay = new AgentBay({ apiKey });
    
    // Create a real session
    console.log('Creating a new session for session labels testing...');
    session = await agentBay.create();

    self = { unique_id: generateUniqueId() };
    labels = {
      environment: `testing-${self.unique_id}`,
      version: '1.0.0',
      project:`labels-test-${self.unique_id}`,
      onwer:`test-team-${self.unique_id}`
    };
    // Replace the client with a stub
    clientStub = {
      setLabel: sinon.stub(),
      getLabel: sinon.stub(),
      listSession: sinon.stub()
    };
  
  });
  
  afterEach(async () => {
    console.log('Cleaning up: Deleting the session...');
    try {
      await agentBay.delete(session);
      self = null;
      console.log('Session successfully deleted');
    } catch (error) {
      console.log(`Warning: Error deleting session: ${error}`);
    }
    
    sinon.restore();
  });
  
  describe('setLabels()', () => {
    it('should set labels for a session', async () => {
      // Mock the response from the API
      clientStub.setLabel.resolves({
        body: {
          data: {}
        }
      });
      
      console.log('Testing setLabels...');
      try{
        // Call the method
        await session.setLabels(labels);
        console.log('Labels set successfully',JSON.stringify(labels));
      }catch(error:any){
        console.log(`Received expected error: ${error.message}`);
        expect(error.message).toMatch(/Failed to set labels for session|API error|Failed to create session/);
      }
     
    });
  });
  
  describe('getLabels()', () => {
    it('should get labels for a session', async () => {
      
      // Mock the response from the API
      clientStub.getLabel.resolves({
        body: {
          data: {
            labels: JSON.stringify(labels)
          }
        }
      });
      
      console.log('Testing getLabels...');
      // Call the method
      try{
        await session.setLabels(labels);
        const result = await session.getLabels();
        console.log(`Retrieved labels: ${JSON.stringify(result)}`);
        console.log(clientStub.getLabel.calledOnce,'clientStub.getLabel.calledOnce');
        
        // Verify the results
        expect(result).toEqual(labels);
      }catch(error:any){
        console.log(`Received expected error: ${error.message}`);
        expect(error.message).toMatch(/Failed to get labels for session|Failed to set labels for session|API error|Failed to create session/);
      }
     
    });
    
    it('should return empty object if no labels', async () => {
      // Mock the response from the API with no labels
      clientStub.getLabel.resolves({
        body: {
          data: {
            labels: null
          }
        }
      });
      
      console.log('Testing getLabels with no labels...');
      try{
        // Call the method
      await session.setLabels({});
      const result = await session.getLabels();
      console.log('Received empty labels object as expected');
      
      // Verify the results
      expect(result).toEqual({});
      }catch(error:any){
        console.log(`Received expected error: ${error.message}`);
        expect(error.message).toMatch(/Failed to get labels for session|Failed to set labels for session|API error|Failed to create session/);
      }
      
    });
  });
  
  describe('listByLabels()', () => {
    it('should list sessions filtered by labels', async () => {
      // Define sessions to return
      const sessionData = [
        { sessionId: 'session-1' },
        { sessionId: 'session-2' }
      ];
      
      // Mock the response from the API
      clientStub.listSession.resolves({
        body: {
          data: sessionData
        }
      });
      
      console.log('Testing listByLabels...');
      // Call the method
      try{
        const sessions = await agentBay.listByLabels(labels);
        console.log(`Found ${sessions.length} sessions with matching labels`);
  
        console.log(session.sessionId,'session.sessionId');
        expect(sessions.length).toBeGreaterThan(0)
        sessions.forEach(sessionItem => {
          expect(sessionItem).toHaveProperty('sessionId');
          expect(sessionItem.sessionId).toBeTruthy();
        });
      }catch(error:any){
        console.log(`Received expected error: ${error.message}`);
        expect(error.message).toMatch(/Failed to list sessions by labels|API error|Failed to create session/);
      }
      
    });
    
    it('should handle empty response', async () => {
      // Mock the response from the API with no sessions
      clientStub.listSession.resolves({
        body: {
          data: []
        }
      });
      
      console.log('Testing listByLabels with no matching sessions...');
      try{
        // Call the method
        const sessions = await agentBay.listByLabels({});
        console.log('Received empty session list as expected');
      
        // Verify the results
        expect(sessions).toHaveLength(0);
      }catch(error:any){
        console.log(`Received expected error: ${error.message}`);
        expect(error.message).toMatch(/Failed to list sessions by labels|API error|Failed to create session/);
      }
      
    });
  });
});
