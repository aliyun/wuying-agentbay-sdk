# Session Pause and Resume Example

This example demonstrates how to pause and resume sessions using the Wuying AgentBay SDK. Pausing a session puts it into a dormant state, consuming fewer resources while maintaining its state. Resuming a session brings it back to an active state.

## Features Demonstrated

- Pausing and resuming sessions
- Handling non-existent session operations
- Using custom timeout and polling interval parameters
- Checking session status before and after operations
- Performing work in sessions before and after pause/resume cycles

## Running the Example

```bash
cd session-pause-resume
npx ts-node session-pause-resume.ts
```

Make sure you have set the `AGENTBAY_API_KEY` environment variable or replace the placeholder in the code with your actual API key.

## Prerequisites

- Node.js installed
- TypeScript installed
- ts-node installed (`npm install -g ts-node`)
- Required dependencies installed (`npm install`)

## Understanding Session States

When working with pause and resume operations, sessions can be in different states:

1. **RUNNING**: Session is active and ready to accept commands
2. **PAUSING**: Session is transitioning to paused state
3. **PAUSED**: Session is in dormant state, consuming fewer resources
4. **RESUMING**: Session is transitioning back to running state

The pause and resume operations are asynchronous, meaning they initiate the state transition and then poll for completion.

## Best Practices

1. **Always check operation results**: Verify that pause and resume operations succeeded
2. **Handle errors gracefully**: Non-existent sessions and other errors should be handled appropriately
3. **Use appropriate timeouts**: Custom timeout values can be used based on your specific requirements
4. **Verify session state**: Check session status before and after operations to ensure expected behavior
5. **Clean up resources**: Always delete sessions when done to avoid resource leaks

## Use Cases

- **Cost optimization**: Pause sessions during idle periods to reduce resource consumption
- **Long-running workflows**: Suspend sessions overnight or during maintenance windows
- **Development and testing**: Pause test environments when not actively working on them
- **Batch processing**: Pause and resume processing jobs based on system load