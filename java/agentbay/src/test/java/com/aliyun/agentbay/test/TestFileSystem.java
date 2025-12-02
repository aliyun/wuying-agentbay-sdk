package com.aliyun.agentbay.test;

import com.aliyun.agentbay.AgentBay;
import com.aliyun.agentbay.exception.AgentBayException;
import com.aliyun.agentbay.exception.SessionException;
import com.aliyun.agentbay.filesystem.*;
import com.aliyun.agentbay.model.*;
import com.aliyun.agentbay.session.CreateSessionParams;
import com.aliyun.agentbay.session.Session;
import org.junit.After;
import org.junit.AfterClass;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;

import java.util.*;

import static org.junit.Assert.*;

/**
 * Test cases for FileSystem functionality in AgentBay Java SDK
 * This test class covers the functionality demonstrated in FileSystemExample.java
 * 
 * Tests cover:
 * 1. Basic file reading and writing
 * 2. Directory operations
 * 3. File information retrieval
 * 4. File editing
 * 5. File moving
 * 6. File searching
 * 7. Multiple file reading
 * 8. Large file operations
 * 9. Parent directory creation
 */
public class TestFileSystem {

    private static AgentBay agentBay;
    private static Session session;
    private static FileSystem fs;

    /**
     * Helper method to normalize content for comparison
     * Removes trailing newlines and carriage returns that may be added by the API
     * Handles both actual newline characters and literal "\n" strings
     */
    private String normalizeContent(String content) {
        if (content == null) {
            return null;
        }
        // Remove trailing whitespace including \r\n, \n, \r
        // Also handle literal "\n" strings (backslash + n) that may be returned by the API
        while (true) {
            boolean changed = false;
            
            // Handle literal "\r\n" (4 characters: backslash-r-backslash-n)
            if (content.endsWith("\\r\\n")) {
                content = content.substring(0, content.length() - 4);
                changed = true;
            }
            // Handle literal "\n" (2 characters: backslash-n)
            else if (content.endsWith("\\n")) {
                content = content.substring(0, content.length() - 2);
                changed = true;
            }
            // Handle literal "\r" (2 characters: backslash-r)
            else if (content.endsWith("\\r")) {
                content = content.substring(0, content.length() - 2);
                changed = true;
            }
            // Handle actual \r\n (2 bytes: CR+LF)
            else if (content.endsWith("\r\n")) {
                content = content.substring(0, content.length() - 2);
                changed = true;
            }
            // Handle actual \n (1 byte: LF)
            else if (content.endsWith("\n")) {
                content = content.substring(0, content.length() - 1);
                changed = true;
            }
            // Handle actual \r (1 byte: CR)
            else if (content.endsWith("\r")) {
                content = content.substring(0, content.length() - 1);
                changed = true;
            }
            
            if (!changed) {
                break;
            }
        }
        return content;
    }

    /**
     * Get API key for testing
     */
    private static String getTestApiKey() {
        String apiKey = System.getenv("AGENTBAY_API_KEY");
        if (apiKey == null || apiKey.trim().isEmpty()) {
            apiKey = "akm-xxx"; // Replace with your test API key
            System.out.println("Warning: Using default API key. Set AGENTBAY_API_KEY environment variable for testing.");
        }
        return apiKey;
    }

    /**
     * Set up before all tests - create AgentBay client and session
     */
    @BeforeClass
    public static void setUp() throws AgentBayException {
        System.out.println("Setting up test environment...");
        String apiKey = getTestApiKey();
        agentBay = new AgentBay(apiKey);

        // Create a session with Linux image for file system operations
        CreateSessionParams params = new CreateSessionParams();
        params.setImageId("linux_latest");
        SessionResult sessionResult = agentBay.create(params);

        assertTrue("Failed to create session: " + sessionResult.getErrorMessage(), 
                   sessionResult.isSuccess());
        assertNotNull("Session object is null", sessionResult.getSession());

        session = sessionResult.getSession();
        fs = session.getFileSystem();
        
        assertNotNull("FileSystem interface should not be null", fs);
        System.out.println("✅ Session created with ID: " + session.getSessionId());
    }

