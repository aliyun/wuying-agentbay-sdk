import { Session } from '../session';
import { BrowserAgent } from './browser_agent';
import { BrowserError } from '../exceptions';
import { InitBrowserRequest } from '../api/models/InitBrowserRequest';
import { FingerprintFormat } from './fingerprint';

// Browser data path constant (moved from config.ts)
const BROWSER_DATA_PATH = "/tmp/agentbay_browser";
// Browser fingerprint persistent path constant (moved from config.ts)
const BROWSER_FINGERPRINT_PERSIST_PATH = "/tmp/browser_fingerprint";
import {
  log,
  logError,
  logInfo,
  logDebug,
  logAPICall,
  logAPIResponseWithDetails,
  setRequestId,
} from '../utils/logger';

export interface BrowserViewport {
  width: number;
  height: number;
}

export interface BrowserScreen {
  width: number;
  height: number;
}

export interface BrowserFingerprint {
  devices?: Array<'desktop' | 'mobile'>;
  operatingSystems?: Array<'windows' | 'macos' | 'linux' | 'android' | 'ios'>;
  locales?: string[];
}

/**
 * Browser fingerprint context configuration.
 */
export class BrowserFingerprintContext {
  /** ID of the fingerprint context for browser fingerprint */
  fingerprintContextId: string;

  /**
   * Initialize BrowserFingerprintContext with context id.
   * 
   * @param fingerprintContextId - ID of the fingerprint context for browser fingerprint.
   * 
   * @throws {Error} If fingerprintContextId is empty.
   */
  constructor(fingerprintContextId: string) {
    if (!fingerprintContextId || !fingerprintContextId.trim()) {
      throw new Error("fingerprintContextId cannot be empty");
    }

    this.fingerprintContextId = fingerprintContextId;
  }
}

export interface BrowserProxy {
  type: 'custom' | 'wuying';
  server?: string;
  username?: string;
  password?: string;
  strategy?: 'restricted' | 'polling';
  pollsize?: number;
  toMap(): Record<string, any>;
}

export class BrowserProxyClass implements BrowserProxy {
  type: 'custom' | 'wuying';
  server?: string;
  username?: string;
  password?: string;
  strategy?: 'restricted' | 'polling';
  pollsize?: number;

  constructor(
    proxyType: 'custom' | 'wuying',
    server?: string,
    username?: string,
    password?: string,
    strategy?: 'restricted' | 'polling',
    pollsize?: number
  ) {
    this.type = proxyType;
    this.server = server;
    this.username = username;
    this.password = password;
    this.strategy = strategy;
    this.pollsize = pollsize;

    // Validation
    if (proxyType !== 'custom' && proxyType !== 'wuying') {
      throw new Error('proxy_type must be custom or wuying');
    }

    if (proxyType === 'custom' && !server) {
      throw new Error('server is required for custom proxy type');
    }

    if (proxyType === 'wuying' && !strategy) {
      throw new Error('strategy is required for wuying proxy type');
    }

    if (proxyType === 'wuying' && strategy !== 'restricted' && strategy !== 'polling') {
      throw new Error('strategy must be restricted or polling for wuying proxy type');
    }

    if (proxyType === 'wuying' && strategy === 'polling' && pollsize !== undefined && pollsize <= 0) {
      throw new Error('pollsize must be greater than 0 for polling strategy');
    }
  }

  toMap(): Record<string, any> {
    const proxyMap: Record<string, any> = {
      type: this.type
    };

    if (this.type === 'custom') {
      proxyMap.server = this.server;
      if (this.username) {
        proxyMap.username = this.username;
      }
      if (this.password) {
        proxyMap.password = this.password;
      }
    } else if (this.type === 'wuying') {
      proxyMap.strategy = this.strategy;
      if (this.strategy === 'polling') {
        proxyMap.pollsize = this.pollsize;
      }
    }

    return proxyMap;
  }

  static fromMap(m: Record<string, any> | null | undefined): BrowserProxyClass | null {
    if (!m || typeof m !== 'object') {
      return null;
    }

    const proxyType = m.type;
    if (!proxyType) {
      return null;
    }

    if (proxyType === 'custom') {
      return new BrowserProxyClass(
        proxyType,
        m.server,
        m.username,
        m.password
      );
    } else if (proxyType === 'wuying') {
      return new BrowserProxyClass(
        proxyType,
        undefined,
        undefined,
        undefined,
        m.strategy,
        m.pollsize || 10
      );
    } else {
      throw new Error(`Unsupported proxy type: ${proxyType}`);
    }
  }
}

