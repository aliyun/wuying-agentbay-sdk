# VPC功能迁移方案

## 概述

本文档详细描述了将Golang模块中新增的VPC（Virtual Private Cloud）功能迁移到Python和TypeScript SDK的完整方案。VPC功能使用户能够在VPC环境中创建session，并通过HTTP直接调用MCP工具。

## 功能分析

### Golang中的VPC功能（已实现）

#### 1. 创建VPC Session参数
- `CreateSessionParams` 结构体中的 `IsVpc bool` 参数
- `WithIsVpc(bool)` 方法用于设置VPC标志  
- API调用时设置 `VpcResource` 参数

#### 2. VPC Session属性
- `IsVpcEnabled bool` - 是否启用VPC
- `NetworkInterfaceIP string` - VPC网络接口IP
- `HttpPortNumber string` - VPC HTTP端口
- 相关方法：`IsVpc()`, `NetworkInterfaceIp()`, `HttpPort()`

#### 3. VPC环境下调用MCP工具
- 所有模块（Application, FileSystem, Window, OSS, Command, UI等）都有 `callMcpToolVPC` 方法
- 使用HTTP GET请求到VPC endpoint: `http://{NetworkInterfaceIP}:{HttpPort}/callTool`
- 请求参数通过Query Parameters传递：server, tool, args, apiKey
- 通过 `FindServerForTool(toolName)` 查找工具对应的服务器

#### 4. 获取MCP工具列表
- `ListMcpTools()` 方法获取可用工具列表
- 返回 `McpToolsResult` 包含工具信息（name, description, inputSchema, server, tool）
- VPC session创建时自动获取MCP tools信息
- 存储在 `McpTools []McpTool` 字段中

## 当前状态分析

### Python SDK现状
✅ **已实现**：
- `CreateSessionParams` 中的 `is_vpc: Optional[bool]` 参数
- Session中的基础VPC属性：`is_vpc`, `network_interface_ip`, `http_port`
- 在 `agentbay.create()` 中设置 `request.vpc_resource = params.is_vpc`

❌ **缺失功能**：
- VPC相关的便捷方法
- VPC模式下的MCP tool调用机制
- 获取MCP tool list功能
- VPC session创建时自动获取工具列表

### TypeScript SDK现状
✅ **已实现**：
- `CreateSessionParams` 接口和类中的 `isVpc?: boolean` 参数
- Session中的基础VPC属性：`isVpc`, `networkInterfaceIp`, `httpPort`
- 在 `agentbay.create()` 中设置 `request.vpcResource = params.isVpc || false`

❌ **缺失功能**：
- VPC相关的便捷方法
- VPC模式下的MCP tool调用机制
- 获取MCP tool list功能
- VPC session创建时自动获取工具列表

## 迁移方案

### 第一阶段：核心数据结构

#### Python

1. **扩展Session类** (`python/agentbay/session.py`)
```python
class Session:
    def __init__(self, agent_bay: "AgentBay", session_id: str):
        # ... 现有代码 ...
        # MCP tools available for this session
        self.mcp_tools = []  # List[McpTool]

    def is_vpc(self) -> bool:
        """Return whether this session uses VPC resources."""
        return self.is_vpc

    def network_interface_ip(self) -> str:
        """Return the network interface IP for VPC sessions."""
        return self.network_interface_ip

    def http_port(self) -> str:
        """Return the HTTP port for VPC sessions."""
        return self.http_port

    def find_server_for_tool(self, tool_name: str) -> str:
        """Find the server that provides the given tool."""
        for tool in self.mcp_tools:
            if tool.name == tool_name:
                return tool.server
        return ""
```

2. **创建McpTool数据类** (`python/agentbay/models/mcp_tool.py`)
```python
from dataclasses import dataclass
from typing import Dict, Any, Optional

@dataclass
class McpTool:
    name: str
    description: str
    input_schema: Dict[str, Any]
    server: str
    tool: str

    def get_name(self) -> str:
        return self.name

    def get_server(self) -> str:
        return self.server
```

3. **创建McpToolsResult类** (`python/agentbay/models/response.py`)
```python
from .api_response import ApiResponse
from .mcp_tool import McpTool
from typing import List

class McpToolsResult(ApiResponse):
    def __init__(self, request_id: str = "", tools: List[McpTool] = None):
        super().__init__(request_id)
        self.tools = tools or []
```