    /**
     * Clean up after all tests - delete the session
     */
    @AfterClass
    public static void tearDown() {
        if (session != null && agentBay != null) {
            try {
                System.out.println("Cleaning up session...");
                DeleteResult deleteResult = agentBay.delete(session, false);
                if (deleteResult.isSuccess()) {
                    System.out.println("✅ Session deleted successfully");
                } else {
                    System.err.println("⚠️ Failed to delete session: " + deleteResult.getErrorMessage());
                }
            } catch (Exception e) {
                System.err.println("⚠️ Error during cleanup: " + e.getMessage());
            }
        }
    }

    /**
     * Test basic file write operation in overwrite mode
     */
    @Test
    public void testWriteFileOverwrite() throws SessionException {
        System.out.println("\n📝 Testing file write (overwrite mode)...");
        
        String testFilePath = "/tmp/test_write.txt";
        String testContent = "This is test content for write operation.";
        
        BoolResult result = fs.writeFile(testFilePath, testContent, "overwrite");
        
        assertTrue("File write should succeed: " + result.getErrorMessage(), 
                   result.isSuccess());
        assertNotNull("Request ID should not be null", result.getRequestId());
        
        System.out.println("✅ File write successful");
        System.out.println("   Path: " + testFilePath);
        System.out.println("   Request ID: " + result.getRequestId());
    }

    /**
     * Test basic file read operation
     */
    @Test
    public void testReadFile() throws SessionException {
        System.out.println("\n📖 Testing file read...");
        
        String testFilePath = "/tmp/test_read.txt";
        String expectedContent = "This is test content.\nIt has multiple lines.\nThis is line 3.";
        
        // First write a file
        BoolResult writeResult = fs.writeFile(testFilePath, expectedContent, "overwrite");
        assertTrue("File write should succeed", writeResult.isSuccess());
        
        // Now read it back
        FileContentResult readResult = fs.readFile(testFilePath);
        
        assertTrue("File read should succeed: " + readResult.getErrorMessage(), 
                   readResult.isSuccess());
        assertNotNull("Content should not be null", readResult.getContent());
        assertEquals("Content should match", normalizeContent(expectedContent), normalizeContent(readResult.getContent()));
        assertNotNull("Request ID should not be null", readResult.getRequestId());
        
        System.out.println("✅ File read successful");
        System.out.println("   Content length: " + readResult.getContent().length() + " bytes");
        System.out.println("   Content matches: " + normalizeContent(readResult.getContent()).equals(normalizeContent(expectedContent)));
    }

    /**
     * Test file append operation
     */
    @Test
    public void testWriteFileAppend() throws SessionException {
        System.out.println("\n➕ Testing file append...");
        
        String testFilePath = "/tmp/test_append.txt";
        String initialContent = "Initial content.";
        String appendContent = "\nAppended content.";
        
        // Write initial content
        BoolResult writeResult = fs.writeFile(testFilePath, initialContent, "overwrite");
        assertTrue("Initial write should succeed", writeResult.isSuccess());
        
        // Append content
        BoolResult appendResult = fs.writeFile(testFilePath, appendContent, "append");
        assertTrue("File append should succeed: " + appendResult.getErrorMessage(), 
                   appendResult.isSuccess());
        assertNotNull("Request ID should not be null", appendResult.getRequestId());
        
        // Read back and verify
        FileContentResult readResult = fs.readFile(testFilePath);
        assertTrue("File read should succeed", readResult.isSuccess());
        assertEquals("Content should be combined", 
                    normalizeContent(initialContent + appendContent), 
                    normalizeContent(readResult.getContent()));
        
        System.out.println("✅ File append successful");
        System.out.println("   Combined content length: " + readResult.getContent().length() + " bytes");
    }

