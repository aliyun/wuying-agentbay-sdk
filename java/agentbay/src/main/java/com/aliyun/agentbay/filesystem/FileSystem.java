package com.aliyun.agentbay.filesystem;

import com.aliyun.agentbay.exception.AgentBayException;
import com.aliyun.agentbay.exception.FileException;
import com.aliyun.agentbay.model.*;
import com.aliyun.agentbay.service.BaseService;
import com.aliyun.agentbay.session.Session;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.util.*;

/**
 * File system operations for a session
 */
public class FileSystem extends BaseService {
    private static final Logger logger = LoggerFactory.getLogger(FileSystem.class);
    private static final ObjectMapper objectMapper = new ObjectMapper();

    private static final int DEFAULT_CHUNK_SIZE = 50 * 1024;
    private static final int DEFAULT_VPC_CHUNK_SIZE = 512 * 1024;

    private FileTransfer fileTransfer;

    public FileSystem(Session session) {
        super(session);
    }

    private FileTransfer ensureFileTransfer() {
        if (fileTransfer == null) {
            if (session.getAgentBay() == null) {
                throw new RuntimeException("FileTransfer requires an AgentBay instance");
            }
            if (session == null) {
                throw new RuntimeException("FileTransfer requires a session");
            }
            fileTransfer = new FileTransfer(session.getAgentBay(), session);
        }
        return fileTransfer;
    }

    /**
     * Read a file
     *
     * @param path File path
     * @return File content
     * @throws AgentBayException if reading fails
     */
    public String read(String path) throws AgentBayException {
        logger.debug("Reading file: {}", path);
        return session.getAgent().readFile(path);
    }

    /**
     * Write content to a file
     *
     * @param path File path
     * @param content Content to write
     * @return Write result
     * @throws AgentBayException if writing fails
     */
    public String write(String path, String content) throws AgentBayException {
        logger.debug("Writing file: {}", path);
        return session.getAgent().writeFile(path, content);
    }

    /**
     * List directory contents
     *
     * @param path Directory path
     * @return Directory listing
     * @throws AgentBayException if listing fails
     */
    public String list(String path) throws AgentBayException {
        logger.debug("Listing directory: {}", path);
        return session.getAgent().listDirectory(path);
    }

    /**
     * Check if a file or directory exists
     *
     * @param path Path to check
     * @return true if exists, false otherwise
     * @throws AgentBayException if check fails
     */
    public boolean exists(String path) throws AgentBayException {
        try {
            String result = session.getAgent().executeCommand("test -e \"" + path + "\" && echo 'exists' || echo 'not exists'");
            return result != null && result.trim().equals("exists");
        } catch (AgentBayException e) {
            logger.warn("Failed to check if path exists: {}", path, e);
            return false;
        }
    }

    /**
     * Create a directory
     *
     * @param path Directory path
     * @return Creation result
     * @throws AgentBayException if creation fails
     */
    public String mkdir(String path) throws AgentBayException {
        logger.debug("Creating directory: {}", path);
        return session.getAgent().executeCommand("mkdir -p \"" + path + "\"");
    }

    /**
     * Remove a file or directory
     *
     * @param path Path to remove
     * @return Removal result
     * @throws AgentBayException if removal fails
     */
    public String remove(String path) throws AgentBayException {
        logger.debug("Removing path: {}", path);
        return session.getAgent().executeCommand("rm -rf \"" + path + "\"");
    }

    /**
     * Copy a file or directory
     *
     * @param source Source path
     * @param destination Destination path
     * @return Copy result
     * @throws AgentBayException if copy fails
     */
    public String copy(String source, String destination) throws AgentBayException {
        logger.debug("Copying from {} to {}", source, destination);
        return session.getAgent().executeCommand("cp -r \"" + source + "\" \"" + destination + "\"");
    }

    /**
     * Move a file or directory
     *
     * @param source Source path
     * @param destination Destination path
     * @return Move result
     * @throws AgentBayException if move fails
     */
    public String move(String source, String destination) throws AgentBayException {
        logger.debug("Moving from {} to {}", source, destination);
        return session.getAgent().executeCommand("mv \"" + source + "\" \"" + destination + "\"");
    }

    /**
     * Get file information
     *
     * @param path File path
     * @return File information
     * @throws AgentBayException if getting info fails
     */
    public String getInfo(String path) throws AgentBayException {
        logger.debug("Getting file info: {}", path);
        return session.getAgent().executeCommand("ls -la \"" + path + "\"");
    }

