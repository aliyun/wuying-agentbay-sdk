# AgentBay + Spring AI 示例项目

这是一个展示如何将 AgentBay SDK 与 Spring AI 集成的示例项目，实现云端执行 Python 代码的 AI Agent。

## 项目结构

```
src/main/java/com/example/agentdemo/
├── AgentDemoApplication.java          # 主应用类
├── config/
│   └── AiConfig.java                  # Spring AI 和 AgentBay 配置
├── service/
│   ├── AgentBayToolService.java       # AgentBay 工具服务（@Tool）
│   └── DataAnalysisService.java       # 业务服务（编排层）
└── controller/
    └── AgentController.java           # REST API 控制器
```

## 环境准备

### 1. 设置环境变量

```bash
# AgentBay API Key（必需）
export AGENTBAY_API_KEY=your_agentbay_api_key

# OpenAI API Key（必需）
export OPENAI_API_KEY=your_openai_api_key
```

### 2. 获取 AgentBay API Key

访问 [AgentBay 控制台](https://agentbay.console.aliyun.com/service-management) 创建 API Key。

### 3. Maven 仓库配置

AgentBay SDK 目前发布在阿里云内部仓库，需要配置相应的 Maven 仓库访问权限。

## 运行项目

```bash
# 编译项目
mvn clean package

# 运行应用
mvn spring-boot:run
```

应用将在 `http://localhost:8080` 启动。

## 使用示例

### 通过 REST API 调用

```bash
curl -X POST http://localhost:8080/api/agent/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "帮我用 Python 计算 1000 以内所有质数的和"
  }'
```

### 响应示例

```json
{
  "result": "1000以内所有质数的和是 76127"
}
```

## 核心特性

### 1. 解耦架构

- **编排层**（DataAnalysisService）：负责与 LLM 交互，处理用户请求
- **工具层**（AgentBayToolService）：提供可调用的工具，封装 AgentBay SDK
- **执行层**（AgentBay Cloud）：在云端隔离沙箱中执行代码

### 2. 安全执行

所有 Python 代码都在 AgentBay 云端沙箱中执行，具备：
- 完全隔离的运行环境
- 自动资源清理
- 防止本地系统受到影响

### 3. Spring AI 集成

使用 Spring AI 的 `@Tool` 注解自动将 Java 方法注册为 LLM 可调用的工具：

```java
@Tool(description = "在安全的云端沙箱中执行 Python 3 代码...")
public String executePythonCode(
    @ToolProperty(description = "要执行的 Python 3 代码字符串") String code
) {
    // AgentBay SDK 调用逻辑
}
```

## 扩展功能

### 添加更多工具

在 `AgentBayToolService` 中添加更多 `@Tool` 方法：

```java
@Tool(description = "在云端浏览器中访问网页并提取内容")
public String fetchWebContent(
    @ToolProperty(description = "要访问的 URL") String url
) {
    // 使用 AgentBay 浏览器沙箱
}
```

### 使用 Context 实现持久化

```java
// 创建持久化上下文
ContextResult contextResult = agentBay.getContext()
    .get("workspace-id", true, "cn-hangzhou");

// 创建会话时绑定 Context
CreateSessionParams params = new CreateSessionParams();
ContextSync sync = ContextSync.create(
    contextResult.getContext().getId(),
    "/workspace",
    SyncPolicy.defaultPolicy()
);
params.setContextSyncs(Arrays.asList(sync));
```

## 注意事项

1. **资源清理**：务必在 `finally` 块中清理 AgentBay 会话
2. **超时控制**：对于长时间运行的任务，设置合适的超时时间
3. **错误处理**：捕获并妥善处理 AgentBay SDK 可能抛出的异常

## 参考资料

- [AgentBay 官方文档](https://agentbay.console.aliyun.com/)
- [Spring AI 文档](https://docs.spring.io/spring-ai/reference/)
- [AgentBay GitHub](https://github.com/aliyun/agentbay-sdk)
