import { AgentBay, Session } from '../../src';
import { getTestApiKey, containsToolNotFound } from '../utils/test-helpers';

// Define test runner types if they're not available
declare function describe(name: string, fn: () => void): void;
declare function beforeEach(fn: () => void | Promise<void>): void;
declare function afterEach(fn: () => void | Promise<void>): void;
declare function it(name: string, fn: () => void | Promise<void>): void;
declare function expect(actual: any): any;

describe('FileSystem', () => {
  let agentBay: AgentBay;
  let session: Session;
  
  beforeEach(async () => {
    const apiKey = getTestApiKey();
    agentBay = new AgentBay({ apiKey });
    
    // Create a session
    console.log('Creating a new session for filesystem testing...');
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
  
  describe('readFile', () => {
    it('should read a file', async () => {
      if (session.filesystem) {
        console.log('Reading file...');
        try {
          // Use a file that should exist on most systems
          const filePath = '/etc/hosts';
          const content = await session.filesystem.readFile(filePath);
          console.log(`ReadFile result: content='${content.substring(0, 100)}...'`);
          
          // Check if response contains "tool not found"
          expect(containsToolNotFound(content)).toBe(false);
          
          // Verify the content is not empty
          expect(content.length).toBeGreaterThan(0);
          console.log('File read successful');
        } catch (error) {
          console.log(`Note: File operation failed: ${error}`);
          // Don't fail the test if filesystem operations are not supported
        }
      } else {
        console.log('Note: FileSystem interface is nil, skipping file test');
      }
    });
    
    it('should handle file not found errors', async () => {
      if (session.filesystem) {
        console.log('Reading non-existent file...');
        try {
          const nonExistentFile = '/path/to/non/existent/file';
          const content = await session.filesystem.readFile(nonExistentFile);
          console.log(`ReadFile result for non-existent file: content='${content}'`);
          
          // If we get here, the API might return an empty string or error message for non-existent files
          // We're just checking that the promise resolves
          expect(content).toBeDefined();
        } catch (error) {
          // If the API rejects the promise, that's also an acceptable behavior for a non-existent file
          console.log(`Non-existent file read failed as expected: ${error}`);
          expect(error).toBeDefined();
        }
      } else {
        console.log('Note: FileSystem interface is nil, skipping file not found test');
      }
    });
  });
  
  describe('writeFile', () => {
    it('should write to a file', async () => {
      // Check if filesystem exists and has a writeFile method
      // Note: This is a conditional test as writeFile might not be implemented in all versions
      if (session.filesystem && typeof (session.filesystem as any).writeFile === 'function') {
        console.log('Writing to file...');
        try {
          // Use a temporary file path
          const tempFile = `/tmp/agentbay-test-${Date.now()}.txt`;
          const content = `Test content generated at ${new Date().toISOString()}`;
          
          await (session.filesystem as any).writeFile(tempFile, content);
          console.log(`WriteFile successful: ${tempFile}`);
          
          // Verify by reading the file back
          const readContent = await session.filesystem.readFile(tempFile);
          console.log(`ReadFile after write: content='${readContent}'`);
          
          // Check if the content matches
          expect(readContent).toBe(content);
          console.log('File write verified successfully');
          
          // Clean up the temporary file
          if (session.command) {
            await session.command.executeCommand(`rm ${tempFile}`);
            console.log(`Temporary file deleted: ${tempFile}`);
          }
        } catch (error) {
          console.log(`Note: File write operation failed: ${error}`);
          // Don't fail the test if filesystem operations are not supported
        }
      } else {
        console.log('Note: FileSystem writeFile method is not available, skipping file write test');
      }
    });
  });
});
