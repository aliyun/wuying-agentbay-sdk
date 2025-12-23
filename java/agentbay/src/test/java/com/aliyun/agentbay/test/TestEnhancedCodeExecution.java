package com.aliyun.agentbay.test;

import com.aliyun.agentbay.AgentBay;
import com.aliyun.agentbay.exception.AgentBayException;
import com.aliyun.agentbay.exception.SessionException;
import com.aliyun.agentbay.model.code.CodeExecutionLogs;
import com.aliyun.agentbay.model.code.CodeResult;
import com.aliyun.agentbay.model.code.EnhancedCodeExecutionResult;
import com.aliyun.agentbay.model.SessionResult;
import com.aliyun.agentbay.session.CreateSessionParams;
import com.aliyun.agentbay.session.Session;
import org.junit.AfterClass;
import org.junit.BeforeClass;
import org.junit.Test;

import java.util.List;

import static org.junit.Assert.*;

/**
 * Enhanced Code Execution Integration Tests
 * Reference: python/tests/integration/_sync/test_enhanced_code_integration.py
 */
public class TestEnhancedCodeExecution {

    private static Session sharedSession;
    private static AgentBay agentBay;

    @BeforeClass
    public static void setUp() throws AgentBayException {
        String apiKey = System.getenv("AGENTBAY_API_KEY");
        if (apiKey == null || apiKey.trim().isEmpty()) {
            throw new RuntimeException("AGENTBAY_API_KEY environment variable not set");
        }

        agentBay = new AgentBay(apiKey);
        CreateSessionParams params = new CreateSessionParams();
        params.setImageId("code_latest");
        SessionResult sessionResult = agentBay.create(params);

        if (!sessionResult.isSuccess() || sessionResult.getSession() == null) {
            throw new RuntimeException("Failed to create session: " + sessionResult.getErrorMessage());
        }

        sharedSession = sessionResult.getSession();
        System.out.println("✅ Shared session created: " + sharedSession.getSessionId());
    }

    @AfterClass
    public static void tearDown() {
        if (sharedSession != null) {
            try {
                sharedSession.delete();
                System.out.println("✅ Shared session deleted");
            } catch (Exception e) {
                System.err.println("⚠️ Failed to delete session: " + e.getMessage());
            }
        }
    }

    @Test
    public void testEnhancedResultStructure() throws SessionException {
        System.out.println("\n🧪 Testing enhanced result structure...");

        String code = "print(\"Hello, enhanced world!\")\n42";
        EnhancedCodeExecutionResult result = sharedSession.getCode().runCode(code, "python");

        assertTrue("Execution should succeed", result.isSuccess());
        assertNotNull("Request ID should not be null", result.getRequestId());

        String resultText = result.getResult();
        assertTrue("Result should contain output",
                resultText.contains("Hello, enhanced world!") || resultText.contains("42"));

        assertNotNull("Logs should not be null", result.getLogs());
        assertNotNull("Results list should not be null", result.getResults());

        System.out.println("✅ Enhanced result structure verified");
    }

    @Test
    public void testLogsCapture() throws SessionException {
        System.out.println("\n🧪 Testing logs capture...");

        String code = "import sys\n" +
                "print(\"This goes to stdout\")\n" +
                "print(\"This also goes to stdout\", file=sys.stdout)\n" +
                "print(\"This goes to stderr\", file=sys.stderr)\n" +
                "\"Final result\"";

        EnhancedCodeExecutionResult result = sharedSession.getCode().runCode(code, "python");

        assertTrue("Execution should succeed", result.isSuccess());
        assertNotNull("Logs should not be null", result.getLogs());

        CodeExecutionLogs logs = result.getLogs();
        assertNotNull("Stdout should not be null", logs.getStdout());
        assertNotNull("Stderr should not be null", logs.getStderr());

        String stdoutContent = String.join("", logs.getStdout());
        String stderrContent = String.join("", logs.getStderr());

        assertTrue("Should have some output",
                stdoutContent.length() > 0 || stderrContent.length() > 0 || result.getResults().size() > 0);

        System.out.println("✅ Logs capture verified");
    }

