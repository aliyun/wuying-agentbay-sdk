package agentbay

import (
	"testing"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/browser"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

func TestSession_BrowserIntegration(t *testing.T) {
	// Create a mock AgentBay instance
	apiKey := "test-api-key"
	
	ab, err := agentbay.NewAgentBay(apiKey)
	require.NoError(t, err)
	require.NotNil(t, ab)

	// Create a session
	session := agentbay.NewSession(ab, "test-session-123")
	require.NotNil(t, session)
	require.NotNil(t, session.Browser)

	t.Run("Browser is initialized on session creation", func(t *testing.T) {
		assert.NotNil(t, session.Browser)
		assert.False(t, session.Browser.IsInitialized())
	})

	t.Run("Browser has access to session methods", func(t *testing.T) {
		// These methods should be accessible through the session
		apiKey := session.GetAPIKey()
		sessionID := session.GetSessionID()
		
		assert.Equal(t, "test-api-key", apiKey)
		assert.Equal(t, "test-session-123", sessionID)
	})
}

func TestBrowserOption_BrowserType(t *testing.T) {
	tests := []struct {
		name         string
		browserType  string
		shouldBeValid bool
	}{
		{
			name:         "chromium",
			browserType:  "chromium",
			shouldBeValid: true,
		},
		{
			name:         "chrome",
			browserType:  "chrome",
			shouldBeValid: true,
		},
		{
			name:         "firefox (invalid)",
			browserType:  "firefox",
			shouldBeValid: false,
		},
		{
			name:         "edge (invalid)",
			browserType:  "edge",
			shouldBeValid: false,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			option := browser.NewBrowserOption()
			browserType := tt.browserType
			option.BrowserType = &browserType

			err := option.Validate()
			if tt.shouldBeValid {
				assert.NoError(t, err)
			} else {
				assert.Error(t, err)
				assert.Contains(t, err.Error(), "browserType must be 'chrome' or 'chromium'")
			}
		})
	}
}

func TestBrowserOption_ToMapWithBrowserType(t *testing.T) {
	t.Run("Chrome browser type", func(t *testing.T) {
		option := browser.NewBrowserOption()
		chromeType := "chrome"
		option.BrowserType = &chromeType

		optionMap := option.ToMap()

		assert.Equal(t, "chrome", optionMap["browserType"])
		assert.Equal(t, false, optionMap["useStealth"])
		assert.Equal(t, false, optionMap["solveCaptchas"])
	})

	t.Run("No browser type specified (default)", func(t *testing.T) {
		option := browser.NewBrowserOption()
		// Don't set browserType, should not be in map

		optionMap := option.ToMap()

		_, hasBrowserType := optionMap["browserType"]
		assert.False(t, hasBrowserType)
	})

	t.Run("Complete browser option with all fields", func(t *testing.T) {
		userAgent := "Mozilla/5.0 Test"
		extPath := "/custom/extensions"
		chromeType := "chrome"

		option := &browser.BrowserOption{
			UseStealth:    true,
			UserAgent:     &userAgent,
			BrowserType:   &chromeType,
			SolveCaptchas: true,
			ExtensionPath: &extPath,
			Viewport: &browser.BrowserViewport{
				Width:  1920,
				Height: 1080,
			},
			Screen: &browser.BrowserScreen{
				Width:  1920,
				Height: 1080,
			},
		}
		
		optionMap := option.ToMap()
		
		assert.Equal(t, true, optionMap["useStealth"])
		assert.Equal(t, "chrome", optionMap["browserType"])
		assert.Equal(t, true, optionMap["solveCaptchas"])
		assert.Equal(t, userAgent, optionMap["userAgent"])
		assert.Equal(t, extPath, optionMap["extensionPath"])
		
		viewport, ok := optionMap["viewport"].(map[string]interface{})
		assert.True(t, ok)
		assert.Equal(t, 1920, viewport["width"])
		assert.Equal(t, 1080, viewport["height"])
		
		screen, ok := optionMap["screen"].(map[string]interface{})
		assert.True(t, ok)
		assert.Equal(t, 1920, screen["width"])
		assert.Equal(t, 1080, screen["height"])
	})
}

