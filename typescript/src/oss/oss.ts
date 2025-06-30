import { APIError } from '../exceptions';
import { Session } from '../session';
import { Client } from '../api/client';
import { CallMcpToolRequest } from '../api/models/model';
import { log, logError } from '../utils/logger';
import { ApiResponse, ApiResponseWithData, extractRequestId } from '../types/api-response';

import * as $_client from '../api';

/**
 * Result object for a CallMcpTool operation
 */
interface CallMcpToolResult {
  data: Record<string, any>;
  content?: any[];
  textContent?: string;
  isError: boolean;
  errorMsg?: string;
  statusCode: number;
  requestId?: string;
}

/**
 * Handles Object Storage Service operations in the AgentBay cloud environment.
 */
export class Oss {
  private session: Session;
  private client!: $_client.Client;
  private baseUrl!: string;

  /**
   * Initialize an Oss object.
   *
   * @param session - The Session instance that this Oss belongs to.
   */
  constructor(session: Session) {
    this.session = session;
  }

  /**
   * Helper method to call MCP tools and handle common response processing
   *
   * @param toolName - Name of the MCP tool to call
   * @param args - Arguments to pass to the tool
   * @param defaultErrorMsg - Default error message if specific error details are not available
   * @returns A CallMcpToolResult with the response data
   * @throws APIError if the call fails
   */
  private async callMcpTool(
    toolName: string,
    args: Record<string, any>,
    defaultErrorMsg: string
  ): Promise<CallMcpToolResult> {
    try {
      const callToolRequest = new $_client.CallMcpToolRequest({
        authorization: `Bearer ${this.session.getAPIKey()}`,
        sessionId: this.session.getSessionId(),
        name: toolName,
        args: JSON.stringify(args)
      });

      // Log API request
      log(`API Call: CallMcpTool - ${toolName}`);
      log(`Request: SessionId=${this.session.getSessionId()}, Args=${JSON.stringify(args)}`);

      const response = await this.session.getClient().callMcpTool(callToolRequest);

      // Log API response
      log(`Response from CallMcpTool - ${toolName}:`, response.body);

      if (!response.body?.data) {
        throw new Error('Invalid response data format');
      }

      // Extract data from response
      const data = response.body.data as Record<string, any>;

      // Create result object
      const result: CallMcpToolResult = {
        data,
        statusCode: response.statusCode || 0,
        isError: false,
        requestId: extractRequestId(response)
      };

      // Check if there's an error in the response
      if (data.isError === true) {
        result.isError = true;

        // Try to extract the error message from the content field
        const contentArray = data.content as any[] | undefined;
        if (contentArray && contentArray.length > 0) {
          result.content = contentArray;

          // Extract error message from the first content item
          if (contentArray[0]?.text) {
            result.errorMsg = contentArray[0].text;
            throw new Error(contentArray[0].text);
          }
        }
        throw new Error(defaultErrorMsg);
      }

      // Extract content array if it exists
      if (Array.isArray(data.content)) {
        result.content = data.content;

        // Extract textContent from content items
        if (result.content.length > 0) {
          const textParts: string[] = [];
          for (const item of result.content) {
            if (item && typeof item === 'object' && item.text && typeof item.text === 'string') {
              textParts.push(item.text);
            }
          }
          result.textContent = textParts.join('\n');
        }
      }

      return result;
    } catch (error) {
      logError(`Error calling CallMcpTool - ${toolName}:`, error);
      throw new APIError(`Failed to call ${toolName}: ${error}`);
    }
  }

