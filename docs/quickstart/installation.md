# Installation and Configuration

## 环境要求

### Python
- Python 3.8+
- pip 或 poetry

### TypeScript/JavaScript
- Node.js 14+
- npm 或 yarn

### Golang
- Go 1.18+

## 安装SDK

### Python
```bash
# 使用pip安装
pip install wuying-agentbay-sdk

# 验证安装
python -c "import agentbay; print('安装成功')"
```

### TypeScript
```bash
# 使用npm安装
npm install wuying-agentbay-sdk

# 验证安装
node -e "const {AgentBay} = require('wuying-agentbay-sdk'); console.log('安装成功')"
```

### Golang
```bash
# 安装包
go get github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay

# 验证安装（创建测试文件）
echo 'package main
import "github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
func main() { println("安装成功") }' > test.go
go run test.go
rm test.go
```

## 获取API密钥

### 步骤1：注册阿里云账号
访问 [https://aliyun.com](https://aliyun.com) 注册账号

### 步骤2：获取API密钥
1. 登录 [AgentBay控制台](https://agentbay.console.aliyun.com/service-management)
2. 在服务管理页面找到API密钥管理
3. 创建新的API密钥
4. 复制密钥备用

## 配置API密钥

### 方式1：环境变量（推荐）
```bash
export AGENTBAY_API_KEY=your_api_key_here
```

### 方式2：代码中设置
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

## 验证配置

创建一个简单的测试程序验证一切正常：

### Python Test
```python
from agentbay import AgentBay

try:
    agent_bay = AgentBay()
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
        const agentBay = new AgentBay();
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
    // Initialize client
    client, err := agentbay.NewAgentBay("", nil)
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

## 🎉 安装完成！

如果上面的测试都通过了，恭喜你已经成功安装并配置了AgentBay SDK！

下一步：[理解基本概念](basic-concepts.md) 