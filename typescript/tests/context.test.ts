import { AgentBay, Context, ContextService } from '../src';
import { expect } from 'chai';
import * as sinon from 'sinon';

describe('Context', () => {
  it('should initialize with the correct attributes', () => {
    const context = new Context(
      'test-id',
      'test-context',
      'available',
      '2025-05-29T12:00:00Z',
      '2025-05-29T12:30:00Z',
      'linux'
    );
    
    expect(context.id).to.equal('test-id');
    expect(context.name).to.equal('test-context');
    expect(context.state).to.equal('available');
    expect(context.createdAt).to.equal('2025-05-29T12:00:00Z');
    expect(context.lastUsedAt).to.equal('2025-05-29T12:30:00Z');
    expect(context.osType).to.equal('linux');
  });
});

describe('ContextService', () => {
  let agentBay: AgentBay;
  let contextService: ContextService;
  let clientStub: any;
  
  beforeEach(() => {
    // Create a stub AgentBay instance
    agentBay = new AgentBay({ apiKey: 'test-api-key' });
    
    // Replace the client with a stub
    clientStub = {
      listContexts: sinon.stub(),
      getContext: sinon.stub(),
      modifyContext: sinon.stub(),
      deleteContext: sinon.stub()
    };
    
    // @ts-ignore - Accessing private property for testing
    agentBay.getClient = () => clientStub;
    
    contextService = new ContextService(agentBay);
  });
  
  afterEach(() => {
    sinon.restore();
  });
  
  describe('list()', () => {
    it('should return a list of contexts', async () => {
      // Mock the response from the API
      clientStub.listContexts.resolves({
        body: {
          data: [
            {
              id: 'context-1',
              name: 'context-1-name',
              state: 'available',
              createTime: '2025-05-29T12:00:00Z',
              lastUsedTime: '2025-05-29T12:30:00Z',
              osType: 'linux'
            },
            {
              id: 'context-2',
              name: 'context-2-name',
              state: 'in-use',
              createTime: '2025-05-29T13:00:00Z',
              lastUsedTime: '2025-05-29T13:30:00Z',
              osType: 'windows'
            }
          ]
        }
      });
      
      // Call the method
      const contexts = await contextService.list();
      
      // Verify the results
      expect(contexts).to.have.lengthOf(2);
      expect(contexts[0].id).to.equal('context-1');
      expect(contexts[0].name).to.equal('context-1-name');
      expect(contexts[0].state).to.equal('available');
      expect(contexts[1].id).to.equal('context-2');
      expect(contexts[1].name).to.equal('context-2-name');
      expect(contexts[1].state).to.equal('in-use');
    });
    
    it('should handle empty response', async () => {
      // Mock the response from the API
      clientStub.listContexts.resolves({
        body: {
          data: []
        }
      });
      
      // Call the method
      const contexts = await contextService.list();
      
      // Verify the results
      expect(contexts).to.have.lengthOf(0);
    });
    
    it('should handle errors', async () => {
      // Mock an error response
      clientStub.listContexts.rejects(new Error('API error'));
      
      // Call the method and expect it to throw
      try {
        await contextService.list();
        expect.fail('Should have thrown an error');
      } catch (error: any) {
        expect(error.message).to.include('Failed to list contexts');
      }
    });
  });
  
  describe('get()', () => {
    it('should get a context by name', async () => {
      // Mock the getContext response
      clientStub.getContext.resolves({
        body: {
          data: {
            id: 'context-1'
          }
        }
      });
      
      // Mock the listContexts response to get full context details
      clientStub.listContexts.resolves({
        body: {
          data: [
            {
              id: 'context-1',
              name: 'test-context',
              state: 'available',
              createTime: '2025-05-29T12:00:00Z',
              lastUsedTime: '2025-05-29T12:30:00Z',
              osType: 'linux'
            }
          ]
        }
      });
      
      // Call the method
      const context = await contextService.get('test-context');
      
      // Verify the results
      expect(context).to.not.be.null;
      if (context) {
        expect(context.id).to.equal('context-1');
        expect(context.name).to.equal('test-context');
        expect(context.state).to.equal('available');
      }
    });
    
    it('should return null if context not found', async () => {
      // Mock the getContext response with no data
      clientStub.getContext.resolves({
        body: {
          data: null
        }
      });
      
      // Call the method
      const context = await contextService.get('non-existent-context');
      
      // Verify the results
      expect(context).to.be.null;
    });
    
    it('should create a context if requested', async () => {
      // Mock the getContext response
      clientStub.getContext.resolves({
        body: {
          data: {
            id: 'new-context-id'
          }
        }
      });
      
      // Mock the listContexts response
      clientStub.listContexts.resolves({
        body: {
          data: [
            {
              id: 'new-context-id',
              name: 'new-context',
              state: 'available',
              createTime: '2025-05-29T12:00:00Z',
              lastUsedTime: '2025-05-29T12:30:00Z',
              osType: null
            }
          ]
        }
      });
      
      // Call the method
      const context = await contextService.get('new-context', true);
      
      // Verify the results
      expect(context).to.not.be.null;
      if (context) {
        expect(context.id).to.equal('new-context-id');
        expect(context.name).to.equal('new-context');
        expect(context.state).to.equal('available');
      }
    });
  });
  
  describe('create()', () => {
    it('should create a new context', async () => {
      // Mock the getContext response
      clientStub.getContext.resolves({
        body: {
          data: {
            id: 'new-context-id'
          }
        }
      });
      
      // Mock the listContexts response
      clientStub.listContexts.resolves({
        body: {
          data: [
            {
              id: 'new-context-id',
              name: 'new-context',
              state: 'available',
              createTime: '2025-05-29T12:00:00Z',
              lastUsedTime: '2025-05-29T12:30:00Z',
              osType: null
            }
          ]
        }
      });
      
      // Call the method
      const context = await contextService.create('new-context');
      
      // Verify the results
      expect(context.id).to.equal('new-context-id');
      expect(context.name).to.equal('new-context');
      expect(context.state).to.equal('available');
    });
  });
  
  describe('update()', () => {
    it('should update a context', async () => {
      // Create a context to update
      const context = new Context(
        'context-to-update',
        'updated-name',
        'available'
      );
      
      // Mock the modifyContext response
      clientStub.modifyContext.resolves({});
      
      // Call the method
      const updatedContext = await contextService.update(context);
      
      // Verify the API was called correctly
      expect(clientStub.modifyContext.calledOnce).to.be.true;
      
      // Verify the results
      expect(updatedContext.id).to.equal('context-to-update');
      expect(updatedContext.name).to.equal('updated-name');
    });
  });
  
  describe('delete()', () => {
    it('should delete a context', async () => {
      // Create a context to delete
      const context = new Context(
        'context-to-delete',
        'context-name',
        'available'
      );
      
      // Mock the deleteContext response
      clientStub.deleteContext.resolves({});
      
      // Call the method
      await contextService.delete(context);
      
      // Verify the API was called correctly
      expect(clientStub.deleteContext.calledOnce).to.be.true;
    });
  });
});
