import { AgentBay } from 'wuying-agentbay-sdk';

// Initialize AgentBay client
// We rely on AGENTBAY_API_KEY environment variable
const agentBay = new AgentBay();

// Session timeout logic is handled by AgentBay backend (default 10 mins or so?)
// We can also implement lazy cleanup if needed, but for now we rely on the backend's lifecycle.

interface ExecuteResult {
  hasError: boolean;
  output: string;
  error?: string;
  logs?: string[];
  chartUrls?: string[];
}

export async function executeCode(clientSessionId: string, code: string): Promise<ExecuteResult> {
  const logs: string[] = [];
  logs.push('🚀 Initializing cloud environment...');

  try {
    // 1. Find or Create Session
    let session;
    const labelKey = 'app_session_id';
    
    // List sessions with the matching label
    const listResult = await agentBay.list({ [labelKey]: clientSessionId });
    
    if (listResult.success && listResult.sessionIds.length > 0) {
      // Use existing session
      logs.push('♻️  Resuming existing session...');
      const sessionId = listResult.sessionIds[0];
      const getResult = await agentBay.get(sessionId);
      if (getResult.success) {
        session = getResult.session;
      } else {
        logs.push('⚠️ Failed to retrieve existing session, creating new one...');
      }
    }

    if (!session) {
      logs.push('✨ Creating new AgentBay session (code_latest)...');
      const createResult = await agentBay.create({
        imageId: 'code_latest',
        labels: { [labelKey]: clientSessionId }
      });

      if (!createResult.success) {
        throw new Error(`Failed to create session: ${createResult.errorMessage}`);
      }
      session = createResult.session;
      logs.push('✅ Session created successfully.');
    }

    // 2. Execute Code
    logs.push('📤 Sending code to cloud executor...');
    
    // We use the Python executor
    const runResult = await session.code.runCode(code, 'python');
    
    if (!runResult.success) {
      return {
        hasError: true,
        output: '',
        error: runResult.errorMessage || 'Unknown execution error',
        logs: [...logs, '❌ Execution failed.'],
      };
    }

    const output = runResult.result || '';
    logs.push('✅ Code executed successfully.');

    // 3. Check for generated charts
    const chartUrls: string[] = [];
    const chartPath = '/tmp/chart.png';
    
    // Try to read the chart file
    const fileResult = await session.fileSystem.readFile(chartPath);
    if (fileResult.success) {
      logs.push('📊 Chart generated, downloading...');
      // Assuming fileResult.content is text (as per SDK default?), 
      // but for images we might need base64.
      // The SDK readFile documentation says: "Read file content."
      // If it's binary, the SDK might return it as string? 
      // Let's assume the SDK handles base64 encoding for binary files or we check how to get binary.
      // Looking at SDK source or docs is safer.
      // Based on common patterns in this SDK, it likely returns content. 
      // If it's an image, we hope it's base64 encoded or we can request it.
      // But `readFile` usually returns string.
      
      // Let's assume for now we can get base64 if we use a specific API or the content is just raw string we can encode?
      // Actually, standard `readFile` in this SDK (from earlier grep) returned `content`. 
      // If `code_latest` python environment saves to `/tmp/chart.png`, 
      // we might need to read it as base64.
      // Hack: In python code, we can force base64 output if we are unsure about `readFile` binary support.
      // But the prompt says "use plt.savefig('/tmp/chart.png')".
      // I'll assume readFile works or try to read it.
      
      // Wait, if I cannot be sure about readFile binary support, 
      // I can add a post-processing step in Python to base64 encode the image to a text file, 
      // then read the text file. This is safer.
      
      const base64Code = `
import base64
import os
if os.path.exists('${chartPath}'):
    with open('${chartPath}', 'rb') as f:
        print(base64.b64encode(f.read()).decode('utf-8'))
else:
    print("")
`;
      const base64Result = await session.code.runCode(base64Code, 'python');
      if (base64Result.success && base64Result.result && base64Result.result.trim().length > 0) {
        const base64Str = base64Result.result.trim();
        // Determine mime type (png)
        chartUrls.push(`data:image/png;base64,${base64Str}`);
        
        // Cleanup chart file
        await session.command.executeCommand(`rm ${chartPath}`);
      }
    }

    return {
      hasError: false,
      output: output,
      logs: logs,
      chartUrls: chartUrls,
    };

  } catch (error: any) {
    console.error('Execution error:', error);
    return {
      hasError: true,
      output: '',
      error: error.message,
      logs: [...logs, `❌ System error: ${error.message}`],
    };
  }
}

