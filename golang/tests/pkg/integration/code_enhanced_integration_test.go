package integration_test

import (
	"strings"
	"testing"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
	"github.com/aliyun/wuying-agentbay-sdk/golang/tests/pkg/agentbay/testutil"
)

// TestCodeEnhancedIntegration tests the enhanced code execution functionality
func TestCodeEnhancedIntegration(t *testing.T) {
	apiKey := testutil.GetTestAPIKey(t)
	agentBay, err := agentbay.NewAgentBay(apiKey)
	if err != nil {
		t.Fatalf("Error initializing AgentBay client: %v", err)
	}

	// Create a session with code_latest image
	t.Log("Creating session with code_latest image...")
	params := agentbay.NewCreateSessionParams().WithImageId("code_latest")
	sessionResult, err := agentBay.Create(params)
	if err != nil {
		t.Fatalf("Error creating session: %v", err)
	}
	session := sessionResult.Session
	t.Logf("Session created with ID: %s", session.SessionID)

	defer func() {
		agentBay.Delete(session)
	}()

	// Test 1: Enhanced Result Structure
	t.Run("EnhancedResultStructure", func(t *testing.T) {
		code := `
print("Hello, enhanced world!")
42
`
		result, err := session.Code.RunCode(code, "python")
		if err != nil {
			t.Fatalf("Error executing code: %v", err)
		}

		// Check basic success
		if !result.Success {
			t.Errorf("Expected Success to be true")
		}
		if result.RequestID == "" {
			t.Error("RequestID should not be empty")
		}

		// Test backward compatibility
		if !strings.Contains(result.Output, "Hello, enhanced world!") && !strings.Contains(result.Output, "42") {
			t.Errorf("Expected output to contain 'Hello, enhanced world!' or '42', got: %s", result.Output)
		}

		// Test enhanced features
		if result.Logs == nil {
			t.Error("Expected Logs to be non-nil")
		}
		if result.Results == nil {
			t.Error("Expected Results to be non-nil")
		}
		// ExecutionTime might be 0 or missing depending on backend
		if result.ExecutionTime < 0 {
			t.Error("Expected ExecutionTime to be >= 0")
		}
	})

	// Test 2: Logs Capture
	t.Run("LogsCapture", func(t *testing.T) {
		code := `
import sys
print("This goes to stdout")
print("This also goes to stdout", file=sys.stdout)
print("This goes to stderr", file=sys.stderr)
"Final result"
`
		result, err := session.Code.RunCode(code, "python")
		if err != nil {
			t.Fatalf("Error executing code: %v", err)
		}

		if result.Logs == nil {
			t.Fatal("Logs is nil")
		}

		stdout := strings.Join(result.Logs.Stdout, "")
		stderr := strings.Join(result.Logs.Stderr, "")
		combined := stdout + stderr

		if !strings.Contains(combined, "This goes to stdout") {
			t.Errorf("Output missing expected stdout content: %s", combined)
		}
		if !strings.Contains(combined, "This goes to stderr") {
			t.Errorf("Output missing expected stderr content: %s", combined)
		}
	})

	// Test 3: Error Details
	t.Run("ErrorDetails", func(t *testing.T) {
		code := `
# This should cause a NameError
print(undefined_variable_that_does_not_exist)
`
		result, err := session.Code.RunCode(code, "python")

		// If RunCode returns error, we check if it's the expected one (execution failed)
		// Ideally we want it to return a Result with Success=false
		if err != nil {
			// Check if error message contains the JSON or expected error text
			if !strings.Contains(err.Error(), "name 'undefined_variable_that_does_not_exist' is not defined") {
				t.Errorf("Expected error message to contain 'undefined_variable...', got: %v", err)
			}
		} else {
			hasError := !result.Success || result.Error != nil || result.ErrorMessage != "" || (result.Logs != nil && len(result.Logs.Stderr) > 0)
			if !hasError {
				t.Error("Expected error indication in result")
			}
		}
	})

	// Test 4: Rich Outputs (HTML, Markdown)
	t.Run("RichOutputs", func(t *testing.T) {
		code := `
from IPython.display import display, HTML, Markdown
display(HTML("<h1>Hello HTML</h1>"))
display(Markdown('# Hello Markdown'))
`
		result, err := session.Code.RunCode(code, "python")
		if err != nil {
			t.Fatalf("Error executing code: %v", err)
		}

		hasHTML := false
		hasMarkdown := false
		for _, res := range result.Results {
			if strings.Contains(res.HTML, "<h1>Hello HTML</h1>") {
				hasHTML = true
			}
			if strings.Contains(res.Markdown, "# Hello Markdown") {
				hasMarkdown = true
			}
		}

		if !hasHTML {
			t.Error("HTML output not found")
		}
		if !hasMarkdown {
			t.Error("Markdown output not found")
		}
	})

	// Test 5: Image Output (PNG/JPEG)
	t.Run("ImageOutput", func(t *testing.T) {
		code := `
import matplotlib.pyplot as plt

plt.figure()
plt.plot([1, 2, 3], [1, 2, 3])
plt.title("Test Plot")
plt.show()
`
		result, err := session.Code.RunCode(code, "python")
		if err != nil {
			t.Fatalf("Error executing code: %v", err)
		}

		hasImage := false
		for _, res := range result.Results {
			if res.PNG != "" || res.JPEG != "" {
				hasImage = true
				break
			}
		}

		if !hasImage {
			t.Error("Image output (PNG/JPEG) not found in results")
		}
	})

	// Test 6: SVG Output
	t.Run("SVGOutput", func(t *testing.T) {
		code := `
from IPython.display import display, SVG

svg_code = '<svg height="100" width="100"><circle cx="50" cy="50" r="40" stroke="black" stroke-width="3" fill="red" /></svg>'
display(SVG(svg_code))
`
		result, err := session.Code.RunCode(code, "python")
		if err != nil {
			t.Fatalf("Error executing code: %v", err)
		}

		hasSVG := false
		for _, res := range result.Results {
			if res.SVG != "" && strings.Contains(res.SVG, "<svg") {
				hasSVG = true
				break
			}
		}

		if !hasSVG {
			t.Error("SVG output not found in results")
		}
	})

	// Test 7: LaTeX Output
	t.Run("LatexOutput", func(t *testing.T) {
		code := `
from IPython.display import display, Latex

display(Latex(r'\frac{1}{2}'))
`
		result, err := session.Code.RunCode(code, "python")
		if err != nil {
			t.Fatalf("Error executing code: %v", err)
		}

		hasLatex := false
		for _, res := range result.Results {
			if res.Latex != "" && strings.Contains(res.Latex, "frac{1}{2}") {
				hasLatex = true
				break
			}
		}

		if !hasLatex {
			t.Error("LaTeX output not found in results")
		}
	})

	// Test 8: Chart Output (Vega-Lite)
	t.Run("ChartOutput", func(t *testing.T) {
		code := `
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
`
		result, err := session.Code.RunCode(code, "python")
		if err != nil {
			t.Fatalf("Error executing code: %v", err)
		}

		v4Found := false
		v5Found := false

		for _, res := range result.Results {
			if res.Chart != nil {
				// We need to inspect the chart data to distinguish versions
				// In Go we get map[string]interface{}
				chartData, ok := res.Chart.(map[string]interface{})
				if ok {
					if dataVal, ok := chartData["data"].(string); ok {
						if dataVal == "mock_v4" {
							v4Found = true
						} else if dataVal == "mock_v5" {
							v5Found = true
						}
					}
				}
			}
		}

		if !v4Found {
			t.Error("Vega-Lite V4 output not found")
		}
		if !v5Found {
			t.Error("Vega-Lite V5 output not found")
		}
	})

	// Test 9: Mixed Output Types
	t.Run("MixedOutputTypes", func(t *testing.T) {
		code := `
import json
print("Starting mixed output test")

# Text output
text_data = "Simple text"
print(f"Text: {text_data}")

# JSON-like output
json_data = {"type": "test", "values": [1, 2, 3]}
print("JSON:", json.dumps(json_data))

# Final result
"Mixed output test completed"
`
		result, err := session.Code.RunCode(code, "python")
		if err != nil {
			t.Fatalf("Error executing code: %v", err)
		}

		// Verify standard logs
		combined := ""
		if result.Logs != nil {
			combined = strings.Join(result.Logs.Stdout, "")
		}
		if !strings.Contains(combined, "Starting mixed output test") {
			t.Errorf("Logs missing expected content: %s", combined)
		}

		// Verify result
		if !strings.Contains(result.Result, "Mixed output test completed") {
			t.Errorf("Result missing expected content: %s", result.Result)
		}
	})

	// Test 10: Execution Count
	t.Run("ExecutionCount", func(t *testing.T) {
		code1 := "print('First')"
		code2 := "print('Second')"

		res1, _ := session.Code.RunCode(code1, "python")
		res2, _ := session.Code.RunCode(code2, "python")

		if res1.ExecutionCount != nil && res2.ExecutionCount != nil {
			t.Logf("Execution counts: %d, %d", *res1.ExecutionCount, *res2.ExecutionCount)
		}
	})
}
