package integration

import (
	"os"
	"path/filepath"
	"strings"
	"testing"
	"time"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/models"
)

const (
	MobileInfoModelA = "SM-A505F"
	MobileInfoModelB = "moto g stylus 5G - 2024"
)

func getInsecureClient(t *testing.T, apiKey string) *agentbay.AgentBay {
	client, err := agentbay.NewAgentBay(apiKey)
	if err != nil {
		t.Fatalf("Failed to create AgentBay client: %v", err)
	}
	return client
}

// TestMobileSimulateForModelAIntegration test mobile simulate feature by model_a prop file
// and check product model is "SM-A505F" after session created
func TestMobileSimulateForModelAIntegration(t *testing.T) {
	if testing.Short() {
		t.Skip("Skipping integration test in short mode")
	}

	apiKey := os.Getenv("AGENTBAY_API_KEY")
	if apiKey == "" {
		t.Skip("AGENTBAY_API_KEY not set, skipping integration test")
	}

	client := getInsecureClient(t, apiKey)

	t.Log("Upload mobile dev info file for model A...")
	// Assuming the test is running from golang/tests/pkg/integration
	mobileInfoFilePath := filepath.Join("..", "..", "..", "..", "resource", "mobile_info_model_a.json")
	mobileInfoContent, err := os.ReadFile(mobileInfoFilePath)
	if err != nil {
		// Try alternative path if running from root
		mobileInfoFilePath = filepath.Join("resource", "mobile_info_model_a.json")
		mobileInfoContent, err = os.ReadFile(mobileInfoFilePath)
		if err != nil {
			t.Fatalf("Failed to read mobile info file: %v", err)
		}
	}

	// Create mobile simulate service and set simulate params
	t.Log("Creating mobile simulate service and set simulate params...")
	simulateService, err := agentbay.NewMobileSimulateService(client)
	if err != nil {
		t.Fatalf("Failed to create mobile simulate service: %v", err)
	}
	simulateService.SetSimulateEnable(true)
	simulateService.SetSimulateMode(models.MobileSimulateModePropertiesOnly)

	uploadResult := simulateService.UploadMobileInfo(string(mobileInfoContent), nil)
	if !uploadResult.Success {
		t.Fatalf("Failed to upload mobile dev info file: %s", uploadResult.ErrorMessage)
	}
	if uploadResult.MobileSimulateContextID == "" {
		t.Fatal("Expected non-empty MobileSimulateContextID")
	}
	mobileSimContextID := uploadResult.MobileSimulateContextID
	t.Logf("Mobile dev info uploaded successfully: %s", mobileSimContextID)

	params := agentbay.NewCreateSessionParams().
		WithImageId("mobile_latest").
		WithExtraConfigs(&models.ExtraConfigs{
			Mobile: &models.MobileExtraConfig{
				SimulateConfig: simulateService.GetSimulateConfig(),
			},
		})

	result, err := client.Create(params)
	if err != nil {
		t.Fatalf("Failed to create session: %v", err)
	}
	if !result.Success {
		t.Fatal("Create session returned Success=false")
	}
	if result.Session == nil {
		t.Fatal("Session is nil")
	}
	session := result.Session
	t.Logf("Session created successfully: %s", session.GetSessionId())

	defer func() {
		t.Log("Deleting session...")
		deleteResult, err := client.Delete(session)
		if err != nil {
			t.Errorf("Failed to delete session: %v", err)
		}
		if deleteResult != nil && deleteResult.Success {
			t.Logf("Session deleted successfully (RequestID: %s)", deleteResult.RequestID)
		}
	}()

	time.Sleep(5 * time.Second)
	t.Log("Getting device model after mobile simulate for model A...")
	cmdResult, err := session.GetCommand().ExecuteCommand("getprop ro.product.model")
	if err != nil {
		t.Fatalf("Failed to execute command: %v", err)
	}
	if cmdResult == nil {
		t.Fatal("Command result is nil")
	}

	modelAProductModel := strings.TrimSpace(cmdResult.Output)
	t.Logf("Simulated model A mobile product model: %s", modelAProductModel)
	if modelAProductModel != MobileInfoModelA {
		t.Errorf("Expected device model %s, got %s", MobileInfoModelA, modelAProductModel)
	}
}

