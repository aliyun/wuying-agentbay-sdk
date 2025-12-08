# Command API 修改方案

## 修改概述

根据新的接口定义，需要修改 `execute_command` 方法的输入参数和返回值解析逻辑。

## 修改内容

### 1. 输入参数修改

**修改文件：**
- `python/agentbay/_sync/command.py`
- `python/agentbay/_async/command.py`

**修改点：**
- 方法签名增加参数：`cwd: Optional[str] = None`, `envs: Optional[Dict[str, str]] = None`
- 保持参数名为 `command`（不变）
- 添加 `cwd`、`envs` 参数到请求参数中（如果提供）
- 保持超时时间默认值为 60s（60000ms），不做限制修改
- 注意：`shell` 是工具名称，不是参数

### 2. CommandResult 模型修改

**修改文件：**
- `python/agentbay/_common/models/command.py`

**修改点：**
- 添加新字段：`exit_code: int = 0`, `stdout: str = ""`, `stderr: str = ""`
- 保留原有字段：`success`, `output`, `error_message`（向后兼容）

### 3. 返回值解析修改

**修改文件：**
- `python/agentbay/_sync/command.py`
- `python/agentbay/_async/command.py`

**修改点：**
- 解析返回的 JSON 字符串（`result.data`）
- 提取字段：
  - `stdout` -> `result.stdout`
  - `stderr` -> `result.stderr`
  - `errorCode` -> `result.exit_code`
  - 根据 `errorCode` 判断 `success`（0 为成功，非 0 为失败）
  - `output` 保持为原有格式（向后兼容，可以是 `stdout` 或 `stderr`）

### 4. 返回值格式说明

**新格式返回：**
```python
result.success      # bool: 根据 exit_code 判断（0 为 True，非 0 为 False）
result.exit_code    # int: 命令退出码
result.stdout       # str: 标准输出
result.stderr       # str: 标准错误
result.output       # str: 保持向后兼容（优先 stdout，如果为空则用 stderr）
```

## 修改逻辑

1. **参数处理**：
   - 保持参数名为 `command`（不变）
   - 添加 `cwd`、`envs` 可选参数到方法签名
   - 构建请求参数时，只包含非 None 的参数（`command`、`timeout_ms` 必传，`cwd`、`envs` 可选）
2. **超时时间**：保持默认值 60s（60000ms），不做限制修改
3. **响应解析**：解析返回的 JSON 字符串（`result.data`），提取 `stdout`、`stderr`、`errorCode`、`traceId`
4. **结果构建**：根据解析结果构建 `CommandResult` 对象，设置所有新字段
5. **向后兼容**：保持 `output` 字段，确保旧代码仍可使用

## 注意事项

- 保持向后兼容性：`output` 字段仍然可用
- JSON 解析需要处理异常情况（解析失败时回退到原有逻辑）
- `success` 字段的语义保持不变（根据 `exit_code` 判断）
- 需要更新相关测试用例

