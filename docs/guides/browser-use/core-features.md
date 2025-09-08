# AIBrowser Core Features

## Context

- [BrowserContext](core-features/browser-context.md) - Create new or reuse existing browser contexts to speed up web page navigation and reduce anti-bot friction

## Extension

## File Upload/Download

## Observability

### Stealth Mode

### IPProxy

### Captcha Resolving

CAPTCHA challenges are common obstacles in web automation that can disrupt your workflow. AIBrowser includes an intelligent CAPTCHA resolution system that automatically handles these verification challenges, ensuring your automation tasks proceed smoothly.

> **Version Information:** CAPTCHA resolution is available starting from version 0.7.0. Currently, the system only supports automatic resolution of slider-type CAPTCHAs. Support for text-based CAPTCHAs will be added in future releases.

**Automatic CAPTCHA Resolution:**

The system works by:
- Detecting CAPTCHA challenges as they appear on web pages
- Processing the challenge using advanced recognition algorithms
- Completing the verification process transparently
- Resolution typically completes within 30 seconds for most CAPTCHA types
- Feature is opt-in and disabled by default for performance optimization

**Event Monitoring:**

Track CAPTCHA resolution progress through console events. This allows you to implement custom logic while the system handles the verification:

```python
def handle_console(msg):
    nonlocal captcha_solving_started, captcha_solving_finished
    print(f"got console msg: {msg.text}")
    if msg.text == "wuying-captcha-solving-started":
        captcha_solving_started = True
        print("setting captchaSolvingStarted = true")
        asyncio.create_task(page.evaluate("window.captchaSolvingStarted = true; window.captchaSolvingFinished = false;"))
    elif msg.text == "wuying-captcha-solving-finished":
        captcha_solving_finished = True
        print("setting captchaSolvingFinished = true")
        asyncio.create_task(page.evaluate("window.captchaSolvingFinished = true;"))

page.on("console", handle_console)
```

**Configuration:**

Enable CAPTCHA resolution by setting the appropriate flag during browser initialization:

```python
params = CreateSessionParams(
    image_id="browser_latest",  # Specify the image ID
)
session_result = agent_bay.create(params)

session = session_result.session
browser_option = BrowserOption(
    solve_captchas=True,
)
await session.browser.initialize_async(browser_option)
```

**Usage Tips:**

- Plan for up to 30 seconds processing time per CAPTCHA
- Implement event listeners to track resolution status
- Disable the feature if manual CAPTCHA handling is preferred for your use case

### Ads Blocking