package agentbay

import (
	// "encoding/json"
	"fmt"
	"os"
	// "path/filepath"

	"github.com/joho/godotenv"
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

// LoadConfig loads the configuration from file or environment variables.
func LoadConfig(cfg *Config) Config {
	if cfg != nil {
		// If config is explicitly provided, use it directly
		return Config{
			RegionID:  cfg.RegionID,
			Endpoint:  cfg.Endpoint,
			TimeoutMs: cfg.TimeoutMs,
		}
	}

	// First try to load from .env file if present in current directory
	var envPath string
	workingDir, err := os.Getwd()
	if err != nil {
		fmt.Printf("Warning: Failed to get current working directory: %v\n", err)
	} else {
		envPath = workingDir + "/.env"
	}

	err = godotenv.Load(envPath)
	if err != nil {
		fmt.Printf("Warning: Failed to load .env file: %v\n", err)
	}

	// Use environment variables if set
	config := DefaultConfig()

	if regionID := os.Getenv("AGENTBAY_REGION_ID"); regionID != "" {
		config.RegionID = regionID
	}
	if endpoint := os.Getenv("AGENTBAY_ENDPOINT"); endpoint != "" {
		config.Endpoint = endpoint
	}
	if timeoutMS := os.Getenv("AGENTBAY_TIMEOUT_MS"); timeoutMS != "" {
		_, err := fmt.Sscanf(timeoutMS, "%d", &config.TimeoutMs)
		if err != nil {
			fmt.Printf("Warning: Failed to parse AGENTBAY_TIMEOUT_MS as integer: %v, using default value %d\n", err, config.TimeoutMs)
		}
	}

	return config
}
