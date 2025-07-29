# VPC 功能迁移方案：从 Golang 到 Python 和 TypeScript

## 概述

本文档详细描述了如何将 Golang 中的 VPC（Virtual Private Cloud）相关功能迁移到 Python 和 TypeScript SDK 中。主要包括两个方面：

1. **代码逻辑迁移**：将 VPC 场景下的 MCP 工具调用逻辑从 Golang 迁移到 Python 和 TypeScript
2. **测试用例迁移**：根据实际的 VPC 环境工具可用性更新测试用例

## 当前状态分析

### Golang 中已实现的 VPC 功能

1. **VPC 工具验证机制**：每个模块都有 `isToolAvailableInVPC` 方法来验证工具在 VPC 环境中的可用性
2. **VPC 调用逻辑**：在 `callMcpToolVPC` 方法中实现了 VPC 环境下的 HTTP 调用
3. **测试用例更新**：根据实际的 tool list 更新了测试用例，跳过不可用的工具测试

### Python 和 TypeScript 中的现状

1. **基础 VPC 支持**：两种语言都已支持 VPC 会话创建（`isVpc` 参数）
2. **缺少 VPC 调用逻辑**：目前的 `_call_mcp_tool`（Python）和 `callMcpTool`（TypeScript）方法只支持标准 API 调用
3. **缺少 VPC 测试**：没有针对 VPC 环境的专门测试用例

## 迁移计划

### 阶段 1：代码逻辑迁移

#### 1.1 Python 迁移

**目标文件：**
- `python/agentbay/api/base_service.py`
- `python/agentbay/code/code.py`
- `python/agentbay/oss/oss.py`
- `python/agentbay/filesystem/filesystem.py`
- `python/agentbay/command/command.py`
- 其他使用 `_call_mcp_tool` 的模块

**修改内容：**

1. **更新 BaseService 类**
   ```python
   # 在 python/agentbay/api/base_service.py 中添加
   
   import requests
   import urllib.parse
   
   def _call_mcp_tool_vpc(self, name: str, args: Dict[str, Any]) -> OperationResult:
       """
       Internal helper to call MCP tool in VPC environment.
       """
       try:
           args_json = json.dumps(args, ensure_ascii=False)
           
           # Find server for this tool
           server = self.session.find_server_for_tool(name)
           if not server:
               raise AgentBayError(f"server not found for tool: {name}")
           
           # Validate tool availability in VPC
           if not self._is_tool_available_in_vpc(name):
               raise AgentBayError(f"tool {name} is not available in VPC environment")
           
           # Construct VPC URL
           base_url = f"http://{self.session.network_interface_ip}:{self.session.http_port}/callTool"
           
           # Prepare query parameters
           params = {
               'server': server,
               'tool': name,
               'args': args_json,
               'apiKey': self.session.get_api_key()
           }
           
           # Send HTTP request
           response = requests.get(base_url, params=params, timeout=30)
           response.raise_for_status()
           
           response_data = response.json()
           
           # Process VPC response (similar to Golang logic)
           # ... (详细实现参考 Golang 代码)
           
       except Exception as e:
           # Error handling
           pass
   
   def _is_tool_available_in_vpc(self, tool_name: str) -> bool:
       """
       Check if a tool is available in VPC environment.
       Subclasses should override this method.
       """
       return True  # Default implementation
   
   def _call_mcp_tool(self, name: str, args: Dict[str, Any]) -> OperationResult:
       """
       Updated to support both VPC and non-VPC calls.
       """
       if self.session.is_vpc:
           return self._call_mcp_tool_vpc(name, args)
       else:
           # Existing non-VPC implementation
           return self._call_mcp_tool_standard(name, args)
   ```

