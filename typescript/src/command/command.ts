import { APIError } from '../exceptions';
import { Session } from '../session';
import Client from '../api/client';
import { CallMcpToolRequest } from '../api/models/model';

import * as $_client from '../api';
/**
 * Handles command execution operations in the AgentBay cloud environment.
 */
export class Command {
  private session: Session;
  private client!: $_client.Client;
  private baseUrl!: string;

  /**
   * Initialize a Command object.
   * 
   * @param session - The Session instance that this Command belongs to.
   */
  constructor(session: Session) {
    this.session = session;
  }

  /**
   * Execute a command in the cloud environment.
   * 
   * @param command - The command to execute.
   * @returns The result of the command execution.
   */
  async executeCommand(command: string): Promise<string> {
    try {
      const args = {
        command
      };
      const callToolRequest = new $_client.CallMcpToolRequest({
        authorization: `Bearer ${this.session.getAPIKey()}`,
        sessionId: this.session.getSessionId(),
        name: 'execute_command',
        args: JSON.stringify(args)
      })
      console.log(callToolRequest,'callToolRequest');
      
      
      const response = await this.session.getClient().callMcpTool(callToolRequest);
      console.log(response,'response');
      
      if (!response.body?.data) {
        throw new Error('Invalid response data format');
      }
      
      // Extract content from response
      const data = response.body.data as any;
      if (!data.content || !Array.isArray(data.content)) {
        throw new Error('Content field not found or not an array');
      }
      
      // Concatenate all text fields
      let fullText = '';
      for (const item of data.content) {
        if (item && typeof item === 'object' && 'text' in item) {
          fullText += item.text + '\n';
        }
      }
      
      return fullText;
    } catch (error) {
      throw new APIError(`Failed to execute command: ${error}`);
    }
  }
}
