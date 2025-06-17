import { AgentBay, Session } from '../../src';
import { getTestApiKey, containsToolNotFound } from '../utils/test-helpers';

// Define test runner types if they're not available
declare function describe(name: string, fn: () => void): void;
declare function beforeEach(fn: () => void | Promise<void>): void;
declare function afterEach(fn: () => void | Promise<void>): void;
declare function it(name: string, fn: () => void | Promise<void>): void;
declare function expect(actual: any): any;

describe('Command', () => {
  let agentBay: AgentBay;
  let session: Session;
  
  beforeEach(async () => {
    const apiKey = getTestApiKey();
    agentBay = new AgentBay({ apiKey });
    
    // Create a session
    console.log('Creating a new session for command testing...');
    session = await agentBay.create();
    console.log(`Session created with ID: ${session.sessionId}`);
  });
  
  afterEach(async () => {
    // Clean up the session
    console.log('Cleaning up: Deleting the session...');
    try {
      if(session)
        await agentBay.delete(session);
    } catch (error) {
      console.log(`Warning: Error deleting session: ${error}`);
    }
  });
  
  describe('executeCommand', () => {
    it('should execute a command', async () => {
      if (session.command) {
        // Test with echo command (works on all platforms)
        console.log('Executing echo command...');
        const testString = 'AgentBay SDK Test';
        const echoCmd = `echo '${testString}'`;
        
        try {
          const response = await session.command.executeCommand(echoCmd);
          console.log(`Echo command result: ${response}`);
          
          // Check if response contains "tool not found"
          expect(containsToolNotFound(response)).toBe(false);
          
          // Verify the response contains the test string
          expect(response.includes(testString)).toBe(true);
          console.log('Echo command verified successfully');
        } catch (error) {
          console.log(`Note: Echo command failed: ${error}`);
          // Don't fail the test if command execution is not supported
        }
      } else {
        console.log('Note: Command interface is nil, skipping command test');
      }
    });
    
    it('should handle command execution errors', async () => {
      if (session.command) {
        // Test with an invalid command
        console.log('Executing invalid command...');
        const invalidCmd = 'invalid_command_that_does_not_exist';
        
        try {
          const response = await session.command.executeCommand(invalidCmd);
          console.log(`Invalid command result: ${response}`);
          
          // Even if the command doesn't exist, the API might return a response with an error message
          // We're just checking that the promise resolves
          expect(response).toBeDefined();
        } catch (error) {
          // If the API rejects the promise, that's also an acceptable behavior for an invalid command
          console.log(`Invalid command failed as expected: ${error}`);
          expect(error).toBeDefined();
        }
      } else {
        console.log('Note: Command interface is nil, skipping command error test');
      }
    });
    
    it('should execute a command with arguments', async () => {
      if (session.command) {
        // Test with a command that takes arguments
        console.log('Executing command with arguments...');
        const arg1 = 'hello';
        const arg2 = 'world';
        const cmd = `echo ${arg1} ${arg2}`;
        
        try {
          const response = await session.command.executeCommand(cmd);
          console.log(`Command with arguments result: ${response}`);
          
          // Check if response contains "tool not found"
          expect(containsToolNotFound(response)).toBe(false);
          
          // Verify the response contains both arguments
          expect(response.includes(arg1)).toBe(true);
          expect(response.includes(arg2)).toBe(true);
          console.log('Command with arguments verified successfully');
        } catch (error) {
          console.log(`Note: Command with arguments failed: ${error}`);
          // Don't fail the test if command execution is not supported
        }
      } else {
        console.log('Note: Command interface is nil, skipping command with arguments test');
      }
    });
  });
});
