import { AgentBay, Session } from "../../src";
import { getTestApiKey } from "../utils/test-helpers";
import { log, logError } from "../../src/utils/logger";

describe("Enhanced Code Execution Integration Test", () => {
  let agentBay: AgentBay;
  let session: Session;

  // Increase timeout for all tests in this suite
  jest.setTimeout(120000);

  beforeAll(async () => {
    const apiKey = getTestApiKey();
    agentBay = new AgentBay({ apiKey });
    log("Creating session for enhanced code test...");
    // Ensure we use the image that supports enhanced code execution
    const createResponse = await agentBay.create({ imageId: "code_latest" });
    if (!createResponse.success || !createResponse.session) {
      throw new Error(`Failed to create session: ${createResponse.errorMessage}`);
    }
    session = createResponse.session;
    log(`Session created with ID: ${session.sessionId}`);
  });

  afterAll(async () => {
    if (session) {
      log(`Cleaning up session: ${session.sessionId}`);
      try {
        await session.delete();
      } catch (error) {
        logError("Failed to delete session:", error);
      }
    }
  });

  test("EnhancedResultStructure", async () => {
    if (!session || !session.code) {
      log("Note: Code interface is nil, skipping test");
      return;
    }

    const code = `
print("Hello, enhanced world!")
x = 42
x
`;
    const result = await session.code.runCode(code, "python");
    
    log("Enhanced Result:", JSON.stringify(result, null, 2));

    expect(result.success).toBe(true);
    
    // Check enhanced fields (using any cast until types are updated)
    const enhanced = result as any;
    expect(enhanced.logs).toBeDefined();
    expect(enhanced.logs.stdout).toBeDefined();
    expect(enhanced.logs.stdout.join("")).toContain("Hello, enhanced world!");

    expect(enhanced.results).toBeDefined();
    expect(enhanced.results.length).toBeGreaterThan(0);
    expect(enhanced.results[0].text).toContain("42");
    expect(enhanced.results[0].isMainResult).toBe(true);
    
    // executionTime might be undefined in some environments
    if (enhanced.executionTime !== undefined) {
      expect(typeof enhanced.executionTime).toBe("number");
    }
    // executionCount might be undefined/null if not supported or first run, but check existence logic
  }, 60000);

  test("LogsCapture", async () => {
    if (!session?.code) return;
    const code = `
import sys
print("This goes to stdout")
print("This also goes to stdout")
print("This goes to stderr", file=sys.stderr)
'Final result'
`;
    const result = await session.code.runCode(code, "python");
    const enhanced = result as any;
    
    const combinedStdout = enhanced.logs?.stdout?.join("") || "";
    const combinedStderr = enhanced.logs?.stderr?.join("") || "";
    const allLogs = combinedStdout + combinedStderr;

    expect(allLogs).toContain("This goes to stdout");
    expect(allLogs).toContain("This also goes to stdout");
    expect(allLogs).toContain("This goes to stderr");
    
    // Legacy output check
    expect(result.result).toContain("Final result");
  }, 60000);

  test("ErrorDetails", async () => {
    if (!session?.code) return;
    const code = `
undefined_variable_that_does_not_exist
`;
    const result = await session.code.runCode(code, "python");
    
    const enhanced = result as any;
    const errorMsg = "undefined_variable_that_does_not_exist";

    // The backend might return success=false (isError=true) but with empty executionError, 
    // putting the traceback in stderr. Or it might return success=true if the tool execution itself was fine.
    // We should check for the error message in any of the possible error locations.
    
    const stderr = enhanced.logs?.stderr?.join("") || "";
    const errorValue = enhanced.error?.value || "";
    const errorMessage = result.errorMessage || "";
    
    const hasError = stderr.includes(errorMsg) || 
                     errorValue.includes(errorMsg) || 
                     errorMessage.includes(errorMsg);
                     
    expect(hasError).toBe(true);
  }, 60000);

  test("RichOutputs", async () => {
    if (!session?.code) return;
    const code = `
from IPython.display import display, HTML, Markdown

display(HTML("<h1>Hello HTML</h1>"))
display(Markdown("# Hello Markdown"))
`;
    const result = await session.code.runCode(code, "python");
    const enhanced = result as any;
    
    let htmlFound = false;
    let markdownFound = false;

    for (const res of enhanced.results) {
        if (res.html && res.html.includes("<h1>Hello HTML</h1>")) {
            htmlFound = true;
        }
        if (res.markdown && res.markdown.includes("# Hello Markdown")) {
            markdownFound = true;
        }
    }

    expect(htmlFound).toBe(true);
    expect(markdownFound).toBe(true);
  }, 60000);

  test("ImageOutput", async () => {
      if (!session?.code) return;
      const code = `
import matplotlib.pyplot as plt

plt.figure()
plt.plot([1, 2, 3], [1, 2, 3])
plt.title("Test Plot")
plt.show()
`;
      const result = await session.code.runCode(code, "python");
      const enhanced = result as any;

      let hasImage = false;
      for (const res of enhanced.results) {
          if (res.png || res.jpeg) {
              hasImage = true;
              break;
          }
      }
      expect(hasImage).toBe(true);
  }, 60000);

  test("SVGOutput", async () => {
      if (!session?.code) return;
      const code = `
from IPython.display import display, SVG
svg_code = '<svg height="100" width="100"><circle cx="50" cy="50" r="40" stroke="black" stroke-width="3" fill="red" /></svg>'
display(SVG(svg_code))
`;
      const result = await session.code.runCode(code, "python");
      const enhanced = result as any;

      let hasSVG = false;
      for (const res of enhanced.results) {
          if (res.svg && res.svg.includes("<svg")) {
              hasSVG = true;
              break;
          }
      }
      expect(hasSVG).toBe(true);
  }, 60000);

  test("ChartOutput", async () => {
      if (!session?.code) return;
      const code = `
from IPython.display import display

class MockChartV4:
    def _repr_mimebundle_(self, include=None, exclude=None):
        return {
            "application/vnd.vegalite.v4+json": {"data": "mock_v4", "mark": "bar"},
            "text/plain": "MockChartV4"
        }

class MockChartV5:
    def _repr_mimebundle_(self, include=None, exclude=None):
        return {
            "application/vnd.vegalite.v5+json": {"data": "mock_v5", "mark": "line"},
            "text/plain": "MockChartV5"
        }

display(MockChartV4())
display(MockChartV5())
`;
      const result = await session.code.runCode(code, "python");
      const enhanced = result as any;
      
      let v4Found = false;
      let v5Found = false;
      
      for (const res of enhanced.results) {
          if (res.chart) {
              // TS might interpret as generic object
              const chartData = res.chart as any;
              if (chartData.data === "mock_v4") v4Found = true;
              if (chartData.data === "mock_v5") v5Found = true;
          }
      }
      
      expect(v4Found).toBe(true);
      expect(v5Found).toBe(true);
  }, 60000);

});

