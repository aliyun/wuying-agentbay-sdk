# Installation and Configuration

## System Requirements

### Python
- Python 3.8+
- pip or poetry

### TypeScript/JavaScript
- Node.js 14+
- npm or yarn

### Golang
- Go 1.18+

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

# Verify installation (create test file)
echo 'package main
import "github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
func main() { println("Installation successful") }' > test.go
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

### Method 1: Environment Variables (Recommended)
```bash
export AGENTBAY_API_KEY=your_api_key_here
```

### Method 2: Setting in Code
```python
# Python
from agentbay import AgentBay
agent_bay = AgentBay(api_key="your_api_key_here")
```

```typescript
// TypeScript
import { AgentBay } from 'wuying-agentbay-sdk';
const agentBay = new AgentBay({ apiKey: 'your_api_key_here' });
```

```go
// Golang
client, err := agentbay.NewAgentBay("your_api_key_here", nil)
```

## Verifying Configuration

Create a simple test program to verify everything is working:

### Python Test
```python
from agentbay import AgentBay

try:
    # Use API key to initialize SDK
    agent_bay = AgentBay(api_key="your_actual_api_key_here")
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
import { AgentBay } from 'wuying-agentbay-sdk';

async function test() {
    try {
        // Use API key to initialize SDK
        const agentBay = new AgentBay({ apiKey: "your_actual_api_key_here" });
        console.log("✅ SDK initialized successfully");
        
        // Create session
        const sessionResult = await agentBay.create();
        const session = sessionResult.session;
        console.log("✅ Session created successfully");
        
        // Execute command
        const result = await session.command.executeCommand("echo Hello AgentBay");
        console.log("✅ Command executed successfully:", result.output);
        
        // Release session
        await agentBay.delete(session);
        console.log("✅ Session released successfully");
        
    } catch (error) {
        console.log(`❌ Configuration issue: ${error}`);
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
    client, err := agentbay.NewAgentBay("your_actual_api_key_here", nil)
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