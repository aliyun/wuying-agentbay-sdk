package browser

import (
	"errors"
	"fmt"
	"os"

	"github.com/alibabacloud-go/tea/dara"
	"github.com/aliyun/wuying-agentbay-sdk/golang/api/client"
	"github.com/playwright-community/playwright-go"
)

// BrowserProxy represents browser proxy configuration.
// Supports two types of proxy: custom proxy and wuying proxy.
// Wuying proxy supports two strategies: restricted and polling.
//
// Example:
//
//	// Custom proxy
//	server := "proxy.example.com:8080"
//	username := "user"
//	password := "pass"
//	customProxy := &browser.BrowserProxy{
//	    Type:     "custom",
//	    Server:   &server,
//	    Username: &username,
//	    Password: &password,
//	}
//
//	// WuYing proxy with restricted strategy
//	strategy := "restricted"
//	wuyingProxy := &browser.BrowserProxy{
//	    Type:     "wuying",
//	    Strategy: &strategy,
//	}
//
//	// WuYing proxy with polling strategy
//	pollingStrategy := "polling"
//	pollSize := 10
//	pollingProxy := &browser.BrowserProxy{
//	    Type:     "wuying",
//	    Strategy: &pollingStrategy,
//	    PollSize: &pollSize,
//	}
type BrowserProxy struct {
	Type     string  `json:"type"`               // Type of proxy - "custom" or "wuying"
	Server   *string `json:"server,omitempty"`   // Proxy server address (required for custom type)
	Username *string `json:"username,omitempty"` // Proxy username (optional for custom type)
	Password *string `json:"password,omitempty"` // Proxy password (optional for custom type)
	Strategy *string `json:"strategy,omitempty"` // Strategy for wuying: "restricted" or "polling"
	PollSize *int    `json:"pollsize,omitempty"` // Pool size (optional for wuying with polling strategy)
}

// NewBrowserProxy creates a new BrowserProxy with validation
func NewBrowserProxy(proxyType string, server, username, password, strategy *string, pollSize *int) (*BrowserProxy, error) {
	proxy := &BrowserProxy{
		Type:     proxyType,
		Server:   server,
		Username: username,
		Password: password,
		Strategy: strategy,
		PollSize: pollSize,
	}

	// Validation
	if proxyType != "custom" && proxyType != "wuying" {
		return nil, errors.New("proxy_type must be custom or wuying")
	}

	if proxyType == "custom" && (server == nil || *server == "") {
		return nil, errors.New("server is required for custom proxy type")
	}

	if proxyType == "wuying" && (strategy == nil || *strategy == "") {
		return nil, errors.New("strategy is required for wuying proxy type")
	}

	if proxyType == "wuying" && strategy != nil && *strategy != "restricted" && *strategy != "polling" {
		return nil, errors.New("strategy must be restricted or polling for wuying proxy type")
	}

	if proxyType == "wuying" && strategy != nil && *strategy == "polling" && pollSize != nil && *pollSize <= 0 {
		return nil, errors.New("pollsize must be greater than 0 for polling strategy")
	}

	return proxy, nil
}

// toMap converts BrowserProxy to map for API request
func (p *BrowserProxy) toMap() map[string]interface{} {
	proxyMap := map[string]interface{}{
		"type": p.Type,
	}

	if p.Type == "custom" {
		if p.Server != nil {
			proxyMap["server"] = *p.Server
		}
		if p.Username != nil {
			proxyMap["username"] = *p.Username
		}
		if p.Password != nil {
			proxyMap["password"] = *p.Password
		}
	} else if p.Type == "wuying" {
		if p.Strategy != nil {
			proxyMap["strategy"] = *p.Strategy
		}
		if p.Strategy != nil && *p.Strategy == "polling" && p.PollSize != nil {
			proxyMap["pollsize"] = *p.PollSize
		}
	}

	return proxyMap
}

// BrowserViewport represents browser viewport options
type BrowserViewport struct {
	Width  int `json:"width"`  // Viewport width
	Height int `json:"height"` // Viewport height
}

// toMap converts BrowserViewport to map for API request
func (v *BrowserViewport) toMap() map[string]interface{} {
	return map[string]interface{}{
		"width":  v.Width,
		"height": v.Height,
	}
}

