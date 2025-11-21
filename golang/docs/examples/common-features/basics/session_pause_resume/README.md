# Session Pause and Resume Example

This example demonstrates how to use the `Pause` and `Resume` APIs to manage session lifecycle and reduce resource consumption.

## Description

The pause/resume feature allows you to temporarily suspend a session to reduce computational resource usage and costs, and then restore it later to continue work. This is particularly useful for long-running sessions where work may be intermittent.

## Prerequisites

- Go 1.21 or higher
- Valid API key set in `AGENTBAY_API_KEY` environment variable

## Usage

```bash
# Set your API key
export AGENTBAY_API_KEY="your-api-key-here"

# Run the example
go run main.go
```

## Code Example

```go
package main

import (
    "fmt"
    "log"
    "os"
    "time"

    "github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

func main() {
    // Initialize AgentBay client
    apiKey := os.Getenv("AGENTBAY_API_KEY")
    client, err := agentbay.NewAgentBay(apiKey, nil)
    if err != nil {
        log.Fatalf("Failed to initialize AgentBay client: %v", err)
    }

    // Create a session
    createResult, err := client.Create(nil)
    if err != nil {
        log.Fatalf("Failed to create session: %v", err)
    }
    session := createResult.Session
    defer session.Delete()

    // Perform some work
    commandResult, _ := session.Command.ExecuteCommand("echo 'Hello World'", 30000)
    fmt.Printf("Command output: %s\n", commandResult.Output)

    // Pause the session to save resources
    pauseResult, err := client.Pause(session, 300, 2.0)
    if err != nil {
        log.Fatalf("Failed to pause session: %v", err)
    }
    if !pauseResult.Success {
        log.Fatalf("Failed to pause session: %s", pauseResult.ErrorMessage)
    }
    fmt.Printf("Session paused (RequestID: %s)\n", pauseResult.RequestID)

    // Wait and verify session is paused
    time.Sleep(2 * time.Second)
    getResult, _ := client.GetSession(session.SessionID)
    fmt.Printf("Session status: %s\n", getResult.Data.Status)

    // Resume the session
    resumeResult, err := client.Resume(session, 300, 2.0)
    if err != nil {
        log.Fatalf("Failed to resume session: %v", err)
    }
    if !resumeResult.Success {
        log.Fatalf("Failed to resume session: %s", resumeResult.ErrorMessage)
    }
    fmt.Printf("Session resumed (RequestID: %s)\n", resumeResult.RequestID)

    // Continue working with the session
    commandResult, _ = session.Command.ExecuteCommand("echo 'Hello after resume'", 30000)
    fmt.Printf("Command output: %s\n", commandResult.Output)
}
```

## API Reference

### Pause

```go
func (ab *AgentBay) Pause(session *Session, timeout int, pollInterval float64) (*models.SessionPauseResult, error)
```

Synchronously pauses a session, putting it into a dormant state to reduce resource usage and costs.

**Parameters:**
- `session` (*Session): The session to pause
- `timeout` (int): Timeout in seconds to wait for the session to pause. Defaults to 600 seconds
- `pollInterval` (float64): Interval in seconds between status polls. Defaults to 2.0 seconds

**Returns:**
- `*models.SessionPauseResult`: Result object containing:
  - `Success` (bool): Whether the operation succeeded
  - `RequestID` (string): The API request ID
  - `ErrorMessage` (string): Error message if failed
  - `Status` (string): Final session status
- `error`: An error if a critical operation fails

### Resume

```go
func (ab *AgentBay) Resume(session *Session, timeout int, pollInterval float64) (*models.SessionResumeResult, error)
```

Synchronously resumes a session from a paused state to continue work.

**Parameters:**
- `session` (*Session): The session to resume
- `timeout` (int): Timeout in seconds to wait for the session to resume. Defaults to 600 seconds
- `pollInterval` (float64): Interval in seconds between status polls. Defaults to 2.0 seconds

**Returns:**
- `*models.SessionResumeResult`: Result object containing:
  - `Success` (bool): Whether the operation succeeded
  - `RequestID` (string): The API request ID
  - `ErrorMessage` (string): Error message if failed
  - `Status` (string): Final session status
- `error`: An error if a critical operation fails

## Expected Output

```
Creating a session...
Created session with ID: session-xxxxxxxxxxxxx

1. Verifying session is running...
Session status: RUNNING

2. Performing work on the session...
Command output: Hello from AgentBay session

3. Pausing the session...
Session paused successfully (RequestID: XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX)

4. Verifying session is paused...
Session status: PAUSED

5. Attempting work on paused session...
Expected: Command failed on paused session: ...

6. Resuming the session...
Session resumed successfully (RequestID: XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX)

7. Verifying session is running again...
Session status: RUNNING

8. Performing work on the resumed session...
Command output: Hello from resumed session

Example completed successfully!

Cleaning up...
Session session-xxxxxxxxxxxxx deleted successfully
```

## Notes

- Sessions in PAUSED state consume significantly fewer resources
- Operations on paused sessions will typically fail or wait until the session is resumed
- Both Pause and Resume are synchronous operations that wait for the session to reach the target state
- Use appropriate timeout values based on your workload requirements
- Always handle errors appropriately in production code