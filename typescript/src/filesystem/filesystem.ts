import { APIError } from '../exceptions';
import { Session } from '../session';
import { CallMcpToolRequest } from '../api/models/model';
import * as $_client from '../api';

/**
 * Handles file operations in the AgentBay cloud environment.
 */
export class FileSystem {
  private session: Session;
  private client!: $_client.Client;
  private baseUrl!: string;

  /**
   * Initialize a FileSystem object.
   * 
   * @param session - The Session instance that this FileSystem belongs to.
   */
  constructor(session: Session) {
    this.session = session;
  }

  /**
   * Read the contents of a file in the cloud environment.
   * 
   * @param path - Path to the file to read.
   * @returns The contents of the file.
   */
  async readFile(path: string): Promise<string> {
    try {
      const args = {
        path
      };
      
      const callToolRequest = new CallMcpToolRequest({
        authorization: `Bearer ${this.session.getAPIKey()}`,
        sessionId: this.session.getSessionId(),
        name: 'read_file',
        args: JSON.stringify(args)
      });
      
      const response = await this.session.getClient().callMcpTool(callToolRequest);
      
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
      throw new APIError(`Failed to read file: ${error}`);
    }
  }
}