// BrowserScreen represents browser screen options
type BrowserScreen struct {
	Width  int `json:"width"`  // Screen width
	Height int `json:"height"` // Screen height
}

// toMap converts BrowserScreen to map for API request
func (s *BrowserScreen) toMap() map[string]interface{} {
	return map[string]interface{}{
		"width":  s.Width,
		"height": s.Height,
	}
}

// BrowserFingerprint represents browser fingerprint options
//
// Example:
//
//	fingerprint := &browser.BrowserFingerprint{
//	    Devices:          []string{"desktop"},
//	    OperatingSystems: []string{"windows", "macos"},
//	    Locales:          []string{"en-US", "en-GB"},
//	}
type BrowserFingerprint struct {
	Devices          []string `json:"devices,omitempty"`          // Device types: "desktop" or "mobile"
	OperatingSystems []string `json:"operatingSystems,omitempty"` // OS types: "windows", "macos", "linux", "android", "ios"
	Locales          []string `json:"locales,omitempty"`          // Locale identifiers
}

// NewBrowserFingerprint creates a new BrowserFingerprint with validation
func NewBrowserFingerprint(devices, operatingSystems, locales []string) (*BrowserFingerprint, error) {
	// Validate devices
	if devices != nil {
		for _, device := range devices {
			if device != "desktop" && device != "mobile" {
				return nil, errors.New("device must be desktop or mobile")
			}
		}
	}

	// Validate operating systems
	if operatingSystems != nil {
		validOS := map[string]bool{"windows": true, "macos": true, "linux": true, "android": true, "ios": true}
		for _, os := range operatingSystems {
			if !validOS[os] {
				return nil, errors.New("operating_system must be windows, macos, linux, android or ios")
			}
		}
	}

	return &BrowserFingerprint{
		Devices:          devices,
		OperatingSystems: operatingSystems,
		Locales:          locales,
	}, nil
}

// toMap converts BrowserFingerprint to map for API request
func (f *BrowserFingerprint) toMap() map[string]interface{} {
	fpMap := make(map[string]interface{})
	if f.Devices != nil {
		fpMap["devices"] = f.Devices
	}
	if f.OperatingSystems != nil {
		fpMap["operatingSystems"] = f.OperatingSystems
	}
	if f.Locales != nil {
		fpMap["locales"] = f.Locales
	}
	return fpMap
}

// BrowserOption represents browser initialization options
//
// Example:
//
//	option := browser.NewBrowserOption()
//
//	// Custom user agent
//	ua := "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"
//	option.UserAgent = &ua
//
//	// Viewport and screen
//	option.Viewport = &browser.BrowserViewport{Width: 1920, Height: 1080}
//	option.Screen = &browser.BrowserScreen{Width: 1920, Height: 1080}
//
//	// Stealth mode
//	option.UseStealth = true
//
//	// Validate configuration
//	if err := option.Validate(); err != nil {
//	    log.Fatalf("Invalid configuration: %v", err)
//	}
type BrowserOption struct {
	UseStealth         bool                `json:"useStealth,omitempty"`         // Enable stealth mode
	UserAgent          *string             `json:"userAgent,omitempty"`          // Custom user agent
	Viewport           *BrowserViewport    `json:"viewport,omitempty"`           // Viewport configuration
	Screen             *BrowserScreen      `json:"screen,omitempty"`             // Screen configuration
	Fingerprint        *BrowserFingerprint `json:"fingerprint,omitempty"`        // Fingerprint configuration
	SolveCaptchas      bool                `json:"solveCaptchas,omitempty"`      // Auto-solve captchas
	Proxies            []*BrowserProxy     `json:"proxies,omitempty"`            // Proxy configurations
	ExtensionPath      *string             `json:"extensionPath,omitempty"`      // Path to extensions directory
	CmdArgs            []string            `json:"cmdArgs,omitempty"`            // Additional command line arguments
	DefaultNavigateUrl *string             `json:"defaultNavigateUrl,omitempty"` // Default URL to navigate to when browser starts
	BrowserType        *string             `json:"browserType,omitempty"`        // Browser type: "chrome" or "chromium"
}

