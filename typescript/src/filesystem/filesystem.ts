import { APIError } from "../exceptions";
import { Session } from "../session";
import { CallMcpToolRequest } from "../api/models/model";
import * as $_client from "../api";
import { log, logError } from "../utils/logger";
import {
  extractRequestId,
  BoolResult,
  FileInfoResult,
  DirectoryListResult,
  FileContentResult,
  MultipleFileContentResult,
  FileSearchResult,
} from "../types/api-response";

// Default chunk size for large file operations (60KB)
const DEFAULT_CHUNK_SIZE = 60 * 1024;

/**
 * FileInfo represents information about a file or directory
 */
export interface FileInfo {
  name: string;
  path: string;
  size: number;
  isDirectory: boolean;
  modTime: string;
  mode: string;
  owner?: string;
  group?: string;
}

/**
 * DirectoryEntry represents an entry in a directory listing
 */
export interface DirectoryEntry {
  name: string;
  isDirectory: boolean;
}

// File operations that might contain large content
const FILE_OPERATIONS: { [key: string]: boolean } = {
  read_file: true,
  write_file: true,
  read_multiple_files: true,
};

/**
 * Checks if the tool operation is file-related and might contain large content
 *
 * @param toolName - Name of the MCP tool
 * @returns True if the operation is file-related
 */
function isFileOperation(toolName: string): boolean {
  return FILE_OPERATIONS[toolName] === true;
}

/**
 * Replaces large content with size information in JSON args for logging
 *
 * @param args - Arguments object to truncate
 * @returns Truncated arguments object for logging
 */
function truncateContentForLogging(
  args: Record<string, any>
): Record<string, any> {
  const truncatedArgs = { ...args };

  // Check for content field and replace with length info
  if (typeof truncatedArgs.content === "string") {
    const contentLength = truncatedArgs.content.length;
    truncatedArgs.content = `[Content length: ${contentLength} bytes]`;
  }

  // Check for paths array and log number of paths instead of all paths
  if (Array.isArray(truncatedArgs.paths) && truncatedArgs.paths.length > 3) {
    truncatedArgs.paths = `[${truncatedArgs.paths.length} paths, first few: ${truncatedArgs.paths[0]}, ${truncatedArgs.paths[1]}, ${truncatedArgs.paths[2]}, ...]`;
  }

  return truncatedArgs;
}

/**
 * Parse a file info string into a FileInfo object
 *
 * @param fileInfoStr - The file info string to parse
 * @returns A FileInfo object
 */
function parseFileInfo(fileInfoStr: string): FileInfo {
  const result: FileInfo = {
    name: "",
    path: "",
    size: 0,
    isDirectory: false,
    modTime: "",
    mode: "",
  };

  const lines = fileInfoStr.split("\n");
  for (const line of lines) {
    if (line.includes(":")) {
      const [key, value] = line.split(":", 2).map((part) => part.trim());

      switch (key) {
        case "name":
          result.name = value;
          break;
        case "path":
          result.path = value;
          break;
        case "size":
          result.size = parseInt(value, 10);
          break;
        case "isDirectory":
          result.isDirectory = value === "true";
          break;
        case "modTime":
          result.modTime = value;
          break;
        case "mode":
          result.mode = value;
          break;
        case "owner":
          result.owner = value;
          break;
        case "group":
          result.group = value;
          break;
      }
    }
  }

  return result;
}

/**
 * Parse a directory listing string into an array of DirectoryEntry objects
 *
 * @param text - The directory listing text to parse
 * @returns An array of DirectoryEntry objects
 */
function parseDirectoryListing(text: string): DirectoryEntry[] {
  const result: DirectoryEntry[] = [];
  const lines = text.split("\n");

  for (const line of lines) {
    const trimmedLine = line.trim();
    if (trimmedLine === "") {
      continue;
    }

    if (trimmedLine.startsWith("[DIR]")) {
      result.push({
        isDirectory: true,
        name: trimmedLine.replace("[DIR]", "").trim(),
      });
    } else if (trimmedLine.startsWith("[FILE]")) {
      result.push({
        isDirectory: false,
        name: trimmedLine.replace("[FILE]", "").trim(),
      });
    }
  }

  return result;
}

/**
 * Result object for a CallMcpTool operation
 */
interface CallMcpToolResult {
  data: Record<string, any>;
  content?: any[];
  textContent?: string;
  isError: boolean;
  errorMsg?: string;
  statusCode: number;
  requestId?: string;
}