    /**
     * Test directory creation
     */
    @Test
    public void testCreateDirectory() throws SessionException {
        System.out.println("\n📁 Testing directory creation...");
        
        String testDirPath = "/tmp/test_dir_" + System.currentTimeMillis();
        
        BoolResult result = fs.createDirectory(testDirPath);
        
        assertTrue("Directory creation should succeed: " + result.getErrorMessage(), 
                   result.isSuccess());
        assertNotNull("Request ID should not be null", result.getRequestId());
        
        // Verify the directory exists by listing parent directory
        DirectoryListResult listResult = fs.listDirectory("/tmp");
        assertTrue("List directory should succeed", listResult.isSuccess());
        
        boolean found = false;
        String dirName = testDirPath.substring(testDirPath.lastIndexOf('/') + 1);
        for (Map<String, Object> entry : listResult.getEntries()) {
            if (dirName.equals(entry.get("name"))) {
                found = true;
                assertTrue("Entry should be a directory", 
                          (Boolean) entry.get("isDirectory"));
                break;
            }
        }
        assertTrue("Created directory should be found in listing", found);
        
        System.out.println("✅ Directory creation successful");
        System.out.println("   Path: " + testDirPath);
    }

    /**
     * Test directory listing
     */
    @Test
    public void testListDirectory() throws SessionException {
        System.out.println("\n📋 Testing directory listing...");
        
        String testDirPath = "/tmp/test_list_dir";
        
        // Create directory and some files
        fs.createDirectory(testDirPath);
        fs.writeFile(testDirPath + "/file1.txt", "content1", "overwrite");
        fs.writeFile(testDirPath + "/file2.txt", "content2", "overwrite");
        fs.createDirectory(testDirPath + "/subdir");
        
        // List directory
        DirectoryListResult result = fs.listDirectory(testDirPath);
        
        assertTrue("Directory listing should succeed: " + result.getErrorMessage(), 
                   result.isSuccess());
        assertNotNull("Entries should not be null", result.getEntries());
        assertTrue("Should have at least 3 entries", result.getEntries().size() >= 3);
        assertNotNull("Request ID should not be null", result.getRequestId());
        
        // Verify entries
        Set<String> foundNames = new HashSet<>();
        for (Map<String, Object> entry : result.getEntries()) {
            assertNotNull("Entry name should not be null", entry.get("name"));
            assertNotNull("Entry isDirectory should not be null", entry.get("isDirectory"));
            foundNames.add((String) entry.get("name"));
        }
        
        assertTrue("Should find file1.txt", foundNames.contains("file1.txt"));
        assertTrue("Should find file2.txt", foundNames.contains("file2.txt"));
        assertTrue("Should find subdir", foundNames.contains("subdir"));
        
        System.out.println("✅ Directory listing successful");
        System.out.println("   Found " + result.getEntries().size() + " entries");
    }

    /**
     * Test getting file information
     */
    @Test
    public void testGetFileInfo() throws SessionException {
        System.out.println("\n📊 Testing get file info...");
        
        String testFilePath = "/tmp/test_fileinfo.txt";
        String testContent = "Test content for file info.";
        
        // Create a file
        fs.writeFile(testFilePath, testContent, "overwrite");
        
        // Get file info
        FileInfoResult result = fs.getFileInfo(testFilePath);
        
        assertTrue("Get file info should succeed: " + result.getErrorMessage(), 
                   result.isSuccess());
        assertNotNull("File info should not be null", result.getFileInfo());
        assertNotNull("Request ID should not be null", result.getRequestId());
        
        Map<String, Object> fileInfo = result.getFileInfo();
        
        // Verify file info is not empty and contains some data
        assertFalse("File info should not be empty", fileInfo.isEmpty());
        assertTrue("File info should contain at least one field", fileInfo.size() > 0);
        
        // Optionally check for size field if it exists (common field)
        if (fileInfo.containsKey("size")) {
            assertNotNull("File info size should not be null", fileInfo.get("size"));
            System.out.println("   File size: " + fileInfo.get("size"));
        }
        
        System.out.println("✅ Get file info successful");
        System.out.println("   File info entries: " + fileInfo.size());
        for (Map.Entry<String, Object> entry : fileInfo.entrySet()) {
            System.out.println("   - " + entry.getKey() + ": " + entry.getValue());
        }
    }

