# Java SDK Examples

This directory documents the Java examples demonstrating various features and capabilities of the AgentBay SDK.

## 📁 Example Files Location

All example source files are located in: `agentbay/src/main/java/com/aliyun/agentbay/examples/`

## 🚀 Quick Start

### Prerequisites

1. Java 8 or later
2. Maven 3.6 or later
3. Valid `AGENTBAY_API_KEY` environment variable

### Running Examples

```bash
# Set your API key
export AGENTBAY_API_KEY=your_api_key_here

# Navigate to the agentbay directory
cd agentbay

# Run any example
mvn clean compile exec:java -Dexec.mainClass="com.aliyun.agentbay.examples.FileSystemExample"
```

## 📚 Available Examples

### Core Features

#### 1. FileSystemExample.java

**Purpose**: Demonstrates comprehensive file system operations

**Features:**
- Read and write files
- Create and list directories
- Search for files
- Edit files (find and replace)
- Move and delete files
- Handle multiple file operations

**Example Usage:**
```bash
mvn exec:java -Dexec.mainClass="com.aliyun.agentbay.examples.FileSystemExample"
```

**Key Concepts:**
- FileSystem API usage
- File content manipulation
- Directory operations
- Error handling patterns

---

#### 2. SessionContextExample.java

**Purpose**: Demonstrates context management and data persistence across sessions

**Features:**
- Create and manage contexts
- Configure context synchronization
- Persist data across sessions
- Upload and download strategies
- Context lifecycle management

**Example Usage:**
```bash
mvn exec:java -Dexec.mainClass="com.aliyun.agentbay.examples.SessionContextExample"
```

**Key Concepts:**
- Context creation and retrieval
- ContextSync configuration
- SyncPolicy setup
- Data persistence patterns

---

#### 3. ContextSyncLifecycleExample.java

**Purpose**: Demonstrates the complete context synchronization lifecycle with different sync modes

**Features:**
- Basic context sync (trigger only, non-blocking)
- Context sync with callback (async mode)
- Context sync and wait (blocking mode)
- Complete context persistence workflow across sessions
- Monitoring sync status with `info()` method
- Data verification after context restoration

**Example Usage:**
```bash
mvn exec:java -Dexec.mainClass="com.aliyun.agentbay.examples.ContextSyncLifecycleExample"
```

**Key Concepts:**
- Three sync modes: trigger-only, callback-based, and blocking
- Context sync lifecycle management
- Data persistence verification
- Session deletion with context sync
- Context data restoration in new sessions

**Example Code Snippet:**
```java
// Example 1: Basic sync (trigger only)
ContextSyncResult result = session.getContext().sync();
// Returns immediately, sync runs in background

// Example 2: Sync with callback (async)
CompletableFuture<Boolean> future = new CompletableFuture<>();
session.getContext().sync(success -> {
    System.out.println("Sync completed: " + success);
    future.complete(success);
});
Boolean success = future.get(5, TimeUnit.MINUTES);

// Example 3: Sync and wait (blocking)
ContextSyncResult result = session.getContext().syncAndWait();
if (result.isSuccess()) {
    System.out.println("Sync completed successfully");
}

// Example 4: Complete workflow - data persistence across sessions
// Step 1: Create context and first session
String contextName = "workflow-demo-" + System.currentTimeMillis();
ContextResult contextResult = agentBay.getContext().get(contextName, true);
Context context = contextResult.getContext();

CreateSessionParams params = new CreateSessionParams();
ContextSync contextSync = ContextSync.create(
    context.getId(),
    "/tmp/persist_data",
    SyncPolicy.defaultPolicy()
);
params.setContextSyncs(Arrays.asList(contextSync));
params.setImageId("linux_latest");
Session session1 = agentBay.create(params).getSession();

// Step 2: Create data in first session
String testContent = "Data from first session - timestamp: " + System.currentTimeMillis();
session1.getFileSystem().writeFile("/tmp/persist_data/persistent_file.txt", testContent);

// Step 3: Sync and delete with sync_context=true
session1.getContext().syncAndWait();
agentBay.delete(session1, true);  // sync_context=true uploads data

// Step 4: Create new session with same context
Session session2 = agentBay.create(params).getSession();

// Step 5: Verify data persisted
String restoredContent = session2.getFileSystem().read("/tmp/persist_data/persistent_file.txt");
if (testContent.equals(restoredContent)) {
    System.out.println("✅ Data persisted correctly!");
}
```

---

### Advanced Features

#### 4. FileTransferExample.java