#### TypeScript

1. **扩展Session类** (`typescript/src/session.ts`)
```typescript
export interface McpTool {
  name: string;
  description: string;
  inputSchema: Record<string, any>;
  server: string;
  tool: string;
}

export interface McpToolsResult extends ApiResponse {
  tools: McpTool[];
}

export class Session {
  // ... 现有属性 ...
  // MCP tools available for this session
  public mcpTools: McpTool[] = [];

  // ... 现有构造函数 ...

  /**
   * Return whether this session uses VPC resources.
   */
  isVpcEnabled(): boolean {
    return this.isVpc;
  }

  /**
   * Return the network interface IP for VPC sessions.
   */
  getNetworkInterfaceIp(): string {
    return this.networkInterfaceIp;
  }

  /**
   * Return the HTTP port for VPC sessions.
   */
  getHttpPort(): string {
    return this.httpPort;
  }

  /**
   * Find the server that provides the given tool.
   */
  findServerForTool(toolName: string): string {
    for (const tool of this.mcpTools) {
      if (tool.name === toolName) {
        return tool.server;
      }
    }
    return "";
  }
}
```

### 第二阶段：ListMcpTools功能

#### Python

1. **在Session类中添加ListMcpTools方法** (`python/agentbay/session.py`)
```python
def list_mcp_tools(self, image_id: Optional[str] = None) -> McpToolsResult:
    """
    List MCP tools available for this session.
    
    Args:
        image_id: Optional image ID, defaults to session's image_id or "linux_latest"
    
    Returns:
        McpToolsResult: Result containing tools list and request ID
    """
    from agentbay.api.models import ListMcpToolsRequest
    from agentbay.models.response import McpToolsResult
    from agentbay.models.mcp_tool import McpTool
    import json
    
    # Use provided image_id, session's image_id, or default
    if image_id is None:
        image_id = getattr(self, 'image_id', '') or "linux_latest"
    
    request = ListMcpToolsRequest(
        authorization=f"Bearer {self.get_api_key()}",
        image_id=image_id
    )
    
    print("API Call: ListMcpTools")
    print(f"Request: ImageId={image_id}")
    
    response = self.get_client().list_mcp_tools(request)
    
    # Extract request ID
    request_id = extract_request_id(response)
    
    if response and response.body:
        print("Response from ListMcpTools:", response.body)
    
    # Parse the response data
    tools = []
    if response and response.body and response.body.data:
        # The Data field is a JSON string, so we need to unmarshal it
        try:
            tools_data = json.loads(response.body.data)
            for tool_data in tools_data:
                tool = McpTool(
                    name=tool_data.get('name', ''),
                    description=tool_data.get('description', ''),
                    input_schema=tool_data.get('inputSchema', {}),
                    server=tool_data.get('server', ''),
                    tool=tool_data.get('tool', '')
                )
                tools.append(tool)
        except json.JSONDecodeError as e:
            print(f"Error unmarshaling tools data: {e}")
    
    self.mcp_tools = tools  # Update the session's mcp_tools field
    
    return McpToolsResult(request_id=request_id, tools=tools)
```

#### TypeScript

1. **在Session类中添加ListMcpTools方法** (`typescript/src/session.ts`)
```typescript
import { ListMcpToolsRequest } from "./api/models";

/**
 * List MCP tools available for this session.
 * 
 * @param imageId Optional image ID, defaults to session's imageId or "linux_latest"
 * @returns McpToolsResult containing tools list and request ID
 */
async listMcpTools(imageId?: string): Promise<McpToolsResult> {
  // Use provided imageId, session's imageId, or default
  if (!imageId) {
    imageId = this.imageId || "linux_latest";
  }

  const request = new ListMcpToolsRequest({
    authorization: `Bearer ${this.getAPIKey()}`,
    imageId: imageId,
  });

  log("API Call: ListMcpTools");
  log(`Request: ImageId=${imageId}`);

  const response = await this.getClient().listMcpTools(request);

  // Extract request ID
  const requestId = extractRequestId(response) || "";

  if (response && response.body) {
    log("Response from ListMcpTools:", response.body);
  }

  // Parse the response data
  const tools: McpTool[] = [];
  if (response && response.body && response.body.data) {
    try {
      const toolsData = JSON.parse(response.body.data as string);
      for (const toolData of toolsData) {
        const tool: McpTool = {
          name: toolData.name || "",
          description: toolData.description || "",
          inputSchema: toolData.inputSchema || {},
          server: toolData.server || "",
          tool: toolData.tool || "",
        };
        tools.push(tool);
      }
    } catch (error) {
      logError(`Error unmarshaling tools data: ${error}`);
    }
  }

  this.mcpTools = tools; // Update the session's mcpTools field

  return {
    requestId,
    tools,
  };
}
```

