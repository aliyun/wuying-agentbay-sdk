package com.aliyun.agentbay.computer;

import com.aliyun.agentbay.model.AppOperationResult;
import com.aliyun.agentbay.model.BoolResult;
import com.aliyun.agentbay.model.InstalledApp;
import com.aliyun.agentbay.model.InstalledAppListResult;
import com.aliyun.agentbay.model.OperationResult;
import com.aliyun.agentbay.model.Process;
import com.aliyun.agentbay.model.ProcessListResult;
import com.aliyun.agentbay.model.Window;
import com.aliyun.agentbay.model.WindowInfoResult;
import com.aliyun.agentbay.model.WindowListResult;
import com.aliyun.agentbay.service.BaseService;
import com.aliyun.agentbay.session.Session;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Computer module for desktop UI automation.
 * Provides comprehensive desktop automation capabilities including mouse, keyboard,
 * window management, application management, and screen operations.
 */
public class Computer extends BaseService {
    private static final Logger logger = LoggerFactory.getLogger(Computer.class);
    private static final ObjectMapper objectMapper = new ObjectMapper();

    public Computer(Session session) {
        super(session);
    }

    /**
     * Starts an application with the given command, optional working directory and optional activity.
     *
     * @param startCmd The command to start the application (e.g., "npm run dev", "notepad.exe")
     * @param workDirectory Optional working directory for the application (e.g., "/tmp/app/react-site-demo-1")
     * @param activity Optional activity name to launch (for mobile apps). Defaults to empty string.
     * @return ProcessListResult containing the list of processes started
     */
    public ProcessListResult startApp(String startCmd, String workDirectory, String activity) {
        try {
            Map<String, Object> args = new HashMap<>();
            args.put("start_cmd", startCmd);
            if (workDirectory != null && !workDirectory.isEmpty()) {
                args.put("work_directory", workDirectory);
            }
            if (activity != null && !activity.isEmpty()) {
                args.put("activity", activity);
            }

            logger.debug("Starting app: {} with work directory: {}, activity: {}", startCmd, workDirectory, activity);
            logger.debug("MCP tool args: {}", args);

            OperationResult result = callMcpTool("start_app", args);

            if (!result.isSuccess()) {
                logger.warn("Failed to start app. Command: {}, WorkDirectory: {}, Error: {}, RequestId: {}", 
                    startCmd, workDirectory, result.getErrorMessage(), result.getRequestId());
                return new ProcessListResult(
                    result.getRequestId(),
                    false,
                    new ArrayList<>(),
                    result.getErrorMessage()
                );
            }

            try {
                // Parse the JSON response to get list of processes
                String data = result.getData();
                if (data == null || data.isEmpty()) {
                    return new ProcessListResult(
                        result.getRequestId(),
                        true,
                        new ArrayList<>(),
                        ""
                    );
                }

                List<Map<String, Object>> processesJson = objectMapper.readValue(
                    data,
                    new TypeReference<List<Map<String, Object>>>() {}
                );

                List<Process> processes = new ArrayList<>();
                for (Map<String, Object> processData : processesJson) {
                    Process process = new Process();
                    if (processData.containsKey("pname")) {
                        process.setPname(String.valueOf(processData.get("pname")));
                    }
                    if (processData.containsKey("pid")) {
                        Object pidObj = processData.get("pid");
                        if (pidObj instanceof Number) {
                            process.setPid(((Number) pidObj).intValue());
                        }
                    }
                    if (processData.containsKey("cmdline")) {
                        process.setCmdline(String.valueOf(processData.get("cmdline")));
                    }
                    processes.add(process);
                }

                return new ProcessListResult(
                    result.getRequestId(),
                    true,
                    processes,
                    ""
                );
            } catch (Exception e) {
                logger.error("Failed to parse processes JSON", e);
                return new ProcessListResult(
                    result.getRequestId(),
                    false,
                    new ArrayList<>(),
                    "Failed to parse processes JSON: " + e.getMessage()
                );
            }
        } catch (Exception e) {
            logger.error("Unexpected error during startApp", e);
            return new ProcessListResult(
                "",
                false,
                new ArrayList<>(),
                "Failed to start app: " + e.getMessage()
            );
        }
    }

    /**
     * Starts an application with the given command and optional working directory.
     *
     * @param startCmd The command to start the application
     * @param workDirectory Optional working directory for the application
     * @return ProcessListResult containing the list of processes started
     */
    public ProcessListResult startApp(String startCmd, String workDirectory) {
        return startApp(startCmd, workDirectory, "");
    }

