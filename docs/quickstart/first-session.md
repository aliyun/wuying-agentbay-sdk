# Create Your First Session

Now let's experience the core features of AgentBay through actual code.

## 🎯 Objectives

- Create your first cloud session
- Perform basic file and command operations
- Understand how sessions work

## 📝 Complete Example

Choose the language you're familiar with to follow along:

### Python Version

```python
from agentbay import AgentBay

def main():
    # 1. Initialize AgentBay client
    print("🚀 Initializing AgentBay...")
    agent_bay = AgentBay()
    
    # 2. Create new session
    print("📱 Creating new session...")
    
    # You can choose different image types
    from agentbay.session_params import CreateSessionParams
    
    # Default Linux image
    result = agent_bay.create()
    
    # Or specify specific image
    # linux_params = CreateSessionParams(image_id="linux_latest")
    # windows_params = CreateSessionParams(image_id="windows_latest") 
    # android_params = CreateSessionParams(image_id="android_latest")
    # result = agent_bay.create(linux_params)
    
    if not result.success:
        print(f"❌ Session creation failed: {result.error_message}")
        return
    
    session = result.session
    print(f"✅ Session created successfully, ID: {session.session_id}")
    print(f"   Image type: {getattr(session, 'image_id', 'Default Linux')}")
    
    # 3. Execute basic commands
    print("\n💻 Executing commands...")
    
    # Check current directory
    cmd_result = session.command.execute("pwd")
    print(f"Current directory: {cmd_result.data.stdout.strip()}")
    
    # Check system information
    cmd_result = session.command.execute("uname -a")
    print(f"System info: {cmd_result.data.stdout.strip()}")
    
    # List files
    cmd_result = session.command.execute("ls -la /tmp")
    print(f"Temporary directory contents:\n{cmd_result.data.stdout}")
    
    # 4. File operations
    print("\n📁 File operations...")
    
    # Create file
    content = f"Hello from AgentBay!\nCreated at: {session.session_id}"
    write_result = session.file_system.write_file("/tmp/hello.txt", content)
    
    if write_result.success:
        print("✅ File written successfully")
    else:
        print(f"❌ File write failed: {write_result.error_message}")
        return
    
    # Read file
    read_result = session.file_system.read_file("/tmp/hello.txt")
    if read_result.success:
        print(f"📖 File content:\n{read_result.data}")
    else:
        print(f"❌ File read failed: {read_result.error_message}")
    
    # 5. Create directory and multiple files
    print("\n📂 Creating directory structure...")
    
    # Create directory
    session.command.execute("mkdir -p /tmp/my_project/data")
    
    # Create multiple files
    files_to_create = {
        "/tmp/my_project/README.md": "# My First AgentBay Project\n\nThis is a test project.",
        "/tmp/my_project/data/config.json": '{"name": "test", "version": "1.0"}',
        "/tmp/my_project/script.py": 'print("Hello from Python in the cloud!")'
    }
    
    for file_path, file_content in files_to_create.items():
        session.file_system.write_file(file_path, file_content)
        print(f"✅ Created file: {file_path}")
    
    # View directory structure
    tree_result = session.command.execute("find /tmp/my_project -type f")
    print(f"\n📋 Project file list:\n{tree_result.data.stdout}")
    
    # 6. Run Python script
    print("\n🐍 Running Python script...")
    python_result = session.command.execute("python3 /tmp/my_project/script.py")
    print(f"Script output: {python_result.data.stdout.strip()}")
    
    # 7. Network operations example
    print("\n🌐 Network operations...")
    curl_result = session.command.execute("curl -s https://httpbin.org/json")
    print(f"Network request result: {curl_result.data.stdout[:100]}...")
    
    print(f"\n🎉 Congratulations! You have successfully completed your first AgentBay session")
    print(f"Session ID: {session.session_id}")
    print("💡 Tip: Sessions will be automatically cleaned up after a period of time, files will be lost")

if __name__ == "__main__":
    main()
```

### TypeScript Version

```typescript
import { AgentBay } from 'wuying-agentbay-sdk';

async function main() {
    // 1. Initialize AgentBay client
    console.log("🚀 Initializing AgentBay...");
    const agentBay = new AgentBay();
    
    // 2. Create new session
    console.log("📱 Creating new session...");
    const result = await agentBay.create();
    
    if (!result.success) {
        console.log(`❌ Session creation failed: ${result.errorMessage}`);
        return;
    }
    
    const session = result.session;
    console.log(`✅ Session created successfully, ID: ${session.sessionId}`);
    
    // 3. Execute basic commands
    console.log("\n💻 Executing commands...");
    
    // Check current directory
    let cmdResult = await session.command.execute("pwd");
    console.log(`Current directory: ${cmdResult.data.stdout.trim()}`);
    
    // Check system information
    cmdResult = await session.command.execute("uname -a");
    console.log(`System info: ${cmdResult.data.stdout.trim()}`);
    
    // 4. File operations
    console.log("\n📁 File operations...");
    
    // Create file
    const content = `Hello from AgentBay!\nCreated at: ${session.sessionId}`;
    const writeResult = await session.fileSystem.writeFile("/tmp/hello.txt", content);
    
    if (writeResult.success) {
        console.log("✅ File written successfully");
    } else {
        console.log(`❌ File write failed: ${writeResult.errorMessage}`);
        return;
    }
    
    // Read file
    const readResult = await session.fileSystem.readFile("/tmp/hello.txt");
    if (readResult.success) {
        console.log(`📖 File content:\n${readResult.data}`);
    }
    
    // 5. Run Node.js code
    console.log("\n🟢 Running Node.js script...");
    
    // Create Node.js script
    const nodeScript = `
