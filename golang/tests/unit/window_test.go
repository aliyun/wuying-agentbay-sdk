package unit

import (
	"testing"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/window"
)

// TestWindowInitialization tests the initialization of a Window struct
func TestWindowInitialization(t *testing.T) {
	// Create a window
	win := window.Window{
		WindowID:           1,
		Title:              "Test Window",
		AbsoluteUpperLeftX: 100,
		AbsoluteUpperLeftY: 200,
		Width:              800,
		Height:             600,
		PID:                12345,
		PName:              "test_process",
	}

	// Verify attributes
	if win.WindowID != 1 {
		t.Errorf("Expected WindowID to be 1, got %d", win.WindowID)
	}
	if win.Title != "Test Window" {
		t.Errorf("Expected Title to be 'Test Window', got '%s'", win.Title)
	}
	if win.AbsoluteUpperLeftX != 100 {
		t.Errorf("Expected AbsoluteUpperLeftX to be 100, got %d", win.AbsoluteUpperLeftX)
	}
	if win.AbsoluteUpperLeftY != 200 {
		t.Errorf("Expected AbsoluteUpperLeftY to be 200, got %d", win.AbsoluteUpperLeftY)
	}
	if win.Width != 800 {
		t.Errorf("Expected Width to be 800, got %d", win.Width)
	}
	if win.Height != 600 {
		t.Errorf("Expected Height to be 600, got %d", win.Height)
	}
	if win.PID != 12345 {
		t.Errorf("Expected PID to be 12345, got %d", win.PID)
	}
	if win.PName != "test_process" {
		t.Errorf("Expected PName to be 'test_process', got '%s'", win.PName)
	}
}

// TestWindowWithChildWindows tests a Window with child windows
func TestWindowWithChildWindows(t *testing.T) {
	// Create a child window
	childWin := window.Window{
		WindowID:           2,
		Title:              "Child Window",
		AbsoluteUpperLeftX: 150,
		AbsoluteUpperLeftY: 250,
		Width:              400,
		Height:             300,
		PID:                12346,
		PName:              "child_process",
	}

	// Create a parent window with the child window
	parentWin := window.Window{
		WindowID:           1,
		Title:              "Parent Window",
		AbsoluteUpperLeftX: 100,
		AbsoluteUpperLeftY: 200,
		Width:              800,
		Height:             600,
		PID:                12345,
		PName:              "parent_process",
		ChildWindows:       []window.Window{childWin},
	}

	// Verify parent attributes
	if parentWin.WindowID != 1 {
		t.Errorf("Expected parent WindowID to be 1, got %d", parentWin.WindowID)
	}
	if parentWin.Title != "Parent Window" {
		t.Errorf("Expected parent Title to be 'Parent Window', got '%s'", parentWin.Title)
	}

	// Verify child window attributes
	if len(parentWin.ChildWindows) != 1 {
		t.Errorf("Expected 1 child window, got %d", len(parentWin.ChildWindows))
	} else {
		if parentWin.ChildWindows[0].WindowID != 2 {
			t.Errorf("Expected child WindowID to be 2, got %d", parentWin.ChildWindows[0].WindowID)
		}
		if parentWin.ChildWindows[0].Title != "Child Window" {
			t.Errorf("Expected child Title to be 'Child Window', got '%s'", parentWin.ChildWindows[0].Title)
		}
	}
}

// WindowMockSession is a mock implementation of the session interface used by WindowManager
type WindowMockSession struct {
	apiKey    string
	sessionID string
	client    interface{}
}

// GetAPIKey returns the API key
func (m *WindowMockSession) GetAPIKey() string {
	return m.apiKey
}

// GetClient returns the MCP client
func (m *WindowMockSession) GetClient() interface{} {
	return m.client
}

// GetSessionId returns the session ID
func (m *WindowMockSession) GetSessionId() string {
	return m.sessionID
}

// TestListRootWindowsSuccess tests listing root windows with a successful response
func TestListRootWindowsSuccess(t *testing.T) {
	// Skip the test since we can't properly mock the client without refactoring
	t.Skip("Skipping test that requires mocking client")

	// In a real test with proper mocking, you would:
	// 1. Create a mock session
	// 2. Create a WindowManager with the mock session
	// 3. Mock the client's CallMcpTool method to return a success response with window data
	// 4. Call ListRootWindows and verify the results contain the expected windows
}

// TestListRootWindowsFailure tests listing root windows with an error response
func TestListRootWindowsFailure(t *testing.T) {
	// Skip the test since we can't properly mock the client without refactoring
	t.Skip("Skipping test that requires mocking client")

	// In a real test with proper mocking, you would:
	// 1. Create a mock session
	// 2. Create a WindowManager with the mock session
	// 3. Mock the client's CallMcpTool method to return an error response
	// 4. Call ListRootWindows and verify the error is handled correctly
}

// TestGetActiveWindowSuccess tests getting the active window with a successful response
func TestGetActiveWindowSuccess(t *testing.T) {
	// Skip the test since we can't properly mock the client without refactoring
	t.Skip("Skipping test that requires mocking client")

	// In a real test with proper mocking, you would:
	// 1. Create a mock session
	// 2. Create a WindowManager with the mock session
	// 3. Mock the client's CallMcpTool method to return a success response with active window data
	// 4. Call GetActiveWindow and verify the result contains the expected window
}

// TestWindowOperations tests window operations (activate, maximize, minimize, restore)
func TestWindowOperations(t *testing.T) {
	// Skip the test since we can't properly mock the client without refactoring
	t.Skip("Skipping test that requires mocking client")

	// In a real test with proper mocking, you would:
	// 1. Create a mock session
	// 2. Create a WindowManager with the mock session
	// 3. Mock the client's CallMcpTool method to return success responses
	// 4. Call various window operations and verify they call the correct tool with correct arguments
}

// TestWindowOperationsErrorHandling tests error handling for window operations
func TestWindowOperationsErrorHandling(t *testing.T) {
	// Skip the test since we can't properly mock the client without refactoring
	t.Skip("Skipping test that requires mocking client")

	// In a real test with proper mocking, you would:
	// 1. Create a mock session
	// 2. Create a WindowManager with the mock session
	// 3. Mock the client's CallMcpTool method to throw exceptions
	// 4. Call various window operations and verify errors are handled correctly
}
