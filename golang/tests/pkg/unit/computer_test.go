package agentbay_test

import (
	"testing"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/computer"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/models"
	"github.com/aliyun/wuying-agentbay-sdk/golang/tests/pkg/unit/mock"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/suite"
)

type ComputerTestSuite struct {
	suite.Suite
	mockSession *mock.MockSessionForComputer
	computer    *computer.Computer
}

func (suite *ComputerTestSuite) SetupTest() {
	suite.mockSession = &mock.MockSessionForComputer{}
	suite.computer = computer.NewComputer(suite.mockSession)
}

func (suite *ComputerTestSuite) TearDownTest() {
	suite.mockSession.AssertExpectations(suite.T())
}

// Test ClickMouse functionality
func (suite *ComputerTestSuite) TestClickMouse_Success() {
	// Arrange
	expectedResult := &models.McpToolResult{
		Success:      true,
		RequestID:    "test-click-123",
		ErrorMessage: "",
	}

	suite.mockSession.On("CallMcpTool", "click_mouse", map[string]interface{}{
		"x":      100,
		"y":      200,
		"button": "left",
	}).Return(expectedResult, nil)

	// Act
	result := suite.computer.ClickMouse(100, 200, computer.MouseButtonLeft)

	// Assert
	assert.True(suite.T(), result.Success)
	assert.Equal(suite.T(), "test-click-123", result.RequestID)
	assert.Empty(suite.T(), result.ErrorMessage)
}

func (suite *ComputerTestSuite) TestClickMouse_InvalidButton() {
	// Act
	result := suite.computer.ClickMouse(100, 200, computer.MouseButton("invalid"))

	// Assert
	assert.False(suite.T(), result.Success)
	assert.Contains(suite.T(), result.ErrorMessage, "invalid button")
	assert.Contains(suite.T(), result.ErrorMessage, "left")
	assert.Contains(suite.T(), result.ErrorMessage, "right")
	assert.Contains(suite.T(), result.ErrorMessage, "middle")
	assert.Contains(suite.T(), result.ErrorMessage, "double_left")
}

func (suite *ComputerTestSuite) TestClickMouse_WithRightButton() {
	// Arrange
	expectedResult := &models.McpToolResult{
		Success:      true,
		RequestID:    "test-click-right",
		ErrorMessage: "",
	}

	suite.mockSession.On("CallMcpTool", "click_mouse", map[string]interface{}{
		"x":      100,
		"y":      200,
		"button": "right",
	}).Return(expectedResult, nil)

	// Act
	result := suite.computer.ClickMouse(100, 200, computer.MouseButtonRight)

	// Assert
	assert.True(suite.T(), result.Success)
}

func (suite *ComputerTestSuite) TestClickMouse_WithDoubleLeft() {
	// Arrange
	expectedResult := &models.McpToolResult{
		Success:      true,
		RequestID:    "test-click-double",
		ErrorMessage: "",
	}

	suite.mockSession.On("CallMcpTool", "click_mouse", map[string]interface{}{
		"x":      100,
		"y":      200,
		"button": "double_left",
	}).Return(expectedResult, nil)

	// Act
	result := suite.computer.ClickMouse(100, 200, computer.MouseButtonDoubleLeft)

	// Assert
	assert.True(suite.T(), result.Success)
}

func (suite *ComputerTestSuite) TestClickMouse_McpToolError() {
	// Arrange
	expectedResult := &models.McpToolResult{
		Success:      false,
		RequestID:    "test-click-error",
		ErrorMessage: "MCP tool failed",
	}

	suite.mockSession.On("CallMcpTool", "click_mouse", map[string]interface{}{
		"x":      100,
		"y":      200,
		"button": "left",
	}).Return(expectedResult, nil)

	// Act
	result := suite.computer.ClickMouse(100, 200, computer.MouseButtonLeft)

	// Assert
	assert.False(suite.T(), result.Success)
	assert.Equal(suite.T(), "test-click-error", result.RequestID)
	assert.Equal(suite.T(), "MCP tool failed", result.ErrorMessage)
}

