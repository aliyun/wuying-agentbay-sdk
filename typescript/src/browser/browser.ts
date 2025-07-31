import { Session } from '../session';
import { BrowserAgent } from './browser_agent';
import { BrowserError } from '../exceptions';
import { BROWSER_DATA_PATH } from '../config';
import { InitBrowserRequest } from '../api/models/InitBrowserRequest';
import { log } from '../utils/logger';

export interface BrowserOption {
  persistentPath?: string;
}

export class Browser {
  private session: Session;
  private _endpointUrl: string | null = null;
  private _initialized = false;
  private _option: BrowserOption | null = null;
  public agent: BrowserAgent;

  constructor(session: Session) {
    this.session = session;
    this.agent = new BrowserAgent(this.session, this);
  }

  /**
   * Initialize the browser instance with the given options.
   * Returns true if successful, false otherwise.
   */
  initialize(option: BrowserOption): boolean {
    if (this.isInitialized()) {
      return true;
    }

    try {
      // Use direct API call to initialize browser
      const request = new InitBrowserRequest();
      request.authorization = `Bearer ${this.session.getAPIKey()}`;
      request.persistentPath = BROWSER_DATA_PATH;
      request.sessionId = this.session.getSessionId();
      const response = this.session.getClient().initBrowserSync(request);
      log(`Response from init_browser data:`, response.body?.data);
      
      const success = response.body?.data?.port !== null && response.body?.data?.port !== undefined;
      if (success) {
        this._initialized = true;
        this._option = option;
        log("Browser instance was successfully initialized.");
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
   */
  async initializeAsync(option: BrowserOption): Promise<boolean> {
    if (this.isInitialized()) {
      return true;
    }

    try {
      // Use direct API call to initialize browser
      const request = new InitBrowserRequest();
      request.authorization = `Bearer ${this.session.getAPIKey()}`;
      request.persistentPath = BROWSER_DATA_PATH;
      request.sessionId = this.session.getSessionId();
      const response = await this.session.getClient().initBrowser(request);
      log(`Response from init_browser data:`, response.body?.data);
      
      const success = response.body?.data?.port !== null && response.body?.data?.port !== undefined;
      if (success) {
        this._initialized = true;
        this._option = option;
        log("Browser instance successfully initialized");
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
   * Returns the endpoint URL if the browser is initialized, otherwise throws an exception.
   * When initialized, always fetches the latest CDP url from session.getLink().
   */
  async getEndpointUrl(): Promise<string> {
    if (!this.isInitialized()) {
      throw new BrowserError("Browser is not initialized. Cannot access endpoint URL.");
    }

    try {
      const linkResult = await this.session.getLink();
      this._endpointUrl = linkResult.data;
      return this._endpointUrl!;
    } catch (error) {
      throw new BrowserError(`Failed to get endpoint URL from session: ${error}`);
    }
  }

  /**
   * Returns the current BrowserOption used to initialize the browser, or null if not set.
   */
  getOption(): BrowserOption | null {
    return this._option;
  }

  /**
   * Returns true if the browser was initialized, false otherwise.
   */
  isInitialized(): boolean {
    return this._initialized;
  }
} 