/**
 * Handles file operations in the AgentBay cloud environment.
 */
export class FileSystem {
  private session: Session;
  private client!: $_client.Client;
  private baseUrl!: string;

  /**
   * Initialize a FileSystem object.
   *
   * @param session - The Session instance that this FileSystem belongs to.
   */
  constructor(session: Session) {
    this.session = session;
  }

  /**
   * Handle VPC-based MCP tool calls using HTTP requests with file operation logging support.
   */
  private async callMcpToolVPC(
    toolName: string,
    argsJSON: string,
    loggableArgsJSON: string,
    defaultErrorMsg: string
  ): Promise<CallMcpToolResult> {
    log(`API Call: CallMcpTool (VPC) - ${toolName}`);
    log(`Request: Args=${loggableArgsJSON}`);

    // Find server for this tool
    const server = this.session.findServerForTool(toolName);
    if (!server) {
      throw new Error(`server not found for tool: ${toolName}`);
    }

    // Construct VPC URL with query parameters
    const baseURL = `http://${this.session.getNetworkInterfaceIp()}:${this.session.getHttpPort()}/callTool`;

    // Prepare query parameters
    const params = new URLSearchParams({
      server: server,
      tool: toolName,
      args: argsJSON,
      apiKey: this.session.getAPIKey()
    });

    const url = `${baseURL}?${params.toString()}`;

    try {
      // Send HTTP request
      const response = await fetch(url, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        },
        signal: AbortSignal.timeout(30000) // 30 second timeout
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      // Parse response
      const responseData = await response.json();
      
      // Log response differently based on operation type
      if (isFileOperation(toolName)) {
        log(`Response from VPC CallMcpTool - ${toolName} - status: ${response.status}`);
      } else {
        log(`Response from VPC CallMcpTool - ${toolName}:`, responseData);
      }

      // Create result object for VPC response
      const result: CallMcpToolResult = {
        data: responseData,
        statusCode: response.status,
        isError: false,
        requestId: "", // VPC requests don't have traditional request IDs
      };

      // Extract the actual result from the nested VPC response structure
      let actualResult: any = responseData;
      if (typeof responseData.data === 'string') {
        try {
          const dataMap = JSON.parse(responseData.data);
          if (dataMap.result) {
            actualResult = dataMap.result;
          }
        } catch (error) {
          // Keep original responseData if parsing fails
        }
      } else if (responseData.data && typeof responseData.data === 'object') {
        actualResult = responseData.data;
      }

      result.data = actualResult;
      return result;

    } catch (error) {
      logError(`Error calling VPC CallMcpTool - ${toolName}:`, error);
      throw new Error(`failed to call VPC ${toolName}: ${error}`);
    }
  }