export interface BrowserOption {
  persistentPath?: string;
  useStealth?: boolean;
  userAgent?: string;
  viewport?: BrowserViewport;
  screen?: BrowserScreen;
  fingerprint?: BrowserFingerprint;
  /** Browser fingerprint format data for detailed fingerprint configuration */
  fingerprintFormat?: FingerprintFormat;
  /** Whether to enable fingerprint persistence across sessions */
  fingerprintPersistent?: boolean;
  solveCaptchas?: boolean;
  proxies?: BrowserProxy[];
  /** Path to the extensions directory. Defaults to "/tmp/extensions/" */
  extensionPath?: string;
  /** Additional command line arguments for the browser */
  cmdArgs?: string[];
  /** Default URL to navigate to when browser starts */
  defaultNavigateUrl?: string;
  /** Browser type: 'chrome' or 'chromium'. Defaults to undefined */
  browserType?: 'chrome' | 'chromium' | undefined;
}

export class BrowserOptionClass implements BrowserOption {
  persistentPath?: string;
  useStealth?: boolean;
  userAgent?: string;
  viewport?: BrowserViewport;
  screen?: BrowserScreen;
  fingerprint?: BrowserFingerprint;
  fingerprintFormat?: FingerprintFormat;
  fingerprintPersistent?: boolean;
  fingerprintPersistPath?: string;
  solveCaptchas?: boolean;
  proxies?: BrowserProxy[];
  extensionPath?: string;
  cmdArgs?: string[];
  defaultNavigateUrl?: string;
  browserType?: 'chrome' | 'chromium' | undefined;

  constructor(
    useStealth = false,
    userAgent?: string,
    viewport?: BrowserViewport,
    screen?: BrowserScreen,
    fingerprint?: BrowserFingerprint,
    fingerprintFormat?: FingerprintFormat,
    fingerprintPersistent = false,
    solveCaptchas = false,
    proxies?: BrowserProxy[],
    cmdArgs?: string[],
    defaultNavigateUrl?: string,
    browserType?: 'chrome' | 'chromium',
  ) {
    this.useStealth = useStealth;
    this.userAgent = userAgent;
    this.viewport = viewport;
    this.screen = screen;
    this.fingerprint = fingerprint;
    this.fingerprintFormat = fingerprintFormat;
    this.fingerprintPersistent = fingerprintPersistent;
    this.solveCaptchas = solveCaptchas;
    this.extensionPath = "/tmp/extensions/";
    this.cmdArgs = cmdArgs;
    this.defaultNavigateUrl = defaultNavigateUrl;
    this.browserType = browserType;

    // Check fingerprint persistent if provided
    if (fingerprintPersistent) {
      // Currently only support persistent fingerprint in docker env
      this.fingerprintPersistPath = `${BROWSER_FINGERPRINT_PERSIST_PATH}/fingerprint.json`;
    } else {
      this.fingerprintPersistPath = undefined;
    }

    // Validate proxies list items
    if (proxies !== undefined) {
      if (!Array.isArray(proxies)) {
        throw new Error('proxies must be a list');
      }
      if (proxies.length > 1) {
        throw new Error('proxies list length must be limited to 1');
      }
    }

    // Set proxies after validation
    this.proxies = proxies;

    // Validate cmdArgs
    if (cmdArgs !== undefined && !Array.isArray(cmdArgs)) {
      throw new Error('cmdArgs must be a list');
    }

    // Validate browser_type
    if (browserType !== undefined && browserType !== 'chrome' && browserType !== 'chromium') {
      throw new Error("browserType must be 'chrome' or 'chromium'");
    }
  }

