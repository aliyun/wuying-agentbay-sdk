import { AgentBay, Session, WindowManager } from '../../src';
import * as sinon from 'sinon';
import { getTestApiKey } from '../utils/test-helpers';

// Define test runner types if they're not available
declare function describe(name: string, fn: () => void): void;
declare function beforeEach(fn: () => void | Promise<void>): void;
declare function afterEach(fn: () => void | Promise<void>): void;
declare function it(name: string, fn: () => void | Promise<void>): void;
declare function expect(actual: any): any;

describe('WindowManager', () => {
  let agentBay: AgentBay;
  let session: Session;
  let windowManager: WindowManager;
  let clientStub: any;
  
  beforeEach(async () => {
    // Create a real AgentBay instance with test API key
    const apiKey = getTestApiKey();
    agentBay = new AgentBay({ apiKey });
    // Create a real session
    console.log('Creating a new session for window testing...');
    session = await agentBay.create();
    // Replace the client with a stub
    clientStub = {
      useMcpTool: sinon.stub()
    };
    
    windowManager = new WindowManager(session);
  });
  
  afterEach(async () => {
    console.log('Cleaning up: Deleting the session...');
    try {
      if(session)
        await agentBay.delete(session);
      console.log('Session successfully deleted');
    } catch (error) {
      console.log(`Warning: Error deleting session: ${error}`);
    }
    
    sinon.restore();
  });
  
  describe('listRootWindows()', () => {
    it('should return a list of root windows', async () => {
      // Mock the response from the API
      clientStub.useMcpTool.resolves({
        body: {
          data: {
            result: JSON.stringify([
              {
                window_id: 1234,
                title: 'Window 1',
                pid: 5678,
                pname: 'Process 1'
              },
              {
                window_id: 5678,
                title: 'Window 2',
                pid: 9012,
                pname: 'Process 2'
              }
            ])
          }
        }
      });
      
      console.log('Testing listRootWindows...');
      try {
          // Call the method
        const windows = await windowManager.listRootWindows();
        console.log(`Found ${windows.length} root windows`);
        // Verify the results
        expect(windows.length).toBeGreaterThan(0);
        windows.forEach(element => {
          expect(element.window_id).toBeGreaterThan(0);
          expect(element.title).toBeDefined();
          expect(element.pid).toBeGreaterThan(0);
          expect(element.pname).toBeDefined();
          
        });
      }catch (error:any) {
        console.log(`Error in listRootWindows test: ${error}`);
        expect(error.message).toContain('Failed to list root windows');
      }
      
    });
    
    it('should handle empty response', async () => {
      // Mock the response from the API
      clientStub.useMcpTool.resolves({
        body: {
          data: {
            result: JSON.stringify([])
          }
        }
      });
      
      console.log('Testing listRootWindows with empty response...');
      try {
        // Call the method
        const windows = await windowManager.listRootWindows();
        console.log('Received empty window list as expected',windows);
        
        // Verify the results
        expect(windows).toHaveLength(0);
      }catch (error:any) {
        console.log(`Error in listRootWindows test: ${error}`);
        expect(error.message).toContain('Failed to list root windows');
      }
      
    });
  });
  
  describe('getActiveWindow()', () => {
    it('should return the active window', async () => {
      // Mock the response from the API
      clientStub.useMcpTool.resolves({
        body: {
          data: {
            result: JSON.stringify({
              window_id: 1234,
              title: 'Active Window',
              pid: 5678,
              pname: 'Active Process'
            })
          }
        }
      });
      
      console.log('Testing getActiveWindow...');
      // Call the method
      try {
        debugger;
        const window = await windowManager.getActiveWindow();
        console.log(`Active window: ${window.title} (ID: ${window.window_id})`);
        
        // Verify the results
        expect(window.window_id).toBeGreaterThan(0);
        expect(window.title).toBeDefined();
        expect(window.pid).toBeGreaterThan(0);
        expect(window.pname).toBeDefined();
      }catch (error:any) {
        console.log(`Error in listRootWindows test: ${error}`);
        expect(error.message).toContain('Failed to get active window');
      }
      
    });
    it('should handle empty response',async () => {
      try {
        const window = await windowManager.getActiveWindow();
        console.log(`Active window: ${window} ${window.title} (ID: ${window.window_id})`);
        
        // Verify the results
        expect(window).toBe({});
       
      }catch (error:any) {
        console.log(`Error in listRootWindows test: ${error}`);
        expect(error.message).toContain('Failed to get active window');
      }
    })
  });
  
  describe('activateWindow()', () => {
    it('should activate a window', async () => {
      // Mock the response from the API
      clientStub.useMcpTool.resolves({
        body: {
          data: {
            result: JSON.stringify({ success: true })
          }
        }
      });
      
      console.log('Testing activateWindow...');
      try {
        // Call the method
        await windowManager.activateWindow(1234);
        console.log('Window activated successfully');
      }catch (error:any) {
        console.log(`Error in listRootWindows test: ${error}`);
        expect(error.message).toContain('Failed to get active window');
      }
      
    });
  });
  
  describe('maximizeWindow()', () => {
    it('should maximize a window', async () => {
      // Mock the response from the API
      clientStub.useMcpTool.resolves({
        body: {
          data: {
            result: JSON.stringify({ success: true })
          }
        }
      });
      
      console.log('Testing maximizeWindow...');
      try {
        // Call the method
        await windowManager.maximizeWindow(1234);
        console.log('Window maximized successfully');
      }catch (error:any) {
        console.log(`Error in listRootWindows test: ${error}`);
        expect(error.message).toContain('Failed to maximize window');
      }
      
    });
  });
  
  describe('minimizeWindow()', () => {
    it('should minimize a window', async () => {
      // Mock the response from the API
      clientStub.useMcpTool.resolves({
        body: {
          data: {
            result: JSON.stringify({ success: true })
          }
        }
      });
      
      console.log('Testing minimizeWindow...');
      try {
          // Call the method
        await windowManager.minimizeWindow(1234);
        console.log('Window minimized successfully');
      }catch (error:any) {
        console.log(`Error in listRootWindows test: ${error}`);
        expect(error.message).toContain('Failed to minimize window');
      }
      
    });
  });
  
  describe('restoreWindow()', () => {
    it('should restore a window', async () => {
      // Mock the response from the API
      clientStub.useMcpTool.resolves({
        body: {
          data: {
            result: JSON.stringify({ success: true })
          }
        }
      });
      
      console.log('Testing restoreWindow...');
      try {
        // Call the method
        await windowManager.restoreWindow(1234);
        console.log('Window restored successfully');
      }catch (error:any) {
        console.log(`Error in listRootWindows test: ${error}`);
        expect(error.message).toContain('Failed to restore window');
      }
      
    });
  });
  
  describe('resizeWindow()', () => {
    it('should resize a window', async () => {
      // Mock the response from the API
      clientStub.useMcpTool.resolves({
        body: {
          data: {
            result: JSON.stringify({ success: true })
          }
        }
      });
      
      console.log('Testing resizeWindow...');
      try {
        // Call the method
        await windowManager.resizeWindow(1234, 800, 600);
        console.log('Window resized successfully to 800x600');
      }catch (error:any) {
        console.log(`Error in listRootWindows test: ${error}`);
        expect(error.message).toContain('Failed to resize window');
      }
      
    });
  });
  
  describe('focusMode()', () => {
    it('should enable focus mode', async () => {
      // Mock the response from the API
      clientStub.useMcpTool.resolves({
        body: {
          data: {
            result: JSON.stringify({ success: true })
          }
        }
      });
      
      console.log('Testing focusMode enable...');
      try {
         // Call the method
        await windowManager.focusMode(true);
        console.log('Focus mode enabled successfully');
      }catch (error:any) {
        console.log(`Error in listRootWindows test: ${error}`);
        expect(error.message).toContain('Failed to enable focus mode');
      }
     
    });
    
    it('should disable focus mode', async () => {
      // Mock the response from the API
      clientStub.useMcpTool.resolves({
        body: {
          data: {
            result: JSON.stringify({ success: true })
          }
        }
      });
      
      console.log('Testing focusMode disable...');
      try {
        // Call the method
        await windowManager.focusMode(false);
        console.log('Focus mode disabled successfully');
        
        // Verify the API was called correctly
        expect(clientStub.useMcpTool.calledOnce).toBe(true);
        const callArgs = clientStub.useMcpTool.firstCall.args[0];
        expect(callArgs.toolName).toBe('focus_mode');
        expect(JSON.parse(callArgs.arguments).enable).toBe(false);
      }catch (error:any) {
        console.log(`Error in listRootWindows test: ${error}`);
        expect(error.message).toContain('Failed to disable focus mode');
      }
      // Call the method
      await windowManager.focusMode(false);
      console.log('Focus mode disabled successfully');
      
      // Verify the API was called correctly
      expect(clientStub.useMcpTool.calledOnce).toBe(true);
      const callArgs = clientStub.useMcpTool.firstCall.args[0];
      expect(callArgs.toolName).toBe('focus_mode');
      expect(JSON.parse(callArgs.arguments).enable).toBe(false);
    });
  });
});