    /**
     * Starts an application with the given command.
     *
     * @param startCmd The command to start the application
     * @return ProcessListResult containing the list of processes started
     */
    public ProcessListResult startApp(String startCmd) {
        return startApp(startCmd, "", "");
    }

    /**
     * Stops an application by process name.
     *
     * @param pname The process name of the application to stop (e.g., "notepad.exe", "chrome.exe")
     * @return AppOperationResult containing success status and error message if any
     */
    public AppOperationResult stopAppByPName(String pname) {
        try {
            Map<String, Object> args = new HashMap<>();
            args.put("pname", pname);

            logger.debug("Stopping app by process name: {}", pname);

            OperationResult result = callMcpTool("stop_app_by_pname", args);

            return new AppOperationResult(
                result.getRequestId(),
                result.isSuccess(),
                result.getErrorMessage()
            );
        } catch (Exception e) {
            logger.error("Unexpected error during stopAppByPName", e);
            return new AppOperationResult(
                "",
                false,
                "Failed to stop app by pname: " + e.getMessage()
            );
        }
    }

    /**
     * Stops an application by process ID.
     *
     * @param pid The process ID of the application to stop
     * @return AppOperationResult containing success status and error message if any
     */
    public AppOperationResult stopAppByPID(int pid) {
        try {
            Map<String, Object> args = new HashMap<>();
            args.put("pid", pid);

            logger.debug("Stopping app by process ID: {}", pid);

            OperationResult result = callMcpTool("stop_app_by_pid", args);

            return new AppOperationResult(
                result.getRequestId(),
                result.isSuccess(),
                result.getErrorMessage()
            );
        } catch (Exception e) {
            logger.error("Unexpected error during stopAppByPID", e);
            return new AppOperationResult(
                "",
                false,
                "Failed to stop app by pid: " + e.getMessage()
            );
        }
    }

    /**
     * Stops an application by stop command.
     *
     * @param stopCmd The command to stop the application (e.g., "taskkill /IM notepad.exe /F")
     * @return AppOperationResult containing success status and error message if any
     */
    public AppOperationResult stopAppByCmd(String stopCmd) {
        try {
            Map<String, Object> args = new HashMap<>();
            args.put("stop_cmd", stopCmd);

            logger.debug("Stopping app by command: {}", stopCmd);

            OperationResult result = callMcpTool("stop_app_by_cmd", args);

            return new AppOperationResult(
                result.getRequestId(),
                result.isSuccess(),
                result.getErrorMessage()
            );
        } catch (Exception e) {
            logger.error("Unexpected error during stopAppByCmd", e);
            return new AppOperationResult(
                "",
                false,
                "Failed to stop app by cmd: " + e.getMessage()
            );
        }
    }

    /**
     * Lists all applications with visible windows.
     *
     * @return ProcessListResult containing list of visible applications with detailed process information
     */
    public ProcessListResult listVisibleApps() {
        try {
            logger.debug("Listing visible apps");

            OperationResult result = callMcpTool("list_visible_apps", new HashMap<>());

            if (!result.isSuccess()) {
                return new ProcessListResult(
                    result.getRequestId(),
                    false,
                    new ArrayList<>(),
                    result.getErrorMessage()
                );
            }

            try {
                // Parse the JSON response to get list of processes
                String data = result.getData();
                if (data == null || data.isEmpty()) {
                    return new ProcessListResult(
                        result.getRequestId(),
                        true,
                        new ArrayList<>(),
                        ""
                    );
                }

                List<Map<String, Object>> processesJson = objectMapper.readValue(
                    data,
                    new TypeReference<List<Map<String, Object>>>() {}
                );

                List<Process> processes = new ArrayList<>();
                for (Map<String, Object> processData : processesJson) {
                    Process process = new Process();
                    if (processData.containsKey("pname")) {
                        process.setPname(String.valueOf(processData.get("pname")));
                    }
                    if (processData.containsKey("pid")) {
                        Object pidObj = processData.get("pid");
                        if (pidObj instanceof Number) {
                            process.setPid(((Number) pidObj).intValue());
                        }
                    }
                    if (processData.containsKey("cmdline")) {
                        process.setCmdline(String.valueOf(processData.get("cmdline")));
                    }
                    processes.add(process);
                }

                return new ProcessListResult(
                    result.getRequestId(),
                    true,
                    processes,
                    ""
                );
            } catch (Exception e) {
                logger.error("Failed to parse processes JSON", e);
                return new ProcessListResult(
                    result.getRequestId(),
                    false,
                    new ArrayList<>(),
                    "Failed to parse processes JSON: " + e.getMessage()
                );
            }
        } catch (Exception e) {
            logger.error("Unexpected error during listVisibleApps", e);
            return new ProcessListResult(
                "",
                false,
                new ArrayList<>(),
                "Failed to list visible apps: " + e.getMessage()
            );
        }
    }

