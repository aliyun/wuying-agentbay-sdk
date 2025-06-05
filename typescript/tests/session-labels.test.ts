import { AgentBay, Session } from '../src';
import { expect } from 'chai';
import * as sinon from 'sinon';

describe('Session Labels', () => {
  let agentBay: AgentBay;
  let session: Session;
  let clientStub: any;
  
  beforeEach(() => {
    // Create a stub AgentBay instance
    agentBay = new AgentBay({ apiKey: 'test-api-key' });
    
    // Create a session
    session = new Session(agentBay, 'test-session-id');
    
    // Replace the client with a stub
    clientStub = {
      setLabel: sinon.stub(),
      getLabel: sinon.stub(),
      listSession: sinon.stub()
    };
    
    // @ts-ignore - Accessing private property for testing
    session.client = clientStub;
    // @ts-ignore - Accessing private property for testing
    agentBay.client = clientStub;
  });
  
  afterEach(() => {
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
      
      // Define labels to set
      const labels = {
        purpose: 'test',
        environment: 'development',
        version: '1.0'
      };
      
      // Call the method
      await session.setLabels(labels);
      
      // Verify the API was called correctly
      expect(clientStub.setLabel.calledOnce).to.be.true;
      const callArgs = clientStub.setLabel.firstCall.args[0];
      expect(callArgs.sessionId).to.equal('test-session-id');
      expect(callArgs.labels).to.equal(JSON.stringify(labels));
    });
    
    it('should handle errors', async () => {
      // Mock an error response
      clientStub.setLabel.rejects(new Error('API error'));
      
      // Define labels to set
      const labels = {
        purpose: 'test',
        environment: 'development'
      };
      
      // Call the method and expect it to throw
      try {
        await session.setLabels(labels);
        expect.fail('Should have thrown an error');
      } catch (error: any) {
        expect(error.message).to.include('Failed to set labels for session');
      }
    });
  });
  
  describe('getLabels()', () => {
    it('should get labels for a session', async () => {
      // Define labels to return
      const labels = {
        purpose: 'test',
        environment: 'development',
        version: '1.0'
      };
      
      // Mock the response from the API
      clientStub.getLabel.resolves({
        body: {
          data: {
            labels: JSON.stringify(labels)
          }
        }
      });
      
      // Call the method
      const result = await session.getLabels();
      
      // Verify the API was called correctly
      expect(clientStub.getLabel.calledOnce).to.be.true;
      const callArgs = clientStub.getLabel.firstCall.args[0];
      expect(callArgs.sessionId).to.equal('test-session-id');
      
      // Verify the results
      expect(result).to.deep.equal(labels);
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
      
      // Call the method
      const result = await session.getLabels();
      
      // Verify the results
      expect(result).to.deep.equal({});
    });
    
    it('should handle errors', async () => {
      // Mock an error response
      clientStub.getLabel.rejects(new Error('API error'));
      
      // Call the method and expect it to throw
      try {
        await session.getLabels();
        expect.fail('Should have thrown an error');
      } catch (error: any) {
        expect(error.message).to.include('Failed to get labels for session');
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
      
      // Define labels to filter by
      const labels = {
        purpose: 'test',
        environment: 'development'
      };
      
      // Call the method
      const sessions = await agentBay.listByLabels(labels);
      
      // Verify the API was called correctly
      expect(clientStub.listSession.calledOnce).to.be.true;
      const callArgs = clientStub.listSession.firstCall.args[0];
      expect(callArgs.labels).to.equal(JSON.stringify(labels));
      
      // Verify the results
      expect(sessions).to.have.lengthOf(2);
      expect(sessions[0].sessionId).to.equal('session-1');
      expect(sessions[1].sessionId).to.equal('session-2');
    });
    
    it('should handle empty response', async () => {
      // Mock the response from the API with no sessions
      clientStub.listSession.resolves({
        body: {
          data: []
        }
      });
      
      // Define labels to filter by
      const labels = {
        purpose: 'test',
        environment: 'production'
      };
      
      // Call the method
      const sessions = await agentBay.listByLabels(labels);
      
      // Verify the results
      expect(sessions).to.have.lengthOf(0);
    });
    
    it('should handle errors', async () => {
      // Mock an error response
      clientStub.listSession.rejects(new Error('API error'));
      
      // Define labels to filter by
      const labels = {
        purpose: 'test'
      };
      
      // Call the method and expect it to throw
      try {
        await agentBay.listByLabels(labels);
        expect.fail('Should have thrown an error');
      } catch (error: any) {
        expect(error.message).to.include('Failed to list sessions by labels');
      }
    });
  });
});
