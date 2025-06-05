import { AgentBay, Session, WindowManager } from '../src';
import { expect } from 'chai';
import * as sinon from 'sinon';

describe('WindowManager', () => {
  let agentBay: AgentBay;
  let session: Session;
  let windowManager: WindowManager;
  let clientStub: any;
  
  beforeEach(() => {
    // Create a stub AgentBay instance
    agentBay = new AgentBay({ apiKey: 'test-api-key' });
    
    // Create a session
    session = new Session(agentBay, 'test-session-id');
    
    // Replace the client with a stub
    clientStub = {
      useMcpTool: sinon.stub()
    };
    
    // @ts-ignore - Accessing private property for testing
    session.client = clientStub;
    
    windowManager = new WindowManager(session);
  });
  
  afterEach(() => {
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
      
      // Call the method
      const windows = await windowManager.listRootWindows();
      
      // Verify the API was called correctly
      expect(clientStub.useMcpTool.calledOnce).to.be.true;
      const callArgs = clientStub.useMcpTool.firstCall.args[0];
      expect(callArgs.toolName).to.equal('list_root_windows');
      
      // Verify the results
      expect(windows).to.have.lengthOf(2);
      expect(windows[0].window_id).to.equal(1234);
      expect(windows[0].title).to.equal('Window 1');
      expect(windows[0].pid).to.equal(5678);
      expect(windows[0].pname).to.equal('Process 1');
      expect(windows[1].window_id).to.equal(5678);
      expect(windows[1].title).to.equal('Window 2');
      expect(windows[1].pid).to.equal(9012);
      expect(windows[1].pname).to.equal('Process 2');
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
      
      // Call the method
      const windows = await windowManager.listRootWindows();
      
      // Verify the results
      expect(windows).to.have.lengthOf(0);
    });
    
    it('should handle errors', async () => {
      // Mock an error response
      clientStub.useMcpTool.rejects(new Error('API error'));
      
      // Call the method and expect it to throw
      try {
        await windowManager.listRootWindows();
        expect.fail('Should have thrown an error');
      } catch (error: any) {
        expect(error.message).to.include('Failed to list root windows');
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
      
      // Call the method
      const window = await windowManager.getActiveWindow();
      
      // Verify the API was called correctly
      expect(clientStub.useMcpTool.calledOnce).to.be.true;
      const callArgs = clientStub.useMcpTool.firstCall.args[0];
      expect(callArgs.toolName).to.equal('get_active_window');
      
      // Verify the results
      expect(window.window_id).to.equal(1234);
      expect(window.title).to.equal('Active Window');
      expect(window.pid).to.equal(5678);
      expect(window.pname).to.equal('Active Process');
    });
    
    it('should handle errors', async () => {
      // Mock an error response
      clientStub.useMcpTool.rejects(new Error('API error'));
      
      // Call the method and expect it to throw
      try {
        await windowManager.getActiveWindow();
        expect.fail('Should have thrown an error');
      } catch (error: any) {
        expect(error.message).to.include('Failed to get active window');
      }
    });
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
      
      // Call the method
      await windowManager.activateWindow(1234);
      
      // Verify the API was called correctly
      expect(clientStub.useMcpTool.calledOnce).to.be.true;
      const callArgs = clientStub.useMcpTool.firstCall.args[0];
      expect(callArgs.toolName).to.equal('activate_window');
      expect(JSON.parse(callArgs.arguments).window_id).to.equal(1234);
    });
    
    it('should handle errors', async () => {
      // Mock an error response
      clientStub.useMcpTool.rejects(new Error('API error'));
      
      // Call the method and expect it to throw
      try {
        await windowManager.activateWindow(1234);
        expect.fail('Should have thrown an error');
      } catch (error: any) {
        expect(error.message).to.include('Failed to activate window');
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
      
      // Call the method
      await windowManager.maximizeWindow(1234);
      
      // Verify the API was called correctly
      expect(clientStub.useMcpTool.calledOnce).to.be.true;
      const callArgs = clientStub.useMcpTool.firstCall.args[0];
      expect(callArgs.toolName).to.equal('maximize_window');
      expect(JSON.parse(callArgs.arguments).window_id).to.equal(1234);
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
      
      // Call the method
      await windowManager.minimizeWindow(1234);
      
      // Verify the API was called correctly
      expect(clientStub.useMcpTool.calledOnce).to.be.true;
      const callArgs = clientStub.useMcpTool.firstCall.args[0];
      expect(callArgs.toolName).to.equal('minimize_window');
      expect(JSON.parse(callArgs.arguments).window_id).to.equal(1234);
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
      
      // Call the method
      await windowManager.restoreWindow(1234);
      
      // Verify the API was called correctly
      expect(clientStub.useMcpTool.calledOnce).to.be.true;
      const callArgs = clientStub.useMcpTool.firstCall.args[0];
      expect(callArgs.toolName).to.equal('restore_window');
      expect(JSON.parse(callArgs.arguments).window_id).to.equal(1234);
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
      
      // Call the method
      await windowManager.resizeWindow(1234, 800, 600);
      
      // Verify the API was called correctly
      expect(clientStub.useMcpTool.calledOnce).to.be.true;
      const callArgs = clientStub.useMcpTool.firstCall.args[0];
      expect(callArgs.toolName).to.equal('resize_window');
      expect(JSON.parse(callArgs.arguments).window_id).to.equal(1234);
      expect(JSON.parse(callArgs.arguments).width).to.equal(800);
      expect(JSON.parse(callArgs.arguments).height).to.equal(600);
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
      
      // Call the method
      await windowManager.focusMode(true);
      
      // Verify the API was called correctly
      expect(clientStub.useMcpTool.calledOnce).to.be.true;
      const callArgs = clientStub.useMcpTool.firstCall.args[0];
      expect(callArgs.toolName).to.equal('focus_mode');
      expect(JSON.parse(callArgs.arguments).enable).to.be.true;
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
      
      // Call the method
      await windowManager.focusMode(false);
      
      // Verify the API was called correctly
      expect(clientStub.useMcpTool.calledOnce).to.be.true;
      const callArgs = clientStub.useMcpTool.firstCall.args[0];
      expect(callArgs.toolName).to.equal('focus_mode');
      expect(JSON.parse(callArgs.arguments).enable).to.be.false;
    });
  });
});