    /**
     * Gets the list of installed applications.
     *
     * @param startMenu Whether to include start menu applications. Defaults to true.
     * @param desktop Whether to include desktop applications. Defaults to false.
     * @param ignoreSystemApps Whether to ignore system applications. Defaults to true.
     * @return InstalledAppListResult containing list of installed apps and error message if any
     */
    public InstalledAppListResult getInstalledApps(boolean startMenu, boolean desktop, boolean ignoreSystemApps) {
        try {
            Map<String, Object> args = new HashMap<>();
            args.put("start_menu", startMenu);
            args.put("desktop", desktop);
            args.put("ignore_system_apps", ignoreSystemApps);

            logger.debug("Getting installed apps (startMenu: {}, desktop: {}, ignoreSystemApps: {})",
                startMenu, desktop, ignoreSystemApps);

            OperationResult result = callMcpTool("get_installed_apps", args);

            if (!result.isSuccess()) {
                return new InstalledAppListResult(
                    result.getRequestId(),
                    false,
                    new ArrayList<>(),
                    result.getErrorMessage()
                );
            }

            try {
                // Parse the JSON response to get list of installed apps
                String data = result.getData();
                if (data == null || data.isEmpty()) {
                    return new InstalledAppListResult(
                        result.getRequestId(),
                        true,
                        new ArrayList<>(),
                        ""
                    );
                }

                List<Map<String, Object>> appsJson = objectMapper.readValue(
                    data,
                    new TypeReference<List<Map<String, Object>>>() {}
                );

                List<InstalledApp> installedApps = new ArrayList<>();
                for (Map<String, Object> appData : appsJson) {
                    InstalledApp app = new InstalledApp();
                    if (appData.containsKey("name")) {
                        app.setName(String.valueOf(appData.get("name")));
                    }
                    if (appData.containsKey("start_cmd")) {
                        app.setStartCmd(String.valueOf(appData.get("start_cmd")));
                    }
                    if (appData.containsKey("stop_cmd")) {
                        Object stopCmdObj = appData.get("stop_cmd");
                        if (stopCmdObj != null) {
                            app.setStopCmd(String.valueOf(stopCmdObj));
                        }
                    }
                    if (appData.containsKey("work_directory")) {
                        Object workDirObj = appData.get("work_directory");
                        if (workDirObj != null) {
                            app.setWorkDirectory(String.valueOf(workDirObj));
                        }
                    }
                    installedApps.add(app);
                }

                return new InstalledAppListResult(
                    result.getRequestId(),
                    true,
                    installedApps,
                    ""
                );
            } catch (Exception e) {
                logger.error("Failed to parse installed apps JSON", e);
                return new InstalledAppListResult(
                    result.getRequestId(),
                    false,
                    new ArrayList<>(),
                    "Failed to parse installed apps JSON: " + e.getMessage()
                );
            }
        } catch (Exception e) {
            logger.error("Unexpected error during getInstalledApps", e);
            return new InstalledAppListResult(
                "",
                false,
                new ArrayList<>(),
                "Failed to get installed apps: " + e.getMessage()
            );
        }
    }

    /**
     * Gets the list of installed applications with default parameters.
     * Defaults: startMenu=true, desktop=false, ignoreSystemApps=true
     *
     * @return InstalledAppListResult containing list of installed apps and error message if any
     */
    public InstalledAppListResult getInstalledApps() {
        return getInstalledApps(true, false, true);
    }

    // ==================== Mouse Operations ====================

    /**
     * Clicks the mouse at the specified screen coordinates.
     *
     * @param x X coordinate in pixels (0 is left edge of screen)
     * @param y Y coordinate in pixels (0 is top edge of screen)
     * @param button Mouse button to click. Defaults to LEFT
     * @return BoolResult containing success status and error message if any
     */
    public BoolResult clickMouse(int x, int y, MouseButton button) {
        return clickMouse(x, y, button.getValue());
    }

    /**
     * Clicks the mouse at the specified screen coordinates with LEFT button.
     *
     * @param x X coordinate in pixels
     * @param y Y coordinate in pixels
     * @return BoolResult containing success status and error message if any
     */
    public BoolResult clickMouse(int x, int y) {
        return clickMouse(x, y, MouseButton.LEFT);
    }