### 第三阶段：VPC模式MCP工具调用

#### Python

1. **扩展BaseService类** (`python/agentbay/api/base_service.py`)
```python
import requests
import json
from typing import Dict, Any

class BaseService:
    # ... 现有代码 ...
    
    def _call_mcp_tool_vpc(self, tool_name: str, args_json: str, default_error_msg: str) -> OperationResult:
        """
        Handle VPC-based MCP tool calls using HTTP requests.
        
        Args:
            tool_name: Name of the tool to call
            args_json: JSON string of arguments
            default_error_msg: Default error message
            
        Returns:
            OperationResult: The response from the tool
        """
        print(f"API Call: CallMcpTool (VPC) - {tool_name}")
        print(f"Request: Args={args_json}")
        
        # Find server for this tool
        server = self.session.find_server_for_tool(tool_name)
        if not server:
            return OperationResult(
                request_id="",
                success=False,
                error_message=f"server not found for tool: {tool_name}"
            )
        
        # Construct VPC URL with query parameters
        base_url = f"http://{self.session.network_interface_ip()}:{self.session.http_port()}/callTool"
        
        # Prepare query parameters
        params = {
            'server': server,
            'tool': tool_name,
            'args': args_json,
            'apiKey': self.session.get_api_key()
        }
        
        # Set headers
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        try:
            # Send HTTP request
            response = requests.get(base_url, params=params, headers=headers, timeout=30)
            response.raise_for_status()
            
            # Parse response
            response_data = response.json()
            print(f"Response from VPC CallMcpTool - {tool_name}:", response_data)
            
            # Extract the actual result from the nested VPC response structure
            actual_result = None
            if isinstance(response_data.get("data"), str):
                try:
                    data_map = json.loads(response_data["data"])
                    if "result" in data_map:
                        actual_result = data_map["result"]
                except json.JSONDecodeError:
                    pass
            elif isinstance(response_data.get("data"), dict):
                actual_result = response_data["data"]
            
            if actual_result is None:
                actual_result = response_data
            
            return OperationResult(
                request_id="",  # VPC requests don't have traditional request IDs
                success=True,
                data=actual_result
            )
            
        except requests.RequestException as e:
            print(f"Error calling VPC CallMcpTool - {tool_name}: {e}")
            return OperationResult(
                request_id="",
                success=False,
                error_message=f"failed to call VPC {tool_name}: {e}"
            )
    
    def _call_mcp_tool(self, name: str, args: Dict[str, Any]) -> OperationResult:
        """
        Internal helper to call MCP tool and handle errors.
        
        Args:
            name: The name of the tool to call.
            args: The arguments to pass to the tool.
            
        Returns:
            OperationResult: The response from the tool with request ID.
        """
        try:
            args_json = json.dumps(args, ensure_ascii=False)
            
            # Check if this is a VPC session
            if self.session.is_vpc():
                return self._call_mcp_tool_vpc(name, args_json, f"Failed to call {name}")
            
            # Non-VPC mode: use traditional API call
            # ... 现有的API调用代码 ...
```

#### TypeScript