  toMap(): Record<string, any> {
    const optionMap: Record<string, any> = {};
    if (process.env.AGENTBAY_BROWSER_BEHAVIOR_SIMULATE) {
      optionMap['behaviorSimulate'] = (process.env.AGENTBAY_BROWSER_BEHAVIOR_SIMULATE !== "0") as boolean;
    }
    if (this.useStealth !== undefined) {
      optionMap['useStealth'] = this.useStealth;
    }
    if (this.userAgent !== undefined) {
      optionMap['userAgent'] = this.userAgent;
    }
    if (this.viewport !== undefined) {
      optionMap['viewport'] = { width: this.viewport.width, height: this.viewport.height };
    }
    if (this.screen !== undefined) {
      optionMap['screen'] = { width: this.screen.width, height: this.screen.height };
    }
    if (this.fingerprint !== undefined) {
      const fp: Record<string, any> = {};
      if (this.fingerprint.devices) fp['devices'] = this.fingerprint.devices;
      if (this.fingerprint.operatingSystems) fp['operatingSystems'] = this.fingerprint.operatingSystems;
      if (this.fingerprint.locales) fp['locales'] = this.fingerprint.locales;
      optionMap['fingerprint'] = fp;
    }
    if (this.fingerprintFormat !== undefined) {
      // Encode fingerprint format to base64 string
      try {
        const jsonStr = this.fingerprintFormat.toJson();
        optionMap['fingerprintRawData'] = Buffer.from(jsonStr, 'utf-8').toString('base64');
      } catch (error) {
        logError('Failed to serialize fingerprint format:', error);
        // Skip fingerprint format if serialization fails
      }
    }
    if (this.fingerprintPersistent) {
      this.fingerprintPersistPath = `${BROWSER_FINGERPRINT_PERSIST_PATH}/fingerprint.json`;
      optionMap['fingerprintPersistPath'] = this.fingerprintPersistPath;
    }
    if (this.solveCaptchas !== undefined) {
      optionMap['solveCaptchas'] = this.solveCaptchas;
    }
    if (this.proxies !== undefined) {
      optionMap['proxies'] = this.proxies.map(proxy => proxy.toMap());
    }
    if (this.extensionPath !== undefined) {
      optionMap['extensionPath'] = this.extensionPath;
    }
    if (this.cmdArgs !== undefined) {
      optionMap['cmdArgs'] = this.cmdArgs;
    }
    if (this.defaultNavigateUrl !== undefined) {
      optionMap['defaultNavigateUrl'] = this.defaultNavigateUrl;
    }
    if (this.browserType !== undefined) {
      optionMap['browserType'] = this.browserType;
    }
    return optionMap;
  }

  fromMap(m: Record<string, any> | null | undefined): BrowserOptionClass {
    const map = m || {};
    if (map.useStealth !== undefined) {
      this.useStealth = map.useStealth;
    } else {
      this.useStealth = false;
    }
    if (map.userAgent !== undefined) {
      this.userAgent = map.userAgent;
    }
    if (map.viewport !== undefined) {
      this.viewport = { width: map.viewport.width, height: map.viewport.height };
    }
    if (map.screen !== undefined) {
      this.screen = { width: map.screen.width, height: map.screen.height };
    }
    if (map.fingerprint !== undefined) {
      const fp: BrowserFingerprint = {};
      if (map.fingerprint.devices) fp.devices = map.fingerprint.devices;
      if (map.fingerprint.operatingSystems) fp.operatingSystems = map.fingerprint.operatingSystems;
      if (map.fingerprint.locales) fp.locales = map.fingerprint.locales;
      this.fingerprint = fp;
    }
    if (map.fingerprintFormat !== undefined) {
      // Handle direct FingerprintFormat object
      if (map.fingerprintFormat instanceof FingerprintFormat) {
        this.fingerprintFormat = map.fingerprintFormat;
      } else {
        // Convert from plain object to FingerprintFormat
        try {
          this.fingerprintFormat = FingerprintFormat.fromDict(map.fingerprintFormat);
        } catch (error) {
          logError('Failed to convert fingerprintFormat from object:', error);
          this.fingerprintFormat = undefined;
        }
      }
    } else if (map.fingerprintRawData !== undefined) {
      // Decode base64 string to fingerprint format
      try {
        const jsonStr = Buffer.from(map.fingerprintRawData, 'base64').toString('utf-8');
        this.fingerprintFormat = FingerprintFormat.fromJson(jsonStr);
      } catch (error) {
        logError('Failed to decode fingerprint raw data:', error);
        this.fingerprintFormat = undefined;
      }
    }
    if (map.fingerprintPersistent !== undefined) {
      this.fingerprintPersistent = map.fingerprintPersistent;
    } else if (map.fingerprintPersistPath !== undefined) {
      this.fingerprintPersistPath = map.fingerprintPersistPath;
      this.fingerprintPersistent = true;
    } else {
      this.fingerprintPersistent = false;
    }
    if (map.solveCaptchas !== undefined) {
      this.solveCaptchas = map.solveCaptchas;
    }
    if (map.proxies !== undefined) {
      const proxyList = map.proxies;
      if (proxyList.length > 1) {
        throw new Error('proxies list length must be limited to 1');
      }
      this.proxies = proxyList.map((proxyData: any) => {
        // If it's already a BrowserProxyClass instance, return it
        if (proxyData instanceof BrowserProxyClass) {
          return proxyData;
        }
        // Otherwise, convert from map
        return BrowserProxyClass.fromMap(proxyData);
      }).filter(Boolean) as BrowserProxy[];
    }
    if (map.extensionPath !== undefined) {
      this.extensionPath = map.extensionPath;
    }
    if (map.cmdArgs !== undefined) {
      this.cmdArgs = map.cmdArgs;
    }
    if (map.defaultNavigateUrl !== undefined) {
      this.defaultNavigateUrl = map.defaultNavigateUrl;
    }
    if (map.browserType !== undefined) {
      this.browserType = map.browserType;
    }
    return this;
  }
}

