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

type ParsedRunCodeRich = {
  text: string;
  imageDataUris: string[];
};

function parseRunCodeRichOutput(runResult: any): ParsedRunCodeRich {
  const imageDataUris: string[] = [];

  // Newer SDKs may expose structured results directly.
  if (Array.isArray(runResult?.results)) {
    for (const res of runResult.results) {
      if (res?.png && typeof res.png === 'string' && res.png.length > 0) {
        imageDataUris.push(`data:image/png;base64,${res.png}`);
      }
      if (res?.jpeg && typeof res.jpeg === 'string' && res.jpeg.length > 0) {
        imageDataUris.push(`data:image/jpeg;base64,${res.jpeg}`);
      }
    }

    const textCandidate =
      runResult?.result && typeof runResult.result === 'string' ? runResult.result : '';
    return { text: textCandidate, imageDataUris };
  }

  // SDK v0.12.0 returns raw backend JSON as a string in `result`.
  const rawText = runResult?.result && typeof runResult.result === 'string' ? runResult.result : '';
  if (!rawText) {
    return { text: '', imageDataUris: [] };
  }

  let raw: any;
  try {
    raw = JSON.parse(rawText);
    if (typeof raw === 'string') {
      try {
        raw = JSON.parse(raw);
      } catch {
        // keep as string
      }
    }
  } catch {
    return { text: rawText, imageDataUris: [] };
  }

  const stdout: string[] = Array.isArray(raw?.stdout) ? raw.stdout : [];
  const stderr: string[] = Array.isArray(raw?.stderr) ? raw.stderr : [];
  const outputText = stdout.length > 0 ? stdout.join('') : stderr.length > 0 ? stderr.join('') : '';

  const flattenedResultItems: any[] = [];
  if (Array.isArray(raw?.result)) {
    for (const entry of raw.result) {
      if (Array.isArray(entry)) {
        flattenedResultItems.push(...entry);
      } else {
        flattenedResultItems.push(entry);
      }
    }
  }

  let mainText = outputText;
  for (const itemRaw of flattenedResultItems) {
    let itemMap: any = itemRaw;
    try {
      if (typeof itemMap === 'string') {
        itemMap = JSON.parse(itemMap);
        if (typeof itemMap === 'string') {
          itemMap = JSON.parse(itemMap);
        }
      }
    } catch {
      continue;
    }

    if (itemMap && typeof itemMap === 'object') {
      const png = itemMap['image/png'];
      if (typeof png === 'string' && png.length > 0) {
        imageDataUris.push(`data:image/png;base64,${png}`);
      }

      const jpeg = itemMap['image/jpeg'];
      if (typeof jpeg === 'string' && jpeg.length > 0) {
        imageDataUris.push(`data:image/jpeg;base64,${jpeg}`);
      }

      const plain = itemMap['text/plain'];
      const isMain = itemMap.isMainResult === true || itemMap.is_main_result === true;
      if (!mainText && typeof plain === 'string' && plain.length > 0) {
        mainText = plain;
      }
      if (isMain && typeof plain === 'string' && plain.length > 0) {
        mainText = plain;
      }
    }
  }

  // If backend didn't produce a good text output, fall back to the raw JSON string.
  return { text: mainText || rawText, imageDataUris };
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

    const parsed = parseRunCodeRichOutput(runResult);
    const output = parsed.text || '';
    logs.push('✅ Code executed successfully.');

    // 3. Check for generated charts
    const chartUrls: string[] = parsed.imageDataUris;
    if (chartUrls.length > 0) {
      logs.push(`📊 Captured ${chartUrls.length} image output(s) from runCode rich result.`);
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