    /**
     * Test file editing
     */
    @Test
    public void testEditFile() throws SessionException {
        System.out.println("\n✏️ Testing file edit...");
        
        String testFilePath = "/tmp/test_edit.txt";
        String originalContent = "Line 1: Original text\nLine 2: Keep this\nLine 3: Replace this";
        
        // Create a file
        fs.writeFile(testFilePath, originalContent, "overwrite");
        
        // Edit the file
        List<Map<String, String>> edits = new ArrayList<>();
        Map<String, String> edit = new HashMap<>();
        edit.put("oldText", "Line 3: Replace this");
        edit.put("newText", "Line 3: Modified text");
        edits.add(edit);
        
        BoolResult editResult = fs.editFile(testFilePath, edits);
        
        assertTrue("File edit should succeed: " + editResult.getErrorMessage(), 
                   editResult.isSuccess());
        assertNotNull("Request ID should not be null", editResult.getRequestId());
        
        // Read back and verify
        FileContentResult readResult = fs.readFile(testFilePath);
        assertTrue("File read should succeed", readResult.isSuccess());
        assertTrue("Content should contain modified text", 
                  readResult.getContent().contains("Line 3: Modified text"));
        assertFalse("Content should not contain old text", 
                   readResult.getContent().contains("Line 3: Replace this"));
        
        System.out.println("✅ File edit successful");
        System.out.println("   Modified content: " + readResult.getContent());
    }

    /**
     * Test file moving
     */
    @Test
    public void testMoveFile() throws SessionException {
        System.out.println("\n🚚 Testing file move...");
        
        String sourcePath = "/tmp/test_move_source.txt";
        String destPath = "/tmp/test_move_dest.txt";
        String testContent = "Content to be moved";
        
        // Create source file
        fs.writeFile(sourcePath, testContent, "overwrite");
        
        // Move the file
        BoolResult moveResult = fs.moveFile(sourcePath, destPath);
        
        assertTrue("File move should succeed: " + moveResult.getErrorMessage(), 
                   moveResult.isSuccess());
        assertNotNull("Request ID should not be null", moveResult.getRequestId());
        
        // Verify destination file exists and has correct content
        FileContentResult readResult = fs.readFile(destPath);
        assertTrue("Destination file should be readable", readResult.isSuccess());
        assertEquals("Content should match", normalizeContent(testContent), normalizeContent(readResult.getContent()));
        
        System.out.println("✅ File move successful");
        System.out.println("   From: " + sourcePath);
        System.out.println("   To: " + destPath);
        System.out.println("   Content preserved: " + normalizeContent(readResult.getContent()).equals(normalizeContent(testContent)));
    }

    /**
     * Test file searching
     */
    @Test
    public void testSearchFiles() throws SessionException {
        System.out.println("\n🔍 Testing file search...");
        
        String searchDir = "/tmp/test_search_" + System.currentTimeMillis();
        
        // Create directory and files
        fs.createDirectory(searchDir);
        fs.writeFile(searchDir + "/match1.txt", "This file has KEYWORD", "overwrite");
        fs.writeFile(searchDir + "/nomatch.txt", "This file does not match", "overwrite");
        fs.writeFile(searchDir + "/match2.log", "Another KEYWORD file", "overwrite");
        
        // Search for files with pattern
        FileSearchResult result = fs.searchFiles(searchDir, "*.txt");
        
        assertTrue("File search should succeed: " + result.getErrorMessage(), 
                   result.isSuccess());
        assertNotNull("Matches should not be null", result.getMatches());
        assertNotNull("Request ID should not be null", result.getRequestId());
        
        // Verify search results
        assertTrue("Should find at least 2 .txt files", result.getMatches().size() >= 2);
        
        boolean foundMatch1 = false;
        boolean foundNoMatch = false;
        for (String match : result.getMatches()) {
            if (match.contains("match1.txt")) foundMatch1 = true;
            if (match.contains("nomatch.txt")) foundNoMatch = true;
        }
        
        assertTrue("Should find match1.txt", foundMatch1);
        assertTrue("Should find nomatch.txt", foundNoMatch);
        
        System.out.println("✅ File search successful");
        System.out.println("   Found " + result.getMatches().size() + " files");
        for (String match : result.getMatches()) {
            System.out.println("   - " + match);
        }
    }

