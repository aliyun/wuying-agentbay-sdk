# LangChain4j + AgentBay Demo

这是一个展示如何结合 LangChain4j 和 AgentBay SDK 构建企业级 AI Agent 的示例项目。

## 项目架构

```
LangChain4j (编排层)
    ↓
AgentBayTools (@Tool)
    ↓
AgentBay SDK (执行层)
    ↓
云端沙箱环境
```

## 功能特性

- ✅ 在云端安全隔离的沙箱中执行 Python 代码
- ✅ 执行 Shell 命令进行文件操作和系统管理
- ✅ 执行 JavaScript/Node.js 代码
- ✅ 自动工具调用（Tool Calling）
- ✅ 完整的资源管理和清理机制

## 前置要求

1. **Java 17+**
2. **Maven 3.6+**
3. **AgentBay API Key**
   - 访问 https://agentbay.console.aliyun.com/service-management
   - 登录阿里云账号并创建 API Key
4. **OpenAI API Key**
   - 用于 LLM 调用（或使用其他兼容的模型提供商）

## 快速开始

### 1. 设置环境变量

```bash
export AGENTBAY_API_KEY=your_agentbay_api_key_here
export OPENAI_API_KEY=your_openai_api_key_here
```

### 2. 配置 Maven 仓库

在 `~/.m2/settings.xml` 中添加阿里云内部仓库配置（如果使用内部版本）：

```xml
<settings>
  <servers>
    <server>
      <id>aliyun-internal</id>
      <username>your-username</username>
      <password>your-password</password>
    </server>
  </servers>

  <profiles>
    <profile>
      <id>aliyun</id>
      <repositories>
        <repository>
          <id>aliyun-internal</id>
          <url>https://your-internal-maven-repo</url>
        </repository>
      </repositories>
    </profile>
  </profiles>

  <activeProfiles>
    <activeProfile>aliyun</activeProfile>
  </activeProfiles>
</settings>
```

### 3. 编译项目

```bash
mvn clean compile
```

### 4. 运行示例

```bash
mvn exec:java -Dexec.mainClass="com.example.agent.AgentBayDemo"
```

## 示例说明

项目包含三个示例场景：

### 示例 1: Python 计算任务
```
用户: 帮我用 Python 计算 1000 以内所有质数的和
```
Agent 会自动调用 `executePythonCode` 工具，在云端沙箱中执行 Python 代码。

### 示例 2: 数据分析任务
```
用户: 用 Python 生成一个包含 100 个随机数的列表，然后计算它们的平均值、中位数和标准差
```
演示了更复杂的数据分析场景。

### 示例 3: Shell 命令任务
```
用户: 在云端环境中，创建一个文本文件，写入当前日期和系统信息，然后读取它
```
展示了如何使用 Shell 命令进行文件操作。

## 核心代码说明

### AgentBayTools.java

封装了 AgentBay SDK 的调用逻辑，使用 `@Tool` 注解将功能暴露给 LLM：

```java
@Tool("在安全的云端沙箱中执行 Python 3 代码...")
public String executePythonCode(String code) {
    // 创建沙箱 -> 执行代码 -> 清理环境
}
```

### DataAnalysisAgent.java

定义了 AI Agent 的接口，使用 `@SystemMessage` 配置 Agent 的行为：

```java
public interface DataAnalysisAgent {
    @SystemMessage("你是一个专业的数据分析助手...")
    String analyze(@UserMessage String query);
}
```

### AgentBayDemo.java

主程序，演示如何构建和使用 Agent：

```java
DataAnalysisAgent agent = AiServices.builder(DataAnalysisAgent.class)
        .chatLanguageModel(chatModel)
        .tools(tools)
        .build();

String response = agent.analyze("你的问题");
```

## 架构优势

1. **解耦设计**
   - 编排层（LangChain4j）与执行层（AgentBay）完全解耦
   - 符合企业级 Java 开发的 IoC 理念

2. **安全隔离**
   - 所有代码执行都在云端隔离沙箱中进行
   - 避免了在本地执行不可信代码的安全风险

3. **资源弹性**
   - 按需创建和销毁沙箱环境
   - 支持多 Agent 并发执行

4. **易于扩展**
   - 只需在 `AgentBayTools` 中添加新的 `@Tool` 方法
   - 无需修改 Agent 接口或主逻辑

## 进阶功能

### 持久化工作区（Context）

```java
ContextResult contextResult = agentBay.getContext().get(workspaceId, true, "cn-hangzhou");
Context workspaceContext = contextResult.getContext();

CreateSessionParams params = new CreateSessionParams();
ContextSync sync = ContextSync.create(
    workspaceContext.getId(),
    "/workspace",
    SyncPolicy.defaultPolicy()
);
params.setContextSyncs(Arrays.asList(sync));
```

### 浏览器自动化

```java
CreateSessionParams params = new CreateSessionParams();
params.setImageId("browser_latest");
Session session = agentBay.create(params).getSession();

// 使用 Playwright API 进行浏览器操作
```

## 最佳实践

1. **资源管理**: 始终使用 try-finally 确保会话被正确清理
2. **超时控制**: 为长时间运行的任务设置合理的超时时间
3. **错误处理**: 捕获并妥善处理 SDK 异常
4. **日志记录**: 记录关键操作以便调试和审计

## 常见问题

### Q: AgentBay SDK 在哪里下载？
A: AgentBay SDK 已在 GitHub 开源，支持 Python/TypeScript/Go。Java 版本可通过阿里云内部 Maven 仓库获取。

### Q: 支持哪些编程语言执行？
A: 目前支持 Python、JavaScript、Shell、Go 等多种语言。

### Q: 沙箱环境的存活时间有多长？
A: 默认 30 分钟，可通过参数配置。建议用完立即删除以节省资源。

### Q: 可以使用其他 LLM 提供商吗？
A: 可以！LangChain4j 支持 OpenAI、Azure OpenAI、Anthropic、本地模型等多种提供商。

## 参考资源

- [AgentBay 官方文档](https://agentbay.console.aliyun.com)
- [LangChain4j 文档](https://docs.langchain4j.dev)
- [Spring AI 集成示例](参考原文档中的 Spring AI 章节)

## 许可证

本项目仅供学习和参考使用。
