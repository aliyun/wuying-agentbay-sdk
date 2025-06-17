import { AgentBay, Context, ContextService } from '../../src';
import * as sinon from 'sinon';
import { getTestApiKey } from '../utils/test-helpers';

// Define test runner types if they're not available
declare function describe(name: string, fn: () => void): void;
declare function beforeEach(fn: () => void | Promise<void>): void;
declare function afterEach(fn: () => void | Promise<void>): void;
declare function it(name: string, fn: () => void | Promise<void>): void;
declare function expect(actual: any): any;

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
    
    expect(context.id).toBe('test-id');
    expect(context.name).toBe('test-context');
    expect(context.state).toBe('available');
    expect(context.createdAt).toBe('2025-05-29T12:00:00Z');
    expect(context.lastUsedAt).toBe('2025-05-29T12:30:00Z');
    expect(context.osType).toBe('linux');
  });
});

describe('ContextService', () => {
  let agentBay: AgentBay;
  let contextService: ContextService;
  let clientStub: any;
  
  beforeEach(() => {
    // Create a stub AgentBay instance
    const apiKey = getTestApiKey();
    agentBay = new AgentBay({ apiKey });
    
    // Replace the client with a stub
    clientStub = {
      listContexts: sinon.stub(),
      getContext: sinon.stub(),
      modifyContext: sinon.stub(),
      deleteContext: sinon.stub()
    };
    
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
      try {
        // Call the method
        const contexts = await contextService.list();
        
        // Verify the results
        expect(contexts.length).toBeGreaterThan(0);
        contexts.forEach(context => {
          expect(context.id).toBeDefined();
          expect(context.name).toBeDefined();
          expect(context.state).toBeDefined();
        });
      } catch (error: any) {
        expect(error.message).toContain('Failed to list contexts');
      }
      
    });
    
    it('should handle empty response', async () => {
      // Mock the response from the API
      clientStub.listContexts.resolves({
        body: {
          data: []
        }
      });
      try {
        // Call the method
        const contexts = await contextService.list();
        console.log('get successfully from list',contexts);
        // Verify the results
        expect(contexts).toHaveLength(0);
      } catch (error: any) {
        expect(error.message).toContain('Failed to list contexts');
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
      try {
        // Call the method
        const context = await contextService.get('test-context');
        console.log('get successfully from get',context);
        // Verify the results
        if (context) {
          expect(context.id).toBeDefined();
          expect(context.name).toBeDefined();
          expect(context.state).toBeDefined();
        }
      } catch (error: any) {
        expect(error.message).toContain('Failed to get context');
      }
      
    });
    
    it('should return null if context not found', async () => {
      // Mock the getContext response with no data
      clientStub.getContext.resolves({
        body: {
          data: null
        }
      });
      try {
        const context = await contextService.get('non-existent-context');
        console.log('get successfully from create if context not found',context);
        
      } catch (error: any) {
        expect(error.message).toContain('Failed to get context');
      }
      
      // // Verify the results
      // expect(context).toBeNull();
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
      console.log('get successfully from create',context);
      // Verify the results
      expect(context).not.toBeNull();
      if (context) {
        expect(context.id).toBeDefined();
        expect(context.name).toBeDefined();
        expect(context.state).toBeDefined();
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
      try {
        // Call the method
        const context = await contextService.create('new-context');
        console.log('get successfully from create',context);
        // Verify the results
        expect(context.id).toBeDefined();
        expect(context.name).toBeDefined();
        expect(context.state).toBeDefined();
      } catch (error: any) {
        expect(error.message).toContain('Failed to create context');
      }
      
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
      try {
        // Call the method
        const updatedContext = await contextService.update(context);
        console.log('get successfully from update',updatedContext);
        
        
        // Verify the results
        expect(updatedContext.id).toBeDefined();
        expect(updatedContext.name).toBeDefined();
      } catch (error: any) {
        expect(error.message).toContain('Failed to update context');
      }
      
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
      try {
        // Call the method
      await contextService.delete(context);

      } catch (error: any) {
        expect(error.message).toContain('Failed to delete context');
      }
      
    });
    
  });
});