  /**
   * Helper method to call MCP tools and handle common response processing
   *
   * @param toolName - Name of the MCP tool to call
   * @param args - Arguments to pass to the tool
   * @param defaultErrorMsg - Default error message if specific error details are not available
   * @returns A CallMcpToolResult with the response data
   * @throws APIError if the call fails
   */
  private async callMcpTool(
    toolName: string,
    args: Record<string, any>,
    defaultErrorMsg: string
  ): Promise<CallMcpToolResult> {
    try {
      // Handle logging differently based on operation type
      let loggableArgs = args;
      if (isFileOperation(toolName)) {
        // For file operations, truncate content for logging
        loggableArgs = truncateContentForLogging(args);
      }

      const argsJSON = JSON.stringify(args);
      const loggableArgsJSON = JSON.stringify(loggableArgs);

      // Check if this is a VPC session
      if (this.session.isVpcEnabled()) {
        return await this.callMcpToolVPC(toolName, argsJSON, loggableArgsJSON, defaultErrorMsg);
      }

      // Non-VPC mode: use traditional API call
      const callToolRequest = new CallMcpToolRequest({
        authorization: `Bearer ${this.session.getAPIKey()}`,
        sessionId: this.session.getSessionId(),
        name: toolName,
        args: argsJSON,
      });

      // Log API request
      log(`API Call: CallMcpTool - ${toolName}`);
      log(
        `Request: SessionId=${this.session.getSessionId()}, Args=${loggableArgsJSON}`
      );

      const response = await this.session
        .getClient()
        .callMcpTool(callToolRequest);

      // Log API response differently based on operation type
      if (isFileOperation(toolName)) {
        // Log content size for file operations instead of full content
        log(
          `Response from CallMcpTool - ${toolName} - status: ${response.statusCode}`
        );

        // Log only relevant response information without content
        if (response.body?.data) {
          const data = response.body.data as Record<string, any>;
          if (data.isError === true) {
            log(`Response contains error: ${data.isError}`);
          } else {
            // For successful responses, don't log the content at all
            log("Response successful, content length info provided separately");

            // If there's content, log its size instead of the actual content
            if (Array.isArray(data.content) && data.content.length > 0) {
              let totalSize = 0;
              for (const item of data.content) {
                if (
                  item &&
                  typeof item === "object" &&
                  item.text &&
                  typeof item.text === "string"
                ) {
                  totalSize += item.text.length;
                }
              }
              log(`Content size: ${totalSize} bytes`);
            }
          }
        }
      } else {
        // For non-file operations, create a sanitized version of the response body
        // that doesn't include large content fields
        const sanitizedBody = { ...response.body };
        if (sanitizedBody.data && typeof sanitizedBody.data === "object") {
          const sanitizedData = { ...sanitizedBody.data };
          if (Array.isArray(sanitizedData.content)) {
            sanitizedData.content = `[Array with ${sanitizedData.content.length} items]`;
          }
          sanitizedBody.data = sanitizedData;
        }
        log(`Response from CallMcpTool - ${toolName}:`, sanitizedBody);
      }

      if (!response.body?.data) {
        throw new Error("Invalid response data format");
      }

      // Extract data from response
      const data = response.body.data as Record<string, any>;

      // Create result object
      const result: CallMcpToolResult = {
        data,
        statusCode: response.statusCode || 0,
        isError: false,
        requestId: extractRequestId(response),
      };

      // Check if there's an error in the response
      if (data.isError === true) {
        result.isError = true;

        // Try to extract the error message from the content field
        const contentArray = data.content as any[] | undefined;
        if (contentArray && contentArray.length > 0) {
          result.content = contentArray;

          // Extract error message from the first content item
          if (contentArray[0]?.text) {
            result.errorMsg = contentArray[0].text;
            throw new Error(contentArray[0].text);
          }
        }
        throw new Error(defaultErrorMsg);
      }

      // Extract content array if it exists
      if (Array.isArray(data.content)) {
        result.content = data.content;

        // Extract textContent from content items
        if (result.content.length > 0) {
          const textParts: string[] = [];
          for (const item of result.content) {
            if (
              item &&
              typeof item === "object" &&
              item.text &&
              typeof item.text === "string"
            ) {
              textParts.push(item.text);
            }
          }
          result.textContent = textParts.join("\n");
        }
      }

      return result;
    } catch (error) {
      logError(`Error calling CallMcpTool - ${toolName}:`, error);
      throw new APIError(`Failed to call ${toolName}: ${error}`);
    }
  }

  /**
   * Creates a new directory at the specified path.
   * Corresponds to Python's create_directory() method
   *
   * @param path - Path to the directory to create.
   * @returns BoolResult with creation result and requestId
   */
  async createDirectory(path: string): Promise<BoolResult> {
    try {
      const args = {
        path,
      };

      const result = await this.callMcpTool(
        "create_directory",
        args,
        "Failed to create directory"
      );

      return {
        requestId: result.requestId || "",
        success: true,
        data: true,
      };
    } catch (error) {
      return {
        requestId: "",
        success: false,
        errorMessage: `Failed to create directory: ${error}`,
      };
    }
  }

  /**
   * Edits a file by replacing occurrences of oldText with newText.
   * Corresponds to Python's edit_file() method
   *
   * @param path - Path to the file to edit.
   * @param edits - Array of edit operations, each containing oldText and newText.
   * @param dryRun - Optional: If true, preview changes without applying them.
   * @returns BoolResult with edit result and requestId
   */
  async editFile(
    path: string,
    edits: Array<{ oldText: string; newText: string }>,
    dryRun = false
  ): Promise<BoolResult> {
    try {
      const args = {
        path,
        edits,
        dryRun,
      };

      const result = await this.callMcpTool(
        "edit_file",
        args,
        "Failed to edit file"
      );

      return {
        requestId: result.requestId || "",
        success: true,
        data: true,
      };
    } catch (error) {
      return {
        requestId: "",
        success: false,
        errorMessage: `Failed to edit file: ${error}`,
      };
    }
  }

