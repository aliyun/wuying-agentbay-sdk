import {ApiResponse} from '../types/api-response';
import {log, logDebug} from '../utils/logger';

/**
 * Result of task execution.
 */
export interface ExecutionResult extends ApiResponse {
  taskId: string;
  taskStatus: string;
  taskResult: string;
}

/**
 * Result of query operations.
 */
export interface QueryResult extends ApiResponse {
  taskStatus: string;
  taskAction: string;
  taskProduct: string;
}

/**
 * Result of agent initialization.
 */
export interface InitializationResult extends ApiResponse {
  success: boolean;
}

/**
 * Options for Agent initialization.

 */
export interface AgentOptions {
  use_vision: boolean;
  output_schema: '';
}

/**
 * Result of an MCP tool call.
 */
export interface McpToolResult {
  success: boolean;
  data: string;
  errorMessage: string;
  requestId: string;
}

/**
 * Interface defining the methods needed by Agent from Session.
 */
export interface McpSession {
  getAPIKey(): string;
  getSessionId(): string;
  callMcpTool(toolName: string, args: any): Promise<McpToolResult>;
}

/**
 * An Agent to perform tasks on the computer.
 */
export class ComputerUseAgent {
  private session: McpSession;
  /**
   * Initialize an Computer Agent object.
   *
   * @param session - The Session instance that this Agent belongs to.
   */
  constructor(session: McpSession) {
    this.session = session;
  }
  /**
   * Execute a specific task described in human language.
   *
   * @param task - Task description in human language.
   * @param maxTryTimes - Maximum number of retry attempts.
   * @returns ExecutionResult containing success status, task output, and error
   *     message if any.
   *
   * @example
   * ```typescript
   * const agentBay = new AgentBay({ apiKey: 'your_api_key' });
   * const result = await agentBay.create({ imageId: 'windows_latest' });
   * if (result.success) {
   *   const taskResult = await result.session.agent.computer.executeTask(
   *     'Open notepad',
   *     10
   *   );
   *   console.log(`Task status: ${taskResult.taskStatus}`);
   *   await result.session.delete();
   * }
   * ```
   */
  async executeTask(task: string, maxTryTimes: number):
      Promise<ExecutionResult> {
    try {
      const args = {task, max_try_times: maxTryTimes};
      const result = await this.session.callMcpTool('flux_execute_task', args);

      if (!result.success) {
        return {
          requestId: result.requestId,
          success: false,
          errorMessage: result.errorMessage,
          taskStatus: 'failed',
          taskId: '',
          taskResult: 'Task Failed',
        };
      }

      // Parse task ID from response
      let content: any;
      try {
        content = JSON.parse(result.data);
      } catch (err) {
        return {
          requestId: result.requestId,
          success: false,
          errorMessage: `Failed to parse response: ${err}`,
          taskStatus: 'failed',
          taskId: '',
          taskResult: 'Invalid execution response.',
        };
      }

      const taskId = content.task_id;
      if (!taskId) {
        return {
          requestId: result.requestId,
          success: false,
          errorMessage: 'Task ID not found in response',
          taskStatus: 'failed',
          taskId: '',
          taskResult: 'Invalid task ID.',
        };
      }

      // Poll for task completion
      let triedTime = 0;
      while (triedTime < maxTryTimes) {
        const query = await this.getTaskStatus(taskId);
        if (!query.success) {
          return {
            requestId: query.requestId,
            success: false,
            errorMessage: query.errorMessage,
            taskStatus: 'failed',
            taskId: taskId,
            taskResult: '',
          };
        }

        switch (query.taskStatus) {
          case 'finished':
            return {
              requestId: query.requestId,
              success: true,
              errorMessage: '',
              taskId: taskId,
              taskStatus: 'finished',
              taskResult: query.taskProduct,
            };
          case 'failed':
            return {
              requestId: query.requestId,
              success: false,
              errorMessage: query.errorMessage || 'Failed to execute task.',
              taskId: taskId,
              taskStatus: 'failed',
              taskResult: '',
            };
          case 'unsupported':
            return {
              requestId: query.requestId,
              success: false,
              errorMessage: query.errorMessage || 'Unsupported task.',
              taskId: taskId,
              taskStatus: 'unsupported',
              taskResult: '',
            };
        }

        logDebug(`Task ${taskId} is still running, please wait for a while.`);
        await new Promise(resolve => setTimeout(resolve, 3000));
        triedTime++;
      }

      return {
        requestId: result.requestId,
        success: false,
        errorMessage: 'Task execution timed out',
        taskStatus: 'timeout',
        taskId: taskId,
        taskResult: 'Task Timed Out',
      };
    } catch (error) {
      return {
        requestId: '',
        success: false,
        errorMessage: `Failed to execute: ${error}`,
        taskStatus: 'failed',
        taskId: '',
        taskResult: 'Task Failed',
      };
    }
  }

