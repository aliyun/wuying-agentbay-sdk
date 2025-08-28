# Installation and Configuration

## System Requirements

### Python
- Python 3.10+
- pip or poetry

### TypeScript/JavaScript
- Node.js 14+
- npm or yarn

### Golang
- Go 1.24+

## Installing the SDK

### Python
```bash
# Install using pip
pip install wuying-agentbay-sdk

# Verify installation
python -c "import agentbay; print('Installation successful')"
```

### TypeScript
```bash
# Install using npm
npm install wuying-agentbay-sdk

# Verify installation
node -e "const {AgentBay} = require('wuying-agentbay-sdk'); console.log('Installation successful')"
```

### Golang
```bash
# Install the package
go get github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay

# Verify installation (create test file) Use bash command
echo 'package main

import (
    "fmt"
	"testing"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
	"github.com/aliyun/wuying-agentbay-sdk/golang/tests/pkg/agentbay/testutil"
)

func main() {
    testAPIKey := testutil.GetTestAPIKey(&testing.T{})

	agentbay.NewAgentBay(testAPIKey)
	fmt.Println("Installation successful")
}' > test.go
go run test.go
rm test.go
```

## Getting API Keys

### Step 1: Register an Alibaba Cloud Account
Visit [https://aliyun.com](https://aliyun.com) to register an account

### Step 2: Obtain API Keys
1. Log in to the [AgentBay Console](https://agentbay.console.aliyun.com/service-management)
2. Find API Key Management in the Service Management page
3. Create a new API key
4. Copy the key for later use

## Configuring API Keys

# Method 1: Environment Variables (Recommended)
- For Linux/MacOS:
```bash
    export AGENTBAY_API_KEY=your_api_key_here
```
- For Windows:
```cmd
    setx AGENTBAY_API_KEY your_api_key_here
```

## Go
```go
import (
	"testing"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
	"github.com/aliyun/wuying-agentbay-sdk/golang/tests/pkg/agentbay/testutil"
)

    testAPIKey := testutil.GetTestAPIKey(&testing.T{})
    agentbay.NewAgentBay(testAPIKey, nil)
```

## TypeScript
```typescript
import { AgentBay,logError,log } from 'wuying-agentbay-sdk';

    const apiKey = process.env.AGENTBAY_API_KEY || 'akm-xxx'; // Replace with your actual API key
    if (!process.env.AGENTBAY_API_KEY) {
      log('Warning: Using placeholder API key. Set AGENTBAY_API_KEY environment variable for production use.');
    }
    new AgentBay({apiKey});
```

## Python
```python
import os
from agentbay import AgentBay
    api_key = os.getenv("AGENTBAY_API_KEY")
    if not api_key:
        api_key = "akm-xxx"  # Replace with your actual API key for testing
        print(
            "Warning: Using default API key. Set AGENTBAY_API_KEY environment variable for production use."
        )

    # Create session and execute command
    AgentBay(api_key=api_key)
```

## Verifying Configuration

Create a simple test program to verify everything is working:

### Python Test
```python
from agentbay import AgentBay

try:
    # Use API key to initialize SDK
    # apikey by getting os env
    agent_bay = AgentBay(api_key=apikey)
    print("✅ SDK initialized successfully")

    # Create session
    session_result = agent_bay.create()
    session = session_result.session
    print("✅ Session created successfully")

    # Execute command
    result = session.command.execute_command("echo Hello AgentBay")
    print("✅ Command executed successfully:", result.output)

    # Release session
    agent_bay.delete(session)
    print("✅ Session released successfully")

except Exception as e:
    print(f"❌ Configuration issue: {e}")
```

### TypeScript Test
```typescript
import { AgentBay,log,logError } from 'wuying-agentbay-sdk';

async function test() {
    try {
        // Use API key to initialize SDK
        // apikey by getting os env
        const agentBay = new AgentBay({ apiKey });
        log("✅ SDK initialized successfully");

        // Create session
        const sessionResult = await agentBay.create();
        const session = sessionResult.session;
        log("✅ Session created successfully");

        // Execute command
        const result = await session.command.executeCommand("echo Hello AgentBay");
        log("✅ Command executed successfully:", result.output);

        // Release session
        await agentBay.delete(session);
        log("✅ Session released successfully");

    } catch (error) {
        logError(`❌ Configuration issue: ${error}`);
    }
}

test();
```

### Golang Test
```go
package main

import (
    "fmt"
    "github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

func main() {
    // Use API key to initialize client
    // get testAPIKey from os env
    client, err := agentbay.NewAgentBay(testAPIKey, nil)
    if err != nil {
        fmt.Printf("❌ Failed to initialize SDK: %v\n", err)
        return
    }
    fmt.Println("✅ SDK initialized successfully")

    // Create session
    sessionResult, err := client.Create(nil)
    if err != nil {
        fmt.Printf("❌ Failed to create session: %v\n", err)
        return
    }
    fmt.Println("✅ Session created successfully")

    // Check if session is nil
    if sessionResult.Session == nil {
        fmt.Println("❌ Session object is nil")
        return
    }

    // Execute command
    result, err := sessionResult.Session.Command.ExecuteCommand("echo Hello AgentBay")
    if err != nil {
        fmt.Printf("❌ Failed to execute command: %v\n", err)
        return
    }
    fmt.Printf("✅ Command executed successfully: %s\n", result.Output)

    // Release session
    _, err = client.Delete(sessionResult.Session, false)
    if err != nil {
        fmt.Printf("❌ Failed to release session: %v\n", err)
        return
    }
    fmt.Println("✅ Session released successfully")
}
```

## 🎉 Installation Complete!

If all the above tests pass, congratulations! You have successfully installed and configured the AgentBay SDK!

Next step: [Understanding Basic Concepts](basic-concepts.md)
