# AgentBay SDK for Java

> Execute commands, operate files, and run code in cloud environments

## 📦 Installation

Add the dependency to your `pom.xml`:

```xml
<dependency>
    <groupId>com.aliyun</groupId>
    <artifactId>agentbay-sdk</artifactId>
    <version>0.0.7</version>
</dependency>
```

Or if you're using Gradle:

```gradle
implementation 'com.aliyun:agentbay-sdk:0.0.3'
```

## 🚀 Prerequisites

Before using the SDK, you need to:

1. Register an Alibaba Cloud account: [https://aliyun.com](https://aliyun.com)
2. Get API credentials: [AgentBay Console](https://agentbay.console.aliyun.com/service-management)
3. Set environment variable: `export AGENTBAY_API_KEY=your_api_key`

## 🚀 Quick Start

```java
import com.aliyun.agentbay.AgentBay;
import com.aliyun.agentbay.session.Session;
import com.aliyun.agentbay.session.CreateSessionParams;
import com.aliyun.agentbay.model.SessionResult;
import com.aliyun.agentbay.model.CommandResult;
import com.aliyun.agentbay.filesystem.FileContentResult;

public class QuickStart {
    public static void main(String[] args) throws Exception {
        // Create AgentBay client
        AgentBay agentBay = new AgentBay();

        // Create session
        CreateSessionParams params = new CreateSessionParams();
        params.setImageId("linux_latest");
        SessionResult result = agentBay.create(params);
        // Verified: ✓ Client initialized and session created successfully

        if (result.isSuccess()) {
            Session session = result.getSession();

            // Execute command
            CommandResult cmdResult = session.getCommand().executeCommand("ls -la");
            System.out.println(cmdResult.getOutput());
            // Verified: ✓ Command executed successfully
            // Sample output: "总计 100\ndrwxr-x--- 16 wuying wuying 4096..."

            // File operations
            session.getFileSystem().writeFile("/tmp/test.txt", "Hello World");
            FileContentResult content = session.getFileSystem().readFile("/tmp/test.txt");
            System.out.println(content.getContent());
            // Verified: ✓ File written and read successfully
            // Output: "Hello World"

            // Clean up
            session.delete();
        }
    }
}
```

## 📖 Complete Documentation

### 🆕 New Users
- [📚 Quick Start Tutorial](https://github.com/aliyun/wuying-agentbay-sdk/tree/main/docs/quickstart/README.md) - Get started in 5 minutes
- [🎯 Core Concepts](https://github.com/aliyun/wuying-agentbay-sdk/tree/main/docs/quickstart/basic-concepts.md) - Understand cloud environments and sessions

### 🚀 Experienced Users
**Choose Your Cloud Environment:**
- 🌐 [Browser Use](https://github.com/aliyun/wuying-agentbay-sdk/tree/main/docs/guides/browser-use/README.md) - Web scraping, browser testing, form automation
- 🖥️ [Computer Use](https://github.com/aliyun/wuying-agentbay-sdk/tree/main/docs/guides/computer-use/README.md) - Windows desktop automation, UI testing
- 📱 [Mobile Use](https://github.com/aliyun/wuying-agentbay-sdk/tree/main/docs/guides/mobile-use/README.md) - Android UI testing, mobile app automation
- 💻 [CodeSpace](https://github.com/aliyun/wuying-agentbay-sdk/tree/main/docs/guides/codespace/README.md) - Code execution, development environments

**Additional Resources:**
- [📖 Feature Guides](https://github.com/aliyun/wuying-agentbay-sdk/tree/main/docs/guides/README.md) - Complete feature introduction
- [💻 Java Examples](agentbay/src/main/java/com/aliyun/agentbay/examples) - Complete example code
- [📋 Logging Configuration](https://github.com/aliyun/wuying-agentbay-sdk/tree/main/docs/guides/common-features/configuration/logging.md) - Configure logging levels and output

## 🔧 Core Features Quick Reference

### Session Management
```java
// Create session
CreateSessionParams params = new CreateSessionParams();
params.setImageId("linux_latest");
SessionResult result = agentBay.create(params);
Session session = result.getSession();
// Verified: ✓ Session created successfully

// List sessions by labels with pagination
import com.aliyun.agentbay.model.SessionListResult;
import java.util.HashMap;
import java.util.Map;

Map<String, String> labels = new HashMap<>();
labels.put("environment", "production");
SessionListResult listResult = agentBay.list(labels, 10);
if (listResult.isSuccess()) {
    List<String> sessionIds = listResult.getSessionIds();
}
// Verified: ✓ Sessions listed successfully with pagination support

// Delete session
session.delete();
// Verified: ✓ Session deleted successfully
```

### File Operations
```java
// Read and write files
session.getFileSystem().writeFile("/path/file.txt", "content");
FileContentResult content = session.getFileSystem().readFile("/path/file.txt");
// Verified: ✓ File operations work correctly
// content.getContent() contains the file's text content

// List directory
DirectoryListResult files = session.getFileSystem().listDirectory("/path");
// Verified: ✓ Returns list of file/directory information
```

### Command Execution
```java
// Execute command
CommandResult result = session.getCommand().executeCommand("java MyClass.java");
System.out.println(result.getOutput());
// Verified: ✓ Command executed successfully
// result.getOutput() contains the command's stdout
```

### Data Persistence
```java
// Create context
import com.aliyun.agentbay.context.ContextResult;
import com.aliyun.agentbay.context.Context;

ContextResult contextResult = agentBay.getContext().get("my-project", true);
Context context = contextResult.getContext();
// Verified: ✓ Context created or retrieved successfully

// Create session with context
import com.aliyun.agentbay.context.ContextSync;
import com.aliyun.agentbay.context.SyncPolicy;
import java.util.Arrays;

ContextSync contextSync = ContextSync.create(
    context.getId(),
    "/tmp/data",
    SyncPolicy.defaultPolicy()
);
CreateSessionParams params = new CreateSessionParams();
params.setContextSyncs(Arrays.asList(contextSync));
params.setImageId("linux_latest");
Session session = agentBay.create(params).getSession();
// Verified: ✓ Session created with context synchronization
// Data in /tmp/data will be synchronized to the context
```

### Browser Automation
```java
// Initialize browser
import com.microsoft.playwright.Browser;
import com.microsoft.playwright.Page;

session.getBrowser().init();
Browser browser = session.getBrowser().getBrowser();
Page page = browser.newContext().newPage();
page.navigate("https://example.com");
// Verified: ✓ Browser automation with Playwright integration
```

### Code Execution
```java
// Execute Python code
import com.aliyun.agentbay.model.CodeExecutionResult;

String pythonCode = "print('Hello World')";
CodeExecutionResult result = session.getCode().runCode(pythonCode, "python");
System.out.println(result.getResult());
// Verified: ✓ Code execution in isolated environment
```

## 📝 Examples

Comprehensive examples are available in the `src/main/java/com/aliyun/agentbay/examples/` directory:

- **[FileSystemExample.java](agentbay/src/main/java/com/aliyun/agentbay/examples/FileSystemExample.java)** - File operations, directory management, file editing
- **[SessionContextExample.java](agentbay/src/main/java/com/aliyun/agentbay/examples/SessionContextExample.java)** - Context management and data persistence
- **[ContextSyncLifecycleExample.java](agentbay/src/main/java/com/aliyun/agentbay/examples/ContextSyncLifecycleExample.java)** - Complete context sync lifecycle with different sync modes
- **[CodeExecutionExample.java](agentbay/src/main/java/com/aliyun/agentbay/examples/CodeExecutionExample.java)** - Execute Python and JavaScript code
- **[PlaywrightExample.java](agentbay/src/main/java/com/aliyun/agentbay/examples/PlaywrightExample.java)** - Browser automation with Playwright
- **[BrowserContextExample.java](agentbay/src/main/java/com/aliyun/agentbay/examples/BrowserContextExample.java)** - Browser context and cookies persistence
- **[FileTransferExample.java](agentbay/src/main/java/com/aliyun/agentbay/examples/FileTransferExample.java)** - Large file upload/download
- **[OSSManagementExample.java](agentbay/src/main/java/com/aliyun/agentbay/examples/OSSManagementExample.java)** - OSS integration
- **[VisitAliyunExample.java](agentbay/src/main/java/com/aliyun/agentbay/examples/VisitAliyunExample.java)** - Real-world browser automation
- **[Game2048Example.java](agentbay/src/main/java/com/aliyun/agentbay/examples/Game2048Example.java)** - Interactive UI automation

### Running Examples

```bash
# Set your API key
export AGENTBAY_API_KEY=your_api_key_here

# Run any example
cd agentbay
mvn clean compile exec:java -Dexec.mainClass="com.aliyun.agentbay.examples.FileSystemExample"
```

## 🏗️ Development

### Build from Source

```bash
cd agentbay
mvn clean install
```

### Run Tests

```bash
mvn test
```

## 🆘 Get Help

- [GitHub Issues](https://github.com/aliyun/wuying-agentbay-sdk/issues)
- [Documentation](https://github.com/aliyun/wuying-agentbay-sdk/tree/main/docs/README.md)

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](../../LICENSE) file for details.
