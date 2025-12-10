import {
  CodeExecutionResult,
  CodeExecutionResultItem,
  CodeExecutionLogs,
  CodeExecutionError,
} from "../types/api-response";

/**
 * Handles code execution operations in the AgentBay cloud environment.
 */
export class Code {
  private session: {
    getAPIKey(): string;
    getSessionId(): string;
    callMcpTool(toolName: string, args: any): Promise<{
      success: boolean;
      data: string;
      errorMessage: string;
      requestId: string;
    }>;
  };

  /**
   * Initialize a Code object.
   *
   * @param session - The Session instance that this Code belongs to.
   */
  constructor(session: {
    getAPIKey(): string;
    getSessionId(): string;
    callMcpTool(toolName: string, args: any): Promise<{
      success: boolean;
      data: string;
      errorMessage: string;
      requestId: string;
    }>;
  }) {
    this.session = session;
  }

  /**
   * Parses the backend JSON response into a structured CodeExecutionResult
   * @param data Raw JSON string from backend
   */
  private parseBackendResponse(data: string): CodeExecutionResult {
    let raw: any;
    try {
      raw = JSON.parse(data);
      // Handle double-encoded JSON if necessary
      if (typeof raw === 'string') {
        try {
          raw = JSON.parse(raw);
        } catch (e) {
          // If second parse fails, keep as string (legacy output)
        }
      }
    } catch (e) {
      // Not JSON, assume legacy plain string result or simple error message
      return {
        requestId: "", // Will be filled later
        success: true,
        result: data,
        logs: { stdout: [data], stderr: [] },
        results: [{ text: data, isMainResult: true }],
      };
    }

    // Check if it's the expected structure (has result array or logs)
    // If parsed but not the structure we want, treat as plain object result?
    // But usually if it parses as object, it's likely our structure or empty object.
    
    const logs: CodeExecutionLogs = {
      stdout: raw.stdout || [],
      stderr: raw.stderr || [],
    };

    const results: CodeExecutionResultItem[] = [];
    if (Array.isArray(raw.result)) {
      for (const itemStr of raw.result) {
        try {
          // Items in 'result' are JSON strings themselves
          const itemMap = typeof itemStr === 'string' ? JSON.parse(itemStr) : itemStr;
          const item: CodeExecutionResultItem = {};

          if (itemMap.isMainResult) item.isMainResult = true;
          if (itemMap.is_main_result) item.isMainResult = true;

          // Map MIME types to fields
          if (itemMap["text/plain"]) item.text = itemMap["text/plain"];
          if (itemMap["text/html"]) item.html = itemMap["text/html"];
          if (itemMap["text/markdown"]) item.markdown = itemMap["text/markdown"];
          if (itemMap["image/png"]) item.png = itemMap["image/png"];
          if (itemMap["image/jpeg"]) item.jpeg = itemMap["image/jpeg"];
          if (itemMap["image/svg+xml"]) item.svg = itemMap["image/svg+xml"];
          if (itemMap["text/latex"]) item.latex = itemMap["text/latex"];
          if (itemMap["application/json"]) item.json = itemMap["application/json"];

          // Chart support (Vega/Vega-Lite)
          if (itemMap["application/vnd.vegalite.v4+json"]) {
            item.chart = itemMap["application/vnd.vegalite.v4+json"];
          } else if (itemMap["application/vnd.vegalite.v5+json"]) {
            item.chart = itemMap["application/vnd.vegalite.v5+json"];
          } else if (itemMap["application/vnd.vega.v5+json"]) {
            item.chart = itemMap["application/vnd.vega.v5+json"];
          }

          results.push(item);
        } catch (e) {
          // Ignore parse errors for individual items
        }
      }
    }

    let error: CodeExecutionError | undefined;
    if (raw.executionError) {
      error = {
        name: "ExecutionError",
        value: raw.executionError,
        traceback: "",
      };
    }

    // Determine legacy result string for backward compatibility
    let resultText = "";
    const mainRes = results.find((r) => r.isMainResult && r.text);
    if (mainRes && mainRes.text) {
      resultText = mainRes.text;
    } else if (results.length > 0 && results[0].text) {
      resultText = results[0].text;
    } else if (logs.stdout.length > 0) {
      resultText = logs.stdout.join("");
    }

    return {
      requestId: "", // Will be filled by caller
      success: !raw.executionError,
      result: resultText,
      errorMessage: raw.executionError,
      logs,
      results,
      error,
      executionTime: raw.executionTime || raw.execution_time,
      executionCount: raw.executionCount || raw.execution_count,
    };
  }

  /**
   * Execute code in the specified language with a timeout.
   * Corresponds to Python's run_code() method
   *
   * @param code - The code to execute.
   * @param language - The programming language of the code. Must be either 'python' or 'javascript'.
   * @param timeoutS - The timeout for the code execution in seconds. Default is 60s.
   *                   Note: Due to gateway limitations, each request cannot exceed 60 seconds.
   * @returns CodeExecutionResult with code execution output and requestId
   * @throws Error if an unsupported language is specified.
   *
   * @example
   * ```typescript
   * const agentBay = new AgentBay({ apiKey: 'your_api_key' });
   * const result = await agentBay.create({ imageId: "code_latest" });
   * if (result.success) {
   *   const codeResult = await result.session.code.runCode('print("Hello")', "python");
   *   console.log(codeResult.result);
   *   if (codeResult.results) {
   *      // Access rich output like images or charts
   *   }
   *   await result.session.delete();
   * }
   * ```
   */
  async runCode(
    code: string,
    language: string,
    timeoutS = 60
  ): Promise<CodeExecutionResult> {
    try {
      // Validate language
      if (language !== "python" && language !== "javascript") {
        return {
          requestId: "",
          success: false,
          result: "",
          errorMessage: `Unsupported language: ${language}. Supported languages are 'python' and 'javascript'`,
        };
      }

      const args = {
        code,
        language,
        timeout_s: timeoutS,
      };

      const response = await this.session.callMcpTool("run_code", args);

      let codeResult: CodeExecutionResult;
      
      // Even if response.success is false, data might contain structured error info
      if (response.success) {
        codeResult = this.parseBackendResponse(response.data);
      } else {
        // Check if errorMessage is JSON
        try {
            if (response.errorMessage && response.errorMessage.trim().startsWith('{')) {
                codeResult = this.parseBackendResponse(response.errorMessage);
                codeResult.success = false;
            } else {
                 // Real failure not from code execution but tool failure
                 return {
                    requestId: response.requestId,
                    success: false,
                    result: "",
                    errorMessage: response.errorMessage,
                  };
            }
        } catch {
             return {
                requestId: response.requestId,
                success: false,
                result: "",
                errorMessage: response.errorMessage,
              };
        }
      }

      codeResult.requestId = response.requestId;
      return codeResult;

    } catch (error) {
      return {
        requestId: "",
        success: false,
        result: "",
        errorMessage: `Failed to run code: ${error}`,
      };
    }
  }
}