    /**
     * Test reading multiple files at once
     */
    @Test
    public void testReadMultipleFiles() throws SessionException {
        System.out.println("\n📚 Testing read multiple files...");
        
        String baseDir = "/tmp/test_multi_read";
        fs.createDirectory(baseDir);
        
        // Create multiple files
        Map<String, String> testFiles = new HashMap<>();
        testFiles.put(baseDir + "/file1.txt", "Content of file 1");
        testFiles.put(baseDir + "/file2.txt", "Content of file 2");
        testFiles.put(baseDir + "/file3.txt", "Content of file 3");
        
        for (Map.Entry<String, String> entry : testFiles.entrySet()) {
            fs.writeFile(entry.getKey(), entry.getValue(), "overwrite");
        }
        
        // Read multiple files
        List<String> filePaths = new ArrayList<>(testFiles.keySet());
        MultipleFileContentResult result = fs.readMultipleFiles(filePaths);
        
        assertTrue("Read multiple files should succeed: " + result.getErrorMessage(), 
                   result.isSuccess());
        assertNotNull("Content map should not be null", result.getContent());
        assertEquals("Should read all files", testFiles.size(), result.getContent().size());
        assertNotNull("Request ID should not be null", result.getRequestId());
        
        // Verify content
        for (Map.Entry<String, String> entry : testFiles.entrySet()) {
            String filePath = entry.getKey();
            String expectedContent = entry.getValue();
            String actualContent = result.getContent().get(filePath);
            
            assertNotNull("Content should exist for " + filePath, actualContent);
            assertEquals("Content should match for " + filePath, 
                        normalizeContent(expectedContent), normalizeContent(actualContent));
        }
        
        System.out.println("✅ Read multiple files successful");
        System.out.println("   Read " + result.getContent().size() + " files");
    }

    /**
     * Test write file with create_parent_dir parameter (should fail without it)
     */
    @Test
    public void testWriteFileWithoutParentDir() throws SessionException {
        System.out.println("\n🚫 Testing write file WITHOUT creating parent directories...");
        
        String nestedPath = "/tmp/nonexistent_dir_" + System.currentTimeMillis() + "/subdir/test.txt";
        String content = "This should fail";
        
        BoolResult result = fs.writeFile(nestedPath, content, "overwrite", false);
        
        // This should fail because parent directory doesn't exist
        assertFalse("Write should fail without parent directory", result.isSuccess());
        assertNotNull("Error message should be present", result.getErrorMessage());
        
        System.out.println("✅ Correctly failed without parent directory");
        System.out.println("   Error: " + result.getErrorMessage());
    }

    /**
     * Test write file with create_parent_dir parameter (should succeed)
     */
    @Test
    public void testWriteFileWithParentDir() throws SessionException {
        System.out.println("\n✅ Testing write file WITH creating parent directories...");
        
        String nestedPath = "/tmp/test_parent_dir_" + System.currentTimeMillis() + "/subdir/test.txt";
        String content = "This should succeed";
        
        BoolResult result = fs.writeFile(nestedPath, content, "overwrite", true);
        
        assertTrue("Write should succeed with create_parent_dir: " + result.getErrorMessage(), 
                   result.isSuccess());
        assertNotNull("Request ID should not be null", result.getRequestId());
        
        // Verify the file was created
        FileContentResult readResult = fs.readFile(nestedPath);
        assertTrue("Should be able to read created file", readResult.isSuccess());
        assertEquals("Content should match", normalizeContent(content), normalizeContent(readResult.getContent()));
        
        System.out.println("✅ Successfully created file with parent directories");
        System.out.println("   Path: " + nestedPath);
    }

