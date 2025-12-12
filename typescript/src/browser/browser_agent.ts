import { Session } from "../session";
import { Browser } from "./browser";
import { BrowserError } from "../exceptions";
import { z, ZodTypeAny } from "zod";
import { zodToJsonSchema } from "zod-to-json-schema";

import { logInfo, logDebug, logWarn } from "../utils/logger";

// Options interfaces
export interface ActOptions {
  action: string;
  timeout?: number;
  variables?: Record<string, string>;
  use_vision?: boolean;
}

export interface ObserveOptions {
  instruction: string;
  use_vision?: boolean;
  selector?: string;
  timeout?: number;
}

export interface ExtractOptions<TSchema extends ZodTypeAny = ZodTypeAny> {
  instruction: string;
  schema: TSchema;
  use_text_extract?: boolean;
  selector?: string;
  use_vision?: boolean;
  timeout?: number;
}

export class ActResult {
  success: boolean;
  message: string;
  constructor(success: boolean, message: string) {
    this.success = success;
    this.message = message;
  }
}

export class ObserveResult {
  selector: string;
  description: string;
  method: string;
  args: Record<string, any>;
  constructor(
    selector: string,
    description: string,
    method: string,
    args: Record<string, any>
  ) {
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

  /** ------------------ NAVIGATE ------------------ **/
  async navigate(url: string): Promise<string> {
    if (!this.browser.isInitialized()) {
      throw new BrowserError(
        "Browser must be initialized before calling navigate."
      );
    }
    try {
      const args: Record<string, any> = { url };
      const response = await this._callMcpTool("page_use_navigate", args);
      if (response.success && response.data) {
        return typeof response.data === "string"
          ? response.data
          : JSON.stringify(response.data);
      }
      return `Navigation failed: ${response.errorMessage || "Unknown error"}`;
    } catch (e: any) {
      throw new BrowserError(`Failed to navigate: ${e}`);
    }
  }

  /** ------------------ SCREENSHOT ------------------ **/
  async screenshot(
    page: any = null,
    full_page = true,
    quality = 80,
    clip?: Record<string, number>,
    timeout?: number
  ): Promise<string> {
    if (!this.browser.isInitialized()) {
      throw new BrowserError(
        "Browser must be initialized before calling screenshot."
      );
    }
    try {
      const [pageId, contextId] = await this._getPageAndContextIndexAsync(page);
      logDebug(`Screenshot page_id: ${pageId}, context_id: ${contextId}`);

      const args: Record<string, any> = {
        context_id: contextId,
        page_id: pageId,
        full_page,
        quality,
        clip,
        timeout,
      };
      Object.keys(args).forEach((k) => {
        if (args[k] === undefined || args[k] === null) delete args[k];
      });

      const response = await this._callMcpTool("page_use_screenshot", args);
      if (response.success && response.data) {
        return typeof response.data === "string"
          ? response.data
          : JSON.stringify(response.data);
      }
      return `Screenshot failed: ${response.errorMessage || "Unknown error"}`;
    } catch (e: any) {
      throw new BrowserError(`Failed to call screenshot: ${e}`);
    }
  }
  /** ------------------ CLOSE ------------------ **/
  async close(): Promise<boolean> {
    try {
      const response = await this._callMcpTool("page_use_close_session", {});
      if (response.success && response.data) {
        logInfo(`Session close status: ${response.data}`);
        return true;
      } else {
        logWarn(
          `Failed to close session: ${response.errorMessage || "Unknown error"}`
        );
        return false;
      }
    } catch (e: any) {
      throw new BrowserError(`Failed to call close: ${e}`);
    }
  }

  /** ------------------ ACT ------------------ **/
  async act(options: ActOptions, page?: any): Promise<ActResult> {
    if (!this.browser.isInitialized())
      throw new BrowserError("Browser must be initialized before calling act.");

    const [pageId, contextId] = await this._getPageAndContextIndexAsync(page);
    logDebug(`Acting page_id: ${pageId}, context_id: ${contextId}`);

    const args: Record<string, any> = {
      context_id: contextId,
      page_id: pageId,
      action: options.action,
      variables: options.variables,
      timeout: options.timeout,
      use_vision: options.use_vision,
    };
    Object.keys(args).forEach((k) => {
      if (args[k] === undefined || args[k] === null) delete args[k];
    });
    const task_name = options.action;
    logInfo(`${task_name}`);

    const response = await this._callMcpTool("page_use_act", args);

    if (response.success && response.data) {
      const msg =
        typeof response.data === "string"
          ? response.data
          : JSON.stringify(response.data);
      logInfo(`${task_name} response data: ${msg}`);
      return new ActResult(true, msg);
    }
    return new ActResult(false, response.errorMessage || "");
  }

  async actAsync(options: ActOptions, page?: any): Promise<ActResult> {
    if (!this.browser.isInitialized())
      throw new BrowserError(
        "Browser must be initialized before calling actAsync."
      );

    const [pageId, contextId] = await this._getPageAndContextIndexAsync(page);
    logDebug(`Acting page_id: ${pageId}, context_id: ${contextId}`);

    const args: Record<string, any> = {
      context_id: contextId,
      page_id: pageId,
      action: options.action,
      variables: options.variables,
      timeout: options.timeout,
      use_vision: options.use_vision,
    };
    Object.keys(args).forEach((k) => {
      if (args[k] === undefined || args[k] === null) delete args[k];
    });
    const task_name = options.action;
    logInfo(`${task_name}`);

    const startResp = await this._callMcpTool("page_use_act_async", args);
    if (!startResp.success) throw new BrowserError("Failed to start act task");

    const { task_id } = JSON.parse(startResp.data);
    const clientTimeout = options.timeout;
    const timeoutS = clientTimeout ?? 300;
    const startTS = Date.now();

    const noActionMsg = "No actions have been executed.";

    while (true) {
      await this._delay(5000);
      const pollResp = await this._callMcpTool("page_use_get_act_result", {
        task_id,
      });

      if (pollResp.success && pollResp.data) {
        const data =
          typeof pollResp.data === "string"
            ? JSON.parse(pollResp.data)
            : pollResp.data;
        const steps = data.steps || [];
        const is_done = data.is_done || false;
        const success = !!data.success;
        if (is_done) {
          const msg = steps.length ? JSON.stringify(steps) : noActionMsg;
          logInfo(
            `Task ${task_id}:${task_name} is done. Success: ${success}. ${msg}`
          );
          return new ActResult(success, msg);
        } else {
          const elapsed = (Date.now() - startTS) / 1000;
          const statusMsg = steps.length
            ? `${steps.length} steps done. Details: ${JSON.stringify(steps)}`
            : noActionMsg;
          logInfo(`Task ${task_id}:${task_name} in progress. ${statusMsg}`);

          if (elapsed >= timeoutS) {
            throw new BrowserError(
              `Task ${task_id}:${task_name} timeout after ${timeoutS}s`
            );
          }
        }
      } else {
        const elapsed = (Date.now() - startTS) / 1000;
        if (elapsed >= timeoutS) {
          throw new BrowserError(
            `Task ${task_id}:${task_name} timeout after ${timeoutS}s`
          );
        }
      }
    }
  }

  /** ------------------ OBSERVE ------------------ **/
  async observe(
    options: ObserveOptions,
    page?: any
  ): Promise<[boolean, ObserveResult[]]> {
    if (!this.browser.isInitialized())
      throw new BrowserError(
        "Browser must be initialized before calling observe."
      );

    const [pageId, contextId] = await this._getPageAndContextIndexAsync(page);
    logDebug(`Observing page_id: ${pageId}, context_id: ${contextId}`);

    const args: Record<string, any> = {
      context_id: contextId,
      page_id: pageId,
      instruction: options.instruction,
      use_vision: options.use_vision,
      selector: options.selector,
    };
    Object.keys(args).forEach((k) => {
      if (args[k] === undefined || args[k] === null) delete args[k];
    });
    const response = await this._callMcpTool("page_use_observe", args);
    if (response.success && response.data) {
      const data =
        typeof response.data === "string"
          ? JSON.parse(response.data)
          : response.data;
      logInfo(`observe results: ${data}`);
      const results: ObserveResult[] = [];

      for (const item of data) {
        let argsParsed: any;
        try {
          argsParsed =
            typeof item.arguments === "string"
              ? JSON.parse(item.arguments)
              : item.arguments;
        } catch {
          logWarn(`Warning: Could not parse arguments JSON: ${item.arguments}`);
          argsParsed = item.arguments;
        }
        results.push(
          new ObserveResult(
            item.selector || "",
            item.description || "",
            item.method || "",
            argsParsed
          )
        );
      }
      return [true, results];
    }
    return [false, []];
  }

  async observeAsync(
    options: ObserveOptions,
    page?: any
  ): Promise<[boolean, ObserveResult[]]> {
    if (!this.browser.isInitialized()) {
      throw new BrowserError(
        "Browser must be initialized before calling observeAsync."
      );
    }

    const [pageId, contextId] = await this._getPageAndContextIndexAsync(page);
    logDebug(`Observing page_id: ${pageId}, context_id: ${contextId}`);

    const args: Record<string, any> = {
      context_id: contextId,
      page_id: pageId,
      instruction: options.instruction,
      use_vision: options.use_vision,
      selector: options.selector,
    };
    Object.keys(args).forEach((k) => {
      if (args[k] === undefined || args[k] === null) delete args[k];
    });
    const startResp = await this._callMcpTool("page_use_observe_async", args);
    if (!startResp.success || !startResp.data) {
      throw new BrowserError("Failed to start observe task");
    }

    const { task_id } =
      typeof startResp.data === "string"
        ? JSON.parse(startResp.data)
        : startResp.data;

    const clientTimeout = options.timeout;
    const timeoutS = clientTimeout ?? 300;
    const startTS = Date.now();

    while (true) {
      await this._delay(5000);
      const pollResp = await this._callMcpTool("page_use_get_observe_result", {
        task_id,
      });

      if (pollResp.success && pollResp.data) {
        const data =
          typeof pollResp.data === "string"
            ? JSON.parse(pollResp.data)
            : pollResp.data;
        logInfo(`observe results: ${JSON.stringify(data)}`);

        const results: ObserveResult[] = [];
        for (const item of data) {
          let argsParsed: any;
          try {
            argsParsed =
              typeof item.arguments === "string"
                ? JSON.parse(item.arguments)
                : item.arguments;
          } catch {
            logWarn(
              `Warning: Could not parse arguments JSON: ${item.arguments}`
            );
            argsParsed = item.arguments;
          }
          results.push(
            new ObserveResult(
              item.selector || "",
              item.description || "",
              item.method || "",
              argsParsed
            )
          );
        }
        return [true, results];
      }

      const elapsed = (Date.now() - startTS) / 1000;
      logDebug(
        `Task ${task_id}: No observe result yet (elapsed=${elapsed.toFixed(0)}s)`
      );
      if (elapsed >= timeoutS) {
        throw new BrowserError(
          `Task ${task_id}: Observe timeout after ${timeoutS}s`
        );
      }
    }
  }

  /** ------------------ EXTRACT ------------------ **/
  async extract<TSchema extends ZodTypeAny>(
    options: ExtractOptions<TSchema>,
    page?: any
  ): Promise<[boolean, z.infer<TSchema> | null]> {
    if (!this.browser.isInitialized())
      throw new BrowserError(
        "Browser must be initialized before calling extract."
      );

    const [pageId, contextId] = await this._getPageAndContextIndexAsync(page);
    logDebug(`Extracting page_id: ${pageId}, context_id: ${contextId}`);

    const jsonSchema = zodToJsonSchema(options.schema, "ExtractSchema");
    const args: Record<string, any> = {
      context_id: contextId,
      page_id: pageId,
      instruction: options.instruction,
      field_schema: `schema: ${JSON.stringify(jsonSchema)}`,
      use_text_extract: options.use_text_extract,
      use_vision: options.use_vision,
      selector: options.selector,
    };
    Object.keys(args).forEach((k) => {
      if (args[k] === undefined || args[k] === null) delete args[k];
    });
    const response = await this._callMcpTool("page_use_extract", args);
    if (response.success && response.data) {
      const raw =
        typeof response.data === "string"
          ? JSON.parse(response.data)
          : response.data;
      const parsed = options.schema.parse(raw) as z.infer<TSchema>;
      return [true, parsed];
    }
    return [false, null];
  }

  async extractAsync<TSchema extends ZodTypeAny>(
    options: ExtractOptions<TSchema>,
    page?: any
  ): Promise<[boolean, z.infer<TSchema> | null]> {
    if (!this.browser.isInitialized())
      throw new BrowserError(
        "Browser must be initialized before calling extractAsync."
      );

    const [pageId, contextId] = await this._getPageAndContextIndexAsync(page);
    logDebug(`Extracting page_id: ${pageId}, context_id: ${contextId}`);

    const jsonSchema = zodToJsonSchema(options.schema, "ExtractSchema");
    const args: Record<string, any> = {
      context_id: contextId,
      page_id: pageId,
      instruction: options.instruction,
      field_schema: `schema: ${JSON.stringify(jsonSchema)}`,
      use_text_extract: options.use_text_extract,
      use_vision: options.use_vision,
      selector: options.selector,
    };
    Object.keys(args).forEach((k) => {
      if (args[k] === undefined || args[k] === null) delete args[k];
    });
    const startResp = await this._callMcpTool("page_use_extract_async", args);
    if (!startResp.success || !startResp.data) {
      throw new BrowserError("Failed to start extract task");
    }

    const { task_id } =
      typeof startResp.data === "string"
        ? JSON.parse(startResp.data)
        : startResp.data;

    const clientTimeout = options.timeout;
    const timeoutS = clientTimeout ?? 300;
    const startTS = Date.now();

    while (true) {
      await this._delay(8000);

      const pollResp = await this._callMcpTool("page_use_get_extract_result", {
        task_id,
      });

      if (pollResp.success && pollResp.data) {
        const raw =
          typeof pollResp.data === "string"
            ? JSON.parse(pollResp.data)
            : pollResp.data;
        const parsed = options.schema.parse(raw) as z.infer<TSchema>;
        return [true, parsed];
      }

      const elapsed = (Date.now() - startTS) / 1000;
      logDebug(
        `Task ${task_id}: No extract result yet (elapsed=${elapsed.toFixed(0)}s)`
      );
      if (elapsed >= timeoutS) {
        throw new BrowserError(
          `Task ${task_id}: Extract timeout after ${timeoutS}s`
        );
      }
    }
  }

  private async _getPageAndContextIndexAsync(
    page: any
  ): Promise<[string | null, number]> {
    if (!page) {
      return [null, 0];
    }

    // Try to use Playwright CDP if available
    try {
      if (page.context && typeof page.context === "function") {
        const context = page.context();
        if (context && typeof context.newCDPSession === "function") {
          const cdpSession = await context.newCDPSession(page);
          const targetInfo = await cdpSession.send("Target.getTargetInfo");
          const pageIndex =
            targetInfo &&
            targetInfo.targetInfo &&
            targetInfo.targetInfo.targetId
              ? targetInfo.targetInfo.targetId
              : null;
          if (typeof cdpSession.detach === "function") {
            await cdpSession.detach();
          }

          let contextIndex = 0;
          if (typeof context.browser === "function") {
            const browserObj = context.browser();
            if (browserObj && typeof browserObj.contexts === "function") {
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
      logWarn(`CDP targetId retrieval failed, fallback to defaults: ${error}`);
    }
    return [null, 0];
  }

  private async _callMcpTool(toolName: string, args: Record<string, any>) {
    return this.session.callMcpTool(toolName, args);
  }

  private _delay(ms: number) {
    return new Promise((res) => setTimeout(res, ms));
  }
}
