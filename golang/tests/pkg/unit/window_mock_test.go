package agentbay_test

import (
	"testing"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/window"
	"github.com/aliyun/wuying-agentbay-sdk/golang/tests/pkg/unit/mock"
	"github.com/golang/mock/gomock"
	"github.com/stretchr/testify/assert"
)

func TestWindowManager_ListRootWindows_WithMockClient(t *testing.T) {
	ctrl := gomock.NewController(t)
	defer ctrl.Finish()

	// Create mock Window
	mockWindow := mock.NewMockWindowInterface(ctrl)

	// Set expected behavior
	expectedResult := &window.WindowListResult{
		Windows: []window.Window{
			{WindowID: 1, Title: "Window 1"},
			{WindowID: 2, Title: "Window 2"},
		},
	}
	mockWindow.EXPECT().ListRootWindows().Return(expectedResult, nil)

	// Test ListRootWindows method call
	result, err := mockWindow.ListRootWindows()

	// Verify call success
	assert.NoError(t, err)
	assert.NotNil(t, result)
	assert.Len(t, result.Windows, 2)
	assert.Equal(t, "Window 1", result.Windows[0].Title)
	assert.Equal(t, "Window 2", result.Windows[1].Title)
}

func TestWindowManager_GetActiveWindow_WithMockClient(t *testing.T) {
	ctrl := gomock.NewController(t)
	defer ctrl.Finish()

	// Create mock Window
	mockWindow := mock.NewMockWindowInterface(ctrl)

	// Set expected behavior
	expectedResult := &window.WindowDetailResult{
		Window: &window.Window{
			WindowID: 3,
			Title:    "Active Window",
			PID:      12345,
		},
	}
	mockWindow.EXPECT().GetActiveWindow().Return(expectedResult, nil)

	// Test GetActiveWindow method call
	result, err := mockWindow.GetActiveWindow()

	// Verify call success
	assert.NoError(t, err)
	assert.NotNil(t, result)
	assert.NotNil(t, result.Window)
	assert.Equal(t, 3, result.Window.WindowID)
	assert.Equal(t, "Active Window", result.Window.Title)
	assert.Equal(t, 12345, result.Window.PID)
}

func TestWindowManager_ActivateWindow_WithMockClient(t *testing.T) {
	ctrl := gomock.NewController(t)
	defer ctrl.Finish()

	// Create mock Window
	mockWindow := mock.NewMockWindowInterface(ctrl)

	// Set expected behavior
	expectedResult := &window.WindowResult{Success: true}
	mockWindow.EXPECT().ActivateWindow(1).Return(expectedResult, nil)

	// Test ActivateWindow method call
	result, err := mockWindow.ActivateWindow(1)

	// Verify call success
	assert.NoError(t, err)
	assert.NotNil(t, result)
	assert.True(t, result.Success)
}

func TestWindowManager_MaximizeWindow_WithMockClient(t *testing.T) {
	ctrl := gomock.NewController(t)
	defer ctrl.Finish()

	// Create mock Window
	mockWindow := mock.NewMockWindowInterface(ctrl)

	// Set expected behavior
	expectedResult := &window.WindowResult{Success: true}
	mockWindow.EXPECT().MaximizeWindow(1).Return(expectedResult, nil)

	// Test MaximizeWindow method call
	result, err := mockWindow.MaximizeWindow(1)

	// Verify call success
	assert.NoError(t, err)
	assert.NotNil(t, result)
	assert.True(t, result.Success)
}

func TestWindowManager_MinimizeWindow_WithMockClient(t *testing.T) {
	ctrl := gomock.NewController(t)
	defer ctrl.Finish()

	// Create mock Window
	mockWindow := mock.NewMockWindowInterface(ctrl)

	// Set expected behavior
	expectedResult := &window.WindowResult{Success: true}
	mockWindow.EXPECT().MinimizeWindow(1).Return(expectedResult, nil)

	// Test MinimizeWindow method call
	result, err := mockWindow.MinimizeWindow(1)

	// Verify call success
	assert.NoError(t, err)
	assert.NotNil(t, result)
	assert.True(t, result.Success)
}

func TestWindowManager_RestoreWindow_WithMockClient(t *testing.T) {
	ctrl := gomock.NewController(t)
	defer ctrl.Finish()

	// Create mock Window
	mockWindow := mock.NewMockWindowInterface(ctrl)

	// Set expected behavior
	expectedResult := &window.WindowResult{Success: true}
	mockWindow.EXPECT().RestoreWindow(1).Return(expectedResult, nil)

	// Test RestoreWindow method call
	result, err := mockWindow.RestoreWindow(1)

	// Verify call success
	assert.NoError(t, err)
	assert.NotNil(t, result)
	assert.True(t, result.Success)
}

func TestWindowManager_Error_WithMockClient(t *testing.T) {
	ctrl := gomock.NewController(t)
	defer ctrl.Finish()

	// Create mock Window
	mockWindow := mock.NewMockWindowInterface(ctrl)

	// Set expected behavior - return error
	mockWindow.EXPECT().ListRootWindows().Return(nil, assert.AnError)

	// Test error case
	result, err := mockWindow.ListRootWindows()

	// Verify error handling
	assert.Error(t, err)
	assert.Nil(t, result)
}