export class Browser {
  private session: Session;
  private _endpointUrl: string | null = null;
  private _initialized = false;
  private _option: BrowserOptionClass | null = null;
  public agent: BrowserAgent;

  constructor(session: Session) {
    this.session = session;
    this.agent = new BrowserAgent(this.session, this);
  }

  /**
   * Initialize the browser instance with the given options.
   * Returns true if successful, false otherwise.
   */
  initialize(option: BrowserOptionClass | BrowserOption): boolean {
    if (this.isInitialized()) {
      return true;
    }

    try {
      logDebug(`Initializing browser with option: ${JSON.stringify(option)}`);
      // Use direct API call to initialize browser
      const request = new InitBrowserRequest();
      request.authorization = `Bearer ${this.session.getAPIKey()}`;
      request.persistentPath = BROWSER_DATA_PATH;
      request.sessionId = this.session.getSessionId();

      // Ensure option is a BrowserOptionClass instance
      let browserOption: BrowserOptionClass;
      if (option instanceof BrowserOptionClass) {
        browserOption = option;
      } else {
        // Convert plain object to BrowserOptionClass instance
        browserOption = new BrowserOptionClass();
        browserOption.fromMap(option as Record<string, any>);
      }

      // Map BrowserOption to API BrowserOption payload
      const browserOptionMap = browserOption.toMap();

      // Enable record if session.enableBrowserReplay is true
      if (this.session.enableBrowserReplay) {
        browserOptionMap['enableRecord'] = true;
      }

      if (Object.keys(browserOptionMap).length > 0) {
        request.browserOption = browserOptionMap;
      }

      const response = this.session.getClient().initBrowserSync(request);
      logDebug(`Response from init_browser data:`, response.body?.data);

      const success = response.body?.data?.port !== null && response.body?.data?.port !== undefined;
      if (success) {
        this._initialized = true;
        this._option = browserOption;
        logInfo("Browser instance was successfully initialized.");
      }

      return success;
    } catch (error) {
      console.error("Failed to initialize browser instance:", error);
      this._initialized = false;
      this._endpointUrl = null;
      this._option = null;
      return false;
    }
  }

  /**
   * Initialize the browser instance with the given options asynchronously.
   * Returns true if successful, false otherwise.
   *
   * @param option - Browser configuration options
   * @returns Promise resolving to true if successful, false otherwise
   *
   * @example
   * ```typescript
   * const agentBay = new AgentBay({ apiKey: process.env.AGENTBAY_API_KEY });
   * const result = await agentBay.create({ imageId: 'browser_latest' });
   * if (result.success) {
   *   const success = await result.session.browser.initializeAsync(new BrowserOptionClass());
   *   console.log('Browser initialized:', success);
   *   await result.session.delete();
   * }
   * ```
   */
  async initializeAsync(option: BrowserOptionClass | BrowserOption): Promise<boolean> {
    if (this.isInitialized()) {
      return true;
    }

    try {
      logDebug(`Initializing browser asynchronously with option: ${JSON.stringify(option)}`);
      // Use direct API call to initialize browser
      const request = new InitBrowserRequest();
      request.authorization = `Bearer ${this.session.getAPIKey()}`;
      request.persistentPath = BROWSER_DATA_PATH;
      request.sessionId = this.session.getSessionId();

      // Ensure option is a BrowserOptionClass instance
      let browserOption: BrowserOptionClass;
      if (option instanceof BrowserOptionClass) {
        browserOption = option;
      } else {
        // Convert plain object to BrowserOptionClass instance
        browserOption = new BrowserOptionClass();
        browserOption.fromMap(option as Record<string, any>);
      }

      // Map BrowserOption to API BrowserOption payload
      const browserOptionMap = browserOption.toMap();

      // Enable record if session.enableBrowserReplay is true
      if (this.session.enableBrowserReplay) {
        browserOptionMap['enableRecord'] = true;
      }

      if (Object.keys(browserOptionMap).length > 0) {
        request.browserOption = browserOptionMap;
      }

      const response = await this.session.getClient().initBrowser(request);
      const requestId = response.body?.requestId || "";
      setRequestId(requestId);

      const success = response.body?.data?.port !== null && response.body?.data?.port !== undefined;
      if (success) {
        logAPIResponseWithDetails(
          "InitBrowser",
          requestId,
          true,
          {
            port: response.body?.data?.port,
            endpoint: response.body?.data?.endpoint,
          }
        );
        this._initialized = true;
        this._option = browserOption;
      } else {
        logAPIResponseWithDetails(
          "InitBrowser",
          requestId,
          false,
          {},
          "Port not found in response"
        );
      }

      return success;
    } catch (error) {
      logError("Failed to initialize browser instance:", error);
      this._initialized = false;
      this._endpointUrl = null;
      this._option = null;
      return false;
    }
  }

