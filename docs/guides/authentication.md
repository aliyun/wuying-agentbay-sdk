# Authentication

This guide explains how to authenticate with the Wuying AgentBay SDK.

## Overview

Authentication with the Wuying AgentBay SDK is done using an API key. This key is used to authenticate all requests to the AgentBay cloud environment.

## Authentication Methods

There are two main ways to provide your API key:

1. **Direct Initialization**: Provide the API key directly when initializing the AgentBay client.
2. **Environment Variable**: Set the `AGENTBAY_API_KEY` environment variable, and the SDK will use it automatically.

## Examples

### Golang

```go
// Method 1: Direct initialization with API key
apiKey := "your_api_key_here"
client, err := agentbay.NewAgentBay(apiKey)
if err != nil {
    fmt.Printf("Error initializing AgentBay client: %v\n", err)
    os.Exit(1)
}

// Method 2: Using environment variable
// First, set the environment variable:
// export AGENTBAY_API_KEY=your_api_key_here
client, err := agentbay.NewAgentBay("")
if err != nil {
    fmt.Printf("Error initializing AgentBay client: %v\n", err)
    os.Exit(1)
}
```

### Python

```python
# Method 1: Direct initialization with API key
api_key = "your_api_key_here"
agent_bay = AgentBay(api_key=api_key)

# Method 2: Using environment variable
# First, set the environment variable:
# export AGENTBAY_API_KEY=your_api_key_here
agent_bay = AgentBay()
```

### TypeScript

```typescript
// Method 1: Direct initialization with API key
const apiKey = 'your_api_key_here';
const agentBay = new AgentBay({ apiKey });

// Method 2: Using environment variable
// First, set the environment variable:
// export AGENTBAY_API_KEY=your_api_key_here
const agentBay = new AgentBay();
```

## Best Practices

1. **Environment Variables**: For production applications, it's recommended to use environment variables rather than hardcoding API keys in your code.

2. **Secure Storage**: Store your API keys securely and never commit them to version control systems.

3. **Key Rotation**: Periodically rotate your API keys to enhance security.

4. **Least Privilege**: Use API keys with the minimum required permissions for your application.

## Related Resources

- [Sessions](../concepts/sessions.md)
- [Error Handling](error-handling.md)
- [Best Practices](best-practices.md)
