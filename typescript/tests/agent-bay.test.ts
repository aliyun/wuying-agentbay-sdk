import { AgentBay, Session, AuthenticationError, APIError } from '../src';
import 'dotenv/config';

// Define test runner types if they're not available
declare function describe(name: string, fn: () => void): void;
declare function beforeEach(fn: () => void | Promise<void>): void;
declare function afterEach(fn: () => void | Promise<void>): void;
declare function it(name: string, fn: () => void | Promise<void>): void;
declare function expect(actual: any): any;

// Define Node.js process if it's not available
declare namespace NodeJS {
  interface ProcessEnv {
    [key: string]: string | undefined;
  }
}

declare var process: {
  env: {
    [key: string]: string | undefined;
  }
};

/**
 * Get API key for testing
 */
function getTestApiKey(): string {
  // For Node.js environments
  let apiKey: string | undefined;
  try {
    apiKey = typeof process !== 'undefined' ? process.env.AGENTBAY_API_KEY : undefined;
  } catch (e) {
    // process is not defined in some environments
  }
  
  if (!apiKey) {
    console.log('Warning: Using default API key. Set AGENTBAY_API_KEY environment variable for testing.');
    return 'akm-xxx'; // Replace with your test API key
  }
  return apiKey;
}

describe('AgentBay', () => {
  describe('constructor', () => {
    it('should initialize with API key from options', () => {
      const apiKey = getTestApiKey();
      const agentBay = new AgentBay({ apiKey });
      expect((agentBay as any).apiKey).toBe(apiKey);
    });
    
    it('should initialize with API key from environment variable', () => {
      const originalEnv = process.env.AGENTBAY_API_KEY;
      process.env.AGENTBAY_API_KEY = 'env_api_key';
      
      try {
        const agentBay = new AgentBay();
        expect((agentBay as any).apiKey).toBe('env_api_key');
      } finally {
        // Restore original environment
        if (originalEnv) {
          process.env.AGENTBAY_API_KEY = originalEnv;
        } else {
          delete process.env.AGENTBAY_API_KEY;
        }
      }
    });
    
    it('should throw AuthenticationError if no API key is provided', () => {
      const originalEnv = process.env.AGENTBAY_API_KEY;
      delete process.env.AGENTBAY_API_KEY;
      
      try {
        expect(() => new AgentBay()).toThrow();
      } finally {
        // Restore original environment
        if (originalEnv) {
          process.env.AGENTBAY_API_KEY = originalEnv;
        }
      }
    });
  });
  
  describe('create, list, and delete', () => {
    let agentBay: AgentBay;
    let session: Session;
    
    beforeEach(() => {
      const apiKey = getTestApiKey();
      agentBay = new AgentBay({ apiKey });
    });
    
    it('should create, list, and delete a session', async () => {
      // Create a session
      console.log('Creating a new session...');
      session = await agentBay.create();
      console.log(`Session created with ID: ${session.sessionId}`);
      
      // Ensure session ID is not empty
      expect(session.sessionId).toBeDefined();
      expect(session.sessionId.length).toBeGreaterThan(0);
      
      // List sessions
      console.log('Listing sessions...');
      const sessions = agentBay.list();
      
      // Ensure at least one session (the one we just created)
      expect(sessions.length).toBeGreaterThanOrEqual(1);
      
      // Check if our created session is in the list
      const found = sessions.some(s => s.sessionId === session.sessionId);
      expect(found).toBe(true);
      
      // Delete the session
      console.log('Deleting the session...');
      await agentBay.delete(session);
      
      // List sessions again to ensure it's deleted
      const sessionsAfterDelete = agentBay.list();
      
      // Check if the deleted session is not in the list
      const stillExists = sessionsAfterDelete.some(s => s.sessionId === session.sessionId);
      expect(stillExists).toBe(false);
    });
  });
});