2. **为每个模块添加工具验证**
   ```python
   # 在各个模块中重写 _is_tool_available_in_vpc 方法
   
   # code/code.py
   def _is_tool_available_in_vpc(self, tool_name: str) -> bool:
       vpc_available_tools = {
           "run_code": False,  # 根据 tool list，run_code 不可用
       }
       return vpc_available_tools.get(tool_name, False)
   
   # filesystem/filesystem.py
   def _is_tool_available_in_vpc(self, tool_name: str) -> bool:
       vpc_available_tools = {
           "create_directory": True,
           "edit_file": True,
           "get_file_info": True,
           "read_file": True,
           "read_multiple_files": True,
           "list_directory": True,
           "move_file": True,
           "search_files": True,
           "write_file": True,
       }
       return vpc_available_tools.get(tool_name, False)
   
   # command/command.py
   def _is_tool_available_in_vpc(self, tool_name: str) -> bool:
       vpc_available_tools = {
           "shell": True,
       }
       return vpc_available_tools.get(tool_name, False)
   
   # oss/oss.py
   def _is_tool_available_in_vpc(self, tool_name: str) -> bool:
       vpc_available_tools = {
           "oss_env_init": False,      # 根据 tool list，OSS 工具不可用
           "oss_upload": False,
           "oss_upload_annon": False,
           "oss_download": False,
           "oss_download_annon": False,
       }
       return vpc_available_tools.get(tool_name, False)
   ```

3. **更新 Session 类**
   ```python
   # 在 python/agentbay/session.py 中添加
   
   def find_server_for_tool(self, tool_name: str) -> str:
       """
       Find the server that provides the given tool.
       """
       for tool in self.mcp_tools:
           if tool.get('name') == tool_name:
               return tool.get('server', '')
       return ''
   ```

#### 1.2 TypeScript 迁移

**目标文件：**
- `typescript/src/code/code.ts`
- `typescript/src/oss/oss.ts`
- `typescript/src/filesystem/filesystem.ts`
- `typescript/src/command/command.ts`
- 其他使用 `callMcpTool` 的模块

**修改内容：**

1. **更新各个模块的 callMcpTool 方法**
   ```typescript
   // 在各个模块中更新 callMcpTool 方法
   
   private async callMcpTool(
     toolName: string,
     args: Record<string, any>,
     defaultErrorMsg: string
   ): Promise<CallMcpToolResult> {
     // Check if this is a VPC session
     if (this.session.isVpc) {
       return this.callMcpToolVPC(toolName, args, defaultErrorMsg);
     }
     
     // Non-VPC mode: use existing implementation
     return this.callMcpToolStandard(toolName, args, defaultErrorMsg);
   }
   
   private async callMcpToolVPC(
     toolName: string,
     args: Record<string, any>,
     defaultErrorMsg: string
   ): Promise<CallMcpToolResult> {
     try {
       const argsJSON = JSON.stringify(args);
       
       // Find server for this tool
       const server = this.session.findServerForTool(toolName);
       if (!server) {
         throw new Error(`server not found for tool: ${toolName}`);
       }
       
       // Validate tool availability in VPC
       if (!this.isToolAvailableInVPC(toolName)) {
         throw new Error(`tool ${toolName} is not available in VPC environment`);
       }
       
       // Construct VPC URL
       const baseURL = `http://${this.session.networkInterfaceIp}:${this.session.httpPort}/callTool`;
       
       // Prepare query parameters
       const params = new URLSearchParams({
         server,
         tool: toolName,
         args: argsJSON,
         apiKey: this.session.getAPIKey()
       });
       
       // Send HTTP request
       const response = await fetch(`${baseURL}?${params}`, {
         method: 'GET',
         headers: {
           'Content-Type': 'application/x-www-form-urlencoded'
         },
         signal: AbortSignal.timeout(30000)
       });
       
       if (!response.ok) {
         throw new Error(`VPC call failed: ${response.statusText}`);
       }
       
       const responseData = await response.json();
       
       // Process VPC response (similar to Golang logic)
       // ... (详细实现参考 Golang 代码)
       
     } catch (error) {
       // Error handling
       throw new APIError(`Failed to call VPC ${toolName}: ${error.message}`);
     }
   }
   
   private isToolAvailableInVPC(toolName: string): boolean {
     // Each module should override this method
     return true;
   }
   ```

2. **为每个模块添加工具验证**
   ```typescript
   // code/code.ts
   private isToolAvailableInVPC(toolName: string): boolean {
     const vpcAvailableTools: Record<string, boolean> = {
       run_code: false, // 根据 tool list，run_code 不可用
     };
     return vpcAvailableTools[toolName] || false;
   }
   
   // filesystem/filesystem.ts
   private isToolAvailableInVPC(toolName: string): boolean {
     const vpcAvailableTools: Record<string, boolean> = {
       create_directory: true,
       edit_file: true,
       get_file_info: true,
       read_file: true,
       read_multiple_files: true,
       list_directory: true,
       move_file: true,
       search_files: true,
       write_file: true,
     };
     return vpcAvailableTools[toolName] || false;
   }
   
   // command/command.ts
   private isToolAvailableInVPC(toolName: string): boolean {
     const vpcAvailableTools: Record<string, boolean> = {
       shell: true,
     };
     return vpcAvailableTools[toolName] || false;
   }
   
   // oss/oss.ts
   private isToolAvailableInVPC(toolName: string): boolean {
     const vpcAvailableTools: Record<string, boolean> = {
       oss_env_init: false,      // 根据 tool list，OSS 工具不可用
       oss_upload: false,
       oss_upload_annon: false,
       oss_download: false,
       oss_download_annon: false,
     };
     return vpcAvailableTools[toolName] || false;
   }
   ```

3. **更新 Session 类**
   ```typescript
   // 在 typescript/src/session.ts 中添加
   
   public findServerForTool(toolName: string): string {
     for (const tool of this.mcpTools) {
       if (tool.name === toolName) {
         return tool.server || '';
       }
     }
     return '';
   }
   ```

### 阶段 2：测试用例迁移

#### 2.1 Python 测试迁移

**创建新文件：** `python/tests/integration/test_vpc_session_integration.py`

**内容结构：**
```python
import pytest
from agentbay import AgentBay, CreateSessionParams

