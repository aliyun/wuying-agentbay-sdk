package main

import (
	"fmt"
	"log"
	"os"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

func main() {
	fmt.Println("🚀 AgentBay Network Management Example")
	fmt.Println("=====================================")

	// Initialize AgentBay client
	apiKey := os.Getenv("AGENTBAY_API_KEY")
	if apiKey == "" {
		fmt.Println("❌ Error: AGENTBAY_API_KEY environment variable is not set")
		fmt.Println("Please set your API key: export AGENTBAY_API_KEY=your_api_key_here")
		os.Exit(1)
	}

	agentBay, err := agentbay.NewAgentBay(apiKey)
	if err != nil {
		log.Fatalf("Failed to create AgentBay client: %v", err)
	}

	// Step 1: Create network
	fmt.Println("\n📡 Step 1: Creating network...")
	result, err := agentBay.Network.CreateNetwork(nil)
	if err != nil {
		fmt.Printf("❌ Error creating network: %v\n", err)
		return
	}

	if result.Success && result.NetworkInfo != nil {
		networkID := result.NetworkInfo.NetworkID
		networkToken := result.NetworkInfo.NetworkToken

		fmt.Printf("✅ Network created successfully!\n")
		fmt.Printf("   Network ID: %s\n", networkID)
		fmt.Printf("   Network Token: %s\n", networkToken)

		// Step 2: Query network status
		fmt.Println("\n🔍 Step 2: Querying network status...")
		statusResult, err := agentBay.Network.DescribeNetwork(networkID)
		if err != nil {
			fmt.Printf("❌ Error querying network: %v\n", err)
			return
		}

		if statusResult.Success && statusResult.NetworkInfo != nil {
			fmt.Printf("✅ Network status retrieved successfully!\n")
			if statusResult.NetworkInfo.Online != nil {
				status := map[bool]string{true: "🟢 Online", false: "🔴 Offline"}[*statusResult.NetworkInfo.Online]
				fmt.Printf("   Status: %s\n", status)
			} else {
				fmt.Println("   Status: ⚪ Unknown")
			}
		} else {
			fmt.Printf("❌ Query failed: %s\n", statusResult.ErrorMessage)
		}

		// Step 3: Demonstrate session creation with network (optional)
		fmt.Println("\n🔗 Step 3: Creating session with network (demonstration)...")
		fmt.Println("   Note: This requires a custom image (imgc-xxxxx format)")

		sessionParams := agentbay.NewCreateSessionParams().
			WithImageId("imgc-12345678"). // Custom image required for network functionality
			WithNetworkId(networkID).
			WithLabels(map[string]string{
				"example": "network-demo",
				"network": "enabled",
			})

		sessionResult, err := agentBay.Create(sessionParams)
		if err != nil {
			fmt.Printf("⚠️  Expected failure with standard image: %v\n", err)
			fmt.Println("   💡 To use network functionality:")
			fmt.Println("      1. Use a custom image (imgc-xxxxx format)")
			fmt.Println("      2. Enable advanced network option when creating the image")
		} else {
			fmt.Printf("✅ Session created with network: %s\n", sessionResult.Session.SessionID)

			// Clean up session
			fmt.Println("\n🧹 Cleaning up session...")
			_, deleteErr := agentBay.Delete(sessionResult.Session)
			if deleteErr != nil {
				fmt.Printf("⚠️  Warning: Failed to delete session: %v\n", deleteErr)
			} else {
				fmt.Println("✅ Session cleaned up successfully")
			}
		}

	} else {
		fmt.Printf("❌ Network creation failed: %s\n", result.ErrorMessage)
	}

	fmt.Println("\n🎉 Network management example completed!")
}