// Test MoveMouse functionality
func (suite *ComputerTestSuite) TestMoveMouse_Success() {
	// Arrange
	expectedResult := &models.McpToolResult{
		Success:      true,
		RequestID:    "test-move-456",
		ErrorMessage: "",
	}

	suite.mockSession.On("CallMcpTool", "move_mouse", map[string]interface{}{
		"x": 150,
		"y": 250,
	}).Return(expectedResult, nil)

	// Act
	result := suite.computer.MoveMouse(150, 250)

	// Assert
	assert.True(suite.T(), result.Success)
	assert.Equal(suite.T(), "test-move-456", result.RequestID)
	assert.Empty(suite.T(), result.ErrorMessage)
}

// Test DragMouse functionality
func (suite *ComputerTestSuite) TestDragMouse_Success() {
	// Arrange
	expectedResult := &models.McpToolResult{
		Success:      true,
		RequestID:    "test-drag-789",
		ErrorMessage: "",
	}

	suite.mockSession.On("CallMcpTool", "drag_mouse", map[string]interface{}{
		"from_x": 100,
		"from_y": 200,
		"to_x":   300,
		"to_y":   400,
		"button": "left",
	}).Return(expectedResult, nil)

	// Act
	result := suite.computer.DragMouse(100, 200, 300, 400, computer.MouseButtonLeft)

	// Assert
	assert.True(suite.T(), result.Success)
	assert.Equal(suite.T(), "test-drag-789", result.RequestID)
}

func (suite *ComputerTestSuite) TestDragMouse_InvalidButton() {
	// Act
	result := suite.computer.DragMouse(100, 200, 300, 400, computer.MouseButton("invalid"))

	// Assert
	assert.False(suite.T(), result.Success)
	assert.Contains(suite.T(), result.ErrorMessage, "invalid button")
}

// Test Scroll functionality
func (suite *ComputerTestSuite) TestScroll_Success() {
	// Arrange
	expectedResult := &models.McpToolResult{
		Success:      true,
		RequestID:    "test-scroll-abc",
		ErrorMessage: "",
	}

	suite.mockSession.On("CallMcpTool", "scroll", map[string]interface{}{
		"x":         100,
		"y":         200,
		"direction": "up",
		"amount":    3,
	}).Return(expectedResult, nil)

	// Act
	result := suite.computer.Scroll(100, 200, computer.ScrollDirectionUp, 3)

	// Assert
	assert.True(suite.T(), result.Success)
	assert.Equal(suite.T(), "test-scroll-abc", result.RequestID)
}

func (suite *ComputerTestSuite) TestScroll_WithDownDirection() {
	// Arrange
	expectedResult := &models.McpToolResult{
		Success:      true,
		RequestID:    "test-scroll-down",
		ErrorMessage: "",
	}

	suite.mockSession.On("CallMcpTool", "scroll", map[string]interface{}{
		"x":         100,
		"y":         200,
		"direction": "down",
		"amount":    5,
	}).Return(expectedResult, nil)

	// Act
	result := suite.computer.Scroll(100, 200, computer.ScrollDirectionDown, 5)

	// Assert
	assert.True(suite.T(), result.Success)
}

func (suite *ComputerTestSuite) TestScroll_InvalidDirection() {
	// Act
	result := suite.computer.Scroll(100, 200, computer.ScrollDirection("diagonal"), 1)

	// Assert
	assert.False(suite.T(), result.Success)
	assert.Contains(suite.T(), result.ErrorMessage, "invalid direction")
	assert.Contains(suite.T(), result.ErrorMessage, "up")
	assert.Contains(suite.T(), result.ErrorMessage, "down")
	assert.Contains(suite.T(), result.ErrorMessage, "left")
	assert.Contains(suite.T(), result.ErrorMessage, "right")
}

