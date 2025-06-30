import { AgentBay } from '../../src';
import { log, logError } from '../../src/utils/logger';
import { getTestApiKey } from '../../tests/utils/test-helpers';

// Define test path prefix
const TestPathPrefix = '/tmp';

async function main() {
  // Get API key from environment variable or use default value for testing
  const apiKey = getTestApiKey();

  // Initialize the AgentBay client
  const agentBay = new AgentBay({ apiKey });

  // Create a new session
  log('\nCreating a new session...');
  const createResponse = await agentBay.create({imageId:'linux_latest'});
  const session = createResponse.data;
  log(`\nSession created with ID: ${session.sessionId}`);
  log(`Create Session RequestId: ${createResponse.requestId}`);

  try {
    // 1. Create a directory
    const testDirPath = `${TestPathPrefix}/test_directory`;
    log(`\nCreating directory: ${testDirPath}`);
    try {
      const createDirResponse = await session.filesystem.createDirectory(testDirPath);
      log(`Directory created: ${createDirResponse.data}`);
      log(`Create Directory RequestId: ${createDirResponse.requestId}`);
    } catch (error) {
      log(`Error creating directory: ${error}`);
    }

    // 2. Write a file
    const testFilePath = `${TestPathPrefix}/test_directory/sample.txt`;
    const testContent = "This is a sample file content.\nThis is the second line.\nThis is the third line.";
    log(`\nWriting file: ${testFilePath}`);
    try {
      const writeResponse = await session.filesystem.writeFile(testFilePath, testContent, "overwrite");
      log(`File written successfully: ${writeResponse.data}`);
      log(`Write File RequestId: ${writeResponse.requestId}`);
    } catch (error) {
      log(`Error writing file: ${error}`);
    }

    // 3. Read the file we just created
    log(`\nReading file: ${testFilePath}`);
    try {
      const readResponse = await session.filesystem.readFile(testFilePath);
      log(`File content:\n${readResponse.data}`);
      log(`Read File RequestId: ${readResponse.requestId}`);

      // Verify content matches what we wrote
      if (readResponse.data === testContent) {
        log('Content verification successful!');
      } else {
        log('Content verification failed!');
      }
    } catch (error) {
      log(`Error reading file: ${error}`);
    }

    // 4. Get file info
    log(`\nGetting file info for: ${testFilePath}`);
    try {
      const fileInfoResponse = await session.filesystem.getFileInfo(testFilePath);
      const fileInfo = fileInfoResponse.data;
      log(`File info: Name=${fileInfo.name}, Path=${fileInfo.path}, Size=${fileInfo.size}, IsDirectory=${fileInfo.isDirectory}`);
      log(`Get File Info RequestId: ${fileInfoResponse.requestId}`);
    } catch (error) {
      log(`Error getting file info: ${error}`);
    }

    // 5. List directory
    log(`\nListing directory: ${testDirPath}`);
    try {
      const listResponse = await session.filesystem.listDirectory(testDirPath);
      log('Directory entries:');
      listResponse.data.forEach(entry => {
        log(`${entry.isDirectory ? '[DIR]' : '[FILE]'} ${entry.name}`);
      });
      log(`List Directory RequestId: ${listResponse.requestId}`);
    } catch (error) {
      log(`Error listing directory: ${error}`);
    }

    // 6. Edit file
    log(`\nEditing file: ${testFilePath}`);
    try {
      const edits = [
        {
          oldText: "second line",
          newText: "MODIFIED second line"
        }
      ];
      const editResponse = await session.filesystem.editFile(testFilePath, edits, false);
      log(`File edited successfully: ${editResponse.data}`);
      log(`Edit File RequestId: ${editResponse.requestId}`);

      // Read the file again to verify the edit
      const readAgainResponse = await session.filesystem.readFile(testFilePath);
      log(`Edited file content:\n${readAgainResponse.data}`);
      log(`Read File Again RequestId: ${readAgainResponse.requestId}`);
    } catch (error) {
      log(`Error editing file: ${error}`);
    }

    // 7. Search files
    log(`\nSearching for files in ${TestPathPrefix} containing 'sample'`);
    try {
      const searchResponse = await session.filesystem.searchFiles(TestPathPrefix, "sample", undefined);
      log(`Search results: ${searchResponse.data.length} files found`);
      searchResponse.data.forEach(path => {
        log(`- ${path}`);
      });
      log(`Search Files RequestId: ${searchResponse.requestId}`);
    } catch (error) {
      log(`Error searching files: ${error}`);
    }

    // 8. Move/Rename file
    const newFilePath = `${TestPathPrefix}/test_directory/renamed.txt`;
    log(`\nMoving file from ${testFilePath} to ${newFilePath}`);
    try {
      const moveResponse = await session.filesystem.moveFile(testFilePath, newFilePath);
      log(`File moved successfully: ${moveResponse.data}`);
      log(`Move File RequestId: ${moveResponse.requestId}`);

      // List directory again to verify the move
      const listAgainResponse = await session.filesystem.listDirectory(testDirPath);
      log('Directory entries after move:');
      listAgainResponse.data.forEach(entry => {
        log(`${entry.isDirectory ? '[DIR]' : '[FILE]'} ${entry.name}`);
      });
      log(`List Directory Again RequestId: ${listAgainResponse.requestId}`);
    } catch (error) {
      log(`Error moving file: ${error}`);
    }
  } finally {
    // Clean up by deleting the session when we're done
    log('\nDeleting the session...');
    try {
      const deleteResponse = await agentBay.delete(session);
      log('Session deleted successfully');
      log(`Delete Session RequestId: ${deleteResponse.requestId}`);
    } catch (error) {
      log(`Error deleting session: ${error}`);
    }
  }
}

main().catch(error => {
  logError('Error in main execution:', error);
  process.exit(1);
});
