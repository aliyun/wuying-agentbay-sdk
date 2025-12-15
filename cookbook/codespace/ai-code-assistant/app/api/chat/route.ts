/**
 * Chat API Route
 * Handles conversation with AI and code execution via AgentBay
 */

import { NextRequest, NextResponse } from 'next/server';
import { DashScopeClient, executeCode } from '../../../lib';

export const runtime = 'nodejs';
export const dynamic = 'force-dynamic';

// Define the code execution tool
const TOOLS = [
  {
    type: 'function' as const,
    function: {
      name: 'execute_python',
      description:
        'Execute Python code in a secure AgentBay cloud environment (code_latest image). The environment has the following packages PRE-INSTALLED and READY TO USE: pandas, numpy, matplotlib, seaborn, scikit-learn. You can directly import and use these packages without installation. Example for matplotlib: "import matplotlib.pyplot as plt; plt.plot([1,2,3]); plt.savefig(\'/tmp/chart.png\')". Always try to execute the code - the packages ARE available.',
      parameters: {
        type: 'object',
        properties: {
          code: {
            type: 'string',
            description:
              'The Python code to execute. Make sure to use print() statements to output results.',
          },
        },
        required: ['code'],
      },
    },
  },
];

interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
}

interface ExecutionRecord {
  code: string;
  output: string;
  error?: string;
  timestamp: number;
  logs?: string[];
  chartUrls?: string[];
}