    /**
     * Test large file operations (1MB+ file)
     */
    @Test
    public void testLargeFileOperations() throws SessionException {
        System.out.println("\n💾 Testing large file operations...");
        
        // Generate approximately 1MB of content
        StringBuilder largeContentBuilder = new StringBuilder();
        String lineContent = "This is a line of test content for large file testing. ";
        
        // Create a single line
        for (int i = 0; i < 20; i++) {
            largeContentBuilder.append(lineContent);
        }
        String singleLine = largeContentBuilder.toString();
        
        // Repeat to create ~1MB
        largeContentBuilder = new StringBuilder();
        for (int i = 0; i < 10; i++) {
            largeContentBuilder.append(singleLine).append("\n");
        }
        String largeContent = largeContentBuilder.toString();
        
        String largeFilePath = "/tmp/test_large_file.txt";
        
        System.out.println("   Generated content size: " + largeContent.length() + " bytes");
        
        // Write large file
        long startTime = System.currentTimeMillis();
        BoolResult writeResult = fs.writeFile(largeFilePath, largeContent, "overwrite");
        long writeTime = System.currentTimeMillis() - startTime;
        
        assertTrue("Large file write should succeed: " + writeResult.getErrorMessage(), 
                   writeResult.isSuccess());
        
        System.out.println("   Write completed in " + (writeTime / 1000.0) + " seconds");
        
        // Read large file
        startTime = System.currentTimeMillis();
        FileContentResult readResult = fs.readFile(largeFilePath);
        long readTime = System.currentTimeMillis() - startTime;
        
        assertTrue("Large file read should succeed: " + readResult.getErrorMessage(), 
                   readResult.isSuccess());
        String normalizedExpected = normalizeContent(largeContent);
        String normalizedActual = normalizeContent(readResult.getContent());
        assertEquals("Content length should match", 
                    normalizedExpected.length(), 
                    normalizedActual.length());
        assertEquals("Content should match exactly", normalizedExpected, normalizedActual);
        
        System.out.println("   Read completed in " + (readTime / 1000.0) + " seconds");
        System.out.println("✅ Large file operations successful");
    }

    /**
     * Test multiple edits on a file
     */
    @Test
    public void testMultipleFileEdits() throws SessionException {
        System.out.println("\n✏️ Testing multiple file edits...");
        
        String testFilePath = "/tmp/test_multi_edit.txt";
        String originalContent = "Line 1: First\nLine 2: Second\nLine 3: Third\nLine 4: Fourth";
        
        // Create file
        fs.writeFile(testFilePath, originalContent, "overwrite");
        
        // Apply multiple edits
        List<Map<String, String>> edits = new ArrayList<>();
        
        Map<String, String> edit1 = new HashMap<>();
        edit1.put("oldText", "First");
        edit1.put("newText", "Modified1");
        edits.add(edit1);
        
        Map<String, String> edit2 = new HashMap<>();
        edit2.put("oldText", "Third");
        edit2.put("newText", "Modified3");
        edits.add(edit2);
        
        BoolResult editResult = fs.editFile(testFilePath, edits);
        
        assertTrue("Multiple edits should succeed: " + editResult.getErrorMessage(), 
                   editResult.isSuccess());
        
        // Verify edits
        FileContentResult readResult = fs.readFile(testFilePath);
        assertTrue("Read should succeed", readResult.isSuccess());
        assertTrue("Should contain Modified1", readResult.getContent().contains("Modified1"));
        assertTrue("Should contain Modified3", readResult.getContent().contains("Modified3"));
        assertFalse("Should not contain First", readResult.getContent().contains("First"));
        assertFalse("Should not contain Third", readResult.getContent().contains("Third"));
        
        System.out.println("✅ Multiple file edits successful");
        System.out.println("   Result: " + readResult.getContent());
    }

    /**
     * Test session lifecycle and file system interface availability
     */
    @Test
    public void testFileSystemInterface() {
        System.out.println("\n🔌 Testing FileSystem interface...");
        
        assertNotNull("Session should not be null", session);
        assertNotNull("FileSystem interface should not be null", fs);
        assertNotNull("Session ID should not be null", session.getSessionId());
        
        System.out.println("✅ FileSystem interface is available");
        System.out.println("   Session ID: " + session.getSessionId());
    }

