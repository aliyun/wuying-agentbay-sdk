package main

import (
	"fmt"
	"os"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/models"
)

// This example demonstrates how to create, list, and delete sessions
// using the Wuying AgentBay SDK.

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

	// Create a new session with default parameters
	fmt.Println("\n1. Creating a new session with default parameters...")
	sessionResult, err := agentBay.Create(nil)
	if err != nil {
		fmt.Printf("\nError creating session: %v\n", err)
		os.Exit(1)
	}
	session := sessionResult.Session
	fmt.Printf("Session created with ID: %s (RequestID: %s)\n", session.SessionID, sessionResult.RequestID)

	// Create mobile sessions with different configurations
	fmt.Println("\n2. Creating mobile sessions with various configurations...")

	// Define different mobile configurations
	mobileConfigs := []struct {
		name        string
		description string
		config      *models.MobileExtraConfig
		labels      map[string]string
	}{
		{
			name:        "Whitelist Configuration",
			description: "Secure whitelist with immersive UI and system protection",
			config: &models.MobileExtraConfig{
				LockResolution:     true,
				HideNavigationBar:  true,
				UninstallBlacklist: []string{"com.android.systemui", "com.android.settings", "com.google.android.gms"},
				AppManagerRule: &models.AppManagerRule{
					RuleType: "White",
					AppPackageNameList: []string{
						"com.android.settings",
						"com.example.test.app",
						"com.trusted.service",
					},
				},
			},
			labels: map[string]string{
				"project":     "mobile-testing",
				"config_type": "whitelist",
				"environment": "development",
				"features":    "navbar_hidden,uninstall_protected,app_whitelist",
			},
		},
		{
			name:        "Blacklist Configuration",
			description: "Flexible blacklist with visible navigation and basic protection",
			config: &models.MobileExtraConfig{
				LockResolution:     false,
				HideNavigationBar:  false,
				UninstallBlacklist: []string{"com.android.systemui", "com.android.settings"},
				AppManagerRule: &models.AppManagerRule{
					RuleType: "Black",
					AppPackageNameList: []string{
						"com.malware.suspicious",
						"com.unwanted.adware",
						"com.blocked.app",
					},
				},
			},
			labels: map[string]string{
				"project":     "mobile-security",
				"config_type": "blacklist",
				"environment": "production",
				"features":    "app_blacklist,basic_protection",
			},
		},
	}

	// Create sessions with different configurations
	var mobileSessions []*agentbay.Session
	for i, config := range mobileConfigs {
		fmt.Printf("\n2.%d. Creating %s...\n", i+1, config.name)

		extraConfigs := &models.ExtraConfigs{
			Mobile: config.config,
		}

		params := agentbay.NewCreateSessionParams().
			WithImageId("mobile_latest").
			WithLabels(config.labels).
			WithExtraConfigs(extraConfigs)

		result, err := agentBay.Create(params)
		if err != nil {
			fmt.Printf("Error creating %s: %v\n", config.name, err)
			continue
		}

		session := result.Session
		fmt.Printf("%s created with ID: %s (RequestID: %s)\n",
			config.name, session.SessionID, result.RequestID)
		fmt.Printf("Description: %s\n", config.description)

		// Display configuration details
		fmt.Println("Configuration applied:")
		fmt.Printf("- Resolution locked: %t\n", config.config.LockResolution)
		fmt.Printf("- Navigation bar hidden: %t\n", config.config.HideNavigationBar)
		fmt.Printf("- Protected apps: %d\n", len(config.config.UninstallBlacklist))
		if config.config.AppManagerRule != nil {
			fmt.Printf("- App rule type: %s (%d apps)\n",
				config.config.AppManagerRule.RuleType,
				len(config.config.AppManagerRule.AppPackageNameList))
		}

		mobileSessions = append(mobileSessions, session)
	}

	// Clean up mobile sessions
	defer func() {
		fmt.Println("\nCleaning up mobile sessions...")
		for i, session := range mobileSessions {
			if deleteResult, err := session.Delete(); err != nil {
				fmt.Printf("Error deleting mobile session %d: %v\n", i+1, err)
			} else {
				fmt.Printf("Mobile session %d deleted (RequestID: %s)\n", i+1, deleteResult.RequestID)
			}
		}
	}()

	// Create multiple sessions to demonstrate listing
	fmt.Println("\n3. Creating additional sessions for demonstration...")
	var additionalSessions []*agentbay.Session
	for i := 0; i < 2; i++ {
		additionalSessionResult, err := agentBay.Create(nil)
		if err != nil {
			fmt.Printf("\nError creating additional session: %v\n", err)
			continue
		}
		additionalSession := additionalSessionResult.Session
		fmt.Printf("Additional session %d created with ID: %s (RequestID: %s)\n", i+1, additionalSession.SessionID, additionalSessionResult.RequestID)

		// Store the session for later cleanup
		additionalSessions = append(additionalSessions, additionalSession)
	}

	// Clean up all sessions
	fmt.Println("\n4. Cleaning up sessions...")
	// First delete the initial session
	deleteResult, err := session.Delete()
	if err != nil {
		fmt.Printf("Error deleting session %s: %v\n", session.SessionID, err)
	} else {
		fmt.Printf("Session %s deleted successfully (RequestID: %s)\n", session.SessionID, deleteResult.RequestID)
	}

	// Then delete the additional sessions
	for _, s := range additionalSessions {
		deleteResult, err := s.Delete()
		if err != nil {
			fmt.Printf("Error deleting session %s: %v\n", s.SessionID, err)
		} else {
			fmt.Printf("Session %s deleted successfully (RequestID: %s)\n", s.SessionID, deleteResult.RequestID)
		}
	}

	fmt.Println("All sessions cleanup completed.")
}
