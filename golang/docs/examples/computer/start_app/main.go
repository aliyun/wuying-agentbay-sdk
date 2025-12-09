package main

import (
	"fmt"
	"os"
	"time"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

func main() {
	apiKey := os.Getenv("AGENTBAY_API_KEY")
	if apiKey == "" {
		fmt.Println("AGENTBAY_API_KEY is not set")
		return
	}

	client, err := agentbay.NewAgentBay(apiKey, nil)
	if err != nil {
		panic(err)
	}

	// Create a session
	fmt.Println("Creating session...")
	params := agentbay.NewCreateSessionParams().WithImageId("windows_latest")
	result, err := client.Create(params)
	if err != nil {
		panic(err)
	}
	defer func() {
		fmt.Println("Deleting session...")
		result.Session.Delete()
	}()

	fmt.Println("Session created:", result.Session.GetSessionId())

	// Start Notepad
	fmt.Println("Starting Notepad...")
	startResult, err := result.Session.Computer.StartApp("notepad.exe", "", "")
	if err != nil {
		fmt.Printf("Failed to start app: %v\n", err)
		return
	}

	fmt.Printf("Started processes: %d\n", len(startResult.Processes))
	for _, p := range startResult.Processes {
		fmt.Printf("- PID: %d, Name: %s\n", p.PID, p.PName)
	}

	// Wait a bit for window to appear
	time.Sleep(5 * time.Second)

	// Check if we can see the window
	windows, err := result.Session.Computer.ListRootWindows()
	if err != nil {
		fmt.Printf("Failed to list windows: %v\n", err)
	} else {
		found := false
		fmt.Println("Visible windows:")
		for _, w := range windows.Windows {
			if w.Title != "" {
				fmt.Printf("- %s\n", w.Title)
				if w.Title == "Untitled - Notepad" || w.PName == "notepad.exe" {
					found = true
				}
			}
		}
		if found {
			fmt.Println("Notepad window verified!")
		} else {
			fmt.Println("Warning: Notepad window not found in list")
		}
	}
}