    /**
     * Clicks the mouse at the specified screen coordinates.
     *
     * @param x X coordinate in pixels
     * @param y Y coordinate in pixels
     * @param button Mouse button as string ("left", "right", "middle", "double_left")
     * @return BoolResult containing success status and error message if any
     */
    public BoolResult clickMouse(int x, int y, String button) {
        try {
            List<String> validButtons = Arrays.asList("left", "right", "middle", "double_left");
            if (!validButtons.contains(button)) {
                throw new IllegalArgumentException(
                    "Invalid button '" + button + "'. Must be one of " + validButtons
                );
            }

            Map<String, Object> args = new HashMap<>();
            args.put("x", x);
            args.put("y", y);
            args.put("button", button);

            logger.debug("Clicking mouse at ({}, {}) with button: {}", x, y, button);

            OperationResult result = callMcpTool("click_mouse", args);

            if (!result.isSuccess()) {
                return new BoolResult(
                    result.getRequestId(),
                    false,
                    null,
                    result.getErrorMessage()
                );
            }

            return new BoolResult(
                result.getRequestId(),
                true,
                true,
                ""
            );
        } catch (Exception e) {
            logger.error("Unexpected error during clickMouse", e);
            return new BoolResult(
                "",
                false,
                null,
                "Failed to click mouse: " + e.getMessage()
            );
        }
    }

    /**
     * Moves the mouse to the specified coordinates.
     *
     * @param x X coordinate
     * @param y Y coordinate
     * @return BoolResult containing success status and error message if any
     */
    public BoolResult moveMouse(int x, int y) {
        try {
            Map<String, Object> args = new HashMap<>();
            args.put("x", x);
            args.put("y", y);

            logger.debug("Moving mouse to ({}, {})", x, y);

            OperationResult result = callMcpTool("move_mouse", args);

            if (!result.isSuccess()) {
                return new BoolResult(
                    result.getRequestId(),
                    false,
                    null,
                    result.getErrorMessage()
                );
            }

            return new BoolResult(
                result.getRequestId(),
                true,
                true,
                ""
            );
        } catch (Exception e) {
            logger.error("Unexpected error during moveMouse", e);
            return new BoolResult(
                "",
                false,
                null,
                "Failed to move mouse: " + e.getMessage()
            );
        }
    }

    /**
     * Drags the mouse from one point to another.
     *
     * @param fromX Starting X coordinate
     * @param fromY Starting Y coordinate
     * @param toX Ending X coordinate
     * @param toY Ending Y coordinate
     * @param button Mouse button to use. Defaults to LEFT
     * @return BoolResult containing success status and error message if any
     */
    public BoolResult dragMouse(int fromX, int fromY, int toX, int toY, MouseButton button) {
        return dragMouse(fromX, fromY, toX, toY, button.getValue());
    }

    /**
     * Drags the mouse from one point to another with LEFT button.
     *
     * @param fromX Starting X coordinate
     * @param fromY Starting Y coordinate
     * @param toX Ending X coordinate
     * @param toY Ending Y coordinate
     * @return BoolResult containing success status and error message if any
     */
    public BoolResult dragMouse(int fromX, int fromY, int toX, int toY) {
        return dragMouse(fromX, fromY, toX, toY, MouseButton.LEFT);
    }

    /**
     * Drags the mouse from one point to another.
     *
     * @param fromX Starting X coordinate
     * @param fromY Starting Y coordinate
     * @param toX Ending X coordinate
     * @param toY Ending Y coordinate
     * @param button Mouse button as string ("left", "right", "middle")
     * @return BoolResult containing success status and error message if any
     */
    public BoolResult dragMouse(int fromX, int fromY, int toX, int toY, String button) {
        try {
            List<String> validButtons = Arrays.asList("left", "right", "middle");
            if (!validButtons.contains(button)) {
                throw new IllegalArgumentException(
                    "Invalid button '" + button + "'. Must be one of " + validButtons
                );
            }

            Map<String, Object> args = new HashMap<>();
            args.put("from_x", fromX);
            args.put("from_y", fromY);
            args.put("to_x", toX);
            args.put("to_y", toY);
            args.put("button", button);

            logger.debug("Dragging mouse from ({}, {}) to ({}, {}) with button: {}", fromX, fromY, toX, toY, button);

            OperationResult result = callMcpTool("drag_mouse", args);

            if (!result.isSuccess()) {
                return new BoolResult(
                    result.getRequestId(),
                    false,
                    null,
                    result.getErrorMessage()
                );
            }

            return new BoolResult(
                result.getRequestId(),
                true,
                true,
                ""
            );
        } catch (Exception e) {
            logger.error("Unexpected error during dragMouse", e);
            return new BoolResult(
                "",
                false,
                null,
                "Failed to drag mouse: " + e.getMessage()
            );
        }
    }