func TestBrowserProxy_ToMap(t *testing.T) {
	t.Run("Custom proxy", func(t *testing.T) {
		server := "127.0.0.1:8080"
		username := "user"
		password := "pass"
		
		proxy, err := browser.NewBrowserProxy(
			"custom",
			&server,
			&username,
			&password,
			nil,
			nil,
		)
		
		require.NoError(t, err)
		require.NotNil(t, proxy)
		
		proxyMap := proxy.ToMap()
		
		assert.Equal(t, "custom", proxyMap["type"])
		assert.Equal(t, server, proxyMap["server"])
		assert.Equal(t, username, proxyMap["username"])
		assert.Equal(t, password, proxyMap["password"])
	})

	t.Run("Wuying proxy with restricted strategy", func(t *testing.T) {
		strategy := "restricted"
		
		proxy, err := browser.NewBrowserProxy(
			"wuying",
			nil,
			nil,
			nil,
			&strategy,
			nil,
		)
		
		require.NoError(t, err)
		require.NotNil(t, proxy)
		
		proxyMap := proxy.ToMap()
		
		assert.Equal(t, "wuying", proxyMap["type"])
		assert.Equal(t, "restricted", proxyMap["strategy"])
	})

	t.Run("Wuying proxy with polling strategy", func(t *testing.T) {
		strategy := "polling"
		pollSize := 10
		
		proxy, err := browser.NewBrowserProxy(
			"wuying",
			nil,
			nil,
			nil,
			&strategy,
			&pollSize,
		)
		
		require.NoError(t, err)
		require.NotNil(t, proxy)
		
		proxyMap := proxy.ToMap()
		
		assert.Equal(t, "wuying", proxyMap["type"])
		assert.Equal(t, "polling", proxyMap["strategy"])
		assert.Equal(t, 10, proxyMap["pollsize"])
	})
}

func TestBrowserFingerprint_ToMap(t *testing.T) {
	t.Run("Complete fingerprint", func(t *testing.T) {
		fingerprint, err := browser.NewBrowserFingerprint(
			[]string{"desktop", "mobile"},
			[]string{"windows", "macos", "linux"},
			[]string{"en-US", "zh-CN"},
		)
		
		require.NoError(t, err)
		require.NotNil(t, fingerprint)
		
		fpMap := fingerprint.ToMap()
		
		devices, ok := fpMap["devices"].([]string)
		assert.True(t, ok)
		assert.Contains(t, devices, "desktop")
		assert.Contains(t, devices, "mobile")
		
		os, ok := fpMap["operatingSystems"].([]string)
		assert.True(t, ok)
		assert.Contains(t, os, "windows")
		assert.Contains(t, os, "macos")
		assert.Contains(t, os, "linux")
		
		locales, ok := fpMap["locales"].([]string)
		assert.True(t, ok)
		assert.Contains(t, locales, "en-US")
		assert.Contains(t, locales, "zh-CN")
	})

	t.Run("Partial fingerprint", func(t *testing.T) {
		fingerprint, err := browser.NewBrowserFingerprint(
			[]string{"desktop"},
			nil,
			nil,
		)
		
		require.NoError(t, err)
		require.NotNil(t, fingerprint)
		
		fpMap := fingerprint.ToMap()
		
		devices, ok := fpMap["devices"].([]string)
		assert.True(t, ok)
		assert.Contains(t, devices, "desktop")
		
		// operatingSystems and locales should not be in map if nil
		_, hasOS := fpMap["operatingSystems"]
		assert.False(t, hasOS)
		
		_, hasLocales := fpMap["locales"]
		assert.False(t, hasLocales)
	})
}

func TestBrowserViewportAndScreen_ToMap(t *testing.T) {
	t.Run("BrowserViewport ToMap", func(t *testing.T) {
		viewport := &browser.BrowserViewport{
			Width:  1366,
			Height: 768,
		}
		
		vpMap := viewport.ToMap()
		
		assert.Equal(t, 1366, vpMap["width"])
		assert.Equal(t, 768, vpMap["height"])
	})

	t.Run("BrowserScreen ToMap", func(t *testing.T) {
		screen := &browser.BrowserScreen{
			Width:  1920,
			Height: 1080,
		}
		
		screenMap := screen.ToMap()
		
		assert.Equal(t, 1920, screenMap["width"])
		assert.Equal(t, 1080, screenMap["height"])
	})
}

func TestBrowserOption_WithProxies(t *testing.T) {
	t.Run("Single proxy in option", func(t *testing.T) {
		server := "127.0.0.1:8080"
		proxy, err := browser.NewBrowserProxy("custom", &server, nil, nil, nil, nil)
		require.NoError(t, err)

		chromiumType := "chromium"
		option := &browser.BrowserOption{
			BrowserType: &chromiumType,
			Proxies:     []*browser.BrowserProxy{proxy},
		}

		err = option.Validate()
		assert.NoError(t, err)

		optionMap := option.ToMap()
		proxies, ok := optionMap["proxies"].([]map[string]interface{})
		assert.True(t, ok)
		assert.Len(t, proxies, 1)
		assert.Equal(t, "custom", proxies[0]["type"])
	})

	t.Run("Multiple proxies should fail validation", func(t *testing.T) {
		server1 := "127.0.0.1:8080"
		server2 := "127.0.0.1:8081"
		proxy1, _ := browser.NewBrowserProxy("custom", &server1, nil, nil, nil, nil)
		proxy2, _ := browser.NewBrowserProxy("custom", &server2, nil, nil, nil, nil)

		chromiumType := "chromium"
		option := &browser.BrowserOption{
			BrowserType: &chromiumType,
			Proxies:     []*browser.BrowserProxy{proxy1, proxy2},
		}

		err := option.Validate()
		assert.Error(t, err)
		assert.Contains(t, err.Error(), "proxies list length must be limited to 1")
	})
}