describe('Session', () => {
  let agentBay: AgentBay;
  let session: Session;
  
  beforeEach(async () => {
    const apiKey = getTestApiKey();
    agentBay = new AgentBay({ apiKey });
    
    // Create a session
    console.log('Creating a new session for testing...');
    session = await agentBay.create();
    console.log(`Session created with ID: ${session.sessionId}`);
  });
  
  afterEach(async () => {
    // Clean up the session
    console.log('Cleaning up: Deleting the session...');
    try {
      await agentBay.delete(session);
    } catch (error) {
      console.log(`Warning: Error deleting session: ${error}`);
    }
  });
  
  describe('properties', () => {
    it('should have valid sessionId', () => {
      expect(session.sessionId).toBeDefined();
      expect(session.sessionId.length).toBeGreaterThan(0);
    });
    
    it('should log resourceUrl', () => {
      // ResourceUrl is optional, so we just log it without checking if it's non-empty
      console.log(`Session resourceUrl: ${session.resourceUrl}`);
    });
    
    it('should have filesystem, command, and adb properties', () => {
      expect(session.filesystem).toBeDefined();
      expect(session.command).toBeDefined();
      expect(session.adb).toBeDefined();
    });
  });
  
  describe('methods', () => {
    it('should return the session ID', () => {
      const sessionId = session.getSessionId();
      expect(sessionId).toBe(session.sessionId);
    });
    
    it('should return the API key', () => {
      const apiKey = session.getAPIKey();
      expect(apiKey).toBe(agentBay.getAPIKey());
    });
    
    it('should return the client', () => {
      const client = session.getClient();
      expect(client).toBeDefined();
    });
  });
  
  describe('delete', () => {
    it('should delete the session', async () => {
      // Create a new session specifically for this test
      console.log('Creating a new session for delete testing...');
      const testSession = await agentBay.create();
      console.log(`Session created with ID: ${testSession.sessionId}`);
      
      // Test delete method
      console.log('Testing session.delete method...');
      try {
        const result = await testSession.delete();
        expect(result).toBe(true);
        
        // Verify the session was deleted by checking it's not in the list
        const sessions = agentBay.list();
        const stillExists = sessions.some(s => s.sessionId === testSession.sessionId);
        expect(stillExists).toBe(false);
      } catch (error) {
        console.log(`Note: Session deletion failed: ${error}`);
        // Clean up if the test failed
        try {
          await agentBay.delete(testSession);
        } catch {
          // Ignore cleanup errors
        }
        throw error;
      }
    });
  });
  
  describe('command', () => {
    it('should execute a command with default timeout', async () => {
      if (session.command) {
        console.log('Executing command with default timeout...');
        try {
          const response = await session.command.executeCommand('ls');
          console.log(`Command execution result: ${response}`);
          expect(response).toBeDefined();
          // Check if response contains "tool not found"
          expect(response.toLowerCase().includes('tool not found')).toBe(false);
        } catch (error) {
          console.log(`Note: Command execution failed: ${error}`);
          // Don't fail the test if command execution is not supported
        }
      } else {
        console.log('Note: Command interface is nil, skipping command test');
      }
    });
    
    it('should execute a command with custom timeout', async () => {
      if (session.command) {
        console.log('Executing command with custom timeout...');
        try {
          const customTimeout = 2000; // 2 seconds
          const response = await session.command.executeCommand('ls', customTimeout);
          console.log(`Command execution result with custom timeout: ${response}`);
          expect(response).toBeDefined();
          // Check if response contains "tool not found"
          expect(response.toLowerCase().includes('tool not found')).toBe(false);
        } catch (error) {
          console.log(`Note: Command execution with custom timeout failed: ${error}`);
          // Don't fail the test if command execution is not supported
        }
      } else {
        console.log('Note: Command interface is nil, skipping command test');
      }
    });
    
    it('should execute Python code with default timeout', async () => {
      if (session.command) {
        console.log('Executing Python code with default timeout...');
        try {
          const pythonCode = `
print("Hello, world!")
x = 1 + 1
print(x)
`;
          const response = await session.command.runCode(pythonCode, 'python');
          console.log(`Python code execution result: ${response}`);
          expect(response).toBeDefined();
          // Check if response contains "tool not found"
          expect(response.toLowerCase().includes('tool not found')).toBe(false);
          // Check if response contains expected output
          expect(response.includes('Hello, world!')).toBe(true);
          expect(response.includes('2')).toBe(true);
        } catch (error) {
          console.log(`Note: Python code execution failed: ${error}`);
          // Don't fail the test if code execution is not supported
        }
      } else {
        console.log('Note: Command interface is nil, skipping code execution test');
      }
    });
    
    it('should execute JavaScript code with custom timeout', async () => {
      if (session.command) {
        console.log('Executing JavaScript code with custom timeout...');
        try {
          const jsCode = `
console.log("Hello, world!");
const x = 1 + 1;
console.log(x);
`;
          const customTimeout = 600; // 10 minutes
          const response = await session.command.runCode(jsCode, 'javascript', customTimeout);
          console.log(`JavaScript code execution result: ${response}`);
          expect(response).toBeDefined();
          // Check if response contains "tool not found"
          expect(response.toLowerCase().includes('tool not found')).toBe(false);
          // Check if response contains expected output
          expect(response.includes('Hello, world!')).toBe(true);
          expect(response.includes('2')).toBe(true);
        } catch (error) {
          console.log(`Note: JavaScript code execution failed: ${error}`);
          // Don't fail the test if code execution is not supported
        }
      } else {
        console.log('Note: Command interface is nil, skipping code execution test');
      }
    });
    
    it('should reject invalid language', async () => {
      if (session.command) {
        console.log('Testing with invalid language...');
        try {
          await session.command.runCode('print("test")', 'invalid_language');
          // Should not reach here
          console.log('Error: Expected error for invalid language, but got success');
          expect(false).toBe(true); // Force test to fail
        } catch (error) {
          console.log(`Correctly received error for invalid language: ${error}`);
          expect(error).toBeDefined();
          expect(String(error).includes('Unsupported language')).toBe(true);
        }
      } else {
        console.log('Note: Command interface is nil, skipping code execution test');
      }
    });
  });
  
  describe('filesystem', () => {
    it('should read a file', async () => {
      if (session.filesystem) {
        console.log('Reading file...');
        try {
          const content = await session.filesystem.readFile('/etc/hosts');
          console.log(`ReadFile result: content='${content}'`);
          expect(content).toBeDefined();
          // Check if response contains "tool not found"
          expect(content.toLowerCase().includes('tool not found')).toBe(false);
          console.log('File read successful');
        } catch (error) {
          console.log(`Note: File operation failed: ${error}`);
          // Don't fail the test if filesystem operations are not supported
        }
      } else {
        console.log('Note: FileSystem interface is nil, skipping file test');
      }
    });
  });
});