// Test GetCursorPosition functionality
func (suite *ComputerTestSuite) TestGetCursorPosition_Success() {
	// Arrange
	expectedResult := &models.McpToolResult{
		Success:      true,
		RequestID:    "test-cursor-def",
		Data:         `{"x": 150, "y": 250}`,
		ErrorMessage: "",
	}

	suite.mockSession.On("CallMcpTool", "get_cursor_position", map[string]interface{}{}).Return(expectedResult, nil)

	// Act
	result := suite.computer.GetCursorPosition()

	// Assert
	assert.Equal(suite.T(), "test-cursor-def", result.RequestID)
	assert.Equal(suite.T(), 150, result.X)
	assert.Equal(suite.T(), 250, result.Y)
	assert.Empty(suite.T(), result.ErrorMessage)
}

func (suite *ComputerTestSuite) TestGetCursorPosition_InvalidJSON() {
	// Arrange
	expectedResult := &models.McpToolResult{
		Success:      true,
		RequestID:    "test-cursor-invalid",
		Data:         `{"x": "invalid", "y": 250}`,
		ErrorMessage: "",
	}

	suite.mockSession.On("CallMcpTool", "get_cursor_position", map[string]interface{}{}).Return(expectedResult, nil)

	// Act
	result := suite.computer.GetCursorPosition()

	// Assert
	assert.Equal(suite.T(), "test-cursor-invalid", result.RequestID)
	assert.Contains(suite.T(), result.ErrorMessage, "failed to parse cursor position")
}

// Test InputText functionality
func (suite *ComputerTestSuite) TestInputText_Success() {
	// Arrange
	expectedResult := &models.McpToolResult{
		Success:      true,
		RequestID:    "test-input-ghi",
		ErrorMessage: "",
	}

	suite.mockSession.On("CallMcpTool", "input_text", map[string]interface{}{
		"text": "Hello World",
	}).Return(expectedResult, nil)

	// Act
	result := suite.computer.InputText("Hello World")

	// Assert
	assert.True(suite.T(), result.Success)
	assert.Equal(suite.T(), "test-input-ghi", result.RequestID)
}

// Test PressKeys functionality
func (suite *ComputerTestSuite) TestPressKeys_Success() {
	// Arrange
	expectedResult := &models.McpToolResult{
		Success:      true,
		RequestID:    "test-press-jkl",
		ErrorMessage: "",
	}

	suite.mockSession.On("CallMcpTool", "press_keys", map[string]interface{}{
		"keys": []string{"Ctrl", "C"},
		"hold": false,
	}).Return(expectedResult, nil)

	// Act
	result := suite.computer.PressKeys([]string{"Ctrl", "C"}, false)

	// Assert
	assert.True(suite.T(), result.Success)
	assert.Equal(suite.T(), "test-press-jkl", result.RequestID)
}

func (suite *ComputerTestSuite) TestPressKeys_WithHold() {
	// Arrange
	expectedResult := &models.McpToolResult{
		Success:      true,
		RequestID:    "test-press-hold",
		ErrorMessage: "",
	}

	suite.mockSession.On("CallMcpTool", "press_keys", map[string]interface{}{
		"keys": []string{"Alt", "Tab"},
		"hold": true,
	}).Return(expectedResult, nil)

	// Act
	result := suite.computer.PressKeys([]string{"Alt", "Tab"}, true)

	// Assert
	assert.True(suite.T(), result.Success)
	assert.Equal(suite.T(), "test-press-hold", result.RequestID)
}

// Test ReleaseKeys functionality
func (suite *ComputerTestSuite) TestReleaseKeys_Success() {
	// Arrange
	expectedResult := &models.McpToolResult{
		Success:      true,
		RequestID:    "test-release-mno",
		ErrorMessage: "",
	}

	suite.mockSession.On("CallMcpTool", "release_keys", map[string]interface{}{
		"keys": []string{"Ctrl", "C"},
	}).Return(expectedResult, nil)

	// Act
	result := suite.computer.ReleaseKeys([]string{"Ctrl", "C"})

	// Assert
	assert.True(suite.T(), result.Success)
	assert.Equal(suite.T(), "test-release-mno", result.RequestID)
}

