package agentbay

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
)

// Config stores SDK configuration
type Config struct {
	RegionID  string `json:"region_id"`
	Endpoint  string `json:"endpoint"`
	TimeoutMs int    `json:"timeout_ms"`
}

// DefaultConfig returns the default configuration
func DefaultConfig() Config {
	return Config{
		RegionID:  "cn-shanghai",
		Endpoint:  "wuyingai.cn-shanghai.aliyuncs.com",
		TimeoutMs: 60000,
	}
}

// LoadConfig loads the configuration from file
func LoadConfig() Config {
	// First check if the config file path is specified in environment variables
	configPath := os.Getenv("AGENTBAY_CONFIG_PATH")
	if configPath == "" {
		// Try to find the config file in the project root directory
		// First try the current directory
		configPath = "config.json"
		if _, err := os.Stat(configPath); os.IsNotExist(err) {
			// Then try the parent directory
			configPath = filepath.Join("..", "config.json")
			if _, err := os.Stat(configPath); os.IsNotExist(err) {
				// Then try the grandparent directory
				configPath = filepath.Join("..", "..", "config.json")
				if _, err := os.Stat(configPath); os.IsNotExist(err) {
					// Config file not found, return default config
					fmt.Println("Warning: Configuration file not found, using default values")
					return DefaultConfig()
				}
			}
		}
	}

	// Read the config file
	data, err := os.ReadFile(configPath)
	if err != nil {
		fmt.Printf("Warning: Failed to read configuration file: %v, using default values\n", err)
		return DefaultConfig()
	}

	// Parse JSON
	var config Config
	if err := json.Unmarshal(data, &config); err != nil {
		fmt.Printf("Warning: Failed to parse configuration file: %v, using default values\n", err)
		return DefaultConfig()
	}

	// Allow environment variables to override config file values
	if regionID := os.Getenv("AGENTBAY_REGION_ID"); regionID != "" {
		config.RegionID = regionID
	}
	if endpoint := os.Getenv("AGENTBAY_ENDPOINT"); endpoint != "" {
		config.Endpoint = endpoint
	}

	return config
}