    /**
     * Scrolls the mouse wheel at the specified coordinates.
     *
     * @param x X coordinate
     * @param y Y coordinate
     * @param direction Scroll direction. Defaults to UP
     * @param amount Scroll amount. Defaults to 1
     * @return BoolResult containing success status and error message if any
     */
    public BoolResult scroll(int x, int y, ScrollDirection direction, int amount) {
        return scroll(x, y, direction.getValue(), amount);
    }

    /**
     * Scrolls the mouse wheel at the specified coordinates with default direction (UP) and amount (1).
     *
     * @param x X coordinate
     * @param y Y coordinate
     * @return BoolResult containing success status and error message if any
     */
    public BoolResult scroll(int x, int y) {
        return scroll(x, y, ScrollDirection.UP, 1);
    }

    /**
     * Scrolls the mouse wheel at the specified coordinates.
     *
     * @param x X coordinate
     * @param y Y coordinate
     * @param direction Scroll direction as string ("up", "down", "left", "right")
     * @param amount Scroll amount
     * @return BoolResult containing success status and error message if any
     */
    public BoolResult scroll(int x, int y, String direction, int amount) {
        try {
            List<String> validDirections = Arrays.asList("up", "down", "left", "right");
            if (!validDirections.contains(direction)) {
                throw new IllegalArgumentException(
                    "Invalid direction '" + direction + "'. Must be one of " + validDirections
                );
            }

            Map<String, Object> args = new HashMap<>();
            args.put("x", x);
            args.put("y", y);
            args.put("direction", direction);
            args.put("amount", amount);

            logger.debug("Scrolling at ({}, {}) direction: {} amount: {}", x, y, direction, amount);

            OperationResult result = callMcpTool("scroll", args);

            if (!result.isSuccess()) {
                return new BoolResult(
                    result.getRequestId(),
                    false,
                    null,
                    result.getErrorMessage()
                );
            }

            return new BoolResult(
                result.getRequestId(),
                true,
                true,
                ""
            );
        } catch (Exception e) {
            logger.error("Unexpected error during scroll", e);
            return new BoolResult(
                "",
                false,
                null,
                "Failed to scroll: " + e.getMessage()
            );
        }
    }

    /**
     * Gets the current cursor position.
     *
     * @return OperationResult containing cursor position data with keys 'x' and 'y', and error message if any
     */
    public OperationResult getCursorPosition() {
        try {
            logger.debug("Getting cursor position");

            OperationResult result = callMcpTool("get_cursor_position", new HashMap<>());

            if (!result.isSuccess()) {
                return new OperationResult(
                    result.getRequestId(),
                    false,
                    null,
                    result.getErrorMessage()
                );
            }

            return new OperationResult(
                result.getRequestId(),
                true,
                result.getData(),
                ""
            );
        } catch (Exception e) {
            logger.error("Unexpected error during getCursorPosition", e);
            return new OperationResult(
                "",
                false,
                null,
                "Failed to get cursor position: " + e.getMessage()
            );
        }
    }

    // ==================== Keyboard Operations ====================

    /**
     * Types text into the currently focused input field.
     *
     * @param text The text to input. Supports Unicode characters.
     * @return BoolResult containing success status and error message if any
     */
    public BoolResult inputText(String text) {
        try {
            Map<String, Object> args = new HashMap<>();
            args.put("text", text);

            logger.debug("Inputting text: {}", text.length() > 50 ? text.substring(0, 50) + "..." : text);

            OperationResult result = callMcpTool("input_text", args);

            if (!result.isSuccess()) {
                return new BoolResult(
                    result.getRequestId(),
                    false,
                    null,
                    result.getErrorMessage()
                );
            }

            return new BoolResult(
                result.getRequestId(),
                true,
                true,
                ""
            );
        } catch (Exception e) {
            logger.error("Unexpected error during inputText", e);
            return new BoolResult(
                "",
                false,
                null,
                "Failed to input text: " + e.getMessage()
            );
        }
    }

    /**
     * Presses the specified keys.
     *
     * @param keys List of keys to press (e.g., ["Ctrl", "a"])
     * @param hold Whether to hold the keys. Defaults to false
     * @return BoolResult containing success status and error message if any
     */
    public BoolResult pressKeys(List<String> keys, boolean hold) {
        try {
            Map<String, Object> args = new HashMap<>();
            args.put("keys", keys);
            args.put("hold", hold);

            logger.debug("Pressing keys: {} (hold: {})", keys, hold);

            OperationResult result = callMcpTool("press_keys", args);

            if (!result.isSuccess()) {
                return new BoolResult(
                    result.getRequestId(),
                    false,
                    null,
                    result.getErrorMessage()
                );
            }

            return new BoolResult(
                result.getRequestId(),
                true,
                true,
                ""
            );
        } catch (Exception e) {
            logger.error("Unexpected error during pressKeys", e);
            return new BoolResult(
                "",
                false,
                null,
                "Failed to press keys: " + e.getMessage()
            );
        }
    }

