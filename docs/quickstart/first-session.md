# 创建你的第一个会话

现在让我们通过实际代码来体验AgentBay的核心功能。

## 🎯 本节目标

- 创建你的第一个云端会话
- 执行基本的文件和命令操作
- 理解会话的工作方式

## 📝 完整示例

选择你熟悉的语言跟着做：

### Python版本

```python
from agentbay import AgentBay

def main():
    # 1. 初始化AgentBay客户端
    print("🚀 初始化AgentBay...")
    agent_bay = AgentBay()
    
    # 2. 创建新会话
    print("📱 创建新会话...")
    
    # 可以选择不同的镜像类型
    from agentbay.session_params import CreateSessionParams
    
    # 默认Linux镜像
    result = agent_bay.create()
    
    # 或者指定特定镜像
    # linux_params = CreateSessionParams(image_id="linux_latest")
    # windows_params = CreateSessionParams(image_id="windows_latest") 
    # android_params = CreateSessionParams(image_id="android_latest")
    # result = agent_bay.create(linux_params)
    
    if not result.success:
        print(f"❌ 创建会话失败: {result.error}")
        return
    
    session = result.session
    print(f"✅ 会话创建成功，ID: {session.session_id}")
    print(f"   镜像类型: {getattr(session, 'image_id', '默认Linux')}")
    
    # 3. 执行基本命令
    print("\n💻 执行命令...")
    
    # 查看当前目录
    cmd_result = session.command.execute("pwd")
    print(f"当前目录: {cmd_result.data.stdout.strip()}")
    
    # 查看系统信息
    cmd_result = session.command.execute("uname -a")
    print(f"系统信息: {cmd_result.data.stdout.strip()}")
    
    # 列出文件
    cmd_result = session.command.execute("ls -la /tmp")
    print(f"临时目录内容:\n{cmd_result.data.stdout}")
    
    # 4. 文件操作
    print("\n📁 文件操作...")
    
    # 创建文件
    content = f"Hello from AgentBay!\n创建时间: {session.session_id}"
    write_result = session.file_system.write_file("/tmp/hello.txt", content)
    
    if write_result.success:
        print("✅ 文件写入成功")
    else:
        print(f"❌ 文件写入失败: {write_result.error}")
        return
    
    # 读取文件
    read_result = session.file_system.read_file("/tmp/hello.txt")
    if read_result.success:
        print(f"📖 文件内容:\n{read_result.data}")
    else:
        print(f"❌ 文件读取失败: {read_result.error}")
    
    # 5. 创建目录和多个文件
    print("\n📂 创建目录结构...")
    
    # 创建目录
    session.command.execute("mkdir -p /tmp/my_project/data")
    
    # 创建多个文件
    files_to_create = {
        "/tmp/my_project/README.md": "# 我的第一个AgentBay项目\n\n这是一个测试项目。",
        "/tmp/my_project/data/config.json": '{"name": "test", "version": "1.0"}',
        "/tmp/my_project/script.py": 'print("Hello from Python in the cloud!")'
    }
    
    for file_path, file_content in files_to_create.items():
        session.file_system.write_file(file_path, file_content)
        print(f"✅ 创建文件: {file_path}")
    
    # 查看目录结构
    tree_result = session.command.execute("find /tmp/my_project -type f")
    print(f"\n📋 项目文件列表:\n{tree_result.data.stdout}")
    
    # 6. 运行Python脚本
    print("\n🐍 运行Python脚本...")
    python_result = session.command.execute("python3 /tmp/my_project/script.py")
    print(f"脚本输出: {python_result.data.stdout.strip()}")
    
    # 7. 网络操作示例
    print("\n🌐 网络操作...")
    curl_result = session.command.execute("curl -s https://httpbin.org/json")
    print(f"网络请求结果: {curl_result.data.stdout[:100]}...")
    
    print(f"\n🎉 恭喜！你已经成功完成了第一个AgentBay会话")
    print(f"会话ID: {session.session_id}")
    print("💡 提示: 会话会在一段时间后自动清理，文件会丢失")

if __name__ == "__main__":
    main()
```

### TypeScript版本

```typescript
import { AgentBay } from 'wuying-agentbay-sdk';

async function main() {
    // 1. 初始化AgentBay客户端
    console.log("🚀 初始化AgentBay...");
    const agentBay = new AgentBay();
    
    // 2. 创建新会话
    console.log("📱 创建新会话...");
    const result = await agentBay.create();
    
    if (!result.success) {
        console.log(`❌ 创建会话失败: ${result.error}`);
        return;
    }
    
    const session = result.session;
    console.log(`✅ 会话创建成功，ID: ${session.sessionId}`);
    
    // 3. 执行基本命令
    console.log("\n💻 执行命令...");
    
    // 查看当前目录
    let cmdResult = await session.command.execute("pwd");
    console.log(`当前目录: ${cmdResult.data.stdout.trim()}`);
    
    // 查看系统信息
    cmdResult = await session.command.execute("uname -a");
    console.log(`系统信息: ${cmdResult.data.stdout.trim()}`);
    
    // 4. 文件操作
    console.log("\n📁 文件操作...");
    
    // 创建文件
    const content = `Hello from AgentBay!\n创建时间: ${session.sessionId}`;
    const writeResult = await session.fileSystem.writeFile("/tmp/hello.txt", content);
    
    if (writeResult.success) {
        console.log("✅ 文件写入成功");
    } else {
        console.log(`❌ 文件写入失败: ${writeResult.error}`);
        return;
    }
    
    // 读取文件
    const readResult = await session.fileSystem.readFile("/tmp/hello.txt");
    if (readResult.success) {
        console.log(`📖 文件内容:\n${readResult.data}`);
    }
    
    // 5. 运行Node.js代码
    console.log("\n🟢 运行Node.js脚本...");
    
    // 创建Node.js脚本
    const nodeScript = `
