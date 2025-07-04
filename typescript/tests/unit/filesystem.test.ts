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

      expect(result.data).toBe("file content");
      expect(result.requestId).toBe("test-request-id");

      expect(callMcpToolStub.calledOnce).toBe(true);
    });
  });

  describe("test_read_file_get_false", () => {
    it("should handle read file error", async () => {
      sandbox
        .stub(mockFileSystem as any, "callMcpTool")
        .rejects(new Error("some error message"));

      await expect(
        mockFileSystem.readFile("/path/to/file.txt")
      ).rejects.toThrow("some error message");
    });
  });

  describe("test_read_file_error_format", () => {
    it("should handle invalid response format", async () => {
      sandbox
        .stub(mockFileSystem as any, "callMcpTool")
        .rejects(new Error("Invalid response body"));

      await expect(
        mockFileSystem.readFile("/path/to/file.txt")
      ).rejects.toThrow("Invalid response body");
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

      expect(result.data).toBe("True");
      expect(result.requestId).toBe("test-request-id");
      expect(callMcpToolStub.calledOnce).toBe(true);
    });
  });

  describe("test_create_directory_error", () => {
    it("should handle create directory error", async () => {
      sandbox
        .stub(mockFileSystem as any, "callMcpTool")
        .rejects(new Error("Directory creation failed"));

      await expect(
        mockFileSystem.createDirectory("/path/to/directory")
      ).rejects.toThrow("Directory creation failed");
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

      expect(result.data).toBe("True");
      expect(result.requestId).toBe("test-request-id");
      expect(callMcpToolStub.calledOnce).toBe(true);
    });
  });

  describe("test_edit_file_error", () => {
    it("should handle edit file error", async () => {
      sandbox
        .stub(mockFileSystem as any, "callMcpTool")
        .rejects(new Error("Edit failed"));

      await expect(
        mockFileSystem.editFile("/path/to/file.txt", [
          { oldText: "foo", newText: "bar" },
        ])
      ).rejects.toThrow("Edit failed");
    });
  });

  describe("test_write_file_success", () => {
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

      const result = await mockFileSystem.writeFile(
        "/path/to/file.txt",
        "content to write",
        "overwrite"
      );

      expect(result.data).toBe("True");
      expect(result.requestId).toBe("test-request-id");
      expect(callMcpToolStub.calledOnce).toBe(true);
    });
  });

  describe("test_write_file_error", () => {
    it("should handle write file error", async () => {
      sandbox
        .stub(mockFileSystem as any, "callMcpTool")
        .rejects(new Error("Write failed"));

      await expect(
        mockFileSystem.writeFile(
          "/path/to/file.txt",
          "content to write",
          "overwrite"
        )
      ).rejects.toThrow("Write failed");
    });
  });

  describe("test_get_file_info_success", () => {
    it("should get file info successfully", async () => {
      const callMcpToolStub = sandbox
        .stub(mockFileSystem as any, "callMcpTool")
        .resolves({
          data: {},
          textContent:
            "size: 36\nisDirectory: false\nisFile: true\npermissions: rw-r--r--",
          isError: false,
          statusCode: 200,
          requestId: "test-request-id",
        });

      const result = await mockFileSystem.getFileInfo("/path/to/file.txt");

      expect(result.data.size).toBe(36);
      expect(result.data.isDirectory).toBe(false);
      expect(result.requestId).toBe("test-request-id");
      expect(callMcpToolStub.calledOnce).toBe(true);
    });
  });

  describe("test_get_file_info_error", () => {
    it("should handle get file info error", async () => {
      sandbox
        .stub(mockFileSystem as any, "callMcpTool")
        .rejects(new Error("File not found"));

      await expect(
        mockFileSystem.getFileInfo("/path/to/file.txt")
      ).rejects.toThrow("File not found");
    });
  });

  describe("test_list_directory_success", () => {
    it("should list directory successfully", async () => {
      const callMcpToolStub = sandbox
        .stub(mockFileSystem as any, "callMcpTool")
        .resolves({
          data: {},
          textContent: "[DIR] subdir\n [FILE] file1.txt",
          isError: false,
          statusCode: 200,
          requestId: "test-request-id",
        });

      const result = await mockFileSystem.listDirectory("/path/to/directory");

      expect(result.data).toHaveLength(2);
      expect(result.data[0].name).toBe("subdir");
      expect(result.data[0].isDirectory).toBe(true);
      expect(result.data[1].name).toBe("file1.txt");
      expect(result.data[1].isDirectory).toBe(false);
      expect(result.requestId).toBe("test-request-id");
      expect(callMcpToolStub.calledOnce).toBe(true);
    });
  });

  describe("test_list_directory_error", () => {
    it("should handle list directory error", async () => {
      sandbox
        .stub(mockFileSystem as any, "callMcpTool")
        .rejects(new Error("Directory not found"));

      await expect(
        mockFileSystem.listDirectory("/path/to/directory")
      ).rejects.toThrow("Directory not found");
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

      expect(result.data).toBe("True");
      expect(result.requestId).toBe("test-request-id");
      expect(callMcpToolStub.calledOnce).toBe(true);
    });
  });

  describe("test_move_file_error", () => {
    it("should handle move file error", async () => {
      sandbox
        .stub(mockFileSystem as any, "callMcpTool")
        .rejects(new Error("Move failed"));

      await expect(
        mockFileSystem.moveFile(
          "/path/to/source.txt",
          "/path/to/destination.txt"
        )
      ).rejects.toThrow("Move failed");
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

      expect(result["/path/to/file1.txt"]).toBe("Content of file1");
      expect(result["/path/to/file2.txt"]).toBe("Content of file2");
      expect(callMcpToolStub.calledOnce).toBe(true);
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

      expect(result.data).toHaveLength(2);
      expect(result.data[0]).toBe("/path/to/file1.txt");
      expect(result.data[1]).toBe("/path/to/file2.txt");
      expect(result.requestId).toBe("test-request-id");
      expect(callMcpToolStub.calledOnce).toBe(true);
    });
  });

  describe("test_read_large_file_success", () => {
    it("should read large file successfully", async () => {
      // Mock getFileInfo to return a file size of 150KB
      const getFileInfoStub = sandbox
        .stub(mockFileSystem, "getFileInfo")
        .resolves({
          data: {
            size: 150 * 1024,
            isDirectory: false,
            name: "",
            path: "",
            modTime: "",
            mode: "",
          },
          requestId: "test-request-id",
        });

      // Mock readFile to return chunks of content
      const readFileStub = sandbox
        .stub(mockFileSystem, "readFile")
        .onFirstCall()
        .resolves({ data: "chunk1_content", requestId: "test-request-id" })
        .onSecondCall()
        .resolves({ data: "chunk2_content", requestId: "test-request-id" })
        .onThirdCall()
        .resolves({ data: "chunk3_content", requestId: "test-request-id" });

      // Set a smaller chunk size for testing (50KB)
      const testChunkSize = 50 * 1024;

      const result = await mockFileSystem.readLargeFile(
        "/path/to/large_file.txt",
        testChunkSize
      );

      // Verify the result is the concatenation of all chunks
      expect(result).toBe("chunk1_contentchunk2_contentchunk3_content");

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

  describe("test_read_large_file_error", () => {
    it("should handle read large file error", async () => {
      // Mock getFileInfo to raise an error
      sandbox
        .stub(mockFileSystem, "getFileInfo")
        .rejects(new Error("File not found"));

      await expect(
        mockFileSystem.readLargeFile("/path/to/nonexistent_file.txt")
      ).rejects.toThrow("File not found");
    });
  });

  describe("test_write_large_file_success", () => {
    it("should write large file successfully", async () => {
      // Mock writeFile to return True
      const writeFileStub = sandbox
        .stub(mockFileSystem, "writeFile")
        .resolves({ data: "True", requestId: "test-request-id" });

      // Create a large content string (150KB)
      const largeContent = "x".repeat(150 * 1024);

      // Set a smaller chunk size for testing (50KB)
      const testChunkSize = 50 * 1024;

      const result = await mockFileSystem.writeLargeFile(
        "/path/to/large_file.txt",
        largeContent,
        testChunkSize
      );

      // Verify the result is True
      expect(result).toBe(true);

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
      // Mock writeFile to return True
      const writeFileStub = sandbox
        .stub(mockFileSystem, "writeFile")
        .resolves({ data: "True", requestId: "test-request-id" });

      // Create a small content string (10KB)
      const smallContent = "x".repeat(10 * 1024);

      // Set a larger chunk size for testing (50KB)
      const testChunkSize = 50 * 1024;

      const result = await mockFileSystem.writeLargeFile(
        "/path/to/small_file.txt",
        smallContent,
        testChunkSize
      );

      // Verify the result is True
      expect(result).toBe(true);

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

  describe("test_write_large_file_error", () => {
    it("should handle write large file error", async () => {
      // Mock writeFile to raise an error
      sandbox
        .stub(mockFileSystem, "writeFile")
        .rejects(new Error("Failed to write large file"));

      // Create a large content string (150KB)
      const largeContent = "x".repeat(150 * 1024);

      await expect(
        mockFileSystem.writeLargeFile("/path/to/large_file.txt", largeContent)
      ).rejects.toThrow("Failed to write large file");
    });
  });
});