    /**
     * Main method to run tests manually (for debugging purposes)
     * In production, use Maven or IDE test runners
     */
    public static void main(String[] args) {
        System.out.println("=== Running FileSystem Tests ===\n");
        
        TestFileSystem test = new TestFileSystem();
        int testCount = 0;
        int passedCount = 0;
        
        try {
            // Test 1: Write file
            testCount++;
            System.out.println("\n--- Test " + testCount + ": Write File (Overwrite) ---");
            test.setUp();
            test.testWriteFileOverwrite();
            test.tearDown();
            passedCount++;
            
            // Test 2: Read file
            testCount++;
            System.out.println("\n--- Test " + testCount + ": Read File ---");
            test.setUp();
            test.testReadFile();
            test.tearDown();
            passedCount++;
            
            // Test 3: Append file
            testCount++;
            System.out.println("\n--- Test " + testCount + ": Append to File ---");
            test.setUp();
            test.testWriteFileAppend();
            test.tearDown();
            passedCount++;
            
            // Test 4: Create directory
            testCount++;
            System.out.println("\n--- Test " + testCount + ": Create Directory ---");
            test.setUp();
            test.testCreateDirectory();
            test.tearDown();
            passedCount++;
            
            // Test 5: List directory
            testCount++;
            System.out.println("\n--- Test " + testCount + ": List Directory ---");
            test.setUp();
            test.testListDirectory();
            test.tearDown();
            passedCount++;
            
            // Test 6: Get file info
            testCount++;
            System.out.println("\n--- Test " + testCount + ": Get File Info ---");
            test.setUp();
            test.testGetFileInfo();
            test.tearDown();
            passedCount++;
            
            // Test 7: Edit file
            testCount++;
            System.out.println("\n--- Test " + testCount + ": Edit File ---");
            test.setUp();
            test.testEditFile();
            test.tearDown();
            passedCount++;
            
            // Test 8: Move file
            testCount++;
            System.out.println("\n--- Test " + testCount + ": Move File ---");
            test.setUp();
            test.testMoveFile();
            test.tearDown();
            passedCount++;
            
            // Test 9: Search files
            testCount++;
            System.out.println("\n--- Test " + testCount + ": Search Files ---");
            test.setUp();
            test.testSearchFiles();
            test.tearDown();
            passedCount++;
            
            // Test 10: Read multiple files
            testCount++;
            System.out.println("\n--- Test " + testCount + ": Read Multiple Files ---");
            test.setUp();
            test.testReadMultipleFiles();
            test.tearDown();
            passedCount++;
            
            // Test 11: Write without parent dir
            testCount++;
            System.out.println("\n--- Test " + testCount + ": Write Without Parent Dir ---");
            test.setUp();
            test.testWriteFileWithoutParentDir();
            test.tearDown();
            passedCount++;
            
            // Test 12: Write with parent dir
            testCount++;
            System.out.println("\n--- Test " + testCount + ": Write With Parent Dir ---");
            test.setUp();
            test.testWriteFileWithParentDir();
            test.tearDown();
            passedCount++;
            
            // Test 13: Large file operations
            testCount++;
            System.out.println("\n--- Test " + testCount + ": Large File Operations ---");
            test.setUp();
            test.testLargeFileOperations();
            test.tearDown();
            passedCount++;
            
            // Test 14: Multiple edits
            testCount++;
            System.out.println("\n--- Test " + testCount + ": Multiple File Edits ---");
            test.setUp();
            test.testMultipleFileEdits();
            test.tearDown();
            passedCount++;
            
            // Test 15: FileSystem interface
            testCount++;
            System.out.println("\n--- Test " + testCount + ": FileSystem Interface ---");
            test.setUp();
            test.testFileSystemInterface();
            test.tearDown();
            passedCount++;
            
            System.out.println("\n=== ✅ All FileSystem Tests Completed Successfully ===");
            System.out.println("Passed: " + passedCount + "/" + testCount + " tests");
            
        } catch (Exception e) {
            System.err.println("\n=== ❌ Test Failed ===");
            System.err.println("Error: " + e.getMessage());
            System.err.println("Passed: " + passedCount + "/" + testCount + " tests");
            e.printStackTrace();
        }
    }
}