// Test GetScreenSize functionality
func (suite *ComputerTestSuite) TestGetScreenSize_Success() {
	// Arrange
	expectedResult := &models.McpToolResult{
		Success:      true,
		RequestID:    "test-screen-pqr",
		Data:         `{"width": 1920, "height": 1080, "dpiScalingFactor": 1.5}`,
		ErrorMessage: "",
	}

	suite.mockSession.On("CallMcpTool", "get_screen_size", map[string]interface{}{}).Return(expectedResult, nil)

	// Act
	result := suite.computer.GetScreenSize()

	// Assert
	assert.Equal(suite.T(), "test-screen-pqr", result.RequestID)
	assert.Equal(suite.T(), 1920, result.Width)
	assert.Equal(suite.T(), 1080, result.Height)
	assert.Equal(suite.T(), 1.5, result.DpiScalingFactor)
	assert.Empty(suite.T(), result.ErrorMessage)
}

// Test Screenshot functionality
func (suite *ComputerTestSuite) TestScreenshot_Success() {
	// Arrange
	expectedResult := &models.McpToolResult{
		Success:      true,
		RequestID:    "test-screenshot-stu",
		Data:         "https://example.com/screenshot.png",
		ErrorMessage: "",
	}

	suite.mockSession.On("CallMcpTool", "system_screenshot", map[string]interface{}{}).Return(expectedResult, nil)

	// Act
	result := suite.computer.Screenshot()

	// Assert
	assert.Equal(suite.T(), "test-screenshot-stu", result.RequestID)
	assert.Equal(suite.T(), "https://example.com/screenshot.png", result.Data)
	assert.Empty(suite.T(), result.ErrorMessage)
}

// Test StartApp functionality
func (suite *ComputerTestSuite) TestStartApp_Success() {
	// Arrange
	expectedResult := &models.McpToolResult{
		Success:      true,
		RequestID:    "test-start-app-123",
		Data:         `[{"pname": "notepad.exe", "pid": 1234, "cmdline": "notepad.exe"}]`,
		ErrorMessage: "",
	}

	suite.mockSession.On("CallMcpTool", "start_app", map[string]interface{}{
		"start_cmd": "notepad.exe",
	}).Return(expectedResult, nil)

	// Act
	result, err := suite.computer.StartApp("notepad.exe", "", "")

	// Assert
	assert.NoError(suite.T(), err)
	assert.NotNil(suite.T(), result)
	assert.Equal(suite.T(), "test-start-app-123", result.RequestID)
	assert.Len(suite.T(), result.Processes, 1)
	assert.Equal(suite.T(), "notepad.exe", result.Processes[0].PName)
	assert.Equal(suite.T(), 1234, result.Processes[0].PID)
}

func (suite *ComputerTestSuite) TestStartApp_McpToolError() {
	// Arrange
	expectedResult := &models.McpToolResult{
		Success:      false,
		RequestID:    "test-start-app-error",
		ErrorMessage: "Failed to start app",
	}

	suite.mockSession.On("CallMcpTool", "start_app", map[string]interface{}{
		"start_cmd": "invalid.exe",
	}).Return(expectedResult, nil)

	// Act
	result, err := suite.computer.StartApp("invalid.exe", "", "")

	// Assert
	assert.Error(suite.T(), err)
	assert.Nil(suite.T(), result)
	assert.Contains(suite.T(), err.Error(), "Failed to start app")
}