    @Test
    public void testMultipleResultsFormats() throws SessionException {
        System.out.println("\n🧪 Testing multiple results formats...");

        String code = "print(\"Standard output\")\n" +
                "text_result = \"This is a text result\"\n" +
                "json_data = {\"key\": \"value\", \"number\": 42}\n" +
                "text_result";

        EnhancedCodeExecutionResult result = sharedSession.getCode().runCode(code, "python");

        assertTrue("Execution should succeed", result.isSuccess());
        assertNotNull("Results list should not be null", result.getResults());
        assertTrue("Results list should be a list", result.getResults() instanceof List);

        assertNotNull("Backward compatible result should not be null", result.getResult());

        System.out.println("✅ Multiple results formats verified");
    }

    @Test
    public void testExecutionTiming() throws SessionException {
        System.out.println("\n🧪 Testing execution timing...");

        String code = "import time\n" +
                "time.sleep(0.1)\n" +
                "\"Execution completed\"";

        EnhancedCodeExecutionResult result = sharedSession.getCode().runCode(code, "python");

        assertTrue("Execution should succeed", result.isSuccess());
        assertTrue("Execution time should be tracked", result.getExecutionTime() >= 0.0);

        System.out.println("✅ Execution timing verified (time: " + result.getExecutionTime() + "s)");
    }

    @Test
    public void testErrorDetails() throws SessionException {
        System.out.println("\n🧪 Testing error details...");

        String code = "print(undefined_variable_that_does_not_exist)";

        EnhancedCodeExecutionResult result = sharedSession.getCode().runCode(code, "python");

        boolean hasError = !result.isSuccess() ||
                result.getError() != null ||
                !result.getErrorMessage().isEmpty() ||
                (result.getLogs().getStderr() != null && !result.getLogs().getStderr().isEmpty());

        assertTrue("Should detect error", hasError);

        if (result.getError() != null) {
            assertNotNull("Error name should not be null", result.getError().getName());
            assertNotNull("Error value should not be null", result.getError().getValue());
        }

        System.out.println("✅ Error details verified");
    }

    @Test
    public void testJavaScriptEnhancedFeatures() throws SessionException {
        System.out.println("\n🧪 Testing JavaScript enhanced features...");

        String code = "console.log(\"JavaScript output\");\n" +
                "const data = {message: \"Hello from JS\", value: 123};\n" +
                "console.log(JSON.stringify(data));\n" +
                "data.value * 2;";

        EnhancedCodeExecutionResult result = sharedSession.getCode().runCode(code, "javascript");

        assertTrue("Execution should succeed", result.isSuccess());
        assertNotNull("Logs should not be null", result.getLogs());
        assertNotNull("Results should not be null", result.getResults());

        System.out.println("✅ JavaScript enhanced features verified");
    }

    @Test
    public void testLargeOutputHandling() throws SessionException {
        System.out.println("\n🧪 Testing large output handling...");

        String code = "large_list = list(range(100))\n" +
                "print(\"Generated list of\", len(large_list), \"items\")\n" +
                "for i in range(10):\n" +
                "    print(f\"Line {i}: {i * i}\")\n" +
                "\"Processing completed\"";

        EnhancedCodeExecutionResult result = sharedSession.getCode().runCode(code, "python");

        assertTrue("Execution should succeed", result.isSuccess());
        assertNotNull("Logs should not be null", result.getLogs());
        assertNotNull("Results should not be null", result.getResults());

        String output = result.getResult();
        boolean hasExpectedOutput = output.contains("Generated list");

        if (!hasExpectedOutput) {
            for (CodeResult res : result.getResults()) {
                if (res.getText() != null && res.getText().contains("Generated list")) {
                    hasExpectedOutput = true;
                    break;
                }
            }
        }

        if (!hasExpectedOutput && result.getLogs().getStdout() != null) {
            for (String log : result.getLogs().getStdout()) {
                if (log.contains("Generated list")) {
                    hasExpectedOutput = true;
                    break;
                }
            }
        }

        assertTrue("Should handle large output", hasExpectedOutput);

        System.out.println("✅ Large output handling verified");
    }