    /**
     * Write content to a file. Automatically handles large files by chunking.
     * Similar to Python's write_file method.
     *
     * @param path File path
     * @param content Content to write
     * @param mode Write mode ("overwrite" or "append")
     * @param createParentDir Whether to create parent directories if they don't exist (default: false)
     * @return BoolResult containing success status and error message if any
     */
    public BoolResult writeFile(String path, String content, String mode, boolean createParentDir) {
        int contentLength = content.getBytes().length;
        logger.debug("Writing file: {} (size: {} bytes, mode: {}, createParentDir: {})", path, contentLength, mode, createParentDir);
        int chunkSize = DEFAULT_CHUNK_SIZE;
        if (session.isVpcEnabled()) {
            chunkSize =DEFAULT_VPC_CHUNK_SIZE;
        }
        // If the content length is less than the chunk size, write it directly
        if (contentLength <= chunkSize) {
            return writeFileChunk(path, content, mode, createParentDir);
        }

        try {
            // Write the first chunk (creates or overwrites the file)
            String firstChunk = content.substring(0, Math.min(chunkSize, content.length()));
            BoolResult result = writeFileChunk(path, firstChunk, mode, createParentDir);
            if (!result.isSuccess()) {
                return result;
            }

            // Write the rest in chunks (appending)
            int offset = chunkSize;
            while (offset < content.length()) {
                int end = Math.min(offset + chunkSize, content.length());
                String currentChunk = content.substring(offset, end);
                result = writeFileChunk(path, currentChunk, "append", false);
                if (!result.isSuccess()) {
                    return result;
                }
                offset = end;
            }

            return new BoolResult(result.getRequestId(), true, true, "");

        } catch (Exception e) {
            logger.error("Failed to write file: {}", path, e);
            return new BoolResult("", false, false, "Failed to write file: " + e.getMessage());
        }
    }

    /**
     * Write file content using BoolResult with default "overwrite" mode
     */
    public BoolResult writeFile(String path, String content) {
        return writeFile(path, content, "overwrite", false);
    }

    /**
     * Write file content using BoolResult with specified mode
     */
    public BoolResult writeFile(String path, String content, String mode) {
        return writeFile(path, content, mode, false);
    }

    // Note: The three-parameter version writeFile(path, content, mode) is the main method above

    /**
     * Internal method to write a file chunk. Used for chunked file operations.
     * Similar to Python's _write_file_chunk method.
     *
     * @param path File path
     * @param content Content to write
     * @param mode Write mode ("overwrite" or "append")
     * @param createParentDir Whether to create parent directories if they don't exist
     * @return BoolResult containing success status and error message if any
     */
    private BoolResult writeFileChunk(String path, String content, String mode, boolean createParentDir) {
        if (!"overwrite".equals(mode) && !"append".equals(mode)) {
            return new BoolResult("", false, false,
                "Invalid write mode: " + mode + ". Must be 'overwrite' or 'append'.");
        }

        Map<String, Object> args = new HashMap<>();
        args.put("path", path);
        args.put("content", content);
        args.put("mode", mode);
        args.put("create_parent_dir", createParentDir);

        try {
            OperationResult result = callMcpTool("write_file", args);
            logger.debug("write_file response: {}", result);

            if (result.isSuccess()) {
                return new BoolResult(result.getRequestId(), true, true, "");
            } else {
                return new BoolResult(result.getRequestId(), false, false, result.getErrorMessage());
            }

        } catch (Exception e) {
            logger.error("Failed to write file chunk: {}", path, e);
            return new BoolResult("", false, false, "Failed to write file chunk: " + e.getMessage());
        }
    }

    /**
     * Read file content using FileContentResult
     */
    public FileContentResult readFile(String path) {
        Map<String, Object> args = new HashMap<>();
        args.put("path", path);

        try {
            OperationResult result = callMcpTool("read_file", args);
            logger.debug("read_file response: {}", result);

            if (result.isSuccess()) {
                return new FileContentResult(result.getRequestId(), true, result.getData(), "");
            } else {
                return new FileContentResult(result.getRequestId(), false, "", result.getErrorMessage());
            }

        } catch (Exception e) {
            logger.error("Failed to read file: {}", path, e);
            return new FileContentResult("", false, "", "Failed to read file: " + e.getMessage());
        }
    }

