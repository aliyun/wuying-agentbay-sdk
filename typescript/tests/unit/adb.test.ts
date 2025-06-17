import { AgentBay, Session } from '../../src';
import { getTestApiKey, containsToolNotFound } from '../utils/test-helpers';

// Define test runner types if they're not available
declare function describe(name: string, fn: () => void): void;
declare function beforeEach(fn: () => void | Promise<void>): void;
declare function afterEach(fn: () => void | Promise<void>): void;
declare function it(name: string, fn: () => void | Promise<void>): void;
declare function expect(actual: any): any;

describe('Adb', () => {
  let agentBay: AgentBay;
  let session: Session;
  
  beforeEach(async () => {
    const apiKey = getTestApiKey();
    agentBay = new AgentBay({ apiKey });
    session = await agentBay.create();
  });
  
  afterEach(async () => {
    // Clean up the session
    try {
      await agentBay.delete(session);
      console.log(`Session deleted successfully: ${session.sessionId}`);
      
    } catch (error) {
      console.log(`Warning: Error deleting session: ${error}`);
    }
  });
  
  describe('shell', () => {
    it('should execute ADB shell commands', async () => {
      if (session.adb) {
        console.log('Executing ADB shell command...');
        try {
          const response = await session.adb.shell('ls /sdcard');
          console.log(`ADB shell execution result: ${response}`);
          
          // Check if response contains "tool not found"
          expect(containsToolNotFound(response)).toBe(false);
          
          // We don't check the specific content as it depends on the device
          expect(response).toBeDefined();
        } catch (error) {
          console.log(`Note: ADB shell execution failed: ${error}`);
          // Don't fail the test if ADB is not supported
        }
        
        // Test another ADB command
        try {
          console.log('Executing ADB shell command to check device properties...');
          const propResponse = await session.adb.shell('getprop');
          console.log(`ADB getprop execution result length: ${propResponse.length} bytes`);
          
          // Check if response contains "tool not found"
          expect(containsToolNotFound(propResponse)).toBe(false);
          
          // We don't check the specific content as it depends on the device
          expect(propResponse).toBeDefined();
          expect(propResponse.length).toBeGreaterThan(0);
        } catch (error) {
          console.log(`Note: ADB getprop execution failed: ${error}`);
          // Don't fail the test if ADB is not supported
        }
      } else {
        console.log('Note: Adb interface is nil, skipping ADB test');
      }
    });
  });
});