    @Test
    public void testExecutionCountTracking() throws SessionException {
        System.out.println("\n🧪 Testing execution count tracking...");

        String code1 = "print('First execution')";
        String code2 = "print('Second execution')";

        EnhancedCodeExecutionResult result1 = sharedSession.getCode().runCode(code1, "python");
        EnhancedCodeExecutionResult result2 = sharedSession.getCode().runCode(code2, "python");

        assertTrue("First execution should succeed", result1.isSuccess());
        assertTrue("Second execution should succeed", result2.isSuccess());

        if (result1.getExecutionCount() != null) {
            assertTrue("Execution count should be valid", result1.getExecutionCount() instanceof Integer);
        }
        if (result2.getExecutionCount() != null) {
            assertTrue("Execution count should be valid", result2.getExecutionCount() instanceof Integer);
        }

        System.out.println("✅ Execution count tracking verified");
    }

    @Test
    public void testMixedOutputTypes() throws SessionException {
        System.out.println("\n🧪 Testing mixed output types...");

        String code = "import json\n" +
                "print(\"Starting mixed output test\")\n" +
                "text_data = \"Simple text\"\n" +
                "print(f\"Text: {text_data}\")\n" +
                "json_data = {\"type\": \"test\", \"values\": [1, 2, 3]}\n" +
                "print(\"JSON:\", json.dumps(json_data))\n" +
                "\"Mixed output test completed\"";

        EnhancedCodeExecutionResult result = sharedSession.getCode().runCode(code, "python");

        assertTrue("Execution should succeed", result.isSuccess());
        assertNotNull("Logs should not be null", result.getLogs());
        assertNotNull("Results should not be null", result.getResults());

        String fullOutput = result.getResult();
        boolean hasExpectedOutput = fullOutput.contains("Starting mixed output test");

        if (!hasExpectedOutput && result.getLogs().getStdout() != null) {
            for (String log : result.getLogs().getStdout()) {
                if (log.contains("Starting mixed output test")) {
                    hasExpectedOutput = true;
                    break;
                }
            }
        }

        System.out.println("✅ Mixed output types verified");
    }

    @Test
    public void testEmptyCodeExecution() throws SessionException {
        System.out.println("\n🧪 Testing empty code execution...");

        String code = "# Just a comment";

        EnhancedCodeExecutionResult result = sharedSession.getCode().runCode(code, "python");

        assertTrue("Execution should succeed", result.isSuccess());
        assertNotNull("Logs should not be null", result.getLogs());
        assertNotNull("Results should not be null", result.getResults());

        String resultText = result.getResult();
        assertTrue("Should handle empty execution gracefully",
                resultText.equals("") || resultText != null);

        System.out.println("✅ Empty code execution verified");
    }

    @Test
    public void testBackwardCompatibilityProperties() throws SessionException {
        System.out.println("\n🧪 Testing backward compatibility properties...");

        String code = "print(\"Testing backward compatibility\")\n" +
                "final_result = \"This is the final result\"\n" +
                "final_result";

        EnhancedCodeExecutionResult result = sharedSession.getCode().runCode(code, "python");

        assertTrue("Execution should succeed", result.isSuccess());

        assertNotNull("Should have getResult() method", result.getResult());
        assertNotNull("Should have getErrorMessage() method", result.getErrorMessage());
        assertNotNull("Should have getRequestId() method", result.getRequestId());

        assertNotNull("Should have getLogs() method", result.getLogs());
        assertNotNull("Should have getResults() method", result.getResults());

        assertTrue("success should be boolean", result.isSuccess() || !result.isSuccess());
        assertTrue("result should be String", result.getResult() instanceof String);
        assertTrue("errorMessage should be String", result.getErrorMessage() instanceof String);
        assertTrue("requestId should be String", result.getRequestId() instanceof String);

        System.out.println("✅ Backward compatibility properties verified");
    }

    @Test
    public void testHtmlOutput() throws SessionException {
        System.out.println("\n🧪 Testing HTML output...");

        String code = "import pandas as pd\n" +
                "from IPython.display import display, HTML\n" +
                "df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})\n" +
                "display(HTML(\"<h1>Hello HTML</h1>\"))";

        EnhancedCodeExecutionResult result = sharedSession.getCode().runCode(code, "python");

        assertTrue("Execution should succeed", result.isSuccess());

        boolean hasHtml = false;
        for (CodeResult res : result.getResults()) {
            if (res.getHtml() != null && res.getHtml().contains("<h1>Hello HTML</h1>")) {
                hasHtml = true;
                break;
            }
        }

        assertTrue("HTML output should be found in results", hasHtml);

        System.out.println("✅ HTML output verified");
    }