  /**
   * Destroy the browser instance.
   */
  async destroy(): Promise<void> {
    if (this.isInitialized()) {
      await this.session.callMcpTool("stopChrome", {});
    } else {
      throw new BrowserError("Browser is not initialized. Cannot destroy browser.");
    }
  }

  /**
   * Returns the endpoint URL if the browser is initialized, otherwise throws an exception.
   * When initialized, always fetches the latest CDP url from session.getLink().
   *
   * @returns Promise resolving to the CDP endpoint URL
   * @throws {BrowserError} If browser is not initialized
   *
   * @example
   * ```typescript
   * const agentBay = new AgentBay({ apiKey: process.env.AGENTBAY_API_KEY });
   * const result = await agentBay.create({ imageId: 'browser_latest' });
   * if (result.success) {
   *   await result.session.browser.initializeAsync(new BrowserOptionClass());
   *   const endpointUrl = await result.session.browser.getEndpointUrl();
   *   const browser = await chromium.connectOverCDP(endpointUrl);
   *   await browser.close();
   *   await result.session.delete();
   * }
   * ```
   */
  async getEndpointUrl(): Promise<string> {
    if (!this.isInitialized()) {
      throw new BrowserError("Browser is not initialized. Cannot access endpoint URL.");
    }

    try {
      if (this.session.isVpc) {
        logDebug(`VPC mode, endpoint_router_port: ${this.session.httpPort}`);
        this._endpointUrl = `ws://${this.session.networkInterfaceIp}:${this.session.httpPort}`;
      } else {
        const { GetCdpLinkRequest } = await import('../api/models/model');
        const request = new GetCdpLinkRequest({
          authorization: `Bearer ${this.session.getAPIKey()}`,
          sessionId: this.session.sessionId
        });
        const response = await this.session.getAgentBay().getClient().getCdpLink(request);
        if (response.body && response.body.success && response.body.data) {
          this._endpointUrl = response.body.data.url || null;
        } else {
          const errorMsg = response.body?.message || "Unknown error";
          throw new BrowserError(`Failed to get CDP link: ${errorMsg}`);
        }
      }
      return this._endpointUrl!;
    } catch (error) {
      throw new BrowserError(`Failed to get endpoint URL from session: ${error}`);
    }
  }

  /**
   * Returns the current BrowserOption used to initialize the browser, or null if not set.
   */
  getOption(): BrowserOptionClass | null {
    return this._option;
  }

  /**
   * Returns true if the browser was initialized, false otherwise.
   */
  isInitialized(): boolean {
    return this._initialized;
  }

  /**
   * Stop the browser instance, internal use only.
   */
  private _stopBrowser(): void {
    if (this.isInitialized()) {
      this.session.callMcpTool("stopChrome", {});
    } else {
      throw new BrowserError("Browser is not initialized. Cannot stop browser.");
    }
  }