    /**
     * Search for files matching a pattern
     */
    public FileSearchResult searchFiles(String directory, String pattern) {
        return searchFiles(directory, pattern, null);
    }

    public FileSearchResult searchFiles(String directory, String pattern, List<String> excludePatterns) {
        try {
            Map<String, Object> args = new HashMap<>();
            args.put("path", directory);
            args.put("pattern", pattern);
            if (excludePatterns != null && !excludePatterns.isEmpty()) {
                args.put("excludePatterns", excludePatterns);
            }

            OperationResult result = callMcpTool("search_files", args);

            if (result.isSuccess()) {
                String[] matchingFiles = result.getData() != null && !result.getData().trim().isEmpty()
                    ? result.getData().trim().split("\n")
                    : new String[0];

                List<String> matches = Arrays.asList(matchingFiles);
                if (matches.size() == 1 && "No matches found".equals(matches.get(0))) {
                    return new FileSearchResult(result.getRequestId(), false, new ArrayList<>(), "No matches found");
                }
                return new FileSearchResult(result.getRequestId(), true, matches, "");
            } else {
                return new FileSearchResult(result.getRequestId(), false, null,
                    result.getErrorMessage() != null ? result.getErrorMessage() : "Failed to search files");
            }
        } catch (Exception e) {
            return new FileSearchResult("", false, null, e.getMessage());
        }
    }

    /**
     * Read multiple files at once
     */
    public MultipleFileContentResult readMultipleFiles(List<String> paths) {
        try {
            Map<String, Object> args = new HashMap<>();
            args.put("paths", paths);

            OperationResult result = callMcpTool("read_multiple_files", args);

            if (result.isSuccess()) {
                Map<String, String> filesContent = parseMultipleFilesResponse(result.getData());
                return new MultipleFileContentResult(result.getRequestId(), true, filesContent, "");
            } else {
                return new MultipleFileContentResult(result.getRequestId(), false, null,
                    result.getErrorMessage() != null ? result.getErrorMessage() : "Failed to read multiple files");
            }
        } catch (Exception e) {
            return new MultipleFileContentResult("", false, null, e.getMessage());
        }
    }

    /**
     * Delete a file or directory using DeleteResult
     */
    public DeleteResult deleteFile(String path) {
        try {
            remove(path);
            return new DeleteResult("", true, "");
        } catch (AgentBayException e) {
            return new DeleteResult("", false, e.getMessage());
        }
    }

    public BoolResult createDirectory(String path) {
        Map<String, Object> args = new HashMap<>();
        args.put("path", path);

        try {
            OperationResult result = callMcpTool("create_directory", args);
            logger.debug("create_directory response: {}", result);

            if (result.isSuccess()) {
                return new BoolResult(result.getRequestId(), true, true, "");
            } else {
                return new BoolResult(result.getRequestId(), false, false, result.getErrorMessage());
            }

        } catch (Exception e) {
            logger.error("Failed to create directory: {}", path, e);
            return new BoolResult("", false, false, "Failed to create directory: " + e.getMessage());
        }
    }

    public com.aliyun.agentbay.model.DirectoryListResult listDirectory(String path) {
        try {
            Map<String, Object> args = new HashMap<>();
            args.put("path", path);

            OperationResult result = callMcpTool("list_directory", args);

            if (result.isSuccess()) {
                // Parse the directory listing response like Python SDK does
                String directoryResponse = result.getData();
                List<Map<String, Object>> entries = parseDirectoryListing(directoryResponse);

                com.aliyun.agentbay.model.DirectoryListResult dirResult =
                    new com.aliyun.agentbay.model.DirectoryListResult(result.getRequestId(), true, null, "");
                dirResult.setEntries(entries);
                return dirResult;
            } else {
                return new com.aliyun.agentbay.model.DirectoryListResult(result.getRequestId(), false, null, result.getErrorMessage());
            }
        } catch (Exception e) {
            return new com.aliyun.agentbay.model.DirectoryListResult("", false, null, e.getMessage());
        }
    }