func (suite *ComputerTestSuite) TestStartApp_WithWorkDirAndActivity() {
	// Arrange
	expectedResult := &models.McpToolResult{
		Success:      true,
		RequestID:    "test-start-app-args",
		Data:         `[]`,
		ErrorMessage: "",
	}

	suite.mockSession.On("CallMcpTool", "start_app", map[string]interface{}{
		"start_cmd":      "cmd.exe",
		"work_directory": "C:\\",
		"activity":       "MainActivity",
	}).Return(expectedResult, nil)

	// Act
	result, err := suite.computer.StartApp("cmd.exe", "C:\\", "MainActivity")

	// Assert
	assert.NoError(suite.T(), err)
	assert.NotNil(suite.T(), result)
	assert.Equal(suite.T(), "test-start-app-args", result.RequestID)
	assert.Empty(suite.T(), result.ErrorMessage)
}

// Test GetInstalledApps functionality
func (suite *ComputerTestSuite) TestGetInstalledApps_Success() {
	// Arrange
	expectedResult := &models.McpToolResult{
		Success:      true,
		RequestID:    "test-get-apps-123",
		Data:         `[{"name": "Notepad", "start_cmd": "notepad.exe", "stop_cmd": "taskkill /F /IM notepad.exe", "work_directory": ""}]`,
		ErrorMessage: "",
	}

	suite.mockSession.On("CallMcpTool", "get_installed_apps", map[string]interface{}{
		"start_menu":         true,
		"desktop":            false,
		"ignore_system_apps": true,
	}).Return(expectedResult, nil)

	// Act
	result, err := suite.computer.GetInstalledApps(true, false, true)

	// Assert
	assert.NoError(suite.T(), err)
	assert.NotNil(suite.T(), result)
	assert.Equal(suite.T(), "test-get-apps-123", result.RequestID)
	assert.Len(suite.T(), result.Apps, 1)
	assert.Equal(suite.T(), "Notepad", result.Apps[0].Name)
	assert.Equal(suite.T(), "notepad.exe", result.Apps[0].StartCmd)
}

func (suite *ComputerTestSuite) TestGetInstalledApps_Error() {
	// Arrange
	expectedResult := &models.McpToolResult{
		Success:      false,
		RequestID:    "test-get-apps-error",
		ErrorMessage: "Failed to get apps",
	}

	suite.mockSession.On("CallMcpTool", "get_installed_apps", map[string]interface{}{
		"start_menu":         true,
		"desktop":            true,
		"ignore_system_apps": true,
	}).Return(expectedResult, nil)

	// Act
	result, err := suite.computer.GetInstalledApps(true, true, true)

	// Assert
	assert.Error(suite.T(), err)
	assert.Nil(suite.T(), result)
	assert.Contains(suite.T(), err.Error(), "Failed to get apps")
}

// Test ListVisibleApps functionality
func (suite *ComputerTestSuite) TestListVisibleApps_Success() {
	// Arrange
	expectedResult := &models.McpToolResult{
		Success:      true,
		RequestID:    "test-visible-apps-123",
		Data:         `[{"pname": "chrome.exe", "pid": 4567, "cmdline": "chrome.exe"}]`,
		ErrorMessage: "",
	}

	suite.mockSession.On("CallMcpTool", "list_visible_apps", map[string]interface{}{}).Return(expectedResult, nil)

	// Act
	result, err := suite.computer.ListVisibleApps()

	// Assert
	assert.NoError(suite.T(), err)
	assert.NotNil(suite.T(), result)
	assert.Equal(suite.T(), "test-visible-apps-123", result.RequestID)
	assert.Len(suite.T(), result.Processes, 1)
	assert.Equal(suite.T(), "chrome.exe", result.Processes[0].PName)
}

// Test StopAppByPName functionality
func (suite *ComputerTestSuite) TestStopAppByPName_Success() {
	// Arrange
	expectedResult := &models.McpToolResult{
		Success:      true,
		RequestID:    "test-stop-pname-123",
		ErrorMessage: "",
	}

	suite.mockSession.On("CallMcpTool", "stop_app_by_pname", map[string]interface{}{
		"pname": "notepad.exe",
	}).Return(expectedResult, nil)

	// Act
	result := suite.computer.StopAppByPName("notepad.exe")

	// Assert
	assert.True(suite.T(), result.Success)
	assert.Equal(suite.T(), "test-stop-pname-123", result.RequestID)
	assert.Empty(suite.T(), result.ErrorMessage)
}

