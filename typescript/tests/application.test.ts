import { AgentBay, Session, ApplicationManager } from '../src';
import { expect } from 'chai';
import * as sinon from 'sinon';

describe('ApplicationManager', () => {
  let agentBay: AgentBay;
  let session: Session;
  let applicationManager: ApplicationManager;
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
    
    applicationManager = new ApplicationManager(session);
  });
  
  afterEach(() => {
    sinon.restore();
  });
  
  describe('getInstalledApps()', () => {
    it('should return a list of installed applications', async () => {
      // Mock the response from the API
      clientStub.useMcpTool.resolves({
        body: {
          data: {
            result: JSON.stringify([
              {
                name: 'App 1',
                path: '/path/to/app1',
                version: '1.0.0'
              },
              {
                name: 'App 2',
                path: '/path/to/app2',
                version: '2.0.0'
              }
            ])
          }
        }
      });
      
      // Call the method
      const apps = await applicationManager.getInstalledApps(true, false, true);
      
      // Verify the API was called correctly
      expect(clientStub.useMcpTool.calledOnce).to.be.true;
      const callArgs = clientStub.useMcpTool.firstCall.args[0];
      expect(callArgs.toolName).to.equal('get_installed_apps');
      expect(JSON.parse(callArgs.arguments).include_system_apps).to.be.true;
      expect(JSON.parse(callArgs.arguments).include_store_apps).to.be.false;
      expect(JSON.parse(callArgs.arguments).include_desktop_apps).to.be.true;
      
      // Verify the results
      expect(apps).to.have.lengthOf(2);
      expect(apps[0].name).to.equal('App 1');
      expect(apps[0].path).to.equal('/path/to/app1');
      expect(apps[0].version).to.equal('1.0.0');
      expect(apps[1].name).to.equal('App 2');
      expect(apps[1].path).to.equal('/path/to/app2');
      expect(apps[1].version).to.equal('2.0.0');
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
      const apps = await applicationManager.getInstalledApps();
      
      // Verify the results
      expect(apps).to.have.lengthOf(0);
    });
    
    it('should handle errors', async () => {
      // Mock an error response
      clientStub.useMcpTool.rejects(new Error('API error'));
      
      // Call the method and expect it to throw
      try {
        await applicationManager.getInstalledApps();
        expect.fail('Should have thrown an error');
      } catch (error: any) {
        expect(error.message).to.include('Failed to get installed applications');
      }
    });
  });
  
  describe('listVisibleApps()', () => {
    it('should return a list of visible applications', async () => {
      // Mock the response from the API
      clientStub.useMcpTool.resolves({
        body: {
          data: {
            result: JSON.stringify([
              {
                pid: 1234,
                pname: 'Process 1',
                path: '/path/to/process1'
              },
              {
                pid: 5678,
                pname: 'Process 2',
                path: '/path/to/process2'
              }
            ])
          }
        }
      });
      
      // Call the method
      const processes = await applicationManager.listVisibleApps();
      
      // Verify the API was called correctly
      expect(clientStub.useMcpTool.calledOnce).to.be.true;
      const callArgs = clientStub.useMcpTool.firstCall.args[0];
      expect(callArgs.toolName).to.equal('list_visible_apps');
      
      // Verify the results
      expect(processes).to.have.lengthOf(2);
      expect(processes[0].pid).to.equal(1234);
      expect(processes[0].pname).to.equal('Process 1');
      expect(processes[0].path).to.equal('/path/to/process1');
      expect(processes[1].pid).to.equal(5678);
      expect(processes[1].pname).to.equal('Process 2');
      expect(processes[1].path).to.equal('/path/to/process2');
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
      const processes = await applicationManager.listVisibleApps();
      
      // Verify the results
      expect(processes).to.have.lengthOf(0);
    });
    
    it('should handle errors', async () => {
      // Mock an error response
      clientStub.useMcpTool.rejects(new Error('API error'));
      
      // Call the method and expect it to throw
      try {
        await applicationManager.listVisibleApps();
        expect.fail('Should have thrown an error');
      } catch (error: any) {
        expect(error.message).to.include('Failed to list visible applications');
      }
    });
  });
});
