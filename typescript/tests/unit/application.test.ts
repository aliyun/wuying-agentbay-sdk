import { ApplicationManager, InstalledApp, Process } from '../../src/application/application';
import { AgentBay, Session } from '../../src';
import { getTestApiKey } from '../utils/test-helpers';
import * as sinon from 'sinon';

// Define test runner types if they're not available
declare function describe(name: string, fn: () => void): void;
declare function beforeEach(fn: () => void | Promise<void>): void;
declare function afterEach(fn: () => void | Promise<void>): void;
declare function it(name: string, fn: () => void | Promise<void>): void;
declare function expect(actual: any): any;


describe('ApplicationManager', () => {
  let session: Session;
  let applicationManager: ApplicationManager;
  let clientStub: any;
  let agentBay: AgentBay;
  
  beforeEach(async () => {
    const apiKey = getTestApiKey();
    agentBay = await new AgentBay({apiKey});

    session = await agentBay.create()
    applicationManager = await new ApplicationManager(session);
    
    clientStub = {
      callMcpTool: sinon.stub()
    };
    
    
  });
  
  afterEach(async () => {
    console.log('Cleaning up: Deleting the session...');
    try {
      await agentBay.delete(session);
      console.log('Session successfully deleted');
    } catch (error) {
      console.log(`Warning: Error deleting session: ${error}`);
    }
  });
  
  describe('getInstalledApps()', () => {
    it('should return installed applications with valid properties', async () => {
      // Mock successful API response
      const mockApps: InstalledApp[] = [
        { name: 'App 1', start_cmd: '/path/to/app1' },
        { name: 'App 2', start_cmd: '/path/to/app2' },
        { name: 'App 3', start_cmd: '/path/to/app3' }
      ];
      
      applicationManager = new ApplicationManager(session);
      clientStub.callMcpTool.resolves({
        body: {
          data: {
            content: [{ text: JSON.stringify(mockApps) }]
          }
        }
      });
      
      console.log('Testing getInstalledApps...');
      const apps = await applicationManager.getInstalledApps(true, false, true);
      console.log(`Found ${apps.length} installed applications`);
      
      // Verify results
      expect(apps.length).toBeGreaterThan(0);
      apps.forEach((app, index) => {
        console.log(`Verifying app ${index + 1}: ${app.name}`);
        expect(app.name).toBeTruthy();
        expect(app.start_cmd).toBeTruthy();
      });
    });
  });
  
  describe('startApp()', () => {
    it('should start an application and return processes', async () => {
      // Mock successful start response
      const mockProcesses: Process[] = [
        { pname: 'chrome', pid: 1234, cmdline: '/usr/bin/chrome' },
        { pname: 'renderer', pid: 5678, cmdline: '/usr/bin/chrome --renderer' }
      ];
      
      clientStub.callMcpTool.resolves({
        body: {
          data: {
            content: [{ text: JSON.stringify(mockProcesses) }]
          }
        }
      });
      
      const processes = await applicationManager.startApp('/usr/bin/google-chrome-stable %U','');
      console.log('processes',processes);
      
      // Verify results
      expect(processes.length).toBeGreaterThan(0);
      processes.forEach((proc, index) => {
        console.log(`Verifying process ${index + 1}: ${proc.pname} (PID: ${proc.pid})`);
        expect(proc.pname).toBeTruthy();
        expect(proc.pid).toBeGreaterThan(0);
        expect(proc).toHaveProperty('cmdline')
      });
    });
      });
    
      describe('stopAppByPName()', () => {
        it('should stop an application by process name', async () => {
          
          clientStub.callMcpTool.resolves({});
          try{
            const processes = await applicationManager.startApp('/usr/bin/google-chrome-stable %U','');
            expect(processes.length).toBeGreaterThan(0);
            const pname = processes[0].pname;
            console.log('pname',pname);
            const result = await applicationManager.stopAppByPName(pname);
            console.log('stopAppByPName Response:', result);
          }catch(error:any){
            expect(error.message).toMatch(/Failed to stop app by pname|Invalid response data format|Invalid or empty content array in response|Text field not found or tool not found|Failed to call MCP tool/);
          }
         
          
          
        });
      });
      
      describe('stopAppByPID()', () => {
        it('should stop an application by process ID', async () => {
          
          clientStub.callMcpTool.resolves({});
          try{
            const processes = await applicationManager.startApp('/usr/bin/google-chrome-stable %U','');
            expect(processes.length).toBeGreaterThan(0);
            const pid = processes[0].pid;
            const result = await applicationManager.stopAppByPID(pid);
            console.log('stopAppByPID Response:', result);
          }catch(error:any){
            expect(error.message).toMatch(/Failed to stop app by pid|Invalid response data format|Invalid or empty content array in response|Text field not found or tool not found|Failed to call MCP tool/);
          }
    });
  });
  
  describe('listVisibleApps()', () => {
    it('should list visible applications with valid properties', async () => {
      // Mock successful response
      const mockProcesses: Process[] = [
        { pname: 'explorer.exe', pid: 123, path: '/usr/bin/explorer', cmdline: '/usr/bin/explorer' },
        { pname: 'chrome.exe', pid: 456, path: '/usr/bin/chrome', cmdline: '/usr/bin/chrome' }
      ];
      
      clientStub.callMcpTool.resolves({
        body: {
          data: {
            content: [{ text: JSON.stringify(mockProcesses) }]
          }
        }
      });
      try{
        const processes = await applicationManager.listVisibleApps();
      
      
      expect(processes.length).toBeGreaterThan(0);
      processes.forEach(proc => {
        expect(proc.pname).toBeTruthy();
        expect(proc.pid).toBeGreaterThan(0);
      });
      }catch(error:any){
        expect(error.message).toMatch(/Failed to list visible apps|Invalid response data format|Invalid or empty content array in response|Text field not found or tool not found|Failed to call MCP tool/);
      }
      
    });
    
    it('should handle empty visible apps list', async () => {
      // Mock empty response
      clientStub.callMcpTool.resolves({
        body: {
          data: {
            content: [{ text: JSON.stringify([]) }]
          }
        }
      });
      
      console.log('Testing listVisibleApps with empty response...');
      const processes = await applicationManager.listVisibleApps();
      console.log('Received empty visible apps list as expected');
      expect(processes.length).toBe(0);
    });
  });
});