    public com.aliyun.agentbay.model.FileInfoResult getFileInfo(String path) {
        try {
            Map<String, Object> args = new HashMap<>();
            args.put("path", path);

            OperationResult result = callMcpTool("get_file_info", args);

            if (result.isSuccess()) {
                Map<String, Object> fileInfo = parseFileInfo(result.getData());
                com.aliyun.agentbay.model.FileInfoResult fileInfoResult =
                    new com.aliyun.agentbay.model.FileInfoResult(result.getRequestId(), true, result.getData(), "");
                fileInfoResult.setFileInfo(fileInfo);
                return fileInfoResult;
            } else {
                return new com.aliyun.agentbay.model.FileInfoResult(result.getRequestId(), false, "",
                    result.getErrorMessage() != null ? result.getErrorMessage() : "Failed to get file info");
            }
        } catch (Exception e) {
            return new com.aliyun.agentbay.model.FileInfoResult("", false, null, e.getMessage());
        }
    }

    public BoolResult editFile(String path, java.util.List<java.util.Map<String, String>> edits) {
        return editFile(path, edits, false);
    }

    public BoolResult editFile(String path, java.util.List<java.util.Map<String, String>> edits, boolean dryRun) {
        Map<String, Object> args = new HashMap<>();
        args.put("path", path);
        args.put("edits", edits);
        args.put("dryRun", dryRun);

        try {
            OperationResult result = callMcpTool("edit_file", args);
            logger.debug("edit_file response: {}", result);

            if (result.isSuccess()) {
                return new BoolResult(result.getRequestId(), true, true, "");
            } else {
                return new BoolResult(result.getRequestId(), false, false, result.getErrorMessage());
            }

        } catch (Exception e) {
            logger.error("Failed to edit file: {}", path, e);
            return new BoolResult("", false, false, "Failed to edit file: " + e.getMessage());
        }
    }

    public BoolResult moveFile(String source, String destination) {
        try {
            Map<String, Object> args = new HashMap<>();
            args.put("source", source);
            args.put("destination", destination);

            OperationResult result = callMcpTool("move_file", args);

            if (result.isSuccess()) {
                return new BoolResult(result.getRequestId(), true, true, "");
            } else {
                return new BoolResult(result.getRequestId(), false, false,
                    result.getErrorMessage() != null ? result.getErrorMessage() : "Failed to move file");
            }
        } catch (Exception e) {
            return new BoolResult("", false, false, e.getMessage());
        }
    }

    /**
     * Parse directory listing text into a list of file/directory entries.
     * This mimics the Python SDK's parse_directory_listing function.
     *
     * @param text Directory listing text in format:
     *             [DIR] directory_name
     *             [FILE] file_name
     *             Each entry should be on a new line with [DIR] or [FILE] prefix
     * @return List of maps containing name and isDirectory fields
     */
    private List<Map<String, Object>> parseDirectoryListing(String text) {
        List<Map<String, Object>> result = new ArrayList<>();
        if (text == null || text.trim().isEmpty()) {
            return result;
        }

        String[] lines = text.split("\n");
        for (String line : lines) {
            line = line.trim();
            if (line.isEmpty()) {
                continue;
            }

            Map<String, Object> entryMap = new HashMap<>();
            if (line.startsWith("[DIR]")) {
                entryMap.put("isDirectory", true);
                entryMap.put("name", line.replace("[DIR]", "").trim());
            } else if (line.startsWith("[FILE]")) {
                entryMap.put("isDirectory", false);
                entryMap.put("name", line.replace("[FILE]", "").trim());
            } else {
                // Skip lines that don't match the expected format
                continue;
            }

            result.add(entryMap);
        }

        return result;
    }