  /**
   * Get the status of the task with the given task ID.
   *
   * @param taskId - Task ID
   * @returns QueryResult containing the task status
   *
   * @example
   * ```typescript
   * const agentBay = new AgentBay({ apiKey: 'your_api_key' });
   * const result = await agentBay.create({ imageId: 'windows_latest' });
   * if (result.success) {
   *   const taskResult = await result.session.agent.computer.executeTask('Open
   * calculator', 10); const statusResult = await
   * result.session.agent.computer.getTaskStatus(taskResult.taskId);
   * console.log(`Status:
   * ${JSON.parse(statusResult.output).status}`); await result.session.delete();
   * }
   * ```
   */
  async getTaskStatus(taskId: string): Promise<QueryResult> {
    try {
      const args = {task_id: taskId};
      const result =
          await this.session.callMcpTool('flux_get_task_status', args);

      if (!result.success) {
        return {
          requestId: result.requestId,
          success: false,
          errorMessage: result.errorMessage,
          taskAction: '',
          taskProduct: '',
          taskStatus: 'failed',
        };
      }
      let queryResult: any;
      try {
        queryResult = JSON.parse(result.data);
        return {
          requestId: result.requestId,
          success: true,
          errorMessage: '',
          taskAction: queryResult.action || '',
          taskProduct: queryResult.product || '',
          taskStatus: queryResult.status || 'failed',
        };
      } catch (error) {
        return {
          requestId: result.requestId,
          success: false,
          errorMessage: `Failed to get task status: ${error}`,
          taskAction: '',
          taskProduct: '',
          taskStatus: 'failed',
        };
      }
    } catch (error) {
      return {
        requestId: '',
        success: false,
        errorMessage: `Failed to get task status: ${error}`,
        taskAction: '',
        taskProduct: '',
        taskStatus: 'failed',
      };
    }
  }

  /**
   * Terminate a task with a specified task ID.
   *
   * @param taskId - The ID of the running task.
   * @returns ExecutionResult containing success status, task output, and
   *     error message if any.
   *
   * @example
   * ```typescript
   * const agentBay = new AgentBay({ apiKey: 'your_api_key' });
   * const result = await agentBay.create({ imageId: 'windows_latest' });
   * if (result.success) {
   *   const taskResult = await result.session.agent.computer.executeTask(
   *     'Open notepad',
   *     5
   *   );
   *   const terminateResult = await result.session.agent.computer.terminateTask(
   *     taskResult.taskId
   *   );
   *   console.log(`Terminated: ${terminateResult.taskStatus}`);
   *   await result.session.delete();
   * }
   * ```
   */
  async terminateTask(taskId: string): Promise<ExecutionResult> {
    logDebug('Terminating task');

    try {
      const args = {task_id: taskId};
      const result =
          await this.session.callMcpTool('flux_terminate_task', args);

      let content: any;
      try {
        content = JSON.parse(result.data);
      } catch (err) {
        return {
          requestId: result.requestId,
          success: false,
          errorMessage: `Failed to parse response: ${err}`,
          taskId,
          taskStatus: 'failed',
          taskResult: '',
        };
      }

      const terminatedTaskId = content.task_id || taskId;
      const status = content.status || 'unknown';

      if (result.success) {
        return {
          requestId: result.requestId,
          success: true,
          errorMessage: '',
          taskId: terminatedTaskId,
          taskStatus: status,
          taskResult: '',
        };
      }

      return {
        requestId: result.requestId,
        success: false,
        errorMessage: result.errorMessage,
        taskId: terminatedTaskId,
        taskStatus: status,
        taskResult: '',
      };
    } catch (error) {
      return {
        requestId: '',
        success: false,
        errorMessage: `Failed to terminate: ${error}`,
        taskId,
        taskStatus: 'failed',
        taskResult: '',
      };
    }
  }
}


export class BrowserUseAgent {
  private session: McpSession;
  /**
   * Initialize an Browser Agent object.
   * @description Browser Use Agent is in BETA ⚠️ .
   *
   * @param session - The Session instance that this Agent belongs to.
   */
  constructor(session: McpSession) {
    this.session = session;
  }

