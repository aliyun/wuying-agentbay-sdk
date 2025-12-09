package agentbay

import (
	"encoding/json"
	"fmt"
	"os"
	"regexp"
	"runtime/debug"
	"strings"

	"github.com/aliyun/wuying-agentbay-sdk/golang/internal/terminal"
)

// Log level constants
const (
	LOG_DEBUG = iota
	LOG_INFO
	LOG_WARN
	LOG_ERROR
)

// Color constants for terminal output
const (
	ColorReset  = "\033[0m"
	ColorGreen  = "\033[32m"
	ColorRed    = "\033[31m"
	ColorYellow = "\033[33m"
	ColorBlue   = "\033[34m"
)

// globalLogLevel (default is LOG_INFO)
var globalLogLevel = LOG_INFO

// File logging configuration
var (
	fileLoggingEnabled    = false
	logFilePath           string
	logFileMaxSize        int64 = 10 * 1024 * 1024 // 10MB default
	consoleLoggingEnabled       = true
	logFile               *os.File
)

// LoggerConfig holds configuration for file logging
type LoggerConfig struct {
	Level         string
	LogFile       string
	MaxFileSize   string
	EnableConsole *bool
}

// sensitiveFields names for data masking
var sensitiveFields = []string{
	"api_key", "apikey", "api-key",
	"password", "passwd", "pwd",
	"token", "access_token", "auth_token",
	"secret", "private_key",
	"authorization",
}

// Initialize log level from environment variable
func init() {
	if levelStr := os.Getenv("AGENTBAY_LOG_LEVEL"); levelStr != "" {
		level := parseLogLevel(levelStr)
		SetLogLevel(level)
	}
}

// parseLogLevel converts string to log level constant
func parseLogLevel(levelStr string) int {
	switch strings.ToUpper(levelStr) {
	case "DEBUG":
		return LOG_DEBUG
	case "INFO":
		return LOG_INFO
	case "WARNING", "WARN":
		return LOG_WARN
	case "ERROR":
		return LOG_ERROR
	default:
		return LOG_INFO // Default to INFO
	}
}

// SetLogLevel sets the global log level
//
// Example:
//
//	agentbay.SetLogLevel(agentbay.LOG_DEBUG)
func SetLogLevel(level int) {
	if level >= LOG_DEBUG && level <= LOG_ERROR {
		globalLogLevel = level
	}
}

// GetLogLevel returns the current global log level
//
// Example:
//
//	package main
//
//	import (
//		"fmt"
//		"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
//	)
//
//	func main() {
//		// Set log level to DEBUG
//		agentbay.SetLogLevel(agentbay.LOG_DEBUG)
//
//		// Check current level
//		currentLevel := agentbay.GetLogLevel()
//		fmt.Printf("Current log level: %d\n", currentLevel)
//	}
func GetLogLevel() int {
	return globalLogLevel
}

// parseFileSize parses size string like "10 MB" to bytes
func parseFileSize(sizeStr string) int64 {
	sizeStr = strings.TrimSpace(sizeStr)
	var value int64
	var unit string

	// Parse value and unit
	n, err := fmt.Sscanf(sizeStr, "%d %s", &value, &unit)
	if err != nil || n < 1 {
		return 10 * 1024 * 1024 // Default 10MB
	}

	unit = strings.ToUpper(unit)
	switch unit {
	case "KB":
		return value * 1024
	case "MB", "M":
		return value * 1024 * 1024
	case "GB", "G":
		return value * 1024 * 1024 * 1024
	default:
		return value * 1024 * 1024 // Default to MB
	}
}

// writeToFile writes a message to the log file with rotation
func writeToFile(message string) {
	if !fileLoggingEnabled || logFilePath == "" {
		return
	}

	// Check file size and rotate if necessary
	if logFile != nil {
		info, err := logFile.Stat()
		if err == nil && info.Size() >= logFileMaxSize {
			// Close current file
			logFile.Close()

			// Rotate: rename current to .1
			rotatedPath := logFilePath + ".1"
			os.Remove(rotatedPath) // Remove old backup
			os.Rename(logFilePath, rotatedPath)

			// Open new file
			logFile, _ = os.OpenFile(logFilePath, os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0644)
		}
	}

	// Open file if not already open
	if logFile == nil {
		var err error
		logFile, err = os.OpenFile(logFilePath, os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0644)
		if err != nil {
			return // Silently fail
		}
	}

	// Write to file
	if logFile != nil {
		logFile.WriteString(message + "\n")
	}
}

