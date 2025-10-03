# Installation and Configuration

## 📋 System Requirements

### Python
- Python 3.10+
- pip or poetry

### TypeScript/JavaScript
- Node.js 14+
- npm or yarn

### Golang
- Go 1.24.4+

## 🚀 Quick Installation

### Python

**✅ Recommended: Using Virtual Environment**
```bash
# Create and activate virtual environment
python3 -m venv agentbay-env
source agentbay-env/bin/activate  # Linux/macOS
# agentbay-env\Scripts\activate   # Windows

# Install the package
pip install wuying-agentbay-sdk

# Verify installation
python -c "import agentbay; print('✅ Installation successful')"
```

**Alternative: Using System Python (if allowed)**
```bash
# Install with user flag (if system allows)
pip install --user wuying-agentbay-sdk

# Verify installation  
python -c "import agentbay; print('✅ Installation successful')"
```

### TypeScript/JavaScript

```bash
# Initialize project (if new project)
mkdir my-agentbay-project && cd my-agentbay-project
npm init -y

# Install the package
npm install wuying-agentbay-sdk

# Verify installation
node -e "const {AgentBay} = require('wuying-agentbay-sdk'); console.log('✅ Installation successful')"
```

### Golang

```bash
# Initialize module (if new project)
mkdir my-agentbay-project && cd my-agentbay-project  
go mod init my-agentbay-project

# Install the package
GOPROXY=direct go get github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay

# Verify installation
go list -m github.com/aliyun/wuying-agentbay-sdk/golang && echo "✅ Installation successful"
```

## 🔑 API Key Setup