// NewBrowserOption creates a new BrowserOption with default values and validation
//
// Example:
//
//	option := browser.NewBrowserOption()
//	option.UseStealth = true
func NewBrowserOption() *BrowserOption {
	defaultExtPath := "/tmp/extensions/"
	return &BrowserOption{
		UseStealth:    false,
		SolveCaptchas: false,
		ExtensionPath: &defaultExtPath,
		BrowserType:   nil, // Default to nil (no browser type specified)
	}
}

// Validate validates the BrowserOption
//
// Example:
//
//	package main
//	import (
//		"fmt"
//		"os"
//		"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/browser"
//	)
//	func main() {
//		option := browser.NewBrowserOption()
//
//		// Set custom configuration
//		customUA := "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"
//		option.UserAgent = &customUA
//		option.UseStealth = true
//
//		// Validate before use
//		if err := option.Validate(); err != nil {
//			fmt.Printf("Error: %v\n", err)
//			os.Exit(1)
//		}
//		fmt.Println("Browser option validated successfully")
//
//		// Output: Browser option validated successfully
//	}
func (o *BrowserOption) Validate() error {
	// Validate proxies
	if len(o.Proxies) > 1 {
		return errors.New("proxies list length must be limited to 1")
	}

	// Validate extension path
	if o.ExtensionPath != nil && *o.ExtensionPath == "" {
		return errors.New("extensionPath cannot be empty")
	}

	// Validate browser type
	if o.BrowserType != nil && *o.BrowserType != "chrome" && *o.BrowserType != "chromium" {
		return errors.New("browserType must be 'chrome' or 'chromium'")
	}

	// Validate cmdArgs (no specific validation needed, just ensure it's not nil when empty)
	// CmdArgs can be any slice of strings

	// Validate defaultNavigateUrl (no specific validation needed for URL format)
	// DefaultNavigateUrl can be any string

	return nil
}

// toMap converts BrowserOption to map for API request
func (o *BrowserOption) toMap() map[string]interface{} {
	optionMap := make(map[string]interface{})

	// Check for AGENTBAY_BROWSER_BEHAVIOR_SIMULATE environment variable
	if behaviorSimulate := os.Getenv("AGENTBAY_BROWSER_BEHAVIOR_SIMULATE"); behaviorSimulate != "" {
		optionMap["behaviorSimulate"] = behaviorSimulate != "0"
	}

	optionMap["useStealth"] = o.UseStealth

	if o.UserAgent != nil {
		optionMap["userAgent"] = *o.UserAgent
	}

	if o.Viewport != nil {
		optionMap["viewport"] = o.Viewport.toMap()
	}

	if o.Screen != nil {
		optionMap["screen"] = o.Screen.toMap()
	}

	if o.Fingerprint != nil {
		optionMap["fingerprint"] = o.Fingerprint.toMap()
	}

	optionMap["solveCaptchas"] = o.SolveCaptchas

	if len(o.Proxies) > 0 {
		proxies := make([]map[string]interface{}, len(o.Proxies))
		for i, proxy := range o.Proxies {
			proxies[i] = proxy.toMap()
		}
		optionMap["proxies"] = proxies
	}

	if o.ExtensionPath != nil {
		optionMap["extensionPath"] = *o.ExtensionPath
	}

	if len(o.CmdArgs) > 0 {
		optionMap["cmdArgs"] = o.CmdArgs
	}

	if o.DefaultNavigateUrl != nil {
		optionMap["defaultNavigateUrl"] = *o.DefaultNavigateUrl
	}

	if o.BrowserType != nil {
		optionMap["browserType"] = *o.BrowserType
	}

	return optionMap
}

// SessionInterface defines a minimal interface for Browser to interact with Session
// This interface allows us to avoid circular dependencies while still accessing
// necessary Session methods
// LinkResult represents the result of GetLink call
type LinkResult struct {
	Link string
}

// McpToolResult represents the result of CallMcpTool call
type McpToolResult struct {
	Success      bool
	Data         string
	ErrorMessage string
}

// SessionInterface defines the interface that Session must implement for Browser
type SessionInterface interface {
	GetAPIKey() string
	GetSessionID() string
	GetClient() *client.Client
	CallMcpToolForBrowser(toolName string, args interface{}) (*McpToolResult, error)
	GetLinkForBrowser(protocolType *string, port *int32, options *string) (*LinkResult, error)
	IsVPCEnabled() bool
	GetNetworkInterfaceIP() string
	GetHttpPortNumber() string
}