console.log("Hello from Node.js in the cloud!");
console.log("Current time:", new Date().toISOString());
`;
    
    await session.fileSystem.writeFile("/tmp/script.js", nodeScript);
    const nodeResult = await session.command.execute("node /tmp/script.js");
    console.log(`Script output: ${nodeResult.data.stdout}`);
    
    console.log(`\n🎉 Congratulations! You have successfully completed your first AgentBay session`);
    console.log(`Session ID: ${session.sessionId}`);
}

main().catch(console.error);
```

### Golang Version

```go
package main

import (
    "fmt"
    "github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

func main() {
    // 1. Initialize AgentBay client
    fmt.Println("🚀 Initializing AgentBay...")
    client, err := agentbay.NewAgentBay("", nil)
    if err != nil {
        fmt.Printf("❌ Initialization failed: %v\n", err)
        return
    }
    
    // 2. Create new session
    fmt.Println("📱 Creating new session...")
    result, err := client.Create(nil)
    if err != nil {
        fmt.Printf("❌ Session creation failed: %v\n", err)
        return
    }
    
    session := result.Session
    fmt.Printf("✅ Session created successfully, ID: %s\n", session.SessionID)
    
    // 3. Execute basic commands
    fmt.Println("\n💻 Executing commands...")
    
    // Check current directory
    cmdResult, err := session.Command.ExecuteCommand("pwd")
    if err == nil {
        fmt.Printf("Current directory: %s", cmdResult.Output)
    }
    
    // 4. File operations
    fmt.Println("\n📁 File operations...")
    
    // Create file
    content := fmt.Sprintf("Hello from AgentBay!\nCreated at: %s", session.SessionID)
    _, err = session.FileSystem.WriteFile("/tmp/hello.txt", content, "")
    
    if err != nil {
        fmt.Printf("❌ File write failed: %v\n", err)
        return
    }
    
    fmt.Println("✅ File written successfully")
    
    // Read file
    readResult, err := session.FileSystem.ReadFile("/tmp/hello.txt")
    if err == nil {
        fmt.Printf("📖 File content:\n%s\n", readResult.Content)
    }
    
    // 5. Run Go code
    fmt.Println("\n🔵 Running Go script...")
    
    // Create Go script
    goScript := `package main
import "fmt"
import "time"
func main() {
    fmt.Println("Hello from Go in the cloud!")
    fmt.Println("Current time:", time.Now().Format("2006-01-02 15:04:05"))
}`
    
    session.FileSystem.WriteFile("/tmp/script.go", goScript, "")
    goResult, _ := session.Command.ExecuteCommand("cd /tmp && go run script.go")
    fmt.Printf("Script output: %s", goResult.Output)
    
    fmt.Printf("\n🎉 Congratulations! You have successfully completed your first AgentBay session\n")
    fmt.Printf("Session ID: %s\n", session.SessionID)
}
```

## 🔍 Code Explanation

### 1. Initialize Client
```python
agent_bay = AgentBay()  # Automatically reads API key from environment variables
```

### 2. Create Session
```python
result = agent_bay.create()  # Returns result object
session = result.session     # Get session instance
```

### 3. Command Execution
```python
cmd_result = session.command.execute("ls -la")
print(cmd_result.data.stdout)    # Standard output
print(cmd_result.data.stderr)    # Error output
print(cmd_result.data.exit_code) # Exit code
```

### 4. File Operations
```python
# Write
session.file_system.write_file(path, content)

# Read
result = session.file_system.read_file(path)
content = result.data
```

## 🎯 Run This Example

1. Ensure you have installed the SDK and configured the API key
2. Save the code to a file (e.g., `first_session.py`)
3. Run: `python first_session.py`

## 💡 Key Points

1. **Sessions are temporary**: All files are lost when the session ends
2. **Network access**: The cloud environment can access the internet
3. **Complete Linux environment**: Supports most Linux commands and tools
4. **Multi-language support**: Can run Python, Node.js, Go, and other programs

## 🚀 Next Steps

- Learn about [Data Persistence](../guides/data-persistence.md) to save important files
- Explore [More Features](../guides/README.md)
- Check out [Best Practices](best-practices.md)

## 🎉 Congratulations!

You have successfully created and used your first AgentBay session! Now you can:
- Execute any Linux command in the cloud
- Create and edit files
- Run code in various programming languages
- Access internet resources

Continue learning more advanced features! 🚀