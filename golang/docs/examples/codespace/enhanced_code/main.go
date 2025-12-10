package main

import (
	"fmt"
	"os"
	"strings"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/code"
)

func main() {
	apiKey := os.Getenv("AGENTBAY_API_KEY")
	if apiKey == "" {
		fmt.Println("AGENTBAY_API_KEY environment variable not set")
		return
	}

	// 1. Initialize AgentBay client
	client, err := agentbay.NewAgentBay(apiKey)
	if err != nil {
		fmt.Printf("Failed to create client: %v\n", err)
		return
	}

	// 2. Create a session with code environment
	fmt.Println("Creating session...")
	params := agentbay.NewCreateSessionParams().WithImageId("code_latest")
	sessionResult, err := client.Create(params)
	if err != nil {
		fmt.Printf("Failed to create session: %v\n", err)
		return
	}
	session := sessionResult.Session
	defer func() {
		fmt.Println("Cleaning up session...")
		client.Delete(session)
	}()
	fmt.Printf("Session created: %s\n", session.SessionID)

	// 3. Execute code with logs (stdout/stderr)
	fmt.Println("\n--- Test 1: Logs Capture ---")
	code1 := `
import sys
print("This is stdout message")
print("This is stderr message", file=sys.stderr)
`
	result1, err := session.Code.RunCode(code1, "python")
	if err != nil {
		fmt.Printf("Execution failed: %v\n", err)
	} else {
		printResult(result1)
	}

	// 4. Execute code with rich output (HTML, Markdown)
	fmt.Println("\n--- Test 2: Rich Output ---")
	code2 := `
from IPython.display import display, HTML, Markdown
display(HTML("<h3>Hello from HTML</h3>"))
display(Markdown("**Hello from Markdown**"))
"Final text result"
`
	result2, err := session.Code.RunCode(code2, "python")
	if err != nil {
		fmt.Printf("Execution failed: %v\n", err)
	} else {
		printResult(result2)
	}

	// 5. Execute code with error
	fmt.Println("\n--- Test 3: Error Handling ---")
	code3 := `
# Division by zero
print(1/0)
`
	result3, err := session.Code.RunCode(code3, "python")
	if err != nil {
		// Note: Depending on implementation, RunCode might return error OR
		// return Success=false in result. We handle both.
		fmt.Printf("Execution returned error: %v\n", err)
	}

	if result3 != nil {
		printResult(result3)
	}
}

func printResult(res *code.CodeResult) {
	if res.Success {
		fmt.Println("✅ Execution Successful")
	} else {
		fmt.Println("❌ Execution Failed")
	}

	if res.Logs != nil {
		if len(res.Logs.Stdout) > 0 {
			fmt.Printf("stdout:\n%s\n", strings.Join(res.Logs.Stdout, ""))
		}
		if len(res.Logs.Stderr) > 0 {
			fmt.Printf("stderr:\n%s\n", strings.Join(res.Logs.Stderr, ""))
		}
	}

	if len(res.Results) > 0 {
		fmt.Println("Results:")
		for i, r := range res.Results {
			fmt.Printf("  Item %d:\n", i+1)
			if r.IsMainResult {
				fmt.Println("    (Main Result)")
			}
			if r.Text != "" {
				fmt.Printf("    Text: %s\n", r.Text)
			}
			if r.HTML != "" {
				fmt.Printf("    HTML: %s\n", r.HTML)
			}
			if r.Markdown != "" {
				fmt.Printf("    Markdown: %s\n", r.Markdown)
			}
		}
	} else if res.Result != "" {
		fmt.Printf("Result: %s\n", res.Result)
	}

	if res.Error != nil {
		fmt.Printf("Error Details:\n  Value: %s\n", res.Error.Value)
		if res.Error.Name != "" {
			fmt.Printf("  Name: %s\n", res.Error.Name)
		}
		if res.Error.Traceback != "" {
			fmt.Printf("  Traceback: %s\n", res.Error.Traceback)
		}
	} else if res.ErrorMessage != "" {
		fmt.Printf("Error Message: %s\n", res.ErrorMessage)
	}
}