console.log("Hello from Node.js in the cloud!");
console.log("当前时间:", new Date().toISOString());
`;
    
    await session.fileSystem.writeFile("/tmp/script.js", nodeScript);
    const nodeResult = await session.command.execute("node /tmp/script.js");
    console.log(`脚本输出: ${nodeResult.data.stdout}`);
    
    console.log(`\n🎉 恭喜！你已经成功完成了第一个AgentBay会话`);
    console.log(`会话ID: ${session.sessionId}`);
}

main().catch(console.error);
```

### Golang版本

```go
package main

import (
    "fmt"
    "github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

func main() {
    // 1. 初始化AgentBay客户端
    fmt.Println("🚀 初始化AgentBay...")
    client, err := agentbay.NewAgentBay("", nil)
    if err != nil {
        fmt.Printf("❌ 初始化失败: %v\n", err)
        return
    }
    
    // 2. 创建新会话
    fmt.Println("📱 创建新会话...")
    result, err := client.Create(nil)
    if err != nil {
        fmt.Printf("❌ 创建会话失败: %v\n", err)
        return
    }
    
    session := result.Session
    fmt.Printf("✅ 会话创建成功，ID: %s\n", session.SessionID)
    
    // 3. 执行基本命令
    fmt.Println("\n💻 执行命令...")
    
    // 查看当前目录
    cmdResult, err := session.Command.ExecuteCommand("pwd")
    if err == nil {
        fmt.Printf("当前目录: %s", cmdResult.Output)
    }
    
    // 4. 文件操作
    fmt.Println("\n📁 文件操作...")
    
    // 创建文件
    content := fmt.Sprintf("Hello from AgentBay!\n创建时间: %s", session.SessionID)
    _, err = session.FileSystem.WriteFile("/tmp/hello.txt", []byte(content))
    
    if err != nil {
        fmt.Printf("❌ 文件写入失败: %v\n", err)
        return
    }
    
    fmt.Println("✅ 文件写入成功")
    
    // 读取文件
    readResult, err := session.FileSystem.ReadFile("/tmp/hello.txt")
    if err == nil {
        fmt.Printf("📖 文件内容:\n%s\n", string(readResult.Data))
    }
    
    // 5. 运行Go代码
    fmt.Println("\n🔵 运行Go脚本...")
    
    // 创建Go脚本
    goScript := `package main
import "fmt"
import "time"
func main() {
    fmt.Println("Hello from Go in the cloud!")
    fmt.Println("当前时间:", time.Now().Format("2006-01-02 15:04:05"))
}`
    
    session.FileSystem.WriteFile("/tmp/script.go", []byte(goScript))
    goResult, _ := session.Command.ExecuteCommand("cd /tmp && go run script.go")
    fmt.Printf("脚本输出: %s", goResult.Output)
    
    fmt.Printf("\n🎉 恭喜！你已经成功完成了第一个AgentBay会话\n")
    fmt.Printf("会话ID: %s\n", session.SessionID)
}
```

## 🔍 代码解析

### 1. 初始化客户端
```python
agent_bay = AgentBay()  # 自动从环境变量读取API密钥
```

### 2. 创建会话
```python
result = agent_bay.create()  # 返回结果对象
session = result.session     # 获取会话实例
```

### 3. 命令执行
```python
cmd_result = session.command.execute("ls -la")
print(cmd_result.data.stdout)    # 标准输出
print(cmd_result.data.stderr)    # 错误输出
print(cmd_result.data.exit_code) # 退出码
```

### 4. 文件操作
```python
# 写入
session.file_system.write_file(path, content)

# 读取
result = session.file_system.read_file(path)
content = result.data
```

## 🎯 运行这个示例

1. 确保已经安装SDK并配置API密钥
2. 将代码保存为文件（如`first_session.py`）
3. 运行：`python first_session.py`

## 💡 关键要点

1. **会话是临时的**：会话结束后，所有文件都会丢失
2. **网络访问**：云端环境可以访问互联网
3. **完整Linux环境**：支持大部分Linux命令和工具
4. **多语言支持**：可以运行Python、Node.js、Go等程序

## 🚀 下一步

- 学习[数据持久化](../guides/data-persistence.md)保存重要文件
- 探索[更多功能](../guides/README.md)
- 查看[实用技巧](best-practices.md)

## 🎉 恭喜！

你已经成功创建并使用了第一个AgentBay会话！现在你可以：
- 在云端执行任何Linux命令
- 创建和编辑文件
- 运行各种编程语言的代码
- 访问互联网资源

继续学习更多高级功能吧！ 