  /**
   * Takes a screenshot of the specified page with enhanced options and error handling.
   * This method requires the caller to connect to the browser via Playwright or similar
   * and pass the page object to this method.
   *
   * Note: This is a placeholder method that indicates where screenshot functionality
   * should be implemented. In a complete implementation, this would use Playwright's
   * page.screenshot() method or similar browser automation API.
   *
   * @param page The Playwright Page object to take a screenshot of. This is a required parameter.
   * @param fullPage Whether to capture the full scrollable page. Defaults to false.
   * @param options Additional screenshot options that will override defaults.
   *                Common options include:
   *                - type: Image type, either 'png' or 'jpeg' (default: 'png')
   *                - quality: Quality of the image, between 0-100 (jpeg only)
   *                - timeout: Maximum time in milliseconds (default: 60000)
   *                - animations: How to handle animations (default: 'disabled')
   *                - caret: How to handle the caret (default: 'hide')
   *                - scale: Scale setting (default: 'css')
   * @returns Screenshot data as Uint8Array.
   * @throws BrowserError If browser is not initialized.
   * @throws Error If screenshot capture fails.
   *
   * @example
   * ```typescript
   * const agentBay = new AgentBay({ apiKey: process.env.AGENTBAY_API_KEY });
   * const result = await agentBay.create({ imageId: 'browser_latest' });
   * if (result.success) {
   *   await result.session.browser.initializeAsync(new BrowserOptionClass());
   *   const browser = await chromium.connectOverCDP(await result.session.browser.getEndpointUrl());
   *   const page = await browser.contexts()[0].newPage();
   *   await page.goto('https://example.com');
   *   const screenshot = await result.session.browser.screenshot(page);
   *   await writeFile('screenshot.png', Buffer.from(screenshot));
   *   await browser.close();
   *   await result.session.delete();
   * }
   * ```
   */
  async screenshot(page: any, fullPage = false, options: Record<string, any> = {}): Promise<Uint8Array> {
    // Check if browser is initialized
    if (!this.isInitialized()) {
      throw new BrowserError("Browser must be initialized before calling screenshot.");
    }

    if (page === null || page === undefined) {
      throw new Error("Page cannot be null or undefined");
    }

    // Set default enhanced options
    const enhancedOptions: Record<string, any> = {
      animations: "disabled",
      caret: "hide",
      scale: "css",
      timeout: options.timeout || 60000,
      fullPage: fullPage, // Use the function parameter, not options
      type: options.type || "png",
    };

    // Update with user-provided options (but fullPage is already set from function parameter)
    Object.assign(enhancedOptions, options);

    try {
      // Wait for page to load
      // await page.waitForLoadState("networkidle");
      await page.evaluate("window.scrollTo(0, document.body.scrollHeight)");
      await page.waitForLoadState("domcontentloaded");

      // Scroll to load all content (especially for lazy-loaded elements)
      await this._scrollToLoadAllContent(page);

      // Ensure images with data-src attributes are loaded
      await page.evaluate(`
        () => {
          document.querySelectorAll('img[data-src]').forEach(img => {
            if (!img.src && img.dataset.src) {
              img.src = img.dataset.src;
            }
          });
          // Also handle background-image[data-bg]
          document.querySelectorAll('[data-bg]').forEach(el => {
            if (!el.style.backgroundImage) {
              el.style.backgroundImage = \`url(\${el.dataset.bg})\`;
            }
          });
        }
      `);

      // Wait a bit for images to load
      await page.waitForTimeout(1500);
      const finalHeight = await page.evaluate("document.body.scrollHeight");
      await page.setViewportSize({ width: 1920, height: Math.min(finalHeight, 10000) });

      // Take the screenshot
      const screenshotBuffer = await page.screenshot(enhancedOptions);
      logInfo("Screenshot captured successfully.");
      
      // Convert Buffer to Uint8Array
      return new Uint8Array(screenshotBuffer);
    } catch (error) {
      // Convert error to string safely to avoid comparison issues
      let errorStr: string;
      try {
        errorStr = String(error);
      } catch {
        errorStr = "Unknown error occurred";
      }
      const errorMsg = `Failed to capture screenshot: ${errorStr}`;
      throw new Error(errorMsg);
    }
  }

  /**
   * Scrolls the page to load all content (especially for lazy-loaded elements)
   */
  private async _scrollToLoadAllContent(page: any, maxScrolls = 8, delayMs = 1200): Promise<void> {
    let lastHeight = 0;
    for (let i = 0; i < maxScrolls; i++) {
      await page.evaluate("window.scrollTo(0, document.body.scrollHeight)");
      await page.waitForTimeout(delayMs);
      const newHeight = await page.evaluate("Math.max(document.body.scrollHeight, document.documentElement.scrollHeight)");
      if (newHeight === lastHeight) {
        break;
      }
      lastHeight = newHeight;
    }
  }
}