// SetupLogger configures the logger with file logging support
//
// Example:
//
//	config := agentbay.LoggerConfig{Level: "DEBUG", LogFile: "/tmp/agentbay.log"}
//	agentbay.SetupLogger(config)
func SetupLogger(config LoggerConfig) {
	if config.Level != "" {
		level := parseLogLevel(config.Level)
		SetLogLevel(level)
	}

	if config.LogFile != "" {
		// Close old log file if switching to a different file
		if logFile != nil && logFilePath != config.LogFile {
			logFile.Close()
			logFile = nil
		}

		logFilePath = config.LogFile
		fileLoggingEnabled = true

		// Create directory if needed
		dir := logFilePath[:strings.LastIndex(logFilePath, "/")]
		if dir != "" {
			os.MkdirAll(dir, 0755)
		}

		// Parse max file size
		if config.MaxFileSize != "" {
			logFileMaxSize = parseFileSize(config.MaxFileSize)
		}
	} else {
		fileLoggingEnabled = false
		if logFile != nil {
			logFile.Close()
			logFile = nil
		}
	}

	// Only update consoleLoggingEnabled if explicitly set
	if config.EnableConsole != nil {
		consoleLoggingEnabled = *config.EnableConsole
	}
}

// getColorCodes returns ANSI color codes based on environment detection
func getColorCodes() (reset, green, red, yellow, blue string) {
	// Priority 1: Check if stdout is a real terminal (TTY)
	// This is the most reliable indicator of an interactive environment
	if terminal.IsTerminal(os.Stdout.Fd()) {
		return ColorReset, ColorGreen, ColorRed, ColorYellow, ColorBlue
	}

	// Priority 2: Check FORCE_COLOR environment variable for explicit control
	// Users can set this to explicitly enable colors in non-TTY environments
	if os.Getenv("FORCE_COLOR") != "" {
		return ColorReset, ColorGreen, ColorRed, ColorYellow, ColorBlue
	}

	// Priority 3: Check if we're in an IDE environment
	// IDEs can display ANSI colors in their output pane even without TTY
	if isIDEEnvironment() {
		return ColorReset, ColorGreen, ColorRed, ColorYellow, ColorBlue
	}

	// Default: No colors - suitable for file output, CI/CD, and pipes
	return "", "", "", "", ""
}

// isIDEEnvironment detects if running in an IDE that supports ANSI colors
func isIDEEnvironment() bool {
	// Check for common IDE environment variables
	// VS Code
	if os.Getenv("TERM_PROGRAM") == "vscode" {
		return true
	}
	// GoLand / IntelliJ IDEA
	if os.Getenv("GOLAND") != "" {
		return true
	}
	if os.Getenv("IDEA_INITIAL_DIRECTORY") != "" {
		return true
	}
	// Generic IDE detection - TERM set to common IDE values
	term := os.Getenv("TERM")
	if term == "xterm-256color" || term == "xterm" || term == "screen" || term == "screen-256color" {
		return true
	}
	// Check if running via IDE test runner environment variable
	if os.Getenv("GO_TEST_IDE") != "" {
		return true
	}

	// Don't auto-enable colors for TERM=dumb or unknown environments
	return false
}

// logAPICall logs an API call with request parameters
//
// Example:
//
//	logAPICall("CreateSession", "ImageId=browser_latest")
func logAPICall(apiName, requestParams string) {
	if globalLogLevel > LOG_INFO {
		return
	}

	reset, _, _, _, blue := getColorCodes()
	coloredMsg := fmt.Sprintf("%s🔗 API Call: %s%s", blue, apiName, reset)
	plainMsg := fmt.Sprintf("🔗 API Call: %s", apiName)

	if consoleLoggingEnabled {
		fmt.Println(coloredMsg)
	}
	writeToFile(plainMsg)

	if requestParams != "" && globalLogLevel <= LOG_DEBUG {
		requestMsg := fmt.Sprintf("   Request: %s", requestParams)
		if consoleLoggingEnabled {
			fmt.Println(requestMsg)
		}
		writeToFile(requestMsg)
	}
}

