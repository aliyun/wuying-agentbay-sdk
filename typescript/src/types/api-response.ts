/**
 * Base interface for API responses
 */
export interface ApiResponse {
  /** Optional request identifier for tracking API calls */
  requestId?: string;
}

/**
 * Generic interface for API responses that include data payload
 * @template T The type of the data being returned
 */
export interface ApiResponseWithData<T> extends ApiResponse {
  /** The actual data payload returned by the API */
  data: T;
}

export function extractRequestId(response: any): string | undefined {
  if (!response) return undefined;

  // Check for requestId in response.body first
  if (response.body && response.body.requestId) {
    return response.body.requestId;
  }
  // Check for requestId directly on response
  if (response.requestId) {
    return response.requestId;
  }

  return undefined;
}