1. **扩展各个模块类** (例如：`typescript/src/command/command.ts`)
```typescript
/**
 * Helper method to call MCP tools and handle both VPC and non-VPC scenarios
 */
private async callMcpTool(
  toolName: string,
  args: Record<string, any>,
  defaultErrorMsg: string
): Promise<CallMcpToolResult> {
  try {
    const argsJSON = JSON.stringify(args);
    
    // Check if this is a VPC session
    if (this.session.isVpcEnabled()) {
      return await this.callMcpToolVPC(toolName, argsJSON, defaultErrorMsg);
    }

    // Non-VPC mode: use traditional API call
    const callToolRequest = new CallMcpToolRequest({
      authorization: `Bearer ${this.session.getAPIKey()}`,
      sessionId: this.session.getSessionId(),
      name: toolName,
      args: argsJSON,
    });

    // ... 现有的API调用代码 ...
  } catch (error) {
    // ... 错误处理 ...
  }
}

/**
 * Handle VPC-based MCP tool calls using HTTP requests.
 */
private async callMcpToolVPC(
  toolName: string,
  argsJSON: string,
  defaultErrorMsg: string
): Promise<CallMcpToolResult> {
  log(`API Call: CallMcpTool (VPC) - ${toolName}`);
  log(`Request: Args=${argsJSON}`);

  // Find server for this tool
  const server = this.session.findServerForTool(toolName);
  if (!server) {
    throw new Error(`server not found for tool: ${toolName}`);
  }

  // Construct VPC URL with query parameters
  const baseURL = `http://${this.session.getNetworkInterfaceIp()}:${this.session.getHttpPort()}/callTool`;

  // Prepare query parameters
  const params = new URLSearchParams({
    server: server,
    tool: toolName,
    args: argsJSON,
    apiKey: this.session.getAPIKey()
  });

  const url = `${baseURL}?${params.toString()}`;

  try {
    // Send HTTP request
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      signal: AbortSignal.timeout(30000) // 30 second timeout
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    // Parse response
    const responseData = await response.json();
    log(`Response from VPC CallMcpTool - ${toolName}:`, responseData);

    // Create result object for VPC response
    const result: CallMcpToolResult = {
      data: responseData,
      statusCode: response.status,
      isError: false,
      requestId: "", // VPC requests don't have traditional request IDs
    };

    // Extract the actual result from the nested VPC response structure
    let actualResult: any = responseData;
    if (typeof responseData.data === 'string') {
      try {
        const dataMap = JSON.parse(responseData.data);
        if (dataMap.result) {
          actualResult = dataMap.result;
        }
      } catch (error) {
        // Keep original responseData if parsing fails
      }
    } else if (responseData.data && typeof responseData.data === 'object') {
      actualResult = responseData.data;
    }

    result.data = actualResult;
    return result;

  } catch (error) {
    logError(`Error calling VPC CallMcpTool - ${toolName}:`, error);
    throw new Error(`failed to call VPC ${toolName}: ${error}`);
  }
}
```

### 第四阶段：Session创建时自动获取工具列表

#### Python

在 `python/agentbay/agentbay.py` 的 `create` 方法中添加：
```python
# Create Session object
session = Session(self, session_id)
if resource_url is not None:
    session.resource_url = resource_url

# Set VPC-related information from response
session.is_vpc = params.is_vpc
if data.get("NetworkInterfaceIp"):
    session.network_interface_ip = data["NetworkInterfaceIp"]
if data.get("HttpPort"):
    session.http_port = data["HttpPort"]

# Store image_id used for this session
session.image_id = params.image_id

with self._lock:
    self._sessions[session_id] = session

# For VPC sessions, automatically fetch MCP tools information
if params.is_vpc:
    print("VPC session detected, automatically fetching MCP tools...")
    try:
        tools_result = session.list_mcp_tools()
        print(f"Successfully fetched {len(tools_result.tools)} MCP tools for VPC session (RequestID: {tools_result.request_id})")
    except Exception as e:
        print(f"Warning: Failed to fetch MCP tools for VPC session: {e}")
        # Continue with session creation even if tools fetch fails
```

#### TypeScript

在 `typescript/src/agent-bay.ts` 的 `create` 方法中添加：
```typescript
// Create Session object
const session = new Session(this, sessionId);
if (resourceUrl) {
  session.resourceUrl = resourceUrl;
}

// Set VPC-related information from response
session.isVpc = params.isVpc || false;
if (data.NetworkInterfaceIp) {
  session.networkInterfaceIp = data.NetworkInterfaceIp;
}
if (data.HttpPort) {
  session.httpPort = data.HttpPort;
}

// Store imageId used for this session
session.imageId = params.imageId;

this.sessions.set(sessionId, session);

// For VPC sessions, automatically fetch MCP tools information
if (params.isVpc) {
  log("VPC session detected, automatically fetching MCP tools...");
  try {
    const toolsResult = await session.listMcpTools();
    log(`Successfully fetched ${toolsResult.tools.length} MCP tools for VPC session (RequestID: ${toolsResult.requestId})`);
  } catch (error) {
    logError(`Warning: Failed to fetch MCP tools for VPC session: ${error}`);
    // Continue with session creation even if tools fetch fails
  }
}
```

## 测试方案

### 1. 单元测试

#### Python测试 (`python/tests/unit/test_vpc_session.py`)
```python
import pytest
from unittest.mock import Mock, patch
from agentbay import AgentBay, CreateSessionParams
from agentbay.models.mcp_tool import McpTool