  /**
   * Initialize the browser agent with specific options.
   * @param options - agent initialization options
   * @returns  InitializationResult containing success status, task output,
   *     and error message if any.
   *
   * @example
   * ```typescript
   * const agentBay = new AgentBay({ apiKey: 'your_api_key' });
   * const result = await agentBay.create({ imageId: 'linux_latest' });
   * if (result.success) {
   *   options:AgentOptions = new AgentOptions(use_vision=False,
   * output_schema=""); const initResult = await
   * result.session.agent.browser.initialize(options); console.log(`Initialize
   * success: ${initResult.success}`); await result.session.delete();
   * }
   * ```
   */
  async initialize(options: AgentOptions): Promise<InitializationResult> {
    const args = {
      use_vision: options.use_vision,
      output_schema: options.output_schema
    };
    try {
      const result =
          await this.session.callMcpTool('browser_use_initialize', args);
      if (!result.success) {
        return {
          success: false,
          errorMessage: result.errorMessage,
        };
      } else {
        return {
          success: true,
          errorMessage: '',
        };
      }
    } catch (error) {
      return {
        success: false,
        errorMessage: `Failed to initialize: ${error}`,
      };
    }
  }

  /**
   * Execute a specific task described in human language.
   *
   * @param task - Task description in human language.
   * @param maxTryTimes - Maximum number of retry attempts.
   * @returns ExecutionResult containing success status, task output, and
   *     error message if any.
   *
   * @example
   * ```typescript
   * const agentBay = new AgentBay({ apiKey: 'your_api_key' });
   * const result = await agentBay.create({ imageId: 'linux_latest' });
   * if (result.success) {
   *   const taskResult = await result.session.agent.browser.executeTask(
   *     'Navigate to baidu and query the weather of Shanghai',
   *     10
   *   );
   *   console.log(`Task status: ${taskResult.taskStatus}`);
   *   await result.session.delete();
   * }
   * ```
   */
  async executeTask(task: string, maxTryTimes: number):
      Promise<ExecutionResult> {
    try {
      const args = {task, max_try_times: maxTryTimes};
      const result =
          await this.session.callMcpTool('browser_use_execute_task', args);

      if (!result.success) {
        return {
          requestId: result.requestId,
          success: false,
          errorMessage: result.errorMessage,
          taskStatus: 'failed',
          taskId: '',
          taskResult: 'Task Failed',
        };
      }

      // Parse task ID from response
      let content: any;
      try {
        content = JSON.parse(result.data);
      } catch (err) {
        return {
          requestId: result.requestId,
          success: false,
          errorMessage: `Failed to parse response: ${err}`,
          taskStatus: 'failed',
          taskId: '',
          taskResult: 'Invalid execution response.',
        };
      }

      const taskId = content.task_id;
      if (!taskId) {
        return {
          requestId: result.requestId,
          success: false,
          errorMessage: 'Task ID not found in response',
          taskStatus: 'failed',
          taskId: '',
          taskResult: 'Invalid task ID.',
        };
      }

      // Poll for task completion
      let triedTime = 0;
      while (triedTime < maxTryTimes) {
        const query = await this.getTaskStatus(taskId);
        if (!query.success) {
          return {
            requestId: query.requestId,
            success: false,
            errorMessage: query.errorMessage,
            taskStatus: 'failed',
            taskId: taskId,
            taskResult: '',
          };
        }

        switch (query.taskStatus) {
          case 'finished':
            return {
              requestId: query.requestId,
              success: true,
              errorMessage: '',
              taskId: taskId,
              taskStatus: 'finished',
              taskResult: query.taskProduct,
            };
          case 'failed':
            return {
              requestId: query.requestId,
              success: false,
              errorMessage: query.errorMessage || 'Failed to execute task.',
              taskId: taskId,
              taskStatus: 'failed',
              taskResult: '',
            };
          case 'unsupported':
            return {
              requestId: query.requestId,
              success: false,
              errorMessage: query.errorMessage || 'Unsupported task.',
              taskId: taskId,
              taskStatus: 'unsupported',
              taskResult: '',
            };
        }

        logDebug(`Task ${taskId} is still running, please wait for a while.`);
        await new Promise(resolve => setTimeout(resolve, 3000));
        triedTime++;
      }

      return {
        requestId: result.requestId,
        success: false,
        errorMessage: 'Task execution timed out',
        taskStatus: 'timeout',
        taskId: taskId,
        taskResult: 'Task Timed Out',
      };
    } catch (error) {
      return {
        requestId: '',
        success: false,
        errorMessage: `Failed to execute: ${error}`,
        taskStatus: 'failed',
        taskId: '',
        taskResult: 'Task Failed',
      };
    }
  }