// logAPIResponseWithDetails logs a structured API response with key fields
//
// Example:
//
//	keyFields := map[string]interface{}{"session_id": "abc123"}
//	logAPIResponseWithDetails("CreateSession", "req-123", true, keyFields, "")
func logAPIResponseWithDetails(apiName, requestID string, success bool, keyFields map[string]interface{}, fullResponse string) {
	if globalLogLevel > LOG_INFO {
		return
	}

	reset, green, red, _, blue := getColorCodes()

	if success {
		coloredMsg := fmt.Sprintf("%s✅ API Response: %s", green, apiName)
		plainMsg := fmt.Sprintf("✅ API Response: %s", apiName)

		if requestID != "" {
			coloredMsg += fmt.Sprintf(", RequestId=%s", requestID)
			plainMsg += fmt.Sprintf(", RequestId=%s", requestID)
		}

		if consoleLoggingEnabled {
			fmt.Printf("%s%s\n", coloredMsg, reset)
		}
		writeToFile(plainMsg)

		if keyFields != nil && len(keyFields) > 0 {
			for key, value := range keyFields {
				coloredField := fmt.Sprintf("%s   └─ %s=%v%s", green, key, value, reset)
				plainField := fmt.Sprintf("   └─ %s=%v", key, value)

				if consoleLoggingEnabled {
					fmt.Println(coloredField)
				}
				writeToFile(plainField)
			}
		}

		if fullResponse != "" && globalLogLevel <= LOG_DEBUG {
			coloredResp := fmt.Sprintf("%s📥 Full Response: %s%s", blue, fullResponse, reset)
			plainResp := fmt.Sprintf("📥 Full Response: %s", fullResponse)

			if consoleLoggingEnabled {
				fmt.Println(coloredResp)
			}
			writeToFile(plainResp)
		}
	} else {
		coloredMsg := fmt.Sprintf("%s❌ API Response Failed: %s", red, apiName)
		plainMsg := fmt.Sprintf("❌ API Response Failed: %s", apiName)

		if requestID != "" {
			coloredMsg += fmt.Sprintf(", RequestId=%s", requestID)
			plainMsg += fmt.Sprintf(", RequestId=%s", requestID)
		}

		if consoleLoggingEnabled {
			fmt.Printf("%s%s\n", coloredMsg, reset)
		}
		writeToFile(plainMsg)

		if fullResponse != "" && globalLogLevel <= LOG_DEBUG {
			coloredResp := fmt.Sprintf("%s📥 Response: %s%s", red, fullResponse, reset)
			plainResp := fmt.Sprintf("📥 Response: %s", fullResponse)

			if consoleLoggingEnabled {
				fmt.Println(coloredResp)
			}
			writeToFile(plainResp)
		}
	}
}

// logOperationError logs an operation error with optional stack trace
//
// Example:
//
//	logOperationError("CreateSession", "connection timeout", false)
func logOperationError(operation, errorMsg string, withStack bool) {
	if globalLogLevel > LOG_ERROR {
		return
	}

	reset, _, red, _, _ := getColorCodes()

	coloredFail := fmt.Sprintf("%s❌ Failed: %s%s", red, operation, reset)
	plainFail := fmt.Sprintf("❌ Failed: %s", operation)

	if consoleLoggingEnabled {
		fmt.Println(coloredFail)
	}
	writeToFile(plainFail)

	coloredError := fmt.Sprintf("%s💥 Error: %s%s", red, errorMsg, reset)
	plainError := fmt.Sprintf("💥 Error: %s", errorMsg)

	if consoleLoggingEnabled {
		fmt.Println(coloredError)
	}
	writeToFile(plainError)

	if withStack {
		stack := debug.Stack()
		coloredStack := fmt.Sprintf("%s[Stack Trace]:\n%s%s", red, string(stack), reset)
		plainStack := fmt.Sprintf("[Stack Trace]:\n%s", string(stack))

		if consoleLoggingEnabled {
			fmt.Println(coloredStack)
		}
		writeToFile(plainStack)
	}
}

// logCodeExecutionOutput extracts and logs the actual code execution output from run_code response
//
// Example:
//
//	client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
//	result, _ := client.Create(agentbay.NewCreateSessionParams().WithImageId("code_latest"))
//	defer result.Session.Delete()
//	execResult, _ := result.Session.Code.RunCode("print('Hello')", "python")
//	logCodeExecutionOutput(execResult.RequestID, execResult.Output)
func logCodeExecutionOutput(requestID, rawOutput string) {
	if globalLogLevel > LOG_INFO {
		return
	}

	// Parse the JSON response to extract the actual code output
	var response struct {
		Content []struct {
			Text string `json:"text"`
			Type string `json:"type"`
		} `json:"content"`
		IsError        bool   `json:"isError"`
		ParsedToolName string `json:"parsedToolName"`
	}

	if err := json.Unmarshal([]byte(rawOutput), &response); err != nil {
		// If parsing fails, just return without logging
		return
	}

	// Extract text from all content items
	var texts []string
	for _, item := range response.Content {
		if item.Type == "text" {
			texts = append(texts, item.Text)
		}
	}

	if len(texts) == 0 {
		return
	}

	actualOutput := strings.Join(texts, "")
	reset, green, _, _, _ := getColorCodes()

	// Format the output with a clear separator
	coloredHeader := fmt.Sprintf("%s📋 Code Execution Output (RequestID: %s):%s", green, requestID, reset)
	plainHeader := fmt.Sprintf("📋 Code Execution Output (RequestID: %s):", requestID)

	if consoleLoggingEnabled {
		fmt.Println(coloredHeader)
		// Print each line with indentation
		lines := strings.Split(strings.TrimRight(actualOutput, "\n"), "\n")
		for _, line := range lines {
			fmt.Printf("%s   %s%s\n", green, line, reset)
		}
	}

	writeToFile(plainHeader)
	// Write to file with indentation
	lines := strings.Split(strings.TrimRight(actualOutput, "\n"), "\n")
	for _, line := range lines {
		writeToFile(fmt.Sprintf("   %s", line))
	}
}

