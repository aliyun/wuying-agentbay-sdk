import { Session } from '../session';
import { Browser } from './browser';
import { BrowserError } from '../exceptions';
import { log } from '../utils/logger';

// Options interfaces
export interface ActOptions {
  action: string;
  timeoutMS?: number;
  iframes?: boolean;
  domSettleTimeoutMS?: number;
}

export interface ObserveOptions {
  instruction: string;
  returnActions?: number;
  iframes?: boolean;
  domSettleTimeoutMS?: number;
}

export interface ExtractOptions<T = any> {
  instruction: string;
  schema: new (...args: any[]) => T;
  use_text_extract: boolean;
  selector?: string;
  iframe?: boolean;
  domSettleTimeoutsMS?: number;
}

// Result classes
export class ActResult {
  success: boolean;
  message: string;
  action: string;

  constructor(success: boolean, message: string, action: string) {
    this.success = success;
    this.message = message;
    this.action = action;
  }
}

export class ObserveResult {
  selector: string;
  description: string;
  method: string;
  args: Record<string, any>;

  constructor(selector: string, description: string, method: string, args: Record<string, any>) {
    this.selector = selector;
    this.description = description;
    this.method = method;
    this.args = args;
  }
}

export class BrowserAgent {
  private session: Session;
  private browser: Browser;

  constructor(session: Session, browser: Browser) {
    this.session = session;
    this.browser = browser;
  }

  /**
   * Perform an action on the given Playwright Page object, using ActOptions to configure behavior.
   * Returns the result of the action.
   */
  async act(options: ActOptions, page: any): Promise<ActResult> {
    if (!this.browser.isInitialized()) {
      throw new BrowserError("Browser must be initialized before calling act.");
    }

    try {
      const [pageIndex, contextIndex] = await this._getPageAndContextIndexAsync(page);
      log(`Acting on page: ${page}, pageIndex: ${pageIndex}, contextIndex: ${contextIndex}`);

      const args: Record<string, any> = {
        context_id: contextIndex,
        page_id: pageIndex,
        action: options.action,
      };

      if (options.timeoutMS !== undefined) {
        args.timeout_ms = options.timeoutMS;
      }
      if (options.iframes !== undefined) {
        args.iframes = options.iframes;
      }
      if (options.domSettleTimeoutMS !== undefined) {
        args.dom_settle_timeout_ms = options.domSettleTimeoutMS;
      }

      const response = await this._callMcpTool("page_use_act", args);
      
      if (response.success) {
        log(`Response from CallMcpTool - page_use_act:`, response.data);
        
        let data: any;
        if (typeof response.data === 'string') {
          data = JSON.parse(response.data);
        } else {
          data = response.data;
        }

        const success = data.success || false;
        const message = data.message || "";
        const action = data.action || "";

        return new ActResult(success, message, action);
      } else {
        return new ActResult(false, response.errorMessage, "");
      }
    } catch (error) {
      throw new BrowserError(`Failed to get page/context index: ${error}`);
    }
  }

  /**
   * Async version of act method for performing actions on the given Playwright Page object.
   */
  async actAsync(options: ActOptions, page: any): Promise<ActResult> {
    return this.act(options, page);
  }

  /**
   * Observe elements or state on the given Playwright Page object.
   * Returns a tuple containing (success, results).
   */
  async observe(options: ObserveOptions, page: any): Promise<[boolean, ObserveResult[]]> {
    if (!this.browser.isInitialized()) {
      throw new BrowserError("Browser must be initialized before calling observe.");
    }

    try {
      const [pageIndex, contextIndex] = await this._getPageAndContextIndexAsync(page);
      log(`Observing page: ${page}, pageIndex: ${pageIndex}, contextIndex: ${contextIndex}`);

      const args: Record<string, any> = {
        context_id: contextIndex,
        page_id: pageIndex,
        instruction: options.instruction,
      };

      if (options.returnActions !== undefined) {
        args.return_actions = options.returnActions;
      }
      if (options.iframes !== undefined) {
        args.iframes = options.iframes;
      }
      if (options.domSettleTimeoutMS !== undefined) {
        args.dom_settle_timeout_ms = options.domSettleTimeoutMS;
      }

      const response = await this._callMcpTool("page_use_observe", args);
      log("Response from CallMcpTool - page_use_observe data:", response.data);

      if (response.success) {
        log(`Response from CallMcpTool - page_use_observe:`, response.data);
        
        let data: any;
        if (typeof response.data === 'string') {
          data = JSON.parse(response.data);
        } else {
          throw new BrowserError("Observe response data is not a json!!!");
        }

        const success = data.success || false;
        if (!success) {
          return [false, []];
        }

        const results: ObserveResult[] = [];
        const observeResults = JSON.parse(data.observe_result || "");
        log("observeResults =", observeResults);

        for (const item of observeResults) {
          const selector = item.selector || "";
          const description = item.description || "";
          const method = item.method || "";
          const itemArgs = item.arguments || {};
          results.push(new ObserveResult(selector, description, method, itemArgs));
        }

        return [success, results];
      } else {
        log(`Response from CallMcpTool - page_use_observe:`, response.errorMessage);
        return [false, []];
      }
    } catch (error) {
      throw new BrowserError(`Failed to get page/context index: ${error}`);
    }
  }

