package main

import (
	"fmt"
	"os"
	"time"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/ui"
)

func main() {
	// Get API key from environment variable or use a default value for testing
	apiKey := os.Getenv("AGENTBAY_API_KEY")
	if apiKey == "" {
		apiKey = "akm-xxx" // Replace with your actual API key for testing
		fmt.Println("Warning: Using default API key. Set AGENTBAY_API_KEY environment variable for production use.")
	}

	// Initialize the AgentBay client
	agentBay, err := agentbay.NewAgentBay(apiKey)
	if err != nil {
		fmt.Printf("Error initializing AgentBay client: %v\n", err)
		os.Exit(1)
	}

	// Create session parameters with ImageId set to mobile_latest for UI operations
	params := agentbay.NewCreateSessionParams().WithImageId("mobile_latest")

	// Create a new session
	fmt.Println("\nCreating a new session with mobile_latest image...")
	sessionResult, err := agentBay.Create(params)
	if err != nil {
		fmt.Printf("\nError creating session: %v\n", err)
		os.Exit(1)
	}
	session := sessionResult.Session
	fmt.Printf("\nSession created with ID: %s (RequestID: %s)\n", session.SessionID, sessionResult.RequestID)
	defer func() {
		// Clean up by deleting the session when we're done
		fmt.Println("\nDeleting the session...")
		deleteResult, err := session.Delete()
		if err != nil {
			fmt.Printf("Error deleting session: %v\n", err)
		} else {
			fmt.Printf("Session deleted successfully (RequestID: %s)\n", deleteResult.RequestID)
		}
	}()

	// 1. Take a screenshot
	fmt.Println("\n1. Taking a screenshot...")
	screenshotResult := session.Mobile.Screenshot()
	if screenshotResult.ErrorMessage != "" {
		fmt.Printf("Error taking screenshot: %s\n", screenshotResult.ErrorMessage)
	} else {
		// The screenshot operation was successful
		fmt.Printf("Screenshot taken successfully (RequestID: %s)\n", screenshotResult.RequestID)

		// Note: The screenshot data is returned in the Data field
		if screenshotResult.Data != "" {
			fmt.Printf("Screenshot data length: %d bytes\n", len(screenshotResult.Data))
		}
	}

	// 2. Get all UI elements
	fmt.Println("\n2. Getting all UI elements...")
	elementsResult := session.Mobile.GetAllUIElements(2000) // 2 second timeout
	if elementsResult.ErrorMessage != "" {
		fmt.Printf("Error getting UI elements: %s\n", elementsResult.ErrorMessage)
	} else if len(elementsResult.Elements) == 0 {
		fmt.Println("No UI elements found.")
	} else {
		fmt.Printf("Found %d UI elements (RequestID: %s)\n", len(elementsResult.Elements), elementsResult.RequestID)
		// Print details of the first few elements if available
		elementsToShow := 3
		if len(elementsResult.Elements) < elementsToShow {
			elementsToShow = len(elementsResult.Elements)
		}

		fmt.Println("\nSample of UI elements found:")
		for i := 0; i < elementsToShow; i++ {
			elem := elementsResult.Elements[i]
			fmt.Printf("Element #%d:\n", i+1)
			fmt.Printf("  Type: %v\n", elem.Type)
			fmt.Printf("  Text: %v\n", elem.Text)
			fmt.Printf("  Bounds: %v\n", elem.Bounds)
			fmt.Printf("  ResourceId: %v\n", elem.ResourceID)
			fmt.Println()
		}
	}

	// 3. Get clickable UI elements
	fmt.Println("\n3. Getting clickable UI elements...")
	clickableElementsResult := session.Mobile.GetClickableUIElements(2000) // 2 second timeout
	if clickableElementsResult.ErrorMessage != "" {
		fmt.Printf("Error getting clickable UI elements: %s\n", clickableElementsResult.ErrorMessage)
	} else if len(clickableElementsResult.Elements) == 0 {
		fmt.Println("No clickable UI elements found.")
	} else {
		fmt.Printf("Found %d clickable UI elements (RequestID: %s)\n", len(clickableElementsResult.Elements), clickableElementsResult.RequestID)
		// Print details of the first few clickable elements if available
		elementsToShow := 3
		if len(clickableElementsResult.Elements) < elementsToShow {
			elementsToShow = len(clickableElementsResult.Elements)
		}

		fmt.Println("\nSample of clickable UI elements found:")
		for i := 0; i < elementsToShow; i++ {
			elem := clickableElementsResult.Elements[i]
			fmt.Printf("Element #%d:\n", i+1)
			fmt.Printf("  Type: %v\n", elem.Type)
			fmt.Printf("  Text: %v\n", elem.Text)
			fmt.Printf("  Bounds: %v\n", elem.Bounds)
			fmt.Printf("  ResourceId: %v\n", elem.ResourceID)
			fmt.Println()
		}
	}

	// 4. Send key event (HOME key)
	fmt.Println("\n4. Sending HOME key event...")
	keyResult := session.Mobile.SendKey(int(ui.KEYCODE_HOME)) // Use KeyCode.HOME constant
	if keyResult.ErrorMessage != "" {
		fmt.Printf("Error sending HOME key: %s\n", keyResult.ErrorMessage)
	} else {
		fmt.Printf("HOME key sent successfully (RequestID: %s, Success: %v)\n", keyResult.RequestID, keyResult.Success)
	}

	// Sleep briefly to allow UI to update after HOME key
	time.Sleep(1 * time.Second)

	// 5. Input text
	fmt.Println("\n5. Inputting text...")
	inputResult := session.Mobile.InputText("Hello from AgentBay SDK!")
	if inputResult.ErrorMessage != "" {
		fmt.Printf("Error inputting text: %s\n", inputResult.ErrorMessage)
	} else {
		fmt.Printf("Text input successful (RequestID: %s, Success: %v)\n", inputResult.RequestID, inputResult.Success)
	}

	// 6. Tap a position on screen
	fmt.Println("\n6. Tapping on screen position...")
	// Coordinates for center of screen (example values)
	x := 540
	y := 960
	tapResult := session.Mobile.Tap(x, y)
	if tapResult.ErrorMessage != "" {
		fmt.Printf("Error tapping on position (%d,%d): %s\n", x, y, tapResult.ErrorMessage)
	} else {
		fmt.Printf("Successfully tapped at position (%d,%d) (RequestID: %s, Success: %v)\n", x, y, tapResult.RequestID, tapResult.Success)
	}

	// Sleep briefly to allow UI to update after tap
	time.Sleep(1 * time.Second)

	// 7. Swipe on screen
	fmt.Println("\n7. Performing swipe gesture...")
	startX := 540
	startY := 1500
	endX := 540
	endY := 500
	swipeDuration := 10000 // milliseconds
	swipeResult := session.Mobile.Swipe(startX, startY, endX, endY, swipeDuration)
	if swipeResult.ErrorMessage != "" {
		fmt.Printf("Error performing swipe from (%d,%d) to (%d,%d): %s\n",
			startX, startY, endX, endY, swipeResult.ErrorMessage)
	} else {
		fmt.Printf("Successfully swiped from (%d,%d) to (%d,%d) (RequestID: %s, Success: %v)\n",
			startX, startY, endX, endY, swipeResult.RequestID, swipeResult.Success)
	}

	// 8. Take another screenshot after interactions
	fmt.Println("\n8. Taking another screenshot after interactions...")
	screenshot2Result := session.Mobile.Screenshot()
	if screenshot2Result.ErrorMessage != "" {
		fmt.Printf("Error taking second screenshot: %s\n", screenshot2Result.ErrorMessage)
	} else {
		fmt.Printf("Second screenshot taken successfully (RequestID: %s)\n", screenshot2Result.RequestID)

		// Note: The screenshot data is returned in the Data field
		if screenshot2Result.Data != "" {
			fmt.Printf("Screenshot data length: %d bytes\n", len(screenshot2Result.Data))
		}
	}

	fmt.Println("\nUI examples completed successfully!")
}
