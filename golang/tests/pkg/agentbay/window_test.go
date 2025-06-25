package agentbay_test

import (
	"fmt"
	"testing"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
	"github.com/aliyun/wuying-agentbay-sdk/golang/tests/pkg/agentbay/testutil"
)

// Window represents a window in the system (copy of the same struct from window package)
type Window struct {
	WindowID           int      `json:"window_id"`
	Title              string   `json:"title"`
	AbsoluteUpperLeftX int      `json:"absolute_upper_left_x,omitempty"`
	AbsoluteUpperLeftY int      `json:"absolute_upper_left_y,omitempty"`
	Width              int      `json:"width,omitempty"`
	Height             int      `json:"height,omitempty"`
	PID                int      `json:"pid,omitempty"`
	PName              string   `json:"pname,omitempty"`
	ChildWindows       []Window `json:"child_windows,omitempty"`
}

func TestWindow_ListRootWindows(t *testing.T) {
	// Setup session with cleanup and ImageId set to linux_latest
	sessionParams := agentbay.NewCreateSessionParams().WithImageId("linux_latest")
	session, cleanup := testutil.SetupAndCleanup(t, sessionParams)
	defer cleanup()

	// Test ListRootWindows
	if session.Window != nil {
		fmt.Println("Listing root windows...")
		listResult, err := session.Window.ListRootWindows()
		if err != nil {
			t.Logf("Note: ListRootWindows failed: %v", err)
		} else {
			t.Logf("Found %d root windows (RequestID: %s)", len(listResult.Windows), listResult.RequestID)

			// Verify we got some windows
			if len(listResult.Windows) == 0 {
				t.Logf("Warning: No root windows found")
			} else {
				// Print the first 3 windows or fewer if less than 3 are available
				count := min(len(listResult.Windows), 3)
				for i := 0; i < count; i++ {
					t.Logf("Window %d: %s (ID: %d)", i+1, listResult.Windows[i].Title, listResult.Windows[i].WindowID)
				}

				// Verify window properties
				for _, window := range listResult.Windows {
					if window.WindowID <= 0 {
						t.Errorf("Found window with invalid ID: %d", window.WindowID)
					}
				}
			}
		}
	} else {
		t.Logf("Note: Window interface is nil, skipping window test")
	}
}

func TestWindow_GetActiveWindow(t *testing.T) {
	// Setup session with cleanup and ImageId set to linux_latest
	sessionParams := agentbay.NewCreateSessionParams().WithImageId("linux_latest")
	session, cleanup := testutil.SetupAndCleanup(t, sessionParams)
	defer cleanup()

	// Test GetActiveWindow
	if session.Window != nil {
		fmt.Println("Getting active window...")
		activeWindowResult, err := session.Window.GetActiveWindow()
		if err != nil {
			t.Logf("Note: GetActiveWindow failed: %v", err)
		} else {
			t.Logf("Active window (RequestID: %s):", activeWindowResult.RequestID)
			t.Logf("Active window: %s (ID: %d, Process: %s, PID: %d)",
				activeWindowResult.Window.Title,
				activeWindowResult.Window.WindowID,
				activeWindowResult.Window.PName,
				activeWindowResult.Window.PID)

			// Verify window properties
			if activeWindowResult.Window.WindowID <= 0 {
				t.Errorf("Active window has invalid ID: %d", activeWindowResult.Window.WindowID)
			}
			if activeWindowResult.Window.PID <= 0 {
				t.Logf("Active window has PID: %d", activeWindowResult.Window.PID)
			}
		}
	} else {
		t.Logf("Note: Window interface is nil, skipping window test")
	}
}

func TestWindow_FocusMode(t *testing.T) {
	// Setup session with cleanup and ImageId set to linux_latest
	sessionParams := agentbay.NewCreateSessionParams().WithImageId("linux_latest")
	session, cleanup := testutil.SetupAndCleanup(t, sessionParams)
	defer cleanup()

	// Test FocusMode
	if session.Window != nil {
		// Enable focus mode
		fmt.Println("Enabling focus mode...")
		enableResult, err := session.Window.FocusMode(true)
		if err != nil {
			t.Logf("Note: FocusMode(true) failed: %v", err)
		} else {
			t.Logf("Focus mode enabled successfully (RequestID: %s)", enableResult.RequestID)
		}

		// Wait a short time
		fmt.Println("Waiting briefly...")
		testutil.SleepWithMessage(2, "Focus mode is active...")

		// Disable focus mode
		fmt.Println("Disabling focus mode...")
		disableResult, err := session.Window.FocusMode(false)
		if err != nil {
			t.Logf("Note: FocusMode(false) failed: %v", err)
		} else {
			t.Logf("Focus mode disabled successfully (RequestID: %s)", disableResult.RequestID)
		}
	} else {
		t.Logf("Note: Window interface is nil, skipping focus mode test")
	}
}
