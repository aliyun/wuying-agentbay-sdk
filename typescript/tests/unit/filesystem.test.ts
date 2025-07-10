import { FileSystem } from "../../src/filesystem/filesystem";
import { APIError } from "../../src/exceptions";
import * as sinon from "sinon";

describe("TestFileSystem", () => {
  let mockFileSystem: FileSystem;
  let mockSession: any;
  let sandbox: sinon.SinonSandbox;

  beforeEach(() => {
    sandbox = sinon.createSandbox();

    mockSession = {
      getAPIKey: sandbox.stub().returns("dummy_key"),
      getClient: sandbox.stub(),
      getSessionId: sandbox.stub().returns("dummy_session"),
    };

    mockFileSystem = new FileSystem(mockSession);
  });

  afterEach(() => {
    sandbox.restore();
  });

  describe("test_read_file_success", () => {
    it("should read file successfully", async () => {
      const callMcpToolStub = sandbox
        .stub(mockFileSystem as any, "callMcpTool")
        .resolves({
          data: {},
          textContent: "file content",
          isError: false,
          statusCode: 200,
          requestId: "test-request-id",
        });

      const result = await mockFileSystem.readFile("/path/to/file.txt");

      // Verify FileContentResult structure
      expect(result.success).toBe(true);
      expect(result.requestId).toBe("test-request-id");
      expect(result.content).toBe("file content");
      expect(result.errorMessage).toBeUndefined();

      expect(callMcpToolStub.calledOnce).toBe(true);
    });
  });

  describe("test_read_file_failure", () => {
    it("should handle read file error", async () => {
      sandbox
        .stub(mockFileSystem as any, "callMcpTool")
        .rejects(new Error("some error message"));

      const result = await mockFileSystem.readFile("/path/to/file.txt");

      // Verify error result structure
      expect(result.success).toBe(false);
      expect(result.requestId).toBe("");
      expect(result.content).toBe("");
      expect(result.errorMessage).toContain("Failed to read file");
    });
  });

  describe("test_create_directory_success", () => {
    it("should create directory successfully", async () => {
      const callMcpToolStub = sandbox
        .stub(mockFileSystem as any, "callMcpTool")
        .resolves({
          data: {},
          textContent: "True",
          isError: false,
          statusCode: 200,
          requestId: "test-request-id",
        });

      const result = await mockFileSystem.createDirectory("/path/to/directory");

      // Verify BoolResult structure
      expect(result.success).toBe(true);
      expect(result.requestId).toBe("test-request-id");
      expect(result.data).toBe(true);
      expect(result.errorMessage).toBeUndefined();

      expect(callMcpToolStub.calledOnce).toBe(true);
    });
  });

  describe("test_create_directory_failure", () => {
    it("should handle create directory error", async () => {
      sandbox
        .stub(mockFileSystem as any, "callMcpTool")
        .rejects(new Error("Directory creation failed"));

      const result = await mockFileSystem.createDirectory("/path/to/directory");

      // Verify error result structure
      expect(result.success).toBe(false);
      expect(result.requestId).toBe("");
      expect(result.errorMessage).toContain("Failed to create directory");
    });
  });

  describe("test_edit_file_success", () => {
    it("should edit file successfully", async () => {
      const callMcpToolStub = sandbox
        .stub(mockFileSystem as any, "callMcpTool")
        .resolves({
          data: {},
          textContent: "True",
          isError: false,
          statusCode: 200,
          requestId: "test-request-id",
        });

      const result = await mockFileSystem.editFile("/path/to/file.txt", [
        { oldText: "foo", newText: "bar" },
      ]);

      // Verify BoolResult structure
      expect(result.success).toBe(true);
      expect(result.requestId).toBe("test-request-id");
      expect(result.data).toBe(true);
      expect(result.errorMessage).toBeUndefined();

      expect(callMcpToolStub.calledOnce).toBe(true);
    });
  });

  describe("test_edit_file_failure", () => {
    it("should handle edit file error", async () => {
      sandbox
        .stub(mockFileSystem as any, "callMcpTool")
        .rejects(new Error("Edit failed"));

      const result = await mockFileSystem.editFile("/path/to/file.txt", [
        { oldText: "foo", newText: "bar" },
      ]);

      // Verify error result structure
      expect(result.success).toBe(false);
      expect(result.requestId).toBe("");
      expect(result.errorMessage).toContain("Failed to edit file");
    });
  });

  describe("test_write_file_success", () => {
    it("should write file successfully", async () => {
      const callMcpToolStub = sandbox
        .stub(mockFileSystem as any, "callMcpTool")
        .resolves({
          data: {},
          textContent: "True",
          isError: false,
          statusCode: 200,
          requestId: "test-request-id",
        });

      const result = await mockFileSystem.writeFile(
        "/path/to/file.txt",
        "content to write",
        "overwrite"
      );

      // Verify BoolResult structure
      expect(result.success).toBe(true);
      expect(result.requestId).toBe("test-request-id");
      expect(result.data).toBe(true);
      expect(result.errorMessage).toBeUndefined();

      expect(callMcpToolStub.calledOnce).toBe(true);
    });
  });

  describe("test_write_file_failure", () => {
    it("should handle write file error", async () => {
      sandbox
        .stub(mockFileSystem as any, "callMcpTool")
        .rejects(new Error("Write failed"));

      const result = await mockFileSystem.writeFile(
        "/path/to/file.txt",
        "content to write",
        "overwrite"
      );

      // Verify error result structure
      expect(result.success).toBe(false);
      expect(result.requestId).toBe("");
      expect(result.errorMessage).toContain("Failed to write file");
    });
  });

  describe("test_write_file_invalid_mode", () => {
    it("should handle invalid write mode", async () => {
      const result = await mockFileSystem.writeFile(
        "/path/to/file.txt",
        "content to write",
        "invalid_mode" as any
      );

      // Verify error result structure
      expect(result.success).toBe(false);
      expect(result.requestId).toBe("");
      expect(result.errorMessage).toContain("Invalid mode: invalid_mode");
    });
  });

  describe("test_get_file_info_success", () => {
    it("should get file info successfully", async () => {
      const callMcpToolStub = sandbox
        .stub(mockFileSystem as any, "callMcpTool")
        .resolves({
          data: {},
          textContent:
            "name: file.txt\npath: /path/to/file.txt\nsize: 36\nisDirectory: false\nmodTime: 2023-01-01T00:00:00Z\nmode: rw-r--r--",
          isError: false,
          statusCode: 200,
          requestId: "test-request-id",
        });

      const result = await mockFileSystem.getFileInfo("/path/to/file.txt");

      // Verify FileInfoResult structure
      expect(result.success).toBe(true);
      expect(result.requestId).toBe("test-request-id");
      expect(result.fileInfo).toBeDefined();
      expect(result.errorMessage).toBeUndefined();

      expect(result.fileInfo!.size).toBe(36);
      expect(result.fileInfo!.isDirectory).toBe(false);
      expect(result.fileInfo!.name).toBe("file.txt");
      expect(result.fileInfo!.path).toBe("/path/to/file.txt");

      expect(callMcpToolStub.calledOnce).toBe(true);
    });
  });

  describe("test_get_file_info_failure", () => {
    it("should handle get file info error", async () => {
      sandbox
        .stub(mockFileSystem as any, "callMcpTool")
        .rejects(new Error("File not found"));

      const result = await mockFileSystem.getFileInfo("/path/to/file.txt");

      // Verify error result structure
      expect(result.success).toBe(false);
      expect(result.requestId).toBe("");
      expect(result.errorMessage).toContain("Failed to get file info");
    });
  });

  describe("test_list_directory_success", () => {
    it("should list directory successfully", async () => {
      const callMcpToolStub = sandbox
        .stub(mockFileSystem as any, "callMcpTool")
        .resolves({
          data: {},
          textContent: "[DIR] subdir\n[FILE] file1.txt",
          isError: false,
          statusCode: 200,
          requestId: "test-request-id",
        });

      const result = await mockFileSystem.listDirectory("/path/to/directory");

      // Verify DirectoryListResult structure
      expect(result.success).toBe(true);
      expect(result.requestId).toBe("test-request-id");
      expect(result.entries).toHaveLength(2);
      expect(result.errorMessage).toBeUndefined();

      expect(result.entries[0].name).toBe("subdir");
      expect(result.entries[0].isDirectory).toBe(true);
      expect(result.entries[1].name).toBe("file1.txt");
      expect(result.entries[1].isDirectory).toBe(false);

      expect(callMcpToolStub.calledOnce).toBe(true);
    });
  });

  describe("test_list_directory_failure", () => {
    it("should handle list directory error", async () => {
      sandbox
        .stub(mockFileSystem as any, "callMcpTool")
        .rejects(new Error("Directory not found"));

      const result = await mockFileSystem.listDirectory("/path/to/directory");

      // Verify error result structure
      expect(result.success).toBe(false);
      expect(result.requestId).toBe("");
      expect(result.entries).toEqual([]);
      expect(result.errorMessage).toContain("Failed to list directory");
    });
  });

  describe("test_move_file_success", () => {
    it("should move file successfully", async () => {
      const callMcpToolStub = sandbox
        .stub(mockFileSystem as any, "callMcpTool")
        .resolves({
          data: {},
          textContent: "True",
          isError: false,
          statusCode: 200,
          requestId: "test-request-id",
        });

      const result = await mockFileSystem.moveFile(
        "/path/to/source.txt",
        "/path/to/destination.txt"
      );

      // Verify BoolResult structure
      expect(result.success).toBe(true);
      expect(result.requestId).toBe("test-request-id");
      expect(result.data).toBe(true);
      expect(result.errorMessage).toBeUndefined();

      expect(callMcpToolStub.calledOnce).toBe(true);
    });
  });

  describe("test_move_file_failure", () => {
    it("should handle move file error", async () => {
      sandbox
        .stub(mockFileSystem as any, "callMcpTool")
        .rejects(new Error("Move failed"));

      const result = await mockFileSystem.moveFile(
        "/path/to/source.txt",
        "/path/to/destination.txt"
      );

      // Verify error result structure
      expect(result.success).toBe(false);
      expect(result.requestId).toBe("");
      expect(result.errorMessage).toContain("Failed to move file");
    });
  });

  describe("test_read_multiple_files_success", () => {
    it("should read multiple files successfully", async () => {
      const callMcpToolStub = sandbox
        .stub(mockFileSystem as any, "callMcpTool")
        .resolves({
          data: {},
          textContent:
            "/path/to/file1.txt: Content of file1\n\n---\n/path/to/file2.txt: \nContent of file2\n",
          isError: false,
          statusCode: 200,
          requestId: "test-request-id",
        });

      const result = await mockFileSystem.readMultipleFiles([
        "/path/to/file1.txt",
        "/path/to/file2.txt",
      ]);

      // Verify MultipleFileContentResult structure
      expect(result.success).toBe(true);
      expect(result.requestId).toBe("test-request-id");
      expect(result.contents["/path/to/file1.txt"]).toBe("Content of file1");
      expect(result.contents["/path/to/file2.txt"]).toBe("Content of file2");
      expect(result.errorMessage).toBeUndefined();

      expect(callMcpToolStub.calledOnce).toBe(true);
    });
  });

  describe("test_read_multiple_files_failure", () => {
    it("should handle read multiple files error", async () => {
      sandbox
        .stub(mockFileSystem as any, "callMcpTool")
        .rejects(new Error("API Error"));

      const result = await mockFileSystem.readMultipleFiles([
        "/path/to/file1.txt",
        "/path/to/file2.txt",
      ]);

      // Verify error result structure
      expect(result.success).toBe(false);
      expect(result.requestId).toBe("");
      expect(result.contents).toEqual({});
      expect(result.errorMessage).toContain("Failed to read multiple files");
    });
  });

  describe("test_search_files_success", () => {
    it("should search files successfully", async () => {
      const callMcpToolStub = sandbox
        .stub(mockFileSystem as any, "callMcpTool")
        .resolves({
          data: {},
          textContent: "/path/to/file1.txt\n/path/to/file2.txt",
          isError: false,
          statusCode: 200,
          requestId: "test-request-id",
        });

      const result = await mockFileSystem.searchFiles(
        "/path/to/directory",
        "pattern",
        ["ignored_pattern"]
      );

      // Verify FileSearchResult structure
      expect(result.success).toBe(true);
      expect(result.requestId).toBe("test-request-id");
      expect(result.matches).toHaveLength(2);
      expect(result.matches[0]).toBe("/path/to/file1.txt");
      expect(result.matches[1]).toBe("/path/to/file2.txt");
      expect(result.errorMessage).toBeUndefined();

      expect(callMcpToolStub.calledOnce).toBe(true);
    });
  });

  describe("test_search_files_failure", () => {
    it("should handle search files error", async () => {
      sandbox
        .stub(mockFileSystem as any, "callMcpTool")
        .rejects(new Error("API Error"));

      const result = await mockFileSystem.searchFiles(
        "/path/to/directory",
        "pattern"
      );

      // Verify error result structure
      expect(result.success).toBe(false);
      expect(result.requestId).toBe("");
      expect(result.matches).toEqual([]);
      expect(result.errorMessage).toContain("Failed to search files");
    });
  });

  describe("test_read_large_file_success", () => {
    it("should read large file successfully", async () => {
      // Mock getFileInfo to return a file size of 150KB
      const getFileInfoStub = sandbox
        .stub(mockFileSystem, "getFileInfo")
        .resolves({
          success: true,
          requestId: "test-request-id",
          fileInfo: {
            size: 150 * 1024,
            isDirectory: false,
            name: "large_file.txt",
            path: "/path/to/large_file.txt",
            modTime: "2023-01-01T00:00:00Z",
            mode: "rw-r--r--",
          },
        });

      // Mock readFile to return chunks of content
      const readFileStub = sandbox
        .stub(mockFileSystem, "readFile")
        .onFirstCall()
        .resolves({
          success: true,
          requestId: "test-request-id",
          content: "chunk1_content"
        })
        .onSecondCall()
        .resolves({
          success: true,
          requestId: "test-request-id",
          content: "chunk2_content"
        })
        .onThirdCall()
        .resolves({
          success: true,
          requestId: "test-request-id",
          content: "chunk3_content"
        });

      // Set a smaller chunk size for testing (50KB)
      const testChunkSize = 50 * 1024;

      const result = await mockFileSystem.readLargeFile(
        "/path/to/large_file.txt",
        testChunkSize
      );

      // Verify FileContentResult structure
      expect(result.success).toBe(true);
      expect(result.requestId).toBe("test-request-id");
      expect(result.content).toBe("chunk1_contentchunk2_contentchunk3_content");
      expect(result.errorMessage).toBeUndefined();

      // Verify getFileInfo was called once
      expect(getFileInfoStub.calledOnce).toBe(true);

      // Verify readFile was called three times
      expect(readFileStub.callCount).toBe(3);
      expect(
        readFileStub
          .getCall(0)
          .calledWith("/path/to/large_file.txt", 0, testChunkSize)
      ).toBe(true);
      expect(
        readFileStub
          .getCall(1)
          .calledWith("/path/to/large_file.txt", testChunkSize, testChunkSize)
      ).toBe(true);
      expect(
        readFileStub
          .getCall(2)
          .calledWith(
            "/path/to/large_file.txt",
            testChunkSize * 2,
            testChunkSize
          )
      ).toBe(true);
    });
  });

  describe("test_read_large_file_failure", () => {
    it("should handle read large file error", async () => {
      // Mock getFileInfo to return error
      sandbox
        .stub(mockFileSystem, "getFileInfo")
        .resolves({
          success: false,
          requestId: "",
          errorMessage: "File not found"
        });

      const result = await mockFileSystem.readLargeFile("/path/to/nonexistent_file.txt");

      // Verify error result structure
      expect(result.success).toBe(false);
      expect(result.requestId).toBe("");
      expect(result.content).toBe("");
      expect(result.errorMessage).toContain("File not found");
    });
  });

  describe("test_write_large_file_success", () => {
    it("should write large file successfully", async () => {
      // Mock writeFile to return success
      const writeFileStub = sandbox
        .stub(mockFileSystem, "writeFile")
        .resolves({
          success: true,
          requestId: "test-request-id",
          data: true
        });

      // Create a large content string (150KB)
      const largeContent = "x".repeat(150 * 1024);

      // Set a smaller chunk size for testing (50KB)
      const testChunkSize = 50 * 1024;

      const result = await mockFileSystem.writeLargeFile(
        "/path/to/large_file.txt",
        largeContent,
        testChunkSize
      );

      // Verify BoolResult structure
      expect(result.success).toBe(true);
      expect(result.requestId).toBe("test-request-id");
      expect(result.data).toBe(true);
      expect(result.errorMessage).toBeUndefined();

      // Verify writeFile was called three times with correct chunks
      expect(writeFileStub.callCount).toBe(3);
      expect(
        writeFileStub
          .getCall(0)
          .calledWith(
            "/path/to/large_file.txt",
            largeContent.substring(0, testChunkSize),
            "overwrite"
          )
      ).toBe(true);
      expect(
        writeFileStub
          .getCall(1)
          .calledWith(
            "/path/to/large_file.txt",
            largeContent.substring(testChunkSize, testChunkSize * 2),
            "append"
          )
      ).toBe(true);
      expect(
        writeFileStub
          .getCall(2)
          .calledWith(
            "/path/to/large_file.txt",
            largeContent.substring(testChunkSize * 2),
            "append"
          )
      ).toBe(true);
    });
  });

  describe("test_write_large_file_small_content", () => {
    it("should write large file with small content", async () => {
      // Mock writeFile to return success
      const writeFileStub = sandbox
        .stub(mockFileSystem, "writeFile")
        .resolves({
          success: true,
          requestId: "test-request-id",
          data: true
        });

      // Create a small content string (10KB)
      const smallContent = "x".repeat(10 * 1024);

      // Set a larger chunk size for testing (50KB)
      const testChunkSize = 50 * 1024;

      const result = await mockFileSystem.writeLargeFile(
        "/path/to/small_file.txt",
        smallContent,
        testChunkSize
      );

      // Verify BoolResult structure
      expect(result.success).toBe(true);
      expect(result.requestId).toBe("test-request-id");
      expect(result.data).toBe(true);
      expect(result.errorMessage).toBeUndefined();

      // Verify writeFile was called once with the entire content
      expect(
        writeFileStub.calledOnceWith(
          "/path/to/small_file.txt",
          smallContent,
          "overwrite"
        )
      ).toBe(true);
    });
  });

  describe("test_write_large_file_failure", () => {
    it("should handle write large file error", async () => {
      // Mock writeFile to return error
      sandbox
        .stub(mockFileSystem, "writeFile")
        .resolves({
          success: false,
          requestId: "",
          errorMessage: "Failed to write large file"
        });

      // Create a large content string (150KB)
      const largeContent = "x".repeat(150 * 1024);

      const result = await mockFileSystem.writeLargeFile("/path/to/large_file.txt", largeContent);

      // Verify error result structure
      expect(result.success).toBe(false);
      expect(result.requestId).toBe("");
      expect(result.errorMessage).toContain("Failed to write large file");
    });
  });
});