// TestMobileSimulateForModelAIntegration test mobile simulate feature by model_b prop file
// and check product model is "moto g stylus 5G - 2024" after session created
func TestMobileSimulateForModelBIntegration(t *testing.T) {
	if testing.Short() {
		t.Skip("Skipping integration test in short mode")
	}

	apiKey := os.Getenv("AGENTBAY_API_KEY")
	if apiKey == "" {
		t.Skip("AGENTBAY_API_KEY not set, skipping integration test")
	}

	client := getInsecureClient(t, apiKey)

	t.Log("Upload mobile dev info file for model B...")
	mobileInfoFilePath := filepath.Join("..", "..", "..", "..", "resource", "mobile_info_model_b.json")
	mobileInfoContent, err := os.ReadFile(mobileInfoFilePath)
	if err != nil {
		// Try alternative path if running from root
		mobileInfoFilePath = filepath.Join("resource", "mobile_info_model_b.json")
		mobileInfoContent, err = os.ReadFile(mobileInfoFilePath)
		if err != nil {
			t.Fatalf("Failed to read mobile info file: %v", err)
		}
	}

	// Create mobile simulate service and set simulate params
	t.Log("Creating mobile simulate service and set simulate params...")
	simulateService, err := agentbay.NewMobileSimulateService(client)
	if err != nil {
		t.Fatalf("Failed to create mobile simulate service: %v", err)
	}
	simulateService.SetSimulateEnable(true)
	simulateService.SetSimulateMode(models.MobileSimulateModePropertiesOnly)

	uploadResult := simulateService.UploadMobileInfo(string(mobileInfoContent), nil)
	if !uploadResult.Success {
		t.Fatalf("Failed to upload mobile dev info file: %s", uploadResult.ErrorMessage)
	}
	if uploadResult.MobileSimulateContextID == "" {
		t.Fatal("Expected non-empty MobileSimulateContextID")
	}
	mobileSimContextID := uploadResult.MobileSimulateContextID
	t.Logf("Mobile dev info uploaded successfully: %s", mobileSimContextID)

	params := agentbay.NewCreateSessionParams().
		WithImageId("mobile_latest").
		WithExtraConfigs(&models.ExtraConfigs{
			Mobile: &models.MobileExtraConfig{
				SimulateConfig: simulateService.GetSimulateConfig(),
			},
		})

	result, err := client.Create(params)
	if err != nil {
		t.Fatalf("Failed to create session: %v", err)
	}
	if !result.Success {
		t.Fatal("Create session returned Success=false")
	}
	if result.Session == nil {
		t.Fatal("Session is nil")
	}
	session := result.Session
	t.Logf("Session created successfully: %s", session.GetSessionId())

	defer func() {
		t.Log("Deleting session...")
		deleteResult, err := client.Delete(session)
		if err != nil {
			t.Errorf("Failed to delete session: %v", err)
		}
		if deleteResult != nil && deleteResult.Success {
			t.Logf("Session deleted successfully (RequestID: %s)", deleteResult.RequestID)
		}
	}()

	time.Sleep(5 * time.Second)
	t.Log("Getting device model after mobile simulate for model B...")
	cmdResult, err := session.GetCommand().ExecuteCommand("getprop ro.product.model")
	if err != nil {
		t.Fatalf("Failed to execute command: %v", err)
	}
	if cmdResult == nil {
		t.Fatal("Command result is nil")
	}

	modelBProductModel := strings.TrimSpace(cmdResult.Output)
	t.Logf("Simulated model B mobile product model: %s", modelBProductModel)
	if modelBProductModel != MobileInfoModelB {
		t.Errorf("Expected device model %s, got %s", MobileInfoModelB, modelBProductModel)
	}
}

