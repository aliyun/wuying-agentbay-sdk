import { AgentBay } from 'wuying-agentbay-sdk';

// Define test path prefix
const TestPathPrefix = '/tmp';

// Define interfaces for file system operations
interface FileEntry {
  name: string;
  isDirectory: boolean;
  size?: number;
  path?: string;
}

async function main() {
  // Get API key from environment variable or use default value for testing
  const apiKey = process.env.AGENTBAY_API_KEY || 'akm-xxx'; // Replace with your actual API key
  if (!process.env.AGENTBAY_API_KEY) {
    console.log('Warning: Using placeholder API key. Set AGENTBAY_API_KEY environment variable for production use.');
  }

  // Initialize the AgentBay client
  const agentBay = new AgentBay({ apiKey });

  // Create a new session
  console.log('\nCreating a new session...');
  const createResponse = await agentBay.create({imageId:'linux_latest'});
  const session = createResponse.session;
  console.log(`\nSession created with ID: ${session.sessionId}`);
  console.log(`Create Session RequestId: ${createResponse.requestId}`);

  try {
    // 1. Create a directory
    const testDirPath = `${TestPathPrefix}/test_directory`;
    console.log(`\nCreating directory: ${testDirPath}`);
    try {
      const createDirResponse = await session.fileSystem.createDirectory(testDirPath);
      console.log(`Directory created: ${createDirResponse.success}`);
      console.log(`Create Directory RequestId: ${createDirResponse.requestId}`);
    } catch (error) {
      console.log(`Error creating directory: ${error}`);
    }

    // 2. Write a file
    const testFilePath = `${TestPathPrefix}/test_directory/sample.txt`;
    const testContent = "This is a sample file content.\nThis is the second line.\nThis is the third line.";
    console.log(`\nWriting file: ${testFilePath}`);
    try {
      const writeResponse = await session.fileSystem.writeFile(testFilePath, testContent, "overwrite");
      console.log(`File written successfully: ${writeResponse.success}`);
      console.log(`Write File RequestId: ${writeResponse.requestId}`);
    } catch (error) {
      console.log(`Error writing file: ${error}`);
    }

    // 3. Read the file we just created
    console.log(`\nReading file: ${testFilePath}`);
    try {
      const readResponse = await session.fileSystem.readFile(testFilePath);
      console.log(`File content:\n${readResponse.content}`);
      console.log(`Read File RequestId: ${readResponse.requestId}`);

      // Verify content matches what we wrote
      if (readResponse.content === testContent) {
        console.log('Content verification successful!');
      } else {
        console.log('Content verification failed!');
      }
    } catch (error) {
      console.log(`Error reading file: ${error}`);
    }

    // 4. Get file info
    console.log(`\nGetting file info for: ${testFilePath}`);
    try {
      const fileInfoResponse = await session.fileSystem.getFileInfo(testFilePath);
      const fileInfo = fileInfoResponse.fileInfo;
     console.log(`File info: ${fileInfo}`);
      console.log(`File info: Name=${fileInfo.name}, Path=${fileInfo.path}, Size=${fileInfo.size}, IsDirectory=${fileInfo.isDirectory}`);
      console.log(`Get File Info RequestId: ${fileInfoResponse.requestId}`);
    } catch (error) {
      console.log(`Error getting file info: ${error}`);
    }

    // 5. List directory
    console.log(`\nListing directory: ${testDirPath}`);
    try {
      const listResponse = await session.fileSystem.listDirectory(testDirPath);
      console.log('Directory entries:');
      listResponse.entries.forEach((entry: FileEntry) => {
        console.log(`${entry.isDirectory ? '[DIR]' : '[FILE]'} ${entry.name}`);
      });
      console.log(`List Directory RequestId: ${listResponse.requestId}`);
    } catch (error) {
      console.log(`Error listing directory: ${error}`);
    }

    // 6. Edit file
    console.log(`\nEditing file: ${testFilePath}`);
    try {
      const edits = [
        {
          oldText: "second line",
          newText: "MODIFIED second line"
        }
      ];
      const editResponse = await session.fileSystem.editFile(testFilePath, edits, false);
      console.log(`File edited successfully: ${editResponse.success}`);
      console.log(`Edit File RequestId: ${editResponse.requestId}`);

      // Read the file again to verify the edit
      const readAgainResponse = await session.fileSystem.readFile(testFilePath);
      console.log(`Edited file content:\n${readAgainResponse.content}`);
      console.log(`Read File Again RequestId: ${readAgainResponse.requestId}`);
    } catch (error) {
      console.log(`Error editing file: ${error}`);
    }

    // 7. Search files
    console.log(`\nSearching for files in ${TestPathPrefix} containing 'sample'`);
    try {
      const searchResponse = await session.fileSystem.searchFiles(TestPathPrefix, "sample", undefined);
      console.log(`Search results: ${searchResponse.matches.length} files found`);
      searchResponse.matches.forEach((path: string) => {
        console.log(`- ${path}`);
      });
      console.log(`Search Files RequestId: ${searchResponse.requestId}`);
    } catch (error) {
      console.log(`Error searching files: ${error}`);
    }

    // 8. Move/Rename file
    const newFilePath = `${TestPathPrefix}/test_directory/renamed.txt`;
    console.log(`\nMoving file from ${testFilePath} to ${newFilePath}`);
    try {
      const moveResponse = await session.fileSystem.moveFile(testFilePath, newFilePath);
      console.log(`File moved successfully: ${moveResponse.success}`);
      console.log(`Move File RequestId: ${moveResponse.requestId}`);

      // List directory again to verify the move
      const listAgainResponse = await session.fileSystem.listDirectory(testDirPath);
      console.log('Directory entries after move:');
      listAgainResponse.entries.forEach((entry: FileEntry) => {
        console.log(`${entry.isDirectory ? '[DIR]' : '[FILE]'} ${entry.name}`);
      });
      console.log(`List Directory Again RequestId: ${listAgainResponse.requestId}`);
    } catch (error) {
      console.log(`Error moving file: ${error}`);
    }
  } finally {
    // Clean up by deleting the session when we're done
    console.log('\nDeleting the session...');
    try {
      const deleteResponse = await agentBay.delete(session);
      console.log('Session deleted successfully');
      console.log(`Delete Session RequestId: ${deleteResponse.requestId}`);
    } catch (error) {
      console.log(`Error deleting session: ${error}`);
    }
  }
}

main().catch(error => {
  console.log('Error in main execution:', error);
  process.exit(1);
});