    /**
     * Presses the specified keys without holding.
     *
     * @param keys List of keys to press
     * @return BoolResult containing success status and error message if any
     */
    public BoolResult pressKeys(List<String> keys) {
        return pressKeys(keys, false);
    }

    /**
     * Releases the specified keys.
     *
     * @param keys List of keys to release (e.g., ["Ctrl", "a"])
     * @return BoolResult containing success status and error message if any
     */
    public BoolResult releaseKeys(List<String> keys) {
        try {
            Map<String, Object> args = new HashMap<>();
            args.put("keys", keys);

            logger.debug("Releasing keys: {}", keys);

            OperationResult result = callMcpTool("release_keys", args);

            if (!result.isSuccess()) {
                return new BoolResult(
                    result.getRequestId(),
                    false,
                    null,
                    result.getErrorMessage()
                );
            }

            return new BoolResult(
                result.getRequestId(),
                true,
                true,
                ""
            );
        } catch (Exception e) {
            logger.error("Unexpected error during releaseKeys", e);
            return new BoolResult(
                "",
                false,
                null,
                "Failed to release keys: " + e.getMessage()
            );
        }
    }

    // ==================== Screen Operations ====================

    /**
     * Gets the screen size and DPI scaling factor.
     *
     * @return OperationResult containing screen size data with keys 'width', 'height', and 'dpiScalingFactor',
     *         and error message if any
     */
    public OperationResult getScreenSize() {
        try {
            logger.debug("Getting screen size");

            OperationResult result = callMcpTool("get_screen_size", new HashMap<>());

            if (!result.isSuccess()) {
                return new OperationResult(
                    result.getRequestId(),
                    false,
                    null,
                    result.getErrorMessage()
                );
            }

            return new OperationResult(
                result.getRequestId(),
                true,
                result.getData(),
                ""
            );
        } catch (Exception e) {
            logger.error("Unexpected error during getScreenSize", e);
            return new OperationResult(
                "",
                false,
                null,
                "Failed to get screen size: " + e.getMessage()
            );
        }
    }

    /**
     * Takes a screenshot of the current screen.
     *
     * @return OperationResult containing the path/URL to the screenshot and error message if any
     */
    public OperationResult screenshot() {
        try {
            logger.debug("Taking screenshot");

            OperationResult result = callMcpTool("system_screenshot", new HashMap<>());

            if (!result.isSuccess()) {
                return new OperationResult(
                    result.getRequestId(),
                    false,
                    null,
                    result.getErrorMessage()
                );
            }

            return new OperationResult(
                result.getRequestId(),
                true,
                result.getData(),
                ""
            );
        } catch (Exception e) {
            logger.error("Unexpected error during screenshot", e);
            return new OperationResult(
                "",
                false,
                null,
                "Failed to take screenshot: " + e.getMessage()
            );
        }
    }

    // ==================== Window Management Operations ====================

    /**
     * Lists all root windows.
     *
     * @param timeoutMs Timeout in milliseconds. Defaults to 3000
     * @return WindowListResult containing list of windows and error message if any
     */
    public WindowListResult listRootWindows(int timeoutMs) {
        try {
            Map<String, Object> args = new HashMap<>();
            args.put("timeout_ms", timeoutMs);

            logger.debug("Listing root windows with timeout: {}ms", timeoutMs);

            OperationResult result = callMcpTool("list_root_windows", args);

            if (!result.isSuccess()) {
                return new WindowListResult(
                    result.getRequestId(),
                    false,
                    new ArrayList<>(),
                    result.getErrorMessage()
                );
            }

            try {
                String data = result.getData();
                if (data == null || data.isEmpty()) {
                    return new WindowListResult(
                        result.getRequestId(),
                        true,
                        new ArrayList<>(),
                        ""
                    );
                }

                List<Map<String, Object>> windowsJson = objectMapper.readValue(
                    data,
                    new TypeReference<List<Map<String, Object>>>() {}
                );

                List<Window> windows = new ArrayList<>();
                for (Map<String, Object> windowData : windowsJson) {
                    windows.add(parseWindow(windowData));
                }

                return new WindowListResult(
                    result.getRequestId(),
                    true,
                    windows,
                    ""
                );
            } catch (Exception e) {
                logger.error("Failed to parse windows JSON", e);
                return new WindowListResult(
                    result.getRequestId(),
                    false,
                    new ArrayList<>(),
                    "Failed to parse windows JSON: " + e.getMessage()
                );
            }
        } catch (Exception e) {
            logger.error("Unexpected error during listRootWindows", e);
            return new WindowListResult(
                "",
                false,
                new ArrayList<>(),
                "Failed to list root windows: " + e.getMessage()
            );
        }
    }

