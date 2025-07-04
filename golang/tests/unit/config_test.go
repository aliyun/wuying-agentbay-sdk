package unit

import (
	"os"
	"testing"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

// TestDefaultConfig tests the default configuration values
func TestDefaultConfig(t *testing.T) {
	// Get default config
	config := agentbay.DefaultConfig()

	// Verify default values
	if config.RegionID != "cn-shanghai" {
		t.Errorf("Expected RegionID to be 'cn-shanghai', got '%s'", config.RegionID)
	}
	if config.Endpoint != "wuyingai.cn-shanghai.aliyuncs.com" {
		t.Errorf("Expected Endpoint to be 'wuyingai.cn-shanghai.aliyuncs.com', got '%s'", config.Endpoint)
	}
	if config.TimeoutMs != 60000 {
		t.Errorf("Expected TimeoutMs to be 60000, got %d", config.TimeoutMs)
	}
}

// TestLoadConfigEnvironmentVariables tests that environment variables override config settings
func TestLoadConfigEnvironmentVariables(t *testing.T) {
	// Save original environment variables
	originalRegionID := os.Getenv("AGENTBAY_REGION_ID")
	originalEndpoint := os.Getenv("AGENTBAY_ENDPOINT")
	originalConfigPath := os.Getenv("AGENTBAY_CONFIG_PATH")

	// Restore environment variables after test
	defer func() {
		os.Setenv("AGENTBAY_REGION_ID", originalRegionID)
		os.Setenv("AGENTBAY_ENDPOINT", originalEndpoint)
		os.Setenv("AGENTBAY_CONFIG_PATH", originalConfigPath)
	}()

	// Set environment variables
	os.Setenv("AGENTBAY_REGION_ID", "cn-zhangjiakou")
	os.Setenv("AGENTBAY_ENDPOINT", "test.endpoint.com")
	os.Setenv("AGENTBAY_CONFIG_PATH", "") // Ensure we don't use a config file

	// Load config
	config := agentbay.LoadConfig()

	// Verify environment variables took effect
	if config.RegionID != "cn-zhangjiakou" {
		t.Errorf("Expected RegionID to be 'cn-zhangjiakou', got '%s'", config.RegionID)
	}
	if config.Endpoint != "test.endpoint.com" {
		t.Errorf("Expected Endpoint to be 'test.endpoint.com', got '%s'", config.Endpoint)
	}
	// TimeoutMs should be default value as we haven't set it
	if config.TimeoutMs != 60000 {
		t.Errorf("Expected TimeoutMs to be 60000, got %d", config.TimeoutMs)
	}
}

// TestLoadConfigFallbackToDefault tests that default values are used when no config is found
func TestLoadConfigFallbackToDefault(t *testing.T) {
	// Save original environment variables
	originalRegionID := os.Getenv("AGENTBAY_REGION_ID")
	originalEndpoint := os.Getenv("AGENTBAY_ENDPOINT")
	originalConfigPath := os.Getenv("AGENTBAY_CONFIG_PATH")

	// Restore environment variables after test
	defer func() {
		os.Setenv("AGENTBAY_REGION_ID", originalRegionID)
		os.Setenv("AGENTBAY_ENDPOINT", originalEndpoint)
		os.Setenv("AGENTBAY_CONFIG_PATH", originalConfigPath)
	}()

	// Clear environment variables to ensure defaults are used
	os.Unsetenv("AGENTBAY_REGION_ID")
	os.Unsetenv("AGENTBAY_ENDPOINT")
	os.Setenv("AGENTBAY_CONFIG_PATH", "/path/to/nonexistent/config.json")

	// Load config (should fall back to defaults)
	config := agentbay.LoadConfig()

	// Verify default values
	if config.RegionID != "cn-shanghai" {
		t.Errorf("Expected RegionID to be 'cn-shanghai', got '%s'", config.RegionID)
	}
	if config.Endpoint != "wuyingai.cn-shanghai.aliyuncs.com" {
		t.Errorf("Expected Endpoint to be 'wuyingai.cn-shanghai.aliyuncs.com', got '%s'", config.Endpoint)
	}
	if config.TimeoutMs != 60000 {
		t.Errorf("Expected TimeoutMs to be 60000, got %d", config.TimeoutMs)
	}
}
