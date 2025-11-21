package com.aliyun.agentbay.agent;

import com.aliyun.agentbay.exception.AgentBayException;
import com.aliyun.agentbay.model.OperationResult;
import com.aliyun.agentbay.service.BaseService;
import com.aliyun.agentbay.session.Session;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.HashMap;
import java.util.Map;

/**
 * Agent for interacting with tools and services in a session
 */
public class Agent extends BaseService {
    private static final Logger logger = LoggerFactory.getLogger(Agent.class);

    public Agent(Session session) {
        super(session);
    }

    /**
     * Execute a command in the session
     *
     * @param command Command to execute
     * @return Command execution result
     * @throws AgentBayException if execution fails
     */
    public String executeCommand(String command) throws AgentBayException {
        logger.debug("Executing command: {}", command);

        Map<String, Object> args = new HashMap<>();
        args.put("command", command);

        OperationResult result = callMcpTool("shell", args);

        if (result.isSuccess()) {
            return result.getData();
        } else {
            throw new AgentBayException(result.getErrorMessage());
        }
    }

    /**
     * Read a file from the session
     *
     * @param filePath Path to the file
     * @return File content
     * @throws AgentBayException if reading fails
     */
    public String readFile(String filePath) throws AgentBayException {
        logger.debug("Reading file: {}", filePath);

        Map<String, Object> args = new HashMap<>();
        args.put("path", filePath);

        OperationResult result = callMcpTool("read_file", args);

        if (result.isSuccess()) {
            return result.getData();
        } else {
            throw new AgentBayException(result.getErrorMessage());
        }
    }

    /**
     * Write content to a file in the session
     *
     * @param filePath Path to the file
     * @param content Content to write
     * @return Write operation result
     * @throws AgentBayException if writing fails
     */
    public String writeFile(String filePath, String content) throws AgentBayException {
        logger.debug("Writing file: {}", filePath);

        Map<String, Object> args = new HashMap<>();
        args.put("path", filePath);
        args.put("content", content);

        OperationResult result = callMcpTool("write_file", args);

        if (result.isSuccess()) {
            return result.getData();
        } else {
            throw new AgentBayException(result.getErrorMessage());
        }
    }

    /**
     * List files in a directory
     *
     * @param directoryPath Directory path
     * @return Directory listing
     * @throws AgentBayException if listing fails
     */
    public String listDirectory(String directoryPath) throws AgentBayException {
        logger.debug("Listing directory: {}", directoryPath);

        Map<String, Object> args = new HashMap<>();
        args.put("path", directoryPath);

        OperationResult result = callMcpTool("list_directory", args);

        if (result.isSuccess()) {
            return result.getData();
        } else {
            throw new AgentBayException(result.getErrorMessage());
        }
    }

    /**
     * Take a screenshot of the browser
     *
     * @return Screenshot data or path
     * @throws AgentBayException if screenshot fails
     */
    public String takeScreenshot() throws AgentBayException {
        logger.debug("Taking screenshot");

        Map<String, Object> args = new HashMap<>();

        OperationResult result = callMcpTool("screenshot", args);

        if (result.isSuccess()) {
            return result.getData();
        } else {
            throw new AgentBayException(result.getErrorMessage());
        }
    }

    /**
     * Navigate browser to a URL
     *
     * @param url URL to navigate to
     * @return Navigation result
     * @throws AgentBayException if navigation fails
     */
    public String navigateTo(String url) throws AgentBayException {
        logger.debug("Navigating to URL: {}", url);

        Map<String, Object> args = new HashMap<>();
        args.put("url", url);

        OperationResult result = callMcpTool("navigate", args);

        if (result.isSuccess()) {
            return result.getData();
        } else {
            throw new AgentBayException(result.getErrorMessage());
        }
    }

    /**
     * Click on an element
     *
     * @param selector CSS selector or XPath
     * @return Click result
     * @throws AgentBayException if click fails
     */
    public String click(String selector) throws AgentBayException {
        logger.debug("Clicking element: {}", selector);

        Map<String, Object> args = new HashMap<>();
        args.put("selector", selector);

        OperationResult result = callMcpTool("click", args);

        if (result.isSuccess()) {
            return result.getData();
        } else {
            throw new AgentBayException(result.getErrorMessage());
        }
    }

    /**
     * Type text into an input field
     *
     * @param selector CSS selector or XPath
     * @param text Text to type
     * @return Type result
     * @throws AgentBayException if typing fails
     */
    public String type(String selector, String text) throws AgentBayException {
        logger.debug("Typing text into element: {}", selector);

        Map<String, Object> args = new HashMap<>();
        args.put("selector", selector);
        args.put("text", text);

        OperationResult result = callMcpTool("type", args);

        if (result.isSuccess()) {
            return result.getData();
        } else {
            throw new AgentBayException(result.getErrorMessage());
        }
    }

    /**
     * Get the session associated with this agent
     *
     * @return Session instance
     */
    public Session getSession() {
        return session;
    }
}