**Purpose**: Demonstrates large file upload and download operations

**Features:**
- Upload files from local to cloud
- Download files from cloud to local
- Handle large file transfers
- Monitor transfer progress
- Context-based file transfer

**Example Usage:**
```bash
mvn exec:java -Dexec.mainClass="com.aliyun.agentbay.examples.FileTransferExample"
```

**Key Concepts:**
- File upload/download API
- Progress monitoring
- Transfer timeout configuration
- Context integration for transfers

---

#### 5. OSSManagementExample.java

**Purpose**: Demonstrates OSS (Object Storage Service) integration

**Features:**
- Initialize OSS with STS credentials
- Upload files to OSS buckets
- Download files from OSS
- Anonymous upload/download with pre-signed URLs
- Bucket and object management

**Example Usage:**
```bash
mvn exec:java -Dexec.mainClass="com.aliyun.agentbay.examples.OSSManagementExample"
```

**Key Concepts:**
- OSS environment initialization
- STS credential usage
- OSS upload/download operations
- Pre-signed URL handling

**Note**: Requires valid STS credentials (AccessKeyId, AccessKeySecret, SecurityToken)

---

### Browser Automation

#### 6. PlaywrightExample.java

**Purpose**: Demonstrates browser automation using Playwright

**Features:**
- Initialize cloud browser
- Connect Playwright to cloud browser
- Navigate web pages
- Interact with page elements
- Take screenshots
- Form automation

**Example Usage:**
```bash
mvn exec:java -Dexec.mainClass="com.aliyun.agentbay.examples.PlaywrightExample"
```

**Dependencies:**
```xml
<dependency>
    <groupId>com.microsoft.playwright</groupId>
    <artifactId>playwright</artifactId>
    <version>1.40.0</version>
</dependency>
```

**Key Concepts:**
- Browser initialization
- Playwright CDP connection
- Page automation
- Browser context management

---

#### 7. BrowserContextExample.java

**Purpose**: Demonstrates browser context configuration and cookie persistence

**Features:**
- Basic browser context for persistent browser data
- Browser context with extension support
- Browser context with fingerprint support
- Complete workflow with context synchronization
- Persist cookies, localStorage across sessions

**Example Usage:**
```bash
mvn exec:java -Dexec.mainClass="com.aliyun.agentbay.examples.BrowserContextExample"
```

**Key Concepts:**
- BrowserContext configuration
- Cookie persistence across sessions
- Extension integration
- Browser fingerprint context
- Context synchronization with auto_upload

**Example Code Snippet:**
```java
// Create a persistent context
ContextResult contextResult = agentBay.getContext().get("my-browser-context", true);
Context context = contextResult.getContext();

// Create BrowserContext with auto-upload
BrowserContext browserContext = new BrowserContext(context.getId(), true);

// Create session with BrowserContext
CreateSessionParams params = new CreateSessionParams();
params.setImageId("browser_latest");
params.setBrowserContext(browserContext);
Session session = agentBay.create(params).getSession();

// Browser data will be automatically saved when session is deleted with sync_context=true
agentBay.delete(session, true);
```

---

#### 8. VisitAliyunExample.java

**Purpose**: Demonstrates real-world browser automation on Alibaba Cloud website

**Features:**
- Navigate to Alibaba Cloud website
- Stealth mode configuration
- Page interaction
- Screenshot capture

**Example Usage:**
```bash
mvn exec:java -Dexec.mainClass="com.aliyun.agentbay.examples.VisitAliyunExample"
```

**Key Concepts:**
- Stealth browser configuration
- Real website automation
- Behavior simulation

---

#### 9. Game2048Example.java

**Purpose**: Demonstrates interactive UI automation by playing the 2048 game

**Features:**
- AI-powered game playing
- Complex UI interaction
- Game state observation
- Automated decision making

**Example Usage:**
```bash
mvn exec:java -Dexec.mainClass="com.aliyun.agentbay.examples.Game2048Example"
```

**Key Concepts:**
- Browser agent usage
- AI-powered automation
- Complex interaction patterns
- State observation and action

---

### Code Execution

#### 10. CodeExecutionExample.java

**Purpose**: Demonstrates Python and JavaScript code execution in cloud

**Features:**
- Execute Python code
- Execute JavaScript code
- Handle code execution results
- Configure execution timeouts

**Example Usage:**
```bash
mvn exec:java -Dexec.mainClass="com.aliyun.agentbay.examples.CodeExecutionExample"
```

**Key Concepts:**
- Code execution API
- Multi-language support
- Result handling
- Timeout configuration