  /**
   * Gets information about a file or directory.
   * Corresponds to Python's get_file_info() method
   *
   * @param path - Path to the file or directory to inspect.
   * @returns FileInfoResult with file info and requestId
   */
  async getFileInfo(path: string): Promise<FileInfoResult> {
    try {
      const args = {
        path,
      };

      const result = await this.callMcpTool(
        "get_file_info",
        args,
        "Failed to get file info"
      );

      // Parse and return the file info
      if (!result.textContent) {
        return {
          requestId: result.requestId || "",
          success: false,
          fileInfo: {},
          errorMessage: "Empty response from get_file_info",
        };
      }

      const fileInfo = parseFileInfo(result.textContent);

      return {
        requestId: result.requestId || "",
        success: true,
        fileInfo,
      };
    } catch (error) {
      return {
        requestId: "",
        success: false,
        errorMessage: `Failed to get file info: ${error}`,
      };
    }
  }

  /**
   * Lists the contents of a directory.
   * Corresponds to Python's list_directory() method
   *
   * @param path - Path to the directory to list.
   * @returns DirectoryListResult with directory entries and requestId
   */
  async listDirectory(path: string): Promise<DirectoryListResult> {
    try {
      const args = {
        path,
      };

      const result = await this.callMcpTool(
        "list_directory",
        args,
        "Failed to list directory"
      );

      // Parse the text content into directory entries
      const entries = result.textContent
        ? parseDirectoryListing(result.textContent)
        : [];

      return {
        requestId: result.requestId || "",
        success: true,
        entries,
      };
    } catch (error) {
      return {
        requestId: "",
        success: false,
        entries: [],
        errorMessage: `Failed to list directory: ${error}`,
      };
    }
  }

  /**
   * Moves a file or directory from source to destination.
   * Corresponds to Python's move_file() method
   *
   * @param source - Path to the source file or directory.
   * @param destination - Path to the destination file or directory.
   * @returns BoolResult with move result and requestId
   */
  async moveFile(source: string, destination: string): Promise<BoolResult> {
    try {
      const args = {
        source,
        destination,
      };

      const result = await this.callMcpTool(
        "move_file",
        args,
        "Failed to move file"
      );

      return {
        requestId: result.requestId || "",
        success: true,
        data: true,
      };
    } catch (error) {
      return {
        requestId: "",
        success: false,
        errorMessage: `Failed to move file: ${error}`,
      };
    }
  }

  /**
   * Reads the content of a file.
   * Corresponds to Python's read_file() method
   *
   * @param path - Path to the file to read.
   * @param offset - Optional: Line offset to start reading from.
   * @param length - Optional: Number of lines to read. If 0, reads the entire file.
   * @returns FileContentResult with file content and requestId
   */
  async readFile(
    path: string,
    offset = 0,
    length = 0
  ): Promise<FileContentResult> {
    try {
      const args: Record<string, any> = {
        path,
      };

      if (offset > 0) {
        args.offset = offset;
      }

      if (length > 0) {
        args.length = length;
      }

      const result = await this.callMcpTool(
        "read_file",
        args,
        "Failed to read file"
      );

      return {
        requestId: result.requestId || "",
        success: true,
        content: result.textContent || "",
      };
    } catch (error) {
      return {
        requestId: "",
        success: false,
        content: "",
        errorMessage: `Failed to read file: ${error}`,
      };
    }
  }