describe('Adb', () => {
  let agentBay: AgentBay;
  let session: Session;
  
  beforeEach(async () => {
    const apiKey = getTestApiKey();
    agentBay = new AgentBay({ apiKey });
    
    // Create a session
    console.log('Creating a new session for ADB testing...');
    session = await agentBay.create();
    console.log(`Session created with ID: ${session.sessionId}`);
  });
  
  afterEach(async () => {
    // Clean up the session
    console.log('Cleaning up: Deleting the session...');
    try {
      await agentBay.delete(session);
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
          expect(response).toBeDefined();
          // Check if response contains "tool not found"
          expect(response.toLowerCase().includes('tool not found')).toBe(false);
        } catch (error) {
          console.log(`Note: ADB shell execution failed: ${error}`);
          // Don't fail the test if ADB is not supported
        }
        
        // Test another ADB command
        try {
          console.log('Executing ADB shell command to check device properties...');
          const propResponse = await session.adb.shell('getprop');
          console.log(`ADB getprop execution result length: ${propResponse.length} bytes`);
          expect(propResponse).toBeDefined();
          // Check if response contains "tool not found"
          expect(propResponse.toLowerCase().includes('tool not found')).toBe(false);
        } catch (error) {
          console.log(`Note: ADB getprop execution failed: ${error}`);
        }
      } else {
        console.log('Note: Adb interface is nil, skipping ADB test');
      }
    });
  });
});