    /**
     * Lists all root windows with default timeout (3000ms).
     *
     * @return WindowListResult containing list of windows and error message if any
     */
    public WindowListResult listRootWindows() {
        return listRootWindows(3000);
    }

    /**
     * Gets the currently active window.
     *
     * @param timeoutMs Timeout in milliseconds. Defaults to 3000
     * @return WindowInfoResult containing active window info and error message if any
     */
    public WindowInfoResult getActiveWindow(int timeoutMs) {
        try {
            Map<String, Object> args = new HashMap<>();
            args.put("timeout_ms", timeoutMs);

            logger.debug("Getting active window with timeout: {}ms", timeoutMs);

            OperationResult result = callMcpTool("get_active_window", args);

            if (!result.isSuccess()) {
                return new WindowInfoResult(
                    result.getRequestId(),
                    false,
                    null,
                    result.getErrorMessage()
                );
            }

            try {
                String data = result.getData();
                if (data == null || data.isEmpty()) {
                    return new WindowInfoResult(
                        result.getRequestId(),
                        true,
                        null,
                        ""
                    );
                }

                Map<String, Object> windowData = objectMapper.readValue(
                    data,
                    new TypeReference<Map<String, Object>>() {}
                );

                Window window = parseWindow(windowData);

                return new WindowInfoResult(
                    result.getRequestId(),
                    true,
                    window,
                    ""
                );
            } catch (Exception e) {
                logger.error("Failed to parse window JSON", e);
                return new WindowInfoResult(
                    result.getRequestId(),
                    false,
                    null,
                    "Failed to parse window JSON: " + e.getMessage()
                );
            }
        } catch (Exception e) {
            logger.error("Unexpected error during getActiveWindow", e);
            return new WindowInfoResult(
                "",
                false,
                null,
                "Failed to get active window: " + e.getMessage()
            );
        }
    }

    /**
     * Gets the currently active window with default timeout (3000ms).
     *
     * @return WindowInfoResult containing active window info and error message if any
     */
    public WindowInfoResult getActiveWindow() {
        return getActiveWindow(3000);
    }

    /**
     * Activates the specified window.
     *
     * @param windowId The ID of the window to activate
     * @return BoolResult containing success status and error message if any
     */
    public BoolResult activateWindow(int windowId) {
        return windowOperation("activate_window", windowId);
    }

    /**
     * Closes the specified window.
     *
     * @param windowId The ID of the window to close
     * @return BoolResult containing success status and error message if any
     */
    public BoolResult closeWindow(int windowId) {
        return windowOperation("close_window", windowId);
    }

    /**
     * Maximizes the specified window.
     *
     * @param windowId The ID of the window to maximize
     * @return BoolResult containing success status and error message if any
     */
    public BoolResult maximizeWindow(int windowId) {
        return windowOperation("maximize_window", windowId);
    }

    /**
     * Minimizes the specified window.
     *
     * @param windowId The ID of the window to minimize
     * @return BoolResult containing success status and error message if any
     */
    public BoolResult minimizeWindow(int windowId) {
        return windowOperation("minimize_window", windowId);
    }

    /**
     * Restores the specified window.
     *
     * @param windowId The ID of the window to restore
     * @return BoolResult containing success status and error message if any
     */
    public BoolResult restoreWindow(int windowId) {
        return windowOperation("restore_window", windowId);
    }

    /**
     * Resizes the specified window.
     *
     * @param windowId The ID of the window to resize
     * @param width New width of the window
     * @param height New height of the window
     * @return BoolResult containing success status and error message if any
     */
    public BoolResult resizeWindow(int windowId, int width, int height) {
        try {
            Map<String, Object> args = new HashMap<>();
            args.put("window_id", windowId);
            args.put("width", width);
            args.put("height", height);

            logger.debug("Resizing window {} to {}x{}", windowId, width, height);

            OperationResult result = callMcpTool("resize_window", args);

            if (!result.isSuccess()) {
                return new BoolResult(
                    result.getRequestId(),
                    false,
                    null,
                    result.getErrorMessage()
                );
            }

            return new BoolResult(
                result.getRequestId(),
                true,
                true,
                ""
            );
        } catch (Exception e) {
            logger.error("Unexpected error during resizeWindow", e);
            return new BoolResult(
                "",
                false,
                null,
                "Failed to resize window: " + e.getMessage()
            );
        }
    }

