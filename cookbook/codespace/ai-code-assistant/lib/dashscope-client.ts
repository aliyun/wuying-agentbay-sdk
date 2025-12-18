import { headers } from 'next/headers';

export class DashScopeClient {
  private apiKey: string;
  private model: string;
  private baseUrl: string;

  constructor() {
    this.apiKey = process.env.DASHSCOPE_API_KEY || '';
    this.model = process.env.DASHSCOPE_MODEL || 'qwen-max';
    // Use the OpenAI-compatible endpoint
    this.baseUrl = 'https://dashscope.aliyuncs.com/compatible-mode/v1';

    if (!this.apiKey) {
      console.warn('DASHSCOPE_API_KEY is not set');
    }
  }

  async chatCompletion(messages: any[], tools?: any[]) {
    if (!this.apiKey) {
      throw new Error('DASHSCOPE_API_KEY is required');
    }

    const payload: any = {
      model: this.model,
      messages: messages,
      stream: false, // We don't support streaming in this client yet for tool calls simplification
    };

    if (tools && tools.length > 0) {
      payload.tools = tools;
      payload.tool_choice = 'auto';
    }

    try {
      const response = await fetch(`${this.baseUrl}/chat/completions`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.apiKey}`,
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`DashScope API error: ${response.status} ${response.statusText} - ${errorText}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error calling DashScope:', error);
      throw error;
    }
  }
}