  /**
   * Async version of observe method.
   */
  async observeAsync(options: ObserveOptions, page: any): Promise<[boolean, ObserveResult[]]> {
    return this.observe(options, page);
  }

  /**
   * Extract information from the given Playwright Page object.
   */
  async extract<T>(options: ExtractOptions<T>, page: any): Promise<[boolean, T[]]> {
    if (!this.browser.isInitialized()) {
      throw new BrowserError("Browser must be initialized before calling extract.");
    }

    try {
      const [pageIndex, contextIndex] = await this._getPageAndContextIndexAsync(page);
      
      // Create a temporary instance to get the schema
      const tempInstance = new options.schema();
      const schema = (tempInstance as any).constructor.name; // This is a simplified approach

      const args: Record<string, any> = {
        context_id: contextIndex,
        page_id: pageIndex,
        instruction: options.instruction,
        schema: `schema: ${JSON.stringify(schema)}` // Simplified schema handling
      };

      log(`Extracting from page: ${page}, pageIndex: ${pageIndex}, contextIndex: ${contextIndex}, args:`, args);

      if (options.selector !== undefined) {
        args.selector = options.selector;
      }
      if (options.iframe !== undefined) {
        args.iframe = options.iframe;
      }
      if (options.domSettleTimeoutsMS !== undefined) {
        args.dom_settle_timeouts_ms = options.domSettleTimeoutsMS;
      }

      const response = await this._callMcpTool("page_use_extract", args);
      log("Response from CallMcpTool - page_use_extract data:", response.data);

      if (response.success) {
        log(`Response from CallMcpTool - page_use_extract:`, response.data);
        
        let data: any;
        if (typeof response.data === 'string') {
          data = JSON.parse(response.data);
        } else {
          data = response.data;
        }

        log("extract data =", data);
        const success = data.success || false;
        const extractObjs: T[] = [];

        if (success) {
          const extractResults = JSON.parse(data.extract_result || "");
          for (const extractResult of extractResults) {
            log("extractResult =", extractResult);
            // Create instance from the constructor - simplified approach
            const instance = extractResult as T;
            extractObjs.push(instance);
          }
        } else {
          const extractResults = data.extract_result || "";
          log("Extract failed due to:", extractResults);
        }

        return [success, extractObjs];
      } else {
        log(`Response from CallMcpTool - page_use_extract:`, response.errorMessage);
        return [false, []];
      }
    } catch (error) {
      throw new BrowserError(`Failed to get page/context index: ${error}`);
    }
  }

  /**
   * Async version of extract method.
   */
  async extractAsync<T>(options: ExtractOptions<T>, page: any): Promise<[boolean, T[]]> {
    return this.extract<T>(options, page);
  }

  private _getPageAndContextIndex(page: any): [string, number] {
    if (!page) {
      throw new BrowserError("Page is null");
    }

    try {
      // Fallback implementation - prefer async version where CDP is available
      const pageIndex = "default-page-id";
      const contextIndex = 0;
      return [pageIndex, contextIndex];
    } catch (error) {
      throw new BrowserError(`Failed to get page/context index: ${error}`);
    }
  }

  private async _getPageAndContextIndexAsync(page: any): Promise<[string, number]> {
    if (!page) {
      throw new BrowserError("Page is null");
    }

    // Try to use Playwright CDP if available
    try {
      if (page.context && typeof page.context === 'function') {
        const context = page.context();
        if (context && typeof context.newCDPSession === 'function') {
          const cdpSession = await context.newCDPSession(page);
          const targetInfo = await cdpSession.send('Target.getTargetInfo');
          const pageIndex = (targetInfo && targetInfo.targetInfo && targetInfo.targetInfo.targetId) ? targetInfo.targetInfo.targetId : 'default-page-id';
          if (typeof cdpSession.detach === 'function') {
            await cdpSession.detach();
          }

          let contextIndex = 0;
          if (typeof context.browser === 'function') {
            const browserObj = context.browser();
            if (browserObj && typeof browserObj.contexts === 'function') {
              const contexts = browserObj.contexts();
              const idx = contexts.indexOf(context);
              if (idx >= 0) {
                contextIndex = idx;
              }
            }
          }
          return [pageIndex, contextIndex];
        }
      }
    } catch (error) {
      log(`CDP targetId retrieval failed, fallback to defaults: ${error}`);
    }

    // Fallback to defaults if CDP is not available
    const pageIndex = "default-page-id";
    const contextIndex = 0;
    return [pageIndex, contextIndex];
  }

  private async _callMcpTool(toolName: string, args: Record<string, any>) {
    return this.session.callMcpTool(toolName, args);
  }
} 