    /**
     * Makes the specified window fullscreen.
     *
     * @param windowId The ID of the window to make fullscreen
     * @return BoolResult containing success status and error message if any
     */
    public BoolResult fullscreenWindow(int windowId) {
        return windowOperation("fullscreen_window", windowId);
    }

    /**
     * Toggles focus mode on or off.
     *
     * @param on True to enable focus mode, False to disable it
     * @return BoolResult containing success status and error message if any
     */
    public BoolResult focusMode(boolean on) {
        try {
            Map<String, Object> args = new HashMap<>();
            args.put("on", on);

            logger.debug("Setting focus mode: {}", on);

            OperationResult result = callMcpTool("focus_mode", args);

            if (!result.isSuccess()) {
                return new BoolResult(
                    result.getRequestId(),
                    false,
                    null,
                    result.getErrorMessage()
                );
            }

            return new BoolResult(
                result.getRequestId(),
                true,
                true,
                ""
            );
        } catch (Exception e) {
            logger.error("Unexpected error during focusMode", e);
            return new BoolResult(
                "",
                false,
                null,
                "Failed to toggle focus mode: " + e.getMessage()
            );
        }
    }

    // ==================== Helper Methods ====================

    /**
     * Helper method for window operations that only require window_id.
     */
    private BoolResult windowOperation(String toolName, int windowId) {
        try {
            Map<String, Object> args = new HashMap<>();
            args.put("window_id", windowId);

            logger.debug("Executing {} for window {}", toolName, windowId);

            OperationResult result = callMcpTool(toolName, args);

            if (!result.isSuccess()) {
                return new BoolResult(
                    result.getRequestId(),
                    false,
                    null,
                    result.getErrorMessage()
                );
            }

            return new BoolResult(
                result.getRequestId(),
                true,
                true,
                ""
            );
        } catch (Exception e) {
            logger.error("Unexpected error during {}", toolName, e);
            return new BoolResult(
                "",
                false,
                null,
                "Failed to " + toolName + ": " + e.getMessage()
            );
        }
    }

    /**
     * Helper method to parse Window object from JSON data.
     */
    private Window parseWindow(Map<String, Object> windowData) {
        Window window = new Window();
        if (windowData.containsKey("window_id")) {
            Object windowIdObj = windowData.get("window_id");
            if (windowIdObj instanceof Number) {
                window.setWindowId(((Number) windowIdObj).intValue());
            }
        }
        if (windowData.containsKey("title")) {
            window.setTitle(String.valueOf(windowData.get("title")));
        }
        if (windowData.containsKey("absolute_upper_left_x")) {
            Object xObj = windowData.get("absolute_upper_left_x");
            if (xObj instanceof Number) {
                window.setAbsoluteUpperLeftX(((Number) xObj).intValue());
            }
        }
        if (windowData.containsKey("absolute_upper_left_y")) {
            Object yObj = windowData.get("absolute_upper_left_y");
            if (yObj instanceof Number) {
                window.setAbsoluteUpperLeftY(((Number) yObj).intValue());
            }
        }
        if (windowData.containsKey("width")) {
            Object widthObj = windowData.get("width");
            if (widthObj instanceof Number) {
                window.setWidth(((Number) widthObj).intValue());
            }
        }
        if (windowData.containsKey("height")) {
            Object heightObj = windowData.get("height");
            if (heightObj instanceof Number) {
                window.setHeight(((Number) heightObj).intValue());
            }
        }
        if (windowData.containsKey("pid")) {
            Object pidObj = windowData.get("pid");
            if (pidObj instanceof Number) {
                window.setPid(((Number) pidObj).intValue());
            }
        }
        if (windowData.containsKey("pname")) {
            window.setPname(String.valueOf(windowData.get("pname")));
        }
        if (windowData.containsKey("child_windows")) {
            Object childWindowsObj = windowData.get("child_windows");
            if (childWindowsObj instanceof List) {
                @SuppressWarnings("unchecked")
                List<Map<String, Object>> childWindowsList = (List<Map<String, Object>>) childWindowsObj;
                List<Window> childWindows = new ArrayList<>();
                for (Map<String, Object> childData : childWindowsList) {
                    childWindows.add(parseWindow(childData));
                }
                window.setChildWindows(childWindows);
            }
        }
        return window;
    }
}