class TestVpcSessionIntegration:
    """VPC session integration tests based on actual tool availability."""
    
    def test_vpc_session_basic_tools(self):
        """Test VPC session creation and basic available tools."""
        # 只测试 FileSystem 和 Command 模块
        pass
    
    @pytest.mark.skip(reason="Code module (run_code) is not available in VPC environment according to tool list")
    def test_vpc_session_code_operations(self):
        """Code operations are not available in VPC."""
        pass
    
    @pytest.mark.skip(reason="UI module is not available in VPC environment according to tool list")
    def test_vpc_session_ui_operations(self):
        """UI operations are not available in VPC."""
        pass
    
    @pytest.mark.skip(reason="Application module is not available in VPC environment according to tool list")
    def test_vpc_session_application_operations(self):
        """Application operations are not available in VPC."""
        pass
    
    @pytest.mark.skip(reason="Window module is not available in VPC environment according to tool list")
    def test_vpc_session_window_operations(self):
        """Window operations are not available in VPC."""
        pass
    
    @pytest.mark.skip(reason="OSS module is not available in VPC environment according to tool list")
    def test_vpc_session_oss_operations(self):
        """OSS operations are not available in VPC."""
        pass
    
    def test_vpc_session_system_tools(self):
        """Test system-level tools available in VPC environment."""
        # 测试 get_resource, system_screenshot, release_resource
        pass
    
    def test_vpc_session_browser_tools(self):
        """Test browser-related tools available in VPC environment."""
        # 测试 cdp, pageuse-mcp-server, playwright 工具
        pass
    
    def test_vpc_session_comprehensive(self):
        """Test all VPC-enabled modules in a single session."""
        # 只测试可用的模块：FileSystem, Command, SystemTools
        pass
```

#### 2.2 TypeScript 测试迁移

**创建新文件：** `typescript/tests/integration/vpc-session-integration.test.ts`

**内容结构：**
```typescript
import { AgentBay, CreateSessionParams } from '../../src';