---

## 💡 Common Patterns

### Basic Session Creation

```java
AgentBay agentBay = new AgentBay(System.getenv("AGENTBAY_API_KEY"));
SessionResult result = agentBay.create();
if (result.isSuccess()) {
    Session session = result.getSession();
    // Use session...
    session.delete();
}
```

### Session with Specific Image

```java
CreateSessionParams params = new CreateSessionParams();
params.setImageId("browser_latest"); // or linux_latest, code_latest, etc.
Session session = agentBay.create(params).getSession();
```

### Error Handling

```java
FileContentResult result = session.getFileSystem().readFile("/tmp/file.txt");
if (result.isSuccess()) {
    String content = result.getContent();
    // Process content...
} else {
    System.err.println("Error: " + result.getErrorMessage());
}
```

### Resource Cleanup

```java
try {
    Session session = agentBay.create().getSession();
    // Use session...
} finally {
    session.delete();
}
```

## 📋 Example Categories

### By Feature

**File Operations:**
- FileSystemExample
- FileTransferExample

**Data Persistence:**
- SessionContextExample
- ContextSyncLifecycleExample
- BrowserContextExample

**Storage Integration:**
- OSSManagementExample
- FileTransferExample

**Browser Automation:**
- PlaywrightExample
- BrowserContextExample
- VisitAliyunExample
- Game2048Example

**Code Execution:**
- CodeExecutionExample

### By Complexity

**Beginner:**
- FileSystemExample
- CodeExecutionExample

**Intermediate:**
- SessionContextExample
- ContextSyncLifecycleExample
- PlaywrightExample
- BrowserContextExample
- OSSManagementExample

**Advanced:**
- FileTransferExample
- Game2048Example

## 🎯 Learning Path

### For Beginners

1. **FileSystemExample** - Learn basic file operations
2. **CodeExecutionExample** - Understand code execution
3. **SessionContextExample** - Learn about persistence
4. **ContextSyncLifecycleExample** - Master context sync modes

### For Web Automation

1. **PlaywrightExample** - Basic browser automation
2. **BrowserContextExample** - Browser context and cookie persistence
3. **VisitAliyunExample** - Real-world website automation
4. **Game2048Example** - AI-powered automation

### For Data Management

1. **SessionContextExample** - Context and persistence
2. **FileTransferExample** - Large file handling
3. **OSSManagementExample** - Object storage integration

## 🔧 Configuration

### Environment Variables

```bash
# Required
export AGENTBAY_API_KEY=your_api_key_here

# Optional (for OSS examples)
export OSS_ACCESS_KEY_ID=your_access_key_id
export OSS_ACCESS_KEY_SECRET=your_access_key_secret
export OSS_SECURITY_TOKEN=your_security_token
```

### Maven Configuration

Add to your `pom.xml`:

```xml
<dependency>
    <groupId>com.aliyun</groupId>
    <artifactId>agentbay-sdk</artifactId>
    <version>0.0.1</version>
</dependency>
```

For browser examples, also add:

```xml
<dependency>
    <groupId>com.microsoft.playwright</groupId>
    <artifactId>playwright</artifactId>
    <version>1.40.0</version>
</dependency>
```

## 🆘 Troubleshooting

### API Key Issues

```
Error: API key is required
```

**Solution**: Set the `AGENTBAY_API_KEY` environment variable:
```bash
export AGENTBAY_API_KEY=your_api_key_here
```

### Resource Creation Delay

```
Message: The system is creating resources, please try again in 90 seconds
```

**Solution**: Wait 90 seconds and retry. This is normal for resource initialization.

### Maven Build Issues

```bash
# Clean and rebuild
mvn clean install

# Update dependencies
mvn dependency:resolve
```

### Playwright Issues

If browser examples fail:

```bash
# Install Playwright browsers (if using local Playwright)
mvn exec:java -e -D exec.mainClass=com.microsoft.playwright.CLI -D exec.args="install"
```

## 📚 Related Documentation

- [API Reference](../api/README.md) - Detailed API documentation
- [Quick Start Guide](../../../docs/quickstart/README.md) - Getting started
- [Feature Guides](../../../docs/guides/README.md) - Comprehensive feature guides
- [Java README](../../README.md) - Java SDK overview

## 🤝 Getting Help

- [GitHub Issues](https://github.com/aliyun/wuying-agentbay-sdk/issues)
- [Documentation](../../../docs/README.md)

---

💡 **Tip**: Start with FileSystemExample to understand basic concepts, then explore other examples based on your use case.