// Browser provides browser-related operations for the session
type Browser struct {
	session     SessionInterface
	endpointURL string
	initialized bool
	option      *BrowserOption
}

// NewBrowser creates a new Browser instance
func NewBrowser(session SessionInterface) *Browser {
	return &Browser{
		session:     session,
		initialized: false,
	}
}

// IsInitialized returns true if the browser was initialized, false otherwise
//
// Example:
//
//	if session.Browser.IsInitialized() {
//	    // Browser is ready
//	}
func (b *Browser) IsInitialized() bool {
	return b.initialized
}

// GetOption returns the current BrowserOption used to initialize the browser, or nil if not set
//
// Example:
//
//	currentOption := session.Browser.GetOption()
//	if currentOption != nil && currentOption.UseStealth {
//	    // Stealth mode is enabled
//	}
func (b *Browser) GetOption() *BrowserOption {
	return b.option
}

// GetEndpointURL returns the endpoint URL if the browser is initialized
//
// Example:
//
//	client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
//	result, _ := client.Create(agentbay.NewCreateSessionParams().WithImageId("browser_latest"))
//	defer result.Session.Delete()
//	session.Browser.Initialize(browser.NewBrowserOption())
//	endpointURL, _ := session.Browser.GetEndpointURL()
//	pw, _ := playwright.Run()
//	browserConn, _ := pw.Chromium.ConnectOverCDP(endpointURL)
//	defer browserConn.Close()
func (b *Browser) GetEndpointURL() (string, error) {
	if !b.initialized {
		return "", errors.New("browser is not initialized. Cannot access endpoint URL")
	}

	if b.session.IsVPCEnabled() {
		// For VPC mode, construct endpoint URL from VPC IP and port
		b.endpointURL = fmt.Sprintf("ws://%s:%s", b.session.GetNetworkInterfaceIP(), b.session.GetHttpPortNumber())
		return b.endpointURL, nil
	}

	// For non-VPC mode, use GetCdpLink API
	request := &client.GetCdpLinkRequest{
		Authorization: dara.String(fmt.Sprintf("Bearer %s", b.session.GetAPIKey())),
		SessionId:     dara.String(b.session.GetSessionID()),
	}

	response, err := b.session.GetClient().GetCdpLink(request)
	if err != nil {
		return "", fmt.Errorf("failed to get CDP link: %w", err)
	}

	if response.Body == nil || response.Body.Success == nil || !*response.Body.Success {
		errorMsg := "Unknown error"
		if response.Body != nil && response.Body.Message != nil {
			errorMsg = *response.Body.Message
		}
		return "", fmt.Errorf("failed to get CDP link: %s", errorMsg)
	}

	if response.Body.Data == nil || response.Body.Data.Url == nil {
		return "", errors.New("CDP link URL is empty in response")
	}

	b.endpointURL = *response.Body.Data.Url
	return b.endpointURL, nil
}

// Initialize initializes the browser instance with the given options.
// Returns true and nil error if successful, false and error otherwise.
//
// Example:
//
//	option := browser.NewBrowserOption()
//	option.UseStealth = true
//	success, _ := session.Browser.Initialize(option)
//	if success {
//	    endpoint, _ := session.Browser.GetEndpointURL()
//	    pw, _ := playwright.Run()
//	    remoteBrowser, _ := pw.Chromium.ConnectOverCDP(endpoint)
//	    defer remoteBrowser.Close()
//	}
func (b *Browser) Initialize(option *BrowserOption) (bool, error) {
	if b.initialized {
		return true, nil
	}

	// Validate the option
	if err := option.Validate(); err != nil {
		return false, fmt.Errorf("invalid browser option: %w", err)
	}

	// Convert option to map
	browserOptionMap := option.toMap()

	// Enable record if session has enableBrowserReplay set to true
	// Check if session implements GetEnableBrowserReplay method
	if enableReplayGetter, ok := b.session.(interface {
		GetEnableBrowserReplay() bool
	}); ok {
		if enableReplayGetter.GetEnableBrowserReplay() {
			browserOptionMap["enableRecord"] = true
		}
	}

	// Create InitBrowserRequest
	authorization := "Bearer " + b.session.GetAPIKey()
	sessionID := b.session.GetSessionID()
	persistentPath := "/tmp/agentbay_browser" // Match Python BROWSER_DATA_PATH

	request := &client.InitBrowserRequest{
		Authorization:  &authorization,
		SessionId:      &sessionID,
		PersistentPath: &persistentPath,
		BrowserOption:  browserOptionMap,
	}

	// Log API request
	fmt.Printf("🔗 API Call: InitBrowser\n")
	fmt.Printf("   Request: SessionId=%s", *request.SessionId)
	if request.PersistentPath != nil {
		fmt.Printf(", PersistentPath=%s\n", *request.PersistentPath)
	}
	if request.BrowserOption != nil {
		fmt.Printf("BrowserOption: %+v\n", request.BrowserOption)
	}

	// Call the client's InitBrowser method
	response, err := b.session.GetClient().InitBrowser(request)
	if err != nil {
		return false, fmt.Errorf("failed to initialize browser: %w", err)
	}

	// Log API response
	fmt.Printf("📥 API Response: InitBrowser\n")
	if response.Body != nil {
		fmt.Printf("Full Response: %+v\n", response.Body)
	}

	// Check the response
	if response == nil || response.Body == nil || response.Body.Data == nil {
		return false, errors.New("browser initialization failed: invalid response")
	}

	// Check if Port is present in the response data
	if response.Body.Data.Port != nil {
		b.initialized = true
		b.option = option
		return true, nil
	}

	return false, errors.New("browser initialization failed: no port in response")
}