  /**
   * Get the status of the task with the given task ID.
   *
   * @param taskId - Task ID
   * @returns QueryResult containing the task status
   *
   * @example
   * ```typescript
   * const agentBay = new AgentBay({ apiKey: 'your_api_key' });
   * const result = await agentBay.create({ imageId: 'linux_latest' });
   * if (result.success) {
   *   const taskResult = await result.session.agent.browser.executeTask(
   *     'Navigate to baidu and query the weather of Shanghai',
   *     10
   *   );
   *   const statusResult = await result.session.agent.browser.getTaskStatus(
   *     taskResult.taskId
   *   );
   *   console.log(`Status: ${statusResult.taskStatus}`);
   *   await result.session.delete();
   * }
   * ```
   */
  async getTaskStatus(taskId: string): Promise<QueryResult> {
    try {
      const args = {task_id: taskId};
      const result =
          await this.session.callMcpTool('browser_use_get_task_status', args);

      if (!result.success) {
        return {
          requestId: result.requestId,
          success: false,
          errorMessage: result.errorMessage,
          taskAction: '',
          taskProduct: '',
          taskStatus: 'failed',
        };
      }
      let queryResult: any;
      try {
        queryResult = JSON.parse(result.data);
        return {
          requestId: result.requestId,
          success: true,
          errorMessage: '',
          taskAction: queryResult.action || '',
          taskProduct: queryResult.product || '',
          taskStatus: queryResult.status || 'failed',
        };
      } catch (error) {
        return {
          requestId: result.requestId,
          success: false,
          errorMessage: `Failed to get task status: ${error}`,
          taskAction: '',
          taskProduct: '',
          taskStatus: 'failed',
        };
      }
    } catch (error) {
      return {
        requestId: '',
        success: false,
        errorMessage: `Failed to get task status: ${error}`,
        taskAction: '',
        taskProduct: '',
        taskStatus: 'failed',
      };
    }
  }

  /**
   * Terminate a task with a specified task ID.
   *
   * @param taskId - The ID of the running task.
   * @returns ExecutionResult containing success status, task output, and
   *     error message if any.
   *
   * @example
   * ```typescript
   * const agentBay = new AgentBay({ apiKey: 'your_api_key' });
   * const result = await agentBay.create({ imageId: 'linux_latest' });
   * if (result.success) {
   *   const taskResult = await result.session.agent.browser.executeTask(
   *     'Navigate to baidu and query the weather of Shanghai',
   *     10
   *   );
   *   const terminateResult = await result.session.agent.browser.terminateTask(
   *     taskResult.taskId
   *   );
   *   console.log(`Terminated: ${terminateResult.taskStatus}`);
   *   await result.session.delete();
   * }
   * ```
   */
  async terminateTask(taskId: string): Promise<ExecutionResult> {
    logDebug('Terminating task');

    try {
      const args = {task_id: taskId};
      const result =
          await this.session.callMcpTool('browser_use_terminate_task', args);

      let content: any;
      try {
        content = JSON.parse(result.data);
      } catch (err) {
        return {
          requestId: result.requestId,
          success: false,
          errorMessage: `Failed to parse response: ${err}`,
          taskId: taskId,
          taskStatus: 'failed',
          taskResult: '',
        };
      }

      const terminatedTaskId = content.task_id || taskId;
      const status = content.status || 'unknown';

      if (result.success) {
        return {
          requestId: result.requestId,
          success: true,
          errorMessage: '',
          taskId: terminatedTaskId,
          taskStatus: status,
          taskResult: '',
        };
      }

      return {
        requestId: result.requestId,
        success: false,
        errorMessage: result.errorMessage,
        taskId: terminatedTaskId,
        taskStatus: status,
        taskResult: '',
      };
    } catch (error) {
      return {
        requestId: '',
        success: false,
        errorMessage: `Failed to terminate: ${error}`,
        taskId: taskId,
        taskStatus: 'failed',
        taskResult: '',
      };
    }
  }
}
/**
 * An Agent to manipulate applications to complete specific tasks.
 * According to the use scenary, The agent can a browser use agent which is
 * specialized for browser automation tasks, The agent also can be  a computer
 * use agent which is specialized for multiple applications automation tasks.
 */
export class Agent {
  /**
   * An instance of Computer Use Agent.
   */
  public computer: ComputerUseAgent;
  /**
   * An instance of Browser Use Agent.
   */
  public browser: BrowserUseAgent;

  /**
   * Initialize an Agent object.
   *
   * @param session - The Session instance that this Agent belongs to.
   */
  constructor(session: McpSession) {
    this.computer = new ComputerUseAgent(session);
    this.browser = new BrowserUseAgent(session);
  }
}