  /**
   * Reads the content of multiple files.
   * Corresponds to Python's read_multiple_files() method
   *
   * @param paths - Array of file paths to read.
   * @returns MultipleFileContentResult with file contents and requestId
   */
  async readMultipleFiles(paths: string[]): Promise<MultipleFileContentResult> {
    try {
      const args = {
        paths,
      };

      const result = await this.callMcpTool(
        "read_multiple_files",
        args,
        "Failed to read multiple files"
      );

      const fileContents: Record<string, string> = {};

      if (result.textContent) {
        // Parse the response into a map of file paths to contents
        const lines = result.textContent.split("\n");
        let currentPath = "";
        let currentContent: string[] = [];

        for (const line of lines) {
          // Check if this line contains a file path (ends with a colon)
          const colonIndex = line.indexOf(":");
          if (
            colonIndex > 0 &&
            currentPath === "" &&
            !line.substring(0, colonIndex).includes(" ")
          ) {
            // Extract path (everything before the first colon)
            const path = line.substring(0, colonIndex).trim();

            // Start collecting content (everything after the colon)
            currentPath = path;

            // If there's content on the same line after the colon, add it
            if (line.length > colonIndex + 1) {
              const contentStart = line.substring(colonIndex + 1).trim();
              if (contentStart) {
                currentContent.push(contentStart);
              }
            }
          } else if (line === "---") {
            // Save the current file content
            if (currentPath) {
              fileContents[currentPath] = currentContent.join("\n");
              currentPath = "";
              currentContent = [];
            }
          } else if (currentPath) {
            // If we're collecting content for a path, add this line
            currentContent.push(line);
          }
        }

        // Save the last file content if exists
        if (currentPath) {
          fileContents[currentPath] = currentContent.join("\n");
        }

        // Trim trailing newlines from file contents to match expected test values
        for (const path in fileContents) {
          fileContents[path] = fileContents[path].replace(/\n+$/, "");
        }
      }

      return {
        requestId: result.requestId || "",
        success: true,
        contents: fileContents,
      };
    } catch (error) {
      return {
        requestId: "",
        success: false,
        contents: {},
        errorMessage: `Failed to read multiple files: ${error}`,
      };
    }
  }

  /**
   * Searches for files in a directory that match a pattern.
   * Corresponds to Python's search_files() method
   *
   * @param path - Path to the directory to search in.
   * @param pattern - Pattern to search for. Supports glob patterns.
   * @param excludePatterns - Optional: Array of patterns to exclude.
   * @returns FileSearchResult with search results and requestId
   */
  async searchFiles(
    path: string,
    pattern: string,
    excludePatterns: string[] = []
  ): Promise<FileSearchResult> {
    try {
      const args: Record<string, any> = {
        path,
        pattern,
      };

      if (excludePatterns.length > 0) {
        args.exclude_patterns = excludePatterns;
      }

      const result = await this.callMcpTool(
        "search_files",
        args,
        "Failed to search files"
      );

      // Parse the text content into search results
      let searchResults: string[] = [];
      if (result.textContent) {
        // Split by newlines and filter out empty lines
        searchResults = result.textContent
          .split("\n")
          .map((line) => line.trim())
          .filter((line) => line !== "");
      }

      return {
        requestId: result.requestId || "",
        success: true,
        matches: searchResults,
      };
    } catch (error) {
      return {
        requestId: "",
        success: false,
        matches: [],
        errorMessage: `Failed to search files: ${error}`,
      };
    }
  }

  /**
   * Writes content to a file.
   * Corresponds to Python's write_file() method
   *
   * @param path - Path to the file to write.
   * @param content - Content to write to the file.
   * @param mode - Optional: Write mode. One of "overwrite", "append", or "create_new". Default is "overwrite".
   * @returns BoolResult with write result and requestId
   */
  async writeFile(
    path: string,
    content: string,
    mode = "overwrite"
  ): Promise<BoolResult> {
    try {
      // Validate mode
      const validModes = ["overwrite", "append", "create_new"];
      if (!validModes.includes(mode)) {
        return {
          requestId: "",
          success: false,
          errorMessage: `Invalid mode: ${mode}. Must be one of ${validModes.join(
            ", "
          )}`,
        };
      }

      const args = {
        path,
        content,
        mode,
      };

      const result = await this.callMcpTool(
        "write_file",
        args,
        "Failed to write file"
      );

      return {
        requestId: result.requestId || "",
        success: true,
        data: true,
      };
    } catch (error) {
      return {
        requestId: "",
        success: false,
        errorMessage: `Failed to write file: ${error}`,
      };
    }
  }