// Test StopAppByPID functionality
func (suite *ComputerTestSuite) TestStopAppByPID_Success() {
	// Arrange
	expectedResult := &models.McpToolResult{
		Success:      true,
		RequestID:    "test-stop-pid-123",
		ErrorMessage: "",
	}

	suite.mockSession.On("CallMcpTool", "stop_app_by_pid", map[string]interface{}{
		"pid": 1234,
	}).Return(expectedResult, nil)

	// Act
	result := suite.computer.StopAppByPID(1234)

	// Assert
	assert.True(suite.T(), result.Success)
	assert.Equal(suite.T(), "test-stop-pid-123", result.RequestID)
	assert.Empty(suite.T(), result.ErrorMessage)
}

// Test StopAppByCmd functionality
func (suite *ComputerTestSuite) TestStopAppByCmd_Success() {
	// Arrange
	expectedResult := &models.McpToolResult{
		Success:      true,
		RequestID:    "test-stop-cmd-123",
		ErrorMessage: "",
	}

	suite.mockSession.On("CallMcpTool", "stop_app_by_cmd", map[string]interface{}{
		"stop_cmd": "kill notepad",
	}).Return(expectedResult, nil)

	// Act
	result := suite.computer.StopAppByCmd("kill notepad")

	// Assert
	assert.True(suite.T(), result.Success)
	assert.Equal(suite.T(), "test-stop-cmd-123", result.RequestID)
	assert.Empty(suite.T(), result.ErrorMessage)
}

// Test edge cases and error scenarios
func (suite *ComputerTestSuite) TestClickMouse_AllButtonTypes() {
	testCases := []struct {
		button    computer.MouseButton
		buttonStr string
	}{
		{computer.MouseButtonLeft, "left"},
		{computer.MouseButtonRight, "right"},
		{computer.MouseButtonMiddle, "middle"},
		{computer.MouseButtonDoubleLeft, "double_left"},
	}

	for _, tc := range testCases {
		suite.SetupTest() // Reset mock for each test

		expectedResult := &models.McpToolResult{
			Success:      true,
			RequestID:    "test-" + tc.buttonStr,
			ErrorMessage: "",
		}

		suite.mockSession.On("CallMcpTool", "click_mouse", map[string]interface{}{
			"x":      100,
			"y":      200,
			"button": tc.buttonStr,
		}).Return(expectedResult, nil)

		result := suite.computer.ClickMouse(100, 200, tc.button)

		assert.True(suite.T(), result.Success, "Button %s should be valid", tc.buttonStr)
		assert.Equal(suite.T(), "test-"+tc.buttonStr, result.RequestID)
	}
}

func (suite *ComputerTestSuite) TestScroll_AllDirections() {
	testCases := []struct {
		direction    computer.ScrollDirection
		directionStr string
	}{
		{computer.ScrollDirectionUp, "up"},
		{computer.ScrollDirectionDown, "down"},
		{computer.ScrollDirectionLeft, "left"},
		{computer.ScrollDirectionRight, "right"},
	}

	for _, tc := range testCases {
		suite.SetupTest() // Reset mock for each test

		expectedResult := &models.McpToolResult{
			Success:      true,
			RequestID:    "test-" + tc.directionStr,
			ErrorMessage: "",
		}

		suite.mockSession.On("CallMcpTool", "scroll", map[string]interface{}{
			"x":         100,
			"y":         200,
			"direction": tc.directionStr,
			"amount":    1,
		}).Return(expectedResult, nil)

		result := suite.computer.Scroll(100, 200, tc.direction, 1)

		assert.True(suite.T(), result.Success, "Direction %s should be valid", tc.directionStr)
		assert.Equal(suite.T(), "test-"+tc.directionStr, result.RequestID)
	}
}

// Run the test suite
func TestComputerTestSuite(t *testing.T) {
	suite.Run(t, new(ComputerTestSuite))
}