    /**
     * Parse file info string into a map.
     * This mimics the Python SDK's parse_file_info function.
     *
     * @param fileInfoStr The file info string to parse
     * @return A map containing the parsed file info
     */
    private Map<String, Object> parseFileInfo(String fileInfoStr) {
        Map<String, Object> result = new HashMap<>();
        if (fileInfoStr == null || fileInfoStr.trim().isEmpty()) {
            return result;
        }

        String[] lines = fileInfoStr.split("\\n");
        for (String line : lines) {
            if (line.contains(":")) {
                String[] parts = line.split(":", 2);
                if (parts.length == 2) {
                    String key = parts[0].trim();
                    String value = parts[1].trim();

                    // Convert boolean values
                    if ("true".equalsIgnoreCase(value)) {
                        result.put(key, true);
                    } else if ("false".equalsIgnoreCase(value)) {
                        result.put(key, false);
                    } else {
                        // Try to convert numeric values
                        try {
                            if (value.contains(".")) {
                                result.put(key, Double.parseDouble(value));
                            } else {
                                result.put(key, Long.parseLong(value));
                            }
                        } catch (NumberFormatException e) {
                            // Keep as string if not numeric
                            result.put(key, value);
                        }
                    }
                }
            }
        }
        return result;
    }
    /**
     * Parse the response from reading multiple files.
     * This mimics the Python SDK's parse_multiple_files_response function.
     *
     * @param text The response string containing file contents in format:
     *             /path/to/file1.txt: Content of file1
     *
     *             ---
     *
     *             /path/to/file2.txt:
     *             Content of file2
     * @return A map mapping file paths to their content
     */
    private Map<String, String> parseMultipleFilesResponse(String text) {
        Map<String, String> result = new HashMap<>();
        if (text == null || text.trim().isEmpty()) {
            return result;
        }

        String[] lines = text.split("\\n");
        String currentPath = null;
        List<String> currentContent = new ArrayList<>();

        for (int i = 0; i < lines.length; i++) {
            String line = lines[i];

            // Check if this line contains a file path (ends with a colon)
            if (line.contains(":") && currentPath == null) {
                // Extract path (everything before the first colon)
                int colonIndex = line.indexOf(":");
                String path = line.substring(0, colonIndex).trim();

                // Start collecting content (everything after the colon)
                currentPath = path;

                // If there's content on the same line after the colon, add it
                if (line.length() > colonIndex + 1) {
                    String contentStart = line.substring(colonIndex + 1).trim();
                    if (!contentStart.isEmpty()) {
                        currentContent.add(contentStart);
                    }
                }
            }
            // Check if this is a separator line
            else if ("---".equals(line.trim())) {
                // Save the current file content
                if (currentPath != null) {
                    result.put(currentPath, String.join("\\n", currentContent).trim());
                    currentPath = null;
                    currentContent.clear();
                }
            }
            // If we're collecting content for a path, add this line
            else if (currentPath != null) {
                currentContent.add(line);
            }
        }

        // Save the last file content if exists
        if (currentPath != null) {
            result.put(currentPath, String.join("\\n", currentContent).trim());
        }

        return result;
    }

    public UploadResult uploadFile(
        String localPath,
        String remotePath,
        String contentType,
        boolean wait,
        float waitTimeout,
        float pollInterval
    ) {
        try {
            FileTransfer transfer = ensureFileTransfer();
            UploadResult result = transfer.upload(localPath, remotePath, contentType, wait, waitTimeout, pollInterval);

            if (result.isSuccess() && session.getFileTransferContextId() != null) {
                String contextId = session.getFileTransferContextId();
                try {
                    session.getAgentBay().getContextService().deleteFile(contextId, remotePath);
                } catch (Exception deleteError) {
                    logger.warn("Error deleting uploaded file from OSS: {}", deleteError.getMessage());
                }
            }

            return result;
        } catch (Exception e) {
            return new UploadResult(
                "", false, null, null, null, null, 0, remotePath,
                "Upload failed: " + e.getMessage()
            );
        }
    }

    public UploadResult uploadFile(String localPath, String remotePath) {
        return uploadFile(localPath, remotePath, null, true, 30.0f, 1.5f);
    }

    public DownloadResult downloadFile(
        String remotePath,
        String localPath,
        boolean overwrite,
        boolean wait,
        float waitTimeout,
        float pollInterval
    ) {
        try {
            FileTransfer transfer = ensureFileTransfer();
            DownloadResult result = transfer.download(remotePath, localPath, overwrite, wait, waitTimeout, pollInterval);

            if (result.isSuccess() && session.getFileTransferContextId() != null) {
                String contextId = session.getFileTransferContextId();
                try {
                    session.getAgentBay().getContextService().deleteFile(contextId, remotePath);
                } catch (Exception deleteError) {
                    logger.warn("Error deleting downloaded file from OSS: {}", deleteError.getMessage());
                }
            }

            return result;
        } catch (Exception e) {
            return new DownloadResult(
                "", false, null, null, null, 0, remotePath, localPath, null,
                "Download failed: " + e.getMessage()
            );
        }
    }

    public DownloadResult downloadFile(String remotePath, String localPath) {
        return downloadFile(remotePath, localPath, true, true, 30.0f, 1.5f);
    }

    public DownloadResult downloadFile(String remotePath) {
        return downloadFile(remotePath, null);
    }
}
