package agentbay_test

import (
	"fmt"
	"os"
	"path"
	"testing"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
	"github.com/stretchr/testify/assert"
)

func TestLoadConfig_WithExplicitConfig(t *testing.T) {
	// 测试显式传入的配置是否被正确使用
	customCfg := &agentbay.Config{
		RegionID:  "custom-region",
		Endpoint:  "custom-endpoint",
		TimeoutMs: 5000,
	}

	result := agentbay.LoadConfig(customCfg)

	assert.Equal(t, "custom-region", result.RegionID)
	assert.Equal(t, "custom-endpoint", result.Endpoint)
	assert.Equal(t, 5000, result.TimeoutMs)
}

func TestLoadConfig_FromEnvFile(t *testing.T) {
	// 创建临时目录和 .env 文件
	dir := t.TempDir()
	envFilePath := path.Join(dir, ".env")
	err := os.WriteFile(envFilePath, []byte(`
AGENTBAY_REGION_ID=env-region
AGENTBAY_ENDPOINT=env-endpoint
AGENTBAY_TIMEOUT_MS=10000
`), 0644)
	if err != nil {
		t.Fatalf("Failed to create .env file: %v", err)
	}

	// 清除环境变量以避免干扰
	os.Unsetenv("AGENTBAY_REGION_ID")
	os.Unsetenv("AGENTBAY_ENDPOINT")
	os.Unsetenv("AGENTBAY_TIMEOUT_MS")

	// 切换到临时目录
	cwd, _ := os.Getwd()
	defer os.Chdir(cwd)
	os.Chdir(dir)

	// 执行测试
	result := agentbay.LoadConfig(nil)

	assert.Equal(t, "env-region", result.RegionID)
	assert.Equal(t, "env-endpoint", result.Endpoint)
	assert.Equal(t, 10000, result.TimeoutMs)
}

func TestLoadConfig_FromEnvironmentVariables(t *testing.T) {
	// 设置环境变量
	os.Setenv("AGENTBAY_REGION_ID", "sys-region")
	os.Setenv("AGENTBAY_ENDPOINT", "sys-endpoint")
	os.Setenv("AGENTBAY_TIMEOUT_MS", "15000")
	defer func() {
		os.Unsetenv("AGENTBAY_REGION_ID")
		os.Unsetenv("AGENTBAY_ENDPOINT")
		os.Unsetenv("AGENTBAY_TIMEOUT_MS")
	}()

	// 执行测试
	result := agentbay.LoadConfig(nil)

	assert.Equal(t, "sys-region", result.RegionID)
	assert.Equal(t, "sys-endpoint", result.Endpoint)
	assert.Equal(t, 15000, result.TimeoutMs)
}

func TestLoadConfig_UsesDefaultsWhenNoSource(t *testing.T) {
	// 确保所有环境变量都未设置
	os.Unsetenv("AGENTBAY_REGION_ID")
	os.Unsetenv("AGENTBAY_ENDPOINT")
	os.Unsetenv("AGENTBAY_TIMEOUT_MS")

	// 执行测试
	result := agentbay.LoadConfig(nil)

	defaultCfg := agentbay.DefaultConfig()
	assert.Equal(t, defaultCfg.RegionID, result.RegionID)
	assert.Equal(t, defaultCfg.Endpoint, result.Endpoint)
	assert.Equal(t, defaultCfg.TimeoutMs, result.TimeoutMs)
}

func TestLoadConfig_ConfigPrecedenceOrder(t *testing.T) {
	dir := t.TempDir()
	envFilePath := path.Join(dir, ".env")
	err := os.WriteFile(envFilePath, []byte(fmt.Sprintf(`
AGENTBAY_REGION_ID=env-region
AGENTBAY_ENDPOINT=env-endpoint
AGENTBAY_TIMEOUT_MS=10000
`)), 0644)
	if err != nil {
		t.Fatalf("Failed to create .env file: %v", err)
	}

	// 切换工作目录
	cwd, _ := os.Getwd()
	defer os.Chdir(cwd)
	os.Chdir(dir)

	// 设置环境变量
	os.Setenv("AGENTBAY_REGION_ID", "sys-region")
	os.Setenv("AGENTBAY_ENDPOINT", "sys-endpoint")
	os.Setenv("AGENTBAY_TIMEOUT_MS", "15000")
	defer func() {
		os.Unsetenv("AGENTBAY_REGION_ID")
		os.Unsetenv("AGENTBAY_ENDPOINT")
		os.Unsetenv("AGENTBAY_TIMEOUT_MS")
	}()

	// 默认配置
	defaultCfg := agentbay.DefaultConfig()

	// 1. 显式传入的配置应该优先
	customCfg := &agentbay.Config{
		RegionID:  "explicit-region",
		Endpoint:  "explicit-endpoint",
		TimeoutMs: 2000,
	}
	result := agentbay.LoadConfig(customCfg)
	assert.Equal(t, "explicit-region", result.RegionID)
	assert.Equal(t, "explicit-endpoint", result.Endpoint)
	assert.Equal(t, 2000, result.TimeoutMs)

	// 2. 当 cfg == nil 时应使用环境变量
	result = agentbay.LoadConfig(nil)
	assert.Equal(t, "sys-region", result.RegionID)
	assert.Equal(t, "sys-endpoint", result.Endpoint)
	assert.Equal(t, 15000, result.TimeoutMs)

	// 3. 清除环境变量后应使用 .env 文件
	os.Unsetenv("AGENTBAY_REGION_ID")
	os.Unsetenv("AGENTBAY_ENDPOINT")
	os.Unsetenv("AGENTBAY_TIMEOUT_MS")

	result = agentbay.LoadConfig(nil)
	assert.Equal(t, "env-region", result.RegionID)
	assert.Equal(t, "env-endpoint", result.Endpoint)
	assert.Equal(t, 10000, result.TimeoutMs)

	// 4. 没有任何配置源时应使用默认值
	os.Remove(envFilePath) // 删除 .env 文件
	os.Unsetenv("AGENTBAY_REGION_ID")
	os.Unsetenv("AGENTBAY_ENDPOINT")
	os.Unsetenv("AGENTBAY_TIMEOUT_MS")

	result = agentbay.LoadConfig(nil)
	assert.Equal(t, defaultCfg.RegionID, result.RegionID)
	assert.Equal(t, defaultCfg.Endpoint, result.Endpoint)
	assert.Equal(t, defaultCfg.TimeoutMs, result.TimeoutMs)
}