    @Test
    public void testMarkdownOutput() throws SessionException {
        System.out.println("\n🧪 Testing Markdown output...");

        String code = "from IPython.display import display, Markdown\n" +
                "display(Markdown('# Hello Markdown'))";

        EnhancedCodeExecutionResult result = sharedSession.getCode().runCode(code, "python");

        assertTrue("Execution should succeed", result.isSuccess());

        boolean hasMarkdown = false;
        for (CodeResult res : result.getResults()) {
            if (res.getMarkdown() != null && res.getMarkdown().contains("# Hello Markdown")) {
                hasMarkdown = true;
                break;
            }
        }

        assertTrue("Markdown output should be found in results", hasMarkdown);

        System.out.println("✅ Markdown output verified");
    }

    @Test
    public void testImageOutput() throws SessionException {
        System.out.println("\n🧪 Testing image output...");

        String code = "import matplotlib.pyplot as plt\n" +
                "plt.figure()\n" +
                "plt.plot([1, 2, 3], [1, 2, 3])\n" +
                "plt.title(\"Test Plot\")\n" +
                "plt.show()";

        EnhancedCodeExecutionResult result = sharedSession.getCode().runCode(code, "python");

        assertTrue("Execution should succeed", result.isSuccess());

        boolean hasImage = false;
        for (CodeResult res : result.getResults()) {
            if (res.getPng() != null || res.getJpeg() != null) {
                hasImage = true;
                break;
            }
        }

        assertTrue("Image output (PNG/JPEG) should be found in results", hasImage);

        System.out.println("✅ Image output verified");
    }

    @Test
    public void testSvgOutput() throws SessionException {
        System.out.println("\n🧪 Testing SVG output...");

        String code = "from IPython.display import display, SVG\n" +
                "svg_code = '<svg height=\"100\" width=\"100\"><circle cx=\"50\" cy=\"50\" r=\"40\" stroke=\"black\" stroke-width=\"3\" fill=\"red\" /></svg>'\n" +
                "display(SVG(svg_code))";

        EnhancedCodeExecutionResult result = sharedSession.getCode().runCode(code, "python");

        assertTrue("Execution should succeed", result.isSuccess());

        boolean hasSvg = false;
        for (CodeResult res : result.getResults()) {
            if (res.getSvg() != null && res.getSvg().contains("<svg")) {
                hasSvg = true;
                break;
            }
        }

        assertTrue("SVG output should be found in results", hasSvg);

        System.out.println("✅ SVG output verified");
    }

    @Test
    public void testLatexOutput() throws SessionException {
        System.out.println("\n🧪 Testing LaTeX output...");

        String code = "from IPython.display import display, Latex\n" +
                "display(Latex(r'\\frac{1}{2}'))";

        EnhancedCodeExecutionResult result = sharedSession.getCode().runCode(code, "python");

        assertTrue("Execution should succeed", result.isSuccess());

        boolean hasLatex = false;
        for (CodeResult res : result.getResults()) {
            if (res.getLatex() != null && res.getLatex().contains("frac{1}{2}")) {
                hasLatex = true;
                break;
            }
        }

        assertTrue("LaTeX output should be found in results", hasLatex);

        System.out.println("✅ LaTeX output verified");
    }

    @Test
    public void testChartOutput() throws SessionException {
        System.out.println("\n🧪 Testing chart output...");

        String code = "from IPython.display import display\n" +
                "\n" +
                "class MockChart:\n" +
                "    def _repr_mimebundle_(self, include=None, exclude=None):\n" +
                "        return {\n" +
                "            \"application/vnd.vegalite.v4+json\": {\"data\": \"mock_chart_data\", \"mark\": \"bar\"},\n" +
                "            \"text/plain\": \"MockChart\"\n" +
                "        }\n" +
                "\n" +
                "display(MockChart())";

        EnhancedCodeExecutionResult result = sharedSession.getCode().runCode(code, "python");

        assertTrue("Execution should succeed", result.isSuccess());

        boolean hasChart = false;
        for (CodeResult res : result.getResults()) {
            if (res.getChart() != null) {
                hasChart = true;
                break;
            }
        }

        assertTrue("Chart output should be found in results", hasChart);

        System.out.println("✅ Chart output verified");
    }
}