### Step 1: Get API Key
1. Register at [https://aliyun.com](https://aliyun.com)
2. Visit [AgentBay Console](https://agentbay.console.aliyun.com/service-management)  
3. Create and copy your API key

### Step 2: Set Environment Variable

**Linux/macOS:**
```bash
export AGENTBAY_API_KEY=your_api_key_here
```

**Windows:**
```cmd
setx AGENTBAY_API_KEY your_api_key_here
```

## ✅ Installation Verification

Create a simple test to verify everything works with your API key:

### Python Test
```python
import os
from agentbay import AgentBay

# Get API key from environment
api_key = os.getenv("AGENTBAY_API_KEY")
if not api_key:
    print("⚠️  Please set AGENTBAY_API_KEY environment variable")
    exit(1)

try:
    # Initialize SDK
    agent_bay = AgentBay(api_key=api_key)
    print("✅ SDK initialized successfully")
    
    # Create a session (requires valid API key and network)
    session_result = agent_bay.create()
    if session_result.success:
        session = session_result.session
        print(f"✅ Session created: {session.session_id}")
        
        # Clean up
        agent_bay.delete(session)
        print("✅ Test completed successfully")
    else:
        print(f"⚠️  Session creation failed: {session_result.error_message}")
        
except Exception as e:
    print(f"❌ Error: {e}")
```

### TypeScript Test
```typescript
import { AgentBay } from 'wuying-agentbay-sdk';

const apiKey = process.env.AGENTBAY_API_KEY;
if (!apiKey) {
    console.log("⚠️  Please set AGENTBAY_API_KEY environment variable");
    process.exit(1);
}

async function test() {
    try {
        // Initialize SDK
        const agentBay = new AgentBay({ apiKey });
        console.log("✅ SDK initialized successfully");
        
        // Create a session (requires valid API key and network)
        const sessionResult = await agentBay.create();
        if (sessionResult.success) {
            const session = sessionResult.session;
            console.log(`✅ Session created: ${session.sessionId}`);
            
            // Clean up
            await agentBay.delete(session);
            console.log("✅ Test completed successfully");
        } else {
            console.log(`⚠️  Session creation failed: ${sessionResult.errorMessage}`);
        }
    } catch (error) {
        console.log(`❌ Error: ${error}`);
    }
}

test();
```

### Golang Test
```go
package main

import (
    "fmt"
    "os"
    "github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

func main() {
    // Get API key from environment
    apiKey := os.Getenv("AGENTBAY_API_KEY")
    if apiKey == "" {
        fmt.Println("⚠️  Please set AGENTBAY_API_KEY environment variable")
        return
    }

    // Initialize SDK
    client, err := agentbay.NewAgentBay(apiKey, nil)
    if err != nil {
        fmt.Printf("❌ Failed to initialize SDK: %v\n", err)
        return
    }
    fmt.Println("✅ SDK initialized successfully")

    // Create a session (requires valid API key and network)
    sessionResult, err := client.Create(nil)
    if err != nil {
        fmt.Printf("⚠️  Session creation failed: %v\n", err)
        return
    }
    
    if sessionResult.Session != nil {
        fmt.Printf("✅ Session created: %s\n", sessionResult.Session.SessionID)
        
        // Clean up
        _, err = client.Delete(sessionResult.Session, false)
        if err != nil {
            fmt.Printf("⚠️  Session cleanup failed: %v\n", err)
        } else {
            fmt.Println("✅ Test completed successfully")
        }
    }
}
```

## 🔧 Advanced Configuration (Optional)

### Using Configuration File

Create a `.env` file in your project root:
```env
AGENTBAY_API_KEY=your_api_key_here
AGENTBAY_REGION_ID=cn-shanghai
AGENTBAY_ENDPOINT=wuyingai.cn-shanghai.aliyuncs.com
AGENTBAY_TIMEOUT_MS=60000
```

### Programmatic Configuration

**Python:**
```python
from agentbay import AgentBay

agent_bay = AgentBay(
    api_key="your_api_key",
    region_id="cn-shanghai",
    endpoint="wuyingai.cn-shanghai.aliyuncs.com"
)
```

**TypeScript:**
```typescript
import { AgentBay } from 'wuying-agentbay-sdk';

const agentBay = new AgentBay({
    apiKey: "your_api_key",
    regionId: "cn-shanghai",
    endpoint: "wuyingai.cn-shanghai.aliyuncs.com"
});
```

## 🆘 Troubleshooting

### Python Issues

**`externally-managed-environment` error:**
```bash
# Solution: Use virtual environment
python3 -m venv agentbay-env
source agentbay-env/bin/activate
pip install wuying-agentbay-sdk
```

**`ModuleNotFoundError: No module named 'agentbay'`:**
```bash
# Check if virtual environment is activated
which python  # Should show venv path
# Re-install if needed
pip install --force-reinstall wuying-agentbay-sdk
```

**Permission denied errors:**
```bash
# Use user installation
pip install --user wuying-agentbay-sdk
```

### TypeScript Issues

**`Cannot find module 'wuying-agentbay-sdk'`:**
```bash
# Ensure you're in the project directory with package.json
pwd
ls package.json  # Should exist
# Re-install if needed
npm install wuying-agentbay-sdk
```

**`require() is not defined`:**
```bash
# Check Node.js version (requires 14+)
node --version
# Ensure you're using CommonJS (default) or update to ES modules
```

### Golang Issues

**`checksum mismatch` error (Most Common):**
```bash
# Always use direct proxy for this package
GOPROXY=direct go get github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay
```

**Import path errors:**
```bash
# Check Go version (requires 1.24.4+)
go version
# Ensure module is initialized
go mod init your-project-name
```

**Build failures:**
```bash
# Clean module cache and retry
go clean -modcache
go mod tidy
go get github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay
```

### Network and API Issues

**Connection timeouts:**
- Check your network connection
- Verify the endpoint region matches your location
- Try different region endpoints if available

**API key errors:**
- Verify API key is correct and active
- Check API key permissions in console
- Ensure environment variable is properly set

**Session creation failures:**
- Verify account has sufficient quota
- Check service status at console
- Try again after a few minutes

## 🎉 Installation Complete!

If all the above tests pass, congratulations! You have successfully installed and configured the AgentBay SDK.

**Next Steps:**
- [Understanding Basic Concepts](basic-concepts.md)
- [Creating Your First Session](first-session.md)