// maskSensitiveData recursively masks sensitive information in data structures
//
// Example:
//
//	package main
//
//	import (
//		"fmt"
//		"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
//	)
//
//	func main() {
//		// Create data with sensitive information
//		data := map[string]interface{}{
//			"api_key":    "sk_live_1234567890",
//			"password":   "secret123",
//			"auth_token": "Bearer xyz",
//			"username":   "john_doe",
//		}
//
//		// Mask sensitive data
//		masked := agentbay.maskSensitiveData(data)
//		fmt.Printf("Masked data: %v\n", masked)
//		// Output: Masked data: map[api_key:sk****90 auth_token:Be****yz password:se****23 username:john_doe]
//	}
func maskSensitiveData(data interface{}) interface{} {
	return maskSensitiveDataInternal(data, sensitiveFields)
}

func maskSensitiveDataInternal(data interface{}, fields []string) interface{} {
	switch v := data.(type) {
	case map[string]interface{}:
		masked := make(map[string]interface{})
		for key, value := range v {
			if isSensitiveField(key, fields) {
				if str, ok := value.(string); ok && len(str) > 4 {
					// Keep first 2 and last 2 chars, mask the middle
					masked[key] = str[:2] + "****" + str[len(str)-2:]
				} else {
					masked[key] = "****"
				}
			} else {
				masked[key] = maskSensitiveDataInternal(value, fields)
			}
		}
		return masked

	case []interface{}:
		masked := make([]interface{}, len(v))
		for i, item := range v {
			masked[i] = maskSensitiveDataInternal(item, fields)
		}
		return masked

	case string:
		// Don't mask plain strings, only dict keys
		return v

	default:
		return data
	}
}

func isSensitiveField(fieldName string, sensitiveFields []string) bool {
	lowerField := strings.ToLower(fieldName)
	for _, field := range sensitiveFields {
		if strings.Contains(lowerField, field) {
			return true
		}
	}
	return false
}

// maskSensitiveDataString masks sensitive information in a JSON string
func maskSensitiveDataString(jsonStr string) string {
	var data map[string]interface{}
	if err := json.Unmarshal([]byte(jsonStr), &data); err != nil {
		// If not JSON, try regex masking
		return maskSensitiveDataWithRegex(jsonStr)
	}

	masked := maskSensitiveData(data)
	if result, err := json.Marshal(masked); err == nil {
		return string(result)
	}

	return jsonStr
}

// maskSensitiveDataWithRegex masks sensitive data using regex patterns
func maskSensitiveDataWithRegex(str string) string {
	patterns := []string{
		`(api[_-]?key=)[^\s&,}]+`,
		`(password=)[^\s&,}]+`,
		`(token=)[^\s&,}]+`,
		`(authorization:\s*)[^\s,}]+`,
	}

	result := str
	for _, pattern := range patterns {
		re := regexp.MustCompile("(?i)" + pattern)
		result = re.ReplaceAllString(result, "$1****")
	}

	return result
}

// LogInfo logs an informational message
//
// Example:
//
//	agentbay.LogInfo("Session created successfully")
func LogInfo(message string) {
	if globalLogLevel > LOG_INFO {
		return
	}

	reset, _, _, _, blue := getColorCodes()
	coloredMsg := fmt.Sprintf("%sℹ️  %s%s", blue, message, reset)
	plainMsg := fmt.Sprintf("ℹ️  %s", message)

	if consoleLoggingEnabled {
		fmt.Println(coloredMsg)
	}
	writeToFile(plainMsg)
}

// LogDebug logs a debug message
//
// Example:
//
//	agentbay.LogDebug("Processing request parameters")
func LogDebug(message string) {
	if globalLogLevel > LOG_DEBUG {
		return
	}

	reset, _, _, _, _ := getColorCodes()
	coloredMsg := fmt.Sprintf("%s🐛 %s%s", reset, message, reset)
	plainMsg := fmt.Sprintf("🐛 %s", message)

	if consoleLoggingEnabled {
		fmt.Println(coloredMsg)
	}
	writeToFile(plainMsg)
}

// logInfoWithColor logs an informational message with custom color
//
// Example:
//
//	logInfoWithColor("Important notification")
func logInfoWithColor(message string) {
	if globalLogLevel > LOG_INFO {
		return
	}

	reset, _, red, _, _ := getColorCodes()
	coloredMsg := fmt.Sprintf("%sℹ️  %s%s", red, message, reset)
	plainMsg := fmt.Sprintf("ℹ️  %s", message)

	if consoleLoggingEnabled {
		fmt.Println(coloredMsg)
	}
	writeToFile(plainMsg)
}
