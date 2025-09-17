package main

import (
	"fmt"
	"log"
	"os"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

func main() {
	fmt.Println("🚀 AgentBay Network Redirection Example")
	fmt.Println("=======================================")
	fmt.Println("💡 Prevent account suspensions by routing cloud traffic through your local IP")
	fmt.Println()

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

	// Step 1: Create network for redirection
	fmt.Println("📡 Step 1: Creating network redirection setup...")
	fmt.Println("   This creates a network that will route cloud traffic through your local IP")
	result, err := agentBay.Network.CreateNetwork(nil)
	if err != nil {
		fmt.Printf("❌ Error creating network: %v\n", err)
		return
	}

	if result.Success && result.NetworkInfo != nil {
		networkID := result.NetworkInfo.NetworkID
		networkToken := result.NetworkInfo.NetworkToken

		fmt.Printf("✅ Network redirection setup created!\n")
		fmt.Printf("   Network ID: %s\n", networkID)
		fmt.Printf("   Network Token: %s (use with Rick Plugin)\n", networkToken)

		// Step 2: Local redirection setup instructions
		fmt.Println("\n🔧 Step 2: Local redirection setup...")
		fmt.Printf("   Run these commands on your local machine to start redirection:\n")
		fmt.Printf("   $ ./rick-cli -m bind -t %s\n", networkToken)
		fmt.Printf("   $ ./rick-cli\n")
		fmt.Println("   ✅ This routes all cloud session traffic through your local IP")
		fmt.Println("   📋 After starting Rick Plugin, the network status will show as Online")

		// Step 3: Query network status (after Rick Plugin setup)
		fmt.Println("\n🔍 Step 3: Querying network status (after Rick Plugin setup)...")
		fmt.Println("   Note: Network will show as Online only after Rick Plugin is running")
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
				if !*statusResult.NetworkInfo.Online {
					fmt.Println("   💡 If showing Offline, ensure Rick Plugin is running on your local machine")
				}
			} else {
				fmt.Println("   Status: ⚪ Unknown")
			}
		} else {
			fmt.Printf("❌ Query failed: %s\n", statusResult.ErrorMessage)
		}

		// Step 4: Demonstrate session creation with network redirection
		fmt.Println("\n🔗 Step 4: Creating session with network redirection (demonstration)...")
		fmt.Println("   Sessions will appear to originate from your local IP, preventing suspensions")
		fmt.Println("   Note: Requires custom image (imgc-xxxxx format) with advanced network option")

		sessionParams := agentbay.NewCreateSessionParams().
			WithImageId("imgc-12345678"). // Custom image required for network functionality
			WithNetworkId(networkID).
			WithLabels(map[string]string{
				"example": "network-redirection-demo",
				"purpose": "ip-reputation-protection",
			})

		sessionResult, err := agentBay.Create(sessionParams)
		if err != nil {
			fmt.Printf("⚠️  Expected failure with test image: %v\n", err)
			fmt.Println("   💡 In production:")
			fmt.Println("      1. Use a real custom image (imgc-xxxxx format)")
			fmt.Println("      2. Enable advanced network option when creating the image")
			fmt.Println("      3. All requests will appear to come from your local IP")
		} else {
			fmt.Printf("✅ Session created with network redirection: %s\n", sessionResult.Session.SessionID)
			fmt.Println("   🛡️  All operations in this session will use your local IP identity")

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

	fmt.Println("\n🎉 Network redirection example completed!")
	fmt.Println("💡 Key benefits: Prevent account suspensions, consistent IP identity, seamless AI operations")
}
