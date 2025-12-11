# Browser Screenshot API

The AgentBay SDK provides comprehensive screenshot capabilities across all supported languages. This document provides a summary of the API functionality and links to detailed documentation for each language implementation.

## Overview

The screenshot functionality allows you to capture web page content with enhanced options including full page capture, custom image formats, quality control, and proper handling of lazy-loaded content. All implementations follow the same design patterns and provide consistent behavior across languages.

## Key Features

All language implementations provide the following core features:

1. **Full Page Capture** - Ability to capture entire web pages including content below the fold
2. **Multiple Formats** - Support for both PNG and JPEG formats with customizable quality
3. **Enhanced Loading** - Wait for network idle state and handle lazy-loaded content
4. **Viewport Management** - Automatic viewport sizing for consistent screenshots
5. **Error Handling** - Comprehensive error handling with descriptive messages
6. **Custom Options** - Configurable timeout, animations, caret handling, and scale settings

## API Methods

### Python Implementation

The Python SDK provides two screenshot methods:

1. **Browser Agent Screenshot** - `session.browser.agent.screenshot()`
   - Returns base64 encoded data
   - Works with or without a page object
   - Suitable for agent-based workflows

2. **Direct Browser Screenshot** - `session.browser.screenshot(page)`
   - Returns raw bytes data
   - Requires a Playwright page object
   - Provides more control over the screenshot process

#### Detailed Documentation
- [Python Browser API Documentation](../../../../python/docs/api/async/async-browser.md#screenshot)

#### Example Usage
- [Python Browser Screenshot Example (Async)](../../../../python/docs/examples/_async/browser-use/browser/browser_screenshot.py)
- [Python Browser Screenshot Example (Sync)](../../../../python/docs/examples/_sync/browser-use/browser/browser_screenshot.py)
- [Python Integration Tests](../../../../python/tests/integration/_async/test_browser_screenshot.py)
- [Python Unit Tests](../../../../python/tests/unit/shared/test_browser_screenshot.py)

### TypeScript Implementation

The TypeScript SDK provides similar functionality with full Playwright integration:

#### Method Signature
```typescript
async screenshot(page: any, fullPage: boolean = false, options: Record<string, any> = {}): Promise<Uint8Array>
```

#### Detailed Documentation
- [TypeScript Browser Source Code](../../../../typescript/src/browser/browser.ts) (Search for the `screenshot` method)

#### Example Usage
- [TypeScript Browser Screenshot Test](../../../../typescript/tests/unit/browser-screenshot.test.ts)
- [TypeScript Integration Test](../../../../typescript/tests/integration/browser-screenshot.integration.test.ts)

### Go Implementation

The Go SDK provides the same screenshot capabilities with proper error handling and Playwright integration:

#### Method Signature
```go
func (b *Browser) Screenshot(page interface{}, options *ScreenshotOptions) ([]byte, error)
```

#### Detailed Documentation
- [Go Browser Source Code](../../../../golang/pkg/agentbay/browser/browser.go) (Search for the `Screenshot` method)

#### Example Usage
- [Go Browser Test](../../../../golang/tests/pkg/unit/browser_test.go)
- [Go Integration Test](../../../../golang/tests/pkg/integration/browser_screenshot_integration_test.go)

## Cross-Language Consistency

The screenshot functionality maintains consistent behavior across all language implementations:

| Feature | Python | TypeScript | Go |
|---------|--------|------------|-----|
| Method Name | `screenshot` | `screenshot` | `Screenshot` |
| Full Page Capture | ✅ | ✅ | ✅ |
| Image Format Support | PNG, JPEG | PNG, JPEG | PNG, JPEG |
| Quality Control | ✅ | ✅ | ✅ |
| Timeout Configuration | ✅ | ✅ | ✅ |
| Error Handling | BrowserError/RuntimeError | BrowserError/Error | error |
| Return Type (Direct) | bytes | Uint8Array | []byte |
| Return Type (Agent) | str (base64) | str (base64) | string (base64) |

## Common Parameters

All implementations support similar parameters:

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `page` | Page object | Playwright page object (required for direct browser method) | N/A |
| `full_page` | boolean | Whether to capture the full scrollable page | false |
| `type` | string | Image type ('png' or 'jpeg') | 'png' |
| `quality` | integer | Quality of the image (0-100, jpeg only) | 0 |
| `timeout` | integer | Maximum time in milliseconds | 60000 |
| `animations` | string | How to handle animations | 'disabled' |
| `caret` | string | How to handle the caret | 'hide' |
| `scale` | string | Scale setting | 'css' |

## Enhanced Functionality

All implementations include enhanced functionality to ensure high-quality screenshots:

1. **Network Idle Waiting** - Waits for page to reach network idle state
2. **Content Scrolling** - Automatically scrolls to load lazy-loaded content
3. **Image Loading** - Ensures images with data-src attributes are properly loaded
4. **Viewport Adjustment** - Sets appropriate viewport size for consistent captures
5. **Error Recovery** - Comprehensive error handling with descriptive messages

## Usage Patterns

### Basic Screenshot

**Python (Sync)**
```python
# Direct Browser
screenshot_data = session.browser.screenshot(page)

# Browser Agent
screenshot_data = session.browser.agent.screenshot()
```

**TypeScript**
```typescript
const screenshotData = await browser.screenshot(page);
```

**Go**
```go
screenshotData, err := browser.Screenshot(page, nil)
```

### Full Page Screenshot

**Python (Sync)**
```python
# Direct Browser
screenshot_data = session.browser.screenshot(page, full_page=True)

# Browser Agent
screenshot_data = session.browser.agent.screenshot(full_page=True)
```

**TypeScript**
```typescript
const screenshotData = await browser.screenshot(page, true);
```

**Go**
```go
options := &browser.ScreenshotOptions{FullPage: true}
screenshotData, err := browser.Screenshot(page, options)
```

### Custom Options

**Python (Sync)**
```python
# Direct Browser
screenshot_data = session.browser.screenshot(
    page,
    full_page=False,
    type="jpeg",
    quality=80,
    timeout=30000
)
```

**TypeScript**
```typescript
const screenshotData = await browser.screenshot(page, false, {
    type: "jpeg",
    quality: 80,
    timeout: 30000
});
```

**Go**
```go
options := &browser.ScreenshotOptions{
    FullPage: false,
    Type: "jpeg",
    Quality: 80,
    Timeout: 30000,
}
screenshotData, err := browser.Screenshot(page, options)
```

## Error Handling

All implementations provide consistent error handling:

1. **Browser Not Initialized** - Error when trying to take screenshot without initializing browser
2. **Page Not Provided** - Error when page parameter is null/undefined
3. **Screenshot Capture Failure** - Errors during actual screenshot capture process
4. **Network Timeout** - Timeout errors during page loading

## Best Practices

1. **Always Initialize Browser** - Ensure browser is initialized before taking screenshots
2. **Handle Errors Gracefully** - Implement proper error handling for network issues
3. **Use Appropriate Timeouts** - Set reasonable timeout values based on page complexity
4. **Consider Image Format** - Use JPEG for smaller file sizes, PNG for transparency support
5. **Verify Page State** - Ensure page is fully loaded before taking screenshots

## Related Documentation

- [Browser Context Management](./browser-context.md)
- [Browser Command Arguments](./browser-command-args.md)
- [Browser Proxies](./browser-proxies.md)
- [Stealth Mode](./browser-fingerprint.md#2-important-notice)