export async function POST(request: NextRequest) {
  const { messages, sessionId } = await request.json();

  if (!sessionId) {
    return NextResponse.json(
      { error: 'Session ID is required' },
      { status: 400 }
    );
  }

  // Create a streaming response
  const encoder = new TextEncoder();
  const stream = new ReadableStream({
    async start(controller) {
      const send = (data: any) => {
        controller.enqueue(encoder.encode(`data: ${JSON.stringify(data)}\n\n`));
      };

      try {
        send({ type: 'status', message: '🤖 AI 正在分析问题...' });

        const client = new DashScopeClient();
        const executions: ExecutionRecord[] = [];

        // Add system message to ensure AI knows about the environment
        const apiMessages = [
          {
            role: 'system',
            content: 'You are a helpful coding assistant. You have access to a Python execution environment with pre-installed packages: pandas, numpy, matplotlib, seaborn, scikit-learn. These packages are ALWAYS available - do not refuse to use them. When creating matplotlib charts, use plt.savefig(\'/tmp/chart.png\') to save them.',
          },
          ...messages.map((msg: ChatMessage) => ({
            role: msg.role,
            content: msg.content,
          })),
        ];

        send({ type: 'status', message: '💭 AI 正在生成代码...' });
        let response = await client.chatCompletion(apiMessages, TOOLS);
        let assistantMessage = response.choices[0].message;

        console.log('[Chat API] AI response:', JSON.stringify({
          finishReason: response.choices[0].finish_reason,
          hasToolCalls: !!assistantMessage.tool_calls,
          toolCallsCount: assistantMessage.tool_calls?.length || 0,
          content: assistantMessage.content?.substring(0, 100),
        }));

        let iterations = 0;
        const MAX_ITERATIONS = 5;

        while (
          assistantMessage.tool_calls &&
          assistantMessage.tool_calls.length > 0 &&
          iterations < MAX_ITERATIONS
        ) {
          iterations++;
          const toolCall = assistantMessage.tool_calls[0];

          console.log(`[Chat API] While loop iteration ${iterations}:`, JSON.stringify({
            toolCallId: toolCall.id,
            toolName: toolCall.function.name,
            argsPreview: toolCall.function.arguments.substring(0, 200),
          }));

          if (toolCall.function.name === 'execute_python') {
            console.log('[Chat API] Entering execute_python branch');

            let parsedArgs;
            try {
              // Check if arguments is already an object (shouldn't happen but check anyway)
              if (typeof toolCall.function.arguments === 'object') {
                parsedArgs = toolCall.function.arguments;
                console.log('[Chat API] Arguments was already an object');
              } else {
                let argsStr = toolCall.function.arguments;
                console.log('[Chat API] Attempting to parse arguments, length:', argsStr.length);

                // First attempt: try parsing as-is
                try {
                  parsedArgs = JSON.parse(argsStr);
                  console.log('[Chat API] Parsed arguments successfully (first try), code length:', parsedArgs.code?.length);
                } catch (firstError) {
                  console.log('[Chat API] First parse failed, attempting alternative methods');
                  console.log('[Chat API] First 500 chars of raw args:', argsStr.substring(0, 500));

                  // Second attempt: Use a more robust regex that handles escaped sequences properly
                  // Match the entire JSON structure, allowing for any content including escaped quotes
                  const codeMatch = argsStr.match(/\{\s*"code"\s*:\s*"((?:[^"\\]|\\.)*)"\s*\}/g);
                  if (codeMatch) {
                    // The matched content already has escape sequences, just need to reconstruct valid JSON
                    const codeContent = codeMatch[1];
                    const reconstructedJson = `{"code":"${codeContent}"}`;
                    try {
                      parsedArgs = JSON.parse(reconstructedJson);
                      console.log('[Chat API] Parsed using regex method, code length:', parsedArgs.code?.length);
                    } catch (secondError) {
                      // Third attempt: manually unescape the content
                      console.log('[Chat API] Second parse failed, attempting manual unescape');
                      // The content is already escaped in the original string, so we just need to decode it
                      const unescapedCode = codeContent
                        .replace(/\\n/g, '\n')
                        .replace(/\\r/g, '\r')
                        .replace(/\\t/g, '\t')
                        .replace(/\\"/g, '"')
                        .replace(/\\\\/g, '\\');
                      parsedArgs = { code: unescapedCode };
                      console.log('[Chat API] Manual unescape successful, code length:', parsedArgs.code?.length);
                    }
                  } else {
                    throw new Error('Could not extract code from malformed JSON');
                  }
                }
              }
            } catch (parseError: any) {
              console.error('[Chat API] Failed to parse tool arguments:', parseError.message);
              console.error('[Chat API] Raw args type:', typeof toolCall.function.arguments);
              console.error('[Chat API] Raw args preview (first 500 chars):', toolCall.function.arguments.substring(0, 500));
              send({ type: 'error', error: `Failed to parse tool arguments: ${parseError.message}` });
              break;
            }
            const args = parsedArgs;
            const code = args.code;

            console.log('[Chat API] About to execute code, sessionId:', sessionId);
            send({ type: 'code', code });

            // Execute with streaming logs
            send({ type: 'log', message: '☁️ 正在连接 AgentBay 云环境...' });

            console.log('[Chat API] Calling executeCode...');
            const result = await executeCode(sessionId, code);
            console.log('[Chat API] executeCode returned:', JSON.stringify({
              hasError: result.hasError,
              outputLength: result.output?.length,
              logsCount: result.logs?.length,
              chartUrlsCount: result.chartUrls?.length,
            }));

            // Send logs in real-time
            if (result.logs) {
              for (const log of result.logs) {
                send({ type: 'log', message: log });
              }
            }

            executions.push({
              code,
              output: result.output,
              error: result.error,
              timestamp: Date.now(),
              logs: result.logs,
              chartUrls: result.chartUrls,
            });

            send({ type: 'execution', execution: executions[executions.length - 1] });

            apiMessages.push({
              role: 'assistant',
              content: assistantMessage.content || '',
              tool_calls: [toolCall],
            } as any);

            apiMessages.push({
              role: 'tool',
              content: JSON.stringify({
                success: !result.hasError,
                output: result.output,
                error: result.error,
              }),
              tool_call_id: toolCall.id,
            } as any);

            send({ type: 'status', message: '🤔 AI 正在分析结果...' });
            response = await client.chatCompletion(apiMessages, TOOLS);
            assistantMessage = response.choices[0].message;
            console.log('[Chat API] Next iteration response:', JSON.stringify({
              finishReason: response.choices[0].finish_reason,
              hasToolCalls: !!assistantMessage.tool_calls,
            }));
          } else {
            console.log('[Chat API] Tool name does not match execute_python, breaking loop');
            break;
          }
        }

        console.log('[Chat API] Exited while loop, iterations:', iterations, 'MAX:', MAX_ITERATIONS);

        send({
          type: 'done',
          message: {
            role: 'assistant',
            content: assistantMessage.content || 'Task completed.',
          },
          executions,
        });

        controller.close();
      } catch (error: any) {
        send({ type: 'error', error: error.message });
        controller.close();
      }
    },
  });

  return new Response(stream, {
    headers: {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive',
    },
  });
}