describe('VPC Session Integration Tests', () => {
  describe('Basic VPC Tools', () => {
    it('should create VPC session and test basic available tools', async () => {
      // 只测试 FileSystem 和 Command 模块
    });
  });

  describe('Unavailable Tools', () => {
    it.skip('Code operations are not available in VPC', () => {
      // Code module (run_code) is not available in VPC environment according to tool list
    });

    it.skip('UI operations are not available in VPC', () => {
      // UI module is not available in VPC environment according to tool list
    });

    it.skip('Application operations are not available in VPC', () => {
      // Application module is not available in VPC environment according to tool list
    });

    it.skip('Window operations are not available in VPC', () => {
      // Window module is not available in VPC environment according to tool list
    });

    it.skip('OSS operations are not available in VPC', () => {
      // OSS module is not available in VPC environment according to tool list
    });
  });

  describe('Available VPC Tools', () => {
    it('should test system-level tools', async () => {
      // 测试 get_resource, system_screenshot, release_resource
    });

    it('should test browser-related tools', async () => {
      // 测试 cdp, pageuse-mcp-server, playwright 工具
    });
  });

  describe('Comprehensive VPC Test', () => {
    it('should test all VPC-enabled modules', async () => {
      // 只测试可用的模块：FileSystem, Command, SystemTools
    });
  });
});
```

### 阶段 3：工具可用性配置

根据实际的 tool list，各模块中工具的可用性配置如下：

#### 可用的工具和服务器：

1. **mcp-server**
   - `get_resource`
   - `system_screenshot`
   - `release_resource`

2. **cdp**
   - `stopChrome`
   - `startChromeByCdp`

3. **filesystem**
   - `create_directory`
   - `edit_file`
   - `get_file_info`
   - `read_file`
   - `read_multiple_files`
   - `list_directory`
   - `move_file`
   - `search_files`
   - `write_file`

4. **pageuse-mcp-server**
   - `page_use_navigate`
   - `page_use_act`
   - `page_use_observe`
   - `page_use_extract`
   - `page_use_screenshot`

5. **playwright**
   - 多个浏览器自动化工具

6. **shell**
   - `shell`

#### 不可用的工具：

1. **Code 模块**：`run_code` 工具不在 tool list 中
2. **OSS 模块**：所有 OSS 相关工具不在 tool list 中
3. **UI 模块**：UI 相关工具不在 tool list 中
4. **Application 模块**：应用管理工具不在 tool list 中
5. **Window 模块**：窗口管理工具不在 tool list 中

## 实施步骤

### 第一步：准备工作
1. 备份现有代码
2. 创建特性分支
3. 设置开发环境

### 第二步：代码迁移
1. 按照上述方案修改 Python 代码
2. 按照上述方案修改 TypeScript 代码
3. 运行单元测试确保现有功能不受影响

### 第三步：测试迁移
1. 创建 VPC 集成测试文件
2. 实现测试用例
3. 验证测试用例的正确性

### 第四步：验证和测试
1. 在 VPC 环境中运行测试
2. 验证工具可用性检查是否正确
3. 确保错误处理机制正常工作

### 第五步：文档更新
1. 更新 API 文档
2. 更新使用示例
3. 添加 VPC 使用说明

## 注意事项

1. **向后兼容性**：确保修改不影响现有的非 VPC 功能
2. **错误处理**：为 VPC 环境添加适当的错误处理和日志记录
3. **性能考虑**：VPC 调用可能有不同的延迟特性
4. **测试覆盖**：确保新增的 VPC 功能有充分的测试覆盖
5. **配置管理**：工具可用性配置应该易于维护和更新

## 风险评估

### 高风险
- 网络调用的稳定性和错误处理
- VPC 环境配置的复杂性

### 中风险
- 工具可用性配置的准确性
- 现有功能的兼容性

### 低风险
- 测试用例的迁移
- 文档更新

## 总结

这个迁移方案确保了 Python 和 TypeScript SDK 能够与 Golang SDK 保持功能一致，同时根据实际的 VPC 环境工具可用性进行了适当的调整。通过分阶段实施，可以最小化风险并确保迁移的成功。 