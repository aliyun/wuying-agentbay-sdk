import { AgentBay } from 'wuying-agentbay-sdk';

async function main() {
  const apiKey = process.env.AGENTBAY_API_KEY;
  if (!apiKey) {
    console.error("Please set AGENTBAY_API_KEY environment variable");
    process.exit(1);
  }

  const agentBay = new AgentBay({ apiKey });

  console.log("Creating session...");
  const sessionResult = await agentBay.create({ imageId: "code_latest" });
  if (!sessionResult.success || !sessionResult.session) {
    console.error("Failed to create session:", sessionResult.errorMessage);
    process.exit(1);
  }

  const session = sessionResult.session;
  console.log(`Session created: ${session.sessionId}`);

  try {
    // 1. Logs Capture
    console.log("\n--- Logs Capture Test ---");
    const logsCode = `
import sys
print("This goes to stdout")
print("This goes to stderr", file=sys.stderr)
`;
    const logsResult = await session.code.runCode(logsCode, "python");
    printResult(logsResult);

    // 2. Rich Output (HTML)
    console.log("\n--- Rich Output (HTML) Test ---");
    const htmlCode = `
from IPython.display import display, HTML
display(HTML("<h1>Hello from AgentBay</h1>"))
`;
    const htmlResult = await session.code.runCode(htmlCode, "python");
    printResult(htmlResult);

    // 3. Error Handling
    console.log("\n--- Error Handling Test ---");
    const errorCode = `
raise ValueError("Something went wrong")
`;
    const errorResult = await session.code.runCode(errorCode, "python");
    printResult(errorResult);

  } finally {
    console.log("\nCleaning up...");
    await session.delete();
  }
}

function printResult(result: any) {
  if (result.success) {
    console.log("Success: true");
    if (result.logs) {
      if (result.logs.stdout.length > 0) {
        console.log("Stdout:", JSON.stringify(result.logs.stdout));
      }
      if (result.logs.stderr.length > 0) {
        console.log("Stderr:", JSON.stringify(result.logs.stderr));
      }
    }
    if (result.results) {
      console.log("Results count:", result.results.length);
      result.results.forEach((item: any, index: number) => {
        const types = Object.keys(item).filter(k => k !== 'isMainResult');
        console.log(`Result [${index}] types:`, types.join(", "));
        if (item.text) console.log(`  Text: ${item.text.substring(0, 50)}...`);
        if (item.html) console.log(`  HTML: ${item.html.substring(0, 50)}...`);
      });
    }
  } else {
    console.log("Success: false");
    console.log("Error Message:", result.errorMessage);
    if (result.error) {
      console.log("Error Details:", JSON.stringify(result.error));
    }
  }
}

main().catch(console.error);