// Destroy the browser instance
//
// Example:
//
//	client, _ := agentbay.NewAgentBay(os.Getenv("AGENTBAY_API_KEY"), nil)
//	result, _ := client.Create(nil)
//	defer result.Session.Delete()
//	session.Browser.Initialize(browser.NewBrowserOption())
//	session.Browser.Destroy()
func (b *Browser) Destroy() error {
	if !b.initialized {
		return errors.New("browser is not initialized. Cannot destroy browser")
	}

	// Call the MCP tool to stop Chrome
	_, err := b.session.CallMcpToolForBrowser("stopChrome", map[string]interface{}{})
	if err != nil {
		return fmt.Errorf("failed to destroy browser: %w", err)
	}

	return nil
}

// ScreenshotOptions represents options for taking screenshots
type ScreenshotOptions struct {
	FullPage bool
	Type     string // "png" or "jpeg"
	Quality  int    // 0-100 for jpeg
	Timeout  int    // timeout in milliseconds
}

// Screenshot takes a screenshot of the specified page with enhanced options and error handling.
// This method requires the caller to connect to the browser via Playwright or similar
// and pass the page object to this method.
//
// Parameters:
//   - page: The Playwright Page object to take a screenshot of. This is a required parameter.
//   - options: Screenshot options including:
//   - FullPage (bool): Whether to capture the full scrollable page. Defaults to false.
//   - Type (string): Image type, either "png" or "jpeg". Defaults to "png".
//   - Quality (int): Quality of the image, between 0-100 (jpeg only). Defaults to 0.
//   - Timeout (int): Maximum time in milliseconds. Defaults to 60000.
//
// Returns:
//   - []byte: Screenshot data as bytes.
//   - error: Error if browser is not initialized or screenshot capture fails.
//
// Example:
//
//	// Connect to browser using Playwright
//	// pw, _ := playwright.Run()
//	// browser, _ := pw.Chromium.ConnectOverCDP(endpointURL)
//	// page, _ := browser.NewPage()
//	screenshotData, _ := session.Browser.Screenshot(page, nil)
func (b *Browser) Screenshot(page playwright.Page, options *ScreenshotOptions) ([]byte, error) {
	if !b.initialized {
		return nil, errors.New("browser must be initialized before calling screenshot")
	}

	// Create default options if none provided
	if options == nil {
		options = &ScreenshotOptions{
			FullPage: false,
			Type:     "png",
			Quality:  0,
			Timeout:  60000,
		}
	}

	// Set default enhanced options
	enhancedOptions := map[string]interface{}{
		"animations": "disabled",
		"caret":      "hide",
		"scale":      "css",
		"timeout":    options.Timeout,
		"fullPage":   options.FullPage,
		"type":       options.Type,
	}

	// Add quality if type is jpeg
	if options.Type == "jpeg" && options.Quality > 0 {
		enhancedOptions["quality"] = options.Quality
	}

	// Use the actual Playwright page object
	playwrightPage := page

	try := func() ([]byte, error) {
		// Wait for page to load
		// if err := playwrightPage.WaitForLoadState("networkidle"); err != nil {
		// 	return nil, err
		// }

		if _, err := playwrightPage.Evaluate("window.scrollTo(0, document.body.scrollHeight)"); err != nil {
			return nil, err
		}

		if err := playwrightPage.WaitForLoadState(playwright.PageWaitForLoadStateOptions{
			State: playwright.LoadStateDomcontentloaded,
		}); err != nil {
			return nil, err
		}

		// Scroll to load all content (especially for lazy-loaded elements)
		if err := b._scrollToLoadAllContent(playwrightPage, 8, 1200); err != nil {
			return nil, err
		}

		// Ensure images with data-src attributes are loaded
		_, err := playwrightPage.Evaluate(`
			() => {
				document.querySelectorAll('img[data-src]').forEach(img => {
					if (!img.src && img.dataset.src) {
						img.src = img.dataset.src;
					}
				});
				// Also handle background-image[data-bg]
				document.querySelectorAll('[data-bg]').forEach(el => {
					if (!el.style.backgroundImage) {
						el.style.backgroundImage = 'url(' + el.dataset.bg + ')';
					}
				});
			}
		`)
		if err != nil {
			return nil, err
		}

		// Wait a bit for images to load
		playwrightPage.WaitForTimeout(1500)

		finalHeightResult, err := playwrightPage.Evaluate("document.body.scrollHeight")
		if err != nil {
			return nil, err
		}

		finalHeight, ok := finalHeightResult.(int)
		if !ok {
			// Try to convert from float64 if that's what we got
			if floatHeight, ok := finalHeightResult.(float64); ok {
				finalHeight = int(floatHeight)
			} else {
				finalHeight = 10000
			}
		}

		if err := playwrightPage.SetViewportSize(1920, min(finalHeight, 10000)); err != nil {
			return nil, err
		}

		// Take the screenshot
		timeoutFloat := float64(options.Timeout)
		screenshotOptions := playwright.PageScreenshotOptions{
			FullPage: &options.FullPage,
			Timeout:  &timeoutFloat,
		}
		if options.Type == "jpeg" {
			screenshotOptions.Type = playwright.ScreenshotTypeJpeg
			if options.Quality > 0 {
				quality := options.Quality
				screenshotOptions.Quality = &quality
			}
		} else {
			screenshotOptions.Type = playwright.ScreenshotTypePng
		}
		screenshotBytes, err := playwrightPage.Screenshot(screenshotOptions)
		if err != nil {
			return nil, err
		}

		fmt.Println("Screenshot captured successfully.")
		return screenshotBytes, nil
	}

	screenshotBytes, err := try()
	if err != nil {
		// Convert error to string safely to avoid comparison issues
		errorStr := fmt.Sprintf("%v", err)
		errorMsg := fmt.Sprintf("Failed to capture screenshot: %s", errorStr)
		return nil, errors.New(errorMsg)
	}

	return screenshotBytes, nil
}

// _scrollToLoadAllContent scrolls the page to load all content (especially for lazy-loaded elements)
func (b *Browser) _scrollToLoadAllContent(page interface {
	Evaluate(string, ...interface{}) (interface{}, error)
	WaitForTimeout(float64)
}, maxScrolls int, delayMs int) error {
	if maxScrolls <= 0 {
		maxScrolls = 8
	}
	if delayMs <= 0 {
		delayMs = 1200
	}

	lastHeight := 0
	for i := 0; i < maxScrolls; i++ {
		_, err := page.Evaluate("window.scrollTo(0, document.body.scrollHeight)")
		if err != nil {
			return err
		}

		page.WaitForTimeout(float64(delayMs))

		newHeightResult, err := page.Evaluate("Math.max(document.body.scrollHeight, document.documentElement.scrollHeight)")
		if err != nil {
			return err
		}

		newHeight := 0
		if intHeight, ok := newHeightResult.(int); ok {
			newHeight = intHeight
		} else if floatHeight, ok := newHeightResult.(float64); ok {
			newHeight = int(floatHeight)
		}

		if newHeight == lastHeight {
			break
		}
		lastHeight = newHeight
	}
	return nil
}

// Helper function to find minimum of two integers
func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}