  /**
   * Initialize OSS environment variables with the specified credentials.
   *
   * @param accessKeyId - The Access Key ID for OSS authentication.
   * @param accessKeySecret - The Access Key Secret for OSS authentication.
   * @param securityToken - The security token for OSS authentication.
   * @param endpoint - The OSS service endpoint. If not specified, the default is used.
   * @param region - The OSS region. If not specified, the default is used.
   * @returns API response with initialization result and requestId
   */
  async envInit(
    accessKeyId: string,
    accessKeySecret: string,
    securityToken: string,
    endpoint?: string,
    region?: string
  ): Promise<ApiResponseWithData<string>> {
    const args: Record<string, any> = {
      access_key_id: accessKeyId,
      access_key_secret: accessKeySecret,
      security_token: securityToken
    };

    // Add optional parameters if provided
    if (endpoint) {
      args.endpoint = endpoint;
    }
    if (region) {
      args.region = region;
    }

    const result = await this.callMcpTool('oss_env_init', args, 'error initializing OSS environment');

    return {
      requestId: result.requestId,
      data: result.textContent || ''
    };
  }

  /**
   * Create an OSS client with the provided credentials.
   *
   * @param accessKeyId - The Access Key ID for OSS authentication.
   * @param accessKeySecret - The Access Key Secret for OSS authentication.
   * @param endpoint - The OSS service endpoint. If not specified, the default is used.
   * @param region - The OSS region. If not specified, the default is used.
   * @returns API response with client creation result and requestId
   */
  async createClient(
    accessKeyId: string,
    accessKeySecret: string,
    endpoint?: string,
    region?: string
  ): Promise<ApiResponseWithData<string>> {
    const args: Record<string, any> = {
      access_key_id: accessKeyId,
      access_key_secret: accessKeySecret
    };

    // Add optional parameters if provided
    if (endpoint) {
      args.endpoint = endpoint;
    }
    if (region) {
      args.region = region;
    }

    const result = await this.callMcpTool('oss_client_create', args, 'error creating OSS client');

    return {
      requestId: result.requestId,
      data: result.textContent || ''
    };
  }

  /**
   * Upload a local file or directory to OSS.
   *
   * @param bucket - OSS bucket name.
   * @param object - Object key in OSS.
   * @param path - Local file or directory path to upload.
   * @returns API response with upload result and requestId
   */
  async upload(bucket: string, object: string, path: string): Promise<ApiResponseWithData<string>> {
    const args = {
      bucket,
      object,
      path
    };

    const result = await this.callMcpTool('oss_upload', args, 'error uploading to OSS');

    return {
      requestId: result.requestId,
      data: result.textContent || ''
    };
  }

  /**
   * Upload a local file or directory to OSS using a pre-signed URL.
   *
   * @param url - Pre-signed URL for anonymous upload.
   * @param path - Local file or directory path to upload.
   * @returns API response with upload result and requestId
   */
  async uploadAnonymous(url: string, path: string): Promise<ApiResponseWithData<string>> {
    const args = {
      url,
      path
    };

    const result = await this.callMcpTool('oss_upload_annon', args, 'error uploading anonymously');

    return {
      requestId: result.requestId,
      data: result.textContent || ''
    };
  }

  /**
   * Download an object from OSS to a local file or directory.
   *
   * @param bucket - OSS bucket name.
   * @param object - Object key in OSS.
   * @param path - Local file or directory path to save the downloaded content.
   * @returns API response with download result and requestId
   */
  async download(bucket: string, object: string, path: string): Promise<ApiResponseWithData<string>> {
    const args = {
      bucket,
      object,
      path
    };

    const result = await this.callMcpTool('oss_download', args, 'error downloading from OSS');

    return {
      requestId: result.requestId,
      data: result.textContent || ''
    };
  }

  /**
   * Download an object from OSS using a pre-signed URL.
   *
   * @param url - Pre-signed URL for anonymous download.
   * @param path - Local file or directory path to save the downloaded content.
   * @returns API response with download result and requestId
   */
  async downloadAnonymous(url: string, path: string): Promise<ApiResponseWithData<string>> {
    const args = {
      url,
      path
    };

    const result = await this.callMcpTool('oss_download_annon', args, 'error downloading anonymously');

    return {
      requestId: result.requestId,
      data: result.textContent || ''
    };
  }
}