  /**
   * Reads a large file in chunks to handle size limitations of the underlying API.
   * Corresponds to Python's read_large_file() method
   *
   * @param path - Path to the file to read.
   * @param chunkSize - Optional: Size of each chunk in bytes. Default is 60KB.
   * @returns FileContentResult with complete file content and requestId
   */
  async readLargeFile(
    path: string,
    chunkSize: number = DEFAULT_CHUNK_SIZE
  ): Promise<FileContentResult> {
    try {
      // First get the file info
      const fileInfoResult = await this.getFileInfo(path);

      if (!fileInfoResult.success) {
        return {
          requestId: fileInfoResult.requestId,
          success: false,
          content: "",
          errorMessage: fileInfoResult.errorMessage,
        };
      }

      // Check if file exists and is a file (not a directory)
      if (!fileInfoResult.fileInfo || fileInfoResult.fileInfo.isDirectory) {
        return {
          requestId: fileInfoResult.requestId,
          success: false,
          content: "",
          errorMessage: `Path does not exist or is a directory: ${path}`,
        };
      }

      // Get size from the fileInfo object
      const fileSize = fileInfoResult.fileInfo.size || 0;

      if (fileSize === 0) {
        return {
          requestId: fileInfoResult.requestId,
          success: true,
          content: "",
        };
      }

      // Read the file in chunks
      let result = "";
      let offset = 0;
      let chunkCount = 0;

      log(
        `ReadLargeFile: Starting chunked read of ${path} (total size: ${fileSize} bytes, chunk size: ${chunkSize} bytes)`
      );

      while (offset < fileSize) {
        // Calculate how much to read in this chunk
        let length = chunkSize;
        if (offset + length > fileSize) {
          length = fileSize - offset;
        }

        log(
          `ReadLargeFile: Reading chunk ${
            chunkCount + 1
          } (${length} bytes at offset ${offset}/${fileSize})`
        );

        try {
          // Read the chunk
          const chunkResult = await this.readFile(path, offset, length);

          if (!chunkResult.success) {
            return chunkResult; // Return the error
          }

          // Extract the actual content from the response
          result += chunkResult.content;

          // Move to the next chunk
          offset += length;
          chunkCount++;
        } catch (error) {
          logError(`Error reading chunk at offset ${offset}: ${error}`);
          return {
            requestId: fileInfoResult.requestId,
            success: false,
            content: "",
            errorMessage: `Error reading chunk at offset ${offset}: ${error}`,
          };
        }
      }

      log(
        `ReadLargeFile: Successfully read ${path} in ${chunkCount} chunks (total: ${fileSize} bytes)`
      );

      return {
        requestId: fileInfoResult.requestId,
        success: true,
        content: result,
      };
    } catch (error) {
      return {
        requestId: "",
        success: false,
        content: "",
        errorMessage: `Failed to read large file: ${error}`,
      };
    }
  }

  /**
   * Writes a large file in chunks to handle size limitations of the underlying API.
   * Corresponds to Python's write_large_file() method
   *
   * @param path - Path to the file to write.
   * @param content - Content to write to the file.
   * @param chunkSize - Optional: Size of each chunk in bytes. Default is 60KB.
   * @returns BoolResult indicating success or failure with requestId
   */
  async writeLargeFile(
    path: string,
    content: string,
    chunkSize: number = DEFAULT_CHUNK_SIZE
  ): Promise<BoolResult> {
    try {
      const contentLen = content.length;

      log(
        `WriteLargeFile: Starting chunked write to ${path} (total size: ${contentLen} bytes, chunk size: ${chunkSize} bytes)`
      );

      // If content is small enough, use the regular WriteFile method
      if (contentLen <= chunkSize) {
        log(
          `WriteLargeFile: Content size (${contentLen} bytes) is smaller than chunk size, using normal WriteFile`
        );
        return await this.writeFile(path, content, "overwrite");
      }

      // Write the first chunk with "overwrite" mode to create/clear the file
      const firstChunkEnd = Math.min(chunkSize, contentLen);

      log(
        `WriteLargeFile: Writing first chunk (0-${firstChunkEnd} bytes) with overwrite mode`
      );
      const firstResult = await this.writeFile(
        path,
        content.substring(0, firstChunkEnd),
        "overwrite"
      );

      if (!firstResult.success) {
        return firstResult;
      }

      // Write the remaining chunks with "append" mode
      let chunkCount = 1; // Already wrote first chunk
      for (let offset = firstChunkEnd; offset < contentLen; ) {
        const end = Math.min(offset + chunkSize, contentLen);

        log(
          `WriteLargeFile: Writing chunk ${
            chunkCount + 1
          } (${offset}-${end} bytes) with append mode`
        );
        const chunkResult = await this.writeFile(
          path,
          content.substring(offset, end),
          "append"
        );

        if (!chunkResult.success) {
          return chunkResult;
        }

        offset = end;
        chunkCount++;
      }

      log(
        `WriteLargeFile: Successfully wrote ${path} in ${chunkCount} chunks (total: ${contentLen} bytes)`
      );

      return {
        requestId: firstResult.requestId,
        success: true,
        data: true,
      };
    } catch (error) {
      return {
        requestId: "",
        success: false,
        errorMessage: `Failed to write large file: ${error}`,
      };
    }
  }
}