class TestVPCSession:
    def test_vpc_session_creation(self):
        """Test VPC session creation with proper parameters."""
        # ... 测试代码 ...
    
    def test_list_mcp_tools(self):
        """Test listing MCP tools for VPC session."""
        # ... 测试代码 ...
    
    def test_vpc_tool_calling(self):
        """Test calling MCP tools in VPC mode."""
        # ... 测试代码 ...
```

#### TypeScript测试 (`typescript/tests/unit/vpc-session.test.ts`)
```typescript
import { AgentBay, CreateSessionParams } from "../src";

describe("VPC Session", () => {
  test("should create VPC session with proper parameters", async () => {
    // ... 测试代码 ...
  });
  
  test("should list MCP tools for VPC session", async () => {
    // ... 测试代码 ...
  });
  
  test("should call MCP tools in VPC mode", async () => {
    // ... 测试代码 ...
  });
});
```

### 2. 集成测试

基于现有的 `golang/tests/pkg/integration/vpc_session_integration_test.go`，创建对应的Python和TypeScript集成测试。

#### Python集成测试 (`python/tests/integration/test_vpc_session_integration.py`)
```python
import pytest
from agentbay import AgentBay, CreateSessionParams

class TestVPCSessionIntegration:
    @pytest.mark.integration
    def test_vpc_session_basic_tools(self):
        """Test VPC session creation and basic tool functionality."""
        # 创建VPC session
        # 测试Command和FileSystem功能
        # 验证工具列表获取
        # ... 测试代码 ...
```

#### TypeScript集成测试 (`typescript/tests/integration/vpc-session-integration.test.ts`)
```typescript
import { AgentBay, CreateSessionParams } from "../../src";

describe("VPC Session Integration", () => {
  test("should support VPC session basic tools", async () => {
    // 创建VPC session
    // 测试Command和FileSystem功能
    // 验证工具列表获取
    // ... 测试代码 ...
  });
});
```

## 实施计划

### 第一周：核心数据结构
- [ ] Python: 扩展Session类，添加VPC相关方法
- [ ] Python: 创建McpTool和McpToolsResult数据类
- [ ] TypeScript: 扩展Session类，添加VPC相关方法和接口
- [ ] 编写基础单元测试

### 第二周：ListMcpTools功能
- [ ] Python: 实现Session.list_mcp_tools()方法
- [ ] TypeScript: 实现Session.listMcpTools()方法
- [ ] 确保API模型包含ListMcpToolsRequest和相关响应类型
- [ ] 编写功能测试

### 第三周：VPC模式MCP工具调用
- [ ] Python: 扩展BaseService，实现VPC模式调用
- [ ] TypeScript: 在各模块中实现VPC模式调用
- [ ] 处理HTTP请求和响应解析
- [ ] 编写VPC调用测试

### 第四周：集成和优化
- [ ] 在session创建时自动获取工具列表
- [ ] 编写完整的集成测试
- [ ] 性能优化和错误处理完善
- [ ] 文档更新

### 第五周：测试和发布
- [ ] 全面测试（单元测试、集成测试）
- [ ] 代码审查和质量检查
- [ ] 更新API文档和示例
- [ ] 准备发布

## 风险评估与缓解

### 风险点
1. **HTTP请求超时**: VPC环境下的网络延迟可能导致请求超时
2. **工具服务器映射**: 工具名称与服务器的映射关系可能出错
3. **响应格式差异**: VPC模式的响应格式可能与标准API不同
4. **向后兼容性**: 现有代码的兼容性问题

### 缓解措施
1. **设置合理的超时时间**: 默认30秒，可配置
2. **完善错误处理**: 详细的错误日志和异常处理
3. **充分测试**: 覆盖各种场景的测试用例
4. **渐进式部署**: 通过特性开关控制新功能启用

## 结论

本迁移方案提供了将Golang中的VPC功能完整迁移到Python和TypeScript SDK的详细路径。通过分阶段实施，可以确保功能的完整性和稳定性，同时保持向后兼容性。预计整个迁移过程需要5周时间完成。 