// TestMobileSimulateForModelAIntegration test mobile simulate persistence feature
// by using a exist mobile simulate context id, and check product model is
// "SM-A505F" after session created
func TestMobileSimulatePersistenceIntegration(t *testing.T) {
	if testing.Short() {
		t.Skip("Skipping integration test in short mode")
	}

	apiKey := os.Getenv("AGENTBAY_API_KEY")
	if apiKey == "" {
		t.Skip("AGENTBAY_API_KEY not set, skipping integration test")
	}

	client := getInsecureClient(t, apiKey)

	// In Session 1
	t.Log("Upload mobile dev info file for model A...")
	// Assuming the test is running from golang/tests/pkg/integration
	mobileInfoFilePath := filepath.Join("..", "..", "..", "..", "resource", "mobile_info_model_a.json")
	mobileInfoContent, err := os.ReadFile(mobileInfoFilePath)
	if err != nil {
		// Try alternative path if running from root
		mobileInfoFilePath = filepath.Join("resource", "mobile_info_model_a.json")
		mobileInfoContent, err = os.ReadFile(mobileInfoFilePath)
		if err != nil {
			t.Fatalf("Failed to read mobile info file: %v", err)
		}
	}

	// Create mobile simulate service and set simulate params
	t.Log("Creating mobile simulate service and set simulate params...")
	simulateService1, err := agentbay.NewMobileSimulateService(client)
	if err != nil {
		t.Fatalf("Failed to create mobile simulate service: %v", err)
	}
	simulateService1.SetSimulateEnable(true)
	simulateService1.SetSimulateMode(models.MobileSimulateModePropertiesOnly)

	uploadResult := simulateService1.UploadMobileInfo(string(mobileInfoContent), nil)
	if !uploadResult.Success {
		t.Fatalf("Failed to upload mobile dev info file: %s", uploadResult.ErrorMessage)
	}
	if uploadResult.MobileSimulateContextID == "" {
		t.Fatal("Expected non-empty MobileSimulateContextID")
	}
	mobileSimContextID := uploadResult.MobileSimulateContextID
	t.Logf("Mobile dev info uploaded successfully: %s", mobileSimContextID)

	params1 := agentbay.NewCreateSessionParams().
		WithImageId("mobile_latest").
		WithExtraConfigs(&models.ExtraConfigs{
			Mobile: &models.MobileExtraConfig{
				SimulateConfig: simulateService1.GetSimulateConfig(),
			},
		})

	result, err := client.Create(params1)
	if err != nil {
		t.Fatalf("Failed to create session: %v", err)
	}
	if !result.Success {
		t.Fatal("Create session returned Success=false")
	}
	if result.Session == nil {
		t.Fatal("Session is nil")
	}
	session1 := result.Session
	t.Logf("Session 1 created successfully: %s", session1.GetSessionId())

	defer func() {
		t.Log("Deleting session 1...")
		deleteResult, err := client.Delete(session1)
		if err != nil {
			t.Errorf("Failed to delete session: %v", err)
		}
		if deleteResult != nil && deleteResult.Success {
			t.Logf("Session 1 deleted successfully (RequestID: %s)", deleteResult.RequestID)
		}
	}()

	time.Sleep(5 * time.Second)
	t.Log("Getting device model after mobile simulate for model A...")
	cmdResult, err := session1.GetCommand().ExecuteCommand("getprop ro.product.model")
	if err != nil {
		t.Fatalf("Failed to execute command: %v", err)
	}
	if cmdResult == nil {
		t.Fatal("Command result is nil")
	}

	modelAProductModel := strings.TrimSpace(cmdResult.Output)
	t.Logf("Simulated model A mobile product model: %s", modelAProductModel)
	if modelAProductModel != MobileInfoModelA {
		t.Errorf("Expected device model %s, got %s", MobileInfoModelA, modelAProductModel)
	}

	// In Session 2
	t.Logf("Using a persistent mobild simulate context id: %s", mobileSimContextID)

	// Create mobile simulate service and set simulate params
	t.Log("Creating mobile simulate service and set simulate params...")
	simulateService2, err := agentbay.NewMobileSimulateService(client)
	if err != nil {
		t.Fatalf("Failed to create mobile simulate service: %v", err)
	}
	simulateService2.SetSimulateEnable(true)
	simulateService2.SetSimulateMode(models.MobileSimulateModePropertiesOnly)
	simulateService2.SetSimulateContextID(mobileSimContextID)

	params2 := agentbay.NewCreateSessionParams().
		WithImageId("mobile_latest").
		WithExtraConfigs(&models.ExtraConfigs{
			Mobile: &models.MobileExtraConfig{
				SimulateConfig: simulateService2.GetSimulateConfig(),
			},
		})

	result2, err := client.Create(params2)
	if err != nil {
		t.Fatalf("Failed to create session: %v", err)
	}
	if !result2.Success {
		t.Fatal("Create session returned Success=false")
	}
	if result2.Session == nil {
		t.Fatal("Session is nil")
	}
	session2 := result2.Session
	t.Logf("Session 2 created successfully: %s", session2.GetSessionId())

	defer func() {
		t.Log("Deleting session 2...")
		deleteResult, err := client.Delete(session2)
		if err != nil {
			t.Errorf("Failed to delete session: %v", err)
		}
		if deleteResult != nil && deleteResult.Success {
			t.Logf("Session 2 deleted successfully (RequestID: %s)", deleteResult.RequestID)
		}
	}()

	time.Sleep(5 * time.Second)
	t.Log("Getting device model after mobile simulate with user context...")
	cmdResult2, err := session2.GetCommand().ExecuteCommand("getprop ro.product.model")
	if err != nil {
		t.Fatalf("Failed to execute command: %v", err)
	}
	if cmdResult2 == nil {
		t.Fatal("Command result is nil")
	}

	productModel2 := strings.TrimSpace(cmdResult2.Output)
	t.Logf("Persistence simulated mobile product model: %s", productModel2)
	if productModel2 != MobileInfoModelA {
		t.Errorf("Expected device model %s, got %s", MobileInfoModelA, productModel2)
	}
}
